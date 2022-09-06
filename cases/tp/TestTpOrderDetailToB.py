import allure
import pytest

from assertcheck.tp.TpOrderDetailToBCheck import TpOrderDetailToBCheck
from libs import utils
from libs.BaseTestToB import BaseTestToB
from libs.decorator import order_create


@allure.feature("订单-tob")
@allure.story("订单详情")
class TestTpOrderDetailToB(BaseTestToB):
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestTpOrderDetailToB", "test_order_detail_succeed", "tp"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    @pytest.mark.usefixtures("order_create")
    def test_order_detail_succeed(self, args, case_name):
        args["param"]["orderNo"] = self.tp_sql.exeCute(args["sql"])["order_no"]
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderDetailToBCheck.check(self, args["param"])
