import allure
import pytest

from assertcheck.ump.UmpCalculateCartPriceCheck import UmpCalculateCartPriceCheck
from libs import utils
from libs.BaseTestToC import BaseTestToC


@allure.feature("计价")
@allure.story("购物车")
class TestUmpCalculateCartPrice(BaseTestToC):
    @pytest.mark.parametrize("args,case_name", utils.yaml_file("TestUmpCalculateCartPrice", "test_calculate_cart_price",
                                                               "ump"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("{case_name}")
    def test_calculate_cart_price(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])
        UmpCalculateCartPriceCheck.check(self, args["param"])

    @pytest.mark.parametrize("args,case_name", utils.yaml_file("TestUmpCalculateCartPrice",
                                                               "test_coupon_calculate_cart_price", "ump"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("{case_name}")
    def test_coupon_calculate_cart_price(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"], account=5)
        UmpCalculateCartPriceCheck.check(self, args["param"])

