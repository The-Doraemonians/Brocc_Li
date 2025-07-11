# Brocc Li

## Overview

Your Personalized Diet Management Companion.

## Setup

### Prerequisites

- Python 3.11
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/The-Doraemonians/Brocc_Li.git
    cd Brocc_Li
    ```

2.  Create a virtual environment (recommended):

    ```bash
    uv venv
    ```

3.  Install the required packages using `uv`:

    ```bash
    uv sync
    ```

## Running the Application

To start the Brocc Li application, run the following command:

```bash
streamlit run main.py
```


### Project Architecture

```
brocc_li/                  # Python package
├── __init__.py            # package marker
├── app.py                 # Streamlit entrypoint: orchestrates UI
├── agent.py               # Agent initialization, agent state graph, and tool factories
├── schemas.py             # Pydantic/TypedDict schemas for agent state and chat
├── state.py               # Streamlit session state helpers
├── tools.py               # Tool factory functions for agent (make_calculate_bmi_tool, etc.)
├── ui.py                  # UI composition helpers
├── utils.py               # Utility functions
└── ...                    # (other files and folders)
```