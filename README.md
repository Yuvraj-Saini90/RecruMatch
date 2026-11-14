# Smart Resume Screening and Candidate Ranking Tool

> **An AI-assisted, explainable recruiter screening system for transparent candidate triage and qualification ranking.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![spaCy NLP](https://img.shields.io/badge/spaCy-3.8-09A3D5.svg)](https://spacy.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-TF--IDF-F7931E.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Project Overview

**Smart Resume Screening and Candidate Ranking Tool** is a B.Tech Computer Science & Engineering (CSE) academic project designed to solve recruiter fatigue and screening subjectivity during initial application triage.

In modern recruitment, HR teams receive hundreds to thousands of resumes for a single job opening. Manual screening is notoriously slow, inconsistent across reviewers, and vulnerable to fatigue. Traditional applicant tracking systems (ATS) often rely on brittle keyword search or opaque "black-box" scores.

This system bridges that gap by combining:
1. **Robust Multi-Format Parsing**: Extracts text from both PDF (`pdfplumber`) and DOCX (`python-docx`) files safely.
2. **spaCy NLP & Canonical Taxonomy**: Normalizes terminology variations (`ML` $\to$ `Machine Learning`, `Postgres` $\to$ `PostgreSQL`, `JS` $\to$ `JavaScript`).
3. **Transparent Weighted Multi-Criteria Scoring**: Replaces mystery AI scores with deterministic, auditable mathematical breakdowns across Required Skills, Preferred Skills, Experience, Education, and Text Similarity.
4. **Interactive SaaS Recruiter Dashboard**: Built with Streamlit, providing radar charts, gap analysis, candidate inspection, and CSV/Markdown audit exports.

> ⚖️ **Human-in-the-Loop Design Principle:**  
> This system is strictly an **assistive screening aid**. It provides triage recommendations and qualification gap analysis, but **never automatically hires or rejects candidates**. Final evaluation and progression remain exclusively with a qualified human recruiter.

---

## 👨‍🎓 Project Credits & Affiliation

- **Student Developer:** Yuvraj Saini
- **Supervisor:** Mr. Ashwini Kr. Verma
- **Department:** Department of Computer Science & Engineering
- **Institution:** GNIOT Engineering Institute, Greater Noida, Uttar Pradesh, India

---

## 🚀 Key Features

- **Multi-Format Resume Support**: Upload batches of PDF and DOCX documents simultaneously with error isolation.
- **Job Description Requirement Extraction**: Automatically detects Required Skills, Preferred/Bonus Skills, Experience requirements, and Target Education degrees from Job Descriptions.
- **Explainability Over Black-Box AI**:
  - Exact breakdown: `Required Skills (40%)`, `Preferred Skills (15%)`, `Experience (15%)`, `Education (10%)`, `Similarity (20%)`.
  - Visual matched vs. missing skills chips for every candidate.
  - Deterministic recruiter narrative generated for every score.
- **Categorized Match Tiers**:
  - 🟢 **Excellent Match (≥ 80%)**
  - 🔵 **Good Match (60% – 79%)**
  - 🟡 **Moderate Match (40% – 59%)**
  - 🔴 **Low Match (< 40%)**
- **Dashboard Analytics**:
  - Score distribution bar charts.
  - Required skill gap analysis highlighting missing skills across the applicant pool.
  - Multi-dimensional radar charts for individual candidate strengths.
- **Interactive Recruiter Controls**:
  - Dynamic weight sliders that allow custom corporate hiring criteria.
  - Threshold adjustments.
  - Candidate name search and tier filtering.
- **Audit Export**:
  - One-click CSV leaderboard export.
  - Downloadable Markdown audit report for hiring managers.
- **100% Local & Privacy-Preserving**: Runs completely offline without external APIs, paid cloud services, or data leakage.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | Streamlit | Modern SaaS recruitment dashboard |
| **REST API Server** | FastAPI & Uvicorn | Standalone dual-tier REST endpoints & Swagger UI (/docs) |
| **Document Parsing** | pdfplumber | Multi-page PDF text extraction |
| **Document Parsing** | python-docx | DOCX paragraph and table parsing |
| **NLP Core** | spaCy (`en_core_web_sm`) | Tokenization, NER, lemmatization |
| **Text Vectorization** | scikit-learn (`TfidfVectorizer`) | N-gram TF-IDF and Cosine Similarity |
| **Data Processing** | pandas, NumPy | Structured candidate tables and metrics |
| **Data Visualization** | Plotly | Interactive radar, gap, and distribution charts |
| **Synthetic Data** | reportlab | Generating standardized PDF test resumes |

---

## 🏗️ System Architecture & Workflow

```text
       Candidate Resumes                         Job Description
       (PDF / DOCX Upload)                      (Pasted or Uploaded)
               │                                         │
               ▼                                         ▼
      1. Text Extraction                        2. JD Requirement
   (pdfplumber / python-docx)                         Analysis
               │                                         │
               ▼                                         ▼
      3. spaCy NLP Layer                        • Required Skills
   • Contact Info Extraction                    • Preferred Skills
   • Education Parsing                          • Target Experience
   • Experience Timeline                        • Target Education
               │                                         │
               ▼                                         ▼
      4. Skill Extraction &                     5. Text Similarity Engine
     Canonical Normalization                     • TF-IDF Vectorizer
   (Centralized Skill Taxonomy)                  • Cosine Similarity Matrix
               │                                         │
               └────────────────────┬────────────────────┘
                                    ▼
                         6. Explainable Scorer
                   (Configurable Weighted Formula)
                                    │
                                    ▼
                         7. Candidate Ranking
                         (Audit Trail & Leaderboard)
                                    │
                                    ▼
                       8. Recruiter Dashboard
               (Radar Charts, Gap Analysis, CSV Export)
```

---

## 🧮 How the Scoring Formula Works

The overall candidate match score is calculated as a multi-criteria weighted linear combination:

$$\text{Final Score} = w_{\text{req}} \cdot S_{\text{req}} + w_{\text{pref}} \cdot S_{\text{pref}} + w_{\text{exp}} \cdot S_{\text{exp}} + w_{\text{edu}} \cdot S_{\text{edu}} + w_{\text{sim}} \cdot S_{\text{sim}}$$

### Component Calculations:

1. **Required Skill Score ($S_{\text{req}}$):**
   $$S_{\text{req}} = \left( \frac{|\text{Candidate Skills} \cap \text{Required Skills}|}{|\text{Required Skills}|} \right) \times 100$$

2. **Preferred Skill Score ($S_{\text{pref}}$):**
   $$S_{\text{pref}} = \left( \frac{|\text{Candidate Skills} \cap \text{Preferred Skills}|}{|\text{Preferred Skills}|} \right) \times 100$$
   *(If no preferred skills are listed in the JD, this factor gracefully normalizes without penalizing the candidate).*

3. **Experience Match Score ($S_{\text{exp}}$):**
   - If candidate experience $\ge$ required experience: $100\%$
   - If candidate experience $> 0$ and $<$ required: $\left( \frac{\text{Candidate Years}}{\text{Required Years}} \right) \times 100$
   - If experience not detected: $50\%$ baseline partial credit with explicit audit notice.

4. **Education Match Score ($S_{\text{edu}}$):**
   - Exact degree match (e.g. Master's required, Master's detected): $100\%$
   - Degree level match (e.g. Bachelor's required, B.Tech detected): $100\%$
   - Adjacent technical degree: $75\%$
   - Unverified / not detected: $50\% - 60\%$

5. **Text Similarity ($S_{\text{sim}}$):**
   $$\text{Cosine Similarity} = \frac{\vec{v}_{\text{JD}} \cdot \vec{v}_{\text{Resume}}}{\|\vec{v}_{\text{JD}}\| \|\vec{v}_{\text{Resume}}\|} \times 100$$

**Default Weights:**
- Required Skills: $40\%$
- Preferred Skills: $15\%$
- Experience: $15\%$
- Education: $10\%$
- Text Similarity: $20\%$  
*(All weights are customizable in the Settings page).*

---

## 📥 Installation & Setup

### Prerequisites
- Python 3.10, 3.11, 3.12, or 3.13
- Git

### 1. Clone or Download Repository
```bash
git clone https://github.com/your-username/smart-resume-screening.git
cd smart-resume-screening
```

### 2. Create and Activate Virtual Environment
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download spaCy English Model
```bash
python -m spacy download en_core_web_sm
```

---

## 🖥️ Running the Application

### Option A: Interactive Streamlit Web Dashboard
Launch the recruiter dashboard:
```bash
streamlit run app.py
```
Access in your browser at: `http://localhost:8501`

### Option B: Standalone FastAPI REST API Server
Launch the REST API server:
```bash
uvicorn api:app --reload --port 8000
```
or:
```bash
python api.py
```
- API Base URL: `http://127.0.0.1:8000`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- Interactive ReDoc: `http://127.0.0.1:8000/redoc`

#### Available REST Endpoints:
* `GET /api/health` — System status, academic metadata, and supported skills count.
* `GET /api/skills` — Lists all 130+ canonical skills supported by the taxonomy.
* `POST /api/parse-jd` — Extracts required skills, experience, and education from a job description.
* `POST /api/screen-resumes` — Multipart endpoint accepting multiple resume files (`.pdf`, `.docx`) + JD text or file, returning a ranked leaderboard and breakdown.

---

## ⚡ 1-Click Demonstration

For immediate testing without preparing files:
1. Open the application.
2. In the sidebar, click the **🚀 Load Sample Dataset (1-Click)** button.
3. The system will load:
   - A Senior Python & Machine Learning Engineer Job Description.
   - 4 diverse candidate resumes (`Aman Verma [PDF]`, `Priya Sharma [PDF]`, `Rahul Kumar [DOCX]`, `Sneha Gupta [DOCX]`).
4. Navigate across the tabs to explore the Leaderboard, Candidate Details, and Analytics.

---

## 📚 Viva Defense & Examination Guide

### Q1: Why use TF-IDF rather than a large generative LLM (e.g., GPT-4)?
- **Zero Hallucination:** TF-IDF and taxonomy parsing only match terms actually present in the candidate's resume.
- **Explainability:** Recruiters can inspect every individual token and requirement weight.
- **Cost & Latency:** Operates entirely locally with instantaneous scoring and zero API billing.
- **Privacy:** Prevents transmitting sensitive candidate PII to third-party cloud servers.

### Q2: How does the system handle terminology differences?
- The application uses a centralized normalization dictionary (`src/skill_dictionary.py`) that maps common variations (e.g., `ML`, `machine-learning`, `Machine Learning`) to canonical representations before comparison.

### Q3: How is bias mitigated?
- Irrelevant demographic factors such as candidate photos, gender, age, religion, marital status, and caste are strictly omitted from the scoring engine.

---

## 🔮 Future Enhancements

- [ ] Dense transformer embeddings using Sentence-BERT (`all-MiniLM-L6-v2`) as default optional toggle.
- [ ] Automated bias auditing metrics (Adverse Impact Ratio / 4/5ths rule verification).
- [ ] Recruiter active learning feedback loop to tune weights dynamically from historical hiring decisions.
- [ ] Database persistence (PostgreSQL / SQLite) for multi-job requisition management.
- [ ] OCR integration for scanned image-based PDF resumes.

---

## 📄 License

This academic project is open-source under the MIT License.
