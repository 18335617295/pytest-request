import allure
import pytest

from libs import utils
from libs.BaseTestToB import BaseTestToB
from libs.decorator import order_pay


@allure.feature("履约")
@allure.story("履约校验核销码")
class TestPerformanceServiceCodeCheck(BaseTestToB):
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestPerformanceServiceCodeCheck", "test_performance_service_code_check",
                                             "performance"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    @pytest.mark.usefixtures("order_pay")
    def test_performance_service_code_check(self, args, case_name):
        db_result = self.performance_sql.exeCute(args["sql"])
        if not args["param"]["voucherCode"]:
            args["param"]["orderNo"], args["param"]["voucherCode"] = db_result["order_no"], db_result["voucher_no"]
        else:
            args["param"]["orderNo"] = db_result["order_no"]
        self.result = self.request.json_post(self.api, args["param"])
        assert self.result["code"] in [1, 2002]
