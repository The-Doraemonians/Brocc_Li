from pathlib import Path
from typing import List, Literal, TypedDict

import streamlit as st
from PIL import Image
from streamlit_chat import message
from streamlit_extras.bottom_container import bottom

USER_INSTRUCTIONS_MARKDOWN: str = """
### Planning Your Diet
Provide the following inputs to personalize your diet plan:

    1. Basic Profile Information: age, gender, height, weight, personal goal
    2. Location: country, city, distance limit
    3. Dietary Preferences & Restrictions: dietary style, cuisine, allergies
    4. Time & Cooking Preferences: cooking skill level, time per meal
    5. Budget Preferences: daily food budget, prioritize deals
"""


class ChatItem(TypedDict):
    by: Literal["agent", "user"]  # Who sent the message (e.g., "agent" or "user")
    type: Literal["normal", "table"]  # Type of the message (e.g., "normal", "table")
    data: str  # The content of the message


Chat = List[ChatItem]


def get_initial_chat_state() -> Chat:
    return [
        {
            "by": "agent",
            "type": "normal",
            "data": USER_INSTRUCTIONS_MARKDOWN,
        }
    ]


def initialize_session_state() -> None:
    """Initialize session state variables."""
    if "chat" not in st.session_state:
        st.session_state.setdefault("chat", get_initial_chat_state())

    if "user_input" not in st.session_state:
        st.session_state.setdefault("user_input", "")


def login() -> None:
    """Handle the login button click."""
    if st.button("Log in"):
        st.session_state["logged_in"] = True
        st.rerun()


def logout() -> None:
    """Handle the logout button click."""
    if st.button("Log out"):
        st.session_state["logged_in"] = False
        st.rerun()


def submit_user_input(user_input) -> None:
    """Handle submission in the user input text area."""
    st.session_state["chat"].append(
        {
            "by": "user",
            "type": "normal",
            "data": user_input,
        }
    )

    st.rerun()


def on_clear_chat_btn_click() -> None:
    """Handle the Clear Chat button click."""
    del st.session_state["chat"]
    st.session_state["chat"] = get_initial_chat_state()


def render_header() -> None:
    """Render the header section."""
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
    """Render the chat container."""
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


def render_input_area() -> None:
    """Render the user input area."""
    with bottom():
        form = st.form("input_form", clear_on_submit=True, border=False)
        with form:
            left, right = form.columns([4, 0.75], vertical_alignment="bottom")
            user_input = left.text_area(
                "User Input:",
                key="user_input",
                placeholder="Ask anything",
            )
            send = right.form_submit_button(
                icon=":material/send:",
                label="Send",
                use_container_width=True,
            )

        if send and user_input and user_input.strip():
            submit_user_input(user_input)


def render_sidebar() -> None:
    """Render the sidebar."""
    st.sidebar.title("Brocc Li")
    st.sidebar.button("Login", use_container_width=True)
    st.sidebar.button(
        "Clear Chat",
        key="clear_chat",
        use_container_width=True,
        type="primary",
        on_click=on_clear_chat_btn_click,
    )


def run() -> None:
    """Main function to run the Streamlit app."""
    initialize_session_state()

    st.set_page_config(
        page_title="Brocc Li - Personalized Diet Management Companion",
        page_icon=icon,
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    st.logo(icon, size="large")

    # Render sections
    render_header()
    render_chat()
    render_input_area()
    render_sidebar()
