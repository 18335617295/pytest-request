import allure
import pytest

from assertcheck.factory.FactoryChangePricePreviewCheck import FactoryChangePricePreviewCheck
from libs import utils
from libs.BaseTestToC import BaseTestToC


@allure.feature("修理厂改价")
@allure.story("修理厂改价预览")
class TestFactoryChangePricePreview(BaseTestToC):
    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestFactoryChangePricePreview",
                                                                "test_factory_change_price_preview", "factory-change"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_factory_change_price_preview(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        FactoryChangePricePreviewCheck.check(self, args["param"])
