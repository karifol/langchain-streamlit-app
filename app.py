import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.title("MORALIM AI ")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "あなたはぶっきらぼうな女友達です。名前はMORALIM（もらりむ）です。"}
    ]

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):  # ユーザー用アイコン
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

    chat = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-4o-mini", streaming=True)
    with st.chat_message("assistant", avatar="assets/20240902_mora.png"):
        response_stream = chat.stream(lc_messages)
        response_content = st.write_stream(response_stream)

    # モデルの応答を追加
    st.session_state.messages.append({"role": "assistant", "content": response_content})