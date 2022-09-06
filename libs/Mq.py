import json
import os

from rocketmq.client import Producer, Message
from conf.GlobalConfig import GlobalConfig
from libs import utils
# 安装mq https://github.com/apache/rocketmq-client-python
from libs.Base import Base
from libs.Singleton import Singleton


class MyMq(Base, metaclass=Singleton):
    def __init__(self, group='gd_aep'):
        mq_info = utils.yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", "Mq")
        self.producer = Producer(group)
        self.producer.set_namesrv_addr(mq_info["host"])
        self.log.debug("开始连接mq")
        self.producer.start()
        self.log.debug("连接成功")

    def send_msg(self, args: dict):
        try:

            msg = Message(args["topic"])
            msg.set_tags(args["tag"])
            msg.set_body(json.dumps(args["message"]).encode('utf-8'))
            self.log.debug(f"开始发送消息: {args['message']}")
            ret = self.producer.send_sync(msg)
            self.log.debug(f"发送消息完成, {ret.status, ret.msg_id, ret.offset}")
            return ret
        except Exception as e:
            self.log.error(e)

    def __del__(self):
        if self.producer:
            self.producer.shutdown()


if __name__ == '__main__':
    mq = MyMq()
