#!/usr/bin/env python3
import json
import os

import allure
import requests

from conf.GlobalConfig import GlobalConfig
from libs import utils
from libs.Base import Base


class Requests(Base):
    def __init__(self):
        self.account_dict = utils.yaml_file(GlobalConfig.ENV, None, f"..{os.sep}conf", "Account")
        self.curl_result = os.popen("curl --location --request POST 'https://int-athena.test.haochezhu.club/api-factory"
                                    "/internal/oauth/authorizeToken?mobile=18335617295' --header 'channel-id: tnclYoifI"
                                    "de0XVBBsVfUT3GoPHKV8H'").read()

    def get_token_to_b(self, account=1):
        data = {
            "username": self.account_dict[account]["username"],
            "password": self.account_dict[account]["password"]
        }
        result = requests.post("https://sso.test.haochezhu.club/api/v2/impersonation", data=data)
        return f"Bearer {result.json()['data']['token']['access_token']}"

    def get_cookie_to_b(self, headers):
        result = requests.put("https://bffv2.uat.haochezhu.club/aep-hades/api/session/shops/221620803889484",
                              headers=headers)
        return result.cookies

    def get_token_to_c(self, account=3):
        data = {
            "appid": "210001",
            "ver": 2,
            "plat": 1,
            "v": "2.2.0",
            "phone": self.account_dict[account]["username"],
            "vcode": 2222,
            "contractor": 0,
        }
        data.update({"sign": utils.get_appid_sign(data, data["appid"])})
        result = requests.post("https://pay.test.haochezhu.club/channel/auth/login", data=data)
        return result.cookies

    @allure.step('发送post请求')
    def form_post(self, url, data=None, **kwargs):
        """
        from_data格式post
        :param url: url
        :param data: 参数
        :param headers:  headers
        :param cookies: cookies
        :param token: url是否是获取token,自动化case不传
        :return:
        """
        try:
            allure.attach(str(data), "请求参数")
        except KeyError:
            pass
        ret = self.request("post", url, data=data, **kwargs)
        return ret

    @allure.step('发送delete请求')
    def delete(self, url, data=None, **kwargs):
        """
        发送delete请求
        :param url:
        :param data:
        :param headers:
        :param cookies:
        :return:
        """
        try:
            allure.attach(str(data), "请求参数")
        except KeyError:
            pass
        ret = self.request("delete", url, params=data, **kwargs)
        return ret

    @allure.step('发送get请求')
    def get(self, url, data=None, **kwargs):
        """
        发送get请求
        :param url:
        :param data:
        :param headers:
        :param cookies:
        :return:
        """
        try:
            allure.attach(str(data), "请求参数")
        except KeyError:
            pass
        ret = self.request("get", url, params=data, **kwargs)
        return ret

    @allure.step('发送post请求')
    def json_post(self, url, data=None, **kwargs):
        """
        json格式的post
        :param url:
        :param data: 字典
        :param headers: 字典
        :param cookies: 字典
        :return:
        """
        try:
            allure.attach(str(data), "请求参数")
        except KeyError:
            pass
        ret = self.request("post", url, json=data, **kwargs)
        return ret

    def request(self, method, url, **kwargs):
        """
        :param method: 例: post
        :param url: 例: http://132.com/{page}/info
        :param headers: 例: header
        :param cookies: 例: cookies
        :param data:
        :return:
        """
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        # 自动添加token
        if utils.get_ip() in url:
            if "account" in kwargs:
                token = self.get_token_to_b(kwargs["account"])
            else:
                token = self.get_token_to_b()
            kwargs["headers"].update({
                "Authorization": token
            })
            kwargs["cookies"] = self.get_cookie_to_b(kwargs["headers"])
        else:
            if "account" in kwargs:
                kwargs["cookies"] = self.get_token_to_c(kwargs["account"])
            else:
                kwargs["cookies"] = self.get_token_to_c()
        if "/aep-vulcan/" in url:

            curl_result = json.loads(self.curl_result)
            kwargs["cookies"] = {"VU-FACTORY-TOKEN": curl_result["data"]["token"]}
        if "data" in kwargs and kwargs["data"]:
            data = kwargs["data"]
        elif "json" in kwargs and kwargs["json"]:
            data = kwargs["json"]
        elif "params" in kwargs and kwargs["params"]:
            data = kwargs["params"]
        else:
            data = ""
        if "{" in url and "}" in url and data:
            url = self.url_analysis(url, data)
        kwargs["timeout"] = 5
        try:
            self.log.info("请求url  " + url)
            self.log.info("接口参数  " + str(data))
            if "account" in kwargs:
                del kwargs["account"]
            ret = requests.request(method, url, **kwargs)
            self.log.info(ret)
            ret = ret.json()
            self.log.info("接口返回  " + str(ret))
            return ret
        except requests.RequestException as e:
            self.log.error(f"{url}  调用失败")
            self.log.error(f"{e}")

    @staticmethod
    def url_analysis(url, data):
        """
        解析url中的参数
        :param url: 例: http://132.com/{page}/info
        :param data:
        :return:
        """
        for i in data:
            if i in url:
                url = url.replace("{"+i+"}", str(data[i]))
            else:
                continue
        return url

    @allure.step('发送put请求')
    def put(self, url, data=None, **kwargs):
        """
        :param url:
        :param data:
        :param headers:
        :param cookies:
        :return:
        """
        try:
            allure.attach(str(data), "请求参数")
        except KeyError:
            pass
        ret = self.request("put", url, params=data, **kwargs)
        return ret


if __name__ == "__main__":
    request = Requests()
