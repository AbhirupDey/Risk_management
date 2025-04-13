import streamlit as st
from crewai import Crew, Task, Process, Agent
from agents.project_risk_manager import ProjectRiskManagerAgent
from agents.market_analysis_agent import MarketAnalysisAgent
from agents.risk_scoring_agent import RiskScoringAgent
from agents.status_tracking_agent import ProjectStatusTrackingAgent
from agents.reporting_agent import ReportingAgent
from langchain_mistralai.chat_models import ChatMistralAI
import os
import re
import json
from datetime import datetime
from chatbot.bot_interface import RiskChatBot
from app.ui_components import (
    init_ui, render_chat_message, render_card, 
    render_status_indicator, render_section_header, 
    render_footer, format_report_text, format_colon_separated_text
)

# LLM Configuration
llm = ChatMistralAI(
    api_key=os.getenv("Y5Ijf2FsA8D6PYLAVZGFigvOvmycMYp6"),
    model="mistral/mistral-large-latest"
)

def clean_markdown_formatting(text):
    """
    Remove markdown formatting characters like asterisks, hashtags, and hyphens.
    """
    # Check if text is not a string (like CrewOutput object) and convert it
    if not isinstance(text, str):
        text = str(text)
        
    # Remove heading markers (#)
    text = re.sub(r'#+\s*', '', text)
    
    # Remove bold/italic markers (*)
    text = re.sub(r'\*+', '', text)
    
    # Remove list item markers (-)
    text = re.sub(r'^\s*-\s*', '', text, flags=re.MULTILINE)
    
    return text

def detect_and_fix_colon_format(text):
    """
    Check if the text follows the problematic colon-separated pattern and fix it.
    """
    # Check for the pattern of multiple lines with only colons or starts with dashes
    colon_only_lines = re.findall(r'(?:\n\s*:\s*){2,}', text)
    dashes_pattern = r'^--+\s*\n'
    title_and_colons = re.search(r'^(.+?)\n\s*:+', text, re.DOTALL)
    
    # If the text matches any of our problematic patterns, apply special formatting
    if colon_only_lines or re.search(dashes_pattern, text) or title_and_colons:
        return format_colon_separated_text(text)
    else:
        return None  # Not the problematic format

