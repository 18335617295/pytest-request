import allure
import pytest

from libs.BaseTestToB import BaseTestToB
from libs import utils

@allure.feature("创建优惠券限制SKU需要调用的接口，添加SKU")
@allure.story("添加SKU")
class TestUmpAddSku(BaseTestToB):
    @pytest.mark.parametrize("args,case_name", utils.yaml_file("TestUmpAddSku", "test_coupon_sku_add_succeed", "ump"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("{case_name}")
    def test_coupon_sku_add_succeed(self, args, case_name):
        self.result = self.request.json_post(self.api, args["param"])




