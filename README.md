# Resume Analyzer

## Name

Resume Analyzer

## Description

Resume Analyzer is an application designed to help job seekers check and optimize their resumes for Applicant Tracking Systems (ATS). Users can drop a PDF file into the app, and it extracts text data to evaluate formatting, composition, and completeness.

### Features

* **PDF Upload Engine:** Processes raw file text on submission.
* **Structural Checklists:** Verifies the presence of Contact Information, Education, Skills, Projects, Experience, and Certifications sections.
* **Scoring Dashboard:** Generates an overall quantitative rating (e.g., 82/100) alongside key counts like word frequency and matching skills.
* **Actionable Suggestions:** Highlights missing elements, page-length warnings, and prompts users to convert passive descriptions into measurable achievements.

## Badges

## Visuals

```text
Resume Strength Score
████████░░ 82/100

[⚠️ Missing Sections]
- Certifications

[💡 Suggestions]
- Add more technical skills.
- Include measurable achievements.
- Keep resume under one page.

```

## Installation

### Requirements

* Node.js (v18 or higher) OR Python 3.9+
* Browser support for drag-and-drop file upload interfaces

### Setup Steps

1. Clone the repository to your environment:
```bash
git clone [https://code.swecha.org/apravallika/resume-analyzer.git](https://code.swecha.org/apravallika/resume-analyzer.git)
cd resume-analyzer

```


2. Install the necessary project libraries:
```bash
# If using npm
npm install

# If using python
pip install -r requirements.txt

```



## Usage

Run the script or development server using your environment's runtime command:

```bash
# Frontend/Node environment
npm run dev

# Backend/Python environment
python app.py

```

Open your local port in a browser, drag a standard single-page or multi-page resume PDF into the analyzer zone, and review the structural breakdown, keyword match lists, and optimization recommendations.

## Support

For bugs, feature requests, or parsing discrepancies, please open an issue tracking ticket inside the [GitLab Issues dashboard](https://www.google.com/search?q=https://code.swecha.org/apravallika/resume-analyzer/-/issues).

## Roadmap

* [ ] Implement deep structural paragraph parsing using regex matching arrays.
* [ ] Integrate a live progress gauge element to animate scoring adjustments.
* [ ] Add a text-generation feature to instantly rewrite static phrases into impact-focused data metrics.

## Contributing

We welcome project adjustments, bug fixes, and parsing engine optimizations.

1. Fork the codebase repository.
2. Branch out your workspace (`git checkout -b feature/NewFeature`).
3. Commit structural modifications (`git commit -m 'Add NewFeature parsing module'`).
4. Push to your working branch (`git push origin feature/NewFeature`).
5. File a fresh **Merge Request** back to the primary branch.

## Authors and acknowledgment

* **A. Pravallika** - *Team Member 1* - [@apravallika](https://www.google.com/search?q=https://code.swecha.org/apravallika)
* **Sri Harshini** - *Team Member 2* - [@sriharshini2901](https://www.google.com/search?q=https://code.swecha.org/apravallika)
* Thank you to all contributors and open-source file-parsing project teams who provided baseline data extraction tooling.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Project status

Active development. Current milestones focus on polishing core parsing regex logic and fixing file submission constraints.

```

```