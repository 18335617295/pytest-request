import time

from assertcheck.CodeCheck import CodeCheck


class TpOrderPerformanceStartCheck:

    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        time.sleep(1)
        TpOrderPerformanceStartCheck.tp_order_check(cls, param)

    @staticmethod
    def tp_order_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order where order_no =  "
                                       f"{param['orderNo']} order by id desc")
        cls.log.debug(db_result)
        cls.assert_equal(db_result["order_status"], 71, "tp_order 订单状态 校验失败")
        cls.assert_equal(db_result["pay_status"], 2, "tp_order 支付状态 校验失败")
        cls.assert_equal(db_result["delivery_status"], 2, "tp_order 发货状态 校验失败")
        cls.assert_equal(db_result["refund_status"], 1, "tp_order 退款状态 校验失败")
        cls.assert_equal(db_result["service_status"], 2, "tp_order 服务状态 校验失败")
