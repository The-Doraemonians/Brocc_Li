from pathlib import Path

from brocc_li.agent import initialize_agent
from brocc_li.state import initialize_session_state
from brocc_li.ui import (
    render_chat,
    render_header,
    render_input_area,
    render_sidebar,
    setup_page,
)
from brocc_li.utils import get_config


def run(title: str, icon_path: str | Path):
    initialize_session_state()

    setup_page(title, icon_path)

    cfg = get_config()
    api_key = cfg.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key is required. Please set GOOGLE_API_KEY in your config."
        )

    state_graph = initialize_agent(api_key)

    # ui sections
    render_header()
    render_chat()
    render_input_area(state_graph)
    render_sidebar()
