# Resume Analyzer

### Name

Resume Analyzer

### Description

Resume Analyzer is an intelligent web application designed to help job seekers evaluate and optimize their resumes for Applicant Tracking Systems (ATS). Users can drop a PDF file into the application to extract text data, evaluate formatting completeness, identify key technical keywords, and leverage advanced AI inference models to rewrite and polish weak resume phrases.

### Features

* **PDF Upload Engine**: Instantly extracts and processes raw text from single or multi-page PDF documents on submission.
* **Structural Checklists**: Verifies the presence of crucial quadrants including Contact Information, Education, Skills, Projects, Experience, Certifications, and Achievements.
* **Scoring Dashboard**: Renders a real-time visual gauge displaying an overall quantitative rating out of 100 alongside exact word counts and found keywords.
* **Multilingual Support**: Supports comprehensive parsing and UI localization for **English**, **Telugu (తెలుగు)**, and **Hindi (हिंदी)**.
* **Hybrid AI Inference Engine**:
* **Local AI Inference**: Connects seamlessly with local LLM frameworks like **Ollama** for secure, private, offline resume text generation and optimization.
* **Bring Your Own Key (BYOK)**: Flexible cloud configuration allowing users to input their own API tokens to route tasks to global proprietary AI backends.


* **Actionable Suggestions**: Flags missing blocks, warns users about suboptimal word limits, and generates specific tips to convert passive statements into measurable achievements.

### Badges

### Visuals

```text
Language Selected: [ 🌐 English | తెలుగు | हिंदी ]

Resume Strength Score ████████░░ 82/100

[⚠️ Missing Sections]
- Certifications / Achievements

[💡 Suggestions]
- Add more technical focus skills.
- Include measurable achievements using the STAR method.
- Keep resume under 800 words for optimal density screening.

[🤖 AI Assistant (Local Ollama / BYOK)]
👉 "Rewrote: 'Responsible for code' ➔ 'Architected modular Python backend pipelines improving scalability by 35%'"

```

### Installation

#### Requirements

* Python 3.9 or higher
* Ollama (Optional, required only for local offline AI inference configurations)
* A modern web browser with support for drag-and-drop file upload interfaces

#### Setup Steps

1. Clone the repository to your environment:
```bash
git clone https://code.swecha.org/apravallika/resume-analyzer.git
cd resume-analyzer

```


2. Install the necessary project libraries:
```bash
pip install -r requirements.txt

```


3. *(Optional)* If using local AI inference, ensure Ollama is installed and running on your system, then pull your preferred model (e.g., Llama3 or Mistral):
```bash
ollama run llama3

```



### Usage

Run the application development server using your environment's runtime command:

```bash
streamlit run app.py

```

Open your local port in a browser (typically `http://localhost:8501`), select your preferred workspace language, toggle your chosen AI routing configuration (Local Ollama or input your cloud token via the BYOK panel), drag a standard resume PDF into the analyzer zone, and review the structural breakdown, keyword match lists, and optimization recommendations.

### Support

For bugs, feature requests, or parsing discrepancies, please open an issue tracking ticket inside the GitLab Issues dashboard.

### Roadmap

* [x] Implement deep structural paragraph parsing using regex matching arrays.
* [x] Integrate a live progress gauge element to animate scoring adjustments.
* [x] Support full multilingual localization (English, Telugu, Hindi).
* [x] Deploy a local AI framework (Ollama) and cloud BYOK token gateway.
* [ ] Add text-generation features to instantly rewrite static phrases into impact-focused data metrics.

### Contributing

We welcome project adjustments, bug fixes, and parsing engine optimizations.

1. Fork the codebase repository.
2. Branch out your workspace (`git checkout -b feature/NewFeature`).
3. Commit structural modifications (`git commit -m 'Add NewFeature parsing module'`).
4. Push to your working branch (`git push origin feature/NewFeature`).
5. File a fresh Merge Request back to the primary branch.

### Authors and acknowledgment

* **A. Pravallika** - Team Member 1 - [@apravallika](https://www.google.com/search?q=https://code.swecha.org/apravallika)
* **Sri Harshini** - Team Member 2 - [@sriharshini2901](https://www.google.com/search?q=https://code.swecha.org/sriharshini2901)

Thank you to all contributors, Swecha mentors, and open-source file-parsing project teams who provided baseline data extraction tooling.


### Project status
**Completed / Production Ready.** Core development milestones—including multi-language expansion (English, Telugu, Hindi), local/cloud AI routing adapters, and text extraction regex matrices—have been fully deployed and verified.
