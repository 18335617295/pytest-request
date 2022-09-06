
class UmpCouponAddCheck:

    @staticmethod
    def check(cls, param):
        UmpCouponAddCheck.code_check(cls)
        DB_ump = cls.ump_sql.exeCute(f"select * from coupon_template_info where coupon_template_name = \"{param['couponTemplateName']}\"")
        cls.log.debug(DB_ump)
        DB_ump_info = cls.ump_sql.exeCute(f"select * from coupon_discount_template_rule_info where coupon_template_name = \"{param['couponTemplateName']}\"")
        cls.log.debug(DB_ump_info)
        DB_ump_rules = cls.ump_sql.exeCute(f"select * from coupon_receive_rules_info where rules_no = \"{DB_ump['rules_no']}\"")

        cls.log.debug(DB_ump_rules)
        # 1 = 满减券
        # 2 = 满折券
        # 3 = 抵用券
        if param["couponType"] == 2:
            cls.assert_equal(DB_ump_info["coupon_discount_prefix"], "30000.0", "优惠券折扣错误")
            cls.assert_equal(DB_ump_info["coupon_discount_surfix"], "7.0", "优惠券折扣错误")
        elif param["couponType"] == 3:
            cls.assert_equal(DB_ump_info["coupon_discount_prefix"], "0.0", "优惠券抵用错误")
            cls.assert_equal(DB_ump_info["coupon_discount_surfix"], "3000.0", "优惠券抵用错误")
        cls.assert_equal(DB_ump_rules["receive_once_num"], 1,"优惠券领取规则错误")
        if param["thirdCategoryIdList"] :
            cls.assert_equal(DB_ump_info["coupon_selected_type"], 2, "指定类目类型错误")
        cls.assert_equal(DB_ump["coupon_use_type"], 1, "优惠券类型错误（平台）")

    @staticmethod
    def code_check(cls):
        assert cls.result["code"] == 1, "code验证失败"
        assert cls.result["data"] == "添加成功" , "data验证失败"
        assert cls.result["msg"] == "ok", "msg验证失败"

    @staticmethod
    def check_fail(cls):
        assert cls.result["code"] == -1, "code验证失败"
        assert cls.result["msg"] == "添加失败,优惠券名称重复", "msg验证失败"