import os

from clickhouse_driver import Client
from conf.GlobalConfig import GlobalConfig
from libs import utils
from libs.Base import Base


class ClickHouse(Base):

    def __init__(self):
        """
        连接clickhouse
        """
        try:
            db_info = utils.yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", "ClickHouse")
            self.client = Client(host=db_info["host"], port=db_info["port"], user=db_info["user"],
                                 password=db_info["passwd"], database=db_info["db"])
        except Exception as e:
            self.log.error("连接CLickHouse失败，请检查...")
            self.log.error("ClickHouse Error %d: %s" % (e.args[0], e.args[1]))

    def exeCute(self, sql):
        return self.client.execute(sql)


if __name__ == '__main__':
    sql = ClickHouse()
    print(sql.exeCute('select bitmapCardinality(b) from (select t5.id as "id", bitmapAndnot(t5.b, t6.b) as "b" from (select t3.id as "id", bitmapOr(t3.b, t4.b) as "b" from (select 1 as "id", groupBitmapOrState(roaring_bitmap) as "b" from default.dmp_tag_user_data_single where tag_id in (139, 42)) as "t3" join (select t1.id as "id", bitmapAnd(t1.b, t2.b) as "b" from (select 1 as "id", roaring_bitmap as "b" from default.dmp_tag_user_data_single where tag_id = 403) as "t1" join (select 1 as "id", groupBitmapOrState(roaring_bitmap) as "b" from default.dmp_tag_user_data_single where tag_id in (399, 400)) as "t2" on t1.id = t2.id) as "t4" on t3.id = t4.id) as "t5" join (select 1 as "id", groupBitmapAndState(roaring_bitmap) as "b" from default.dmp_tag_user_data_single where tag_id in (436, 439)) as "t6" on t5.id = t6.id) as "aggregated_result"'))
