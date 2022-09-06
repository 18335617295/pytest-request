class FactoryChangeMaintenanceListCheck:
    @staticmethod
    def check(cls):
        FactoryChangeMaintenanceListCheck.list_check(cls)

    @staticmethod
    def list_check(cls):
        assert cls.result["code"] == 1, "接口code验证失败"
        for maintenanceGroup in cls.result["data"]["maintenanceGroupResList"]:
            for maintenanceList in maintenanceGroup:
                if not isinstance(maintenanceGroup[maintenanceList], list):
                    continue
                for serverDetailDetailRes in maintenanceGroup[maintenanceList]:
                    print(maintenanceGroup[maintenanceList])
                    print(serverDetailDetailRes)
                    for serverDetailDetail in serverDetailDetailRes["serverDetailDetailRes"]:
                        db_result = cls.gaea_sql.exeCute(f"SELECT config_num,sku_id,default_status,work_hours_price "
                                                         f"FROM price_change_server  INNER JOIN price_change_server_"
                                                         f"config ON price_change_server.id = server_id INNER JOIN pr"
                                                         f"ice_change_server_config_sku ON price_change_server_config."
                                                         f"id = server_config_id WHERE price_change_server.id = "
                                                         f"{str(serverDetailDetail['serverId'])} and price_change_"
                                                         f"server.deleted = 0 and price_change_server_config_sku."
                                                         f"deleted = 0", "all")
                        originPrice = targetPrice = 0
                        cls.log.debug("*" * 100)
                        for serverDetail in db_result:
                            cls.log.debug(serverDetailDetail['serverId'])
                            if serverDetail["default_status"]:
                                cls.log.debug("-"*100)
                                cls.log.debug(serverDetail)
                                cls.log.debug("-"*100)
                                items_result = cls.items_sql.exeCute(f"select * from sku where sku_id in ("
                                                                     f"{str(serverDetail['sku_id'])}) AND deleted =0",
                                                                     "all")
                                originPrice += items_result[0]["promotion_price"] * serverDetail["config_num"]
                                change_sku_result = cls.gaea_sql.exeCute(f"SELECT * FROM store_change_sku WHERE store_"
                                                                         f"id = 231624529234580 and sku_id = "
                                                                         f"{serverDetail['sku_id']} and deleted = 0 and"
                                                                         f" server_id = "
                                                                         f"{serverDetailDetail['serverId']}")
                                if not change_sku_result:
                                    targetPrice += items_result[0]["promotion_price"] * serverDetail["config_num"]
                                    cls.log.debug(targetPrice)
                                else:
                                    targetPrice += (items_result[0]["promotion_price"] + (items_result[0][
                                        "promotion_price"] * change_sku_result["premium_rate"]) / 100) * \
                                                   serverDetail["config_num"]
                                    cls.log.debug(targetPrice)
                        if targetPrice == 0:
                            targetPrice = originPrice
                        originPrice += db_result[0]["work_hours_price"]
                        targetPrice += db_result[0]["work_hours_price"]
                        cls.log.debug(f"溢价前价格： {originPrice}")

                        cls.log.debug(f"溢价后价格： {targetPrice}")
                        cls.log.debug(serverDetailDetail["originPrice"])
                        cls.log.debug(serverDetailDetail["targetPrice"])
                        assert int(originPrice) == int(serverDetailDetail["originPrice"])
                        assert int(targetPrice) == int(serverDetailDetail["targetPrice"])

