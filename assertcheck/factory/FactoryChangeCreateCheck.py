class FactoryChangeCreateCheck:
    @staticmethod
    def check(cls, param):
        price_change_server = FactoryChangeCreateCheck.price_change_server(cls, param)
        FactoryChangeCreateCheck.price_change_server_config(cls, param, price_change_server)

    @staticmethod
    def price_change_server(cls, param):
        if "id" in param and param["id"]:
            db_result = cls.gaea_sql.exeCute(f"SELECT * FROM price_change_server WHERE id = {param['id']} and deleted "
                                             "= 0 ORDER BY id DESC")
        else:
            db_result = cls.gaea_sql.exeCute("SELECT * FROM price_change_server WHERE maintenance_id = 98 and deleted "
                                             "= 0 ORDER BY id DESC")
            cls.gaea_sql.exeCute(f"UPDATE  price_change_server SET deleted = 1 WHERE id = {db_result['id']}")
        assert db_result["work_hours_price"] == param["workHoursPrice"], "工时费存储错误"
        assert db_result["server_name"] == param["serverName"], "服务项名称错误"
        assert db_result["server_desc"] == param["serverDesc"], "服务描述错误"
        return db_result

    @staticmethod
    def price_change_server_config(cls, param, price_change_server):
        db_result = cls.gaea_sql.exeCute(f"SELECT * FROM price_change_server_config WHERE server_id = "
                                         f"{price_change_server['id']} and deleted = 0 ORDER BY id DESC", "all")
        assert len(db_result) == len(param["priceChangeConfigs"]), "坑位数量不一致"
        for db_info in db_result:
            for change_config in param["priceChangeConfigs"]:
                if db_info["maintenance_config_id"] == change_config["maintenanceConfigId"]:
                    assert db_info["valuation_flag"] == change_config["valuationFlag"], "改价状态错误"
                    assert db_info["config_num"] == change_config["configNum"], "改价默认数量错误"
                    if change_config["selectSkus"]:
                        sku_db_result = cls.gaea_sql.exeCute(f"SELECT * FROM price_change_server_config_sku WHERE "
                                                             f"server_config_id ={db_info['id']}", "all")
                        assert len(change_config["selectSkus"]) == len(sku_db_result), "sku总数错误"
                        for sku_info in change_config["selectSkus"]:
                            for db_sku_info in sku_db_result:
                                if db_sku_info["sku_id"] == sku_info["skuId"]:
                                    assert db_sku_info["default_status"] == sku_info["defaultStatus"], "默认sku状态错误"
