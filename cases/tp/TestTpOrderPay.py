import allure
import pytest

from assertcheck.tp.TpOrderPayCheck import TpOrderPayCheck
from libs import utils
from libs.BaseTestToB import BaseTestToB
from libs.Mq import MyMq
from libs.decorator import order_create


@allure.feature("订单-内部")
@allure.story("订单支付成功回调")
class TestTpOrderPay(BaseTestToB):
    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestTpOrderPay", "test_order_py_succeed", "tp"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    @pytest.mark.usefixtures("order_create")
    def test_order_py_succeed(self, args, case_name):
        self.mq = MyMq()
        db_result = self.tp_sql.exeCute(args["sql"])
        args["param"]["message"]["payOrderNo"] = db_result["pay_no"]
        self.result = self.mq.send_msg(args["param"])
        TpOrderPayCheck.check(self, args["param"]["message"])
