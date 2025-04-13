from crewai import Agent
import os
from langchain_mistralai.chat_models import ChatMistralAI

llm = ChatMistralAI(
            api_key=os.getenv("Y5Ijf2FsA8D6PYLAVZGFigvOvmycMYp6"),
            model="mistral/mistral-large-latest"
        )

# Project domain-specific context data
PROJECT_CONTEXT = {
    "domain": "Project Risk Management",
    "projects": {
        "primary": "Project Phoenix",
        "description": "A strategic digital transformation initiative with a budget of $2.5M and a 12-month timeline",
        "key_risks": ["technology adoption", "resource constraints", "market volatility", "stakeholder alignment", "scope creep"]
    },
    "risk_categories": ["Market & Economic", "Financial", "Operational", "Technical", "Organizational", "External"]
}

ProjectRiskManagerAgent = Agent(
    role="Project Risk Manager",
    goal="Evaluate and mitigate overall project risk based on all available information.",
    backstory=(
        "You are responsible for overseeing the risk landscape of multiple projects including Project Phoenix. "
        "You coordinate insights from various agents to synthesize a clear risk picture "
        "and propose mitigation strategies to the leadership team. Your expertise includes "
        "PMBOK risk management practices, quantitative risk analysis, and enterprise risk frameworks. "
        "You specialize in balancing trade-offs between scope, time, cost, and quality while "
        "managing uncertainties across the project lifecycle."
    ),
    allow_delegation=True,
    llm=llm,
    tools=[],  # Add any specific tools if needed
    context=PROJECT_CONTEXT
)
