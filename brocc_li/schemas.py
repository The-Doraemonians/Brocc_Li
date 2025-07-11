from typing import Annotated, List, Literal, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

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
