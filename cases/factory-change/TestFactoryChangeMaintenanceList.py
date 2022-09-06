import allure

from assertcheck.factory.FactoryChangeMaintenanceListCheck import FactoryChangeMaintenanceListCheck
from libs.BaseTestToC import BaseTestToC


@allure.feature("修理厂改价")
@allure.story("修理厂改价服务项列表")
class TestFactoryChangeMaintenanceList(BaseTestToC):
    def test_factory_maintenance_list(self):
        self.result = self.request.get(self.api)
        FactoryChangeMaintenanceListCheck.list_check(self)
