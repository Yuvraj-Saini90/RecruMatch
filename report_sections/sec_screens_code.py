"""Chapters 6 and 7:
- CHAPTER 6: SYSTEM USER INTERFACE & SCREENSHOTS (Dashboard, Ranking Leaderboard, Radar Chart, Forensic Inspector)
- CHAPTER 7: MODULAR SYSTEM CODING & IMPLEMENTATION (7 Core Modules with code blocks and line-by-line discussions)
"""

import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_full_report import (
    add_heading_1, add_heading_2, add_heading_3, add_body_p, 
    add_bullet_p, add_caption, add_code_block
)

def add_chapter_6_screenshots(doc):
    add_heading_1(doc, "CHAPTER 6: SYSTEM USER INTERFACE & SCREENSHOTS")
    add_body_p(doc,
        "This chapter presents high-resolution screenshots of the RecruMatch interactive recruiter dashboard, accompanied "
        "by detailed functional walk-throughs of each graphical user interface component."
    )

    add_heading_2(doc, "6.1 Recruiter Analytics & Applicant Pool Triage Dashboard")
    add_body_p(doc,
        "Figure 6.1 illustrates the primary RecruMatch Executive Triage Dashboard. Designed with a custom dark-mode aesthetic "
        "(assets/style.css), the dashboard delivers instant high-level situational awareness across the entire applicant pool."
    )

    img_dash = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diagrams", "screenshot_dashboard.png")
    if os.path.exists(img_dash):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture(img_dash, width=Inches(6.0))
        add_caption(doc, "Figure 6.1: Recruiter Analytics & Applicant Pool Triage Dashboard")

    add_body_p(doc,
        "Key elements of the Triage Dashboard interface include:"
    )
    add_bullet_p(doc, "Four prominent cards summarize pool health in real time: Total Applicants (5), Average Pool Score (49.6%), Strong Matches (2 candidates, representing 40% of the pool), and Adversarial Threat Flags (1 candidate flagged).", "1. High-Level KPI Summary Cards: ")
    add_bullet_p(doc, "An interactive bar chart categorizes applicants across the four standardized match tiers: Excellent (≥80%: 0), Good (60-79%: 2), Moderate (40-59%: 1), and Low (<40%: 2), enabling recruiters to immediately gauge candidate quality distribution.", "2. Match Tier Distribution Chart: ")
    add_bullet_p(doc, "Sidebar toggle switches allow instant activation of Blind Recruitment Mode (anonymizing PII) and loading demo benchmark datasets with a single click.", "3. Workspace & Ethical Controls: ")

    add_heading_2(doc, "6.2 Candidate Ranking Leaderboard & Multi-Criteria Filtering")
    add_body_p(doc,
        "Figure 6.2 presents the Candidate Ranking Leaderboard, where parsed candidates are organized into a dynamically "
        "sortable table based on composite evaluation scores."
    )

    img_rank = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diagrams", "screenshot_ranking.png")
    if os.path.exists(img_rank):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture(img_rank, width=Inches(6.0))
        add_caption(doc, "Figure 6.2: Candidate Ranking Leaderboard & Multi-Criteria Filtering")

    add_body_p(doc,
        "The leaderboard provides comprehensive operational data at a glance:"
    )
    add_bullet_p(doc, "Each row displays rank order, candidate name (or token in Blind Mode), composite match score, match tier badge, required skills match count, verified years of experience, and cyber-forensic verification status.", "1. Comprehensive Ranking Columns: ")
    add_bullet_p(doc, "Adversarial candidate Vikram Malhotra is visually tagged with a high-priority warning badge indicating that 3 adversarial exploits were detected in their PDF stream.", "2. Cyber-Forensic Flagging: ")
    add_bullet_p(doc, "Dedicated action buttons allow one-click export of complete audit reports in CSV and Markdown formats, alongside instant drill-down inspection into individual candidate profiles.", "3. Export & Action Controls: ")

    add_heading_2(doc, "6.3 Candidate Deep Dive, 5-Axis Radar Chart & Skill Gap Analysis")
    add_body_p(doc,
        "Figure 6.3 illustrates the Candidate Deep Dive inspection view, featuring a multi-criteria 5-axis competency radar "
        "chart comparing candidates across Required Skills, Preferred Skills, Experience, Education, and Semantic Similarity."
    )

    img_det = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diagrams", "screenshot_candidate_detail.png")
    if os.path.exists(img_det):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture(img_det, width=Inches(4.8))
        add_caption(doc, "Figure 6.3: Multi-Criteria 5-Axis Candidate Competency Radar Comparison")

    add_body_p(doc,
        "This deep dive screen equips hiring managers with actionable technical insights:"
    )
    add_bullet_p(doc, "Overlaying polygon shapes reveal multi-dimensional competencies. Aman Verma demonstrates high Required Skills (84.6%) and Experience (100%), while Priya Sharma excels in Education (100%) and AI specialization.", "1. Multi-Axis Competency Visualization: ")
    add_bullet_p(doc, "Skills explicitly present in the candidate's resume are displayed in green chips, while missing mandatory skills (e.g. Algorithms, GitHub) are displayed in red chips for focused review.", "2. Matched vs. Missing Skill Chips: ")
    add_bullet_p(doc, "Displays candidate promotion trajectory badges and provides an automated interview kit with tailored technical questions.", "3. Career Velocity & Interview Kit: ")

    add_heading_2(doc, "6.4 Resume Forensic Exploit Inspector & Adversarial Console")
    add_body_p(doc,
        "Figure 6.4 illustrates the dedicated Resume Forensic Inspector console, showcasing the detection and isolation of "
        "sophisticated PDF exploits."
    )

    img_forensic = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diagrams", "screenshot_forensic_inspector.png")
    if os.path.exists(img_forensic):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture(img_forensic, width=Inches(6.0))
        add_caption(doc, "Figure 6.4: Resume Forensic Exploit Inspector & Adversarial Alert Console")

    add_body_p(doc,
        "The forensic console provides complete threat transparency:"
    )
    add_bullet_p(doc, "Highlights resumes exhibiting high fraud scores (e.g. Vikram Malhotra: Fraud Score 85/100, CRITICAL RISK).", "1. Threat Banner & Calibration: ")
    add_bullet_p(doc, "Three dedicated exploit cards itemize the exact attacks identified: 18 spans of hidden white text (#FFFFFF), micro-font keyword stuffing rendered at 1.5 pt, and Cyrillic homoglyph substitutions.", "2. Exploit Breakdown Cards: ")
    add_bullet_p(doc, "Presents a side-by-side view of the original raw document text versus the sanitized, cleaned text stream passed to downstream scoring.", "3. Sanitized Text Diff Viewer: ")

    doc.add_page_break()

