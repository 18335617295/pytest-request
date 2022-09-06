import allure
import pytest

from assertcheck.tp.TpOrderRefundRenderCheck import TpOrderRefundRenderCheck
from libs import utils
from libs.BaseTestToC import BaseTestToC


@allure.feature("订单-toc")
@allure.story("退款单申请渲染")
class TestTpOrderRefundRender(BaseTestToC):
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestTpOrderRefundRender", "test_order_refund_render", "tp"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_order_refund_render(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderRefundRenderCheck.check(self, args["param"])

