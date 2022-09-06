import allure
import pytest

from assertcheck.factory.FactoryChangeCreateCheck import FactoryChangeCreateCheck
from libs import utils
from libs.BaseTestToB import BaseTestToB


@allure.feature("修理厂改价")
@allure.story("改价服务项目创建")
class TestFactoryChangeCreate(BaseTestToB):
    print(__name__)
    print()
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file(__name__, "test_factory_change_create", "factory-change"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_factory_change_create(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        FactoryChangeCreateCheck.check(self, args["param"])

    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestFactoryChangeCreate", "test_factory_change_edit", "factory-change"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_factory_change_edit(self, args, case_name):
        self.result = self.request.put(self.api + f'/{args["param"]["id"]}', json=args["param"])
        FactoryChangeCreateCheck.check(self, args["param"])

