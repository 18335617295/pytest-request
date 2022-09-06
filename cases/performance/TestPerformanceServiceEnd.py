import allure
import pytest

from assertcheck.performance.PerformanceServiceEndCheck import PerformanceServiceEndCheck
from libs import utils
from libs.BaseTestToB import BaseTestToB
from libs.decorator import performance_start


@allure.feature("履约")
@allure.story("履约结束")
class TestPerformanceServiceEnd(BaseTestToB):
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestPerformanceServiceEnd", "test_performance_service_end",
                                             "performance"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    @pytest.mark.usefixtures("performance_start")
    def test_performance_service_end(self, args, case_name):
        db_result = self.performance_sql.exeCute(args["sql"])
        args["param"]["orderNo"], args["param"]["voucherCode"] = db_result["order_no"], db_result["voucher_no"]
        args["param"]["serviceNo"] = db_result["service_no"]
        self.result = self.request.json_post(self.api, args["param"])
        PerformanceServiceEndCheck.check(self, args["param"])
