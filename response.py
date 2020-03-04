# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     response.py
   Description :
   Author :       tangjiawei
   date:          2018/08/23
-------------------------------------------------
   Change Activity:
                   2018/08/23: v1
-------------------------------------------------
"""


class Response(object):
    """
        获得响应内容和状态码
    """
    def __init__(self, status_code, result):
        self.status_code = status_code
        self.response = result

    def __repr__(self):
        res = ""
        res += "#" * 50 + '\n'
        res += "status_code: {}\n".format(self.status_code)
        res += "-------------------------response----------------------\n"
        res += str(self.response) + '\n'
        return res
