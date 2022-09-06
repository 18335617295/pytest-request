import allure
import pytest

from assertcheck.tp.TpOrderListCheck import TpOrderListCheck
from libs import utils
from libs.BaseTestToC import BaseTestToC


@allure.feature("订单-toc")
@allure.story("订单列表")
class TestTpOrderList(BaseTestToC):
    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestTpOrderList", "test_order_list_succeed", "tp"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_order_list_succeed(self, args, case_name):
        self.result = self.request.get(self.api, args["param"])
        TpOrderListCheck.check(self, args)
