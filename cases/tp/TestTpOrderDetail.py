import allure
import pytest

from assertcheck.tp.TpOrderDetailCheck import TpOrderDetailCheck
from libs import utils
from libs.BaseTestToC import BaseTestToC


@allure.feature("订单-toc")
@allure.story("订单详情")
class TestTpOrderDetail(BaseTestToC):
    @pytest.mark.parametrize("args, case_name", utils.yaml_file("TestTpOrderDetail", "test_order_detail_succeed", "tp"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_order_detail_succeed(self, args, case_name):
        args["param"]["orderNo"] = list(self.tp_sql.exeCute(args["sql"]).values())[0]
        self.result = self.request.json_post(self.api, args["param"])
        TpOrderDetailCheck.code_check(self, args["param"])