def save_analysis_results(results, filename=None):
    """
    Save analysis results to a file and return the file path
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"risk_analysis_{timestamp}.txt"
    
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, "w") as f:
        f.write(str(results))
    
    return filepath

# Define task creator function to ensure fresh task instances
def create_tasks():
    # Tasks for sequential process
    return [
        Task(
            description="Assess the overall risk for Project Phoenix and generate a mitigation report.",
            expected_output="A detailed report highlighting potential risks and strategies to mitigate them.",
            agent=ProjectRiskManagerAgent,
        ),
        Task(
            description="Analyze market conditions that may impact Project Phoenix's success.",
            expected_output="A comprehensive market analysis report with key trends and threats.",
            agent=MarketAnalysisAgent,
        ),
        Task(
            description="Evaluate risk factors and provide a numerical risk score for Project Phoenix.",
            expected_output="A clear risk score (1-10) with reasoning.",
            agent=RiskScoringAgent,
        ),
        Task(
            description="Monitor current project progress and highlight delays or issues.",
            expected_output="A real-time status update report identifying bottlenecks or blockers.",
            agent=ProjectStatusTrackingAgent,
        )
    ]

# Create managed crew task
managed_task = Task(
    description="Assess the overall risk for Project Phoenix and generate a comprehensive report covering market conditions, financial risks, project status, and mitigation strategies.",
    expected_output="A detailed risk assessment report with actionable insights.",
    agent=ProjectRiskManagerAgent,
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
if 'bot' not in st.session_state:
    st.session_state.bot = RiskChatBot()
    
if 'latest_report' not in st.session_state:
    st.session_state.latest_report = None
    
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0

if 'raw_results' not in st.session_state:
    st.session_state.raw_results = None

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = "expanded"

if 'current_project' not in st.session_state:
    st.session_state.current_project = "Project Phoenix"

# Initialize the UI with professional design and use full page width
init_ui(use_wide_mode=True)

# Create sidebar for navigation and project selection
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <div style="font-size: 1.8rem; margin-right: 10px;">🔍</div>
        <div style="font-weight: 600; font-size: 1.2rem; color: #102a43;">
            ProjectRisk AI
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu
    st.markdown("### Navigation", unsafe_allow_html=True)
    
    nav_options = ["Dashboard", "Risk Analysis", "Interactive Query"]
    nav_icons = ["📊", "📝", "💬"]
    
    for i, (option, icon) in enumerate(zip(nav_options, nav_icons)):
        if st.button(f"{icon} {option}", use_container_width=True, key=f"nav_{option}"):
            st.session_state.active_tab = i
            st.rerun()
    
    st.divider()
    
    # Project selection
    # st.markdown("### Project")
    # project_options = ["Project Phoenix", "Project Athena", "Project Titan"]
    # selected_project = st.selectbox("Select project", project_options, index=project_options.index(st.session_state.current_project))
    
    # if selected_project != st.session_state.current_project:
    #     st.session_state.current_project = selected_project
    #     st.rerun()
    
    # st.divider()
    
    # Settings and tools with improved contrast
    st.markdown("### Settings", unsafe_allow_html=True)
    analysis_depth = st.select_slider(
        "Analysis Depth",
        options=["Basic", "Standard", "Comprehensive"],
        value="Standard"
    )
    
    show_advanced = st.checkbox("Show Advanced Options", value=False)
    
    if show_advanced:
        st.markdown("### Advanced Options")
        st.slider("Risk Threshold", min_value=1, max_value=10, value=7)
        st.multiselect("Focus Areas", 
                     ["Market Trends", "Financial", "Technical", "Resource", "Schedule"],
                     default=["Market Trends", "Financial"])
    
    # Bottom section with app info - improved contrast
    st.divider()
    st.markdown("""
    <div style="font-size: 0.8rem; color: #3e4c59;">
        <div style="font-weight: 500; margin-bottom: 0.5rem;">About</div>
        <div>ProjectRisk AI v1.0</div>
        <div>Using Mistral AI</div>
        <div style="margin-top: 0.5rem;">© 2025 Risk Analytics</div>
    </div>
    """, unsafe_allow_html=True)

# Create tabs with improved styling
tabs = st.tabs([
    "📊 Dashboard", 
    "📝 Risk Analysis", 
    "💬 Interactive Query"
])

with tabs[0]:
    # Dashboard Layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_section_header("Project Overview", "Current status and key metrics")
        
        # Project Status Card
        project_status = """
        <div style="display: flex; flex-direction: column; gap: 0.75rem;">
            <div>
                <span style="font-weight: 500;">Current Phase:</span> Implementation
            </div>
            <div>
                <span style="font-weight: 500;">Progress:</span> 67% Complete
            </div>
            <div style="display: flex; align-items: center;">
                <span style="font-weight: 500; margin-right: 0.5rem;">Status:</span>
                <div style="display: flex; align-items: center;">
                    <div class="status-indicator status-warning"></div>
                    <span>At Risk</span>
                </div>
            </div>
        </div>
        """
        render_card("Project Status", project_status, icon="🚀")
        
        # Timeline Card
        if st.session_state.latest_report:
            render_card("Latest Risk Assessment", 
                      format_report_text(st.session_state.latest_report[:500] + "..." if len(st.session_state.latest_report) > 500 else st.session_state.latest_report),
                      icon="📈")
        else:
            render_card("Latest Risk Assessment", 
                     "<em>No risk assessment has been run yet. Use the Risk Analysis tab to generate one.</em>",
                     icon="📈")
    
    with col2:
        render_section_header("Quick Actions", "Run common tasks")
        
        # Quick action buttons with better styling
        st.markdown("""
        <div style="background-color: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);">
            <div style="margin-bottom: 1rem; font-weight: 500;">Start an analysis or query the AI:</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Using button clicks to change tabs without reloading the page
        if st.button("📝 Run Full Risk Analysis"):
            st.session_state.active_tab = 1
            st.rerun()
        
        if st.button("💬 Ask a Question"):
            st.session_state.active_tab = 2
            st.rerun()
        
        # Recent Activity Card
        activity_content = """
        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                <div>Risk Analysis Run</div>
                <div style="color: #6B7280;">Today, 10:15 AM</div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                <div>Market Analysis Updated</div>
                <div style="color: #6B7280;">Yesterday, 2:30 PM</div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                <div>Timeline Adjusted</div>
                <div style="color: #6B7280;">Apr 11, 9:45 AM</div>
            </div>
        </div>
        """
        render_card("Recent Activity", activity_content, icon="🕒")

