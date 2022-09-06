import time

import allure
import pytest

from libs import utils
from libs.BaseTestToC import BaseTestToC


@allure.feature("预售")
@allure.story("商品详情预售信息")
class TestSkuDetailList(BaseTestToC):
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestSkuDetailList", "test_sku_detail_list", "maintenance-recommend"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_sku_detail_list(self, args, case_name):
        by_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 5))
        sql = f'UPDATE pre_sale_base SET pre_end_time = "{by_time}", buy_start_time = "{by_time}" WHERE id = 57'
        self.tartars_sql.exeCute(sql)
        self.result = self.request.get(self.api)
        assert self.result["data"]["preSaleStatus"] == 1, "预售预约状态错误"
        # self.assert_list(list(self.result["data"]["preSaleDetail"].values()))
        time.sleep(5)
        self.result = self.request.get(self.api)
        assert self.result["data"]["preSaleStatus"] == 2, "预售抢购状态错误"
        # self.assert_list(list(self.result["data"]["preSaleDetail"].values()))
