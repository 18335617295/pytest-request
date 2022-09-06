#!/bin/env python

import difflib
import hashlib
import linecache
import json
import os
import threading

import yaml

from conf.GlobalConfig import GlobalConfig

threadLock = threading.Lock()

root_dir = GlobalConfig.ROOT_DIR


def num_str_to_sorted_num_list(str, decollator, is_int=True):
    """
    数字字符串转列表
    :param str:  "1,3,4,5"
    :param decollator 切割符号
    :param is_int 是否转int 默认转
    :return: [1,3,4,5]
    """
    str_list = str.split(decollator)
    if is_int:
        num_list = [int(i) for i in str_list]
    else:
        num_list = str_list
    num_list.sort()
    return sorted(num_list)


def md5(preosign):
    """
    md5加密
    :param preosign: 加密串
    :return:
    """
    m = hashlib.md5()
    preosign = preosign.encode('utf-8')
    m.update(preosign)
    return m.hexdigest()


def md5_file(file_name):
    """
    :param file_name: 加密文件名称
    :return: (加密串,文件大小)
    """
    m = hashlib.md5()
    with open(root_dir + f"{os.sep}data{os.sep}{file_name}", 'rb') as f:
        m.update(f.read())
    return m.hexdigest(), os.path.getsize(root_dir + f"{os.sep}data{os.sep}{file_name}")


def dict_2_str(dictin):
    """
    将字典变成，key='value',key='value' 的形式
    """
    tmplist = []
    for k, v in dictin.items():
        tmp = "%s=%s" % (str(k), str(v))
        tmplist.append(tmp)
    tmplist.sort()
    return '&'.join(tmplist)


def get_appid_sign(dict, key):
    """
    :param dict: 参数
    :param key: 固定串的key
    :return: 加密后的串
    """
    value = dict_2_str(dict)
    appid_dict = {
        "210001": "3gkcyhreglmp7chvg6k8ntkf5ymo1ark",
        "992001": "e74cb4423b4c4c23bc3d19437f52958a"
    }
    return md5(value + appid_dict[key])


def yaml_file(file_name, key, path="", outer_key="Input", index=None):
    """
    :param file_name: 数据文件名称
    :param key: 数据参数key
    :param outer_key: 最外层key,默认Input
    :param path: 数据文件路径,默认data
    :param index: 指定下标参数
    :return: 参数化list
    """
    with open(root_dir + f"{os.sep}data{os.sep}{path}{os.sep}{file_name}.yml", "r", encoding='UTF-8') as f:
        try:
            yam_data = yaml.load(f, Loader=yaml.FullLoader)
            if outer_key in yam_data:
                case_data = yam_data[outer_key]
            else:
                return None
            # 外层key直接返回值
            if outer_key not in ["Template", "Input"]:
                return case_data
            # 参数模板
            if "Template" in yam_data:
                template_data = yam_data["Template"]
            else:
                template_data = {}
            data_list = []
            # 获取指定下标数据
            if index:
                for i in index:
                    data_list.append(case_data[key][i])
            else:
                data_list = list(case_data[key].values())
            case_name = []
            # case_list = []
            # 合并模板与实际参数
            for i in data_list:
                case_name.append(i["case_name"])
                if template_data:
                    i["param"] = (dict_merge(template_data, i["param"]))
                    # case_list.append(dict_merge(template_data, i["param"]))
                # else:
                # case_list.append(i["param"])

            return list(zip(data_list, case_name))
        except Exception as e:
            raise e


def get_result_list(file_path):
    """
    :param file_path: 从json文件获取执行结果
    :return: 结果list
    """
    case_info = []
    for i in linecache.getlines(file_path):
        with open(i.strip(), 'r')as f:
            case_info.append(json.load(f))
    return case_info


def file_split(file, split_size=4194304):
    """
    文件切片
    :param file: 切割的源文件
    :param split_size: 指定大小
    :return: 切割后文件名list
    """
    file_list = []
    file_path = (root_dir + f"{os.sep}data{os.sep}{file}")
    file_size = os.path.getsize(file_path)
    file_extension = os.path.splitext(file_path)[1]
    i = 0
    while file_size > 0:
        split_info = {
            "size": split_size if (file_size >= split_size) else file_size,
            "file": file_path.replace(f"{file_extension}", "_" + str(i) + f"{file_extension}"),
            "index": i
        }
        file_size -= split_size
        file_list.append(split_info)
        i += 1
    with open(file_path, "rb") as f0:
        for i in file_list:
            with open(i["file"], "wb") as f1:
                f1.write(f0.read(i["size"]))
    return file_list


