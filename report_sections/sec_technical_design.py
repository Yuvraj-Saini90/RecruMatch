"""Chapters 4 and 5:
- CHAPTER 4: SYSTEM SPECIFICATIONS & ARCHITECTURAL MODELING (Requirements, DFDs 0/1/2, ER Diagram, Data & Table Structures)
- CHAPTER 5: PROPOSED SYSTEM & CORE ALGORITHMIC ENGINES (4-Tier Architecture, 8 Modules, Scoring Formula, Taxonomy Table)
"""

import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from build_full_report import (
    add_heading_1, add_heading_2, add_heading_3, add_body_p, 
    add_bullet_p, add_caption, build_table, add_code_block
)

def add_chapter_4_analysis(doc):
    add_heading_1(doc, "CHAPTER 4: SYSTEM SPECIFICATIONS & ARCHITECTURAL MODELING")
    
    add_heading_2(doc, "4.1 Detailed Requirement Specifications")
    add_body_p(doc,
        "System analysis defines the precise operational capabilities, behavioral contracts, and performance thresholds "
        "that RecruMatch must fulfill. Requirements are categorized into Functional and Non-Functional specifications."
    )

    add_heading_3(doc, "4.1.1 Functional Requirements (FR)")
    add_bullet_p(doc, "The system shall ingest job descriptions via direct text pasting or pre-configured benchmark templates (Senior Python/ML Engineer, Full Stack Web Developer, Cloud DevOps Specialist).", "FR-1 (Job Description Parsing): ")
    add_bullet_p(doc, "The system shall automatically parse required technical skills, preferred skills, minimum experience thresholds, and target education levels from the job description.", "FR-2 (Requirement Extraction): ")
    add_bullet_p(doc, "The system shall accept batch uploads of candidate resumes in portable document format (.pdf) and Microsoft Word OpenXML format (.docx).", "FR-3 (Multi-Format Document Ingestion): ")
    add_bullet_p(doc, "The system shall inspect low-level PDF stream properties to identify and flag adversarial manipulations, including white text (#FFFFFF), micro-fonts (<2.0 pt), Unicode homoglyph substitutions, and prompt injection strings.", "FR-4 (Cyber-Forensic Inspection): ")
    add_bullet_p(doc, "The system shall normalize extracted technical keywords against a standardized taxonomy of 130+ canonical skills, resolving informal abbreviations and industry synonyms.", "FR-5 (Canonical Taxonomy Normalization): ")
    add_bullet_p(doc, "The system shall infer foundational competencies from specialized frameworks via an implicit skill knowledge graph.", "FR-6 (Knowledge Graph Inference): ")
    add_bullet_p(doc, "The system shall compute an explainable composite match score based on a transparent, configurable 5-criteria weighted formula.", "FR-7 (Multi-Criteria Scoring): ")
    add_bullet_p(doc, "The system shall categorize candidates into four standardized match tiers: Excellent (≥80%), Good (60-79%), Moderate (40-59%), and Low (<40%).", "FR-8 (Match Tier Classification): ")
    add_bullet_p(doc, "The system shall provide a Blind Recruitment Mode that dynamically masks candidate names, contact details, and institutional branding to prevent unconscious bias.", "FR-9 (Blind Recruitment Anonymization): ")
    add_bullet_p(doc, "The system shall generate tailored technical interview kits comprising skill verification, qualification gap, and seniority architecture questions for each candidate.", "FR-10 (Interview Kit Generation): ")

    add_heading_3(doc, "4.1.2 Non-Functional Requirements (NFR)")
    add_bullet_p(doc, "The system shall process and score an individual resume in less than 0.5 seconds on standard commodity CPU hardware.", "NFR-1 (Performance & Latency): ")
    add_bullet_p(doc, "Scoring algorithms shall be 100% deterministic, producing identical scores and ranking positions for identical inputs across all runs.", "NFR-2 (Determinism & Reproducibility): ")
    add_bullet_p(doc, "All text parsing, forensic auditing, and scoring operations shall execute completely offline without transmitting candidate data to external cloud APIs.", "NFR-3 (Data Privacy & Confidentiality): ")
    add_bullet_p(doc, "A corrupted, password-protected, or unreadable document shall be safely isolated without interrupting batch processing of remaining candidate files.", "NFR-4 (Robustness & Fault Tolerance): ")
    add_bullet_p(doc, "The system shall expose an interactive, responsive Streamlit dashboard and a standard OpenAPI / Swagger REST API backend running on port 8000.", "NFR-5 (Usability & Interoperability): ")

    add_heading_2(doc, "4.2 Data Flow Diagrams (DFD)")
    add_body_p(doc,
        "Data Flow Diagrams model the flow of information through the system, illustrating how unstructured resume data "
        "and job descriptions are transformed into explainable candidate rankings and forensic audit logs."
    )

    add_heading_3(doc, "4.2.1 DFD Level 0 (Context Level Diagram)")
    add_body_p(doc,
        "Figure 4.1 illustrates the context-level DFD (Level 0) of RecruMatch. The system is represented as a single central "
        "process (0.0) interacting with three primary external entities: the Recruiter / HR Specialist, Candidate Resumes, "
        "and the Talent Review & Compliance Audit department."
    )
    
    img_dfd0 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diagrams", "dfd_level_0.png")
    if os.path.exists(img_dfd0):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture(img_dfd0, width=Inches(5.8))
        add_caption(doc, "Figure 4.1: Data Flow Diagram (DFD Level 0 - Context Level)")

    add_body_p(doc,
        "As depicted in Figure 4.1, the Recruiter provides the Job Description (JD) text and customizable criteria weights. "
        "Simultaneously, Candidate Resumes in PDF and DOCX formats enter the system. Process 0.0 transforms these inputs, "
        "issuing real-time interactive shortlists and match explanations to the Recruiter, while dispatching ranked leaderboards, "
        "candidate radar analytics, CSV export files, adversarial exploit alerts, and DEI compliance certificates to the talent "
        "review team."
    )

    add_heading_3(doc, "4.2.2 DFD Level 1 (Major System Subsystems)")
    add_body_p(doc,
        "Figure 4.2 presents the DFD Level 1 decomposition, partitioning the system into four discrete sub-processes "
        "and three central data stores."
    )

    img_dfd1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diagrams", "dfd_level_1.png")
    if os.path.exists(img_dfd1):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture(img_dfd1, width=Inches(6.0))
        add_caption(doc, "Figure 4.2: Data Flow Diagram (DFD Level 1 - System Subsystems)")

    add_body_p(doc,
        "The four Level 1 processes operate as follows:"
    )
    add_bullet_p(doc, "Ingests raw PDF and DOCX documents, performs font-color and glyph-scale stream inspection to detect adversarial attacks, strips fraudulent tokens, and produces sanitized document text.", "Process 1.0 (Document Parsing & Forensics): ")
    add_bullet_p(doc, "Applies spaCy NLP pipelines for entity extraction (names, emails, phones, education, experience) and queries Data Store D1 (Canonical Skill Taxonomy) to extract and normalize technical competencies.", "Process 2.0 (Canonical Taxonomy & NLP Extraction): ")
    add_bullet_p(doc, "Receives candidate profiles from Data Store D2 and job requirements from the recruiter, evaluating candidate qualifications against requirements across five mathematical dimensions.", "Process 3.0 (Multi-Criteria Scoring & Similarity): ")
    add_bullet_p(doc, "Compiles scored candidates into ranked leaderboards, computes pool-wide triage metrics, applies blind recruitment anonymization, generates interview guides, and persists audit logs to Data Store D3.", "Process 4.0 (Ranking, DEI & Interview Kit Generator): ")

    add_heading_3(doc, "4.2.3 DFD Level 2 (Decomposition of Process 3.0 Scoring Engine)")
    add_body_p(doc,
        "Figure 4.3 illustrates the Level 2 DFD decomposition of Process 3.0 (Multi-Criteria Scoring Engine), providing a granular "
        "view of the parallel evaluation pipelines."
    )

    img_dfd2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diagrams", "dfd_level_2.png")
    if os.path.exists(img_dfd2):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture(img_dfd2, width=Inches(6.0))
        add_caption(doc, "Figure 4.3: Data Flow Diagram (DFD Level 2 - Scoring Engine Decomposition)")

    add_body_p(doc,
        "The scoring engine executes five distinct evaluation sub-processes in parallel: Sub-process 3.1 calculates the Required "
        "Skills match percentage (S_req); Sub-process 3.2 computes the Preferred / Bonus Skills match percentage (S_pref); "
        "Sub-process 3.3 computes the Experience score (S_exp) via linear threshold scaling; Sub-process 3.4 evaluates the "
        "Educational tier alignment (S_edu); and Sub-process 3.5 computes the contextual semantic cosine similarity (S_sim) "
        "using TF-IDF / SBERT vector representations. Finally, Sub-process 3.6 (Weighted Sum Aggregator) applies recruiter "
        "weights to generate the final composite score and assign the standardized match tier."
    )

    add_heading_2(doc, "4.3 Entity-Relationship (ER) Diagram & Schema Cardinality")
    add_body_p(doc,
        "Figure 4.4 presents the Entity-Relationship (ER) Diagram representing the logical data architecture of RecruMatch. "
        "The model is designed in Third Normal Form (3NF) to eliminate data redundancy, enforce referential integrity, and "
        "support audit traceability."
    )

    img_er = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diagrams", "er_diagram.png")
    if os.path.exists(img_er):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture(img_er, width=Inches(6.2))
        add_caption(doc, "Figure 4.4: Entity-Relationship Diagram (ER Diagram)")

    add_body_p(doc,
        "The relational model comprises six core entities with clear cardinalities:"
    )
    add_bullet_p(doc, "Stores recruiter credentials and departmental metadata. Has a 1:N relationship with JOB_DESCRIPTION.", "RECRUITER Entity: ")
    add_bullet_p(doc, "Captures job requirements, role titles, and minimum qualification thresholds. Has a 1:N relationship with REQUIRED_SKILL and a 1:N relationship with CANDIDATE_SCORE.", "JOB_DESCRIPTION Entity: ")
    add_bullet_p(doc, "Stores individual mandatory and preferred technical skills linked to a specific job requisition.", "REQUIRED_SKILL Entity: ")
    add_bullet_p(doc, "Represents applicant profiles extracted from ingested resumes. Maintains a 1:N relationship with EXTRACTED_SKILL, a 1:1 relationship with FORENSIC_AUDIT_LOG, and a 1:N relationship with CANDIDATE_SCORE.", "CANDIDATE_PROFILE Entity: ")
    add_bullet_p(doc, "Stores normalized canonical skills identified in a candidate's resume, including confidence scores and implicit inference flags.", "EXTRACTED_SKILL Entity: ")
    add_bullet_p(doc, "Maintains the complete mathematical breakdown of candidate evaluation against a job requisition, including sub-scores, final weighted percentage, and match tier classification.", "CANDIDATE_SCORE Entity: ")

    add_heading_2(doc, "4.4 Data Structures & Relational Table Structures")
    add_body_p(doc,
        "The following tables specify the exact physical schema, data types, constraints, and descriptions for all relational "
        "entities within the system architecture."
    )

    # Table 4.1
    add_caption(doc, "Table 4.1: Job Description Relational Table Structure (job_description)", is_table=True)
    build_table(doc, 
        ["Field Name", "Data Type", "Constraint", "Description"],
        [
            ["jd_id", "UUID", "PRIMARY KEY", "Unique identifier for each job description"],
            ["recruiter_id", "UUID", "FOREIGN KEY", "References recruiter who created the requisition"],
            ["role_title", "VARCHAR(120)", "NOT NULL", "Official job title (e.g. Senior Python & ML Engineer)"],
            ["min_experience", "FLOAT", "NOT NULL, DEFAULT 0.0", "Minimum required professional experience in years"],
            ["target_education", "VARCHAR(80)", "NOT NULL", "Minimum educational qualification requirement"],
            ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Requisition creation timestamp"],
            ["raw_text", "TEXT", "NOT NULL", "Complete unparsed raw text of the job description"]
        ],
        col_widths=[Inches(1.2), Inches(1.1), Inches(1.6), Inches(2.35)]
    )

    # Table 4.2
    add_caption(doc, "Table 4.2: Required Skill Relational Table Structure (required_skill)", is_table=True)
    build_table(doc,
        ["Field Name", "Data Type", "Constraint", "Description"],
        [
            ["req_skill_id", "UUID", "PRIMARY KEY", "Unique identifier for each required skill entry"],
            ["jd_id", "UUID", "FOREIGN KEY (job_description)", "Links required skill to its parent job requisition"],
            ["skill_name", "VARCHAR(80)", "NOT NULL", "Canonical skill name (e.g. FastAPI, Docker, SQL)"],
            ["is_mandatory", "BOOLEAN", "NOT NULL, DEFAULT TRUE", "True = Required Skill (40%), False = Preferred (15%)"],
            ["category", "VARCHAR(50)", "NOT NULL", "Skill domain (e.g. Programming, Cloud & DevOps)"],
            ["weight", "FLOAT", "DEFAULT 1.0", "Custom importance multiplier for the skill"]
        ],
        col_widths=[Inches(1.2), Inches(1.1), Inches(1.6), Inches(2.35)]
    )

    # Table 4.3
    add_caption(doc, "Table 4.3: Candidate Profile Relational Table Structure (candidate_profile)", is_table=True)
    build_table(doc,
        ["Field Name", "Data Type", "Constraint", "Description"],
        [
            ["candidate_id", "UUID", "PRIMARY KEY", "Unique identifier for each candidate profile"],
            ["full_name", "VARCHAR(120)", "NOT NULL", "Candidate extracted full name"],
            ["email", "VARCHAR(120)", "NOT NULL", "Extracted email address (masked in Blind Mode)"],
            ["phone", "VARCHAR(30)", "NULLABLE", "Extracted contact number (masked in Blind Mode)"],
            ["experience_years", "FLOAT", "NOT NULL, DEFAULT 0.0", "Total computed professional experience in years"],
            ["normalized_degree", "VARCHAR(80)", "NULLABLE", "Standardized academic degree (e.g. B.Tech, M.Tech)"],
            ["raw_text_hash", "VARCHAR(64)", "NOT NULL, UNIQUE", "SHA-256 hash of resume text to prevent duplicates"]
        ],
        col_widths=[Inches(1.2), Inches(1.1), Inches(1.6), Inches(2.35)]
    )

    # Table 4.4
    add_caption(doc, "Table 4.4: Extracted Skill Relational Table Structure (extracted_skill)", is_table=True)
    build_table(doc,
        ["Field Name", "Data Type", "Constraint", "Description"],
        [
            ["extracted_id", "UUID", "PRIMARY KEY", "Unique identifier for each extracted candidate skill"],
            ["candidate_id", "UUID", "FOREIGN KEY (candidate_profile)", "Links extracted skill to candidate profile"],
            ["canonical_name", "VARCHAR(80)", "NOT NULL", "Standardized canonical taxonomy skill name"],
            ["category", "VARCHAR(50)", "NOT NULL", "Technical domain category (e.g. Databases, AI/ML)"],
            ["is_inferred", "BOOLEAN", "DEFAULT FALSE", "True if inferred via Knowledge Graph (e.g. PyTorch->Python)"],
            ["confidence", "FLOAT", "DEFAULT 1.0", "Extraction confidence score (0.0 to 1.0)"]
        ],
        col_widths=[Inches(1.2), Inches(1.1), Inches(1.6), Inches(2.35)]
    )

    # Table 4.5
    add_caption(doc, "Table 4.5: Candidate Assessment Score Table Structure (candidate_score)", is_table=True)
    build_table(doc,
        ["Field Name", "Data Type", "Constraint", "Description"],
        [
            ["score_id", "UUID", "PRIMARY KEY", "Unique identifier for candidate evaluation instance"],
            ["candidate_id", "UUID", "FOREIGN KEY (candidate_profile)", "References evaluated candidate profile"],
            ["jd_id", "UUID", "FOREIGN KEY (job_description)", "References target job description"],
            ["final_score", "FLOAT", "NOT NULL", "Final composite score (0.0 to 100.0%)"],
            ["required_skills_pct", "FLOAT", "NOT NULL", "Required skills match percentage (S_req)"],
            ["preferred_skills_pct", "FLOAT", "NOT NULL", "Preferred skills match percentage (S_pref)"],
            ["experience_score", "FLOAT", "NOT NULL", "Experience relevance match percentage (S_exp)"],
            ["education_score", "FLOAT", "NOT NULL", "Educational qualification score (S_edu)"],
            ["semantic_similarity", "FLOAT", "NOT NULL", "TF-IDF / SBERT Cosine similarity percentage (S_sim)"],
            ["match_tier", "VARCHAR(30)", "NOT NULL", "Tier: Excellent, Good, Moderate, or Low Match"]
        ],
        col_widths=[Inches(1.2), Inches(1.1), Inches(1.6), Inches(2.35)]
    )

    # Table 4.6
    add_caption(doc, "Table 4.6: Forensic Audit Log Relational Table Structure (forensic_audit_log)", is_table=True)
    build_table(doc,
        ["Field Name", "Data Type", "Constraint", "Description"],
        [
            ["audit_id", "UUID", "PRIMARY KEY", "Unique identifier for each PDF forensic inspection"],
            ["candidate_id", "UUID", "FOREIGN KEY (candidate_profile)", "Links audit record to candidate resume"],
            ["fraud_score", "FLOAT", "NOT NULL, DEFAULT 0.0", "Composite fraud risk score calibrated from 0 to 100"],
            ["white_text_count", "INT", "DEFAULT 0", "Number of hidden white (#FFFFFF) text spans detected"],
            ["micro_font_count", "INT", "DEFAULT 0", "Number of sub-readable micro-font (<2.0 pt) tokens"],
            ["homoglyph_count", "INT", "DEFAULT 0", "Number of Cyrillic/Greek spoofed characters found"],
            ["risk_level", "VARCHAR(20)", "NOT NULL", "Risk Tier: Clean, Low, Moderate, High, or Critical"]
        ],
        col_widths=[Inches(1.2), Inches(1.1), Inches(1.6), Inches(2.35)]
    )

    doc.add_page_break()

