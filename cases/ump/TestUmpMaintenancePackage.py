import json

import allure
import pytest

from libs import utils
from libs.BaseTestToC import BaseTestToC
from assertcheck.ump.UmpCouponMaintenancePackageCheck import UmpCouponMaintenancePackageCheck


class TestUmpMaintenancePackage(BaseTestToC):
    @pytest.mark.parametrize("args,case_name", utils.yaml_file("TestUmpMaintenancePackage", "test_coupon_maintenance_package_succeed", "ump"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("{case_name}")
    @allure.story("正向case")
    def test_coupon_maintenance_package_succeed(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"], account=5)
        UmpCouponMaintenancePackageCheck.code_check(self)
