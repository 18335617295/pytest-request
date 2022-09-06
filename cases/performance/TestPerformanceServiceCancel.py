import allure
import pytest

from libs import utils
from libs.BaseTestToB import BaseTestToB
from libs.decorator import order_pay


@allure.feature("履约")
@allure.story("saas取消服务单")
class TestPerformanceServiceCancel(BaseTestToB):
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestPerformanceServiceCancel", "test_performance_service_cancel",
                                             "performance"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    @pytest.mark.usefixtures("order_pay")
    def test_performance_service_cancel(self, args, case_name):
        db_result = self.performance_sql.exeCute(args["sql"])
        args["param"]["orderNo"] = db_result["order_no"]
        self.log.debug(args["param"])
        self.result = self.request.json_post(self.api, args["param"])
        assert self.result["code"] == 1
