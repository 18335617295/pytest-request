import time

from assertcheck.CodeCheck import CodeCheck
from libs import utils


class SeckillPerformanceListCheck:
    @staticmethod
    def check(cls):
        CodeCheck.tp_code_check(cls)
        SeckillPerformanceListCheck.seckill_list_check(cls)

    @staticmethod
    def seckill_list_check(cls):
        by_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        db_result = cls.tartars_sql.exeCute(f"SELECT count(*) FROM seckill_list WHERE is_online = 1 and begin_time > '"
                                            f"{by_time} 00:00:00' and end_time <= '{by_time} 23:59:59'")
        cls.log.debug(db_result)
        cls.log.debug(len(cls.result["data"]))
        cls.assert_equal(db_result["count(*)"], len(cls.result["data"]), "秒杀列表数据总数不一致")
