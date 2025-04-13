from crewai import Agent
import os
from langchain_mistralai.chat_models import ChatMistralAI

llm = ChatMistralAI(
            api_key=os.getenv("Y5Ijf2FsA8D6PYLAVZGFigvOvmycMYp6"),
            model="mistral/mistral-large-latest"
        )

# Market-specific context data
MARKET_CONTEXT = {
    "domain": "Project Risk Management",
    "project_focus": "Project Phoenix",
    "project_type": "Digital Transformation",
    "market_factors": [
        "inflation trends", "industry regulations", "competitor landscape", 
        "supply chain disruptions", "technology shifts", "labor market"
    ],
    "economic_indicators": [
        "GDP growth", "interest rates", "unemployment", "consumer confidence", 
        "industry-specific indices", "technology adoption rates"
    ],
    "risk_thresholds": {
        "high": "Immediate action required - significant impact on project viability",
        "medium": "Planning and monitoring required - moderate impact possible",
        "low": "Regular monitoring - minimal impact expected"
    }
}

MarketAnalysisAgent = Agent(
    role="Market Analysis Agent",
    goal="Monitor and interpret financial trends, economic indicators, and market news to detect external project risks.",
    backstory=(
        "You scan external data sources including economic reports and financial news to understand "
        "potential threats from the market that might affect Project Phoenix's delivery. Your analysis "
        "focuses specifically on digital transformation projects in the current economic climate. "
        "You have expertise in market trend analysis, competitive intelligence, and industry forecasting "
        "with special attention to how external factors create risk exposure for technology initiatives. "
        "You translate complex market data into actionable insights for project stakeholders."
    ),
    llm=llm,
    tools=[],  # Add any specific tools if needed
    context=MARKET_CONTEXT
)
