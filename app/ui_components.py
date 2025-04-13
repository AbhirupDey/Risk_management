import streamlit as st
from datetime import datetime
import base64
import re

# Color scheme
PRIMARY_COLOR = "#1A56DB"  # Darker blue with better contrast
SECONDARY_COLOR = "#1E293B"  # Darker shade for headers
ACCENT_COLOR = "#059669"  # Darker teal for better contrast
BG_COLOR = "#F8FAFC"  # Very light background
DARK_BG_COLOR = "#0F172A"  # Darker background for contrast areas
TEXT_COLOR = "#1E293B"  # Dark text for readability
LIGHT_TEXT_COLOR = "#FFFFFF"  # White text
GRAY_TEXT = "#475569"  # Darker gray for better readability
ERROR_COLOR = "#DC2626"  # Brighter red for errors
SUCCESS_COLOR = "#059669"  # Darker green for success
WARNING_COLOR = "#D97706"  # Darker orange for warnings

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
        
def add_custom_css():
    """Add custom CSS styling"""
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
            background-color: #164db0; /* Slightly darker on hover */
        }}
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            white-space: pre-wrap;
            background-color: rgba(255, 255, 255, 0.8); /* More opaque for better contrast */
            border-radius: 8px 8px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            color: {SECONDARY_COLOR}; /* Ensure tab text is visible */
            font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: white;
            border-top: 3px solid {PRIMARY_COLOR}; /* Thicker border for selected tab */
            font-weight: 600;
        }}
        
        /* Card styling */
        .card {{
            background-color: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.5rem;
            border-left: 4px solid {PRIMARY_COLOR};
        }}
        
        /* Message styling for chat */
        .user-message {{
            background-color: #EFF6FF; /* Slightly darker blue background */
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
        
        /* Text input styling */
        .stTextInput>div>div>input {{
            border-radius: 12px;
            border: 2px solid #CBD5E1; /* Darker border for better contrast */
            padding: 10px 15px;
            font-size: 16px;
            color: white; /* Text color changed to white */
            background-color: {SECONDARY_COLOR}; /* Dark background for white text */
        }}
        .stTextInput>div>div>input:focus {{
            border-color: {PRIMARY_COLOR};
            box-shadow: 0 0 0 2px rgba(26, 86, 219, 0.15);
        }}
        .stTextInput>div>div>input::placeholder {{
            color: rgba(255, 255, 255, 0.7); /* Light placeholder text for contrast */
        }}
        
        /* Text area styling */
        .stTextArea textarea {{
            border-radius: 12px;
            border: 2px solid #CBD5E1; /* Darker border for better contrast */
            padding: 10px 15px;
            font-size: 16px;
            color: white; /* Text color changed to white */
            background-color: {SECONDARY_COLOR}; /* Dark background for white text */
        }}
        .stTextArea textarea:focus {{
            border-color: {PRIMARY_COLOR};
            box-shadow: 0 0 0 2px rgba(26, 86, 219, 0.15);
        }}
        .stTextArea textarea::placeholder {{
            color: rgba(255, 255, 255, 0.7); /* Light placeholder text for contrast */
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
            border-top: 1px solid #CBD5E1; /* Darker border for better contrast */
            margin-top: 2rem;
        }}
        
        /* Streamlit overrides */
        div.block-container {{
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 1000px;
        }}
        
        /* Text styling */
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
            background-color: rgba(26, 86, 219, 0.1); /* Transparent primary color */
            color: {PRIMARY_COLOR};
        }}
        
        /* Data item styling for formatted reports */
        .data-item {{
            margin-bottom: 1rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #E2E8F0; /* Darker border for better contrast */
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
            background: #F1F5F9;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #94A3B8;
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #64748B;
        }}
        
        /* Ensure radio buttons have good contrast */
        .stRadio > div {{
            margin-bottom: 0.5rem;
        }}
        .stRadio label {{
            color: {TEXT_COLOR} !important;
            font-weight: 500;
        }}
    </style>
    """, unsafe_allow_html=True)

def init_ui():
    """Initialize the UI with a professional look and feel"""
    st.set_page_config(
        page_title="ProjectRisk AI", 
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Add custom CSS
    add_custom_css()
    
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
    """Render a chat message with professional styling and improved readability"""
    timestamp = datetime.now().strftime("%H:%M")
    
    if role == "user":
        st.markdown(f"""
        <div class="user-message">
            <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
                <div style="font-weight: 600; color: {SECONDARY_COLOR}; display: flex; align-items: center;">
                    <span style="display: inline-block; width: 24px; height: 24px; background-color: #E0E7FF; border-radius: 50%; margin-right: 8px; text-align: center; line-height: 24px;">👤</span>
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
            <div style="display: flex; align-items: center; margin-bottom: 0.75rem; border-bottom: 1px solid #F1F5F9; padding-bottom: 0.5rem;">
                <div style="font-weight: 600; color: {PRIMARY_COLOR}; display: flex; align-items: center;">
                    <span style="display: inline-block; width: 24px; height: 24px; background-color: #EEF2FF; border-radius: 50%; margin-right: 8px; text-align: center; line-height: 24px;">🔍</span>
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
        <span>{label}</span>
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
                    list_items.append(f'<li style="margin-bottom: 0.5rem;">{item.strip()}</li>')
            
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
                formatted_paragraphs.append(f'<p style="margin-bottom: 1rem; line-height: 1.6;">{paragraph}</p>')
        else:
            # Regular paragraph
            formatted_paragraphs.append(f'<p style="margin-bottom: 1rem; line-height: 1.6;">{paragraph}</p>')
    
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
                <div style="margin-bottom: 0.75rem; line-height: 1.5;">
                    {line}
                </div>
                """)
    
    # Add conclusion section if it exists
    if conclusion_text:
        html_parts.append(f"""
        <div style="margin-top: 1rem; border-top: 1px solid #e5e7eb; padding-top: 1rem;">
            <div style="font-weight: 600; color: {SECONDARY_COLOR}; margin-bottom: 0.5rem;">Conclusion</div>
            <div style="line-height: 1.5;">{conclusion_text}</div>
        </div>
        """)
    
    # Join all parts and wrap in a container
    result = f"""
    <div style="background-color: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); margin-bottom: 1.5rem;">
        {''.join(html_parts)}
    </div>
    """
    
    return result
