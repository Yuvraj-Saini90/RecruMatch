"""Preliminary Pages for B.Tech Mini Project Report:
- Cover / Title Page (matching GNIOT/AKTU exact format)
- Certificate of Authenticity
- Candidate's Declaration
- Acknowledgement
- Abstract (Executive Summary)
- Index / Table of Contents (Dynamic, accurate page numbers)
- List of Figures & List of Tables
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from build_full_report import set_cell_background, set_cell_margins, set_cell_borders

def add_title_page(doc):
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.space_before = Pt(8)
    p_top.paragraph_format.space_after = Pt(12)
    p_top.paragraph_format.line_spacing = 1.25
    
    r_title = p_top.add_run("RECRUMATCH: INTELLIGENT RESUME SCREENING AND CANDIDATE RANKING SYSTEM\n")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(16.5)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0, 0, 0)
    
    r_sub = p_top.add_run("A Mini Project Report\n")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(13)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0, 0, 0)

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_before = Pt(4)
    p_by.paragraph_format.space_after = Pt(4)
    r_by = p_by.add_run("Submitted By\n")
    r_by.font.name = "Times New Roman"
    r_by.font.size = Pt(12)
    r_by.font.italic = True
    
    r_sname = p_by.add_run("YUVRAJ SAINI\n(University Roll No: [____________________])")
    r_sname.font.name = "Times New Roman"
    r_sname.font.size = Pt(13)
    r_sname.font.bold = True
    r_sname.font.color.rgb = RGBColor(0, 0, 0)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(8)
    p_sub.paragraph_format.space_after = Pt(8)
    p_sub.paragraph_format.line_spacing = 1.25
    
    lines_sub = [
        ("Submitted to the Department of Computer Science & Engineering\n", 12, False),
        ("In partial fulfillment of the requirements\n", 12, False),
        ("For the degree of\n", 12, False),
        ("BACHELOR OF TECHNOLOGY\n", 14, True),
        ("In\nComputer Science & Engineering\n", 12, False),
        ("\nUnder the Supervision of:\n", 12, False),
        ("Mr. Ashwini Kr. Verma\nAssistant Professor, Department of Computer Science & Engineering", 12.5, True)
    ]
    for text, sz, bld in lines_sub:
        r = p_sub.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(sz)
        r.font.bold = bld

    # GNIOT Logo
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "diagrams", "gniot_logo.jpg")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(6)
        p_logo.paragraph_format.space_after = Pt(6)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(2.2))

    # University Footer
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(8)
    p_foot.paragraph_format.space_after = Pt(0)
    p_foot.paragraph_format.line_spacing = 1.25
    
    r_inst = p_foot.add_run("Greater Noida Institute of Technology, Greater Noida\n")
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(13.5)
    r_inst.font.bold = True
    
    r_univ = p_foot.add_run("Dr. A.P.J. Abdul Kalam Technical University, Lucknow\n")
    r_univ.font.name = "Times New Roman"
    r_univ.font.size = Pt(15)
    r_univ.font.bold = True
    
    r_date = p_foot.add_run("October 2026")
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(12)
    r_date.font.bold = False

    doc.add_page_break()

def add_certificate_page(doc):
    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert.paragraph_format.space_before = Pt(18)
    p_cert.paragraph_format.space_after = Pt(18)
    r_c = p_cert.add_run("CERTIFICATE")
    r_c.font.name = "Times New Roman"
    r_c.font.size = Pt(16)
    r_c.font.bold = True
    r_c.underline = True

    p_body = doc.add_paragraph()
    p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_body.paragraph_format.space_before = Pt(12)
    p_body.paragraph_format.space_after = Pt(14)
    p_body.paragraph_format.line_spacing = 2.0
    
    text = (
        "This is to certify that the Mini Project Report entitled \"RECRUMATCH: INTELLIGENT RESUME "
        "SCREENING AND CANDIDATE RANKING SYSTEM\" submitted by Yuvraj Saini (University Roll No: "
        "[____________________]) in partial fulfillment of the requirements for the award of the degree "
        "of Bachelor of Technology in Computer Science & Engineering from Dr. A.P.J. Abdul Kalam Technical "
        "University, Lucknow, is an authentic record of bonafide academic work carried out under my "
        "supervision and guidance during the academic session 2026–2027.\n\n"
        "To the best of my knowledge, the matter embodied in this report has not been submitted to any "
        "other University or Institute for the award of any degree or diploma."
    )
    r = p_body.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    # Signatures Table
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(36)
    
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    c1 = table.cell(0, 0)
    c1.width = Inches(3.2)
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p1.paragraph_format.line_spacing = 1.3
    r1 = p1.add_run(
        "_____________________________\n"
        "(Supervisor / Guide Signature)\n"
        "Mr. Ashwini Kr. Verma\n"
        "Assistant Professor\n"
        "Department of Computer Science & Engg.\n"
        "GNIOT, Greater Noida"
    )
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r1.font.bold = True

    c2 = table.cell(0, 1)
    c2.width = Inches(3.2)
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.paragraph_format.line_spacing = 1.3
    r2 = p2.add_run(
        "_____________________________\n"
        "(Head of Department Signature)\n"
        "[Head of Department Name]\n"
        "Head, Dept. of Computer Science & Engg.\n"
        "GNIOT, Greater Noida\n"
        "Date: October 2026"
    )
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(11)
    r2.font.bold = True

    doc.add_page_break()

def add_declaration_page(doc):
    p_dec = doc.add_paragraph()
    p_dec.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dec.paragraph_format.space_before = Pt(18)
    p_dec.paragraph_format.space_after = Pt(18)
    r_d = p_dec.add_run("CANDIDATE'S DECLARATION")
    r_d.font.name = "Times New Roman"
    r_d.font.size = Pt(16)
    r_d.font.bold = True
    r_d.underline = True

    p_body = doc.add_paragraph()
    p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_body.paragraph_format.space_before = Pt(12)
    p_body.paragraph_format.space_after = Pt(14)
    p_body.paragraph_format.line_spacing = 2.0
    
    text = (
        "I hereby declare that the work presented in this Mini Project Report entitled "
        "\"RECRUMATCH: INTELLIGENT RESUME SCREENING AND CANDIDATE RANKING SYSTEM\" in partial "
        "fulfillment of the requirements for the award of the degree of Bachelor of Technology in "
        "Computer Science & Engineering submitted to Greater Noida Institute of Technology, Greater "
        "Noida, affiliated with Dr. A.P.J. Abdul Kalam Technical University, Lucknow, is an authentic "
        "record of my own work carried out under the supervision of Mr. Ashwini Kr. Verma, "
        "Assistant Professor, Department of Computer Science & Engineering.\n\n"
        "I have not submitted the embodied matter herein for the award of any other degree or diploma "
        "elsewhere. All sources of code, algorithms, published literature, and academic resources utilized "
        "in the development of this project have been duly acknowledged."
    )
    r = p_body.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(40)
    p_sig.paragraph_format.space_after = Pt(0)
    p_sig.paragraph_format.line_spacing = 1.3
    
    r_sig = p_sig.add_run(
        "_____________________________\n"
        "(Candidate Signature)\n\n"
        "Yuvraj Saini\n"
        "University Roll No.: [____________________]\n"
        "Branch: Computer Science & Engineering\n"
        "Greater Noida Institute of Technology\n"
        "Date: October 2026\n"
        "Place: Greater Noida"
    )
    r_sig.font.name = "Times New Roman"
    r_sig.font.size = Pt(11)
    r_sig.font.bold = True

    doc.add_page_break()

def add_acknowledgement_page(doc):
    p_ack = doc.add_paragraph()
    p_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack.paragraph_format.space_before = Pt(18)
    p_ack.paragraph_format.space_after = Pt(18)
    r_a = p_ack.add_run("ACKNOWLEDGEMENT")
    r_a.font.name = "Times New Roman"
    r_a.font.size = Pt(16)
    r_a.font.bold = True
    r_a.underline = True

    paragraphs = [
        "I would like to express my deepest and most sincere gratitude to my esteemed project guide, "
        "Mr. Ashwini Kr. Verma, Assistant Professor, Department of Computer Science & Engineering, Greater "
        "Noida Institute of Technology, Greater Noida, for his invaluable guidance, constant encouragement, "
        "and critical academic insights throughout the conception, architectural design, and implementation "
        "of this project. His domain expertise in Natural Language Processing and software architecture has "
        "been instrumental in bringing this work to fruition.",
        
        "I extend my sincere appreciation to the Head of the Department of Computer Science & Engineering, "
        "for providing continuous administrative support, access to high-performance computing laboratories, "
        "and creating an intellectually stimulating environment conducive to research.",
        
        "I am profoundly grateful to the Director, Greater Noida Institute of Technology, for fostering an "
        "institution dedicated to academic excellence, state-of-the-art technical infrastructure, and "
        "industry-aligned project initiatives.",
        
        "Special thanks are also due to the faculty members, technical laboratory assistants, and staff of "
        "the Department of Computer Science & Engineering for their co-operation, constructive feedback during "
        "interim evaluations, and timely guidance.",
        
        "Finally, I express my heartfelt gratitude to my family and friends for their enduring patience, "
        "moral support, and encouragement during the course of this project."
    ]

    for para in paragraphs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 2.0
        r = p.add_run(para)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    p_end = doc.add_paragraph()
    p_end.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_end.paragraph_format.space_before = Pt(24)
    p_end.paragraph_format.space_after = Pt(0)
    p_end.paragraph_format.line_spacing = 1.3
    
    r_end = p_end.add_run(
        "Yuvraj Saini\n"
        "University Roll No.: [____________________]\n"
        "Department of Computer Science & Engineering\n"
        "Greater Noida Institute of Technology, Greater Noida"
    )
    r_end.font.name = "Times New Roman"
    r_end.font.size = Pt(11)
    r_end.font.bold = True

    doc.add_page_break()

def add_abstract_page(doc):
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs.paragraph_format.space_before = Pt(18)
    p_abs.paragraph_format.space_after = Pt(18)
    r_ab = p_abs.add_run("ABSTRACT")
    r_ab.font.name = "Times New Roman"
    r_ab.font.size = Pt(16)
    r_ab.font.bold = True
    r_ab.underline = True

    abstract_paras = [
        "In contemporary technical recruitment, talent acquisition teams routinely receive hundreds to thousands of "
        "unstructured resumes for each open requisition. Manual resume screening is painfully slow, susceptible to recruiter "
        "fatigue, and deeply vulnerable to unconscious demographic bias. At the same time, existing commercial Applicant "
        "Tracking Systems (ATS) suffer from severe limitations: brittle keyword search algorithms that reject qualified candidates "
        "using synonyms, opaque black-box machine learning scores that lack actionable rationale, high recurring cloud API "
        "subscription costs, and alarming security vulnerabilities to adversarial PDF manipulations such as invisible white-text "
        "keyword stuffing, sub-readable micro-fonts, and Unicode homoglyph spoofing.",
        
        "This project presents RecruMatch, an intelligent, explainable, and cyber-resilient resume screening and candidate "
        "ranking system engineered to address these challenges comprehensively. RecruMatch combines robust multi-format document "
        "ingestion (PDF and DOCX), an integrated pre-flight PDF stream forensic analyzer, a centralized canonical skill taxonomy "
        "normalizing over 130+ technical skills across 9 domains, an implicit skill knowledge graph, and a transparent multi-criteria "
        "scoring algorithm evaluated across five mathematical dimensions: Required Skills (40%), Preferred Skills (15%), Experience "
        "Relevance (15%), Education Alignment (10%), and Semantic Contextual Cosine Similarity (20%). Crucially, the system features "
        "a one-click Blind Recruitment Mode that dynamically masks candidate Personally Identifiable Information (PII) and institutional "
        "pedigree to enforce meritocratic hiring, alongside an automated dynamic technical interview kit generator.",
        
        "RecruMatch delivers dual interfaces: an interactive, responsive Streamlit recruiter dashboard featuring 5-axis competency "
        "radar charts, pool triage KPIs, and forensic alert diff viewers, alongside a standalone FastAPI REST backend server. "
        "Empirical benchmarks demonstrate that the system processes candidate resumes in an average of 381.9 milliseconds on a single "
        "standard CPU core, achieves a 100% detection rate against adversarial white-text exploits, operates 100% offline with zero cloud "
        "API fees, and strictly adheres to a Human-in-the-Loop paradigm ensuring complete compliance with global ethical AI standards."
    ]

    for para in abstract_paras:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 2.0
        r = p.add_run(para)
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.space_before = Pt(10)
    p_kw.paragraph_format.space_after = Pt(0)
    p_kw.paragraph_format.line_spacing = 1.3
    
    r_kwh = p_kw.add_run("Keywords: ")
    r_kwh.font.name = "Times New Roman"
    r_kwh.font.size = Pt(11.5)
    r_kwh.font.bold = True
    
    r_kwt = p_kw.add_run("Resume Screening, Applicant Tracking System (ATS), Natural Language Processing, Canonical Skill Taxonomy, Explainable AI, Adversarial PDF Defense, White-Text Detection, Blind Recruitment, Streamlit, FastAPI.")
    r_kwt.font.name = "Times New Roman"
    r_kwt.font.size = Pt(11)
    r_kwt.font.italic = True

    doc.add_page_break()

def get_default_toc_items():
    return [
        ("Certificate of Authenticity", "ii"),
        ("Candidate's Declaration", "iii"),
        ("Acknowledgement", "iv"),
        ("Abstract", "v"),
        ("List of Figures", "viii"),
        ("List of Tables", "ix"),
        ("CHAPTER 1: INTRODUCTION / AIMS AND OBJECTIVE", "1"),
        ("   1.1 Background of Technical Recruitment & Talent Acquisition", "1"),
        ("   1.2 Challenges in Current Hiring Workflows: High Volume & Resume Fatigue", "2"),
        ("   1.3 Critical Vulnerabilities in Legacy Keyword ATS Systems", "3"),
        ("   1.4 The Emergence of Adversarial Exploits (White Text, Micro-Fonts, Homoglyphs)", "4"),
        ("   1.5 Problem Statement", "5"),
        ("   1.6 Project Objectives (Functional, Technical & Ethical)", "6"),
        ("   1.7 Scope and Significance of the Work", "7"),
        ("CHAPTER 2: SYSTEM ANALYSIS", "8"),
        ("   2.1 Identification of Need", "8"),
        ("       2.1.1 Industry Recruitment Inefficiencies & Recruiter Fatigue", "8"),
        ("       2.1.2 The High Cost of Mishires & False Positives", "9"),
        ("       2.1.3 Need for Explainable, Multi-Criteria Scoring (vs. Black-Box AI)", "10"),
        ("       2.1.4 Need for Ethical AI, Diversity & Unconscious Bias Mitigation", "11"),
        ("       2.1.5 Need for Cyber-Resilient ATS & Adversarial Text Defense", "12"),
        ("   2.2 Preliminary Investigation", "13"),
        ("       2.2.1 Survey of Existing Recruitment Platforms & Commercial ATS", "13"),
        ("       2.2.2 Comparative Limitations of Existing Solutions", "14"),
        ("       2.2.3 Feasibility of Local Offline Processing vs. Cloud APIs", "15"),
        ("       2.2.4 User Profile & Stakeholder Needs", "16"),
        ("CHAPTER 3: FEASIBILITY STUDY", "17"),
        ("   3.1 Technical Feasibility", "17"),
        ("       3.1.1 Natural Language Processing & Document Extraction Toolchain", "17"),
        ("       3.1.2 Computational Complexity & Local Hardware Sizing", "18"),
        ("       3.1.3 Scalability & Performance Benchmarks", "19"),
        ("   3.2 Economic Feasibility", "20"),
        ("       3.2.1 Capital & Operational Expenditure Analysis (Zero Cloud API Fees)", "20"),
        ("       3.2.2 ROI and Cost-Benefit Analysis for Enterprise Deployments", "21"),
        ("       3.2.3 Time Savings & Productivity Valuation", "22"),
        ("   3.3 Operational Feasibility", "23"),
        ("       3.3.1 User Acceptance & Workflow Integration (Human-in-the-Loop)", "23"),
        ("       3.3.2 Training & Maintainability Requirements", "24"),
        ("       3.3.3 Legal, Regulatory & DEI Compliance (EEOC, GDPR, Ethical AI)", "25"),
        ("CHAPTER 4: SYSTEM SPECIFICATIONS & ARCHITECTURAL MODELING", "26"),
        ("   4.1 Detailed Requirement Specifications", "26"),
        ("   4.2 Data Flow Diagrams (DFD)", "28"),
        ("       4.2.1 DFD Level 0 (Context Level Diagram)", "28"),
        ("       4.2.2 DFD Level 1 (Major System Subsystems)", "29"),
        ("       4.2.3 DFD Level 2 (Decomposition of Process 3.0 Scoring Engine)", "31"),
        ("   4.3 Entity-Relationship (ER) Diagram & Schema Cardinality", "32"),
        ("   4.4 Data Structures & Relational Table Structures", "34"),
        ("CHAPTER 5: PROPOSED SYSTEM & CORE ALGORITHMIC ENGINES", "37"),
        ("   5.1 System Overview & Architectural Paradigm Shift", "37"),
        ("   5.2 4-Tier High-Level System Architecture", "37"),
        ("   5.3 Core Algorithmic Engines", "39"),
        ("       5.3.1 Multi-Format Document Ingestion & Parsing Engine", "39"),
        ("       5.3.2 Resume Forensic Inspector & Adversarial ATS Shield", "40"),
        ("       5.3.3 Canonical Skill Taxonomy & Synonym Normalization", "41"),
        ("       5.3.4 Skill Knowledge Graph & Implicit Competency Engine", "43"),
        ("       5.3.5 Career Velocity & Trajectory Assessment Model", "44"),
        ("       5.3.6 Explainable Multi-Criteria Scoring Mathematical Formulation", "45"),
        ("       5.3.7 Blind Recruitment & Ethical AI Anonymizer", "47"),
        ("       5.3.8 Dynamic Technical Interview Kit Generator", "48"),
        ("CHAPTER 6: SYSTEM USER INTERFACE & SCREENSHOTS", "50"),
        ("   6.1 Recruiter Analytics & Applicant Pool Triage Dashboard", "50"),
        ("   6.2 Candidate Ranking Leaderboard & Multi-Criteria Filtering", "51"),
        ("   6.3 Candidate Deep Dive, 5-Axis Radar Chart & Skill Gap Analysis", "52"),
        ("   6.4 Resume Forensic Exploit Inspector & Adversarial Console", "53"),
        ("CHAPTER 7: MODULAR SYSTEM CODING & IMPLEMENTATION", "54"),
        ("   7.1 Multi-Format Document Text Extraction", "54"),
        ("   7.2 Adversarial PDF Forensic Detection Engine", "55"),
        ("   7.3 Canonical Skill Extraction & Synonym Mapping", "57"),
        ("   7.4 Skill Knowledge Graph & Implicit Competencies", "58"),
        ("   7.5 Explainable Multi-Criteria Scoring Algorithm", "59"),
        ("   7.6 Blind Recruitment & DEI PII Anonymizer", "60"),
        ("   7.7 FastAPI REST API Server Implementation", "61"),
        ("CHAPTER 8: EXPERIMENTAL RESULTS & PERFORMANCE BENCHMARKING", "62"),
        ("   8.1 Experimental Setup & Evaluation Environment", "62"),
        ("   8.2 Benchmark Test Dataset", "63"),
        ("   8.3 Comprehensive Experimental Results & Candidate Scoring Breakdown", "64"),
        ("   8.4 Comparative Performance Analysis (RecruMatch vs. Legacy ATS vs. LLM)", "65"),
        ("   8.5 Adversarial Exploit Detection Efficacy Evaluation", "66"),
        ("   8.6 Latency & Computational Throughput Benchmarking", "67"),
        ("   8.7 DEI Anonymization Impact & Fairness Evaluation", "68"),
        ("CHAPTER 9: CONCLUSION & FUTURE SCOPE", "69"),
        ("   9.1 Project Summary & Achievements", "69"),
        ("   9.2 Limitations of the Current Implementation", "70"),
        ("   9.3 Future Scope & Engineering Roadmap", "71"),
        ("CHAPTER 10: REFERENCES & TECHNICAL GLOSSARY", "72"),
        ("   10.1 Academic & Technical References (IEEE Format)", "72"),
        ("   10.2 Technical Glossary", "74")
    ]

def add_index_pages(doc, custom_toc=None):
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc.paragraph_format.space_before = Pt(18)
    p_toc.paragraph_format.space_after = Pt(16)
    r_t = p_toc.add_run("INDEX / TABLE OF CONTENTS")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(16)
    r_t.font.bold = True
    r_t.underline = True

    toc_items = custom_toc if custom_toc else get_default_toc_items()

    table_toc = doc.add_table(rows=len(toc_items) + 1, cols=3)
    table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_toc.autofit = False
    
    col_w = [Inches(0.8), Inches(4.7), Inches(0.9)]
    
    hdr = table_toc.rows[0]
    for idx, (cell, w, txt) in enumerate(zip(hdr.cells, col_w, ["S.No.", "Topic / Section Title", "Page No."])):
        cell.width = w
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    sno_counter = 1
    for r_idx, (title, page) in enumerate(toc_items):
        row = table_toc.rows[r_idx + 1]
        bg = "FFFFFF" if r_idx % 2 == 0 else "F8FAFC"
        
        # S.No logic
        is_sub = title.startswith("   ")
        is_chap = title.startswith("CHAPTER")
        if is_chap or (not is_sub and title in ["Certificate of Authenticity", "Candidate's Declaration", "Acknowledgement", "Abstract", "List of Figures", "List of Tables"]):
            sno = str(sno_counter)
            sno_counter += 1
        else:
            sno = ""

        for c_idx, (cell, w, val) in enumerate(zip(row.cells, col_w, [sno, title, page])):
            cell.width = w
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=55, bottom=55, left=100, right=100)
            set_cell_borders(cell, top="E2E8F0", bottom="E2E8F0", left="none", right="none", sz="2")
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 1 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5 if not is_sub else 9)
            if not is_sub:
                r.font.bold = True
            r.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_page_break()

def get_default_figures():
    return [
        ("Figure 4.1", "Data Flow Diagram (DFD Level 0 - Context Level)", "28"),
        ("Figure 4.2", "Data Flow Diagram (DFD Level 1 - System Subsystems)", "29"),
        ("Figure 4.3", "Data Flow Diagram (DFD Level 2 - Scoring Engine Decomposition)", "31"),
        ("Figure 4.4", "Entity-Relationship Diagram (ER Diagram)", "32"),
        ("Figure 5.1", "RecruMatch 4-Tier High-Level System Architecture", "38"),
        ("Figure 6.1", "Recruiter Analytics & Applicant Pool Triage Dashboard", "50"),
        ("Figure 6.2", "Candidate Ranking Leaderboard & Multi-Criteria Filtering", "51"),
        ("Figure 6.3", "Multi-Criteria 5-Axis Candidate Competency Radar Comparison", "52"),
        ("Figure 6.4", "Resume Forensic Exploit Inspector & Adversarial Alert Console", "53")
    ]

def get_default_tables():
    return [
        ("Table 4.1", "Job Description Relational Table Structure (job_description)", "34"),
        ("Table 4.2", "Required Skill Relational Table Structure (required_skill)", "34"),
        ("Table 4.3", "Candidate Profile Relational Table Structure (candidate_profile)", "35"),
        ("Table 4.4", "Extracted Skill Relational Table Structure (extracted_skill)", "35"),
        ("Table 4.5", "Candidate Assessment Score Table Structure (candidate_score)", "35"),
        ("Table 4.6", "Forensic Audit Log Relational Table Structure (forensic_audit_log)", "36"),
        ("Table 5.1", "Canonical Technical Skill Taxonomy (Sample Across 9 Domains)", "41"),
        ("Table 8.1", "Experimental Candidate Scoring Breakdown on Benchmark Senior Python/ML Role", "64"),
        ("Table 8.2", "System Execution Latency & Processing Throughput Benchmarks", "67")
    ]

def add_figures_and_tables_lists(doc, custom_figures=None, custom_tables=None):
    # List of Figures
    p_lof = doc.add_paragraph()
    p_lof.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lof.paragraph_format.space_before = Pt(12)
    p_lof.paragraph_format.space_after = Pt(12)
    r_f = p_lof.add_run("LIST OF FIGURES")
    r_f.font.name = "Times New Roman"
    r_f.font.size = Pt(14)
    r_f.font.bold = True
    r_f.underline = True

    figures = custom_figures if custom_figures else get_default_figures()
    for fig_no, fig_name, pno in figures:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(f"{fig_no}:  ")
        r1.font.bold = True
        r2 = p.add_run(f"{fig_name} ")
        r3 = p.add_run(f"........................................................................... Page {pno}")
        r3.font.color.rgb = RGBColor(100, 116, 139)
        for rx in [r1, r2, r3]:
            rx.font.name = "Times New Roman"
            rx.font.size = Pt(11)

    p_lot = doc.add_paragraph()
    p_lot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lot.paragraph_format.space_before = Pt(18)
    p_lot.paragraph_format.space_after = Pt(12)
    r_t = p_lot.add_run("LIST OF TABLES")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(14)
    r_t.font.bold = True
    r_t.underline = True

    tables_list = custom_tables if custom_tables else get_default_tables()
    for tab_no, tab_name, pno in tables_list:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(f"{tab_no}:  ")
        r1.font.bold = True
        r2 = p.add_run(f"{tab_name} ")
        r3 = p.add_run(f"........................................................................... Page {pno}")
        r3.font.color.rgb = RGBColor(100, 116, 139)
        for rx in [r1, r2, r3]:
            rx.font.name = "Times New Roman"
            rx.font.size = Pt(11)

    doc.add_page_break()

print("Preliminary pages module configured with Abstract and dynamic TOC.")
