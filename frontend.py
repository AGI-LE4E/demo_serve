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
            st.session_state["longitude"] = my_coordinates[0]
            st.session_state["latitude"] = my_coordinates[1]
        st.session_state["chain"] = graph

if clear_btn:
    retriever = st.session_state["messages"].clear()


if "chain" not in st.session_state:
    # user_prompt
    st.session_state["chain"] = graph
if user_input := st.chat_input():
    st.chat_message("user", avatar="😀").write(user_input)
    with st.chat_message("assistant", avatar="💻"):
        chat_container = st.empty()
        human_message = HumanMessage(content=user_input)

        res = st.session_state["chain"].invoke(input=human_message)
        if res[-1].content == "No location found.":
            st.text("찾지 못했습니다.")
        else:
            locations = res[-1].content.split("\n\n")
            # 각 장소 정보를 처리하여 화면에 표시
            info_list = []
            for location in locations:
                # 각 줄을 분리하여 정보 추출
                details = location.split("\n")
                info = {}
                for detail in details:
                    if ": " not in detail:
                        continue
                    key, value = detail.strip().split(": ", 1)
                    info[key] = value
                info_list.append(info)
            try:
                longitude, latitude = (
                    float(st.session_state["longitude"]),
                    float(st.session_state["latitude"]),
                )
            except KeyError:
                longitude, latitude = 126.4959513, 33.5059364
            # Order by distance ASC
            info_list = sorted(
                info_list,
                key=lambda x: (
                    (float(x["Latitude"]) - latitude) ** 2
                    + (float(x["Longitude"]) - longitude) ** 2
                ),
            )
            for info in info_list[:5]:
                st.text(info["Title"])
                st.image(info["repPhoto"])
                st.text(f"Address: {info['Address']}")
                st.text(
                    f"Distance: {round(((float(info['Latitude']) - latitude) ** 2 + (float(info['Longitude']) - longitude) ** 2) ** 0.5,2)} km"
                )
                st.text(f"Phone Number: {info['Phone Number']}")
                st.markdown("---")  # 구분선
