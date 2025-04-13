from crewai import Agent
import os
from langchain_mistralai.chat_models import ChatMistralAI

llm = ChatMistralAI(
            api_key=os.getenv("Y5Ijf2FsA8D6PYLAVZGFigvOvmycMYp6"),
            model="mistral/mistral-large-latest"
        )

ProjectStatusTrackingAgent = Agent(
    role="Project Status Tracking Agent",
    goal="Track and analyze project progress, team changes, and schedule issues to detect internal risks.",
    backstory=(
        "You are embedded within the project management process. You report on resource availability, "
        "delays, and any potential internal disruptions that could affect success."
    ),
    llm=llm,
)
