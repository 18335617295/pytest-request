from assertcheck.CodeCheck import CodeCheck
from libs import utils


class UmpCalculatePriceCheck:
    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        UmpCalculatePriceCheck.amount_check(cls, param)

    @staticmethod
    def amount_check(cls, param):
        sku_id, sku_num = utils.list_dict_to_list(param[0]["goodsList"], "id"), utils.list_dict_to_list(
            param[0]["goodsList"], "num")
        cls.log.debug(f"sku_id: {sku_id}, sku_num: {sku_num}")
        sku_result = cls.items_sql.exeCute(f"select * from sku where id in ({utils.list_to_str(sku_id)})",
                                           "all")
        cls.log.debug(sku_result)
        # 商品库查询sku价格总和
        sku_amount = 0
        for i in range(len(sku_result)):
            sku_amount += sku_result[i]["promotion_price"] * sku_num[i]
        cls.log.debug(f"sku总价: {sku_amount}")
        cls.log.debug(cls.result["data"]["totalPrice"])
        # 从接口计算工时费
        hour_amount = cls.result["data"]["totalServicePrice"]
        coupon_list = cls.result["data"]["selectedCoupons"]
        if coupon_list:
            db_coupon = cls.ump_sql.select_in(table="coupon_info",
                                              cond_dict={"coupon_id": coupon_list})
            cls.log.debug(db_coupon)
            for coupon in db_coupon:
                sku_amount -= int(coupon["coupon_discount_surfix"])
            cls.log.debug(sku_amount)
            cls.log.debug(cls.result["data"]["totalPrice"])
            assert sku_amount / 100 - cls.result["data"]["totalPrice"] <= 0.01, "优惠券计价错误"
        else:
            assert cls.result["data"]["totalPrice"] * 100 == sku_amount + hour_amount * 100, "价格计算错误"
        assert hour_amount > 0, "保养工时费错误"
