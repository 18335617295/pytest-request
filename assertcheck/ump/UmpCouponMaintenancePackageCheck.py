from libs import utils


class UmpCouponMaintenancePackageCheck:
    @staticmethod
    def code_check(cls):
        uat = utils.list_dict_to_list(cls.result["data"]["platformDeductCouponList"], "performanceType")
        cls.log.info(uat)
        assert cls.result["code"] == 1, "可用优惠券到家code错误"
        for i in uat:
            assert i in [2, 3], "保养可用优惠券列表数据出现到家优惠券"
