from agents.project_risk_manager import ProjectRiskManagerAgent
from agents.market_analysis_agent import MarketAnalysisAgent
from agents.risk_scoring_agent import RiskScoringAgent
from agents.status_tracking_agent import ProjectStatusTrackingAgent
from agents.reporting_agent import ReportingAgent
from crewai import Task, Crew, Process

class RiskChatBot:
    def __init__(self):
        self.agents = {
            "market": MarketAnalysisAgent,
            "finance": RiskScoringAgent,
            "status": ProjectStatusTrackingAgent,
            "reporting": ReportingAgent,
            "manager": ProjectRiskManagerAgent
        }

    def ask(self, query):
        # Check if this is a full analysis request
        if "full analysis" in query.lower() or "market analysis" in query.lower() or "comprehensive report" in query.lower() or "generate report" in query.lower():
            return self.run_full_analysis(query)
            
        # Standard routing logic for regular questions
        query_lower = query.lower()

        if "market" in query_lower or "economic" in query_lower:
            agent = self.agents["market"]
        elif "finance" in query_lower or "transaction" in query_lower:
            agent = self.agents["finance"]
        elif "status" in query_lower or "delay" in query_lower or "resource" in query_lower:
            agent = self.agents["status"]
        elif "report" in query_lower or "alert" in query_lower:
            agent = self.agents["reporting"]
        else:
            # Default to manager
            agent = self.agents["manager"]
        
        # Create a task for the agent with the user query
        task = Task(
            description=f"Answer the following question: {query}",
            expected_output="A detailed and helpful response to the user's query.",
            agent=agent
        )
        
        # Create a temporary crew with just the one agent
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )
        
        # Run the task and get the result
        result = crew.kickoff()
        return result
        
    def run_full_analysis(self, query):
        """Run a comprehensive analysis based on the user's query"""
        # Create custom task from the user query
        custom_task = Task(
            description=query,
            expected_output="A comprehensive analysis report addressing the specific request.",
            agent=ProjectRiskManagerAgent,
        )
        
        # Create a managed crew with the appropriate agents
        crew = Crew(
            agents=[
                MarketAnalysisAgent,
                RiskScoringAgent,
                ProjectStatusTrackingAgent,
                ReportingAgent
            ],
            tasks=[custom_task],
            manager=ProjectRiskManagerAgent,
            verbose=True
        )
        
        # Run the analysis
        result = crew.kickoff()
        return result