def add_chapter_5_proposed_system(doc):
    add_heading_1(doc, "CHAPTER 5: PROPOSED SYSTEM & CORE ALGORITHMIC ENGINES")
    
    add_heading_2(doc, "5.1 System Overview & Architectural Paradigm Shift")
    add_body_p(doc,
        "RecruMatch introduces a paradigm shift in automated talent acquisition by bridging the divide between brittle "
        "first-generation keyword filters and opaque, stochastic large language models. The system is designed upon three "
        "foundational engineering pillars: (1) Total Algorithmic Explainability, (2) Active Cyber-Resilience against Adversarial "
        "Resume Exploits, and (3) Ethical AI Compliance via Dynamic Demographic Anonymization."
    )

    add_heading_2(doc, "5.2 4-Tier High-Level System Architecture")
    add_body_p(doc,
        "The architecture of RecruMatch is organized into four clean, loosely-coupled layers, as illustrated in Figure 5.1."
    )

    img_arch = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diagrams", "system_architecture.png")
    if os.path.exists(img_arch):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        r = p_img.add_run()
        r.add_picture(img_arch, width=Inches(6.0))
        add_caption(doc, "Figure 5.1: RecruMatch 4-Tier High-Level System Architecture")

    add_body_p(doc,
        "The four tiers operate cooperatively across the application lifecycle:"
    )
    add_bullet_p(doc, "Comprises the reactive Streamlit Web UI (assets/style.css, custom SaaS dark mode) with interactive Plotly radar charts, applicant pool KPI cards, and dynamic weight sliders, alongside a standalone FastAPI REST backend server providing interactive OpenAPI / Swagger UI documentation at /docs.", "Tier 1: Presentation & User Interface Layer: ")
    add_bullet_p(doc, "Acts as an impenetrable security boundary before text parsing occurs. Utilizes PyMuPDF C-level stream extractors to inspect RGB color channels, glyph bounding boxes, font sizes, and Unicode codepoints, actively neutralizing white text, micro-fonts, homoglyph character substitutions, and prompt injection attempts.", "Tier 2: Security & Forensic Pre-Flight Shield: ")
    add_bullet_p(doc, "Houses core algorithmic intelligence: pdfplumber and python-docx text extractors; spaCy en_core_web_sm entity parser; a 130+ term canonical skill taxonomy; an implicit skill knowledge graph; dual vectorization engines (TF-IDF Cosine Similarity and Sentence-BERT); a career velocity analyzer; and the explainable multi-criteria scoring algorithm.", "Tier 3: Core AI, NLP & Scoring Engine Layer: ")
    add_bullet_p(doc, "Manages benchmark job description templates, applicant profile records, the blind recruitment PII scrubber, and report export engines generating audit-ready CSV, Markdown, and DEI fairness compliance documentation.", "Tier 4: Data, Storage & Reporting Layer: ")

    add_heading_2(doc, "5.3 Core Algorithmic Engines")
    add_body_p(doc,
        "RecruMatch incorporates eight specialized algorithmic subsystems engineered to ensure precision, transparency, "
        "and security."
    )

    add_heading_3(doc, "5.3.1 Multi-Format Document Ingestion & Parsing Engine")
    add_body_p(doc,
        "The ingestion layer reliably processes heterogeneous resume formats. For PDF files, the system employs pdfplumber "
        "with an automated fallback to PyMuPDF (fitz), extracting structured layout text while preserving word boundaries. "
        "For DOCX files, python-docx navigates the underlying WordprocessingML XML tree, recursively extracting text from "
        "standard body paragraphs, table cells, and bulleted lists. Robust exception isolation ensures that malformed or "
        "password-protected documents generate descriptive error notifications without halting batch processing."
    )

    add_heading_3(doc, "5.3.2 Resume Forensic Inspector & Adversarial ATS Shield")
    add_body_p(doc,
        "The Forensic Inspector (forensic_inspector.py) performs pre-flight threat detection directly upon PDF rendering streams:"
    )
    add_bullet_p(doc, "Extracts character fill color triples (R, G, B). A text span is flagged as hidden white text if R > 0.98, G > 0.98, and B > 0.98, or if the color matches the document page background. In standard ATS parsers, these invisible strings trigger fraudulent keyword matches; RecruMatch captures and isolates them.", "1. Hidden White Text Detection: ")
    add_bullet_p(doc, "Extracts the font point size for each rendered text span. Any text rendered at fontsize < 2.0 pt is flagged as micro-font stacking.", "2. Micro-Font Stacking Detection: ")
    add_bullet_p(doc, "Scans Unicode codepoint ranges. Detects Cyrillic and Greek characters embedded inside predominantly Latin words (e.g. Cyrillic 'а' U+0430 inside 'FastAPI'). Normalizes spoofed characters to canonical ASCII equivalents.", "3. Homoglyph Spoofing Detection: ")
    add_bullet_p(doc, "Identifies and strips zero-width non-joiners and format characters (U+200B to U+200D, U+FEFF) utilized to break word boundaries and deceive regex scanners.", "4. Zero-Width Space Stripping: ")
    add_bullet_p(doc, "Computes a calibrated Fraud Score from 0 to 100 based on detected adversarial anomalies, categorizing resumes into Clean, Low, Moderate, High, or Critical risk tiers, and outputs a sanitized text stream.", "5. Automated Text Sanitization: ")

    add_heading_3(doc, "5.3.3 Canonical Skill Taxonomy & Synonym Normalization")
    add_body_p(doc,
        "To eliminate the brittleness of exact keyword matching, RecruMatch maintains a centralized taxonomy "
        "(src/skill_dictionary.py) containing over 130+ technical skills categorized into 9 distinct domains:"
    )
    add_bullet_p(doc, "Python, Java, C++, JavaScript, TypeScript, Go, Rust, C#, PHP, Ruby, Kotlin, Swift, Scala, R, Dart, Julia, Shell, Bash, PowerShell.", "1. Programming Languages: ")
    add_bullet_p(doc, "React, Next.js, Angular, Vue.js, Node.js, Express.js, Django, FastAPI, Flask, Spring Boot, HTML, CSS, Tailwind CSS, Bootstrap, GraphQL, REST API.", "2. Web & Frameworks: ")
    add_bullet_p(doc, "Machine Learning, Deep Learning, Natural Language Processing, Computer Vision, Scikit-learn, TensorFlow, PyTorch, Keras, Pandas, NumPy, spaCy, Hugging Face, LLMs, LangChain.", "3. Data & AI: ")
    add_bullet_p(doc, "PostgreSQL, MySQL, MongoDB, Redis, SQLite, Oracle, Cassandra, Elasticsearch, DynamoDB, SQL, NoSQL.", "4. Databases: ")
    add_bullet_p(doc, "AWS, Azure, Google Cloud, Docker, Kubernetes, Terraform, Ansible, Jenkins, CI/CD, Linux, Nginx, Prometheus, Grafana.", "5. Cloud & DevOps: ")
    add_bullet_p(doc, "Git, GitHub, GitLab, JIRA, Postman, Linux, VS Code, Agile, Scrum.", "6. Tools & Methodologies: ")

    add_body_p(doc,
        "Every taxonomy entry maintains an exhaustive synonym dictionary mapping informal aliases to canonical names "
        "(e.g., 'ML' -> 'Machine Learning', 'JS' -> 'JavaScript', 'Postgres' -> 'PostgreSQL', 'K8s' -> 'Kubernetes', "
        "'Fast API' -> 'FastAPI', 'Amazon Web Services' -> 'AWS')."
    )

    # Table 5.1: Canonical Skill Taxonomy
    add_caption(doc, "Table 5.1: Canonical Technical Skill Taxonomy (Sample Across 9 Domains)", is_table=True)
    build_table(doc,
        ["Technical Domain", "Canonical Standard", "Synonyms & Aliases Resolved", "Example Normalized Extraction"],
        [
            ["Programming Languages", "Python", "py, python3, cpython, python 3.x", "Candidate writing 'Python3' -> Python"],
            ["Web & Microservices", "FastAPI", "fast api, fast-api, tiangolo fastapi", "Candidate writing 'fast-api' -> FastAPI"],
            ["Web & Microservices", "Django", "django framework, django rest", "Candidate writing 'Django REST' -> Django"],
            ["Data & AI", "Machine Learning", "ml, statistical learning, auto-ml", "Candidate writing 'ML algorithms' -> Machine Learning"],
            ["Data & AI", "PyTorch", "torch, pytorch deep learning", "Candidate writing 'torch' -> PyTorch"],
            ["Databases & Storage", "PostgreSQL", "postgres, pgsql, postgre, postgresql 15", "Candidate writing 'Postgres' -> PostgreSQL"],
            ["Cloud & Containers", "Kubernetes", "k8s, kube, kubectl, k8 clusters", "Candidate writing 'K8s' -> Kubernetes"],
            ["Cloud Infrastructure", "AWS", "amazon web services, aws cloud, ec2/s3", "Candidate writing 'Amazon Web Services' -> AWS"],
            ["DevOps & Pipeline", "CI/CD", "continuous integration, continuous deployment, cicd", "Candidate writing 'CI/CD pipelines' -> CI/CD"]
        ],
        col_widths=[Inches(1.5), Inches(1.3), Inches(2.0), Inches(1.45)]
    )

    add_heading_3(doc, "5.3.4 Skill Knowledge Graph & Implicit Competency Engine")
    add_body_p(doc,
        "RecruMatch incorporates a directed acyclic knowledge graph (src/skill_graph.py) modeling hierarchical relationships "
        "between technical competencies. Senior software professionals frequently omit basic prerequisite skills from their "
        "resumes. The inference engine models implicit parent dependencies: if a candidate explicitly demonstrates mastery of "
        "'PyTorch', the graph automatically infers 'Python' with a confidence weight of 0.90; 'Kubernetes' infers 'Docker' "
        "(0.85); 'React' or 'Next.js' infers 'JavaScript' (0.95); and 'Django' or 'FastAPI' infers 'Python' and 'REST API'. "
        "This prevents penalizing experienced candidates who focus their resume space on advanced architectural achievements."
    )

    add_heading_3(doc, "5.3.5 Career Velocity & Trajectory Assessment Model")
    add_body_p(doc,
        "Beyond static keyword counts, RecruMatch evaluates candidate career momentum (src/career_velocity.py). By parsing "
        "historical employment titles, promotion cadences, and company tenures, the model categorizes applicants into "
        "actionable career trajectory tiers: (1) High Velocity (rapid promotions and accelerated leadership progression), "
        "(2) Steady Progression (consistent career growth with stable multi-year tenures), and (3) Emerging Talent (high-potential "
        "early-career professionals demonstrating rapid skill acquisition)."
    )

    add_heading_3(doc, "5.3.6 Explainable Multi-Criteria Scoring Mathematical Formulation")
    add_body_p(doc,
        "The scoring engine (src/scorer.py) rejects opaque machine learning weights in favor of an auditable, transparent "
        "mathematical formulation. The Final Composite Match Score is computed as a normalized convex combination of five "
        "constituent sub-scores:"
    )

    add_code_block(doc, 
        "Final Score = w_req * S_req + w_pref * S_pref + w_exp * S_exp + w_edu * S_edu + w_sim * S_sim\n\n"
        "Constraint: w_req + w_pref + w_exp + w_edu + w_sim = 1.0\n"
        "Default Enterprise Weights:\n"
        "  - w_req  = 0.40  (Required Skills: 40%)\n"
        "  - w_pref = 0.15  (Preferred / Bonus Skills: 15%)\n"
        "  - w_exp  = 0.15  (Experience Relevance: 15%)\n"
        "  - w_edu  = 0.10  (Educational Qualification: 10%)\n"
        "  - w_sim  = 0.20  (Contextual Semantic Similarity: 20%)",
        "Mathematical Equation 5.1: Explainable Multi-Criteria Scoring Formulation"
    )

    add_body_p(doc,
        "The mathematical formulation of each constituent sub-score is defined as follows:"
    )
    add_bullet_p(doc, "Calculated as the cardinality of the intersection between candidate skills and mandatory job requirements divided by the total number of mandatory job requirements: S_req = (|Skills_cand ∩ Req_skills|) / |Req_skills|.", "1. Required Skills Match (S_req): ")
    add_bullet_p(doc, "Calculated as the proportion of preferred bonus skills matched: S_pref = (|Skills_cand ∩ Pref_skills|) / |Pref_skills|. If no preferred skills are specified in the requisition, S_pref defaults to 1.0 (100%).", "2. Preferred Skills Match (S_pref): ")
    add_bullet_p(doc, "Evaluated via a piecewise linear threshold function against the minimum required experience (E_min): If E_cand >= E_min, S_exp = 1.0. If E_cand < E_min, S_exp = E_cand / E_min.", "3. Experience Relevance Score (S_exp): ")
    add_bullet_p(doc, "Evaluated against a standardized academic hierarchy: Ph.D. (1.0), Master's (M.Tech/M.S./MCA: 0.90), Bachelor's (B.Tech/B.E./BCA: 0.75), and Diploma/Others (0.50). If E_cand_degree satisfies or exceeds the job requirement, S_edu = 1.0; otherwise, proportional credit is assigned.", "4. Educational Qualification Score (S_edu): ")
    add_bullet_p(doc, "Computed as the normalized cosine similarity between the TF-IDF vector representations of the candidate resume text (v_cand) and the job description (v_jd): S_sim = (v_cand · v_jd) / (||v_cand|| * ||v_jd||).", "5. Contextual Semantic Similarity (S_sim): ")

    add_body_p(doc,
        "Candidates are subsequently categorized into four standardized, actionable match tiers based on Final Score:"
    )
    add_bullet_p(doc, "Final Score >= 80.0%. Exceptional qualification alignment; immediate technical interview recommended.", "🟢 Excellent Match: ")
    add_bullet_p(doc, "60.0% <= Final Score < 80.0%. Strong candidate alignment; minor qualification gaps to probe in interviews.", "🔵 Good Match: ")
    add_bullet_p(doc, "40.0% <= Final Score < 60.0%. Partial qualification alignment; suitable for backup pools or alternative requisitions.", "🟡 Moderate Match: ")
    add_bullet_p(doc, "Final Score < 40.0%. Substantial qualification deficiencies relative to mandatory role criteria.", "🔴 Low Match: ")

    add_heading_3(doc, "5.3.7 Blind Recruitment & Ethical AI Anonymizer")
    add_body_p(doc,
        "To enforce meritocratic hiring, the Blind Recruitment module (src/anonymizer.py) provides a single-click toggle "
        "in the dashboard. When activated, candidate names are replaced with cryptographic tokens (e.g., 'Candidate #1 "
        "[Token: a8f9c2]'), phone numbers and email addresses are securely redacted, and institutional academic names "
        "(e.g., 'IIT Delhi' or 'State Technical College') are normalized into generic degree designations (e.g., 'Bachelor of "
        "Technology in Computer Science'). The module generates an exportable DEI Fairness Compliance Certificate, verifying "
        "that initial screening decisions occurred in the complete absence of demographic or institutional prestige markers."
    )

    add_heading_3(doc, "5.3.8 Dynamic Technical Interview Kit Generator")
    add_body_p(doc,
        "The interview kit engine (src/interview_generator.py) automatically generates an individualized technical assessment "
        "guide for each candidate. The kit generates three specialized question categories: (1) Skill Verification Questions "
        "(in-depth inquiries probing claimed core competencies, such as connection pooling in PostgreSQL or concurrency handling "
        "in FastAPI), (2) Qualification Gap Questions (targeted technical questions addressing missing requirements from the JD), "
        "and (3) Seniority & Architecture Questions (evaluating system scalability, trade-off analysis, and mentoring ability based "
        "on the candidate's career velocity)."
    )
    doc.add_page_break()

print("Chapters 4 and 5 module configured.")
