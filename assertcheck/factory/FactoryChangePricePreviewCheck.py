class FactoryChangePricePreviewCheck:
    @staticmethod
    def check(cls, param):
        FactoryChangePricePreviewCheck.result_check(cls, param)

    @staticmethod
    def result_check(cls, param):
        db_result = cls.gaea_sql.exeCute(f"SELECT config_num,sku_id,default_status,work_hours_price,valuation_flag "
                                         f"FROM price_change_server  INNER JOIN price_change_server_config ON price_"
                                         f"change_server.id = server_id INNER JOIN price_change_server_config_sku ON "
                                         f"price_change_server_config.id = server_config_id WHERE price_change_server"
                                         f".id = {param['serverId']} and price_change_server.deleted = 0 and price_"
                                         f"change_server_config_sku.deleted = 0 order by valuation_flag,default_status"
                                         f" desc", "all")
        param["changePrice"] *= 100
        param["changePrice"] -= db_result[0]["work_hours_price"]
        default_sku_price = 0
        for change_info in db_result:
            sku_info = cls.items_sql.exeCute(f"select * from sku where sku_id in ({change_info['sku_id']}) AND deleted"
                                             f" = 0", "all")
            if change_info["valuation_flag"] == 0 and change_info["default_status"] == 1:
                param["changePrice"] -= (sku_info[0]["promotion_price"] * change_info["config_num"])
                cls.log.debug(f"减去不参与改价的价格：{param['changePrice']}")
            if change_info["valuation_flag"] == 1 and change_info["default_status"] == 1:
                default_sku_price += (sku_info[0]["promotion_price"] * change_info["config_num"])
                cls.log.debug(f"参与改价的价格：{default_sku_price}")
        premium_rate = int((param["changePrice"] - default_sku_price) / default_sku_price * 10000)
        cls.log.debug(premium_rate)
        for result_change_info in cls.result["data"]["skuChangePriceResList"]:
            assert int(result_change_info["premiumRate"] * 100) == premium_rate
            assert int(result_change_info["skuOriginPrice"] * (1 + premium_rate / 10000)) == \
                   result_change_info["skuTargetPrice"]
