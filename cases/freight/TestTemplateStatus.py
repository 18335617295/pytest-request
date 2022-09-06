import allure
import pytest

from assertcheck.freight.TemplateSaveCheck import TemplateSaveCheck
from libs import utils
from libs.BaseTestToB import BaseTestToB


@allure.feature("运费模版")
@allure.story("运费模版状态")
class TestTemplateStatus(BaseTestToB):
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestTemplateStatus", "test_template_status", "freight"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_template_status(self, args, case_name):
        self.result = self.request.put(self.api, args["param"])
        TemplateSaveCheck.product_template_status_check(self, args["param"])
