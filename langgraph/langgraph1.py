from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START

# 공통 상태 정의
class State(TypedDict):
    foo: str

# 서브그래프 만들기
def subgraph_node_1(state: State):
    return {"foo": "Hi! " + state["foo"]}

subgraph_builder = StateGraph(State)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()

# 상위(parent) 그래프에 서브그래프를 노드처럼 추가
builder = StateGraph(State)
builder.add_node("subgraph", subgraph)
builder.add_edge(START, "subgraph")
graph = builder.compile()

# 실행
result = graph.invoke({"foo": "YBIGTA"})
print(result)  # {'foo': 'Hi! World'}
