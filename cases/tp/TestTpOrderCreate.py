import os,sys

import allure
import pytest

from assertcheck.tp.TpOrderCreateCheck import TpOrderCreateCheck
from libs.BaseTestToC import BaseTestToC
from libs import utils
path = os.getcwd().split(os.sep)[-1]


@allure.feature("订单-toc")
@allure.story("创建订单")
class TestTpOrderCreate(BaseTestToC):
    @pytest.mark.parametrize("args, case_name", utils.yaml_file(__name__, "test_order_create_succeed", path))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("正向case: {case_name}")
    def test_order_create_succeed(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderCreateCheck.check(self, args["param"])

    @pytest.mark.parametrize("args, case_name", utils.yaml_file(__name__, "test_order_create_fail", path))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("反向case {case_name}")
    def test_order_create_fail(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderCreateCheck.fail_code_check(self, args["expect"])

    @pytest.mark.parametrize("args, case_name", utils.yaml_file(__name__, "test_order_create_pre_sale", path))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("正向case {case_name}")
    def test_order_create_pre_sale(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderCreateCheck.check(self, args["param"])
