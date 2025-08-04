from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START

# 상태 타입 1 정의
class ParentState(TypedDict):
    foo: str

# 상태 타입 2 정의 (서브그래프는 상태 타입이 다름!)
class SubgraphState(TypedDict):
    bar: str

# 서브그래프 노드
def subgraph_node(state: SubgraphState):
    return {"bar": state["bar"] + " world"}

# 서브그래프 생성 (상태는 SubgraphState)
subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node("subgraph_node", subgraph_node)
subgraph_builder.add_edge(START, "subgraph_node")
subgraph = subgraph_builder.compile()

# 상위 그래프 생성 (상태는 ParentState)
parent_builder = StateGraph(ParentState)

# 오류 발생 지점: 상태 타입이 다른 서브그래프를 add_node에 추가
parent_builder.add_node("subgraph", subgraph)  # 여기서 오류 발생 예상

parent_builder.add_edge(START, "subgraph")
graph = parent_builder.compile()

# 실행 시도
result = graph.invoke({"foo": "Hello"})
print(result)