with tabs[1]:
    render_section_header("Risk Analysis", "Generate comprehensive risk reports for Projects")
    
    # Add some professional description text
    st.markdown("""
    <div style="background-color: white; border-radius: 12px; padding: 1rem; margin-bottom: 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);">
        <p>The risk analysis will evaluate multiple factors including market conditions, financial data, project status, and potential anomalies.
        This comprehensive analysis helps identify threats and opportunities for Projects.</p>
        
        The AI-powered crew will collaborate to provide actionable insights and mitigation strategies.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Analysis Options
        analysis_options = st.radio(
            "Analysis Type",
            ["Comprehensive (Manager-led)", "Sequential (Task-based)"],
            horizontal=True
        )
        
        st.markdown('<div style="margin-bottom: 1rem;"><span class="badge">Comprehensive</span></div>', unsafe_allow_html=True)
        
        # Custom task description input field
        custom_description = st.text_area(
            "Custom Analysis Request (Optional)", 
            placeholder="Enter your specific analysis request here. Leave blank to use the default analysis.", 
            help="Customize what you want the AI to analyze. For example: 'Analyze Project Phoenix's market risks with focus on supply chain disruptions'",
            height=100
        )
        
        # Run Analysis Button with better styling
        if st.button("Run Analysis", key="run_analysis_btn"):
            # Use custom description if provided, otherwise use default
            task_description = custom_description if custom_description.strip() else "Assess the overall risk for Project Phoenix and generate a comprehensive report covering market conditions, financial risks, project status, and mitigation strategies."
            
            # Create task with custom or default description
            custom_task = Task(
                description=task_description,
                expected_output="A detailed risk assessment report with actionable insights based on the specific request.",
                agent=ProjectRiskManagerAgent,
            )
            
            if analysis_options == "Comprehensive (Manager-led)":
                # Create a managed crew with the custom task
                crew_to_use = Crew(
                    agents=[
                        MarketAnalysisAgent,
                        RiskScoringAgent,
                        ProjectStatusTrackingAgent,
                        ReportingAgent
                    ],
                    tasks=[custom_task],  # Using custom task
                    manager=ProjectRiskManagerAgent,
                    verbose=True
                )
                spinner_text = "AI crew manager is coordinating the risk analysis..."
            else:
                # For sequential process, customize the first task
                tasks = create_tasks()
                tasks[0] = custom_task  # Replace the first task with the custom one
                
                # Create a sequential crew with multiple tasks
                crew_to_use = Crew(
                    agents=[
                        ProjectRiskManagerAgent,
                        MarketAnalysisAgent,
                        RiskScoringAgent,
                        ProjectStatusTrackingAgent
                    ],
                    tasks=tasks,
                    process=Process.sequential,
                    verbose=True
                )
                spinner_text = "AI crew is sequentially analyzing project risks..."
                
            with st.spinner(spinner_text):
                results = crew_to_use.kickoff()
            
            # Convert CrewOutput to string and clean the markdown formatting
            formatted_results = clean_markdown_formatting(str(results))
            st.session_state.latest_report = formatted_results
            st.session_state.raw_results = str(results)
            
            st.success("Analysis Complete!")
            
            # Display the report in a professional card
            st.markdown('<div class="section-header">📄 Risk Assessment Report</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #00C6B6;">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="font-size: 1.5rem; margin-right: 10px;">📊</div>
                    <h3 style="margin: 0; color: #2E3559;">Project Risk Assessment</h3>
                    <div style="margin-left: auto; font-size: 0.9rem; color: #6B7280;">
                        Generated {datetime.now().strftime("%B %d, %Y at %H:%M")}
                    </div>
                </div>
                <div>{format_report_text(formatted_results)}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add download button for the analysis results
            filepath = save_analysis_results(st.session_state.raw_results)
            st.download_button(
                label="Download Analysis Results",
                data=open(filepath, "r").read(),
                file_name=filepath,
                mime="text/plain"
            )
            
            # Show raw results
            with st.expander("Show Raw Results"):
                st.text_area("Raw Analysis Results", st.session_state.raw_results, height=300)
    
    with col2:
        # Analysis Options
        st.markdown("""
        <div style="background-color: white; border-radius: 12px; padding: 1rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); margin-bottom: 1rem;">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">Analysis Scope</div>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="width: 1rem; height: 1rem; border-radius: 4px; background-color: #4F6AFF; margin-right: 0.5rem;"></div>
                <div>Market Conditions</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="width: 1rem; height: 1rem; border-radius: 4px; background-color: #4F6AFF; margin-right: 0.5rem;"></div>
                <div>Financial Risk</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="width: 1rem; height: 1rem; border-radius: 4px; background-color: #4F6AFF; margin-right: 0.5rem;"></div>
                <div>Project Status</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="width: 1rem; height: 1rem; border-radius: 4px; background-color: #4F6AFF; margin-right: 0.5rem;"></div>
                <div>Risk Mitigation</div>
            </div>
        </div>
        
        <div style="background-color: white; border-radius: 12px; padding: 1rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">Agent Crew</div>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="width: 2rem; height: 2rem; border-radius: 50%; background-color: #2E3559; display: flex; align-items: center; justify-content: center; color: white; margin-right: 0.5rem;">PM</div>
                <div>Risk Manager</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="width: 2rem; height: 2rem; border-radius: 50%; background-color: #4F6AFF; display: flex; align-items: center; justify-content: center; color: white; margin-right: 0.5rem;">MA</div>
                <div>Market Analyst</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="width: 2rem; height: 2rem; border-radius: 50%; background-color: #00C6B6; display: flex; align-items: center; justify-content: center; color: white; margin-right: 0.5rem;">RS</div>
                <div>Risk Scorer</div>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <div style="width: 2rem; height: 2rem; border-radius: 50%; background-color: #FFAD33; display: flex; align-items: center; justify-content: center; color: white; margin-right: 0.5rem;">ST</div>
                <div>Status Tracker</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tabs[2]:
    render_section_header("Interactive Query", "Ask questions and get AI-powered answers about Projects")
    
    # Column layout for chat interface
    chat_col1, chat_col2 = st.columns([3, 1])
    
    with chat_col1:
        # Enhanced chat container with better styling
        st.markdown("""
        <div style="background-color: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08); margin-bottom: 1.5rem; max-height: 550px; overflow-y: auto;">
            <div id="chat-container" style="min-height: 0px;">
        """, unsafe_allow_html=True)
        
        # Display chat history
        if not st.session_state.chat_history:
            st.markdown("""
                <div style="text-align: center; padding: 3rem 1rem; color: #475569;">
                    <div style="font-size: 3rem; margin-bottom: 1.5rem;">💬</div>
                    <div style="font-weight: 500; font-size: 1.1rem; margin-bottom: 0.75rem;">No messages yet</div>
                    <div>Start a conversation by asking a question about Projects or request a full analysis.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            for message in st.session_state.chat_history:
                render_chat_message(message["content"], message["role"])
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Enhanced chat input with better styling
        with st.container():
            st.markdown("""
            <div style="background-color: white; border-radius: 12px; padding: 1.25rem; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);">
                <div style="font-weight: 500; font-size: 0.9rem; color: #475569; margin-bottom: 0.75rem;">
                    Type your question...
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([5, 1])
            with col1:
                query = st.text_input("Query Input", key="query_input", placeholder="E.g., What is the current risk score for the project?", label_visibility="collapsed")
            with col2:
                send_btn = st.button("Send", key="send_btn", use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
                
            if send_btn and query:
                # Add user query to chat history
                st.session_state.chat_history.append({"role": "user", "content": query})
                
                # Get response from the appropriate agent
                with st.spinner("AI is thinking..."):
                    response = st.session_state.bot.ask(query)
                    
                    # Clean the response formatting
                    raw_response = str(response)
                    
                    # Check if the response has the problematic colon format first
                    formatted_response = detect_and_fix_colon_format(raw_response)
                    
                    # If it's not in the problematic format, just clean the markdown
                    if formatted_response is None:
                        formatted_response = clean_markdown_formatting(raw_response)
                    
                # Add bot response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": formatted_response})
                
                # Rerun to update the chat display
                st.rerun()
    
    with chat_col2:
        # Enhanced suggested questions
        st.markdown("""
        <div style="background-color: white; border-radius: 12px; padding: 1.25rem; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08); margin-bottom: 1.5rem;">
            <div style="font-weight: 600; margin-bottom: 1rem; color: #1E293B;">Suggested Questions</div>
        """, unsafe_allow_html=True)
        
        # Create clickable suggested questions with improved styling
        questions = [
            "What is the current risk score?",
            "What market trends affect Phoenix?",
            "Summarize project status",
            "Any financial anomalies?",
            "What are the top risks?"
        ]
        
        for i, question in enumerate(questions):
            button_style = "margin-bottom: 0.6rem;" if i < len(questions)-1 else ""
            if st.button(question, key=f"suggest_{question}", use_container_width=True):
                # Add user query to chat history
                st.session_state.chat_history.append({"role": "user", "content": question})
                
                # Get response from the appropriate agent
                with st.spinner("AI is thinking..."):
                    response = st.session_state.bot.ask(question)
                    # Clean the response formatting
                    formatted_response = clean_markdown_formatting(str(response))
                    
                # Add bot response to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": formatted_response})
                
                # Rerun to update the chat display
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Enhanced information card
        st.markdown("""
        <div style="background-color: white; border-radius: 12px; padding: 1.25rem; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);">
            <div style="font-weight: 600; margin-bottom: 0.75rem; color: #1E293B;">How It Works</div>
            <div style="color: #334155; line-height: 1.5;">
                <p style="margin-bottom: 0.75rem;">Questions are routed to specialized AI agents based on topic:</p>
                <div style="background-color: #F8FAFC; border-radius: 8px; padding: 1rem; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <div style="width: 1.5rem; height: 1.5rem; border-radius: 50%; background-color: #1A56DB; display: flex; align-items: center; justify-content: center; color: white; margin-right: 0.5rem; font-size: 0.7rem;">PM</div>
                        <div style="font-weight: 500;">Project Manager</div>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <div style="width: 1.5rem; height: 1.5rem; border-radius: 50%; background-color: #2563EB; display: flex; align-items: center; justify-content: center; color: white; margin-right: 0.5rem; font-size: 0.7rem;">MA</div>
                        <div style="font-weight: 500;">Market Analyst</div>
                    </div>
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <div style="width: 1.5rem; height: 1.5rem; border-radius: 50%; background-color: #059669; display: flex; align-items: center; justify-content: center; color: white; margin-right: 0.5rem; font-size: 0.7rem;">RS</div>
                        <div style="font-weight: 500;">Risk Scorer</div>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <div style="width: 1.5rem; height: 1.5rem; border-radius: 50%; background-color: #D97706; display: flex; align-items: center; justify-content: center; color: white; margin-right: 0.5rem; font-size: 0.7rem;">ST</div>
                        <div style="font-weight: 500;">Status Tracker</div>
                    </div>
                </div>
                <div style="font-size: 0.9rem; margin-top: 0.75rem; color: #475569;">
                    For comprehensive analysis, try asking for a "full market analysis" or "risk report".
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Pro tip box
        st.markdown("""
        <div style="background-color: #F0F9FF; border-radius: 12px; padding: 1rem; margin-top: 1.5rem; border-left: 3px solid #0EA5E9;">
            <div style="font-weight: 600; color: #0369A1; display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="margin-right: 0.5rem;">💡</span> Pro Tip
            </div>
            <div style="color: #334155; font-size: 0.9rem;">
                Try asking detailed questions like "What supply chain risks might affect Project Phoenix in the next quarter?"
            </div>
        </div>
        """, unsafe_allow_html=True)

# Render professional footer
render_footer()

# Set the active tab based on session state (for navigation from dashboard)
if st.session_state.active_tab != 0:
    # This JavaScript will switch to the appropriate tab
    # Note: In real deployment, we'd need to ensure this JS runs after the page loads
    js = f"""
    <script>
        // Function to click the {st.session_state.active_tab}th tab
        function clickTab() {{
            const tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
            if (tabs.length > {st.session_state.active_tab}) {{
                tabs[{st.session_state.active_tab}].click();
            }}
        }}
        // Try to run immediately
        clickTab();
        // If that didn't work, try again after a short delay
        setTimeout(clickTab, 100);
    </script>
    """
    st.components.v1.html(js)
    # Reset the active tab to prevent loop
    st.session_state.active_tab = 0