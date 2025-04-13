from crewai import Agent
import os
from langchain_mistralai.chat_models import ChatMistralAI

llm = ChatMistralAI(
            api_key=os.getenv("Y5Ijf2FsA8D6PYLAVZGFigvOvmycMYp6"),
            model="mistral/mistral-large-latest"
        )

# Reporting context data
REPORTING_CONTEXT = {
    "domain": "Project Risk Management",
    "project_focus": "Project Phoenix",
    "report_types": [
        "Executive Summary", 
        "Risk Register", 
        "Mitigation Action Plan", 
        "Status Dashboard",
        "Trend Analysis"
    ],
    "stakeholder_groups": [
        {"group": "Executive Leadership", "focus": "Strategic impact, ROI, governance"},
        {"group": "Project Team", "focus": "Tactical risks, resource needs, blockers"},
        {"group": "Business Units", "focus": "Operational impacts, change management, training"},
        {"group": "Technical Teams", "focus": "Technical debt, integration risks, security concerns"}
    ],
    "key_performance_indicators": [
        "Schedule Variance", "Cost Performance Index", "Risk Exposure Index", 
        "Scope Change Rate", "Resource Utilization", "Quality Metrics", 
        "Stakeholder Satisfaction"
    ],
    "alert_thresholds": {
        "critical": "Immediate action required (24-hour response)",
        "high": "Action required within 48 hours",
        "medium": "Action plan needed within 1 week",
        "low": "Monitor in regular project reviews"
    },
    "communication_protocols": {
        "emergency": "Direct call + email + alert in project dashboard",
        "high_priority": "Email + messaging + next status meeting",
        "routine": "Include in weekly status report"
    }
}

ReportingAgent = Agent(
    role="Reporting Agent",
    goal="Generate clear risk reports and real-time alerts for decision-makers.",
    backstory=(
        "You are responsible for compiling a comprehensive view of Project Phoenix's risks and mitigation plans, "
        "and you create reports and alerts that are sent to leadership. You excel at translating complex project "
        "risk data into clear, actionable insights tailored to different stakeholder groups. Your expertise includes "
        "data visualization, executive communication, risk prioritization frameworks, and creating dashboards that "
        "highlight trends and emerging issues. You ensure that the right information reaches the right stakeholders "
        "at the right time to enable informed decision-making about project risks, focusing on digital transformation initiatives."
    ),
    llm=llm,
    tools=[],  # Add any specific tools if needed
    context=REPORTING_CONTEXT
)
