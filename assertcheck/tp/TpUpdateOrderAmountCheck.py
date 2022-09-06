from assertcheck.CodeCheck import CodeCheck


class TpUpdateOrderAmountCheck:
    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        TpUpdateOrderAmountCheck.db_tp_order_check(cls, param)
        TpUpdateOrderAmountCheck.db_tp_order_amount_record(cls, param)

    @staticmethod
    def db_tp_order_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order where order_no = {param['orderNo']}")
        cls.assert_equal(db_result["actual_price"], param["payAmount"], "tp_order表 actual_price金额 校验错误")

    # TODO
    @staticmethod
    def db_tp_parent_order_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_parent_order where order_no = {param['orderNo']}")
        cls.assert_equal(db_result["actual_price"], param["payAmount"], "tp_order表 actual_price金额 校验错误")

    # TODO 父订单改价未校验
    @staticmethod
    def db_tp_order_amount_record(cls, param):
        db_result = cls.tp_sql.exeCute(
            f"select * from tp_order_amount_record where order_no = {param['orderNo']} order by id desc")
        cls.assert_equal(db_result["after_actual_price"], param["payAmount"],
                         "tp_order_amount_record after_actual_price 校验失败")
        cls.assert_equal(db_result["original_actual_price"], param["originAmount"],
                         "tp_order_amount_record original_actual_price 校验失败")
        cls.assert_equal(db_result["order_type"], 2, "tp_order_amount_record order_type 校验失败")
