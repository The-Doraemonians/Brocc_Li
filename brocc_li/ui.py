from pathlib import Path

import streamlit as st
from langgraph.graph.state import CompiledStateGraph
from PIL import Image
from streamlit_chat import message
from streamlit_extras.bottom_container import bottom

from brocc_li.agent import process_agent_response
from brocc_li.schemas import Chat
from brocc_li.state import get_initial_chat_state


def setup_page(title: str, icon_path: str | Path) -> None:
    icon = Image.open(icon_path)

    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    st.logo(icon, size="large")


def render_header() -> None:
    st.markdown(
        """
        <style>
            .welcome-text {
                text-align: center;
                font-size: 2rem;
                font-weight: bold;
            }
        </style>
        <div class="welcome-text">Welcome to Brocc Li!</div>
        """,
        unsafe_allow_html=True,
    )


def render_chat() -> None:
    chat: Chat = st.session_state["chat"]

    with st.container(border=True):
        for idx, chat_item in enumerate(chat):
            message(
                chat_item["data"],
                key=f"chat-item-{idx}",
                is_user=(chat_item["by"] == "user"),
                avatar_style="no-avatar",
                allow_html=True,
                is_table=(chat_item["type"] == "table"),
            )


def render_input_area(state_graph: CompiledStateGraph) -> None:
    if st.session_state.get("pending_response"):
        user_input = st.session_state["pending_response"]
        process_agent_response(user_input, state_graph)
        st.rerun()

    with bottom():
        form = st.form("input_form", clear_on_submit=True, border=False)
        with form:
            left, right = form.columns([4, 0.75], vertical_alignment="bottom")
            user_input = left.text_area(
                "User Input:",
                key="user_input",
                placeholder="Ask anything about diet planning...",
            )
            send = right.form_submit_button(
                icon=":material/send:",
                label="Send",
                use_container_width=True,
            )

        if send and user_input and user_input.strip():
            st.session_state["pending_response"] = user_input
            submit_user_input(user_input)


def render_sidebar() -> None:
    st.sidebar.title("Brocc Li")
    st.sidebar.button("Login", use_container_width=True)
    st.sidebar.button(
        "Clear Chat",
        key="clear_chat",
        use_container_width=True,
        type="primary",
        on_click=on_clear_chat_btn_click,
    )

    # current conversation stats
    if st.session_state.get("agent_messages"):
        st.sidebar.markdown("### Conversation Stats")
        st.sidebar.write(f"Messages: {len(st.session_state.agent_messages)}")


def submit_user_input(user_input: str) -> None:
    st.session_state["chat"].append(
        {
            "by": "user",
            "type": "normal",
            "data": user_input,
        }
    )

    st.rerun()


def on_clear_chat_btn_click() -> None:
    del st.session_state["chat"]
    del st.session_state["agent_messages"]

    st.session_state["chat"] = get_initial_chat_state()
    st.session_state["agent_messages"] = []
