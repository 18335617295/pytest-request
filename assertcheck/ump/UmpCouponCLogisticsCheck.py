from libs import utils


class UmpCouponCLogisticsCheck:
    @staticmethod
    def code_check(cls):
        uat = utils.list_dict_to_list(cls.result["data"]["platformCouponList"], "performanceType")
        assert cls.result["code"] == 1, "可用优惠券code错误"
        for i in uat:
            assert i in [1, 3], "到家可用优惠券出现到店优惠券"
