import allure
import pytest

from assertcheck.tp.TpOrderCancelCheck import TpOrderCancelCheck
from libs import utils
from libs.BaseTestToC import BaseTestToC
from libs.decorator import order_create


@allure.feature("订单-toc")
@allure.story("取消订单")
class TestTpOrderCancel(BaseTestToC):
    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestTpOrderCancel", "test_order_cancel_succeed", "tp"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("正向case: {case_name}")
    @pytest.mark.usefixtures("order_create")
    def test_order_cancel_succeed(self, args, case_name):
        args["param"]["orderNo"] = self.tp_sql.exeCute(args["sql"])["parent_order_no"]
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderCancelCheck.check(self, args["param"])

    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestTpOrderCancel", "test_order_cancel_failed", "tp"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("反向: case: {case_name}")
    def test_order_cancel_failed(self, args, case_name):
        args["param"]["orderNo"] = self.tp_sql.exeCute(args["sql"])["parent_order_no"]
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderCancelCheck.fail_code_check(self, args["expect"])