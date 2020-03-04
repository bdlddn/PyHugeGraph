# PyHugeGraph
PyHugeGraph是一个百度HugeGraph数据库的python接口包。

## 特点
+ 接口风格同gremlin语言类似。

## 使用方法
### 1 HugeGraphClient
HugeGraph-Client 是操作 graph 的总入口，用户必须先创建出 HugeGraph-Client 对象，与 HugeGraph-Server 建立连接（伪连接）后，才能获取到 schema、graph 以及 gremlin 的操作入口对象。

目前 HugeGraph-Client 只允许连接服务端已存在的图，无法自定义图进行创建。其创建方法如下：
```
form PyHugeGraph.huge_graph_client import HugeGraphClient

client = HugeClient("http://localhost:8080", "hugegraph");
```

### 2 元数据
#### 2.1 SchemaManager
SchemaManager 用于管理 HugeGraph 中的四种元数据，分别是PropertyKey（属性类型）、VertexLabel（顶点类型）、EdgeLabel（边类型）和 IndexLabel（索引标签）。在定义元数据信息之前必须先创建 SchemaManager 对象。

用户可使用如下方法获得SchemaManager对象：
```
schema = client.schema()
```

#### 2.2 PropertyKey
PropertyKey 用来规范顶点和边的属性的约束，暂不支持定义属性的属性。

PropertyKey 允许定义的约束信息包括：name、datatype、cardinality、userdata。
具体参数信息请参考https://hugegraph.github.io/hugegraph-doc/clients/hugegraph-client.html中相关内容。这里只简单介绍接口的使用方法

###### 2.2.1 创建PropertyKey
```
schema.propertyKey("name").asText().valueSet().ifNotExist().create()
schema.propertyKey("age").asText().valueSet().ifNotExist().create()
```
ifNotExist()：为 create 添加判断机制，若当前 PropertyKey 已经存在则不再创建，否则创建该属性。若不添加判断，在 properkey 已存在的情况下会抛出异常信息，下同，不再赘述。

###### 2.2.2 追加PropertyKey
```
schema.porpertyKey("age").user_data({"min":12, "max": 18}).append()
```
给PropertyKey追加user_data。

###### 2.2.3 清除PropertyKey
```
schema.porpertyKey("age").user_data({"min": 12}).eliminate()
```
清除PorpertyKey的user_data中相关项，目前仅支持清除user_data。

###### 2.2.4 删除PropertyKey
```
schema.propertyKey("age").remove()
```

###### 2.2.5 查询PropertyKey
```
# 获取PropertyKey对象
schema.getPropertyKey("name")

# 获取PropertyKey属性
schema.getPropertyKey("name").cardinality
schema.getPropertyKey("name").dataType
schema.getPropertyKey("name").name
schema.getPropertyKey("name").userdata

# 获取图中所有的PropertyKey
schema.getPropertyKeys()
```
