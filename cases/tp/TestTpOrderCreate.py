import allure
import pytest

from assertcheck.tp.TpOrderCreateCheck import TpOrderCreateCheck
from libs.BaseTestToC import BaseTestToC
from libs import utils


@allure.feature("订单-toc")
@allure.story("创建订单")
class TestTpOrderCreate(BaseTestToC):
    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestTpOrderCreate", "test_order_create_succeed", "tp"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("正向case: {case_name}")
    def test_order_create_succeed(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderCreateCheck.check(self, args["param"])

    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestTpOrderCreate", "test_order_create_fail", "tp"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("反向case {case_name}")
    def test_order_create_fail(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderCreateCheck.fail_code_check(self, args["expect"])

    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestTpOrderCreate", "test_order_create_pre_sale", "tp"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("正向case {case_name}")
    def test_order_create_pre_sale(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderCreateCheck.check(self, args["param"])
