import allure
import pytest

from assertcheck.ump.UmpCouponAddShoppingCheck import UmpCouponAddCheck
from libs.BaseTestToB import BaseTestToB
from libs import utils
from libs.decorator import ump_sku_add


@allure.feature("平台优惠券-toB")
@allure.story("添加平台优惠券模版")
class TestUmpCouponAddShopping(BaseTestToB):
    @pytest.mark.parametrize("args,case_name",
                             utils.yaml_file("TestUmpCouponAddShopping", "test_coupon_add_succeed", "ump",index=[4,5,6]))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("{case_name}")
    def test_coupon_add_succeed(self, args, case_name):
        if args["param"]["couponSelectedType"] == 1:
            args["param"]["couponItemInfoId"] = ump_sku_add()
        self.result = self.request.json_post(self.api, args["param"])
        UmpCouponAddCheck.check(self, args["param"])
        self.ump_sql.exe_cute_all(args["sqllist"])

