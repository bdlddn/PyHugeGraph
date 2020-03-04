import json

from .huge_graph_class import HugeGraphBase
from .graph_data_class import VertexData, EdgeData
from .exceptions import NotFoundError
from .util import create_exception


class Traverser(HugeGraphBase):
    def __init__(self, host, graph_name, timeout):
        super().__init__(host, graph_name, timeout)
        self.session = None

    def set_session(self, session):
        self.session = session

    def close_session(self):
        if self.session:
            self.session.close()

    def getVerticesById(self, vertex_ids):
        if not vertex_ids:
            return []
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/traversers/vertices?"
        for vertex_id in vertex_ids:
            url += 'ids="{}"&'.format(vertex_id)
        url = url.rstrip("&")
        response = self.session.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code == 200:
            res = []
            for item in json.loads(response.content)["vertices"]:
                res.append(VertexData(item))
            return res
        else:
            create_exception(response.content)
            # raise NotFoundError("traverse vertices failed: {}".format(response.content))

    def getEdgesById(self, edge_ids):
        if not edge_ids:
            return []
        url = self._host + "/graphs" + "/" + self._graph_name \
              + "/traversers/edges?"
        for vertex_id in edge_ids:
            url += 'ids={}&'.format(vertex_id)
        url = url.rstrip("&")
        response = self.session.get(url, headers=self._headers, timeout=self.timeout)
        if response.status_code == 200:
            res = []
            for item in json.loads(response.content)["edges"]:
                res.append(EdgeData(item))
            return res
        else:
            create_exception(response.content)
            # raise NotFoundError("traverse edges failed: {}".format(response.content))
