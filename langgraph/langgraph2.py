from typing_extensions import TypedDict

# 서브그래프용 상태
class SubgraphState(TypedDict):
    bar: str
    baz: str

def subgraph_node_1(state: SubgraphState):
    return {"baz": state["baz"]}

def subgraph_node_2(state: SubgraphState):
    return {"bar": state["bar"] + state["baz"]}

# 서브그래프 생성
from langgraph.graph import StateGraph, START
subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_node(subgraph_node_2)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
subgraph = subgraph_builder.compile()

# 상위 그래프의 상태
class ParentState(TypedDict):
    foo: str

def node_1(state: ParentState):
    return {"foo": "Hi! " + state["foo"]}

def node_2(state: ParentState):
    # 필요한 값만 추출해서 서브그래프에 입력
    response = subgraph.invoke({"bar": state["foo"], "baz": "26th"})
    return {"foo": response["bar"]}

parent_builder = StateGraph(ParentState)
parent_builder.add_node("node_1", node_1)
parent_builder.add_node("node_2", node_2)
parent_builder.add_edge(START, "node_1")
parent_builder.add_edge("node_1", "node_2")
graph = parent_builder.compile()

# 실행
result = graph.invoke({"foo": "YBIGTA"})
print(result)  
