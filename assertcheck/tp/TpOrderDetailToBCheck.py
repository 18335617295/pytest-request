from assertcheck.CodeCheck import CodeCheck
from libs import utils


class TpOrderDetailToBCheck:
    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        TpOrderDetailToBCheck.result_data_check(cls, param)

    @staticmethod
    def result_data_check(cls, param):
        # 校验订单信息
        db_order_result = cls.tp_sql.exeCute(f"select * from tp_order where order_no = {param['orderNo']}")
        cls.assert_equal(db_order_result["actual_price"], cls.result["data"]["actualPrice"], "订单详情 实付金额 校验失败")
        cls.assert_equal(db_order_result["order_no"], cls.result["data"]["orderNo"], "订单详情 订单号 校验失败")
        cls.assert_equal(db_order_result["parent_order_no"], cls.result["data"]["parentOrderNo"], "订单详情 父订单号 校验失败")
        cls.assert_equal(db_order_result["order_status"], cls.result["data"]["orderStatus"], "订单详情 订单状态 校验失败")
        # 校验支付信息
        db_pay_result = cls.tp_sql.exeCute(
            f"select * from tp_order_pay where parent_order_no = {db_order_result['parent_order_no']} order by id desc")
        cls.assert_equal(db_pay_result["pay_no"], cls.result["data"]["orderPay"]["payNo"], "订单详情 支付单号 校验失败")
        cls.assert_equal(db_pay_result["pay_status"], cls.result["data"]["orderPay"]["payStatus"], "订单详情 支付状态 校验失败")
        if cls.result["data"]["orderStatus"] == 10:
            cls.assert_equal(db_pay_result["pay_time"], cls.result["data"]["orderPay"]["payTime"], "订单详情 支付时间 校验失败")
        cls.assert_equal(db_pay_result["pay_type"], cls.result["data"]["orderPay"]["payType"], "订单详情 支付类型 校验失败")
        cls.assert_equal(db_pay_result["payment_price"], cls.result["data"]["orderPay"]["paymentPrice"],
                         "订单详情 支付金额 校验失败")
        # 如果有优惠券则校验
        db_coupon_result = cls.tp_sql.exeCute(
            f"select coupon_amount,coupon_id,coupon_name,coupon_num,coupon_total_amount,coupon_t"
            f"ype from tp_order_coupon where order_no = {param['orderNo']}", "all")
        if db_coupon_result or cls.result["data"]["orderCouponList"]:
            for i in range(0, len(db_coupon_result)):
                cls.assert_equal(db_coupon_result[i]["coupon_amount"],
                                 cls.result["data"]["orderCouponList"][i]["couponAmount"], "订单详情 优惠券coupon_amount 校验失败")
                cls.assert_equal(db_coupon_result[i]["coupon_id"], cls.result["data"]["orderCouponList"][i]["couponId"],
                                 "订单详情 优惠券coupon_id 校验失败")
                cls.assert_equal(db_coupon_result[i]["coupon_name"],
                                 cls.result["data"]["orderCouponList"][i]["couponName"],
                                 "订单详情 优惠券coupon_name 校验失败")
                cls.assert_equal(db_coupon_result[i]["coupon_num"],
                                 cls.result["data"]["orderCouponList"][i]["couponNum"],
                                 "订单详情 优惠券coupon_num 校验失败")
                cls.assert_equal(db_coupon_result[i]["coupon_total_amount"],
                                 cls.result["data"]["orderCouponList"][i]["couponTotalAmount"],
                                 "订单详情 优惠券coupon_total_amount 校验失败")
                cls.assert_equal(db_coupon_result[i]["coupon_type"],
                                 cls.result["data"]["orderCouponList"][i]["couponType"],
                                 "订单详情 优惠券coupon_type 校验失败")
        # 如果有售后信息则校验
        db_order_after_sale = cls.tp_sql.exeCute(
            f"select * from tp_order_after_sale where order_no  = {param['orderNo']}", "all")
        if cls.result["data"]["orderAfterSaleList"] or db_order_after_sale:
            for i in range(0, len(cls.result["data"]["orderAfterSaleList"])):
                cls.assert_equal(cls.result["data"]["orderAfterSaleList"][i]["applyCode"],
                                 db_order_after_sale[i]["apply_code"], "订单详情 退款单号 校验失败")
                cls.assert_equal(cls.result["data"]["orderAfterSaleList"][i]["applyReason"],
                                 db_order_after_sale[i]["apply_reason"], "订单详情 退款原因 校验失败")
                cls.assert_equal(cls.result["data"]["orderAfterSaleList"][i]["applyType"],
                                 db_order_after_sale[i]["apply_type"], "订单详情 退款类型 校验失败")

                cls.assert_equal(cls.result["data"]["orderAfterSaleList"][i]["auditStatus"],
                                 db_order_after_sale[i]["audit_status"], "订单详情 退款状态 校验失败")
        db_sku_result = cls.tp_sql.exeCute(f"select * from tp_order_sku where order_no = "
                                           f"{param['orderNo']} order by sku_no desc", "all")
        result_list = utils.list_dict_to_list(cls.result["data"]["orderSkuList"], "skuId", True)
        db_sku_result_list = utils.list_dict_to_list(db_sku_result, "skuId", True)
        cls.assert_equal(result_list, db_sku_result_list, "sku列表校验失败")
