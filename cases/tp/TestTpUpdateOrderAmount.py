import allure
import pytest

from assertcheck.tp.TpUpdateOrderAmountCheck import TpUpdateOrderAmountCheck
from libs import utils
from libs.BaseTestToB import BaseTestToB
from libs.decorator import order_create


@allure.feature("订单-tob")
@allure.story("修改订单金额")
class TestTpUpdateOrderAmount(BaseTestToB):
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestTpUpdateOrderAmount", "test_update_order_amount_succeed", "tp"))
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("正向case: {case_name}")
    @pytest.mark.usefixtures("order_create")
    def test_update_order_amount_succeed(self, args, case_name):
        sql_result = self.tp_sql.exeCute(args["sql"])
        args["param"]["orderNo"], args["param"]["originAmount"] = sql_result["order_no"], sql_result["actual_price"]
        self.result = self.request.put(self.api, args["param"])
        TpUpdateOrderAmountCheck.check(self, args["param"])
