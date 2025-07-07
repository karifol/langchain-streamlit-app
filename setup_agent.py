from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langgraph.prebuilt import create_react_agent
import os

def main():
    # 状態定義
    class ChatState(TypedDict):
        user_input: str
        bot_output: str
        history : list[dict]  # 各メッセージを辞書形式で保持

    # ノード1: ユーザー入力をそのまま次へ
    def receive_input(state: ChatState) -> ChatState:
        return state

    # ノード2: LLMで応答生成
    def generate_response(state: ChatState) -> ChatState:
        response = llm_with_react.invoke({
            "messages": state["history"]
        })
        response = response["messages"][-1].content  # 最後のメッセージを表示
        return {**state, "bot_output": response}

    # ノード3: 結果を表示（またはUI連携などに返す）
    def return_output(state: ChatState) -> ChatState:
        return state

    # OpenAIモデル初期化
    llm = ChatOpenAI(model="gpt-4o-mini")
    llm_with_react = create_react_agent(llm)

    # LangGraphを構築
    builder = StateGraph(ChatState)
    builder.add_node("receive", receive_input)
    builder.add_node("generate", generate_response)
    builder.add_node("output", return_output)

    # グラフの流れを定義
    builder.set_entry_point("receive")
    builder.add_edge("receive", "generate")
    builder.add_edge("generate", "output")
    builder.add_edge("output", END)

    # グラフをコンパイル
    graph = builder.compile()

    return graph