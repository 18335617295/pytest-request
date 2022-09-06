import allure
import pytest

from libs import utils
from libs.BaseTestToB import BaseTestToB


@allure.feature("运费模版")
@allure.story("运费模版列表")
class TestTemplatePage(BaseTestToB):

    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestTemplatePage", "test_template_page", "freight"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_template_page(self, args, case_name):
        self.result = self.request.get(self.api, args["param"])
        assert self.result["code"] == 1
        assert self.result["data"]["records"]
        if "templateCode" in args["param"]:
            assert self.result["data"]["records"][0]["templateCode"] == str(args["param"]["templateCode"])
        if "templateName" in args["param"]:
            assert self.result["data"]["records"][0]["templateName"] == str(args["param"]["templateName"])
