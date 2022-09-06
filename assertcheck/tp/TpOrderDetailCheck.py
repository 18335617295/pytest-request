from assertcheck.CodeCheck import CodeCheck
from libs import utils


class TpOrderDetailCheck:
    @staticmethod
    def code_check(cls, param):
        CodeCheck.tp_code_check(cls)
        TpOrderDetailCheck.result_data_check(cls, param)

    @staticmethod
    def result_data_check(cls, param):
        sku_list = db_sku_list = []
        for i in cls.result["data"]["skuItemGroupList"]:
            for sku in utils.list_dict_to_list(i["skus"], "skuId"):
                sku_list.append(sku)
        sku_list.sort()
        cls.log.debug(sku_list)
        if param["orderStatus"] in [10, 100]:  # 待支付
            db_order_pay = cls.tp_sql.exeCute(
                f"select * from tp_order_pay where parent_order_no = {param['orderNo']} and deleted = 0")
            cls.log.debug(db_order_pay)
            cls.assert_equal(cls.result["data"]["orderPay"]["payStatus"], 1, "详情接口 payStatus 校验失败")
            cls.assert_equal(cls.result["data"]["orderPay"]["payNo"], db_order_pay["pay_no"], "详情接口 payNo 校验失败")
            cls.assert_equal(cls.result["data"]["orderPay"]["payTime"], db_order_pay["pay_time"], "详情接口 payTime 校验失败")
            cls.assert_equal(cls.result["data"]["orderPay"]["payType"], db_order_pay["pay_type"], "详情接口 payType 校验失败")
            cls.assert_equal(cls.result["data"]["orderPay"]["paymentPrice"], db_order_pay["payment_price"],
                             "详情接口 payTime 校验失败")

            db_order = cls.tp_sql.exeCute(f"select * from tp_order where parent_order_no = {param['orderNo']}")
            db_order_sku = cls.tp_sql.exeCute(f"select * from tp_order_sku where order_no = {db_order['order_no']}",
                                              "all")
            for i in db_order_sku:
                db_sku_list.append(int(i["sku_no"]))
            db_sku_list.sort()
            cls.log.debug(db_sku_list)
            cls.log.debug(sku_list)
            cls.assert_equal(db_sku_list, sku_list, "接口返回sku 与tp_order_sku不一致")
        else:
            db_order = cls.tp_sql.exeCute(f"select * from tp_order where order_no = {param['orderNo']}")
            db_order_pay = cls.tp_sql.exeCute(
                f"select * from tp_order_pay where parent_order_no = {db_order['parent_order_no']} and deleted = 0")
            cls.log.debug(db_order_pay)
            cls.assert_equal(cls.result["data"]["orderPay"]["payStatus"], 2, "详情接口 payStatus 校验失败")
            cls.assert_equal(cls.result["data"]["orderPay"]["payNo"], db_order_pay["pay_no"], "详情接口 payNo 校验失败")
            # 时间格式无法转换
            cls.assert_no_equal(cls.result["data"]["orderPay"]["payTime"], db_order_pay["pay_time"],
                                "详情接口 payTime 校验失败")
            cls.assert_equal(cls.result["data"]["orderPay"]["payType"], db_order_pay["pay_type"], "详情接口 payType 校验失败")
            cls.assert_equal(cls.result["data"]["orderPay"]["paymentPrice"], db_order_pay["payment_price"],
                             "详情接口 payTime 校验失败")

            db_order_sku = cls.tp_sql.exeCute(f"select * from tp_order_sku where order_no = {param['orderNo']}",
                                              "all")
            for i in db_order_sku:
                db_sku_list.append(int(i["sku_no"]))
            db_sku_list.sort()
            cls.log.debug(db_sku_list)
            cls.log.debug(sku_list)
            cls.assert_equal(db_sku_list, sku_list, "接口返回sku 与tp_order_sku不一致")
