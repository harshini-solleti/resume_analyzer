import streamlit as st
import pypdf
import re
import plotly.graph_objects as go
import openai  # Used for OpenAI (Ollama uses native package now)
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
            background-color: #ffffff !important;
            color: #1e293b !important;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            margin-bottom: 20px;
            border-left: 5px solid #2563EB;
        }
        .report-card h1, .report-card h2, .report-card h3, .report-card h4 {
            color: #0f172a !important; 
            font-weight: 700;
            margin-top: 0;
        }
        .report-card p {
            color: #334155 !important;
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
# 2. LOCALIZATION (l10n) DICTIONARY ENGINE
# ==========================================
LANGUAGES = {
    "English": {
        "nav_title": "Resume Analyzer",
        "ai_config_header": "🤖 Advanced AI Configuration",
        "ai_engine_label": "AI Execution Engine",
        "endpoint_label": "Local Network Endpoint Connection",
        "model_label": "Active Engine Identifier Tag",
        "pk_label": "Personal Access Key",
        "model_target_label": "Model Matrix Target",
        "platform_standards": "Platform Standards",
        "compliance_check": "✔️ Parsing compliance checklist based on standard Recruiter filters.",
        "schema_check": "✔️ Extraction mapped directly through standard Python data schema structures.",
        "main_title": "💼 AI-Powered Resume Scoring Engine",
        "main_subtitle": "Evaluate structural compliance, scan core technical proficiencies, and optimize your application parameters instantly.",
        "uploader_label": "Upload your resume (PDF format only)",
        "spinner_parsing": "Initializing Deep Parsing Pipelines...",
        "dashboard_title": "### System Diagnostics Dashboard",
        "verdict_title": "System Verdict",
        "verdict_desc": "Your resume has undergone comprehensive programmatic evaluation matching corporate screening protocols.",
        "metric_length": "Calculated Length (Words)",
        "metric_sections": "Identified Key Core Sections",
        "tech_skills_title": "### Detected Technical Focus Skills",
        "no_skills_warn": "No standard technical focus keywords identified.",
        "chart_title": "ATS Compatibility Score",
        "matrix_title": "### Section Parsing Matrix",
        "found_label": "**Found ✅**",
        "missing_label": "**Missing / Obscured ❌**",
        "perfect_alignment": "None! Perfect structural alignment.",
        "roadmap_title": "### Actionable Enhancement Roadmaps",
        "ai_opt_title": "### 🧠 AI Generative Content Optimization",
        "ai_opt_desc": "Leave heavy contextual breakdown to your connected interface node.",
        "ai_button": "✨ Generate Advanced AI Diagnostic Insight",
        "ai_spinner": "Routing payloads directly via active clusters... Please hold.",
        "ai_success_msg": "Analysis successfully structured using model identifier:",
        "export_title": "### Export Operations",
        "download_button_label": "📥 Download System Analytics Report",
        "raw_stream_title": "🔍 View Raw Parsed Text Payload Stream",
        "raw_stream_label": "Extracted Stream Logs Data",
        "unreadable_error": "The selected file contains unreadable content.",
        "awaiting_input": "💡 **Awaiting Input Data:** Please upload your targeted resume file above to trigger analytics processing modules.",
        "missing_sec_sug": "📌 **Missing Key Sections:** Consider adding: ",
        "expand_skills_sug": "💡 **Expand Skills Inventory:** List more hard skills or technical proficiencies relevant to your target role.",
        "expand_content_sug": "📝 **Expand Content:** Your resume is concise. Elaborate more on your project bullet points using metrics or results.",
        "trim_content_sug": "✂️ **Trim Content:** Your resume is slightly verbose. Keep it tight and ideally limited to 1 page.",
        "outstanding_sug": "🚀 **Outstanding Job!** Your resume structure matches institutional benchmarks.",
        "no_ai_report": "No generative AI report extracted.",
        "system_prompt": "You are a professional ATS coach specializing in corporate human resource compliance parsing workflows."
    },
    "Hindi (हिन्दी)": {
        "nav_title": "रेज़्यूमे विश्लेषक",
        "ai_config_header": "🤖 उन्नत एआई कॉन्फ़िगरेशन",
        "ai_engine_label": "एआई निष्पादन इंजन",
        "endpoint_label": "स्थानीय नेटवर्क एंडपॉइंट कनेक्शन",
        "model_label": "सक्रिय इंजन पहचानकर्ता टैग",
        "pk_label": "व्यक्तिगत एक्सेस कुंजी",
        "model_target_label": "मॉडल मैट्रिक्स लक्ष्य",
        "platform_standards": "मंच मानक",
        "compliance_check": "✔️ मानक रिक्रूटर फिल्टर के आधार पर पार्सिंग अनुपालन चेकलिस्ट।",
        "schema_check": "✔️ निष्कर्षण सीधे मानक पायथन डेटा स्कीमा संरचनाओं के माध्यम से मैप किया गया।",
        "main_title": "💼 एआई-पावर्ड रेज़्यूमे स्कोरिंग इंजन",
        "main_subtitle": "संरचनात्मक अनुपालन का मूल्यांकन करें, मुख्य तकनीकी दक्षताओं को स्कैन करें, और अपने एप्लिकेशन मापदंडों को तुरंत अनुकूलित करें।",
        "uploader_label": "अपना रेज़्यूमे अपलोड करें (केवल पीडीएफ प्रारूप)",
        "spinner_parsing": "गहन पार्सिंग पाइपलाइन प्रारंभ की जा रही है...",
        "dashboard_title": "### सिस्टम निदान डैशबोर्ड",
        "verdict_title": "सिस्टम का निर्णय",
        "verdict_desc": "आपका रेज़्यूमे कॉर्पोरेट स्क्रीनिंग प्रोटोकॉल से मेल खाने वाले व्यापक प्रोग्रामेटिक मूल्यांकन से गुजरा है।",
        "metric_length": "परिकलित लंबाई (शब्द)",
        "metric_sections": "पहचाने गए मुख्य खंड",
        "tech_skills_title": "### पाए गए तकनीकी कौशल",
        "no_skills_warn": "कोई मानक तकनीकी कौशल कीवर्ड नहीं मिला।",
        "chart_title": "एटीएस संगतता स्कोर",
        "matrix_title": "### अनुभाग पार्सिंग मैट्रिक्स",
        "found_label": "**प्राप्त खंड ✅**",
        "missing_label": "**लापता / अस्पष्ट खंड ❌**",
        "perfect_alignment": "कोई नहीं! उत्तम संरचनात्मक संरेखण।",
        "roadmap_title": "### व्यावहारिक संवर्द्धन रोडमैप",
        "ai_opt_title": "### 🧠 एआई जनरेटिव सामग्री अनुकूलन",
        "ai_opt_desc": "गहन संदर्भ विश्लेषण को अपने जुड़े हुए इंटरफ़ेस नोड पर छोड़ दें।",
        "ai_button": "✨ उन्नत एआई नैदानिक ​​अंतर्दृष्टि उत्पन्न करें",
        "ai_spinner": "सक्रिय समूहों के माध्यम से सीधे पेलोड रूट किया जा रहा है... कृपया प्रतीक्षा करें।",
        "ai_success_msg": "मॉडल पहचानकर्ता का उपयोग करके विश्लेषण सफलतापूर्वक संरचित किया गया:",
        "export_title": "### निर्यात संचालन",
        "download_button_label": "📥 सिस्टम एनालिटिक्स रिपोर्ट डाउनलोड करें",
        "raw_stream_title": "🔍 रॉ पार्स किए गए टेक्स्ट पेलोड स्ट्रीम देखें",
        "raw_stream_label": "निकाला गया स्ट्रीम लॉग डेटा",
        "unreadable_error": "चयनित फ़ाइल में अपठनीय सामग्री है।",
        "awaiting_input": "💡 **इनपुट डेटा की प्रतीक्षा है:** विश्लेषण प्रक्रिया को ट्रिगर करने के लिए कृपया ऊपर अपनी लक्षित रेज़्यूमे फ़ाइल अपलोड करें।",
        "missing_sec_sug": "📌 **लापता मुख्य अनुभाग:** इन्हें जोड़ने पर विचार करें: ",
        "expand_skills_sug": "💡 **कौशल सूची का विस्तार करें:** अपने लक्षित पद के लिए प्रासंगिक अधिक कठिन कौशल या तकनीकी दक्षताओं को सूचीबद्ध करें।",
        "expand_content_sug": "📝 **सामग्री का विस्तार करें:** आपकी रेज़्यूमे बहुत संक्षिप्त है। मेट्रिक्स या परिणामों का उपयोग करके अपने प्रोजेक्ट बिंदुओं को और विस्तार से समझाएं।",
        "trim_content_sug": "✂️ **सामग्री कम करें:** आपका रेज़्यूमे थोड़ा लंबा है। इसे संक्षिप्त रखें और आदर्श रूप से 1 पृष्ठ तक सीमित करें।",
        "outstanding_sug": "🚀 **उत्कृष्ट कार्य!** आपकी रेज़्यूमे संरचना संस्थागत बेंचमार्क से मेल खाती है।",
        "no_ai_report": "कोई जनरेटिव एआई रिपोर्ट नहीं निकाली गई।",
        "system_prompt": "आप एक पेशेवर एटीएस कोच हैं जो कॉर्पोरेट मानव संसाधन अनुपालन पार्सिंग वर्कफ़्लो में विशेषज्ञता रखते हैं।"
    },
    "Telugu (తెలుగు)": {
        "nav_title": "రెజ్యూమే అనలైజర్",
        "ai_config_header": "🤖 అడ్వాన్స్డ్ AI కాన్ఫిగరేషన్",
        "ai_engine_label": "AI ఎగ్జిక్యూషన్ ఇంజిన్",
        "endpoint_label": "లోకల్ నెట్‌వర్క్ ఎండ్‌పాయింట్ కనెక్షన్",
        "model_label": "యాక్టివ్ ఇంజిన్ ఐడెంటిఫైయర్ ట్యాగ్",
        "pk_label": "వ్యక్తిగత యాక్సెస్ కీ",
        "model_target_label": "మోడల్ మ్యాట్రిక్స్ టార్గెట్",
        "platform_standards": "ప్లాట్‌ఫారమ్ ప్రమాణాలు",
        "compliance_check": "✔️ ప్రామాణిక రిక్రూటర్ ఫిల్టర్‌ల ఆధారంగా పార్సింగ్ నిబంధనల చెక్‌లిస్ట్.",
        "schema_check": "✔️ ఎక్స్‌ట్రాక్షన్ నేరుగా స్టాండర్డ్ పైథాన్ డేటా స్కీమా స్ట్రక్చర్స్ ద్వారా మ్యాప్ చేయబడింది.",
        "main_title": "💼 AI- పవర్డ్ రెజ్యూమే స్కోరింగ్ ఇంజిన్",
        "main_subtitle": "నిర్మాణాత్మక అనుకూలతను అంచనా వేయండి, కోర్ సాంకేతిక నైపుణ్యాలను స్కాన్ చేయండి మరియు మీ అప్లికేషన్ పారామితులను తక్షణమే ఆప్టిమైజ్ చేయండి.",
        "uploader_label": "మీ రెజ్యూమేని అప్‌లోడ్ చేయండి (PDF ఫార్మాట్ మాత్రమే)",
        "spinner_parsing": "డీప్ పార్సింగ్ పైప్‌లైన్‌లను ప్రారంభిస్తోంది...",
        "dashboard_title": "### సిస్టమ్ డయాగ్నోస్టిక్స్ డ్యాష్‌బోర్డ్",
        "verdict_title": "సిస్టమ్ తీర్పు",
        "verdict_desc": "మీ రెజ్యూమే కార్పొరేట్ స్క్రీనింగ్ ప్రోటోకాల్‌లకు సరిపోయేలా సమగ్రమైన ప్రోగ్రామాటిక్ మూల్యాంకనానికి గురైంది.",
        "metric_length": "లెక్కించబడిన పొడవు (పదాలు)",
        "metric_sections": "గుర్తించబడిన ముఖ్య విభాగాలు",
        "tech_skills_title": "### గుర్తించబడిన సాంకేతిక నైపుణ్యాలు",
        "no_skills_warn": "ఎటువంటి ప్రామాణిక సాంకేతిక నైపుణ్యాలు కనుగొనబడలేదు.",
        "chart_title": "ATS అనుకూలత స్కోర్",
        "matrix_title": "### సెక్షన్ పార్సింగ్ మ్యాట్రిక్స్",
        "found_label": "**కనుగొనబడినవి ✅**",
        "missing_label": "**తప్పిపోయినవి / స్పష్టంగా లేనివి ❌**",
        "perfect_alignment": "ఏమీ లేవు! పరిపూర్ణ నిర్మాణ అమరిక.",
        "roadmap_title": "### ఆచరణాత్మక మెరుగుదల రోడ్‌మ్యాప్‌లు",
        "ai_opt_title": "### 🧠 AI జెనరేటివ్ కంటెంట్ ఆప్టిమైజేషన్",
        "ai_opt_desc": "భారీ సందర్భోచిత విశ్లేషణను మీ కనెక్ట్ చేయబడిన ఇంటర్‌ఫేస్ నోడ్‌కు వదిలివేయండి.",
        "ai_button": "✨ అడ్వాన్స్డ్ AI డయాగ్నోస్టిక్ అంతర్దృష్టిని సృష్టించండి",
        "ai_spinner": "యాక్టివ్ క్లస్టర్‌ల ద్వారా పేలోడ్‌లను నేరుగా రూట్ చేస్తోంది... దయచేసి వేచి ఉండండి.",
        "ai_success_msg": "మోడల్ ఐడెంటిఫైయర్‌ని ఉపయోగించి విశ్లేషణ విజయవంతంగా రూపొందించబడింది:",
        "export_title": "### ఎగుమతి కార్యకలాపాలు",
        "download_button_label": "📥 సిస్టమ్ అనలిటిక్స్ రిపోర్ట్‌ను డౌన్‌లోడ్ చేయండి",
        "raw_stream_title": "🔍 రా పార్స్డ్ టెక్స్ట్ పేలోడ్ స్ట్రీమ్‌ను వీక్షించండి",
        "raw_stream_label": "సేకరించిన స్ట్రీమ్ లాగ్స్ డేటా",
        "unreadable_error": "ఎంచుకున్న ఫైల్‌లో చదవలేని కంటెంట్ ఉంది.",
        "awaiting_input": "💡 **ఇన్‌పుట్ డేటా కోసం నిరీక్షణ:** విశ్లేషణ ప్రక్రియను ప్రారంభించడానికి దయచేసి పైన మీ టార్గెటెడ్ రెజ్యూమే ఫైల్‌ను అప్‌లోడ్ చేయండి.",
        "missing_sec_sug": "📌 **తప్పిపోయిన ముఖ్య విభాగాలు:** వీటిని జోడించడాన్ని పరిశీలించండి: ",
        "expand_skills_sug": "💡 **నైపుణ్యాల జాబితాను విస్తరించండి:** మీ టార్గెట్ ఉద్యోగానికి సంబంధించిన మరిన్ని కఠినమైన నైపుణ్యాలు లేదా సాంకేతిక సామర్థ్యాలను జాబితా చేయండి.",
        "expand_content_sug": "📝 **కంటెంట్‌ను విస్తరించండి:** మీ రెజ్యూమే చాలా క్లుప్తంగా ఉంది. మెట్రిక్స్ లేదా ఫలితాలను ఉపయోగించి మీ ప్రాజెక్ట్ పాయింట్లను మరింత వివరంగా వివరించండి.",
        "trim_content_sug": "✂️ **కంటెంట్‌ను తగ్గించండి:** మీ రెజ్యూమే కొంచెం సుదీర్ఘంగా ఉంది. దీన్ని సంక్షిప్తంగా ఉంచండి మరియు ఆదర్శంగా 1 పేజీకి పరిమితం చేయండి.",
        "outstanding_sug": "🚀 **అద్భుతమైన పని!** మీ రెజ్యూమే నిర్మాణం... సంస్థాగత ప్రమాణాలకు సరిపోలింది.",
        "no_ai_report": "జెనరేటివ్ AI రిపోర్ట్ ఏదీ సేకరించబడలేదు.",
        "system_prompt": "మీరు కార్పొరేట్ మానవ వనరుల నిబంధనల పార్సింగ్ వర్క్‌ఫ్లోలలో నైపుణ్యం కలిగిన ప్రొఫెషనల్ ATS కోచ్."
    }
}

# ==========================================
# 3. CORE UTILITY & PARSING FUNCTIONS
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

def analyze_resume(text, lang_dict):
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
    
    sections = {
        "Contact Information": r"(email|phone|contact|linkedin|github|address)",
        "Education": r"(education|academic|university|college|degree|school)",
        "Skills": r"(skills|technologies|proficiencies|expertise|technical)",
        "Projects": r"(projects|academic projects|personal projects)",
        "Experience": r"(experience|work history|employment|professional experience|internship)",
        "Certifications": r"(certifications|certificates|courses|achievements)",
        "Achievements": r"(achievements|awards|honors|accomplishments)"
    }
    
    text_lower = text.lower()
    for section, pattern in sections.items():
        if re.search(pattern, text_lower):
            analysis["sections_found"].append(section)
        else:
            analysis["sections_missing"].append(section)
            
    common_skills = [
        "python", "javascript", "java", "c++", "c programming", "c#", "ruby", "golang", "swift", "kotlin", "typescript", "r programming", "php", "sql", "html", "css",
        "react", "angular", "vue", "node.js", "django", "flask", "streamlit", "spring boot", "express", "laravel", "fastapi", "jquery", "bootstrap", "tailwind",
        "machine learning", "deep learning", "data analysis", "data science", "nlp", "computer vision", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "opencv", "textblob",
        "mysql", "postgresql", "mongodb", "sqlite", "redis", "oracle", "firebase", "hadoop", "spark", "hive", "data ops", "data structures",
        "aws", "azure", "gcp", "docker", "kubernetes", "git", "github", "gitlab", "ci/cd", "jenkins", "terraform", "ansible", "linux",
        "figma", "canva", "adobe xd", "tableau", "power bi", "excel", "jira", "postman",
        "agile", "scrum", "project management", "sdlc", "object oriented programming", "oop"
    ]
    
    for skill in common_skills:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            analysis["skills_found"].append(skill.title())

    section_score = (len(analysis["sections_found"]) / len(sections)) * 40
    skill_score = min(len(analysis["skills_found"]) * 3, 30)
    
    word_count = analysis["word_count"]
    if 150 <= word_count <= 800:
        word_count_score = 30
    elif 800 < word_count <= 1200:
        word_count_score = 20
    else:
        word_count_score = 10
        
    analysis["score"] = int(section_score + skill_score + word_count_score)
    
    if analysis["score"] >= 80:
        analysis["verdict"] = "Excellent"
    elif analysis["score"] >= 55:
        analysis["verdict"] = "Good"
    else:
        analysis["verdict"] = "Needs Improvement"
        
    if analysis["sections_missing"]:
        analysis["suggestions"].append(f"{lang_dict['missing_sec_sug']}{', '.join(analysis['sections_missing'])}.")
    if len(analysis["skills_found"]) < 5:
        analysis["suggestions"].append(lang_dict["expand_skills_sug"])
    if word_count < 150:
        analysis["suggestions"].append(lang_dict["expand_content_sug"])
    elif word_count > 800:
        analysis["suggestions"].append(lang_dict["trim_content_sug"])
        
    if not analysis["suggestions"]:
        analysis["suggestions"].append(lang_dict["outstanding_sug"])

    return analysis

def generate_gauge_chart(score, title_text):
    colors = {"Excellent": "#10B981", "Good": "#F59E0B", "Needs Improvement": "#EF4444"}
    current_color = colors["Excellent"] if score >= 80 else colors["Good"] if score >= 55 else colors["Needs Improvement"]
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title_text, 'font': {'size': 18, 'color': '#475569'}},
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

