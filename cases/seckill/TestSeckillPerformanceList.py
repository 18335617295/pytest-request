import allure
import pytest

from assertcheck.seckill.SeckillPerformanceListCheck import SeckillPerformanceListCheck
from libs import utils
from libs.BaseTestToC import BaseTestToC


@allure.feature("秒杀")
@allure.story("商品秒杀列表")
class TestSeckillPerformanceList(BaseTestToC):
    @pytest.mark.parametrize("args, case_name",
                             utils.yaml_file("TestSeckillPerformanceList", "test_seckill_performance_list", "seckill"))
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("正向case: {case_name}")
    def test_seckill_performance_list(self, args, case_name):
        self.result = self.request.get(self.api)
        SeckillPerformanceListCheck.check(self)
