# -*- coding:utf-8 -*-
# Author: san yuan

import time
import hashlib
import json
import httpx
from urllib import parse
from pydantic import BaseModel


def sign(secret, parameters):
    str_parameters = ""
    if hasattr(parameters, "items"):
        keys = sorted(parameters.keys())
        str_parameters = "%s&%s" % ("&".join('%s=%s' % (key, parameters[key]) for key in keys), f"signSecret={secret}")
    print("str_parameters:", str_parameters)
    a_sign = hashlib.md5(str_parameters.encode("utf-8")).hexdigest()
    return a_sign


def mixStr(pstr):
    if isinstance(pstr, str):
        return pstr
    elif isinstance(pstr, bytes):
        return pstr.decode('utf-8')
    else:
        return str(pstr)


class KsException(Exception):

    def __init__(self):
        self.errorcode = None
        self.message = None
        self.subcode = None
        self.submsg = None
        self.application_host = None
        self.service_host = None

    def __str__(self, *args, **kwargs):
        sb = "errorcode=" + mixStr(self.errorcode) + \
             " message=" + mixStr(self.message) + \
             " subcode=" + mixStr(self.subcode) + \
             " submsg=" + mixStr(self.submsg) + \
             " application_host=" + mixStr(self.application_host) + \
             " service_host=" + mixStr(self.service_host)
        return sb


class RequestException(Exception):
    pass


class RestApi(object):
    # ===========================================================================
    # Rest api
    # ===========================================================================

    def __init__(self, appkey, secret, sign_secret):
        self.appkey = appkey
        self.secret = secret
        self.sign_secret = sign_secret
        self.version = 1
        self.signMethod = "MD5"
        self.base_url = "https://openapi.kwaixiaodian.com"
        self.__httpmethod = "GET"

    def get_api_name(self):
        return ""

    def get_version(self):
        return '1'

    def getMultipartParas(self):
        return []

    def getTranslateParas(self):
        return {}

    def _check_requst(self):
        pass

    def process_with_url_before_request(self):
        tmp_url = self.get_api_name().replace(".", "/")
        return self.base_url + "/" + tmp_url

    def getResponse(self, access_token, params: dict | BaseModel = {}, timeout=30):
        sys_parameters = {
            "appkey": self.appkey,
            "version": self.version,
            "method": self.get_api_name(),
            "timestamp": int(time.time()*1000),
            "access_token": access_token,
            "signMethod": self.signMethod,
        }
        url = self.process_with_url_before_request()
        if params:
            sys_parameters["param"] = json.dumps(params, ensure_ascii=False, default=lambda value: value.__dict__)
        sys_parameters["sign"] = sign(self.sign_secret, sys_parameters)
        if self.__httpmethod == 'POST':
            json_obj = httpx.post(url, data=sys_parameters, timeout=timeout).json()
        else:
            url = url + "?" + parse.urlencode(sys_parameters)
            json_obj = httpx.get(url, timeout=timeout).json()
        return json_obj
