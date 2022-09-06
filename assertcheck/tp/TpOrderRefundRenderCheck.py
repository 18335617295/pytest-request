from assertcheck.CodeCheck import CodeCheck


class TpOrderRefundRenderCheck:
    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        TpOrderRefundRenderCheck.data_check(cls, param)

    @staticmethod
    def data_check(cls, param):
        # 退款金额
        refund_amount = 0
        # 退款商品
        for i in range(len(param["skuNoList"])):
            result = cls.tp_sql.exeCute(f"select * from tp_order_sku where order_no = {param['orderNo']} "
                                        f"and snapshot like '%SKU1003%'")

            cls.assert_equal(result["sku_no"], cls.result["data"]["orderSkuCommonResultList"][i]["skuId"],
                             "退款渲染 sku 校验失败", True)
            refund_amount += result["actual_price"]
        cls.assert_equal(refund_amount, cls.result["data"]["refundAmount"], "退款商品总金额错误")
