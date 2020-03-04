import json, os

import requests

from .graph_data_class import PropertyKeyData, VertexLabelData, EdgeLabelData, IndexLabelData
from .huge_graph_class import HugeGraphBase, EdgeLabel, PropertyKey, VertexLabel, IndexLabel
from .exceptions import NotFoundError
from .util import log


class SchemaManager(HugeGraphBase):
    def __init__(self, host, graph_name, timeout):
        super().__init__(host, graph_name, timeout)

    def propertyKey(self, property_name):
        property_key = PropertyKey(self._host, self._graph_name, self.timeout)
        property_key.create_parameter_holder()
        property_key.add_parameter("name", property_name)
        property_key.add_parameter("not_exist", True)
        return property_key

    def getPropertyKey(self, property_name):
        """
            根据name获取PropertyKey
            :param
            property_name:
            :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys" \
              + "/" + property_name
        response = requests.get(url)
        # res = Response(response.status_code, response.content)
        # warning 如果通讯失败应该判断status_code
        if response.status_code == 200:
            property_keys_data = PropertyKeyData(json.loads(response.content))
            return property_keys_data
        else:
            raise NotFoundError("PorpertyKey not found: {}".format(response.content))

    def getPropertyKeys(self):
        """
            根据获取所有PropertyKey
            :param
            property_name:
            :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys"
        response = requests.get(url)
        res = []
        for item in json.loads(response.content)["propertykeys"]:
            res.append(PropertyKeyData(item))
        return res

    def vertexLabel(self, vertex_name):
        vertex_label = VertexLabel(self._host, self._graph_name, self.timeout)
        vertex_label.create_parameter_holder()
        vertex_label.add_parameter("name", vertex_name)
        # vertex_label.add_parameter("id_strategy", "AUTOMATIC")
        vertex_label.add_parameter("not_exist", True)
        return vertex_label

    def getVertexLabel(self, name):
        """
        按name获取VertexLabel
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/vertexlabels/" + name
        response = requests.get(url, headers=self._headers)
        if response.status_code == 200:
            res = VertexLabelData(json.loads(response.content))
            return res
        else:
            raise NotFoundError("VertexLabel not found: {}".format(response.content))

    def getVertexLabels(self):
        """
        获取VertexLabel全部
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/vertexlabels/"
        response = requests.get(url, headers=self._headers)
        res = []
        for item in json.loads(response.content)["vertexlabels"]:
            res.append(VertexLabelData(item))
        return res

    def edgeLabel(self, name):
        edge_label = EdgeLabel(self._host, self._graph_name, self.timeout)
        edge_label.create_parameter_holder()
        edge_label.add_parameter("name", name)
        edge_label.add_parameter("not_exist", True)
        return edge_label

    def getEdgeLabel(self, label_name):
        """
            根据name获取EdgeLabel
            :param name:
            :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels" + "/" + label_name
        response = requests.get(url, headers=self._headers)
        if response.status_code == 200:
            res = EdgeLabelData(json.loads(response.content))
            return res
        else:
            raise NotFoundError("EdgeLabel not found: {}".format(response.content))

    def getEdgeLabels(self):
        """
            根据name获取EdgeLabel
            :param name:
            :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels"
        response = requests.get(url, headers=self._headers)
        res = []
        for item in json.loads(response.content)["edgelabels"]:
            res.append(EdgeLabelData(item))
        return res

    def indexLabel(self, name):
        index_label = IndexLabel(self._host, self._graph_name, self.timeout)
        index_label.create_parameter_holder()
        index_label.add_parameter("name", name)
        return index_label

    def getIndexLabel(self, name):
        """
        根据name获取indexlabel
        :param name:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/indexlabels" + "/" + name
        response = requests.get(url, headers=self._headers)
        if response.status_code == 200:
            res = IndexLabelData(json.loads(response.content))
            return res
        else:
            raise NotFoundError("IndexLabel not found: {}".format(response.content))

    def getIndexLabels(self):
        """
        根据name获取indexlabel
        :param name:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/indexlabels"
        response = requests.get(url, headers=self._headers)
        res = []
        for item in json.loads(response.content)['indexlabels']:
            res.append(IndexLabelData(item))
        return res








