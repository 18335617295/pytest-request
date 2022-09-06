from assertcheck.CodeCheck import CodeCheck
from libs import utils


class TpOrderAfterSalesApplyCheck:
    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        TpOrderAfterSalesApplyCheck.tp_order_after_sale_check(cls, param)
        TpOrderAfterSalesApplyCheck.tp_order_after_sale_item(cls, param)

    @staticmethod
    def tp_order_after_sale_check(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order_after_sale where order_no = {param['orderNo']} order by"
                                       f" id desc")
        cls.assert_equal(db_result["apply_code"], cls.result["data"]["applyCode"], "退款申请单号校验失败")
        cls.assert_equal(db_result["apply_type"], 2, "售后类型校验失败")
        cls.assert_equal(db_result["audit_status"], 1, "售后类型校验失败")
        cls.assert_equal(db_result["refund_amount"], param["refundTotalAmt"] * 100, "退款金额校验失败")

    @staticmethod
    def tp_order_after_sale_item(cls, param):
        db_result = cls.tp_sql.exeCute(f"select * from tp_order_after_sale_item where apply_code = "
                                       f"{cls.result['data']['applyCode']}", "all")
        db_sku, param_sku = utils.list_dict_to_list(db_result, "sku_no"), \
                            utils.list_dict_to_list(param["skuList"], "skuNo")
        cls.assert_equal(len(db_sku), len(param_sku), "sku 数量校验失败")
        for i in db_sku:
            cls.assert_in(param_sku, i, "sku验证失败")
