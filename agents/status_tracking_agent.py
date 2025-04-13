from crewai import Agent
import os
from langchain_mistralai.chat_models import ChatMistralAI

llm = ChatMistralAI(
            api_key=os.getenv("Y5Ijf2FsA8D6PYLAVZGFigvOvmycMYp6"),
            model="mistral/mistral-large-latest"
        )

# Project status context data
PROJECT_STATUS_CONTEXT = {
    "domain": "Project Risk Management",
    "project_focus": "Project Phoenix",
    "current_phase": "Implementation",
    "progress": "67% complete",
    "timeline": {
        "start_date": "May 15, 2024",
        "planned_end_date": "May 15, 2025",
        "current_milestone": "System Integration",
        "next_milestone": "User Acceptance Testing",
        "critical_path_items": ["API development", "Database migration", "Security testing"]
    },
    "resource_allocation": {
        "developers": "85% allocated",
        "designers": "60% allocated",
        "qa_testers": "75% allocated",
        "project_managers": "100% allocated"
    },
    "key_metrics": {
        "sprint_velocity": "Declining (last 3 sprints)",
        "bug_count": "Increasing (37 open issues)",
        "requirements_stability": "Medium (8 change requests pending)"
    },
    "recent_issues": [
        "Integration delays with third-party services",
        "Key developer resignation",
        "Stakeholder disagreement on feature priority"
    ]
}

ProjectStatusTrackingAgent = Agent(
    role="Project Status Tracking Agent",
    goal="Track and analyze project progress, team changes, and schedule issues to detect internal risks.",
    backstory=(
        "You are embedded within the Project Phoenix management process. You report on resource availability, "
        "delays, and any potential internal disruptions that could affect success. Your expertise includes "
        "project schedule analysis, resource utilization tracking, critical path management, and agile metrics "
        "monitoring. You identify early warning signs of project issues by analyzing trends in progress data, "
        "team performance metrics, and deliverable quality indicators. You provide objective status assessments "
        "that highlight internal risk factors specifically for digital transformation initiatives."
    ),
    llm=llm,
    tools=[],  # Add any specific tools if needed
    context=PROJECT_STATUS_CONTEXT
)
