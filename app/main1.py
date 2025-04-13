from crewai import Agent, Task, Crew, Process
from agents.project_risk_manager import ProjectRiskManagerAgent
from agents.market_analysis_agent import MarketAnalysisAgent
from agents.risk_scoring_agent import RiskScoringAgent
from agents.status_tracking_agent import ProjectStatusTrackingAgent
from langchain_openai import ChatOpenAI
import streamlit as st
import re
from chatbot.bot_interface import RiskChatBot

# Function to clean markdown formatting
def clean_markdown_formatting(text):
    """
    Remove markdown formatting characters like asterisks, hashtags, and hyphens.
    """
    if not isinstance(text, str):
        text = str(text)
        
    # Remove heading markers (#)
    text = re.sub(r'#+\s*', '', text)
    
    # Remove bold/italic markers (*)
    text = re.sub(r'\*+', '', text)
    
    # Remove list item markers (-)
    text = re.sub(r'^\s*-\s*', '', text, flags=re.MULTILINE)
    
    return text

# Initialize session state to store chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
if 'bot' not in st.session_state:
    st.session_state.bot = RiskChatBot()

# Define tasks
risk_task = Task(
    description="Assess the overall risk for Project Phoenix and generate a mitigation report.",
    expected_output="A detailed report highlighting potential risks and strategies to mitigate them.",
    agent=ProjectRiskManagerAgent,
)

market_task = Task(
    description="Analyze market conditions that may impact Project Phoenix's success.",
    expected_output="A comprehensive market analysis report with key trends and threats.",
    agent=MarketAnalysisAgent,
)

score_task = Task(
    description="Evaluate risk factors and provide a numerical risk score for Project Phoenix.",
    expected_output="A clear risk score (1-10) with reasoning.",
    agent=RiskScoringAgent,
)

status_task = Task(
    description="Monitor current project progress and highlight delays or issues.",
    expected_output="A real-time status update report identifying bottlenecks or blockers.",
    agent=ProjectStatusTrackingAgent,
)

tasks = [risk_task, market_task, score_task, status_task]

# Create crew
crew = Crew(
    agents=[
        ProjectRiskManagerAgent,
        MarketAnalysisAgent,
        RiskScoringAgent,
        ProjectStatusTrackingAgent
    ],
    tasks=tasks,
    process=Process.sequential,
    verbose=True,
)

# Streamlit UI
st.set_page_config(page_title="Project Risk Manager", layout="wide")
st.title("🚀 Project Risk Analysis Dashboard")

# Create tabs for different features
tab1, tab2 = st.tabs(["Full Risk Analysis", "Interactive Query"])

with tab1:
    if st.button("Run Full Risk Analysis"):
        with st.spinner("Running risk assessment..."):
            results = crew.kickoff()
        
        # Convert CrewOutput to string and clean the markdown formatting
        formatted_results = clean_markdown_formatting(str(results))

        st.success("Analysis Complete!")
        st.markdown("### 📄 Mitigation Report")
        st.write(formatted_results)

with tab2:
    st.markdown("### 💬 Ask the Crew")
    st.markdown("Enter your query about any aspect of the project risk, profiles, or reports.")
    
    # Chat input and send button
    query = st.text_input("Your Query:")
    if st.button("Send Query"):
        if query:
            # Add user query to chat history
            st.session_state.chat_history.append({"role": "user", "content": query})
            
            # Get response from the appropriate agent
            with st.spinner("Processing your query..."):
                response = st.session_state.bot.ask(query)
                # Clean the response formatting
                formatted_response = clean_markdown_formatting(str(response))
                
            # Add bot response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": formatted_response})
    
    # Display chat history
    st.markdown("### Conversation History")
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Assistant:** {message['content']}")
