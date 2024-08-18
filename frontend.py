import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ChatMessage
from langchain_upstage import ChatUpstage

from langchain_core.messages import HumanMessage

from app.graphs import graph
from app.naver_map import get_geocode


st.set_page_config(page_title="Jeju Travel 💬", page_icon="💬")
st.title("Jeju Travel 💬")

if "messages" not in st.session_state:
    st.session_state["messages"] = []


def print_history():
    for msg in st.session_state["messages"]:
        st.chat_message(msg.role, avatar="💻" if msg.role == "ai" else "😀").write(
            msg.content
        )


def add_history(role, content):
    st.session_state["messages"].append(ChatMessage(role=role, content=content))


with st.sidebar:
    clear_btn = st.button("Clear Chat History")
    user_place = st.text_area(
        "Current Location", value="제주 제주시 공항로 2 제주국제공항"
    )

    tab1, tab2 = st.tabs(["My Location", "_"])
    user_text_apply_btn = tab1.button("Apply My Current Location", key="apply1")
    if user_text_apply_btn:
        my_coordinates = get_geocode(user_place)
        if my_coordinates[0] is None:
            tab1.markdown("❌ Cannot find the location.")
        else:
            tab1.markdown(
                f"""
                ✅ Checked.\n
                Longitude: {my_coordinates[0]}\n
                Latitude: {my_coordinates[1]}
            """
            )
        st.session_state["chain"] = graph

if clear_btn:
    retriever = st.session_state["messages"].clear()

print_history()


if "chain" not in st.session_state:
    # user_prompt
    st.session_state["chain"] = graph
if user_input := st.chat_input():
    add_history("user", user_input)
    st.chat_message("user", avatar="😀").write(user_input)
    with st.chat_message("assistant", avatar="💻"):
        chat_container = st.empty()
        human_message = HumanMessage(content=user_input)

        res = st.session_state["chain"].invoke(input=human_message)
        chat_container.text(res[-1].content)
        add_history("ai", res[-1].content)
