import datetime

from assertcheck.CodeCheck import CodeCheck
from libs import utils


class TpOrderCreateCheck:
    order_no = None
    parent_order_no = None

    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        TpOrderCreateCheck.db_tp_order_check(cls, param)
        TpOrderCreateCheck.db_tp_order_pay_check(cls, param)
        TpOrderCreateCheck.db_tp_parent_order_check(cls, param)
        TpOrderCreateCheck.db_tp_order_performance_check(cls, param)
        TpOrderCreateCheck.db_tp_order_sku_check(cls, param)

    @staticmethod
    def db_tp_order_check(cls, param):
        TpOrderCreateCheck.parent_order_no = cls.result['data']['parentOrderNo']
        db_result = cls.tp_sql.exeCute(f"select * from tp_order where parent_order_no = "
                                       f"{TpOrderCreateCheck.parent_order_no}")
        TpOrderCreateCheck.order_no = db_result["order_no"]
        # tp_order表数据校验
        cls.assert_equal(db_result["order_status"], 10, "tp_order表 订单状态 校验失败")
        cls.assert_equal(db_result["pay_status"], 1, "tp_order表 支付状态 校验失败")
        cls.assert_equal(db_result["delivery_status"], 1, "tp_order表 发货状态 校验失败")
        cls.assert_equal(db_result["refund_status"], 1, "tp_order表 退款状态 校验失败")
        cls.assert_equal(db_result["service_status"], 1, "tp_order表 服务状态 校验失败")
        if param["bizType"] == "maintenance-package":
            cls.assert_equal(db_result["order_type"], 2, "tp_order表 订单类型 校验失败")
        if param["bizType"] == "c-logistics" or param["bizType"] == 'PRE_SALE':
            cls.assert_equal(db_result["order_type"], 1, "tp_order表 订单类型 校验失败")
        # 目前没有拆单场景子订单金额等于父订单金额
        if param["bizType"] == 'PRE_SALE':
            sku_result = cls.tartars_sql.exeCute(f"SELECT * FROM pre_sale_sku_rel WHERE pre_sale_id = 57 and sku_id = "
                                                 f"{param['skuInfoList'][0]['skuId']} ORDER BY id DESC LIMIT 1;")
            cls.log.debug(sku_result)
            cls.assert_equal(db_result["actual_price"], param["payAmount"], "tp_order表 应付金额 校验失败")
            cls.assert_equal(sku_result["pre_price"], db_result["actual_price"]-db_result["freight"],
                             "tp_order表 预售金额 校验失败")
            cls.assert_equal(db_result["discount_price"], db_result["payment_price"] - sku_result["pre_price"],
                             "tp_order表 优惠金额 校验失败")

        else:
            # cls.assert_equal(db_result["payment_price"], param["payAmount"], "tp_order表 应付金额 校验失败")
            cls.assert_equal(db_result["discount_price"], 0, "tp_order表 优惠金额 校验失败")
            cls.assert_equal(db_result["biz_type"], param["bizType"], "tp_order 业务身份 校验失败")
        cls.assert_equal(db_result["actual_price"], param["payAmount"], "tp_order表 实付金额 校验失败")
        cls.assert_equal(db_result["vin"], param["vin"], "tp_order vin码 校验失败")

    @staticmethod
    def db_tp_parent_order_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_parent_order where parent_order_no = "
                                       f"{cls.result['data']['parentOrderNo']}")
        # 目前没有拆单场景子订单金额等于父订单金额
        if param["bizType"] != 'PRE_SALE':
            # cls.assert_equal(db_result["payment_price"], param["payAmount"], "tp_parent_order表 应付金额 校验失败")
            cls.assert_equal(db_result["discount_price"], 0, "tp_parent_order表 优惠金额 校验失败")
        cls.assert_equal(db_result["actual_price"], param["payAmount"], "tp_parent_order表 实付金额 校验失败")

    @staticmethod
    def db_tp_order_pay_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order_pay where parent_order_no = "
                                       f"{cls.result['data']['parentOrderNo']} and deleted = 0 "
                                       f"and pay_no = \"{cls.result['data']['payNo']}\"")
        cls.assert_equal(db_result["pay_status"], 1, "tp_order_pay表 支付状态 校验失败")
        cls.assert_equal(db_result["payment_price"], param["payAmount"], "tp_order_pay表 实付金额错误 校验失败")
        cls.assert_equal(db_result["pay_no"], cls.result["data"]["payNo"], "tp_order_pay表 支付单号 校验失败")
        cls.assert_equal(db_result["pay_time"], None, "tp_order_pay表 支付时间 校验失败")

    @staticmethod
    def db_tp_order_performance_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order_performance where parent_order_no = "
                                       f"{cls.result['data']['parentOrderNo']} and deleted = 0")
        cls.assert_equal(db_result["performance_type"], param["type"], "tp_order_performance表 履约方式 校验失败")
        cls.assert_equal(db_result["store_id"], param["storeId"], "tp_order_performance表 指定门店 校验失败")
        # cls.assert_equal(db_result["service_start_time"].strftime("%Y-%m-%d %H:%M:%S"), param["serviceStartTime"],
        #                  "tp_order_performance表 服务开始时间"" 校验失败")
        # cls.assert_equal(db_result["service_start_time"] + datetime.timedelta(hours=+1), db_result["service_end_time"],
        #                  "tp_order_performance表 服务结束时间"" 校验失败")

    @staticmethod
    def db_tp_order_sku_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order_sku where order_no = "
                                       f"{TpOrderCreateCheck.order_no} order by sku_no desc", "all")
        sku_id, sku_num = utils.list_dict_to_list(param["skuInfoList"], "skuId"), utils.list_dict_to_list(
            param["skuInfoList"], "skuNum")
        cls.log.debug(f"sku_id: {sku_id}, sku_num: {sku_num}")
        sku_result = cls.items_sql.exeCute(f"select * from sku where id in ({utils.list_to_str(sku_id)})", "all")
        cls.log.debug(sku_result)
        # 商品库查询sku价格总和
        sku_amount = 0
        for i in range(len(sku_result)):
            sku_amount += sku_result[i]["promotion_price"] * sku_num[i]
        for i in db_result:
            for p in param["skuInfoList"]:
                if i["sku_no"] in utils.list_to_str(p.values()).split(',')[-2] and i["sku_no"] != "739":
                    cls.assert_equal(i["sku_no"], str(p["skuId"]), "tp_order_sku表 sku_no数据 校验失败")
                    cls.assert_equal(i["sku_num"], p["skuNum"], "tp_order_sku表 sku_num数据 校验失败")
        cls.assert_equal(len(db_result), len(param["skuInfoList"]), "tp_order_sku表 条数记录错误")

    @staticmethod
    def fail_code_check(cls, param):
        CodeCheck.code_check(cls, param)
