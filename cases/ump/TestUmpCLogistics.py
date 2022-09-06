import json

import allure
import pytest

from libs import utils
from libs.BaseTestToC import BaseTestToC
from assertcheck.ump.UmpCouponCLogisticsCheck import UmpCouponCLogisticsCheck


class TestUmpCLogistics(BaseTestToC):
    @pytest.mark.parametrize("args,case_name", utils.yaml_file("TestUmpCLogistics", "test_coupon_c_logistics_succeed", "ump"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("{case_name}")
    @allure.story("正向case")
    def test_coupon_maintenance_package_succeed(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"],account=4)
        UmpCouponCLogisticsCheck.code_check(self)
