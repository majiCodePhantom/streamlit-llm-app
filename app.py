
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from streamlit_chat import message
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



st.title("switchLLM-streamlit")

st.write("このアプリでは、料理とファッションの専門家からの回答を得ることができます。専門家を選択して、質問を入力してください。" \
"")




selected_item = st.radio(
    "どっちの専門家を選びますか？",
    ["料理専門家", "ファッション専門家"]
)


def get_expert_answer(selected_item, user_input):
    if selected_item == "料理専門家":
        system_content = "あなたは料理の専門家です。料理のレシピ、栄養、調理法などについて詳しく回答してください。"
    elif selected_item == "ファッション専門家":
        system_content = "あなたはファッションの専門家です。スタイリング、コーディネート、トレンドなどについて詳しく回答してください。"
    else:
        system_content = ""

    if not user_input or not system_content:
        return None

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# 選択した専門家に応じたメッセージを表示
st.markdown(f"### {selected_item}への質問")
user_input = st.text_input(f"{selected_item}に聞きたいことを入力してください:")

if st.button("送信"):
    if user_input:
        with st.spinner("回答を生成中..."):
            answer = get_expert_answer(selected_item, user_input)
        if answer:
            st.markdown(f"### {selected_item}の回答")
            message(answer, is_user=False)
        else:
            st.warning("回答を生成できませんでした。もう一度お試しください。")
    else:
        st.warning("質問を入力してください。")


