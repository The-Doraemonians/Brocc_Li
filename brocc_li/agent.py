import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64
import json
from langchain_core.messages import HumanMessage, AnyMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)

class AgentState(TypedDict):
    # input_file: Optional[str]  # Contains file path, type (PNG)
    messages: Annotated[list[AnyMessage], add_messages]
    # preferences: Optional[dict]
    # bmi: Optional[float]
    # diet_plan: Optional[str]

def bmi_calculator(weight: float, height: float) -> float:
    """Calculate BMI from weight and height."""
    if height <= 0 or weight <= 0:
        raise ValueError("Height and weight must be greater than zero.")
    return weight / (height ** 2)

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
    # Remove any leading/trailing whitespace again
    content = content.strip()
    print("Cleaned content:", repr(content))
    try:
        return json.loads(content)
    except Exception as e:
        print("Error parsing JSON from extract_preferences:", e)
        print("Raw content:", repr(content))
        return {}

def plan_diet(preferences: dict) -> str:
    """Plan a diet based on user preferences."""
    prompt = f"""Create a diet plan based on these preferences: {preferences}. 
    Include meals, snacks, and drinks. Ensure it meets the user's dietary needs."""
    response = llm.invoke(prompt)
    return response.content

tools = [
    bmi_calculator,
    # extract_text,
    extract_preferences,
    plan_diet
]
llm_with_tools = llm.bind_tools(tools)

# class AgentState(TypedDict):
#     # The input document
#     # input_file: Optional[str]  # Contains file path, type (PNG)
#     messages: Annotated[list[AnyMessage], add_messages]
#     preferences: Optional[dict]
#     bmi: Optional[float]
#     diet_plan: Optional[str]
    
def assistant(state: AgentState):
    # System message
    textual_description_of_tool = """
    bmi_calculator(weight: float, height: float) -> float:
        Calculate BMI from weight and height.

        Args:
            weight: Weight in kilograms.
            height: Height in meters.

        Returns:
            The calculated BMI as a float.

    extract_preferences(user_input: str) -> dict:
        Extract structured diet preferences from user input.

        Args:
            user_input: A string containing the user's dietary preferences.

        Returns:
            A dictionary with fields like calories, protein, allergies, likes, dislikes, budget.
    plan_diet(preferences: dict) -> str:
        Plan a diet based on user preferences.

        Args:
            preferences: A dictionary containing the user's dietary preferences.

        Returns:
            A string containing a diet plan that includes meals, snacks, and drinks.
    """
    # image = state["input_file"]
    sys_msg = SystemMessage(content=f"You are an helpful agent that can analyse diet for user and run some computatio without provided tools :\n{textual_description_of_tool}")

    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

builder = StateGraph(AgentState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")
react_graph = builder.compile()

messages = []

print("🤖 I am your personal diet agent. You can ask me anything about diet or type 'quit/exit' to turn off.")
while True:
    user_input = input("👨 You: ")
    if user_input.lower().strip() in ["exit", "quit"]:
        print("👋 Exiting...")
        break
    # Add user message to history
    messages.append(HumanMessage(content=user_input))
    # Run the agent with the full history
    result = react_graph.invoke({"messages": messages, "input_file": None})
    print("🤖 Agent:")
    for m in result['messages']:
        m.pretty_print()
    # Optionally, add the latest assistant message to history for context
    messages.append(result['messages'][-1])



