from crewai import Agent
import os
from langchain_mistralai.chat_models import ChatMistralAI

llm = ChatMistralAI(
            api_key=os.getenv("Y5Ijf2FsA8D6PYLAVZGFigvOvmycMYp6"),
            model="mistral/mistral-large-latest"
        )


ReportingAgent = Agent(
    role="Reporting Agent",
    goal="Generate clear risk reports and real-time alerts for decision-makers.",
    backstory=(
        "You are responsible for compiling a comprehensive view of all risks and mitigation plans, "
        "and you create reports and alerts that can be sent to leadership."
    ),
    llm=llm,
)
