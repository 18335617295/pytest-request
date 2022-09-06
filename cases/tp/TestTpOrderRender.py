import allure
import pytest

from assertcheck.tp.TpOrderRenderCheck import TpOrderRenderCheck
from libs.BaseTestToC import BaseTestToC
from libs import utils


@allure.feature("订单-toc")
@allure.story("订单渲染")
class TestTpOrderRender(BaseTestToC):
    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestTpOrderRender", "test_order_render_succeed", "tp"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("正向case: {case_name}")
    def test_order_render_succeed(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderRenderCheck.check(self, args["param"])

    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestTpOrderRender", "test_order_render_pre_sale", "tp"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("正向case: {case_name}")
    def test_order_render_pre_sale(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderRenderCheck.check(self, args["param"])

    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestTpOrderRender", "test_order_render_maintenance_factory", "tp"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("正向case: {case_name}")
    def test_order_render_maintenance_factory(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderRenderCheck.check(self, args["param"])
