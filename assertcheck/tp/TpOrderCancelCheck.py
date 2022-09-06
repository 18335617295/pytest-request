from assertcheck.CodeCheck import CodeCheck


class TpOrderCancelCheck:
    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        TpOrderCancelCheck.db_tp_order_check(cls, param)
        TpOrderCancelCheck.db_tp_order_after_sale_check(cls, param)

    @staticmethod
    def db_tp_order_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order where parent_order_no = {param['orderNo']}", "all")
        for i in db_result:
            cls.assert_equal(i["order_status"], 100, "tp_order表 订单状态 校验错误")
            cls.assert_equal(i["pay_status"], 1, "tp_order表 支付状态 校验错误")
            cls.assert_equal(i["delivery_status"], 1, "tp_order表 发货状态 校验错误")
            cls.assert_equal(i["refund_status"], 1, "tp_order表 退款状态 校验错误")
            cls.assert_equal(i["service_status"], 1, "tp_order表 服务状态 校验错误")

    @staticmethod
    def db_tp_order_after_sale_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order_after_sale where parent_order_no="
                                       f"{param['orderNo']}")
        cls.assert_equal(db_result["apply_type"], 1, "tp_order_after_sale表 售后类型 校验失败")
        cls.assert_equal(db_result["audit_status"], 2, "tp_order_after_sale表 审核状态 校验失败")
        cls.assert_equal(db_result["refund_amount"], 0, "tp_order_after_sale表 退款金额 校验失败")
        cls.assert_no_equal(db_result["apply_reason"], "", "tp_order_after_sale表 申请原因 校验失败")
        cls.assert_equal(db_result["auditor_name"], "C端取消", "tp_order_after_sale表 审核人 校验失败")

    @staticmethod
    def fail_code_check(cls, param):
        CodeCheck.code_check(cls, param)
