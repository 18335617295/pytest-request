class FactoryChangeMaintenanceCheck:
    @staticmethod
    def check(cls, param):
        FactoryChangeMaintenanceCheck.result_check(cls, param)

    @staticmethod
    def result_check(cls, param):
        assert cls.result["data"]["serverId"] == param["serverId"], "服务ID不一致"
        db_result = cls.gaea_sql.exeCute(f"SELECT * FROM price_change_server WHERE id = {param['serverId']} and "
                                         f"deleted = 0")
        assert db_result["server_name"] == cls.result["data"]["serverName"]
        assert db_result["server_no"] == cls.result["data"]["serverNo"]
        change_sku_list = cls.gaea_sql.exeCute(f"SELECT config_num,sku_id,default_status,work_hours_price FROM "
                                               f"price_change_server  INNER JOIN price_change_server_config ON "
                                               f"price_change_server.id = server_id INNER JOIN price_change_ser"
                                               f"ver_config_sku ON price_change_server_config.id = server_conf"
                                               f"ig_id WHERE price_change_server.id = {param['serverId']} and "
                                               f"price_change_server.deleted = 0 and price_change_server_conf"
                                               f"ig_sku.deleted = 0 AND valuation_flag = 1", "all")
        assert len(change_sku_list) == len(cls.result["data"]["skuChangePriceResList"]), "改价详情数量不一致"
        for skuChangePriceRes in cls.result["data"]["skuChangePriceResList"]:
            for change_sku in change_sku_list:
                if skuChangePriceRes["skuId"] == change_sku["sku_id"]:
                    sku_premium_rate = cls.gaea_sql.exeCute(f"SELECT * FROM store_change_sku WHERE store_id = "
                                                            f"{skuChangePriceRes['storeId']} and sku_id = "
                                                            f"{change_sku['sku_id']} and deleted = 0 and server_id ="
                                                            f"{param['serverId']}")
                    if sku_premium_rate:
                        cls.log.debug(type(skuChangePriceRes["premiumRate"]))
                        cls.log.debug(type(sku_premium_rate["premium_rate"]))
                        assert str(skuChangePriceRes["premiumRate"]) == str(sku_premium_rate["premium_rate"]), "溢价率错误"
                        assert skuChangePriceRes["serialNum"] == sku_premium_rate["serial_num"], "流水号错误"
                    else:
                        assert skuChangePriceRes["premiumRate"] == 0, "溢价率错误"

