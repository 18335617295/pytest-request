import time
import json
import pytest

from conf.GlobalConfig import GlobalConfig
from libs import utils
from libs.Mq import MyMq
from libs.MySQL import MySqlHandler
from libs.Requests import Requests


def run_env(env="uat"):
    """
    切换环境
    :param env:  "uat", "sim", "dev", "pro"
    :return:
    """
    if env in GlobalConfig.ENV_LIST:
        GlobalConfig.ENV = env
    else:
        GlobalConfig.ENV = "uat"

    def dec2(cls):
        return cls

    return dec2


request = Requests()
tp_sql = MySqlHandler(f"gd_tp_{GlobalConfig.ENV}")


@pytest.fixture
def order_create():
    tp_order_create()


def tp_order_create():
    url = utils.get_ip("ToC") + utils.yaml_file("TestTpOrderCreate", None, 'tp', "Api")
    data = utils.yaml_file("TestTpOrderCreate", "test_order_create_succeed", "tp")
    render_data = tp_order_render()
    render_data.pop(1)
    for i in range(len(data)):
        try:
            # 把渲染返回结果替换yaml参数
            data[i][0]["param"].update(render_data[i][0])
            # 替换skulist
            data[i][0]["param"]["skuInfoList"] = render_data[i][0]["skuItemGroupList"][0]["skus"]
        except Exception as e:
            print(e)
            continue
    result = []
    for i in data:
        result.append(request.json_post(url, i[0]["param"]))
    time.sleep(1)
    return result


@pytest.fixture
def order_pay():
    tp_order_pay()


def tp_order_pay():
    data = utils.yaml_file("TestTpOrderPay", "test_order_py_succeed", "tp")[0][0]["param"]
    for i in tp_order_create():
        try:
            data["message"]["payOrderNo"] = i["data"]["payNo"]
            MyMq().send_msg(data)
        except Exception as e:
            print(e)
    time.sleep(2)


@pytest.fixture
def performance_start():
    tp_performance_start()


def tp_performance_start():
    tp_order_pay()
    performance_sql = MySqlHandler(f"gd_performance_{GlobalConfig.ENV}")
    url = utils.yaml_file("TestPerformanceServiceStart", None, 'performance', "Api")
    data = utils.yaml_file("TestPerformanceServiceStart", "test_performance_service_start", "performance")[0][0]
    db_result = performance_sql.exeCute(data["sql"])
    data["param"]["orderNo"], data["param"]["voucherCode"] = db_result["order_no"], db_result["voucher_no"]
    data["param"]["serviceNo"] = db_result["service_no"]
    request.json_post(url, data["param"])
    time.sleep(1)


def ump_sku_add():
    url = utils.get_ip("ToB") + utils.yaml_file("TestUmpAddSku", None, 'ump', "Api")
    data = utils.yaml_file("TestUmpAddSku", "test_coupon_sku_add_succeed", "ump")
    sku_add = request.json_post(url, data[0][0]["param"])
    return sku_add["data"]["couponItemInfoId"]


# 退款申请单参数
def after_sales_apply():
    tp_order_pay()
    data = utils.yaml_file("TestTpOrderAfterSalesApply", "test_order_after_sales_apply", "tp")
    for i in tp_sql.exeCute(data[0][0]["sql"], "all"):
        data[0][0]["param"]["orderNo"] = i["order_no"]
        del i["order_no"]
        i["skuNo"] = json.loads(i["snapshot"])["skuNo"]
        del i["snapshot"]
        sku_dict = {
            "skuId": int(i["sku_no"]),
            "skuNo": i["skuNo"],
            "skuNum": i["sku_num"]
        }
        data[0][0]["param"]["skuList"].append(sku_dict)
    return data


def tp_order_render():
    url = utils.get_ip("ToC") + utils.yaml_file("TestTpOrderRender", None, 'tp', "Api")
    data = utils.yaml_file("TestTpOrderRender", "test_order_render_succeed", "tp")
    result = []
    for i in data:
        ret = request.json_post(url, i[0]["param"])['data']
        result.append((ret, i[0]["case_name"]))
    return result


if __name__ == '__main__':
    print(tp_order_create())
