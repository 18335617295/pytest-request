import allure
import pytest

from libs import utils
from libs.BaseTestToC import BaseTestToC
from libs.decorator import order_create


@allure.feature("收银台")
@allure.story("支付方式")
class TestCashierPayTypeQuery(BaseTestToC):
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestCashierPayTypeQuery", "test_cashier_pay_type_query", "cashier"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    @pytest.mark.usefixtures("order_create")
    def test_cashier_pay_type_query(self, args, case_name):
        args["API"]["param"]["payOrderNo"] = args["param"]["payOrderNo"] = self.tp_sql.exeCute(args["sql"])["pay_no"]
        self.result = self.request.json_post(self.api, args["param"])
        assert self.result["data"]["list"]
        self.result = self.request.json_post(args["API"]["api"], args["API"]["param"])
        assert self.result["data"]["h5Url"] is not None
