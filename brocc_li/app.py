from pathlib import Path
from typing import List, Literal, TypedDict
import json

import streamlit as st
from PIL import Image
from streamlit_chat import message
from streamlit_extras.bottom_container import bottom

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated

from brocc_li.utils import get_config

cfg = get_config()

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


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def get_initial_chat_state() -> Chat:
    return [
        {
            "by": "agent",
            "type": "normal",
            "data": USER_INSTRUCTIONS_MARKDOWN,
        }
    ]


@st.cache_resource
def initialize_agent():
    """Initialize the LangGraph agent - cached to avoid recreating on every rerun."""
    
    GOOGLE_API_KEY = cfg["GOOGLE_API_KEY"]
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1, api_key=GOOGLE_API_KEY)

    def bmi_calculator(weight: float, height: float) -> float:
        """Calculate BMI from weight and height."""
        if height <= 0 or weight <= 0:
            raise ValueError("Height and weight must be greater than zero.")
        return weight / (height**2)

    def extract_preferences(user_input: str) -> dict:
        """Extract preferences from user input."""
        prompt = f"""Extract structured diet preferences from this: "{user_input}". 
        Return ONLY a dictionary with fields like calories, protein, allergies, likes, dislikes, budget.
        Do NOT include any extra text, code block markers, or the word 'json'. Just output the JSON object.
        All the options just optional, if not provided, just return undefined.
        Example: 
        {{
            "calories": 2000,
            "protein": 150,
            "allergies": ["nuts", "gluten"],
            "likes": ["chicken", "rice"],
            "dislikes": ["fish"],
            "budget": 50
        }}"""
        response = llm.invoke(prompt)
        content = response.content.strip()
        # Remove code block markers and 'json' if present
        if content.startswith("```"):
            content = content.strip("`")
            if content.lower().startswith("json"):
                content = content[4:].strip()
        if content.lower().startswith("json"):
            content = content[4:].strip()
        content = content.strip()
        try:
            return json.loads(content)
        except Exception as e:
            st.error(f"Error parsing JSON: {e}")
            return {}

    def plan_diet(preferences: dict) -> str:
        """Plan a diet based on user preferences."""
        prompt = f"""Create a diet plan based on these preferences: {preferences}. 
        Include meals, snacks, and drinks. Ensure it meets the user's dietary needs."""
        response = llm.invoke(prompt)
        return response.content

    tools = [bmi_calculator, extract_preferences, plan_diet]
    llm_with_tools = llm.bind_tools(tools)

    def assistant(state: AgentState):
        textual_description_of_tool = """
        bmi_calculator(weight: float, height: float) -> float:
            Calculate BMI from weight and height.

        extract_preferences(user_input: str) -> dict:
            Extract structured diet preferences from user input.

        plan_diet(preferences: dict) -> str:
            Plan a diet based on user preferences.
        """
        
        sys_msg = SystemMessage(
            content=f"You are a helpful agent that can analyze diet for users and run computations with provided tools:\n{textual_description_of_tool}"
        )

        return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

    # Build the graph
    builder = StateGraph(AgentState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")
    
    return builder.compile()


def initialize_session_state() -> None:
    """Initialize session state variables."""
    if "chat" not in st.session_state:
        st.session_state.setdefault("chat", get_initial_chat_state())

    if "user_input" not in st.session_state:
        st.session_state.setdefault("user_input", "")
    
    # Initialize message history for the agent
    if "agent_messages" not in st.session_state:
        st.session_state.setdefault("agent_messages", [])


def process_agent_response(user_input: str, react_graph) -> None:
    """Process user input with detailed step-by-step display."""
    try:
        # Add user message to agent history
        st.session_state.agent_messages.append(HumanMessage(content=user_input))
        
        # Create a placeholder for streaming updates
        response_placeholder = st.empty()
        
        with st.spinner("🤖 Agent is processing..."):
            # Stream the agent execution
            current_responses = []
            
            result = react_graph.invoke({
                "messages": st.session_state.agent_messages,
                "input_file": None
            })
            
            # Get all new messages
            new_messages = result["messages"][len(st.session_state.agent_messages):]
            # print("Agent responses:", result["messages"])
            st.session_state.agent_messages.extend(new_messages)
            
            # Process each message and show progress
            for i, msg in enumerate(new_messages):
                # Check message type and extract content
                if hasattr(msg, 'content') and msg.content:
                    if "bmi_calculator" in str(msg):
                        current_responses.append("🧮 Calculating BMI...")
                    elif "extract_preferences" in str(msg):
                        current_responses.append("📝 Extracting your preferences...")
                    elif "plan_diet" in str(msg):
                        current_responses.append("🍽️ Creating your personalized diet plan...")
                    
                    # Add the actual content
                    content = str(msg.content)
                    if content and content.strip() and len(content) > 10:
                        current_responses.append(content)
                
                # Update the display with current progress
                if current_responses:
                    response_placeholder.markdown("\n\n".join(current_responses))
        
        # Final response
        if current_responses:
            final_response = "\n\n".join(current_responses)
        else:
            # Fallback
            final_response = str(new_messages[-1].content) if new_messages else "No response generated"
        
        # Clear placeholder and add to chat
        response_placeholder.empty()
        
        st.session_state["chat"].append({
            "by": "agent",
            "type": "normal",
            "data": final_response,
        })
        
        # Clear the pending response flag
        if "pending_response" in st.session_state:
            del st.session_state["pending_response"]
            
    except Exception as e:
        st.error(f"Error processing with agent: {str(e)}")
        st.session_state["chat"].append({
            "by": "agent",
            "type": "normal",
            "data": "Sorry, I encountered an error while processing your request.",
        })
        if "pending_response" in st.session_state:
            del st.session_state["pending_response"]


def submit_user_input(user_input: str, react_graph) -> None:
    """Handle submission in the user input text area."""
    # Add user message to chat first
    st.session_state["chat"].append({
        "by": "user",
        "type": "normal",
        "data": user_input,
    })
    
    # Trigger a rerun to show the user message immediately
    st.rerun()


def on_clear_chat_btn_click() -> None:
    """Handle the Clear Chat button click."""
    del st.session_state["chat"]
    del st.session_state["agent_messages"]
    st.session_state["chat"] = get_initial_chat_state()
    st.session_state["agent_messages"] = []


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


def render_input_area(react_graph) -> None:
    """Render the user input area."""
    # Check if we need to process a pending response
    if st.session_state.get("pending_response"):
        user_input = st.session_state["pending_response"]
        process_agent_response(user_input, react_graph)
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
            # Set pending response to process after rerun
            st.session_state["pending_response"] = user_input
            submit_user_input(user_input, react_graph)


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
    
    # Display current conversation stats
    if st.session_state.get("agent_messages"):
        st.sidebar.markdown("### Conversation Stats")
        st.sidebar.write(f"Messages: {len(st.session_state.agent_messages)}")


def run(icon_path: str | Path) -> None:
    """Main function to run the Streamlit app."""
    initialize_session_state()
    
    icon = Image.open(icon_path)

    st.set_page_config(
        page_title="Brocc Li - Personalized Diet Management Companion",
        page_icon=icon,
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    st.logo(icon, size="large")

    # Initialize the agent
    react_graph = initialize_agent()

    # Render sections
    render_header()
    render_chat()
    render_input_area(react_graph)
    render_sidebar()
