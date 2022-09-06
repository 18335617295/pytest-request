import os

import redis

from conf.GlobalConfig import GlobalConfig
from libs import utils
from libs.Base import Base


class MyRedis(Base):
    def __init__(self, key, db=0):
        try:
            redis_info = utils.yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", key)
            pool = redis.ConnectionPool(host=redis_info["host"], port=redis_info["port"],
                                        password=redis_info["password"], decode_responses=True, db=db)
            self.r = redis.Redis(connection_pool=pool)
        except Exception as e:
            self.log.error(f"redis 链接错误：{e}")

    def get(self, key):
        return self.r.get(key)


if __name__ == '__main__':
    print(MyRedis("Redis").r.get("PRODUCT:TEMPLATE:11"))
