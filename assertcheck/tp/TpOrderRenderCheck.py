import math

from assertcheck.CodeCheck import CodeCheck
from libs import utils


class TpOrderRenderCheck:
    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        TpOrderRenderCheck.amount_check(cls, param)

    @staticmethod
    def amount_check(cls, param):
        sku_id, sku_num = utils.list_dict_to_list(param["skuInfoList"], "skuId"), utils.list_dict_to_list(
            param["skuInfoList"], "skuNum")
        cls.log.debug(f"sku_id: {sku_id}, sku_num: {sku_num}")
        # 预售商品
        if param["bizType"] == "PRE_SALE":
            sku_result = [cls.tartars_sql.exeCute(f"SELECT * FROM pre_sale_sku_rel WHERE pre_sale_id = 57 and sku_id in"
                                                  f" ({utils.list_to_str(sku_id)}) ORDER BY id DESC LIMIT 1;")]
        else:
            sku_result = cls.items_sql.exeCute(f"select * from sku where sku_id in ({utils.list_to_str(sku_id)}) AND "
                                               f"deleted = 0", "all")
        if param["bizType"] == "maintenance-factory":
            factory_result = cls.plutus_sql.exeCute(f"SELECT sku_id,premium_rate from store_premium_sku_rate WHERE "
                                                    f"sku_id IN ({utils.list_to_str(sku_id)}) and store_id = "
                                                    f"{param['storeId']} and deleted = 0", "all")
            cls.log.debug(factory_result)
        else:
            factory_result = []
        cls.log.debug(sku_result)
        # 商品库查询sku价格总和
        sku_amount = 0
        for i in range(len(sku_result)):
            # 预售商品
            if param["bizType"] == "PRE_SALE":
                sku_amount += sku_result[i]["pre_price"] * sku_num[i]
            elif param["bizType"] == "maintenance-factory":
                # 循环溢价数据计算价格
                for factory in factory_result:
                    for key in factory.keys():
                        if key == "sku_id" and factory[key] in sku_id:
                            sku_index = sku_id.index(factory[key])
                            factory["num"] = sku_num[sku_index]
                            break
                    # 累加sku总价
                    if factory["sku_id"] == sku_result[i]["sku_id"]:
                        sku_amount += (sku_result[i]["promotion_price"] + sku_result[i]["promotion_price"] *
                                       factory["premium_rate"] / 100)*factory["num"]

            else:
                sku_amount += sku_result[i]["promotion_price"] * sku_num[i]
        cls.log.debug(f"sku总价: {sku_amount}")
        # 从接口计算工时费
        hour_amount = 0
        for grep in cls.result["data"]["skuItemGroupList"]:
            for sku in grep["skus"]:
                if sku["name"] == "工时费":
                    hour_amount += sku["promotionPrice"] * sku["skuNum"]
        cls.log.debug(f"工时费: {hour_amount}")
        amount = sku_amount + hour_amount
        # 保养工时费
        if param["bizType"] == "maintenance-package":
            assert hour_amount > 0, "工时费错误"
        # 邮费计算
        if param["bizType"] in ["c-logistics", "PRE_SALE"]:
            freight = 0
            city = cls.user_vehicle_sql.exeCute(
                f"SELECT * FROM user_address_info WHERE id = {cls.result['data']['orderAddress']['userAddressId']}")
            freight_template_list = cls.items_sql.exeCute(f"SELECT sku_id,product_template_id FROM sku  LEFT JOIN item_"
                                                          f"verification_rule as rule ON sku.item_id=rule.item_id WHERE"
                                                          f" sku_id IN({utils.list_to_str(sku_id)}) and sku.deleted = 0"
                                                          f" and rule.deleted = 0", "all")
            # 合并sku数量邮费模版
            for i in freight_template_list:
                for j in list(zip(sku_id, sku_num)):
                    if j[0] == i["sku_id"]:
                        i.update({"sku_num": j[1]})
            cls.log.debug(freight_template_list)
            # 计算同一个邮费模版的总sku数量
            template_sku_num = {}
            for i in freight_template_list:
                # 设置一个默认的模版数量
                if not template_sku_num or i["product_template_id"] not in template_sku_num:
                    template_sku_num.update({i["product_template_id"]: i["sku_num"]})
                    continue
                if i["product_template_id"] in template_sku_num:
                    template_sku_num[i["product_template_id"]] += i["sku_num"]
            # 查询邮费模版计价
            for i in template_sku_num:
                template = cls.plutus_sql.exeCute(f"SELECT * FROM product_template_rule WHERE template_id = {i} and "
                                                  f"deleted =0", 'all')
                sku_freight = 0

                for temp in template:
                    if temp["city"] == "CN":
                        continue
                    elif str(city["district_id"]) in temp["city"]:
                        if temp["free_condition"] < template_sku_num[i] and temp["free_condition"] != 0:
                            cls.log.debug("城市包邮")
                            continue
                        else:
                            cls.log.debug("城市不包邮")
                            if temp["continue_num"] and template_sku_num[i] > temp["default_num"]:
                                sku_freight = temp["default_price"] + math.ceil(
                                    (template_sku_num[i] - temp["default_num"]) / temp["continue_num"]) * temp[
                                                  "continue_price"]
                            else:
                                sku_freight = temp["default_price"]
                if not sku_freight:
                    for temp in template:
                        if temp["city"] == "CN":
                            if temp["free_condition"] < template_sku_num[i] and temp["free_condition"] != 0:
                                cls.log.debug("全国包邮")
                                continue
                            else:
                                cls.log.debug("全国不包邮")
                                if temp["continue_num"] and template_sku_num[i] > temp["default_num"]:
                                    sku_freight = temp["default_price"] + math.ceil(
                                        (template_sku_num[i] - temp["default_num"]) / temp["continue_num"]) * temp[
                                                      "continue_price"]
                                else:
                                    sku_freight = temp["default_price"]
                freight += sku_freight
                cls.log.debug(sku_freight)
            cls.log.debug(template_sku_num)
            amount += freight
            cls.log.debug(f"计算邮费: {freight}")
        cls.log.debug(f"接口返回总价: {cls.result['data']['payAmount']}")
        cls.log.debug(f"计算总价: {amount}")
        assert int(amount) == cls.result["data"]["payAmount"], "渲染总金额计算错误"
