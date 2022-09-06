import allure
import pytest

from libs import utils
from libs.BaseTestToC import BaseTestToC
from assertcheck.ump.UmpCouponGetCheck import UmpCouponGetCheck


class TestUmpCouponGet(BaseTestToC):
    @pytest.mark.parametrize("args,case_name", utils.yaml_file("TestUmpCouponGet", "test_coupon_get_succeed", "ump"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("{case_name}")
    @allure.story("正向case")
    def test_coupon_get_succeed(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        UmpCouponGetCheck.code_check(self)
        UmpCouponGetCheck.check(self)

    @pytest.mark.parametrize("args,case_name", utils.yaml_file("TestUmpCouponGet", "test_coupon_get_fail", "ump"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("{case_name}")
    @allure.story("逆向case")
    def test_coupon_get_fail(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        UmpCouponGetCheck.check_fail(self)
        UmpCouponGetCheck.delete_sql(self)