# 文件对比
def file_diff(file1, file2):
    """
    文件对比
    :param file1: 文件1
    :param file2: 文件2
    :return:
    """
    f1 = read_file(file1)
    f2 = read_file(file2)
    diff = difflib.HtmlDiff()
    with open(f"{root_dir}{os.sep}data{os.sep}diff_{file1}_{file2}.html", "w")as f:
        f.write("<meta charset='UTF-8'>")
        f.write(diff.make_file(f1, f2))
    print("文件比对完成")
    return "文件比对完成"


def read_file(file):
    with open(f"{root_dir}{os.sep}data{os.sep}{file}", "r", encoding='UTF-8') as f:
        return f.read().splitlines()


def dict_merge(d1, d2):
    """
    合并字典
    :param d1: 字典1,大字典
    :param d2: 字典2
    :return: 合并后字典
    """
    result_dict = {}
    # 如果第二个字典为空直接返回第一个字典
    if not d2:
        return d1.copy()
    # 循环key合并字典
    for i in d1:
        if i in d2:
            # 类型是字典时递归合并
            if type(d1[i]) is dict:
                dic = dict_merge(d1[i], d2[i])
                result_dict[i] = dic
                continue
            result_dict[i] = d2[i]
        else:
            result_dict[i] = d1[i]
    # 合并后字典去除指定key
    for i in list(result_dict.keys()):
        if result_dict[i] is None:
            result_dict.pop(i)

    return result_dict


def get_ip(env="ToB"):
    """
    根据全局变量获取域名
    :param env B代表调用b端域名  C代表调用c端域名
    :return: 域名
    """
    if GlobalConfig.ENV == "uat" and "ToB" in env:
        server = yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", outer_key="Services_name")
        return server["to_b"]
    elif GlobalConfig.ENV == "uat" and "ToC" in env:
        server = yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", outer_key="Services_name")
        return server["to_c"]
    elif GlobalConfig.ENV == "sim" and "ToB" in env:
        server = yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", outer_key="Services_name")
        return server["to_c"]
    elif GlobalConfig.ENV == "sim" and "ToC" in env:
        server = yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", outer_key="Services_name")
        return server["to_c"]
    elif GlobalConfig.ENV == "pro" and "ToB" in env:
        server = yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", outer_key="Services_name")
        return server["to_c"]
    elif GlobalConfig.ENV == "pro" and "ToC" in env:
        server = yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", outer_key="Services_name")
        return server["to_c"]
    else:
        server = yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", outer_key="Services_name")
        return server["to_c"]


def list_dict_to_list(l1, key, sort=False):
    """
    字典list转列表,只能是指定格式,排序只支持正序,默认不排序
    :param l1: 例:[{'skuId': 967, 'skuNum': 4, 'context': {'configId': 639, 'serviceId': 68}, 'hidden': 1}]
    :param key: 指定key
    :param sort: 是否排序
    :return:
    """
    l2 = []
    for i in l1:
        if key in i:
            l2.append(i[key])
    if sort:
        l2.sort()
    return l2


def set_global_env(env):
    """
    设置全局环境
    :param env: "uat", "sim", "dev", "pro"
    """
    threadLock.acquire()
    GlobalConfig.ENV = env
    threadLock.release()


def list_to_str(list):
    """
    数字列表转字符串 [1,2,3] "1,2,3"
    :param list:
    :return:
    """
    new_str = ""
    for i in list:
        new_str += str(i) + ","
    return new_str.rstrip(",")


def get_path(class_name, format=".py", index=-2):
    print(f'find {GlobalConfig.ROOT_DIR} -name "{class_name}{format}"')
    return os.popen(f'find {GlobalConfig.ROOT_DIR} -name "{class_name}{format}"').read().split("/")[index]


def hump_to_underline(hump: str):
    underline = hump[0].lower()
    for i in range(1, len(hump)):
        if hump[i].isupper():
            underline += f"_{hump[i].lower()}"
        else:
            underline += hump[i]
    return underline


if __name__ == '__main__':
    # print(list_dict_to_list([{'business_application': 1}, {'business_application': 2}]))
    print(yaml_file("TpOrderRenderTest", "test_order_render_succeed"))

