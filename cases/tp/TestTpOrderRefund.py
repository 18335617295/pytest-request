import allure
import pytest

from assertcheck.tp.TpOrderRefundCheck import TpOrderRefundCheck
from libs import utils
from libs.BaseTestToC import BaseTestToC
from libs.decorator import order_pay


@allure.feature("订单-toc")
@allure.story("订单退款")
@pytest.mark.skip(reason="接口废弃")
class TestTpOrderRefund(BaseTestToC):
    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestTpOrderRefund", "test_order_refund_succeed", "tp"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("正向case: {case_name}")
    @pytest.mark.usefixtures("order_pay")
    def test_order_refund_succeed(self, args, case_name):
        args["param"]["orderNo"] = self.tp_sql.exeCute(args["sql"])["order_no"]
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderRefundCheck.check(self, args["param"])

    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestTpOrderRefund", "test_order_refund_fail", "tp"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("反向case: {case_name}")
    def test_order_refund_fail(self, args, case_name):
        args["param"]["orderNo"] = self.tp_sql.exeCute(args["sql"])["order_no"]
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderRefundCheck.fail_code_check(self, args["expect"])
