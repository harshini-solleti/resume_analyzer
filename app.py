import streamlit as st
import pypdf
import re
import plotly.graph_objects as go
from io import BytesIO

# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for an elegant, corporate HR tech aesthetic
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; font-family: 'Inter', sans-serif; }
        div[data-testid="stMetricSimpleValue"] { font-size: 2rem !important; font-weight: 700 !important; color: #1E3A8A !important; }
        .report-card {
            background-color: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            margin-bottom: 20px;
            border-left: 5px solid #2563EB;
        }
        .success-card { border-left-color: #10B981; }
        .warning-card { border-left-color: #F59E0B; }
        .danger-card { border-left-color: #EF4444; }
        h1, h2, h3 { color: #0F172A; font-weight: 700; }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CORE UTILITY & PARSING FUNCTIONS
# ==========================================
def extract_text_from_pdf(uploaded_file):
    """Extracts raw text content from an uploaded PDF file."""
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        st.error(f"Error parsing PDF: {str(e)}")
        return None

def analyze_resume(text):
    """Analyzes the extracted text to find sections, skills, and compute scores."""
    analysis = {
        "word_count": len(text.split()),
        "sections_found": [],
        "sections_missing": [],
        "skills_found": [],
        "score": 0,
        "verdict": "",
        "suggestions": []
    }
    
    # Define target sections with regex patterns
    sections = {
        "Contact Information": r"(email|phone|contact|linkedin|github|address)",
        "Education": r"(education|academic|university|college|degree|school)",
        "Skills": r"(skills|technologies|proficiencies|expertise|technical)",
        "Projects": r"(projects|academic projects|personal projects)",
        "Experience": r"(experience|work history|employment|professional experience|internship)",
        "Certifications": r"(certifications|certificates|courses|achievements)",
        "Achievements": r"(achievements|awards|honors|accomplishments)"
    }
    
    # 1. Section Detection
    text_lower = text.lower()
    for section, pattern in sections.items():
        if re.search(pattern, text_lower):
            analysis["sections_found"].append(section)
        else:
            analysis["sections_missing"].append(section)
            
    # 2. HEAVILY EXPANDED SKILL DETECTION INDEX
    common_skills = [
        # Languages
        "python", "javascript", "java", "c++", "c programming", "c#", "ruby", "golang", "swift", "kotlin", "typescript", "r programming", "php", "sql", "html", "css",
        # Frameworks & Libraries
        "react", "angular", "vue", "node.js", "django", "flask", "streamlit", "spring boot", "express", "laravel", "fastapi", "jquery", "bootstrap", "tailwind",
        # Data Science & AI
        "machine learning", "deep learning", "data analysis", "data science", "nlp", "computer vision", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "opencv", "textblob",
        # Databases & Big Data
        "mysql", "postgresql", "mongodb", "sqlite", "redis", "oracle", "firebase", "hadoop", "spark", "hive", "data ops", "data structures",
        # Cloud & DevOps
        "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "gitlab", "ci/cd", "jenkins", "terraform", "ansible", "linux",
        # UI/UX & Tools
        "figma", "canva", "adobe xd", "tableau", "power bi", "excel", "jira", "postman",
        # Methodologies & Management
        "agile", "scrum", "project management", "sdlc", "object oriented programming", "oop"
    ]
    
    for skill in common_skills:
        # Escaping and matching word patterns safely
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            analysis["skills_found"].append(skill.title())

    # 3. Dynamic Scoring Engine
    section_score = (len(analysis["sections_found"]) / len(sections)) * 40
    skill_score = min(len(analysis["skills_found"]) * 3, 30)
    
    word_count = analysis["word_count"]
    if 150 <= word_count <= 800: # Broadened limits to adapt to student resumes
        word_count_score = 30
    elif 800 < word_count <= 1200:
        word_count_score = 20
    else:
        word_count_score = 10
        
    analysis["score"] = int(section_score + skill_score + word_count_score)
    
    # 4. Benchmarking Verdict
    if analysis["score"] >= 80:
        analysis["verdict"] = "Excellent"
    elif analysis["score"] >= 55:
        analysis["verdict"] = "Good"
    else:
        analysis["verdict"] = "Needs Improvement"
        
    # Generate tailored suggestions
    if analysis["sections_missing"]:
        analysis["suggestions"].append(f"📌 **Missing Key Sections:** Consider adding: {', '.join(analysis['sections_missing'])}.")
    if len(analysis["skills_found"]) < 5:
        analysis["suggestions"].append("💡 **Expand Skills Inventory:** List more hard skills or technical proficiencies relevant to your target role.")
    if word_count < 150:
        analysis["suggestions"].append("📝 **Expand Content:** Your resume is concise. Elaborate more on your project bullet points using metrics or results.")
    elif word_count > 800:
        analysis["suggestions"].append("✂️ **Trim Content:** Your resume is slightly verbose. Keep it tight and ideally limited to 1 page.")
        
    if not analysis["suggestions"]:
        analysis["suggestions"].append("🚀 **Outstanding Job!** Your resume structure matches institutional benchmarks.")

    return analysis

def generate_gauge_chart(score):
    colors = {"Excellent": "#10B981", "Good": "#F59E0B", "Needs Improvement": "#EF4444"}
    current_color = colors["Excellent"] if score >= 80 else colors["Good"] if score >= 55 else colors["Needs Improvement"]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "ATS Compatibility Score", 'font': {'size': 18, 'color': '#475569'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
            'bar': {'color': current_color},
            'bgcolor': "#f1f5f9",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 55], 'color': 'rgba(239, 68, 68, 0.08)'},
                {'range': [55, 80], 'color': 'rgba(245, 158, 11, 0.08)'},
                {'range': [80, 100], 'color': 'rgba(16, 185, 129, 0.08)'}
            ],
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def generate_report_text(analysis):
    report = f"""========================================
RESUME ANALYTICS REPORT
========================================
Overall Score: {analysis['score']}/100
Verdict: {analysis['verdict']}
Total Word Count: {analysis['word_count']}

IDENTIFIED SECTIONS:
{', '.join(analysis['sections_found']) if analysis['sections_found'] else 'None'}

MISSING SECTIONS:
{', '.join(analysis['sections_missing']) if analysis['sections_missing'] else 'None'}

IDENTIFIED KEY SKILLS:
{', '.join(analysis['skills_found']) if analysis['skills_found'] else 'None'}

STRATEGIC IMPROVEMENT SUGGESTIONS:
"""
    for sug in analysis['suggestions']:
        clean_sug = sug.replace("**", "").replace("📌 ", "").replace("💡 ", "").replace("📝 ", "").replace("✂ ", "").replace("🚀 ", "")
        report += f"- {clean_sug}\n"
    return report

# ==========================================
# 3. USER INTERFACE LAYOUT
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#2563EB;'>Resume Analyzer</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Platform Standards")
    st.caption("✔️ Parsing compliance checklist based on standard Recruiter filters.")
    st.caption("✔️ Extraction mapped directly through standard Python data schema structures.")

st.title("💼 AI-Powered Resume Scoring Engine")
st.markdown("Evaluate structural compliance, scan core technical proficiencies, and optimize your application parameters instantly.")
st.markdown("---")

uploaded_file = st.file_uploader("Upload your resume (PDF format only)", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Initializing Deep Parsing Pipelines..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        
        if resume_text:
            analysis = analyze_resume(resume_text)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### System Diagnostics Dashboard")
                card_class = "success-card" if analysis["score"] >= 80 else "warning-card" if analysis["score"] >= 55 else "danger-card"
                st.markdown(f"""
                    <div class="report-card {card_class}">
                        <h4>System Verdict: <span style="text-decoration: underline;">{analysis['verdict']}</span></h4>
                        <p>Your resume has undergone comprehensive programmatic evaluation matching corporate screening protocols.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.metric(label="Calculated Length (Words)", value=analysis["word_count"])
                with m_col2:
                    st.metric(label="Identified Key Core Sections", value=f"{len(analysis['sections_found'])} / 7")
                    
                st.markdown("### Detected Technical Focus Skills")
                if analysis["skills_found"]:
                    skills_html = "".join([f"<span style='background-color:#E0F2FE; color:#0369A1; padding: 6px 12px; margin: 4px; border-radius: 20px; display: inline-block; font-size: 14px; font-weight: 500;'>{skill}</span>" for skill in analysis["skills_found"]])
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.warning("No standard technical focus keywords identified.")
                    
            with col2:
                st.plotly_chart(generate_gauge_chart(analysis["score"]), use_container_width=True)
                
                st.markdown("### Section Parsing Matrix")
                sec_col1, sec_col2 = st.columns(2)
                with sec_col1:
                    st.markdown("**Found ✅**")
                    for sect in analysis["sections_found"]:
                        st.caption(f"🍏 {sect}")
                with sec_col2:
                    st.markdown("**Missing / Obscured ❌**")
                    if analysis["sections_missing"]:
                        for sect in analysis["sections_missing"]:
                            st.caption(f"🍎 {sect}")
                    else:
                        st.caption("None! Perfect structural alignment.")
            
            st.markdown("---")
            st.markdown("### Actionable Enhancement Roadmaps")
            for suggestion in analysis["suggestions"]:
                st.markdown(suggestion)
            
            st.markdown("---")
            b_col1, b_col2 = st.columns([1, 1])
            with b_col1:
                st.markdown("### Export Operations")
                st.download_button(
                    label="📥 Download System Analytics Report",
                    data=generate_report_text(analysis),
                    file_name="Resume_Analysis_Report.txt",
                    mime="text/plain"
                )
            with b_col2:
                with st.expander("🔍 View Raw Parsed Text Payload Stream"):
                    st.text_area("Extracted Stream Logs Data", value=resume_text, height=250, disabled=True)
        else:
            st.error("The selected file contains unreadable content.")
else:
    st.markdown("---")
    st.info("💡 **Awaiting Input Data:** Please drag and drop or select your targeted resume file in the system upload dashboard above to trigger analytics processing modules.")
    