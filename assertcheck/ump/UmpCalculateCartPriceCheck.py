from assertcheck.CodeCheck import CodeCheck
from libs import utils


class UmpCalculateCartPriceCheck:
    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        UmpCalculateCartPriceCheck.amount_check(cls, param)

    @staticmethod
    def amount_check(cls, param):
        sku_id, sku_num = utils.list_dict_to_list(param[0]["itemParamList"], "skuId"), utils.list_dict_to_list(
            param[0]["itemParamList"], "skuNum")
        # 购买商品和数量绑定
        sku_info_dict = {}
        for i in range(len(sku_num)):
            sku_info_dict[sku_id[i]] = sku_num[i]
        cls.log.debug(f"sku_id: {sku_id}, sku_num: {sku_num}")
        sku_result = cls.items_sql.exeCute(f"select * from sku where sku_id in ({utils.list_to_str(sku_id)}) and "
                                           f"deleted = 0", "all")
        cls.log.debug(sku_result)
        # 商品库查询sku价格总和
        sku_amount = 0
        for i in range(len(sku_result)):
            sku_amount += sku_result[i]["promotion_price"] * sku_info_dict[sku_result[i]["sku_id"]]
        cls.log.debug(f"sku总价: {sku_amount}")
        cls.log.debug(cls.result["data"]["calculateInfoResponseList"])
        original_sku_amount = sku_amount
        # 获取接口使用的优惠券
        coupon_list = []
        if cls.result["data"]["calculateInfoResponseList"]:
            for calculateInfoResponseList in cls.result["data"]["calculateInfoResponseList"]:
                for coupon in (
                        utils.num_str_to_sorted_num_list(calculateInfoResponseList["usedCouponIds"], ",", False)):
                    if coupon not in coupon_list:
                        coupon_list.append(coupon)
        # 优惠券计价
        cls.log.debug(coupon_list)
        if coupon_list:
            db_coupon = cls.ump_sql.select_in(table="coupon_info",
                                              cond_dict={"coupon_id": coupon_list})
            cls.log.debug(db_coupon)
            for coupon in db_coupon:
                coupon_template_info = cls.ump_sql.select_one(table="coupon_discount_template_rule_info", cond_dict={
                    "coupon_template_rule_id": coupon["coupon_template_info_id"]})
                # 抵用和满减券
                if coupon["coupon_type"] in [1, 3]:
                    coupon_amount = int(coupon["coupon_discount_surfix"])
                    # 满件减
                    if coupon_template_info["coupon_prefix_type"] == "1" and str(len(sku_id)) >= coupon[
                            "coupon_discount_prefix"]:
                        # 非限品券
                        if coupon_template_info["coupon_selected_type"] == "3":
                            sku_amount -= coupon_amount
                        # 限品券
                        # elif True:
                        #     pass
                    elif coupon_template_info["coupon_prefix_type"] == "0" and original_sku_amount >= int(coupon[
                            "coupon_discount_prefix"]):
                        sku_amount -= coupon_amount
                    else:
                        continue
                # 满折优惠券
                elif coupon["coupon_type"] in [2]:
                    coupon_amount = float(coupon["coupon_discount_surfix"])
                    if coupon_template_info["coupon_prefix_type"] == "1" and str(len(sku_id)) >= coupon[
                            "coupon_discount_prefix"]:
                        sku_amount *= coupon_amount
                    elif coupon_template_info["coupon_prefix_type"] == "0" and original_sku_amount >= coupon[
                            "coupon_discount_prefix"]:
                        sku_amount *= coupon_amount
                    else:
                        continue
            cls.log.debug(sku_amount)
            cls.log.debug(cls.result["data"]["couponShareTotalOrderPrice"])
            assert sku_amount - cls.result["data"]["couponShareTotalOrderPrice"] <= 1, "优惠券计价错误"
        else:
            assert sku_amount == cls.result['data']["couponShareTotalOrderPrice"]
        assert cls.result["data"]["originalTotalOrderPrice"] - cls.result["data"]["discountTotalOrderPrice"] - \
               cls.result["data"]["couponShareTotalOrderPrice"] <= 1
