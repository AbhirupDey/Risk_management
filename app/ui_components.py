import streamlit as st
from datetime import datetime
import base64
import re

# Enhanced color scheme with better contrast
PRIMARY_COLOR = "#0052cc"  # Darker blue for better contrast
SECONDARY_COLOR = "#102a43"  # Darker shade for headers - almost black
ACCENT_COLOR = "#026e57"  # Darker teal for better contrast
BG_COLOR = "#ffffff"  # White background for maximum contrast
DARK_BG_COLOR = "#0c1524"  # Darker background for contrast areas
TEXT_COLOR = "#102a43"  # Very dark blue/gray text for readability
LIGHT_TEXT_COLOR = "#ffffff"  # White text for dark backgrounds
GRAY_TEXT = "#3e4c59"  # Darker gray for better readability
ERROR_COLOR = "#b91c1c"  # Darker red for errors
SUCCESS_COLOR = "#046c4e"  # Darker green for success
WARNING_COLOR = "#c05621"  # Darker orange for warnings
INPUT_BG_COLOR = "#f0f4f8"  # Light gray for input backgrounds
INPUT_TEXT_COLOR = "#102a43"  # Dark text for inputs

def get_base64_encoded_image(image_path):
    """Convert an image to base64 encoding"""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
        
def add_bg_from_local(image_path):
    """Add a local background image"""
    try:
        bin_str = get_base64_encoded_image(image_path)
        bg_styling = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-repeat: no-repeat;
        }}
        </style>
        '''
        st.markdown(bg_styling, unsafe_allow_html=True)
        return True
    except Exception as e:
        return False
        
def add_custom_css(use_wide_mode=False):
    """Add custom CSS styling with improved contrast"""
    st.markdown(f"""
    <style>
        /* Base Styling */
        .stApp {{
            background-color: {BG_COLOR};
            color: {TEXT_COLOR};
            font-family: 'Inter', sans-serif;
        }}
        
        /* Main header */
        .main-header {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {SECONDARY_COLOR};
            margin-bottom: 0.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid {PRIMARY_COLOR};
        }}
        
        /* UI Element Styling */
        .stButton>button {{
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            border: none;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            background-color: {PRIMARY_COLOR};
            color: white;
        }}
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            background-color: #00408f; /* Darker on hover */
        }}
        
        /* Tab styling with better contrast */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            white-space: pre-wrap;
            background-color: #f0f4f8; /* Light gray background */
            border-radius: 8px 8px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            color: {SECONDARY_COLOR}; /* Ensure tab text is dark for contrast */
            font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: white;
            border-top: 3px solid {PRIMARY_COLOR}; /* Thicker border for selected tab */
            font-weight: 600;
        }}
        
        /* Card styling with improved contrast */
        .card {{
            background-color: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.5rem;
            border-left: 4px solid {PRIMARY_COLOR};
        }}
        
        /* Message styling for chat with better contrast */
        .user-message {{
            background-color: #e6f0ff; /* Lighter blue background */
            padding: 1rem;
            border-radius: 12px 12px 2px 12px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            position: relative;
            color: {SECONDARY_COLOR}; /* Ensure text is dark enough */
        }}
        .assistant-message {{
            background-color: white;
            padding: 1rem;
            border-radius: 12px 12px 12px 2px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
            border-left: 3px solid {PRIMARY_COLOR};
            color: {TEXT_COLOR}; /* Ensure consistent text color */
        }}
        
        /* Text input styling with improved contrast */
        .stTextInput>div>div>input {{
            border-radius: 12px;
            border: 2px solid #cbd5e1; 
            padding: 10px 15px;
            font-size: 16px;
            color: {INPUT_TEXT_COLOR}; /* Dark text for readability */
            background-color: {INPUT_BG_COLOR}; /* Light background */
        }}
        .stTextInput>div>div>input:focus {{
            border-color: {PRIMARY_COLOR};
            box-shadow: 0 0 0 2px rgba(0, 82, 204, 0.15);
        }}
        .stTextInput>div>div>input::placeholder {{
            color: #829ab1; /* Darker placeholder text for better contrast */
        }}
        
        /* Text area styling with improved contrast */
        .stTextArea textarea {{
            border-radius: 12px;
            border: 2px solid #cbd5e1;
            padding: 10px 15px;
            font-size: 16px;
            color: {INPUT_TEXT_COLOR}; /* Dark text for readability */
            background-color: {INPUT_BG_COLOR}; /* Light background */
        }}
        .stTextArea textarea:focus {{
            border-color: {PRIMARY_COLOR};
            box-shadow: 0 0 0 2px rgba(0, 82, 204, 0.15);
        }}
        .stTextArea textarea::placeholder {{
            color: #829ab1; /* Darker placeholder text for better contrast */
        }}
        
        /* Status indicators */
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }}
        .status-good {{
            background-color: {SUCCESS_COLOR};
        }}
        .status-warning {{
            background-color: {WARNING_COLOR};
        }}
        .status-critical {{
            background-color: {ERROR_COLOR};
        }}
        
        /* Section headers */
        .section-header {{
            font-size: 1.5rem;
            font-weight: 600;
            color: {SECONDARY_COLOR};
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 1.5rem 0;
            font-size: 0.9rem;
            color: {GRAY_TEXT};
            border-top: 1px solid #cbd5e1;
            margin-top: 2rem;
        }}
        
        /* Streamlit overrides */
        div.block-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
            {'' if use_wide_mode else 'max-width: 1000px;'}
        }}
        
        /* Text styling with improved contrast */
        p {{
            line-height: 1.6;
            color: {TEXT_COLOR}; /* Ensure consistent paragraph text color */
        }}
        
        /* Badge styles */
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 500;
            margin-right: 0.5rem;
            background-color: rgba(0, 82, 204, 0.1); /* Transparent primary color */
            color: {PRIMARY_COLOR};
        }}
        
        /* Data item styling for formatted reports */
        .data-item {{
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #e2e8f0;
        }}
        .data-item:last-child {{
            border-bottom: none;
        }}
        .data-label {{
            font-weight: 600;
            color: {SECONDARY_COLOR};
            margin-bottom: 0.25rem;
        }}
        .data-value {{
            font-size: 1rem;
            color: {TEXT_COLOR}; /* Ensure consistent text color */
        }}
        
        /* Make scrollbars more visible */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: #f1f5f9;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #64748b;
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #475569;
        }}
        
        /* Ensure radio buttons have good contrast */
        .stRadio > div {{
            margin-bottom: 0.5rem;
        }}
        .stRadio label {{
            color: {TEXT_COLOR} !important;
            font-weight: 500;
        }}
        
        /* Sidebar styling with improved contrast */
        [data-testid="stSidebar"] {{
            background-color: #f8fafc;
            border-right: 1px solid #e2e8f0;
            padding: 1rem;
        }}
        [data-testid="stSidebar"] .block-container {{
            padding-top: 0;
        }}
        [data-testid="stSidebar"] button {{
            margin-bottom: 0.5rem;
            background-color: transparent;
            color: black;
            border: 1px solid #e2e8f0;
            box-shadow: none;
            text-align: left;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        [data-testid="stSidebar"] button:hover {{
            background-color: #f0f4f8;
            border-color: {PRIMARY_COLOR};
            transform: none;
        }}
        [data-testid="stSidebar"] hr {{
            margin: 1rem 0;
        }}
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stSlider label {{
            font-size: 0.9rem;
            font-weight: 500;
            color: black;
        }}
        
        /* Make all text in sidebar black */
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMarkdown {{
            color: black !important;
        }}

        /* Improved select box contrast */
        .stSelectbox div[data-baseweb="select"] > div {{
            background-color: {INPUT_BG_COLOR};
            color: {INPUT_TEXT_COLOR};
        }}
        
        /* Metric styling for better visibility */
        [data-testid="stMetric"] {{
            background-color: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        
        [data-testid="stMetric"] > div {{
            width: 100%;
        }}
        
        [data-testid="stMetricLabel"] {{
            display: flex;
            justify-content: center;
            align-items: center;
            color: {SECONDARY_COLOR};
            font-weight: 600;
        }}
        
        [data-testid="stMetricValue"] {{
            font-weight: 700;
            color: {PRIMARY_COLOR};
        }}

    </style>
    """, unsafe_allow_html=True)

def init_ui(use_wide_mode=False):
    """Initialize the UI with a professional look and feel"""
    st.set_page_config(
        page_title="ProjectRisk AI", 
        page_icon="🔍",
        layout="wide" if use_wide_mode else "centered",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS
    add_custom_css(use_wide_mode)
    
    # Try to load background image (optional)
    # Uncomment this if you have a background image
    # bg_image = "path/to/subtle_background.png"
    # if not add_bg_from_local(bg_image):
    #    pass  # If background image fails, we'll use the color background
    
    # Custom header with logo and title
    header_html = f"""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <div style="font-size: 2.5rem; margin-right: 10px;">🔍</div>
        <div>
            <h1 class="main-header">ProjectRisk AI</h1>
            <p style="color: {GRAY_TEXT}; margin-top: -5px;">
                Advanced risk analysis and intelligence for project management
            </p>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Current date
    current_date = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"<p style='color: {GRAY_TEXT};'>{current_date}</p>", unsafe_allow_html=True)

def render_chat_message(message, role):
    """Render a chat message with improved contrast for better readability"""
    timestamp = datetime.now().strftime("%H:%M")
    
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
            <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                <div style="font-weight: 600; color: {SECONDARY_COLOR}; display: flex; align-items: center;">
                    <span style="display: inline-block; width: 24px; height: 24px; background-color: #e6effc; border-radius: 50%; margin-right: 8px; text-align: center; line-height: 24px;">👤</span>
                    You
                </div>
                <div style="margin-left: auto; font-size: 0.8rem; color: {GRAY_TEXT};">
                    {timestamp}
                </div>
            </div>
            <div style="line-height: 1.6; color: {SECONDARY_COLOR}; font-size: 1rem;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <div style="display: flex; align-items: center; margin-bottom: 0.75rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.5rem;">
                <div style="font-weight: 600; color: {PRIMARY_COLOR}; display: flex; align-items: center;">
                    <span style="display: inline-block; width: 24px; height: 24px; background-color: #e6f0ff; border-radius: 50%; margin-right: 8px; text-align: center; line-height: 24px;">🔍</span>
                    ProjectRisk AI
                </div>
                <div style="margin-left: auto; font-size: 0.8rem; color: {GRAY_TEXT};">
                    {timestamp}
                </div>
            </div>
            <div style="line-height: 1.6; color: {TEXT_COLOR}; font-size: 1rem;">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_card(title, content, icon="📊"):
    """Render content in a professional card layout"""
    st.markdown(f"""
    <div class="card">
        <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
            <div style="font-size: 1.5rem; margin-right: 10px;">{icon}</div>
            <h3 style="margin: 0; color: {SECONDARY_COLOR};">{title}</h3>
        </div>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def render_status_indicator(status, label):
    """Render a visual status indicator"""
    status_class = "status-good" if status == "good" else "status-warning" if status == "warning" else "status-critical"
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
        <span class="status-indicator {status_class}"></span>
        <span style="color: {SECONDARY_COLOR};">{label}</span>
    </div>
    """, unsafe_allow_html=True)

def render_section_header(title, description=None):
    """Render a section header with optional description"""
    st.markdown(f"""
    <h2 class="section-header">{title}</h2>
    {f'<p style="color: {GRAY_TEXT}; margin-top: -0.5rem;">{description}</p>' if description else ''}
    """, unsafe_allow_html=True)

def render_footer():
    """Render a professional footer"""
    st.markdown("""
    <div class="footer">
        <div>© 2025 ProjectRisk AI</div>
        <div style="margin-top: 0.5rem;">
            Powered by advanced AI for comprehensive project risk analysis
        </div>
    </div>
    """, unsafe_allow_html=True)

def format_report_text(text):
    """Format report text for better readability with proper paragraph structure"""
    if not text:
        return ""
        
    # Add paragraph breaks at double newlines
    paragraphs = re.split(r'\n\s*\n', text)
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # Check if this looks like a section header
        if re.match(r'^[A-Z][A-Z\s]+:?$', paragraph) or re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+:?$', paragraph):
            # It's a section header, format it as a heading
            formatted_paragraphs.append(f'<h4 style="margin-top: 1.5rem; margin-bottom: 0.75rem; color: {SECONDARY_COLOR};">{paragraph}</h4>')
        
        # Check if this is a list item (starts with number or dash)
        elif re.match(r'^\s*(?:\d+\.|-)\s+', paragraph):
            # Process list items
            items = re.split(r'\n\s*(?:\d+\.|-)\s+', paragraph)
            list_items = []
            
            # The first item might be empty if the paragraph starts with a list marker
            if items and items[0].strip() == '':
                items = items[1:]
                
            for item in items:
                if item.strip():
                    list_items.append(f'<li style="margin-bottom: 0.5rem; color: {TEXT_COLOR};">{item.strip()}</li>')
            
            if list_items:
                formatted_list = f'<ul style="margin-top: 0.75rem; margin-bottom: 1rem; padding-left: 1.5rem;">{" ".join(list_items)}</ul>'
                formatted_paragraphs.append(formatted_list)
        
        # Check for key-value pairs (term: definition)
        elif ":" in paragraph and not re.search(r'\n', paragraph):
            parts = paragraph.split(":", 1)
            if len(parts) == 2 and parts[0].strip() and parts[1].strip():
                key = parts[0].strip()
                value = parts[1].strip()
                formatted_paragraphs.append(
                    f'<div class="data-item"><div class="data-label">{key}</div>'
                    f'<div class="data-value">{value}</div></div>'
                )
            else:
                # Regular paragraph
                formatted_paragraphs.append(f'<p style="margin-bottom: 1rem; line-height: 1.6; color: {TEXT_COLOR};">{paragraph}</p>')
        else:
            # Regular paragraph
            formatted_paragraphs.append(f'<p style="margin-bottom: 1rem; line-height: 1.6; color: {TEXT_COLOR};">{paragraph}</p>')
    
    # Add styling to section titles (detected by capitalized text followed by colon)
    result = "".join(formatted_paragraphs)
    
    # Add styling to important metrics and numbers
    result = re.sub(r'(\d+(?:\.\d+)?(?:\s*%)?\s*(?:out of)\s*\d+)', 
                r'<span style="color:' + PRIMARY_COLOR + '; font-weight: 600;">\1</span>', result)
    
    # Format risk level indicators with proper colors
    result = re.sub(r'(High)\s+Risk', 
                r'<span style="font-weight: 600; color: ' + ERROR_COLOR + ';">\1 Risk</span>', result)
    result = re.sub(r'(Medium)\s+Risk', 
                r'<span style="font-weight: 600; color: ' + WARNING_COLOR + ';">\1 Risk</span>', result)
    result = re.sub(r'(Low)\s+Risk', 
                r'<span style="font-weight: 600; color: ' + SUCCESS_COLOR + ';">\1 Risk</span>', result)
    
    # Highlight specific keywords
    result = re.sub(r'(Risk Score:)\s+(\d+(?:\.\d+)?)', 
                r'\1 <span style="font-size: 1.1rem; font-weight: 600; color: ' + SECONDARY_COLOR + ';">\2</span>', result)
    
    # Add visual separation for sections
    result = re.sub(r'<h4', r'<div style="margin-top: 1rem;"></div><h4', result)
    
    return result

def format_colon_separated_text(text):
    """
    Format text that uses colons as separators with empty lines between sections.
    This handles cases where the text looks like:
    
    --
    
    :
    :
    Some content
    :
    More content
    """
    if not text:
        return ""
    
    # First, extract the title if present (before the colons)
    title_match = re.match(r'^(.*?)\n\s*:+', text, re.DOTALL)
    title = ""
    if title_match:
        title = title_match.group(1).strip()
    
    # Clean up the text by removing dashes and colons
    text = re.sub(r'^--+\s*\n', '', text)  # Remove leading dashes
    text = re.sub(r'\n\s*--+\s*$', '', text)  # Remove trailing dashes
    
    # Process conclusion section separately if it exists
    conclusion_match = re.search(r'Conclusion\s*\n\n?(.*?)(?=\n\n|$)', text, re.DOTALL)
    conclusion_text = ""
    if conclusion_match:
        conclusion_text = conclusion_match.group(1).strip()
        # Remove conclusion from the main text to avoid duplication
        text = re.sub(r'Conclusion\s*\n\n?.*?(?=\n\n|$)', '', text, re.DOTALL)
    
    # Replace isolated colons with empty strings
    text = re.sub(r'^\s*:\s*$', '', text, flags=re.MULTILINE)
    
    # Split the text by newlines and filter out empty lines and lines with only colons
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line and line != ':' and not re.match(r'^\s*:\s*$', line):
            lines.append(line)
    
    # Format the content into clean paragraphs
    html_parts = []
    
    if title:
        html_parts.append(f"""
        <div style="font-size: 1.5rem; font-weight: 600; color: {SECONDARY_COLOR}; margin-bottom: 1rem; text-align: center;">
            {title}
        </div>
        """)
    
    # Process remaining content
    current_section = ""
    for line in lines:
        if line and not line.isspace():  # Make sure line has content
            # Clean any remaining colons at the beginning or end of lines
            line = re.sub(r'^\s*:\s*', '', line)
            line = re.sub(r'\s*:\s*$', '', line)
            
            if line and not line.isspace():  # Check again after cleaning
                html_parts.append(f"""
                <div style="margin-bottom: 0.75rem; line-height: 1.5; color: {TEXT_COLOR};">
                    {line}
                </div>
                """)
    
    # Add conclusion section if it exists
    if conclusion_text:
        html_parts.append(f"""
        <div style="margin-top: 1rem; border-top: 1px solid #e5e7eb; padding-top: 1rem;">
            <div style="font-weight: 600; color: {SECONDARY_COLOR}; margin-bottom: 0.5rem;">Conclusion</div>
            <div style="line-height: 1.5; color: {TEXT_COLOR};">{conclusion_text}</div>
        </div>
        """)
    
    # Join all parts and wrap in a container
    result = f"""
    <div style="background-color: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); margin-bottom: 1.5rem;">
        {''.join(html_parts)}
    </div>
    """
    
    return result
