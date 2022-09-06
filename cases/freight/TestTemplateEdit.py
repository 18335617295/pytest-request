import allure
import pytest

from assertcheck.freight.TemplateSaveCheck import TemplateSaveCheck
from libs import utils
from libs.BaseTestToB import BaseTestToB


@allure.feature("运费模版")
@allure.story("运费模版编辑")
class TestTemplateEdit(BaseTestToB):

    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestTemplateEdit", "test_template_edit", "freight"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_template_edit(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        TemplateSaveCheck.check(self, args["param"])
