from crewai import Agent
import os
from langchain_mistralai.chat_models import ChatMistralAI

llm = ChatMistralAI(
            api_key=os.getenv("Y5Ijf2FsA8D6PYLAVZGFigvOvmycMYp6"),
            model="mistral/mistral-large-latest"
        )


RiskScoringAgent = Agent(
    role="Risk Scoring Agent",
    goal="Analyze transaction history and investment data to assess project financial risk.",
    backstory=(
        "You are a data-focused risk specialist who evaluates financial risks, "
        "flags unusual patterns, and updates the project risk score accordingly."
    ),
    llm=llm,
)
