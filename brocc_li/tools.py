import json

import streamlit as st
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI


def make_calculate_bmi_tool():
    """Create a tool to calculate BMI from weight and height."""

    @tool
    def calculate_bmi(weight: float, height: float) -> float:
        """Calculate BMI from weight (kg) and height (m)."""
        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive values.")
        return weight / (height**2)

    return calculate_bmi


def make_extract_preferences_tool(llm: ChatGoogleGenerativeAI):
    """Create a tool to extract diet preferences from user input."""

    @tool
    def extract_preferences(user_input: str) -> dict:
        """Extract structured diet preferences from user input."""
        prompt = (
            f"Extract structured diet preferences from this: '{user_input}'. "
            "Return ONLY a JSON object with keys: calories, protein, allergies, likes, dislikes, budget."
        )
        response = llm.invoke(prompt)
        content = response.content.strip()

        # strip markdown fences and leading 'json' if present
        if content.startswith("```"):
            content = content.strip("`")
            if content.lower().startswith("json"):
                content = content[4:].strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse preferences JSON: {e}")
            return {}

    return extract_preferences


def make_plan_diet_tool(llm: ChatGoogleGenerativeAI):
    """Create a tool to plan a diet based on user preferences."""

    @tool
    def plan_diet(preferences: dict) -> str:
        """Plan a diet based on user preferences."""
        prompt = (
            f"Create a diet plan that meets these preferences: {preferences}. "
            "Include meals, snacks, and drinks."
        )
        response = llm.invoke(prompt)

        return response.content

    return plan_diet
