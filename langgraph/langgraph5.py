from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_upstage import ChatUpstage  # Gemini 모델용
import os
from dotenv import load_dotenv

load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")

# 상태 정의
class State(TypedDict):
    user_input: str
    decision: str
    result: str

# LLM 준비
llm = ChatUpstage(model="solar-pro2")  # model 이름은 gemini-pro

# 라우팅 노드: 언어모델이 yes/no를 판단
def router(state: State) -> State:
    prompt = (
        f"다음 문장이 긍정인지 부정인지 판단하여 'yes' 또는 'no'만 출력하세요.\n"
        f"문장: {state['user_input']}"
    )
    result = llm.invoke(prompt)
    decision = result.content.strip().lower()
    return {**state, "decision": decision}

# 긍정 분기 처리
def handle_yes(state: State) -> State:
    return {**state, "result": "긍정 처리"}

# 부정 분기 처리
def handle_no(state: State) -> State:
    return {**state, "result": "부정 처리"}

# 그래프 구성
graph = StateGraph(State)
graph.add_node("router", router)
graph.add_node("handle_yes", handle_yes)
graph.add_node("handle_no", handle_no)
graph.add_edge(START, "router")

# 조건부 분기
def branching(state: State) -> str:
    return "handle_yes" if state["decision"] == "yes" else "handle_no"

graph.add_conditional_edges(
    "router",
    branching,
    {"handle_yes": "handle_yes", "handle_no": "handle_no"}
)

graph.add_edge("handle_yes", END)
graph.add_edge("handle_no", END)
compiled = graph.compile()

# 실행 예시
if __name__ == "__main__":
    result = compiled.invoke({
        "user_input": input("문장을 입력해주세요:"),
        "decision": "",
        "result": ""
    })
    print(result)
