# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:     HugeGraph.py
   Description :
   Author :       bdlddn
   date:          2019/07/05
-------------------------------------------------
   Change Activity:
                   2019/07/05: v1
-------------------------------------------------
"""
import json

import requests

from .response import Response
from .schema_manager import SchemaManager
from .graph_manager import GraphManager
from .huge_graph_class import HugeGraphBase
from .traverser_manager import Traverser


class HugeGraphClient(HugeGraphBase):
    """
    HugeGraph restful API
    """
    def __init__(self, host, graph_name, timeout):
        super().__init__(host, graph_name, timeout)
        self._token = "162f7848-0b6d-4faf-b557-3a0797869c55"
        self._conform_message = "I%27m+sure+to+delete+all+data"
        self._schema = None
        self._graph = None
        self._traverser = None

    def schema(self):
        if self._schema:
            return self._schema
        self._schema = SchemaManager(self._host, self._graph_name, self.timeout)
        return self._schema

    def graph(self):
        if self._graph:
            return self._graph
        self._graph = GraphManager(self._host, self._graph_name, self.timeout)
        return self._graph

    def traverser(self):
        if self._traverser:
            return self._traverser
        self._traverser = Traverser(self._host, self._graph_name, self.timeout)
        return self._traverser

    # 下面是通用方法
    def get_all_graphs(self):
        """
        列出数据库中全部的图（传统数据库中的数据库database）
        :return:
        """
        url = self._host + "/graphs"
        response = requests.get(url, headers=self._headers)
        res = Response(response.status_code, response.content)
        return res

    def get_version(self):
        """
        查看HugeGraph的版本信息
        :return:
        """
        url = self._host + "/versions"
        response = requests.get(url, headers=self._headers)
        res = Response(response.status_code, response.content)
        return res

    def get_graphinfo(self):
        """
        查看某个图的信息
        :return:
        """
        url = self._host + "/graphs" + "/" + self.graph
        response = requests.get(url, headers=self._headers)
        res = Response(response.status_code, response.content)
        return res

    def clear_graph_all_data(self):
        """
        清空某个图的全部数据，包括schema、vertex、edge和索引等，该操作需要管理员权限
        :return:
        """
        # url = self._host + "/graphs" + "/" + self.graph + "clear?token=" + \
        #       self._token + "&confirm_message=" + self._conform_message
        url = self._host + "/graphs" + "/" + self._graph_name + "clear?" + \
              "confirm_message=" + self._conform_message
        response = requests.delete(url, headers=self._headers)
        res = Response(response.status_code, response.content)
        return res

    def get_graph_config(self):
        """
        查看某个图的配置，该操作需要管理员权限
        :return:
        """
        url = self._host + "/graphs" + "/" + self.graph + "conf?token=" + self._token
        response = requests.get(url, headers=self._headers)
        res = Response(response.status_code, response.content)
        return res