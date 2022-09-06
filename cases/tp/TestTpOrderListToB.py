import allure
import pytest

from assertcheck.tp.TpOrderListToBCheck import TpOrderListToBCheck
from libs import utils
from libs.BaseTestToB import BaseTestToB


@allure.feature("订单-tob")
@allure.story("订单列表")
class TestTpOrderListToB(BaseTestToB):
    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestTpOrderListToB", "test_order_list_succeed", "tp"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_order_list_succeed(self, args, case_name):
        self.result = self.request.get(self.api, args["param"])
        TpOrderListToBCheck.check(self, args["param"])