def generate_report_text(analysis, ai_feedback="", lang_dict=None):
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
        
    if ai_feedback:
        report += f"\n========================================\nAI EXTENDED GENERATIVE ANALYSIS\n========================================\n{ai_feedback}\n"
        
    return report

# ==========================================
# 4. AI INFERENCE LOGIC (Direct Native Ollama & BYOK)
# ==========================================
def generate_ai_analysis(resume_text, diagnostic_summary, lang_dict, ai_provider, selected_model, base_url, api_key):
    if ai_provider != "Local Ollama" and not api_key:
        st.error("❌ Action Required: Provide an API Token in the sidebar panel.")
        return None

    prompt_payload = (
        "You are an advanced executive tech recruiter and Senior ATS optimization analyst. "
        "Analyze the following candidate profile.\n\n"
        f"SYSTEM DIAGNOSTIC SCORE MAPPED BY APPLICATION:\n- Score: {diagnostic_summary['score']}/100\n"
        f"- Missing Core Sub-structures: {', '.join(diagnostic_summary['sections_missing']) if diagnostic_summary['sections_missing'] else 'None'}\n\n"
        f"RAW RESUME STRUCTURAL TEXT:\n\"\"\"{resume_text}\"\"\"\n\n"
        "TASK:\nGenerate highly targeted, actionable recommendations. Breakdown feedback into:\n"
        "1. Critical Impact Fixes (Verb patterns, formatting errors, metric absence).\n"
        "2. Missing Industry Context Keywords or High-Value Skill targets.\n"
        "3. An executive optimization rewrite blueprint.\n\n"
        "CRITICAL REQUIREMENT FOR LOCALIZATION:\nPlease provide your entire output response in the same language context requested by the user interface translation parameters."
    )

    try:
        if ai_provider == "Local Ollama":
            import ollama
            # Direct, native runtime execution bypassing HTTP translation layers
            response = ollama.chat(
                model=selected_model,
                messages=[
                    {"role": "system", "content": lang_dict["system_prompt"]},
                    {"role": "user", "content": prompt_payload}
                ],
                options={"temperature": 0.4}
            )
            return response['message']['content']
            
        elif "OpenAI" in ai_provider:
            client = openai.OpenAI(api_key=api_key, base_url=base_url)
            response = client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": lang_dict["system_prompt"]},
                    {"role": "user", "content": prompt_payload}
                ],
                temperature=0.4
            )
            return response.choices[0].message.content
            
        elif "Anthropic" in ai_provider:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model=selected_model,
                max_tokens=2000,
                temperature=0.4,
                system=lang_dict["system_prompt"],
                messages=[{"role": "user", "content": prompt_payload}]
            )
            return message.content[0].text
            
    except Exception as e:
        st.error(f"❌ Core AI Pipeline Infrastructure Error. Details: {e}")
        return None

