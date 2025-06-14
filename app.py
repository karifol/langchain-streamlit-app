import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime

# LangChain
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-4o-mini", streaming=True)

# ツール
@tool
def search_web(query: str) -> str:
    """ウェブ検索を行います。"""
    if not query:
        return "検索内容がカラだね。何を探してるの？"
    search_tool = DuckDuckGoSearchRun()
    results = search_tool.run(query)
    if not results:
        return "なんも見つからないよ"
    return f"検索結果: {results[:500]}..."  # 最初の500文字だけ返す
llm_with_tool = chat.bind_tools([search_web])

st.title("MORALIM AI Chatbot")

if "messages" not in st.session_state:
    today = datetime.now().strftime("%Y-%m-%d")
    st.session_state.messages = [
        {"role": "system", "content": f"あなたはぶっきらぼうな女友達です。名前はMORALIM（もらりむ）です。今日は{today}です。"},
        {"role": "assistant", "content": "久しぶり、元気？"},
    ]

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant", avatar="assets/20240902_mora.png"):
            st.markdown(message["content"])

prompt = st.chat_input("どうしましたか？")

if prompt:
    # ユーザーの入力を追加
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # LangChain用のメッセージリストを作成
    lc_messages = []
    for m in st.session_state.messages:
        if m["role"] == "user":
            lc_messages.append(HumanMessage(content=m["content"]))
        elif m["role"] == "assistant":
            lc_messages.append(AIMessage(content=m["content"], name="assistant", avatar="assets/20240902_mora.png"))
        elif m["role"] == "system":
            lc_messages.append(SystemMessage(content=m["content"]))

    # LLM呼び出し
    response = llm_with_tool.invoke(lc_messages)

    if response.tool_calls:
        # ツールコールがある場合は、ツールを実行
        for call in response.tool_calls:
            with st.chat_message("assistant", avatar="assets/20240902_mora.png"):
                st.markdown("調べるね...")
            st.session_state.messages.append({"role": "assistant", "content": "調べるね..."})
            tool_result = search_web(call["args"])
            summary_prompt = f"以下はウェブ検索の結果です。これを参考にして、ユーザーの質問に日本語で分かりやすく答えてください。\n\n検索結果:\n{tool_result}\n\n質問:\n{prompt}"
            lc_messages.append(HumanMessage(content=summary_prompt))
            response = chat.invoke(lc_messages)
            with st.chat_message("assistant", avatar="assets/20240902_mora.png"):
                st.markdown(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})
    else:
        # ツールコールがない場合はそのまま応答
        with st.chat_message("assistant", avatar="assets/20240902_mora.png"):
            st.markdown(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})