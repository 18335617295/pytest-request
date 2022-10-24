import os
import platform

from conf.GlobalConfig import GlobalConfig
from libs import utils
from libs.Base import Base
# from libs.ClickHouse import ClickHouse
from libs.MySQL import MySqlHandler
from libs.Requests import Requests


class BaseTestToB(Base):
    api = path = Insert = None
    ump_sql = tp_sql = items_sql = tartars_sql = performance_sql = plutus_sql = user_vehicle_sql = gaea_sql = None
    request = Requests()
    # clickhouse = ClickHouse()

    @classmethod
    def setup_class(cls):

        sys_str = platform.system()
        if sys_str == "Windows":
            cls.path = os.getcwdb().decode().split(os.sep)[-1]
        elif sys_str == "Linux":
            cls.path = f"{utils.get_path(cls.__name__)}"
        else:
            cls.log.error("Other System")
        cls.api = utils.yaml_file(f"{cls.__name__}", None, cls.path, "Api")
        if "://" not in cls.api:
            cls.api = utils.get_ip(str(cls.__bases__[0])) + utils.yaml_file(f"{cls.__name__}", None, cls.path, "Api")
        cls.Insert = utils.yaml_file(f"{cls.__name__}", None, cls.path, "InsertDB")
        # uat环境mysql用到的需要全部连接  同步toc类 teardown  关闭, 类变量创建
        if GlobalConfig.ENV == "uat":
            cls.tp_sql = MySqlHandler(f"gd_tp_{GlobalConfig.ENV}")
            cls.ump_sql = MySqlHandler(f"gd_ump_{GlobalConfig.ENV}")
            cls.items_sql = MySqlHandler(f"gd_items_{GlobalConfig.ENV}")
            cls.performance_sql = MySqlHandler(f"gd_performance_{GlobalConfig.ENV}")
            cls.tartars_sql = MySqlHandler(f"gd_share_activity_{GlobalConfig.ENV}")
            cls.plutus_sql = MySqlHandler(f"gd_aep_plutus_{GlobalConfig.ENV}")
            cls.user_vehicle_sql = MySqlHandler(f"gd_user_vehicle_{GlobalConfig.ENV}")
            cls.gaea_sql = MySqlHandler(f"gd_gaea_{GlobalConfig.ENV}")
        else:
            cls.tp_sql = MySqlHandler(f"gd_tp")
            cls.ump_sql = MySqlHandler(f"gd_ump")
            cls.items_sql = MySqlHandler(f"gd_items")
            cls.performance_sql = MySqlHandler(f"gd_performance")
            cls.tartars_sql = MySqlHandler(f"gd_share_activity")
            cls.plutus_sql = MySqlHandler(f"gd_aep_plutus")
            cls.user_vehicle_sql = MySqlHandler(f"gd_user_vehicle")
            cls.gaea_sql = MySqlHandler(f"gd_gaea")

    @classmethod
    def setup_method(cls):
        if cls.Insert:
            if cls.path == "tp":
                cls.tp_sql.exe_cute_all(cls.Insert)
            if cls.path == "ump":
                cls.ump_sql.exe_cute_all(cls.Insert)
            if cls.path == "items":
                cls.items_sql.exe_cute_all(cls.Insert)

    @classmethod
    def teardown_class(cls):
        if not GlobalConfig.MAIN_ENV:
            GlobalConfig.ENV = "uat"
        cls.tp_sql.close_database()
        cls.ump_sql.close_database()
        cls.items_sql.close_database()
        cls.tartars_sql.close_database()
        cls.performance_sql.close_database()
        cls.plutus_sql.close_database()
        cls.user_vehicle_sql.close_database()
        cls.gaea_sql.close_database()

    def assert_equal(self, expect, actual, message, ignoreType=False):
        """
        断言等于
        :param expect: 预期
        :param actual: 实际
        :param message: 错误消息
        :param ignoreType: true 忽略类型校验
        :return:
        """
        if ignoreType:
            assert str(expect) == str(actual), message
        else:
            assert expect == actual, message

    def assert_no_equal(self, expect, actual, message, ignoreType=False):
        """
        断言不等于
        :param expect: 预期
        :param actual: 实际
        :param message: 错误消息
        :param ignoreType: true 忽略类型校验
        :return:
        """
        if ignoreType:
            assert str(expect) != str(actual), message
        else:
            assert expect != actual, message

    def assert_in(self, expect, actual, message):
        """
        断言
        :param expect: 预期
        :param actual: 实际
        :param message: 错误消息
        :return:
        """
        assert actual in expect, message

    def assert_list(self, actual, expect=True, message="值为空"):
        """
        断言
        :param expect: 预期
        :param actual: 实际
        :param message: 错误消息
        :return:
        """
        for i in actual:
            if expect:
                assert i is not None, message
            else:
                assert i is None, message
