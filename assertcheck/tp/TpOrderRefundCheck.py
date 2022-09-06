from assertcheck.CodeCheck import CodeCheck


class TpOrderRefundCheck:
    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        TpOrderRefundCheck.db_tp_order_after_sale_check(cls, param)

    @staticmethod
    def db_tp_order_after_sale_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order_after_sale where order_no= {param['orderNo']}")
        tp_order_result = cls.tp_sql.exeCute(
            f"select * from tp_order where order_no= {param['orderNo']}")

        cls.assert_equal(db_result["apply_type"], 2, "tp_order_after_sale表 售后类型 校验失败")
        cls.assert_in((1, 2), db_result["audit_status"], "tp_order_after_sale表 审核状态 校验失败")
        cls.assert_equal(db_result["refund_amount"], tp_order_result["actual_price"],
                         "tp_order_after_sale表 退款金额 校验失败")
        cls.assert_no_equal(db_result["apply_reason"], "", "tp_order_after_sale表 申请原因 校验失败")

    @staticmethod
    def db_tp_order_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order where parent_order_no = {param['orderNo']}", "all")
        for i in db_result:
            cls.assert_equal(i["order_status"], 90, "tp_order表 订单状态 校验错误")
            cls.assert_equal(i["pay_status"], 2, "tp_order表 支付状态 校验错误")
            cls.assert_equal(i["delivery_status"], 2, "tp_order表 发货状态 校验错误")
            cls.assert_in((2, 3), i["refund_status"], "tp_order表 退款状态 校验错误")
            cls.assert_equal(i["service_status"], 2, "tp_order表 服务状态 校验错误")

    @staticmethod
    def fail_code_check(cls, expect):
        CodeCheck.code_check(cls, expect)
