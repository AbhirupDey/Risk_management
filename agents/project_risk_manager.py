from crewai import Agent
import os
from langchain_mistralai.chat_models import ChatMistralAI

llm = ChatMistralAI(
            api_key=os.getenv("Y5Ijf2FsA8D6PYLAVZGFigvOvmycMYp6"),
            model="mistral/mistral-large-latest"
        )

ProjectRiskManagerAgent = Agent(
    role="Project Risk Manager",
    goal="Evaluate and mitigate overall project risk based on all available information.",
    backstory=(
        "You are responsible for overseeing the risk landscape of multiple projects. "
        "You coordinate insights from various agents to synthesize a clear risk picture "
        "and propose mitigation strategies to the leadership team."
    ),
    allow_delegation=True,
    llm=llm,
)
