import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from brocc_li.schemas import AgentState
from brocc_li.tools import (
    make_calculate_bmi_tool,
    make_extract_preferences_tool,
    make_plan_diet_tool,
)


@st.cache_resource
def initialize_agent(api_key: str):
    """Initialize the LangGraph agent - cached to avoid recreating on every rerun."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        api_key=api_key,
    )

    # LLM tools
    tools = [
        make_calculate_bmi_tool(),
        make_extract_preferences_tool(llm),
        make_plan_diet_tool(llm),
    ]
    llm_with_tools = llm.bind_tools(tools)

    def assistant(state: AgentState):
        textual_description_of_tool = """
        calculate_bmi(weight: float, height: float) -> float:
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

    # graph
    builder = StateGraph(AgentState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    return builder.compile()


def process_agent_response(user_input: str, state_graph: CompiledStateGraph) -> None:
    """Process user input with detailed step-by-step display."""
    try:
        # Add user message to agent history
        st.session_state.agent_messages.append(HumanMessage(content=user_input))

        # Create a placeholder for streaming updates
        response_placeholder = st.empty()

        with st.spinner("🤖 Agent is processing..."):
            # Stream the agent execution
            current_responses = []

            result = state_graph.invoke(
                {"messages": st.session_state.agent_messages, "input_file": None}
            )

            # Get all new messages
            new_messages = result["messages"][len(st.session_state.agent_messages) :]
            # print("Agent responses:", result["messages"])
            st.session_state.agent_messages.extend(new_messages)

            # Process each message and show progress
            for i, msg in enumerate(new_messages):
                # Check message type and extract content
                if hasattr(msg, "content") and msg.content:
                    if "calculate_bmi" in str(msg):
                        current_responses.append("🧮 Calculating BMI...")
                    elif "extract_preferences" in str(msg):
                        current_responses.append("📝 Extracting your preferences...")
                    elif "plan_diet" in str(msg):
                        current_responses.append(
                            "🍽️ Creating your personalized diet plan..."
                        )

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
            final_response = (
                str(new_messages[-1].content)
                if new_messages
                else "No response generated"
            )

        # Clear placeholder and add to chat
        response_placeholder.empty()

        st.session_state["chat"].append(
            {
                "by": "agent",
                "type": "normal",
                "data": final_response,
            }
        )

        # Clear the pending response flag
        if "pending_response" in st.session_state:
            del st.session_state["pending_response"]

    except Exception as e:
        st.error(f"Error processing with agent: {str(e)}")
        st.session_state["chat"].append(
            {
                "by": "agent",
                "type": "normal",
                "data": "Sorry, I encountered an error while processing your request.",
            }
        )
        if "pending_response" in st.session_state:
            del st.session_state["pending_response"]
