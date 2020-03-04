import json

import requests

from .my_decorator import decorator1, decorator2
from .response import Response
from .exceptions import InvalidParameter, CreateError, UpdateError, RemoveError


class ParameterHolder:
    def __init__(self):
        self._dic = {}

    def set(self, key, value):
        self._dic[key] = value

    def get_value(self, key):
        if key not in self._dic:
            return None
        else:
            return self._dic[key]

    def get_dic(self):
        return self._dic

    def get_keys(self):
        return self._dic.keys()


class HugeGraphBase:
    def __init__(self, host, graph_name, timeout):
        self._host = host
        self._graph_name = graph_name
        self._parameter_holder = None
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Content-Type': 'application/json'
        }
        self.timeout = timeout

    def add_parameter(self, key, value):
        self._parameter_holder.set(key, value)
        return

    def get_parameter_holder(self):
        return self._parameter_holder

    def create_parameter_holder(self):
        self._parameter_holder = ParameterHolder()

    def clean_parameter_holder(self):
        self._parameter_holder = None


class PropertyKey(HugeGraphBase):
    def __init__(self, host, graph_name, timeout):
        super().__init__(host, graph_name, timeout)

    @decorator1
    def asInt(self):
        self._parameter_holder.set("data_type", "INT")
        return self

    @decorator1
    def asText(self):
        self._parameter_holder.set("data_type", "TEXT")
        return self

    @decorator1
    def asDouble(self):
        self._parameter_holder.set("data_type", "DOUBLE")
        return self

    @decorator1
    def asDate(self):
        self._parameter_holder.set("data_type", "DATE")
        return self

    # warning 还有一些asType没有加入

    @decorator1
    def valueSingle(self):
        self._parameter_holder.set("cardinality", "SINGLE")
        return self

    @decorator1
    def valueList(self):
        self._parameter_holder.set("cardinality", "LIST")
        return self

    @decorator1
    def valueSet(self):
        self._parameter_holder.set("cardinality", "SET")
        return self

    @decorator1
    def calcMax(self):
        self._parameter_holder.set("aggregate_type", "MAX")
        return self

    @decorator1
    def calcMin(self):
        self._parameter_holder.set("aggregate_type", "MIN")
        return self

    @decorator1
    def calcSum(self):
        self._parameter_holder.set("aggregate_type", "SUM")
        return self

    @decorator1
    def calcOld(self):
        self._parameter_holder.set("aggregate_type", "OLD")
        return self

    @decorator1
    def userdata(self, *args):
        user_data = self._parameter_holder.get_value("user_data")
        if not user_data:
            self._parameter_holder.set("user_data", dict())
            user_data = self._parameter_holder.get_value("user_data")
        i = 0
        while i < len(args):
            user_data[args[i]] = args[i+1]
            i += 2
        return self

    def ifNotExist(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys" \
              + "/" + self._parameter_holder.get_value("name")
        response = requests.get(url)
        # warning 如果通讯失败应该判断status_code
        if response.status_code == 200:
            self._parameter_holder.set("not_exist", False)
        return self

    @decorator2
    def create(self):
        """"
        创建一个propertykey
        :return:
        """
        dic = self._parameter_holder.get_dic()
        propertykeys = {
            "name": dic["name"]
        }
        if "data_type" in dic:
            propertykeys["data_type"] = dic["data_type"]
        if "cardinality" in dic:
            propertykeys["cardinality"] = dic["cardinality"]
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys"
        response = requests.post(url, data=json.dumps(propertykeys), headers=self._headers)
        res = Response(response.status_code, response.content)
        # 如果创建失败，将错误记录在日志当中
        self.clean_parameter_holder()
        if res.status_code == 201:
            return 'create PropertyKey success, Detail: {}'.format(response.content)
        else:
            raise CreateError('CreateError: "create PropertyKey failed", Detail: {}'.format(response.content))

    @decorator1
    def append(self):
        """
        为已存在的 PropertyKey 添加userdata
        :param property_name:
        :param user_data:
        :return:
        """
        property_name = self._parameter_holder.get_value("name")
        user_data = self._parameter_holder.get_value("user_data")
        if not user_data:
            user_data = dict()
        data = {
            "name": property_name,
            "user_data": user_data
        }
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys" \
              + "/" + property_name + "?action=append"
        response = requests.put(url, data=json.dumps(data), headers=self._headers)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 200:
            return 'append PropertyKey success, Detail: {}'.format(response.content)
        else:
            raise UpdateError('UpdateError: "append PropertyKey failed", Detail: {}'.format(response.content))

    @decorator1
    def eliminate(self):
        """
        为已存在的 PropertyKey 删除userdata
        :param property_name:
        :param user_data:
        :return:
        """
        property_name = self._parameter_holder.get_value("name")
        user_data = self._parameter_holder.get_value("user_data")
        if not user_data:
            user_data = dict()
        data = {
            "name": property_name,
            "user_data": user_data
        }
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/propertykeys" \
              + "/" + property_name + "?action=eliminate"
        response = requests.put(url, data=json.dumps(data), headers=self._headers)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 200:
            return 'eliminate PropertyKey success, Detail: {}'.format(str(res.response))
        else:
            raise UpdateError('UpdateError: "eliminate PropertyKey failed", Detail: {}'.format(str(res.response)))

    @decorator1
    def remove(self):
        """
            移除 PropertyKey
            :return:
        """
        dic = self._parameter_holder.get_dic()
        url = self._host + "/graphs" + "/" + self._graph_name + \
              "/schema/propertykeys" + "/" + dic["name"]
        response = requests.delete(url)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 204:
            return 'delete PropertyKey success, Detail: {}'.format(dic["name"])
        else:
            raise RemoveError('RemoveError: "delete PropertyKey failed", Detail: {}'.format(str(res.response)))


class VertexLabel(HugeGraphBase):
    def __init__(self, host, graph_name, timeout):
        super().__init__(host, graph_name, timeout)

    @decorator1
    def useAutomaticId(self):
        self._parameter_holder.set("id_strategy", "AUTOMATIC")
        return self

    @decorator1
    def useCustomizeStringId(self):
        self._parameter_holder.set("id_strategy", "CUSTOMIZE_STRING")
        return self

    @decorator1
    def useCustomizeNumberId(self):
        self._parameter_holder.set("id_strategy", "CUSTOMIZE_NUMBER")
        return self

    @decorator1
    def usePrimaryKeyId(self):
        self._parameter_holder.set("id_strategy", "PRIMARY_KEY")
        return self

    @decorator1
    def properties(self, *args):
        self._parameter_holder.set("properties", list(args))
        return self

    @decorator1
    def primaryKeys(self, *args):
        self._parameter_holder.set("primary_keys", list(args))
        return self

    @decorator1
    def nullableKeys(self, *args):
        self._parameter_holder.set("nullable_keys", list(args))
        return self

    @decorator1
    def enableLabelIndex(self, flag):
        self._parameter_holder.set("enable_label_index", flag)
        return self

    @decorator1
    def userdata(self, *args):
        if "user_data" not in self._parameter_holder.get_keys():
            self._parameter_holder.set('user_data', dict())
        user_data = self._parameter_holder.get_value('user_data')
        i = 0
        while i < len(args):
            user_data[args[i]] = args[i+1]
            i += 2
        return self

    def ifNotExist(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/vertexlabels" \
              + "/" + self._parameter_holder.get_value("name")
        response = requests.get(url)
        # warning 如果通讯失败应该判断status_code
        if response.status_code == 200:
            self._parameter_holder.set("not_exist", False)
        return self

    @decorator2
    def create(self):
        """
            创建一个VertexLabel
            9 known properties for data:
                "primary_keys","nullable_keys",
                "properties","id_strategy", "id",
                "user_data", "name", "enable_label_index"
            :return:
        """
        dic = self._parameter_holder.get_dic()
        key_list = ["name", "id_strategy", "primary_keys", "nullable_keys", "index_labels",
                    "properties", "enable_label_index", "user_data"]
        data = {}
        for key in key_list:
            if key in dic:
                data[key] = dic[key]
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/vertexlabels"
        response = requests.post(url, data=json.dumps(data), headers=self._headers)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 201:
            return 'create VertexLabel success, Detail: "{}"'.format(str(res.response))
        else:
            raise CreateError('CreateError: "create VertexLabel failed", Detail: "{}"'
                              .format(str(res.response)))

    @decorator1
    def append(self):
        dic = self._parameter_holder.get_dic()
        properties = dic['properties'] if "properties" in dic else []
        nullable_keys = dic['nullable_keys'] if "nullable_keys" in dic else[]
        user_data = dic['user_data'] if 'user_data' in dic else {}
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/schema/vertexlabels" + "/" + dic["name"] + "?action=append"
        data = {
            "name": dic["name"],
            "properties": properties,
            "nullable_keys": nullable_keys,
            "user_data": user_data
        }
        response = requests.put(url, data=json.dumps(data), headers=self._headers)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 200:
            return 'append VertexLabel success, Detail: "{}"'.format(str(res.response))
        else:
            raise UpdateError('UpdateError: "append VertexLabel failed", Detail: "{}"'.
                              format(str(res.response)))

    @decorator1
    def remove(self):
        """
            根据name删除VertexLabel
            :param name:
            :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/vertexlabels" + "/" + \
              self._parameter_holder.get_value("name")
        response = requests.delete(url, headers=self._headers)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 202:
            return 'remove VertexLabel success, Detail: "{}"'.format(str(res.response))
        else:
            raise RemoveError('RemoveError: "remove VertexLabel failed", Detail: "{}"'.
                              format(str(res.response)))

    @decorator1
    def eliminate(self):
        """
        为一个VertexLabel删除userdata属性,不支持删除其他的属性
        :param name:
        :param userdata:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/vertexlabels" \
              + "/" + self._parameter_holder.get_value("name") + "?action=eliminate"
        dic = self._parameter_holder.get_dic()
        user_data = dic['user_data'] if 'user_data' in dic else {}
        data = {
            "name": self._parameter_holder.get_value("name"),
            "user_data": user_data,
        }
        response = requests.put(url, data=json.dumps(data), headers=self._headers)
        res = Response(response.status_code, response.content)
        if res.status_code == 200:
            return 'eliminate VertexLabel success, Detail: "{}"'.format(str(res.response))
        else:
            raise UpdateError('UpdateError: "eliminate VertexLabel failed", Detail: "{}"'.
                              format(str(res.response)))


class IndexLabel(HugeGraphBase):
    def __init__(self, host, graph_name, timeout):
        super().__init__(host, graph_name, timeout)

    @decorator1
    def onV(self, vertex_label):
        self._parameter_holder.set("base_value", vertex_label)
        self._parameter_holder.set("base_type", "VERTEX_LABEL")
        return self

    @decorator1
    def onE(self, edge_label):
        self._parameter_holder.set("base_value", edge_label)
        self._parameter_holder.set("base_type", "EDGE_LABEL")
        return self

    @decorator1
    def by(self, *args):
        if "fields" not in self._parameter_holder.get_keys():
            self._parameter_holder.set("fields", set())
        s = self._parameter_holder.get_value("fields")
        for item in args:
            s.add(item)
        return self

    @decorator1
    def secondary(self):
        self._parameter_holder.set("index_type", "SECONDARY")
        return self

    @decorator1
    def range(self):
        self._parameter_holder.set("index_type", "RANGE")
        return self

    @decorator1
    def Search(self):
        self._parameter_holder.set("index_type", "SEARCH")
        return self

    @decorator1
    def ifNotExist(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/indexlabels" \
              + "/" + self._parameter_holder.get_value("name")
        response = requests.get(url)
        # warning 如果通讯失败应该判断status_code
        if response.status_code == 200:
            self._parameter_holder.set("not_exist", False)
        return self

    @decorator2
    def create(self):
        dic = self._parameter_holder.get_dic()
        data = dict()
        data["name"] = dic["name"]
        data["base_type"] = dic["base_type"]
        data["base_value"] = dic["base_value"]
        data["index_type"] = dic["index_type"]
        data["fields"] = list(dic["fields"])
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/indexlabels"
        response = requests.post(url, data=json.dumps(data), headers=self._headers)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 202:
            return 'create IndexLabel success, Deatil: "{}"'.format(str(res.response))
        else:
            raise CreateError('CreateError: "create IndexLabel failed", '
                              'Detail "{}"'.format(str(res.response)))

    @decorator1
    def remove(self):
        name = self._parameter_holder.get_value("name")
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/indexlabels" + "/" + name
        response = requests.delete(url, headers=self._headers)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 202:
            return 'remove IndexLabel success, Deatil: "{}"'.format(str(res.response))
        else:
            raise RemoveError('RemoveError: "remove IndexLabel failed", '
                              'Detail "{}"'.format(str(res.response)))


class EdgeLabel(HugeGraphBase):
    def __init__(self, host, graph_name, timeout):
        super().__init__(host, graph_name, timeout)

    @decorator1
    def link(self, source_label, target_label):
        self._parameter_holder.set("source_label", source_label)
        self._parameter_holder.set("target_label", target_label)
        return self

    @decorator1
    def sourceLabel(self, source_label):
        self._parameter_holder.set("source_label", source_label)
        return self

    @decorator1
    def targetLabel(self, target_label):
        self._parameter_holder.set("target_label", target_label)
        return self

    @decorator1
    def userdata(self, *args):
        if not self._parameter_holder.get_value("user_data"):
            self._parameter_holder.set('user_data', dict())
        user_data = self._parameter_holder.get_value("user_data")
        i = 0
        while i < len(args):
            user_data[args[i]] = args[i+1]
            i += 2
        return self

    @decorator1
    def properties(self, *args):
        self._parameter_holder.set("properties", list(args))
        return self

    @decorator1
    def singleTime(self):
        self._parameter_holder.set("frequency", "SINGLE")
        return self

    @decorator1
    def multiTimes(self):
        self._parameter_holder.set("frequency", "MULTIPLE")
        return self

    @decorator1
    def sortKeys(self, *args):
        self._parameter_holder.set("sort_keys", list(args))
        return self

    @decorator1
    def nullableKeys(self, *args):
        nullable_keys = set(args)
        self._parameter_holder.set("nullable_keys", list(nullable_keys))
        return self

    @decorator1
    def ifNotExist(self):
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels" \
              + "/" + self._parameter_holder.get_value("name")
        response = requests.get(url)
        # warning 如果通讯失败应该判断status_code
        if response.status_code == 200:
            self._parameter_holder.set("not_exist", False)
        return self

    @decorator2
    def create(self):
        """
            创建一个EdgeLabel
            9 known properties for self._parameter_holder:
                    "source_label", "nullable_keys", "properties",
                    "sort_keys", "target_label",
                    "frequency", "user_data",
                    "name", "enable_label_index"
            :return:
        """
        dic = self._parameter_holder.get_dic()
        data = dict()
        keys = ['name', 'source_label', 'target_label', 'nullable_keys', 'properties',
                'enable_label_index', 'sort_keys', 'user_data', 'frequency']
        for key in keys:
            if key in dic:
                data[key] = dic[key]
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels"
        response = requests.post(url, data=json.dumps(data), headers=self._headers)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 201:
            return 'create EdgeLabel success, Detail: "{}"'.format(str(res.response))
        else:
            raise CreateError('CreateError: "create EdgeLabel failed", Detail:  "{}"'
                              .format(str(res.response)))

    @decorator1
    def remove(self):
        """
        根据name删除EdgeLabel
        :param label_name:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels" + "/" + \
              self._parameter_holder.get_value("name")
        response = requests.delete(url, headers=self._headers)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 202:
            return 'remove EdgeLabel success, Detail: "{}"'.format(str(res.response))
        else:
            raise RemoveError('RemoveError: "remove EdgeLabel failed", Detail:  "{}"'
                              .format(str(res.response)))

    @decorator1
    def append(self):
        """
        为一个EdgeLabel添加properties
        :param name:
        :param properties:
        :param nullable:give a list
        :return:
        """
        dic = self._parameter_holder.get_dic()
        data = dict()
        keys = ['name', 'nullable_keys', 'properties', 'user_data']
        for key in keys:
            if key in dic:
                data[key] = dic[key]
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels" \
              + "/" + data["name"] + "?action=append"
        response = requests.put(url, data=json.dumps(data), headers=self._headers)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 200:
            return 'append EdgeLabel success, Detail: "{}"'.format(str(res.response))
        else:
            raise UpdateError('UpdateError: "append EdgeLabel failed", Detail: "{}"'.format(str(res.response)))

    @decorator1
    def eliminate(self):
        """
        为一个EdgeLabel删除userdata
        :param name:
        :param userdata:
        :return:
        """
        name = self._parameter_holder.get_value("name")
        user_data = self._parameter_holder.get_value("user_data") if \
            self._parameter_holder.get_value("user_data") else {}
        url = self._host + "/graphs" + "/" + self._graph_name + "/schema/edgelabels" \
              + "/" + self._parameter_holder.get_value("name") + "?action=eliminate"
        data = {
            "name": name,
            "user_data": user_data
        }
        response = requests.put(url, data=json.dumps(data), headers=self._headers)
        res = Response(response.status_code, response.content)
        self.clean_parameter_holder()
        if res.status_code == 200:
            return 'eliminate EdgeLabel success, Detail: "{}"'.format(str(res.response))
        else:
            raise UpdateError('UpdateError: "eliminate EdgeLabel failed", Detail: "{}"'.format(str(res.response)))