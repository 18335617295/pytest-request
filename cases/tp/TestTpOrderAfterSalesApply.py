import allure
import pytest

from assertcheck.tp.TpOrderAfterSalesApplyCheck import TpOrderAfterSalesApplyCheck
from libs.BaseTestToC import BaseTestToC
from libs.decorator import after_sales_apply


@allure.feature("订单-toc")
@allure.story("退款单申请申请")
class TestTpOrderAfterSalesApply(BaseTestToC):
    @pytest.mark.parametrize("args, case_name", after_sales_apply())
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_order_after_sales_apply(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"], timeout=10)
        TpOrderAfterSalesApplyCheck.check(self, args["param"])
