class PropertyKeyData:
    def __init__(self, dic):
        self.__id = dic["id"]
        self.__name = dic["name"]
        self.__cardinality = dic["cardinality"]
        self.__data_type = dic["data_type"]
        self.__user_data = dic["user_data"]

    @property
    def id(self):
        return self.__id

    @property
    def cardinality(self):
        return self.__cardinality

    @property
    def name(self):
        return self.__name

    @property
    def dataType(self):
        return self.__data_type

    @property
    def userdata(self):
        return self.__user_data

    def __repr__(self):
        res = "name: {}, cardinality: {}, data_type: {}".format(
            self.__name, self.__cardinality, self.__data_type
        )
        return res


class VertexLabelData:
    def __init__(self, dic):
        self.__id = dic["id"]
        self.__name = dic["name"]
        self.__id_strategy = dic["id_strategy"]
        self.__primary_keys = dic["primary_keys"]
        self.__nullable_keys = dic["nullable_keys"]
        self.__index_labels = dic["index_labels"]
        self.__properties = dic["properties"]
        self.__enable_label_index = dic["enable_label_index"]
        self.__user_data = dic["user_data"]

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def primaryKeys(self):
        return self.__primary_keys

    @property
    def idStrategy(self):
        return self.__id_strategy

    @property
    def properties(self):
        return self.__properties

    @property
    def nullableKeys(self):
        return self.__nullable_keys

    @property
    def userdata(self):
        return self.__user_data

    def __repr__(self):
        res = "name: {}, primary_keys: {}, properties: {}".format(
            self.__name, self.__primary_keys, self.__properties)
        return res


class EdgeLabelData:
    def __init__(self, dic):
        self.__id = dic["id"]
        self.__name = dic["name"]
        self.__source_label = dic["source_label"]
        self.__target_label = dic["target_label"]
        self.__frequency = dic["frequency"]
        self.__sort_keys = dic["sort_keys"]
        self.__nullable_keys = dic["nullable_keys"]
        self.__index_labels = dic["index_labels"]
        self.__properties = dic["properties"]
        self.__enable_label_index = dic["enable_label_index"]
        self.__user_data = dic["user_data"]

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def sourceLabel(self):
        return self.__source_label

    @property
    def targetLabel(self):
        return self.__target_label

    @property
    def frequency(self):
        return self.__frequency

    @property
    def sortKeys(self):
        return self.__sort_keys

    @property
    def properties(self):
        return self.__properties

    @property
    def nullableKeys(self):
        return self.__nullable_keys

    @property
    def userdata(self):
        return self.__user_data

    def __repr__(self):
        res = "{}--{}-->{}".format(
            self.__source_label, self.__name, self.__target_label)
        return res


class IndexLabelData:
    def __init__(self, dic):
        self.__id = dic["id"] if "id" in dic else None
        self.__base_type = dic["base_type"] if "base_type" in dic else None
        self.__base_value = dic["base_value"] if "base_value" in dic else None
        self.__name = dic["name"] if "name" in dic else None
        self.__fields = dic["fields"] if "fields" in dic else None
        self.__index_type = dic["index_type"] if "index_type" in dic else None

    @property
    def id(self):
        return self.__id

    @property
    def baseType(self):
        return self.__base_type

    @property
    def baseValue(self):
        return self.__base_value

    @property
    def name(self):
        return self.__name

    @property
    def fields(self):
        return self.__fields

    @property
    def indexType(self):
        return self.__index_type

    def __repr__(self):
        res = "index_name: {}, base_value: {}, base_type: {}, fields: [], index_type: {}"\
            .format(self.__name, self.__base_value, self.__base_type, self.__fields,
                    self.__index_type)
        return res


class VertexData:
    def __init__(self, dic):
        self.__id = dic["id"]
        self.__label = dic["label"] if "label" in dic else None
        self.__type = dic["type"] if "type" in dic else None
        self.__properties = dic["properties"] if "properties" in dic else None

    @property
    def id(self):
        return self.__id

    @property
    def label(self):
        return self.__label

    @property
    def type(self):
        return self.__type

    @property
    def properties(self):
        return self.__properties

    def __repr__(self):
        res = "id: {}, label: {}, type: {}".format(self.__id, self.__label, self.__type)
        return res


class EdgeData:
    def __init__(self, dic):
        self.__id = dic["id"]
        self.__label = dic["label"] if "label" in dic else None
        self.__type = dic["type"] if "type" in dic else None
        self.__outV = dic["outV"] if "outV" in dic else None
        self.__outVLabel = dic["outVLabel"] if "outVLabel" in dic else None
        self.__inV = dic["inV"] if "inV" in dic else None
        self.__inVLabel = dic["inVLabel"] if "inVLabel" in dic else None
        self.__properties = dic["properties"] if "properties" in dic else None

    @property
    def id(self):
        return self.__id

    @property
    def label(self):
        return self.__label

    @property
    def type(self):
        return self.__type

    @property
    def outV(self):
        return self.__outV

    @property
    def outVLabel(self):
        return self.__outVLabel

    @property
    def inV(self):
        return self.__inV

    @property
    def inVLabel(self):
        return self.__inVLabel

    @property
    def properties(self):
        return self.__properties

    def __repr__(self):
        res = "{}--{}-->{}".format(self.__outV, self.__label, self.__inV)
        return res