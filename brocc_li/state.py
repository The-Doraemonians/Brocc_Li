import streamlit as st

from brocc_li.schemas import USER_INSTRUCTIONS_MARKDOWN, Chat


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

    # message history for the agent
    if "agent_messages" not in st.session_state:
        st.session_state.setdefault("agent_messages", [])
