import time

from assertcheck.CodeCheck import CodeCheck


class TpOrderPayCheck:
    link_id = None
    parent_order_no = None

    @staticmethod
    def check(cls, param):
        time.sleep(1)
        TpOrderPayCheck.tp_order_pay_check(cls, param)
        TpOrderPayCheck.tp_order_performance_check(cls)
        TpOrderPayCheck.tp_order_check(cls)
        TpOrderPayCheck.tp_order_check(cls)

    @staticmethod
    def tp_order_pay_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order_pay where pay_no =  "
                                       f"'{param['payOrderNo']}' order by id desc")
        TpOrderPayCheck.parent_order_no = db_result['parent_order_no']
        cls.assert_equal(db_result["pay_status"], 2, "tp_order_pay 支付状态 校验失败")
        cls.assert_no_equal(db_result["pay_time"], None, "tp_order_pay 支付状态 校验失败")

    @staticmethod
    def tp_order_performance_check(cls):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order_performance where parent_order_no =  "
                                       f"{TpOrderPayCheck.parent_order_no} order by id desc")
        TpOrderPayCheck.link_id = db_result["link_id"]

    @staticmethod
    def tp_order_check(cls):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order where parent_order_no =  "
                                       f"{TpOrderPayCheck.parent_order_no} order by id desc")
        cls.log.debug(db_result)
        cls.assert_equal(db_result["pay_status"], 2, "tp_order 支付状态 校验失败")
        if TpOrderPayCheck.link_id:
            cls.assert_equal(db_result["order_status"], 70, "tp_order 订单状态 校验失败")
            cls.assert_equal(db_result["delivery_status"], 2, "tp_order 发货状态 校验失败")
        else:
            cls.assert_equal(db_result["order_status"], 30, "tp_order 订单状态 校验失败")
            cls.assert_equal(db_result["delivery_status"], 1, "tp_order 发货状态 校验失败")
        cls.assert_equal(db_result["refund_status"], 1, "tp_order 退款状态 校验失败")
        cls.assert_equal(db_result["service_status"], 1, "tp_order 服务状态 校验失败")
