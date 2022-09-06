from assertcheck.CodeCheck import CodeCheck


class TpOrderListCheck:
    @staticmethod
    def check(cls, param):
        CodeCheck.tp_code_check(cls)
        TpOrderListCheck.result_check(cls, param)

    @staticmethod
    def result_check(cls, param):
        db_count = cls.tp_sql.exeCute(param["sql"])
        cls.log.debug(db_count)
        if param["param"]["frontOrderStatus"] != 1:
            cls.assert_no_equal(cls.result["data"]["records"], [], "校验失败借口数据为空")
