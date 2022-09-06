import allure
import pytest

from assertcheck.performance.TpOrderPerformanceStartCheck import TpOrderPerformanceStartCheck
from libs import utils
from libs.BaseTestToB import BaseTestToB
from libs.decorator import order_pay


@allure.feature("履约")
@allure.story("履约开始")
class TestPerformanceServiceStart(BaseTestToB):
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestPerformanceServiceStart", "test_performance_service_start",
                                             "performance"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    @pytest.mark.usefixtures("order_pay")
    def test_performance_service_start(self, args, case_name):
        db_result = self.performance_sql.exeCute(args["sql"])
        self.log.debug(db_result)
        args["param"]["orderNo"], args["param"]["voucherCode"] = db_result["order_no"], db_result["voucher_no"]
        args["param"]["serviceNo"] = db_result["service_no"]
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderPerformanceStartCheck.check(self, args["param"])
