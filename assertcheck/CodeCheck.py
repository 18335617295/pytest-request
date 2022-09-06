class CodeCheck:
    @staticmethod
    def tp_code_check(cls):
        assert cls.result["code"] == 1, "code 校验失败"
        assert cls.result["data"] is not None, "返回数据结果"
        assert cls.result["msg"] == "ok", "msg 校验失败"

    @staticmethod
    def code_check(cls, expect):
        assert cls.result["code"] == expect["code"], "code 校验失败"
        assert cls.result["data"] == expect["data"], "返回数据校验失败"
        assert cls.result["msg"] == expect["msg"], "msg 校验失败"