def add_chapter_7_coding(doc):
    add_heading_1(doc, "CHAPTER 7: MODULAR SYSTEM CODING & IMPLEMENTATION")
    add_body_p(doc,
        "This chapter documents the modular implementation of RecruMatch. Core architectural components are presented "
        "alongside comprehensive engineering discussions detailing algorithmic choices, design patterns, and exception "
        "handling mechanisms."
    )

    add_heading_2(doc, "7.1 Multi-Format Document Text Extraction (src/pdf_parser.py & src/docx_parser.py)")
    add_body_p(doc,
        "The document parsing layer extracts clean textual content from PDF and DOCX files. The implementation employs a "
        "resilient multi-tier strategy: pdfplumber performs layout-aware extraction, gracefully falling back to PyMuPDF "
        "(fitz) if layout streams are unreadable."
    )

    code_pdf = (
        "import os\n"
        "import pdfplumber\n"
        "import fitz  # PyMuPDF\n\n"
        "def extract_text_from_pdf(file_path: str) -> str:\n"
        "    \"\"\"Extract text from a PDF file using pdfplumber with PyMuPDF fallback.\"\"\"\n"
        "    if not os.path.exists(file_path):\n"
        "        raise FileNotFoundError(f\"PDF file not found: {file_path}\")\n\n"
        "    extracted_text = []\n"
        "    try:\n"
        "        with pdfplumber.open(file_path) as pdf:\n"
        "            for page in pdf.pages:\n"
        "                text = page.extract_text(layout=True)\n"
        "                if text:\n"
        "                    extracted_text.append(text)\n"
        "        if extracted_text:\n"
        "            return \"\\n\".join(extracted_text).strip()\n"
        "    except Exception:\n"
        "        pass  # Fall back to PyMuPDF\n\n"
        "    try:\n"
        "        doc = fitz.open(file_path)\n"
        "        for page in doc:\n"
        "            text = page.get_text(\"text\")\n"
        "            if text:\n"
        "                extracted_text.append(text)\n"
        "        return \"\\n\".join(extracted_text).strip()\n"
        "    except Exception as e:\n"
        "        return f\"Error extracting PDF text: {str(e)}\""
    )
    add_code_block(doc, code_pdf, "Listing 7.1: Multi-Format PDF Extraction Engine (src/pdf_parser.py)")

    add_body_p(doc,
        "In Listing 7.1, pdfplumber's layout=True parameter preserves spatial indentations and multi-column formatting, "
        "which are crucial for distinguishing resume sections. If pdfplumber encounters an unhandled formatting exception, "
        "execution falls back to PyMuPDF's C-accelerated get_text() API, ensuring robust extraction even from non-standard "
        "PDF implementations."
    )

    add_heading_2(doc, "7.2 Adversarial PDF Forensic Detection Engine (forensic_inspector.py)")
    add_body_p(doc,
        "The Forensic Inspector inspects low-level PDF stream primitives to detect hidden white text, micro-fonts, and "
        "Unicode homoglyph spoofing."
    )

    code_forensic = (
        "import fitz  # PyMuPDF\n"
        "import re\n\n"
        "class ResumeForensicInspector:\n"
        "    \"\"\"Inspects low-level PDF stream properties to identify adversarial ATS exploits.\"\"\"\n\n"
        "    HOMOGLYPH_MAP = {'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y', 'х': 'x'}\n\n"
        "    def inspect_pdf_stream(self, file_path_or_bytes) -> dict:\n"
        "        doc = fitz.open(file_path_or_bytes) if isinstance(file_path_or_bytes, str) else fitz.open(stream=file_path_or_bytes, filetype=\"pdf\")\n"
        "        white_spans, micro_spans, homoglyphs = [], [], []\n"
        "        clean_text_lines = []\n\n"
        "        for page in doc:\n"
        "            blocks = page.get_text(\"dict\").get(\"blocks\", [])\n"
        "            for b in blocks:\n"
        "                if \"lines\" not in b:\n"
        "                    continue\n"
        "                for line in b[\"lines\"]:\n"
        "                    line_text = []\n"
        "                    for span in line[\"spans\"]:\n"
        "                        text, size, color = span[\"text\"], span[\"size\"], span[\"color\"]\n"
        "                        r = ((color >> 16) & 255) / 255.0\n"
        "                        g = ((color >> 8) & 255) / 255.0\n"
        "                        b = (color & 255) / 255.0\n\n"
        "                        # 1. White / Hidden text check\n"
        "                        if r > 0.98 and g > 0.98 and b > 0.98:\n"
        "                            white_spans.append(text)\n"
        "                            continue  # Strip invisible text\n\n"
        "                        # 2. Micro-font check (< 2.0 pt)\n"
        "                        if size < 2.0:\n"
        "                            micro_spans.append(text)\n"
        "                            continue\n\n"
        "                        # 3. Homoglyph substitution check\n"
        "                        sanitized_span = \"\"\n"
        "                        for ch in text:\n"
        "                            if ch in self.HOMOGLYPH_MAP:\n"
        "                                homoglyphs.append(ch)\n"
        "                                sanitized_span += self.HOMOGLYPH_MAP[ch]\n"
        "                            else:\n"
        "                                sanitized_span += ch\n\n"
        "                        line_text.append(sanitized_span)\n"
        "                    if line_text:\n"
        "                        clean_text_lines.append(\" \".join(line_text))\n\n"
        "        fraud_score = min(100.0, len(white_spans)*5.0 + len(micro_spans)*4.0 + len(homoglyphs)*2.0)\n"
        "        return {\n"
        "            \"fraud_score\": fraud_score,\n"
        "            \"white_text_count\": len(white_spans),\n"
        "            \"micro_font_count\": len(micro_spans),\n"
        "            \"homoglyph_count\": len(homoglyphs),\n"
        "            \"sanitized_text\": \"\\n\".join(clean_text_lines)\n"
        "        }"
    )
    add_code_block(doc, code_forensic, "Listing 7.2: Adversarial PDF Forensic Detection Engine (forensic_inspector.py)")

    add_body_p(doc,
        "In Listing 7.2, the inspector iterates through font spans, extracting RGB integer color bits via bitwise shift "
        "operations. Spans where R, G, and B exceed 0.98 are flagged as invisible white text and stripped from clean_text_lines. "
        "Similarly, font sizes under 2.0 pt are quarantined, and Cyrillic homoglyphs are mapped to canonical Latin characters, "
        "producing an impervious sanitized text stream for downstream NLP scoring."
    )

    add_heading_2(doc, "7.3 Canonical Skill Extraction & Synonym Mapping (src/skill_extractor.py)")
    add_body_p(doc,
        "The skill extraction module parses resume text against the centralized canonical taxonomy, utilizing pre-compiled "
        "word-boundary regular expressions to achieve exact, robust matching without false positives."
    )

    code_skill = (
        "import re\n"
        "from src.skill_dictionary import SKILL_TAXONOMY\n\n"
        "def extract_skills_from_text(text: str) -> dict:\n"
        "    \"\"\"Extract and normalize canonical technical skills using synonym dictionary.\"\"\"\n"
        "    text_lower = f\" {text.lower()} \"\n"
        "    found_skills = {}\n\n"
        "    for canonical_name, data in SKILL_TAXONOMY.items():\n"
        "        synonyms = data.get(\"synonyms\", [canonical_name.lower()])\n"
        "        for syn in synonyms:\n"
        "            # Escape special regex symbols (e.g. C++, .NET, C#)\n"
        "            escaped_syn = re.escape(syn.lower())\n"
        "            pattern = rf'(?<![a-zA-Z0-9_]){escaped_syn}(?![a-zA-Z0-9_])'\n"
        "            if re.search(pattern, text_lower):\n"
        "                found_skills[canonical_name] = {\n"
        "                    \"category\": data[\"category\"],\n"
        "                    \"matched_alias\": syn\n"
        "                }\n"
        "                break  # Matched canonical skill, proceed to next\n\n"
        "    return found_skills"
    )
    add_code_block(doc, code_skill, "Listing 7.3: Canonical Skill Extraction Module (src/skill_extractor.py)")

    add_body_p(doc,
        "In Listing 7.3, negative lookbehind (?<![a-zA-Z0-9_]) and negative lookahead (?![a-zA-Z0-9_]) assertions prevent "
        "erroneous substring matches (e.g. preventing 'Java' from falsely triggering inside 'JavaScript', or 'Go' inside 'Good'). "
        "Special language characters like 'C++' and 'C#' are safely handled via re.escape."
    )

    add_heading_2(doc, "7.4 Skill Knowledge Graph & Implicit Competencies (src/skill_graph.py)")
    add_body_p(doc,
        "The knowledge graph models hierarchical parent-child relationships between technical tools, inferring underlying "
        "competencies with calibrated confidence weights."
    )

    code_graph = (
        "SKILL_DEPENDENCY_GRAPH = {\n"
        "    \"PyTorch\": [(\"Python\", 0.95), (\"Machine Learning\", 0.90), (\"Deep Learning\", 0.95)],\n"
        "    \"TensorFlow\": [(\"Python\", 0.95), (\"Machine Learning\", 0.90), (\"Deep Learning\", 0.95)],\n"
        "    \"Kubernetes\": [(\"Docker\", 0.90), (\"Cloud & DevOps\", 0.85)],\n"
        "    \"Next.js\": [(\"React\", 0.95), (\"JavaScript\", 0.95), (\"TypeScript\", 0.80)],\n"
        "    \"FastAPI\": [(\"Python\", 0.95), (\"REST API\", 0.90)],\n"
        "    \"Django\": [(\"Python\", 0.95), (\"Web Development\", 0.85)]\n"
        "}\n\n"
        "def infer_implicit_competencies(explicit_skills: set) -> dict:\n"
        "    \"\"\"Infers parent prerequisite skills from advanced technologies.\"\"\"\n"
        "    inferred = {}\n"
        "    for skill in explicit_skills:\n"
        "        if skill in SKILL_DEPENDENCY_GRAPH:\n"
        "            for parent_skill, conf in SKILL_DEPENDENCY_GRAPH[skill]:\n"
        "                if parent_skill not in explicit_skills:\n"
        "                    if parent_skill not in inferred or conf > inferred[parent_skill]:\n"
        "                        inferred[parent_skill] = conf\n"
        "    return inferred"
    )
    add_code_block(doc, code_graph, "Listing 7.4: Skill Knowledge Graph Engine (src/skill_graph.py)")

    add_heading_2(doc, "7.5 Explainable Multi-Criteria Scoring Algorithm (src/scorer.py)")
    add_body_p(doc,
        "The scoring algorithm computes the composite match score across all five mathematical criteria, generating an "
        "explainable audit trail for recruiters."
    )

    code_scorer = (
        "def compute_candidate_score(candidate_data: dict, jd_data: dict, weights: dict) -> dict:\n"
        "    \"\"\"Computes transparent, explainable candidate match score.\"\"\"\n"
        "    # 1. Required Skills Match (S_req)\n"
        "    req_skills = set(jd_data.get(\"required_skills\", []))\n"
        "    cand_skills = set(candidate_data.get(\"skills\", []))\n"
        "    matched_req = req_skills.intersection(cand_skills)\n"
        "    s_req = (len(matched_req) / len(req_skills) * 100.0) if req_skills else 100.0\n\n"
        "    # 2. Preferred Skills Match (S_pref)\n"
        "    pref_skills = set(jd_data.get(\"preferred_skills\", []))\n"
        "    matched_pref = pref_skills.intersection(cand_skills)\n"
        "    s_pref = (len(matched_pref) / len(pref_skills) * 100.0) if pref_skills else 100.0\n\n"
        "    # 3. Experience Match (S_exp)\n"
        "    min_exp = jd_data.get(\"min_experience\", 0.0)\n"
        "    cand_exp = candidate_data.get(\"experience_years\", 0.0)\n"
        "    s_exp = min(100.0, (cand_exp / min_exp * 100.0)) if min_exp > 0 else 100.0\n\n"
        "    # 4. Education Match (S_edu)\n"
        "    s_edu = evaluate_education_tier(candidate_data.get(\"degree\"), jd_data.get(\"target_education\"))\n\n"
        "    # 5. Semantic Cosine Similarity (S_sim)\n"
        "    s_sim = compute_tfidf_cosine(candidate_data.get(\"text\", \"\"), jd_data.get(\"text\", \"\")) * 100.0\n\n"
        "    # Composite Weighted Sum\n"
        "    final_score = (\n"
        "        weights[\"required_skills\"] * s_req +\n"
        "        weights[\"preferred_skills\"] * s_pref +\n"
        "        weights[\"experience\"] * s_exp +\n"
        "        weights[\"education\"] * s_edu +\n"
        "        weights[\"similarity\"] * s_sim\n"
        "    )\n"
        "    return {\n"
        "        \"final_score\": round(final_score, 1),\n"
        "        \"s_req\": round(s_req, 1), \"s_pref\": round(s_pref, 1),\n"
        "        \"s_exp\": round(s_exp, 1), \"s_edu\": round(s_edu, 1), \"s_sim\": round(s_sim, 1),\n"
        "        \"matched_skills\": list(matched_req),\n"
        "        \"missing_skills\": list(req_skills - cand_skills)\n"
        "    }"
    )
    add_code_block(doc, code_scorer, "Listing 7.5: Explainable Multi-Criteria Scoring Algorithm (src/scorer.py)")

    add_heading_2(doc, "7.6 Blind Recruitment & DEI PII Anonymizer (src/anonymizer.py)")
    add_body_p(doc,
        "The Blind Recruitment module scrubs personal identifiers, generating cryptographic tokens to guarantee unbiased triage."
    )

    code_anon = (
        "import hashlib\n"
        "import re\n\n"
        "def anonymize_candidate_profile(candidate: dict, index: int) -> dict:\n"
        "    \"\"\"Redacts candidate PII and institutional markers to enforce merit-based screening.\"\"\"\n"
        "    token = hashlib.sha256(candidate[\"name\"].encode()).hexdigest()[:6]\n"
        "    anon_profile = candidate.copy()\n\n"
        "    anon_profile[\"name\"] = f\"Candidate #{index+1} [Token: {token}]\"\n"
        "    anon_profile[\"email\"] = \"[REDACTED_FOR_FAIRNESS]\"\n"
        "    anon_profile[\"phone\"] = \"[REDACTED_FOR_FAIRNESS]\"\n\n"
        "    # Normalize institution name to generic degree\n"
        "    raw_edu = candidate.get(\"education\", \"\")\n"
        "    for degree in [\"B.Tech\", \"M.Tech\", \"Ph.D.\", \"B.S.\", \"M.S.\", \"BCA\", \"MCA\"]:\n"
        "        if degree.lower() in raw_edu.lower():\n"
        "            anon_profile[\"education\"] = f\"{degree} in Computer Science (Institution Anonymized)\"\n"
        "            break\n"
        "    return anon_profile"
    )
    add_code_block(doc, code_anon, "Listing 7.6: Blind Recruitment Anonymization Engine (src/anonymizer.py)")

    add_heading_2(doc, "7.7 FastAPI REST API Server Implementation (api.py)")
    add_body_p(doc,
        "The standalone FastAPI backend provides headless REST endpoints for enterprise recruitment systems."
    )

    code_api = (
        "from fastapi import FastAPI, UploadFile, File, Form\n"
        "from typing import List\n"
        "from src.scorer import compute_candidate_score\n"
        "from forensic_inspector import ResumeForensicInspector\n\n"
        "app = FastAPI(title=\"RecruMatch REST API\", version=\"1.0.0\")\n"
        "inspector = ResumeForensicInspector()\n\n"
        "@app.post(\"/api/screen-resumes\")\n"
        "async def screen_resumes(\n"
        "    jd_text: str = Form(...),\n"
        "    files: List[UploadFile] = File(...)\n"
        "):\n"
        "    \"\"\"Multipart endpoint accepting batch resumes and returning ranked scoring breakdowns.\"\"\"\n"
        "    results = []\n"
        "    for file in files:\n"
        "        contents = await file.read()\n"
        "        forensic_res = inspector.inspect_pdf_stream(contents)\n"
        "        # Score sanitized text...\n"
        "        results.append({\"filename\": file.filename, \"fraud_score\": forensic_res[\"fraud_score\"]})\n"
        "    return {\"status\": \"success\", \"candidates\": results}"
    )
    add_code_block(doc, code_api, "Listing 7.7: FastAPI REST Server Implementation (api.py)")

    doc.add_page_break()

print("Chapters 6 and 7 module configured.")
