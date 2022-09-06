import allure
import pytest

from assertcheck.ump.UmpCalculatePriceCheck import UmpCalculatePriceCheck
from libs import utils
from libs.BaseTestToC import BaseTestToC


@allure.feature("计价")
@allure.story("保养")
class TestUmpCalculatePrice(BaseTestToC):
    @pytest.mark.parametrize("args,case_name", utils.yaml_file("TestUmpCalculatePrice", "test_calculate_price", "ump"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("{case_name}")
    def test_calculate_price(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        UmpCalculatePriceCheck.check(self, args["param"])

    @pytest.mark.parametrize("args,case_name", utils.yaml_file("TestUmpCalculatePrice", "test_calculate_price", "ump"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("{case_name}")
    def test_coupon_calculate_price(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"], account=5)
        UmpCalculatePriceCheck.check(self, args["param"])
