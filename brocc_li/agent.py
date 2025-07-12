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
    make_web_search_tools,
)


@st.cache_resource
def initialize_agent(api_key: str):
    """Initialize the LangGraph agent - cached to avoid recreating on every rerun."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        api_key=api_key,
    )

    # Get web search tools
    web_tools = make_web_search_tools()

    # LLM tools
    tools = [
        make_calculate_bmi_tool(),
        make_extract_preferences_tool(llm),
        make_plan_diet_tool(llm),
        web_tools['search_nearby_stores'],
        web_tools['search_product_prices'],
        web_tools['search_coupons'],
        web_tools['search_recipes'],
        web_tools['scrape_store_website'],
        web_tools['get_store_hours_and_location'],
        web_tools['compare_prices_across_stores'],
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

        search_nearby_stores(location: str, store_types: List[str] = None) -> List[Dict]:
            Search for nearby grocery stores using Google Maps API.

        search_product_prices(product_name: str, location: str = None) -> List[Dict]:
            Search for product prices across different stores (Rewe, Aldi, Lidl, Edeka).

        search_coupons(store_name: str = None, category: str = None) -> List[Dict]:
            Search for available coupons and deals from various coupon websites.

        search_recipes(query: str, dietary_restrictions: List[str] = None, max_time: int = None) -> List[Dict]:
            Search for recipes from popular cooking websites including German sites.

        scrape_store_website(store_url: str, product_search: str = None) -> Dict:
            Scrape product information from a specific store website using Selenium.

        get_store_hours_and_location(store_name: str, location: str) -> Dict:
            Get detailed store information including hours and exact location.

        compare_prices_across_stores(product_list: List[str], location: str) -> Dict:
            Compare prices for multiple products across different stores.
        """

        sys_msg = SystemMessage(
            content=f"""You are a comprehensive diet assistant that can analyze diet preferences, plan meals, and help with grocery shopping. You have access to these tools:

{textual_description_of_tool}

You can help users with:
- Diet planning and BMI calculations
- Finding nearby grocery stores
- Comparing product prices across stores
- Finding coupons and deals
- Searching for recipes
- Web scraping store information

When users ask about shopping, recipes, or store locations, use the appropriate web search tools to provide real-time information."""
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
                    elif "search_nearby_stores" in str(msg):
                        current_responses.append("🏪 Searching for nearby stores...")
                    elif "search_product_prices" in str(msg):
                        current_responses.append("💰 Checking product prices...")
                    elif "search_coupons" in str(msg):
                        current_responses.append("🎫 Looking for coupons and deals...")
                    elif "search_recipes" in str(msg):
                        current_responses.append("👨‍🍳 Finding recipes...")
                    elif "scrape_store_website" in str(msg):
                        current_responses.append("🌐 Scraping store information...")
                    elif "get_store_hours_and_location" in str(msg):
                        current_responses.append("📍 Getting store details...")
                    elif "compare_prices_across_stores" in str(msg):
                        current_responses.append("⚖️ Comparing prices across stores...")

                    # Add the actual content
                    content = str(msg.content)
                    if content and content.strip() and len(content) > 10:
                        print('--------------------------------')
                        print(i)
                        print(msg)
                        print(content)
                        print('--------------------------------')
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
