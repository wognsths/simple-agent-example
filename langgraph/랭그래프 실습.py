from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# 최하위(손자) 서브그래프
class GrandChildState(TypedDict):
    message: str

def grandchild_1(state: GrandChildState):
#    return {"message": #####수정해보세요###### + ", I love u"}

grandchild_builder = StateGraph(GrandChildState)
grandchild_builder.add_node("grandchild_1", grandchild_1)
grandchild_builder.add_edge(START, "grandchild_1")
grandchild_builder.add_edge("grandchild_1", END)
grandchild_graph = grandchild_builder.compile()

# 자식 서브그래프
class ChildState(TypedDict):
    child_message: str

def call_grandchild_graph(state: ChildState):
    output = grandchild_graph.invoke({"message": state["child_message"]})
#    return {"child_message": #####수정해보세요###### + ", and thank you."}

child_builder = StateGraph(ChildState)
child_builder.add_node("child_1", call_grandchild_graph)
child_builder.add_edge(START, "child_1")
child_builder.add_edge("child_1", END)
child_graph = child_builder.compile()

# 상위(parent) 그래프
class ParentState(TypedDict):
    main_message: str

def parent_1(state: ParentState):
#    return {"main_message": "Hi " + #####수정해보세요######}

def call_child_graph(state: ParentState):
    output = child_graph.invoke({"child_message": state["main_message"]})
#    return {"main_message": #####수정해보세요######}

parent_builder = StateGraph(ParentState)
parent_builder.add_node("parent_1", parent_1)
parent_builder.add_node("child", call_child_graph)
parent_builder.add_edge(START, "parent_1")
parent_builder.add_edge("parent_1", "child")
graph = parent_builder.compile()

# 실행
result = graph.invoke({"main_message": "YBIGTA"})
print(result)  # 정답 {'main_message': 'Hi YBIGTA, I love u. and thank you.'}
