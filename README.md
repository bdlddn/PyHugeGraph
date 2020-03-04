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
