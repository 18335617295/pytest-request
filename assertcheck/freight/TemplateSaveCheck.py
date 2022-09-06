from libs import utils


class TemplateSaveCheck:
    @staticmethod
    def check(cls, param):
        template_id = TemplateSaveCheck.product_template_check(cls, param)
        TemplateSaveCheck.product_template_rule_check(cls, param, template_id)

    @staticmethod
    def product_template_check(cls, param):
        if "id" in param and param["id"]:
            db_result = cls.plutus_sql.exeCute(f"SELECT * FROM product_template WHERE id = {param['id']} "
                                               f"ORDER BY id DESC")
        else:
            db_result = cls.plutus_sql.exeCute("SELECT * FROM product_template WHERE deleted = 0 ORDER BY id DESC")
            cls.assert_equal(db_result["status"], 2, "状态错误")
        cls.log.debug(db_result)
        cls.assert_equal(db_result["template_name"], param["templateName"], "模版名称保存错误")
        cls.assert_equal(db_result["rule_type"], param["ruleType"], "计费类型错误")
        return db_result

    @staticmethod
    def product_template_rule_check(cls, param, template_id):
        db_result = cls.plutus_sql.exeCute(f"SELECT * FROM product_template_rule WHERE template_id = "
                                           f"{template_id['id']} and deleted =0", "all")
        for template in db_result:
            for par in param["templateRules"]:
                if template["city"] == utils.list_to_str(par["citys"]):
                    cls.log.debug(template)
                    cls.assert_equal(template["default_num"], par["defaultNum"], "首件数量错误")
                    cls.assert_equal(template["default_price"], par["defaultPrice"] * 100, "首件价格错误")
                    cls.assert_equal(template["continue_num"], par["continueNum"], "续件数量错误")
                    cls.assert_equal(template["continue_price"], par["continuePrice"] * 100, "续件价格错误")
                    cls.assert_equal(template["free_condition"], par["freeCondition"], "包邮数量错误")

    @staticmethod
    def product_template_status_check(cls, param):
        db_result = cls.plutus_sql.exeCute(f"SELECT * FROM product_template WHERE id = {param['id']} "
                                           f"ORDER BY id DESC")
        cls.log.debug(db_result)
        cls.assert_equal(db_result["status"], param["status"], "状态错误")
