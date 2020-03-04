import json
import urllib

from .response import Response
from .huge_graph_class import HugeGraphBase
from .graph_data_class import VertexData, EdgeData
from .exceptions import NotFoundError, CreateError, RemoveError, UpdateError


class GraphManager(HugeGraphBase):
    def __init__(self, host, graph_name, timeout):
        super().__init__(host, graph_name, timeout)
        self.session = None

    def set_session(self, session):
        self.session = session

    def close_session(self):
        if self.session:
            self.session.close()

    def addVertex(self, label, properties):
        """
        创建一个顶点
        :param label:
        :param properties:
        :return:
        """
        data = dict()
        data['label'] = label
        data["properties"] = properties
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices"
        response = self.session.post(url, data=json.dumps(data), headers=self._headers, timeout=self.timeout)
        if response.status_code == 201:
            res = VertexData(json.loads(response.content))
            return res
        else:
            # logger.error(" create vertex failed:  {}".format(response.content))
            raise CreateError("create vertex failed: {}".format(response.content))

    def addVertices(self, input_data):
        """
        创建多个顶点
        :param input_data:
                [[label, properties],
                [label, properties]]
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices/batch"
        data = []
        for item in input_data:
            data.append({'label': item[0], 'properties': item[1]})
        # response = self.session.post(url, data=json.dumps(data), headers=self._headers, timeout=self.timeout)
        response = self.session.post(url, data=json.dumps(data), headers=self._headers, timeout=self.timeout)
        if response.status_code == 201:
            res = []
            for item in json.loads(response.content):
                res.append(VertexData({"id": item}))
            return res
        else:
            # logger.error(" create vertexes failed:  {}".format(response.content))
            raise CreateError("create vertexes failed: {}".format(response.content))

    def appendVertex(self, vertex_id, properties):
        """
        更新顶点属性
        :param vertex_id:
        :param properties:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/graph/vertices/\"" + vertex_id + "\"?action=append"
        data = {
            "properties": properties
        }
        response = self.session.put(url, data=json.dumps(data), headers=self._headers, timeout=self.timeout)
        if response.status_code == 200:
            res = VertexData(json.loads(response.content))
            return res
        else:
            # logger.error(" append vertex failed:  {}".format(response.content))
            raise UpdateError("append vertex failed: {}".format(response.content))

    def eliminateVertex(self, vertex_id, properties):
        """
        更新顶点属性
        :param vertex_id:
        :param properties:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/graph/vertices/\"" + vertex_id + "\"?action=eliminate"
        data = {
            # "label": label,
            "properties": properties
        }
        response = self.session.put(url, data=json.dumps(data), headers=self._headers, timeout=self.timeout)
        if response.status_code == 200:
            res = VertexData(json.loads(response.content))
            return res
        else:
            # logger.error(" eliminate vertex failed:  {}".format(response.content))
            raise UpdateError("eliminate vertex failed: {}".format(response.content))

    def getVertexById(self, vertex_id):
        """
        根据ID 获取顶点
        :param vertex_id:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices/\"" + vertex_id + "\""
        response = self.session.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code == 200:
            res = VertexData(json.loads(response.content))
            return res
        else:
            # logger.error("Vertex not found: {}".format(response.content))
            raise NotFoundError("Vertex not found: {}".format(response.content))

    def getVertexByPage(self, label, limit, page, properties=None):
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices?"
        para = ""
        para = para + "&label=" + label
        if properties:
            para = para + "&properties=" + json.dumps(properties)
        if page:
            para += '&page={}'.format(urllib.parse.quote(page))
        else:
            para += '&page'
        para = para + "&limit=" + str(limit)
        url = url + para[1:]
        response = self.session.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code == 200:
            res = []
            for item in json.loads(response.content)["vertices"]:
                res.append(VertexData(item))
            next_page = json.loads(response.content)["page"]
            return res, next_page
        else:
            # logger.error("Vertex not found: {}".format(response.content))
            raise NotFoundError("Vertex not found: {}".format(response.content))

    # def getVertexByCondition(self, label="",  limit=0, page='', properties=None):
    #     """
    #     获取符合条件的顶点
    #     :param label:
    #     :param properties:give a dict
    #     :param page:
    #     :param limit:
    #     :return:
    #     """
    #     # 以上参数都是可选的，如果提供page参数，必须提供limit参数，不允许带其他参数。
    #     url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices?"
    #     para = ""
    #     if label:
    #         para = para + "&label=" + label
    #     if properties:
    #         para = para + "&properties=" + json.dumps(properties)
    #     if limit > 0:
    #         para = para + "&limit=" + str(limit)
    #     if page:
    #         para += '&page={}'.format(urllib.parse.quote(page))
    #     else:
    #         para += '&page'
    #     url = url + para[1:]
    #     response = self.session.get(url, headers=self._headers, timeout=self.timeout)
    #     if response.status_code == 200:
    #         res = []
    #         for item in json.loads(response.content)["vertices"]:
    #             res.append(VertexData(item))
    #         return res
    #     else:
    #         # logger.error("Vertex not found: {}".format(response.content))
    #         raise NotFoundError("Vertex not found: {}".format(response.content))

    def removeVertexById(self, vertex_id):
        """
        根据ID 删除顶点
        :param vertex_id:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/vertices/\"" + vertex_id + "\""
        response = self.session.delete(url, headers=self._headers, timeout=self.timeout)
        if response.status_code == 204:
            res = Response(response.status_code, response.content)
            # logger.info(" remove vertex successful:  {}".format(response.content))
            return res
        else:
            # logger.error(" remove vertex failed:  {}".format(response.content))
            raise RemoveError("remove vertex failed: {}".format(response.content))

    def addEdge(self, edge_label, out_id, in_id, properties):
        """
                 create an edge
                :param edge_label:
                :param outv:
                :param inv:
                :param outv_label:
                :param inv_label:
                :param properties:
                :return:
                """
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/edges"
        data = {
            "label": edge_label,
            "outV": out_id,
            "inV": in_id,
            "properties": properties
        }
        response = self.session.post(url, data=json.dumps(data), headers=self._headers, timeout=self.timeout)
        if response.status_code == 201:
            res = EdgeData(json.loads(response.content))
            return res
        else:
            # logger.error(" created edge failed:  {}".format(response.content))
            raise CreateError("created edge failed: {}".format(response.content))

    def addEdges(self, input_data):
        """
                 create edges
                 [[edge_label, out_id, in_id, out_label, in_label, properties],
                 [edge_label, out_id, in_id, out_label, in_label, properties]]

        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/edges/batch"
        data = []
        for item in input_data:
            data.append({'label': item[0], 'outV': item[1], 'inV': item[2], 'outVLabel': item[3],
                         'inVLabel': item[4], 'properties': item[5]})
        response = self.session.post(url, data=json.dumps(data), headers=self._headers, timeout=self.timeout)
        if response.status_code == 201:
            res = []
            for item in json.loads(response.content):
                res.append(EdgeData({"id": item}))
            return res
        else:
            # logger.error(" created edges failed:  {}".format(response.content))
            raise CreateError("created edges failed:  {}".format(response.content))

    def appendEdge(self, edge_id, properties):
        """
        更新边的属性
        :param properties:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/graph/edges/" + edge_id + "?action=append"
        data = {
            "properties": properties
        }
        response = self.session.put(url, data=json.dumps(data), headers=self._headers, timeout=self.timeout)
        if response.status_code == 200:
            res = EdgeData(json.loads(response.content))
            return res
        else:
            # logger.error(" append edge failed:  {}".format(response.content))
            raise UpdateError("append edge failed: {}".format(response.content))

    def eliminateEdge(self, edge_id, properties):
        """
        删除边的属性
        :param properties:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/graph/edges/" + edge_id + "?action=eliminate"
        data = {
            "properties": properties
        }
        response = self.session.put(url, data=json.dumps(data), headers=self._headers, timeout=self.timeout)
        if response.status_code == 200:
            res = EdgeData(json.loads(response.content))
            return res
        else:
            # logger.error(" eliminate edge failed:  {}".format(response.content))
            raise UpdateError("eliminate edge failed: {}".format(response.content))

    def getEdgeById(self, edge_id):
        """
        根据Id 获取边
        :param edge_id:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/edges/" + edge_id
        response = self.session.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code == 200:
            res = EdgeData(json.loads(response.content))
            return res
        else:
            # logger.error(" not found edge:  {}".format(response.content))
            raise NotFoundError("not found edge: {}".format(response.content))

    def getEdgeByPage(self, label=None, vertex_id=None, direction=None, limit=0, page=None, properties=None):

        """
        根据条件查询获取边
        :param vertex_id: vertex_id为可选参数，如果提供参数vertex_id则必须同时提供参数direction。
        :param direction: (IN | OUT | BOTH)
        :param label:
        :param properties:give a dict
        :param limit:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/edges?"
        para = ""
        if vertex_id:
            if direction:
                para = para + "&vertex_id=\"" + vertex_id + "\"&direction=" + direction
            else:
                return Response(400, "Direction can not be empty")
        if label:
            para = para + "&label=" + label
        if properties:
            para = para + "&properties=" + json.dumps(properties)
        if page is not None:
            if page:
                para += '&page={}'.format(urllib.parse.quote(page))
            else:
                para += '&page'
        if limit > 0:
            para = para + "&limit=" + str(limit)
        url = url + para[1:]
        response = self.session.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code == 200:
            res = []
            for item in json.loads(response.content)["edges"]:
                res.append(EdgeData(item))
            return res, json.loads(response.content)["page"]
        else:
            # logger.error(" not found edges:  {}".format(response.content))
            raise NotFoundError("not found edges: {}".format(response.content))

    def removeEdgeById(self, edge_id):
        """
        根据Id 删除边
        :param edge_id:
        :return:
        """
        url = self._host + "/graphs" + "/" + self._graph_name + "/graph/edges/" + edge_id
        response = self.session.delete(url, headers=self._headers, timeout=self.timeout)
        if response.status_code == 204:
            res = Response(response.status_code, response.content)
            return res
        else:
            # logger.error(" remove edge failed:  {}".format(response.content))
            raise RemoveError("remove edge failed: {}".format(response.content))