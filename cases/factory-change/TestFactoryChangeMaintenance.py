import allure
import pytest

from assertcheck.factory.FactoryChangeMaintenanceCheck import FactoryChangeMaintenanceCheck
from libs import utils
from libs.BaseTestToC import BaseTestToC


@allure.feature("修理厂改价")
@allure.story("修理厂改价服务sku列表")
class TestFactoryChangeMaintenance(BaseTestToC):
    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestFactoryChangeMaintenance",
                                                                "test_factory_change_sku_list", "factory-change"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_factory_change_sku_list(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        FactoryChangeMaintenanceCheck.check(self, args["param"])
