import math

from assertcheck.CodeCheck import CodeCheck
from libs import utils


class TpOrderListToBCheck:
    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        TpOrderListToBCheck.result_data_check(cls, param)

    @staticmethod
    def result_data_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order where shop_id = {param['shopId']} order by mtime desc "
                                       f"limit {(param['current'] - 1) * param['size']},{param['size']}", "all")
        db_count = cls.tp_sql.exeCute(
            f"select count(*) count from tp_order where shop_id = {param['shopId']} order by mtime desc")
        if "orderNo" in param and param["orderNo"]:
            db_result = cls.tp_sql.exeCute(
                f"select * from tp_order where shop_id = {param['shopId']} and order_no = {param['orderNo']} order by "
                f"mtime desc limit {(param['current'] - 1) * param['size']},{param['size']}", "all")
            db_count = cls.tp_sql.exeCute(f"select count(*) count from tp_order where shop_id = {param['shopId']} and "
                                          f"order_no = {param['orderNo']} order by mtime desc")
        cls.log.debug(db_count)
        cls.log.debug((cls.result["data"]["total"]))
        cls.assert_equal(cls.result["data"]["total"], (db_count["count"]), "接口总数与数据库总数不一致")
        cls.assert_equal(cls.result["data"]["totalPage"], math.ceil(db_count["count"] / param['size']), "分页总数与数据库总数不一致")
        api_result_order_no_list = utils.list_dict_to_list(cls.result["data"]["records"], "orderNo", True)
        db_result_order_no_list = utils.list_dict_to_list(db_result, "order_no", True)
        cls.log.debug(api_result_order_no_list)
        cls.log.debug(db_result_order_no_list)
        cls.assert_equal(api_result_order_no_list, db_result_order_no_list, "接口返回订单号与数据库不一致")
