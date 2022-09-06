class UmpCouponGetCheck():
    @staticmethod
    def check(cls):
        DB_ump_info = cls.ump_sql.exeCute("SELECT m.coupon_id,i.coupon_template_info_id from coupon_info i,my_coupon_info m where i.coupon_id = m.coupon_id and  i.coupon_template_info_id = \"cf2163641b0b429c8af435901dd3b89e\"")
        cls.log.debug(DB_ump_info)

        DB_ump_my_info = cls.ump_sql.exeCute(f"SELECT * from my_coupon_info where coupon_id = \"{DB_ump_info['coupon_id']}\"")
        cls.log.debug(DB_ump_my_info)
        cls.assert_equal(DB_ump_info["coupon_template_info_id"], "cf2163641b0b429c8af435901dd3b89e", "领取优惠券错误")

    @staticmethod
    def delete_sql(cls):
        DB_ump_info = cls.ump_sql.exeCute("SELECT m.coupon_id from coupon_info i,my_coupon_info m where i.coupon_id = m.coupon_id and  i.coupon_template_info_id = \"cf2163641b0b429c8af435901dd3b89e\"")
        uat=cls.ump_sql.exeCute(f"delete from my_coupon_info where coupon_id = \"{DB_ump_info['coupon_id']}\"")
        cls.log.debug(uat)
        uct=cls.ump_sql.exeCute(f"delete from coupon_info where coupon_id = \"{DB_ump_info['coupon_id']}\"")
        cls.log.debug(uct)

    @staticmethod
    def code_check(cls):
        assert cls.result["code"] ==1 , "领取优惠券场景code错误"
        assert cls.result["data"]["couponName"] == "自动化用优惠券勿动", "领取优惠券场景data coupon_name错误"


    @staticmethod
    def check_fail(cls):
        assert cls.result["code"] == 3046 , "领取优惠券重复场景code错误"
        assert cls.result["msg"] == "您已经领取过了" , "领取优惠券重复场景msg错误"