# ==========================================
# 5. USER INTERFACE LAYOUT & SIDEBAR
# ==========================================
with st.sidebar:
    selected_lang = st.selectbox(
        "🌐 Language / भाषा / భాష",
        ["English", "Hindi (हिन्दी)", "Telugu (తెలుగు)"]
    )
    t = LANGUAGES[selected_lang]
    
    st.markdown(f"<h2 style='color:#2563EB;'>{t['nav_title']}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown(f"### {t['ai_config_header']}")
    ai_provider = st.selectbox(
        t['ai_engine_label'], 
        ["Local Ollama", "OpenAI (BYOK)", "Anthropic Claude (BYOK)"]
    )

    api_key = None
    base_url = None
    selected_model = ""

    if ai_provider == "Local Ollama":
        base_url = st.text_input(t['endpoint_label'], value="http://localhost:11434/v1")
        selected_model = st.text_input(t['model_label'], value="llama3.2")
        api_key = "local-runtime"

    elif ai_provider == "OpenAI (BYOK)":
        api_key = st.text_input(t['pk_label'], type="password", placeholder="sk-...")
        selected_model = st.selectbox(t['model_target_label'], ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"])
        base_url = "https://api.openai.com/v1"

    elif ai_provider == "Anthropic Claude (BYOK)":
        api_key = st.text_input(t['pk_label'], type="password", placeholder="sk-ant-...")
        selected_model = st.selectbox(t['model_target_label'], ["claude-3-5-sonnet-latest", "claude-3-opus-latest"])

    st.markdown("---")
    st.markdown(f"### {t['platform_standards']}")
    st.caption(t['compliance_check'])
    st.caption(t['schema_check'])

st.title(t['main_title'])
st.markdown(t['main_subtitle'])
st.markdown("---")

uploaded_file = st.file_uploader(t['uploader_label'], type=["pdf"])

if uploaded_file is not None:
    with st.spinner(t['spinner_parsing']):
        resume_text = extract_text_from_pdf(uploaded_file)
        
        if resume_text:
            analysis = analyze_resume(resume_text, t)
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown(t['dashboard_title'])
                card_class = "success-card" if analysis["score"] >= 80 else "warning-card" if analysis["score"] >= 55 else "danger-card"
                
                display_verdict = analysis["verdict"]
                if selected_lang == "Hindi (हिन्दी)":
                    display_verdict = "उत्कृष्ट" if analysis["score"] >= 80 else "अच्छा" if analysis["score"] >= 55 else "सुधार की आवश्यकता है"
                elif selected_lang == "Telugu (తెలుగు)":
                    display_verdict = "అద్భుతమైనది" if analysis["score"] >= 80 else "మంచిది" if analysis["score"] >= 55 else "మెరుగుదల అవసరం"

                st.markdown(f"""
                    <div class="report-card {card_class}">
                        <h4>{t['verdict_title']}: <span style="text-decoration: underline;">{display_verdict}</span></h4>
                        <p>{t['verdict_desc']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    st.metric(label=t['metric_length'], value=analysis["word_count"])
                with m_col2:
                    st.metric(label=t['metric_sections'], value=f"{len(analysis['sections_found'])} / 7")
                    
                st.markdown(t['tech_skills_title'])
                if analysis["skills_found"]:
                    skills_html = "".join([f"<span style='background-color:#E0F2FE; color:#0369A1; padding: 6px 12px; margin: 4px; border-radius: 20px; display: inline-block; font-size: 14px; font-weight: 500;'>{skill}</span>" for skill in analysis["skills_found"]])
                    st.markdown(skills_html, unsafe_allow_html=True)
                else:
                    st.warning(t['no_skills_warn'])
                    
            with col2:
                st.plotly_chart(generate_gauge_chart(analysis["score"], t['chart_title']), use_container_width=True)
                st.markdown(t['matrix_title'])
                sec_col1, sec_col2 = st.columns(2)
                with sec_col1:
                    st.markdown(t['found_label'])
                    for sect in analysis["sections_found"]:
                        st.caption(f"🍏 {sect}")
                with sec_col2:
                    st.markdown(t['missing_label'])
                    if analysis["sections_missing"]:
                        for sect in analysis["sections_missing"]:
                            st.caption(f"🍎 {sect}")
                    else:
                        st.caption(t['perfect_alignment'])
            
            st.markdown("---")
            st.markdown(t['roadmap_title'])
            for suggestion in analysis["suggestions"]:
                st.markdown(suggestion)
                
            # ==========================================
            # 6. GENERATIVE INTELLIGENCE INTERFACE LAYER
            # ==========================================
            st.markdown("---")
            st.markdown(t['ai_opt_title'])
            st.write(f"{t['ai_opt_desc']} (**{ai_provider}**)")
            
            if "ai_response_cache" not in st.session_state:
                st.session_state.ai_response_cache = None
            
            if st.button(t['ai_button']):
                with st.spinner(t['ai_spinner']):
                    # FIXED: Added all required arguments matching Section 4 definition update
                    ai_result = generate_ai_analysis(
                        resume_text, analysis, t, 
                        ai_provider, selected_model, base_url, api_key
                    )
                    if ai_result:
                        st.session_state.ai_response_cache = ai_result

            if st.session_state.ai_response_cache:
                st.info(f"{t['ai_success_msg']} **{selected_model}**")
                st.markdown(st.session_state.ai_response_cache)
            
            st.markdown("---")
            b_col1, b_col2 = st.columns([1, 1])
            with b_col1:
                st.markdown(t['export_title'])
                final_download_payload = generate_report_text(analysis, st.session_state.ai_response_cache or t['no_ai_report'], t)
                st.download_button(
                    label=t['download_button_label'],
                    data=final_download_payload,
                    file_name="Resume_Analysis_Report.txt",
                    mime="text/plain"
                )
            with b_col2:
                with st.expander(t['raw_stream_title']):
                    st.text_area(t['raw_stream_label'], value=resume_text, height=250, disabled=True)
        else:
            st.error(t['unreadable_error'])
else:
    st.markdown("---")
    st.info(t['awaiting_input'])
