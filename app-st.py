from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict
import dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
import streamlit as st
import os

# OpenAI APIキーを設定
import os
os.environ["OPENAI_API_KEY"] = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

# ツール
@tool
def search_web(query: str) -> str:
    """ウェブ検索を行います。"""
    search_tool = DuckDuckGoSearchRun()
    results = search_tool.run(query)
    return f"検索結果: {results[:500]}..."  # 最初の500文字だけ返す

# 状態定義
class ChatState(TypedDict):
    user_input: str
    bot_output: str
    history : list[dict]  # 各メッセージを辞書形式で保持

# OpenAIモデル初期化
llm = ChatOpenAI(model="gpt-4o-mini")  # または gpt-3.5-turbo
llm_with_react = create_react_agent(llm, tools=[search_web])

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

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "あなたは天才です。"},
        {"role": "assistant", "content": "何が聞きたい？"}
    ]

# streamlit
st.title("AI Chatbot")

# streamlit
for message in st.session_state.messages:
    if message['role'] == 'user':
        st.chat_message("user").markdown(message['content'])
    elif message['role'] == 'assistant':
        st.chat_message("assistant").markdown(message['content'])

# 最新プロンプト
prompt = st.chat_input("どうしましたか？")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    state = {
        "user_input": prompt,
        "bot_output": "",
        "history": st.session_state.messages.copy()  # 初期状態の履歴をコピー
    }

    # グラフを実行
    state = graph.invoke(state)

    # 最終的な応答を履歴に追加
    st.session_state.messages.append({"role": "assistant", "content": state["bot_output"]})
    st.chat_message("assistant").markdown(state["bot_output"])