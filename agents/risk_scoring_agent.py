from crewai import Agent
import os
from langchain_mistralai.chat_models import ChatMistralAI

llm = ChatMistralAI(
            api_key=os.getenv("Y5Ijf2FsA8D6PYLAVZGFigvOvmycMYp6"),
            model="mistral/mistral-large-latest"
        )

# Financial risk context data
FINANCIAL_RISK_CONTEXT = {
    "domain": "Project Risk Management",
    "project_focus": "Project Phoenix",
    "budget": "$2.5 million",
    "financial_metrics": {
        "ROI_threshold": "15%",
        "NPV_threshold": "$500,000",
        "payback_period": "24 months",
        "IRR_minimum": "12%"
    },
    "risk_scoring": {
        "scale": "1-10 (10 being highest risk)",
        "thresholds": {
            "critical": "8-10",
            "high": "6-7.9",
            "medium": "4-5.9",
            "low": "1-3.9"
        },
        "factors": [
            "probability", "impact", "detectability", 
            "proximity", "controllability", "urgency"
        ]
    },
    "cost_categories": [
        "technology infrastructure", "licensing", "implementation", 
        "training", "maintenance", "contingency"
    ]
}

RiskScoringAgent = Agent(
    role="Risk Scoring Agent",
    goal="Analyze transaction history and investment data to assess project financial risk.",
    backstory=(
        "You are a data-focused risk specialist who evaluates financial risks for Project Phoenix, "
        "flags unusual patterns, and updates the project risk score accordingly. You apply statistical "
        "methods and financial modeling techniques to quantify project uncertainties. Your expertise "
        "includes earned value management, ROI analysis, NPV calculations, cost variance analysis, and "
        "budget forecasting. You combine historical project data with current performance metrics to "
        "predict financial risks throughout the project lifecycle, focusing on digital transformation initiatives."
    ),
    llm=llm,
    tools=[],  # Add any specific tools if needed
    context=FINANCIAL_RISK_CONTEXT
)
