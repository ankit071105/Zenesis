# app.py
import streamlit as st
import google.generativeai as genai
import os
import json
import re
import plotly.graph_objects as go
from PIL import Image
import io
import base64
from dotenv import load_dotenv
import time
import numpy as np
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    st.error("GEMINI_API_KEY not found. Please set it in your environment variables.")
st.set_page_config(
    page_title="Zenesis",
    page_icon="⚒️",
    layout="wide",
    initial_sidebar_state="expanded"
)
SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "JavaScript", "Java", "C++", "C#", "TypeScript", "Go", "Rust", 
        "Swift", "Kotlin", "PHP", "Ruby", "R", "Scala"
    ],
    "Web Development": [
        "HTML/CSS", "React", "Vue.js", "Angular", "Node.js", "Express.js", "Django", 
        "Flask", "Spring Boot", "Ruby on Rails", "ASP.NET", "FastAPI", "Svelte"
    ],
    "Mobile Development": [
        "React Native", "Flutter", "iOS Development", "Android Development", 
        "Ionic", "Xamarin", "Kotlin Multiplatform"
    ],
    "Database Technologies": [
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra", "Elasticsearch",
        "Firebase", "Supabase", "SQLite", "Oracle", "SQL Server"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Terraform", 
        "Jenkins", "GitLab CI/CD", "GitHub Actions", "Ansible", "Nginx", "Apache"
    ],
    "Data Science & ML": [
        "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "Pandas", "NumPy", 
        "Matplotlib", "Seaborn", "OpenCV", "NLTK", "SpaCy", "Hugging Face"
    ],
    "AI & Advanced Topics": [
        "Deep Learning", "Computer Vision", "Natural Language Processing", 
        "Generative AI", "LLMs", "Agentic AI", "Reinforcement Learning",
        "GANs", "Transformers", "LangChain", "LlamaIndex", "AutoML"
    ],
    "Tools & Others": [
        "Git", "Linux", "Bash Scripting", "REST APIs", "GraphQL", "WebSockets",
        "WebRTC", "WebAssembly", "Blockchain", "Web3", "Unity", "Unreal Engine"
    ]
}
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #4FC3F7;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px #4FC3F7, 0 0 20px #4FC3F7;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #29B6F6;
        border-bottom: 2px solid #4FC3F7;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    .project-card {
        background: linear-gradient(135deg, #1A237E, #0D47A1);
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(79, 195, 247, 0.3);
        border: 1px solid #4FC3F7;
        color: white;
    }
    .feature-card {
        background: rgba(25, 118, 210, 0.2);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(79, 195, 247, 0.2);
        border: 1px solid #29B6F6;
        color: #E1F5FE;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0277BD, #01579B);
        color: white;
        border: none;
        padding: 0.7rem 1.5rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(2, 119, 189, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #0288D1, #0277BD);
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(2, 119, 189, 0.4);
    }
    .success-box {
        background: rgba(46, 125, 50, 0.2);
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
        color: #E8F5E9;
    }
    .info-box {
        background: rgba(25, 118, 210, 0.2);
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
        color: #E3F2FD;
    }
    .code-block {
        background: #0D1B2A;
        color: #E0E0E0;
        padding: 1rem;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        overflow-x: auto;
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #1E88E5;
        box-shadow: 0 4px 10px rgba(30, 136, 229, 0.2);
    }
    .flowchart-container {
        background: #0D1B2A;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(79, 195, 247, 0.3);
        margin: 1.5rem 0;
        height: 600px;
        overflow: auto;
        border: 1px solid #4FC3F7;
    }
    .error-box {
        background: rgba(198, 40, 40, 0.2);
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #F44336;
        margin: 1rem 0;
        color: #FFEBEE;
    }
    .gemini-flash-badge {
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 1rem;
    }
    .full-width {
        width: 100%;
    }
    .tab-content {
        padding: 1rem;
    }
    /* Make tabs more visible */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #0D1B2A;
        padding: 0.5rem;
        border-radius: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background: linear-gradient(135deg, #1A237E, #0D47A1);
        border-radius: 6px;
        gap: 8px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: bold;
        color: white;
        border: 1px solid #4FC3F7;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0277BD, #01579B);
        color: white;
        box-shadow: 0 0 10px rgba(79, 195, 247, 0.5);
    }
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0D1B2A, #1B263B);
        color: #E0E0E0;
    }
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #1A237E, #0D47A1);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #1A237E, #0D47A1);
        color: white;
    }
    /* Input fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stMultiselect>div>div>div {
        background: #1B263B;
        color: white;
        border: 1px solid #4FC3F7;
    }
    /* Text color for labels */
    .stTextInput label, .stSelectbox label, .stMultiselect label, .stSlider label {
        color: #4FC3F7 !important;
        font-weight: bold;
    }
    /* Skill category headers */
    .skill-category {
        background: linear-gradient(135deg, #0277BD, #01579B);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-weight: bold;
        border: 1px solid #4FC3F7;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'project_data' not in st.session_state:
    st.session_state.project_data = None
if 'flowchart_generated' not in st.session_state:
    st.session_state.flowchart_generated = False
if 'code_scaffold' not in st.session_state:
    st.session_state.code_scaffold = None
if 'repo_structure' not in st.session_state:
    st.session_state.repo_structure = None
if 'project_generated' not in st.session_state:
    st.session_state.project_generated = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Project Idea"

def extract_json_from_text(text):
    """Try to extract JSON from text response"""
    try:
        # Try to parse the entire text as JSON first
        return json.loads(text)
    except json.JSONDecodeError:
        # If that fails, try to find JSON within the text
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
    return None

def analyze_interests(interests, skills, experience_level):
    """Analyze user interests and skills """
    prompt = f"""
    Analyze the following user profile and suggest suitable project ideas:
    
    Interests: {interests}
    Skills: {skills}
    Experience Level: {experience_level}
    
    Provide a JSON response with:
    1. A summary of the user's profile
    2. 5 project ideas tailored to this profile
    3. For each project idea, include:
       - Title
       - Description
       - Difficulty level
       - Required skills
       - Potential learning outcomes
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error analyzing interests: {str(e)}"

def generate_project_idea(interests, skills, experience_level):
    """Generate a specific project idea"""
    prompt = f"""
    Based on the following profile:
    - Interests: {interests}
    - Skills: {skills}
    - Experience Level: {experience_level}
    
    Generate one specific, unique project idea. Provide the response in JSON format with these fields:
    - title: Project title
    - description: Detailed project description
    - difficulty: Difficulty level (Beginner, Intermediate, Advanced)
    - core_concepts: List of core concepts and technologies needed
    - features: List of main features
    - timeline: Estimated timeline for completion
    - resources: List of helpful learning resources
    
    Make sure your response is valid JSON that can be parsed.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating project idea: {str(e)}"

def generate_flowchart(project_description):
    """Generate a flowchart for the project using Gemini 2.0 Flash"""
    prompt = f"""
    Based on the following project description:
    {project_description}
    
    Create a simple flowchart representation of this project's main workflow.
    Focus on the key steps and processes. Use rectangular boxes for processes and diamonds for decisions.
    Keep it simple with 5-7 main steps.
    
    Provide the response as a list of steps in plain text format, with arrows between them.
    For example: Start -> Process Data -> Make Decision -> End
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating flowchart: {str(e)}"

def create_visual_flowchart(flowchart_description):
    """Create a visual flowchart from the description using Plotly with rectangular boxes"""
    try:
        nodes = []
        edges = []
        lines = flowchart_description.split('\n')
        for line in lines:
            if '->' in line:
                parts = line.split('->')
                for i in range(len(parts) - 1):
                    source = parts[i].strip()
                    target = parts[i + 1].strip()
                    edges.append((source, target))
                    if source not in nodes:
                        nodes.append(source)
                    if target not in nodes:
                        nodes.append(target)
            elif line.strip() and ':' not in line and '->' not in line:
                node = line.strip()
                if node not in nodes:
                    nodes.append(node)
        
        if not nodes:
            nodes = ['Start', 'Process Data', 'Make Decision', 'End']
            edges = [('Start', 'Process Data'), ('Process Data', 'Make Decision'), ('Make Decision', 'End')]
        node_positions = {}
        levels = {}
        for i, node in enumerate(nodes):
            levels[node] = i % 4 
        for node in nodes:
            level = levels[node]
            x = level * 0.25 + 0.1
            y = 0.5 + (nodes.index(node) % 3) * 0.2 - 0.2
            node_positions[node] = (x, y)
        edge_x = []
        edge_y = []
        for edge in edges:
            x0, y0 = node_positions[edge[0]]
            x1, y1 = node_positions[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=3, color='#4FC3F7'),
            hoverinfo='none',
            mode='lines')
        node_x = []
        node_y = []
        node_text = []
        for node in nodes:
            x, y = node_positions[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=node_text,
            textposition="middle center",
            textfont=dict(color='white', size=12),
            marker=dict(
                symbol='square',
                size=100,
                color='#0277BD',
                line=dict(width=3, color='#4FC3F7')
            ))
        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 1]),
                        height=500,
                        width=800,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                        ))
        
        return fig
    except Exception as e:
        st.error(f"Error creating visual flowchart: {str(e)}")
        return None

def generate_code_scaffold(project_title, project_description, skills):
    """Generate code scaffold for the project...."""
    prompt = f"""
    Project Title: {project_title}
    Project Description: {project_description}
    Skills: {skills}
    
    Create a code scaffold for this project. Include:
    1. Recommended project structure (files and folders)
    2. For each main file, provide a code skeleton with:
       - Appropriate imports
       - Class/function definitions with docstrings
       - TODO comments for implementation guidance
    3. Setup instructions (dependencies, environment setup)
    4. Basic configuration files if needed (e.g., .gitignore, requirements.txt)
    
    Format the response clearly with code blocks for each file.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating code scaffold: {str(e)}"

def create_github_repo_structure(project_title, code_scaffold):
    """Create GitHub repository structure based on code scaffold...."""
    prompt = f"""
    Based on the following project title and code scaffold:
    
    Project Title: {project_title}
    Code Scaffold: {code_scaffold}
    
    Create a GitHub repository structure with:
    1. Recommended folder structure
    2. Key files to include
    3. README.md outline with project description, setup instructions, and usage guide
    
    Provide the response in a structured format.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error creating GitHub structure: {str(e)}"

def main():
    st.markdown('<h1 class="main-header">AI Project Idea Generator </h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem; color: #BBDEFB;'>
        <p style='font-size: 1.2rem;'>Struggling to find your next project? This AI tool will analyze your skills and interests to generate unique project ideas with complete code scaffolds and flowcharts.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for user input
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/1688/1688400.png", width=100)
        st.markdown("### 👤 Your Developer Profile")
        
        with st.form("profile_form"):
            interests = st.text_input("Your Interests", placeholder="e.g., AI, Web Development, Games, Mobile Apps")
            
            # Display skills in categorized expanders
            selected_skills = []
            for category, skills in SKILL_CATEGORIES.items():
                with st.expander(f"{category} ({len(skills)} skills)"):
                    category_skills = st.multiselect(
                        f"Select {category} skills",
                        skills,
                        key=f"skills_{category}"
                    )
                    selected_skills.extend(category_skills)
            
            experience_level = st.select_slider(
                "Experience Level",
                options=["Beginner", "Intermediate", "Advanced"]
            )
            
            analyze_submitted = st.form_submit_button("Analyze Profile")
            generate_submitted = st.form_submit_button("Generate Project Idea")
    
    # Handle form submissions
    if analyze_submitted:
        if not interests or not selected_skills:
            st.warning("Please fill in your interests and select at least one skill.")
        else:
            # Profile Analysis Section
            with st.spinner("Analyzing your profile....."):
                analysis = analyze_interests(interests, ", ".join(selected_skills), experience_level)
                
                st.markdown("### 📊 Profile Analysis")
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.write(analysis)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.session_state.analysis_complete = True
    
    if generate_submitted:
        if not interests or not selected_skills:
            st.warning("Please fill in your interests and select at least one skill.")
        else:
            with st.spinner("Generating your custom project idea..."):
                project_idea = generate_project_idea(interests, ", ".join(selected_skills), experience_level)
                project_data = extract_json_from_text(project_idea)
                
                if project_data:
                    st.session_state.project_data = project_data
                    st.session_state.project_generated = True
                    st.success("Project idea generated successfully!")
                else:
                    st.session_state.project_data = {
                        'title': 'Custom Project',
                        'description': project_idea,
                        'difficulty': experience_level
                    }
                    st.session_state.project_generated = True
                    st.success("Project idea generated successfully!")
    if st.session_state.project_generated and st.session_state.project_data:
        project_data = st.session_state.project_data
        tab1, tab2, tab3, tab4 = st.tabs(["💡 Project Idea", "📋 Flowchart", "💻 Code Scaffold", "📁 GitHub Structure"])
        
        with tab1:
            st.markdown("### 💡 Your Custom Project Idea")
            st.markdown('<div class="project-card">', unsafe_allow_html=True)
            
            st.markdown(f"#### {project_data.get('title', 'Project Title')}")
            st.markdown(f"**Description:** {project_data.get('description', '')}")
            st.markdown(f"**Difficulty:** {project_data.get('difficulty', '')}")
            
            st.markdown("**Core Concepts:**")
            core_concepts = project_data.get('core_concepts', [])
            if isinstance(core_concepts, list):
                for concept in core_concepts:
                    st.markdown(f"- {concept}")
            else:
                st.markdown(f"- {core_concepts}")
            
            st.markdown("**Features:**")
            features = project_data.get('features', [])
            if isinstance(features, list):
                for feature in features:
                    st.markdown(f'<div class="feature-card">- {feature}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="feature-card">- {features}</div>', unsafe_allow_html=True)
            
            st.markdown(f"**Timeline:** {project_data.get('timeline', '')}")
            
            st.markdown("**Resources:**")
            resources = project_data.get('resources', [])
            if isinstance(resources, list):
                for resource in resources:
                    st.markdown(f"- {resource}")
            else:
                st.markdown(f"- {resources}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Button to generate flowchart
            if st.button("📋 Generate Flowchart", key="flowchart_btn"):
                st.session_state.current_tab = "Flowchart"
                st.rerun()
        
        with tab2:
            st.markdown("### 📋 Project Flowchart")
            
            if st.button("🔄 Generate Flowchart", key="gen_flowchart_btn"):
                with st.spinner("Creating project flowchart"):
                    project_desc = st.session_state.project_data.get('description', '')
                    if project_desc:
                        flowchart_desc = generate_flowchart(project_desc)
                        st.session_state.flowchart_generated = True
                        st.session_state.flowchart_desc = flowchart_desc
                        st.rerun()
                    else:
                        st.error("No project description available to generate flowchart.")
            
            if st.session_state.get('flowchart_generated', False) and st.session_state.get('flowchart_desc'):
                flowchart_desc = st.session_state.flowchart_desc
                
                st.markdown("#### Flowchart Description")
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.write(flowchart_desc)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Create visual flowchart
                visual_flowchart = create_visual_flowchart(flowchart_desc)
                if visual_flowchart:
                    st.markdown("#### Visual Flowchart")
                    st.markdown('<div class="flowchart-container">', unsafe_allow_html=True)
                    st.plotly_chart(visual_flowchart, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Click the button above to generate a flowchart for your project.")
        
        with tab3:
            st.markdown("### 💻 Code Scaffold")
            
            if st.button("🔄 Generate Code Scaffold", key="gen_code_btn"):
                with st.spinner("Creating code scaffold.."):
                    project_title = st.session_state.project_data.get('title', 'Custom Project')
                    project_desc = st.session_state.project_data.get('description', '')
                    
                    code_scaffold = generate_code_scaffold(project_title, project_desc, ", ".join(selected_skills))
                    st.session_state.code_scaffold = code_scaffold
                    st.rerun()
            
            if st.session_state.code_scaffold:
                st.markdown('<div class="code-block">', unsafe_allow_html=True)
                st.code(st.session_state.code_scaffold, language='python')
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Click the button above to generate a code scaffold for your project.")
        
        with tab4:
            st.markdown("### 📁 GitHub Repository Structure")
            
            if st.button("🔄 Generate GitHub Structure", key="gen_github_btn"):
                if st.session_state.code_scaffold:
                    with st.spinner("Creating GitHub repository structure with Gemini 2.0 Flash..."):
                        project_title = st.session_state.project_data.get('title', 'Custom Project')
                        repo_structure = create_github_repo_structure(project_title, st.session_state.code_scaffold)
                        st.session_state.repo_structure = repo_structure
                        st.rerun()
                else:
                    st.warning("Please generate the code scaffold first.")
            
            if st.session_state.repo_structure:
                st.markdown('<div class="info-box">', unsafe_allow_html=True)
                st.write(st.session_state.repo_structure)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Click the button above to generate a GitHub repository structure for your project.")
    if not st.session_state.project_generated:
        st.markdown("---")
        st.markdown("### How It Works")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #1A237E, #0D47A1); border-radius: 10px; border: 1px solid #4FC3F7; color: white;'>
                <h3>1. Tell Us About Yourself</h3>
                <p>Share your interests, skills, and experience level in the sidebar.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #1A237E, #0D47A1); border-radius: 10px; border: 1px solid #4FC3F7; color: white;'>
                <h3>2. Get Project Ideas</h3>
                <p>Our AI will analyze your profile and suggest tailored project ideas.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #1A237E, #0D47A1); border-radius: 10px; border: 1px solid #4FC3F7; color: white;'>
                <h3>3. Generate Assets</h3>
                <p>Get flowcharts, code scaffolds, and GitHub structures for your project.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 💡 Example Projects")
        
        example_col1, example_col2 = st.columns(2)
        
        with example_col1:
            st.markdown("""
            <div class="project-card">
                <h4>AI-Powered Mobile App</h4>
                <p>A cross-platform mobile app with AI features using React Native and TensorFlow Lite.</p>
                <p><strong>Skills:</strong> React Native, JavaScript, TensorFlow Lite, Firebase</p>
                <p><strong>Level:</strong> Intermediate</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="project-card">
                <h4>Generative AI Content Creator</h4>
                <p>A web app that generates creative content using LLMs and LangChain.</p>
                <p><strong>Skills:</strong> Python, FastAPI, LangChain, React, OpenAI API</p>
                <p><strong>Level:</strong> Advanced</p>
            </div>
            """, unsafe_allow_html=True)
        
        with example_col2:
            st.markdown("""
            <div class="project-card">
                <h4>Agentic AI Assistant</h4>
                <p>An AI assistant that can perform tasks autonomously using agentic AI principles.</p>
                <p><strong>Skills:</strong> Python, LangChain, AutoGPT, API Integration</p>
                <p><strong>Level:</strong> Advanced</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="project-card">
                <h4>Computer Vision Web Service</h4>
                <p>A web service that processes images using computer vision algorithms.</p>
                <p><strong>Skills:</strong> Python, Flask, OpenCV, TensorFlow, Docker</p>
                <p><strong>Level:</strong> Intermediate</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()