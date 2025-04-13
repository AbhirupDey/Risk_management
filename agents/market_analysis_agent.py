from crewai import Agent
import os
from langchain_mistralai.chat_models import ChatMistralAI

llm = ChatMistralAI(
            api_key=os.getenv("Y5Ijf2FsA8D6PYLAVZGFigvOvmycMYp6"),
            model="mistral/mistral-large-latest"
        )

MarketAnalysisAgent = Agent(
    role="Market Analysis Agent",
    goal="Monitor and interpret financial trends, economic indicators, and market news to detect external project risks.",
    backstory=(
        "You scan external data sources including economic reports and financial news to understand "
        "potential threats from the market that might affect project delivery."
    ),
    llm=llm,
)
