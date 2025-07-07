import dotenv
import streamlit as st
import os
import setup_agent

# OpenAI APIキーを設定
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

graph = setup_agent.main()

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
        "history": st.session_state.messages.copy()
    }

    # グラフを実行
    with st.spinner("考え中..."):
        state = graph.invoke(state)

    # 最終的な応答を履歴に追加
    st.session_state.messages.append({"role": "assistant", "content": state["bot_output"]})
    st.chat_message("assistant").markdown(state["bot_output"])