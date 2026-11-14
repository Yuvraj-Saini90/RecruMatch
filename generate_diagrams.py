"""Script to generate all technical diagrams and visual figures for RecruMatch Project Report."""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set matplotlib styling for academic publication
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.autolayout'] = True

os.makedirs("diagrams", exist_ok=True)

# -------------------------------------------------------------
# 1. DFD Level 0 (Context Diagram)
# -------------------------------------------------------------
def generate_dfd_level_0():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')

    # Central System Process (Circle)
    circle = patches.Circle((50, 30), 16, edgecolor='#1e3a8a', facecolor='#dbeafe', linewidth=2.5, zorder=2)
    ax.add_patch(circle)
    ax.text(50, 33, "0.0", fontsize=13, fontweight='bold', ha='center', va='center', color='#1e3a8a')
    ax.text(50, 29, "RecruMatch System", fontsize=12, fontweight='bold', ha='center', va='center', color='#0f172a')
    ax.text(50, 25, "(Resume Screening &\nCandidate Ranking)", fontsize=9, ha='center', va='center', color='#334155')

    # External Entity: Recruiter / HR Specialist (Rectangle)
    recruiter = patches.FancyBboxPatch((4, 34), 22, 16, boxstyle="round,pad=0.5", edgecolor='#047857', facecolor='#d1fae5', linewidth=2)
    ax.add_patch(recruiter)
    ax.text(15, 42, "Recruiter /\nHR Specialist", fontsize=11, fontweight='bold', ha='center', va='center', color='#065f46')

    # External Entity: Candidate Resumes (Rectangle)
    candidates = patches.FancyBboxPatch((4, 10), 22, 16, boxstyle="round,pad=0.5", edgecolor='#047857', facecolor='#d1fae5', linewidth=2)
    ax.add_patch(candidates)
    ax.text(15, 18, "Candidate Resumes\n(PDF / DOCX)", fontsize=11, fontweight='bold', ha='center', va='center', color='#065f46')

    # External Entity: Talent Acquisition & Audit (Rectangle)
    audit = patches.FancyBboxPatch((74, 22), 22, 16, boxstyle="round,pad=0.5", edgecolor='#b91c1c', facecolor='#fee2e2', linewidth=2)
    ax.add_patch(audit)
    ax.text(85, 30, "Talent Review &\nCompliance Audit", fontsize=11, fontweight='bold', ha='center', va='center', color='#991b1b')

    # Arrows and Data Flow Labels
    # From Recruiter to System
    ax.annotate("", xy=(34, 36), xytext=(26, 42), arrowprops=dict(arrowstyle="->", color="#1e293b", lw=1.8))
    ax.text(28, 43, "Job Description (JD)\n& Weight Criteria", fontsize=8.5, ha='center', color='#1e293b', fontweight='semibold')

    # From Resumes to System
    ax.annotate("", xy=(35, 24), xytext=(26, 18), arrowprops=dict(arrowstyle="->", color="#1e293b", lw=1.8))
    ax.text(28, 17, "Batch Applicant Files\n(PDF / DOCX)", fontsize=8.5, ha='center', color='#1e293b', fontweight='semibold')

    # From System to Recruiter (Screening feedback)
    ax.annotate("", xy=(26, 38), xytext=(36, 32), arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5, ls="--"))
    ax.text(31, 32, "Ranked Shortlist &\nMatch Rationale", fontsize=8, ha='center', color='#0369a1')

    # From System to Talent Review
    ax.annotate("", xy=(74, 33), xytext=(66, 33), arrowprops=dict(arrowstyle="->", color="#1e293b", lw=1.8))
    ax.text(70, 36, "Ranked Leaderboard,\nRadar Analytics & CSV", fontsize=8.5, ha='center', color='#1e293b', fontweight='semibold')

    ax.annotate("", xy=(74, 27), xytext=(65, 27), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.8))
    ax.text(70, 23, "Forensic Exploit Alerts &\nDEI Fairness Certificate", fontsize=8.5, ha='center', color='#b91c1c', fontweight='semibold')

    plt.title("Figure 7.1: Data Flow Diagram (DFD Level 0 - Context Level)", fontsize=13, fontweight='bold', pad=15)
    plt.savefig("diagrams/dfd_level_0.png", bbox_inches='tight')
    plt.close()
    print("Generated dfd_level_0.png")

# -------------------------------------------------------------
# 2. DFD Level 1 (Major System Subsystems)
# -------------------------------------------------------------
def generate_dfd_level_1():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 80)
    ax.axis('off')

    # Entities
    recruiter = patches.FancyBboxPatch((2, 54), 18, 18, boxstyle="round,pad=0.3", edgecolor='#047857', facecolor='#d1fae5', lw=2)
    ax.add_patch(recruiter)
    ax.text(11, 63, "Recruiter /\nHR Specialist", fontsize=9.5, fontweight='bold', ha='center', va='center')

    resumes = patches.FancyBboxPatch((2, 14), 18, 18, boxstyle="round,pad=0.3", edgecolor='#047857', facecolor='#d1fae5', lw=2)
    ax.add_patch(resumes)
    ax.text(11, 23, "Applicant\nResumes\n(PDF/DOCX)", fontsize=9.5, fontweight='bold', ha='center', va='center')

    # Process 1.0
    p1 = patches.Circle((36, 23), 9, edgecolor='#1e3a8a', facecolor='#dbeafe', lw=2)
    ax.add_patch(p1)
    ax.text(36, 26, "1.0", fontsize=10, fontweight='bold', ha='center')
    ax.text(36, 21, "Document\nParsing &\nForensics", fontsize=8, ha='center', va='center', fontweight='semibold')

    # Process 2.0
    p2 = patches.Circle((62, 23), 9, edgecolor='#1e3a8a', facecolor='#dbeafe', lw=2)
    ax.add_patch(p2)
    ax.text(62, 26, "2.0", fontsize=10, fontweight='bold', ha='center')
    ax.text(62, 21, "Canonical\nTaxonomy &\nNLP Extraction", fontsize=8, ha='center', va='center', fontweight='semibold')

    # Process 3.0
    p3 = patches.Circle((62, 63), 9, edgecolor='#1e3a8a', facecolor='#dbeafe', lw=2)
    ax.add_patch(p3)
    ax.text(62, 66, "3.0", fontsize=10, fontweight='bold', ha='center')
    ax.text(62, 61, "Multi-Criteria\nScoring &\nSimilarity", fontsize=8, ha='center', va='center', fontweight='semibold')

    # Process 4.0
    p4 = patches.Circle((90, 63), 9, edgecolor='#1e3a8a', facecolor='#dbeafe', lw=2)
    ax.add_patch(p4)
    ax.text(90, 66, "4.0", fontsize=10, fontweight='bold', ha='center')
    ax.text(90, 61, "Ranking, DEI\n& Interview\nKit Generator", fontsize=8, ha='center', va='center', fontweight='semibold')

    # Data Stores
    # D1: Taxonomy DB
    d1 = patches.Rectangle((48, 2), 28, 8, edgecolor='#b45309', facecolor='#fef3c7', lw=1.8)
    ax.add_patch(d1)
    ax.text(62, 6, "D1: Canonical Skill Taxonomy (130+)", fontsize=8, ha='center', va='center', fontweight='bold', color='#92400e')

    # D2: Candidate Profiles
    d2 = patches.Rectangle((48, 39), 28, 8, edgecolor='#b45309', facecolor='#fef3c7', lw=1.8)
    ax.add_patch(d2)
    ax.text(62, 43, "D2: Candidate Structured Profiles", fontsize=8, ha='center', va='center', fontweight='bold', color='#92400e')

    # D3: Ranked Audit Store
    d3 = patches.Rectangle((80, 20), 24, 8, edgecolor='#b45309', facecolor='#fef3c7', lw=1.8)
    ax.add_patch(d3)
    ax.text(92, 24, "D3: Audit Logs & Reports", fontsize=8, ha='center', va='center', fontweight='bold', color='#92400e')

    # Data flows
    # Resumes -> 1.0
    ax.annotate("", xy=(27, 23), xytext=(20, 23), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(23.5, 25, "Files", fontsize=8, ha='center')

    # 1.0 -> 2.0 (Clean text)
    ax.annotate("", xy=(53, 23), xytext=(45, 23), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(49, 25, "Sanitized Text", fontsize=7.5, ha='center')

    # D1 <-> 2.0
    ax.annotate("", xy=(62, 14), xytext=(62, 10), arrowprops=dict(arrowstyle="<->", lw=1.3, color='#92400e'))
    ax.text(67, 12, "Synonym Map", fontsize=7, color='#92400e')

    # 2.0 -> D2
    ax.annotate("", xy=(62, 39), xytext=(62, 32), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(67, 35, "Extracted JSON", fontsize=7.5)

    # D2 -> 3.0
    ax.annotate("", xy=(62, 54), xytext=(62, 47), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(67, 50, "Candidate Data", fontsize=7.5)

    # Recruiter -> 3.0 (JD & Weights)
    ax.annotate("", xy=(53, 63), xytext=(20, 63), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(36, 65, "JD Requirements & Weights", fontsize=8, ha='center')

    # 3.0 -> 4.0
    ax.annotate("", xy=(81, 63), xytext=(71, 63), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(76, 65, "Raw Scores", fontsize=8, ha='center')

    # 4.0 -> D3
    ax.annotate("", xy=(90, 28), xytext=(90, 54), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(96, 40, "Persist Results", fontsize=7.5)

    # 4.0 -> Recruiter (Dashboard Output)
    ax.annotate("", xy=(16, 72), xytext=(90, 72), arrowprops=dict(arrowstyle="->", lw=1.5, ls="--", color='#0369a1'))
    ax.plot([90, 90], [72, 72], color='#0369a1')
    ax.text(50, 74, "Interactive Ranked Dashboard, Radar Charts & DEI Audit", fontsize=8.5, ha='center', color='#0369a1', fontweight='bold')

    plt.title("Figure 7.2: Data Flow Diagram (DFD Level 1 - System Subsystems)", fontsize=13, fontweight='bold', pad=15)
    plt.savefig("diagrams/dfd_level_1.png", bbox_inches='tight')
    plt.close()
    print("Generated dfd_level_1.png")

# -------------------------------------------------------------
# 3. DFD Level 2 (Decomposition of Process 3.0 - Scoring Engine)
# -------------------------------------------------------------
def generate_dfd_level_2():
    fig, ax = plt.subplots(figsize=(11, 7), dpi=300)
    ax.set_xlim(0, 110)
    ax.set_ylim(0, 70)
    ax.axis('off')

    # Input Data
    cand_box = patches.FancyBboxPatch((2, 25), 18, 20, boxstyle="round,pad=0.3", edgecolor='#1e3a8a', facecolor='#eff6ff', lw=2)
    ax.add_patch(cand_box)
    ax.text(11, 35, "Input:\nCandidate Profile\n& Resume Text", fontsize=9, fontweight='bold', ha='center', va='center')

    jd_box = patches.FancyBboxPatch((2, 50), 18, 16, boxstyle="round,pad=0.3", edgecolor='#047857', facecolor='#ecfdf5', lw=2)
    ax.add_patch(jd_box)
    ax.text(11, 58, "Input:\nJob Description\nCriteria", fontsize=9, fontweight='bold', ha='center', va='center')

    # 5 Sub-processes of 3.0
    sub_processes = [
        ("3.1", "Required Skills\nMatcher (S_req)", 58),
        ("3.2", "Preferred Skills\nMatcher (S_pref)", 46),
        ("3.3", "Experience\nScorer (S_exp)", 34),
        ("3.4", "Education Level\nNormalizer (S_edu)", 22),
        ("3.5", "TF-IDF / SBERT\nCosine Similarity (S_sim)", 10)
    ]

    for code, label, y in sub_processes:
        p = patches.FancyBboxPatch((32, y-4), 32, 8, boxstyle="round,pad=0.2", edgecolor='#4338ca', facecolor='#e0e7ff', lw=1.6)
        ax.add_patch(p)
        ax.text(35, y, code, fontsize=8.5, fontweight='bold', color='#312e81', va='center')
        ax.text(48, y, label, fontsize=8, fontweight='semibold', color='#1e1b4b', ha='center', va='center')

        # Input arrows to sub-processes
        ax.annotate("", xy=(32, y), xytext=(20, 35), arrowprops=dict(arrowstyle="->", lw=1.1, color='#64748b'))

    # Process 3.6: Weighted Aggregator
    p_agg = patches.Circle((84, 34), 10, edgecolor='#b91c1c', facecolor='#fee2e2', lw=2)
    ax.add_patch(p_agg)
    ax.text(84, 37, "3.6", fontsize=10, fontweight='bold', ha='center', color='#991b1b')
    ax.text(84, 32, "Weighted Sum\nAggregator &\nTier Classifier", fontsize=7.5, ha='center', va='center', fontweight='bold', color='#7f1d1d')

    # Arrows from sub-processes to aggregator
    for _, _, y in sub_processes:
        ax.annotate("", xy=(74, 34), xytext=(64, y), arrowprops=dict(arrowstyle="->", lw=1.2, color='#4338ca'))

    # Output Box
    out_box = patches.FancyBboxPatch((98, 25), 11, 18, boxstyle="round,pad=0.3", edgecolor='#047857', facecolor='#d1fae5', lw=2)
    ax.add_patch(out_box)
    ax.text(103.5, 34, "Final Score\n& Tier\n(0 - 100%)", fontsize=8.5, fontweight='bold', ha='center', va='center', color='#065f46')

    ax.annotate("", xy=(98, 34), xytext=(94, 34), arrowprops=dict(arrowstyle="->", lw=1.8, color='#047857'))

    plt.title("Figure 7.3: Data Flow Diagram (DFD Level 2 - Process 3.0 Scoring Engine)", fontsize=13, fontweight='bold', pad=15)
    plt.savefig("diagrams/dfd_level_2.png", bbox_inches='tight')
    plt.close()
    print("Generated dfd_level_2.png")

# -------------------------------------------------------------
# 4. Entity-Relationship Diagram (ER Diagram)
# -------------------------------------------------------------
def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 120)
    ax.set_ylim(0, 80)
    ax.axis('off')

    def draw_entity(x, y, w, h, title, attrs, pk_idx=0):
        # Header
        header = patches.Rectangle((x, y + h - 6), w, 6, facecolor='#1e3a8a', edgecolor='#0f172a', lw=1.5)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 3, title, color='white', fontsize=9, fontweight='bold', ha='center', va='center')
        # Body
        body = patches.Rectangle((x, y), w, h - 6, facecolor='#f8fafc', edgecolor='#0f172a', lw=1.5)
        ax.add_patch(body)
        for i, attr in enumerate(attrs):
            color = '#b91c1c' if i == pk_idx else ('#0369a1' if '(FK)' in attr else '#334155')
            weight = 'bold' if (i == pk_idx or '(FK)' in attr) else 'normal'
            ax.text(x + 2, y + h - 9 - i*3.8, attr, fontsize=7.5, color=color, fontweight=weight, va='center')

    # Draw Entities
    draw_entity(4, 48, 30, 28, "JOB_DESCRIPTION", [
        "jd_id (PK: UUID)",
        "role_title (VARCHAR)",
        "min_experience (FLOAT)",
        "target_education (VARCHAR)",
        "created_at (TIMESTAMP)",
        "raw_text (TEXT)"
    ])

    draw_entity(44, 48, 32, 28, "REQUIRED_SKILL", [
        "req_skill_id (PK: UUID)",
        "jd_id (FK: UUID)",
        "skill_name (VARCHAR)",
        "is_mandatory (BOOLEAN)",
        "category (VARCHAR)",
        "weight (FLOAT)"
    ])

    draw_entity(86, 48, 30, 28, "CANDIDATE_PROFILE", [
        "candidate_id (PK: UUID)",
        "full_name (VARCHAR)",
        "email (VARCHAR)",
        "phone (VARCHAR)",
        "experience_years (FLOAT)",
        "normalized_degree (VARCHAR)"
    ])

    draw_entity(4, 6, 32, 32, "CANDIDATE_SCORE", [
        "score_id (PK: UUID)",
        "candidate_id (FK: UUID)",
        "jd_id (FK: UUID)",
        "final_score (FLOAT)",
        "required_skills_pct (FLOAT)",
        "preferred_skills_pct (FLOAT)",
        "experience_score (FLOAT)",
        "education_score (FLOAT)",
        "semantic_similarity (FLOAT)",
        "match_tier (VARCHAR)"
    ])

    draw_entity(46, 6, 30, 28, "FORENSIC_AUDIT_LOG", [
        "audit_id (PK: UUID)",
        "candidate_id (FK: UUID)",
        "fraud_score (FLOAT)",
        "white_text_count (INT)",
        "micro_font_count (INT)",
        "homoglyph_count (INT)",
        "risk_level (VARCHAR)"
    ])

    draw_entity(86, 6, 30, 28, "EXTRACTED_SKILL", [
        "extracted_id (PK: UUID)",
        "candidate_id (FK: UUID)",
        "canonical_name (VARCHAR)",
        "category (VARCHAR)",
        "is_inferred (BOOLEAN)",
        "confidence (FLOAT)"
    ])

    # Connecting Relationship Lines
    # JD to REQUIRED_SKILL (1:N)
    ax.annotate("", xy=(44, 62), xytext=(34, 62), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1e293b'))
    ax.text(39, 64, "1 : N", fontsize=8, fontweight='bold', color='#1e293b', ha='center')

    # CANDIDATE to EXTRACTED_SKILL (1:N)
    ax.annotate("", xy=(101, 34), xytext=(101, 48), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1e293b'))
    ax.text(104, 41, "1 : N", fontsize=8, fontweight='bold', color='#1e293b')

    # CANDIDATE to FORENSIC_LOG (1:1)
    ax.annotate("", xy=(76, 20), xytext=(86, 48), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1e293b'))
    ax.text(80, 36, "1 : 1", fontsize=8, fontweight='bold', color='#1e293b')

    # CANDIDATE to SCORE (1:N) & JD to SCORE (1:N)
    ax.annotate("", xy=(36, 22), xytext=(86, 52), arrowprops=dict(arrowstyle="->", lw=1.3, ls="--", color='#4338ca'))
    ax.annotate("", xy=(19, 38), xytext=(19, 48), arrowprops=dict(arrowstyle="->", lw=1.3, ls="--", color='#4338ca'))
    ax.text(32, 28, "M : N Scored", fontsize=8, fontweight='bold', color='#4338ca')

    plt.title("Figure 7.4: Entity-Relationship Diagram (ER Diagram)", fontsize=13, fontweight='bold', pad=15)
    plt.savefig("diagrams/er_diagram.png", bbox_inches='tight')
    plt.close()
    print("Generated er_diagram.png")

# -------------------------------------------------------------
# 5. System Architecture Diagram
# -------------------------------------------------------------
def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 85)
    ax.axis('off')

    tiers = [
        ("Tier 1: Presentation & User Interface Layer", 66, 15, "#eff6ff", "#1e40af", [
            "Streamlit Recruiter Dashboard (6 Pages, Reactive UI)",
            "FastAPI REST Endpoints & OpenAPI / Swagger UI",
            "Interactive Plotly Radar Charts & Triage Distributions"
        ]),
        ("Tier 2: Security & Forensic Pre-Flight Shield", 46, 16, "#fef2f2", "#991b1b", [
            "PyMuPDF Low-Level Color & Font Stream Analyzer (#FFFFFF White Text)",
            "Micro-Font (<2pt) & Homoglyph Spoofing Detector (Cyrillic to Latin)",
            "Zero-Width Space Stripper & Automated Text Sanitizer"
        ]),
        ("Tier 3: Core AI, NLP & Scoring Engine Layer", 24, 18, "#f0fdf4", "#166534", [
            "Document Parsers: pdfplumber & python-docx Engine",
            "spaCy NLP Entity & Experience Processor",
            "Canonical Skill Taxonomy (130+ Skills) & Skill Knowledge Graph",
            "Dual Vectorizer: TF-IDF Cosine Similarity & SBERT Embeddings",
            "Explainable Multi-Criteria Scoring Formula & Career Velocity Analyzer"
        ]),
        ("Tier 4: Data, Storage & Reporting Layer", 4, 16, "#fafaf9", "#44403c", [
            "Benchmark Job Description Presets (Python/ML, Full Stack, DevOps)",
            "Blind Recruitment PII Anonymizer & DEI Compliance Generator",
            "Export Engine: Recruiter Audit Reports (CSV, Markdown, JSON)"
        ])
    ]

    for title, y, h, bg, border, items in tiers:
        rect = patches.FancyBboxPatch((5, y), 90, h, boxstyle="round,pad=0.5", facecolor=bg, edgecolor=border, lw=2)
        ax.add_patch(rect)
        ax.text(8, y + h - 3.5, title, fontsize=10, fontweight='bold', color=border)
        for i, item in enumerate(items):
            ax.text(12, y + h - 7 - i*3.5, f"•  {item}", fontsize=8.5, color='#1e293b')

    # Connection Arrows between Tiers
    ax.annotate("", xy=(50, 66), xytext=(50, 62), arrowprops=dict(arrowstyle="<->", lw=2, color='#1e40af'))
    ax.annotate("", xy=(50, 46), xytext=(50, 42), arrowprops=dict(arrowstyle="<->", lw=2, color='#166534'))
    ax.annotate("", xy=(50, 24), xytext=(50, 20), arrowprops=dict(arrowstyle="<->", lw=2, color='#44403c'))

    plt.title("Figure 8.1: RecruMatch 4-Tier High-Level System Architecture", fontsize=13, fontweight='bold', pad=15)
    plt.savefig("diagrams/system_architecture.png", bbox_inches='tight')
    plt.close()
    print("Generated system_architecture.png")

# -------------------------------------------------------------
# 6. UI Screenshot Mockups for Chapter 9
# -------------------------------------------------------------
def generate_ui_mockups():
    # 6.1 Dashboard Overview
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_facecolor('#0f172a')
    fig.patch.set_facecolor('#0f172a')

    # KPI Cards
    cards = [
        ("Total Applicants", "5", "#38bdf8", 0.05),
        ("Average Pool Score", "49.6%", "#818cf8", 0.28),
        ("Strong Matches", "2 (40%)", "#34d399", 0.51),
        ("Adversarial Flags", "1 Flagged", "#f87171", 0.74)
    ]
    for label, val, color, x in cards:
        rect = patches.FancyBboxPatch((x, 0.72), 0.21, 0.22, transform=ax.transAxes, boxstyle="round,pad=0.03", facecolor='#1e293b', edgecolor=color, lw=1.8)
        ax.add_patch(rect)
        ax.text(x + 0.105, 0.86, val, transform=ax.transAxes, color='white', fontsize=16, fontweight='bold', ha='center')
        ax.text(x + 0.105, 0.76, label, transform=ax.transAxes, color=color, fontsize=8.5, fontweight='semibold', ha='center')

    # Match Tier Distribution Bar Chart
    categories = ['Excellent (≥80%)', 'Good (60-79%)', 'Moderate (40-59%)', 'Low (<40%)']
    counts = [0, 2, 1, 2]
    colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444']

    bars = ax.bar(categories, counts, color=colors, width=0.45, edgecolor='white', lw=0.8)
    ax.set_ylim(0, 3)
    ax.set_ylabel("Number of Candidates", color='#94a3b8', fontsize=9)
    ax.tick_params(colors='#cbd5e1')
    ax.spines['bottom'].set_color('#334155')
    ax.spines['left'].set_color('#334155')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.08, int(yval), ha='center', va='bottom', color='white', fontweight='bold')

    plt.title("RecruMatch Recruiter Dashboard - Applicant Pool Triage & KPI Overview", color='white', fontsize=11, fontweight='bold', pad=12)
    plt.savefig("diagrams/screenshot_dashboard.png", bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Generated screenshot_dashboard.png")

    # 6.2 Candidate Ranking Leaderboard
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.axis('off')
    fig.patch.set_facecolor('#0f172a')

    headers = ["Rank", "Candidate Name", "Match Score", "Tier", "Req. Skills Match", "Experience", "Forensic Status"]
    data = [
        ["#1", "Vikram Malhotra", "73.1%", "Good Match", "76.9% (10/13)", "10.0 Yrs", "[FLAGGED] 3 Exploits"],
        ["#2", "Aman Verma", "65.2%", "Good Match", "84.6% (11/13)", "4.0 Yrs", "[CLEAN] Verified"],
        ["#3", "Priya Sharma", "48.9%", "Moderate Match", "46.2% (6/13)", "2.5 Yrs", "[CLEAN] Verified"],
        ["#4", "Sneha Gupta", "37.1%", "Low Match", "23.1% (3/13)", "3.5 Yrs", "[CLEAN] Verified"],
        ["#5", "Rahul Kumar", "23.8%", "Low Match", "23.1% (3/13)", "1.2 Yrs", "[CLEAN] Verified"]
    ]

    table = ax.table(cellText=data, colLabels=headers, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1, 1.8)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor('#1e3a8a')
            cell.set_text_props(color='white', fontweight='bold')
        else:
            cell.set_facecolor('#1e293b' if row % 2 == 1 else '#0f172a')
            if col == 2:
                cell.set_text_props(color='#38bdf8', fontweight='bold')
            elif col == 6 and "🚨" in cell.get_text().get_text():
                cell.set_text_props(color='#f87171', fontweight='bold')
            else:
                cell.set_text_props(color='#e2e8f0')
        cell.set_edgecolor('#334155')

    plt.title("Candidate Ranking Leaderboard (Senior Python & ML Engineer)", color='white', fontsize=11, fontweight='bold', pad=15)
    plt.savefig("diagrams/screenshot_ranking.png", bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Generated screenshot_ranking.png")

    # 6.3 Radar Chart Analysis
    labels = ['Required Skills', 'Preferred Skills', 'Experience', 'Education', 'Semantic Sim.']
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    # Scores for Aman Verma (Clean) vs Priya Sharma
    aman_scores = [84.6, 37.5, 100.0, 75.0, 16.2]
    aman_scores += aman_scores[:1]

    priya_scores = [46.2, 37.5, 83.3, 100.0, 11.8]
    priya_scores += priya_scores[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True), dpi=300)
    ax.set_facecolor('#1e293b')
    fig.patch.set_facecolor('#0f172a')

    ax.plot(angles, aman_scores, color='#38bdf8', linewidth=2, label='Aman Verma (Score: 65.2%)')
    ax.fill(angles, aman_scores, color='#38bdf8', alpha=0.25)

    ax.plot(angles, priya_scores, color='#a855f7', linewidth=2, label='Priya Sharma (Score: 48.9%)')
    ax.fill(angles, priya_scores, color='#a855f7', alpha=0.2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='#e2e8f0', fontsize=8.5, fontweight='bold')
    ax.tick_params(colors='#94a3b8')
    ax.spines['polar'].set_color('#475569')
    ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.1), facecolor='#1e293b', edgecolor='#475569', labelcolor='white', fontsize=8)

    plt.title("Multi-Criteria 5-Axis Candidate Competency Radar Comparison", color='white', fontsize=10, fontweight='bold', pad=15)
    plt.savefig("diagrams/screenshot_candidate_detail.png", bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Generated screenshot_candidate_detail.png")

    # 6.4 Forensic Inspector View
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    ax.axis('off')
    fig.patch.set_facecolor('#0f172a')

    # Security Alert Box
    alert_box = patches.FancyBboxPatch((0.05, 0.65), 0.9, 0.28, transform=ax.transAxes, boxstyle="round,pad=0.03", facecolor='#450a0a', edgecolor='#ef4444', lw=2)
    ax.add_patch(alert_box)
    ax.text(0.5, 0.82, "⚠️ HIGH ADVERSARIAL RISK DETECTED: Vikram_Malhotra_Adversarial_Exploit.pdf", transform=ax.transAxes, color='#fca5a5', fontsize=10, fontweight='bold', ha='center')
    ax.text(0.5, 0.72, "Fraud Score: 85/100 | Risk Tier: CRITICAL | Automated Sanitization Applied", transform=ax.transAxes, color='#fecaca', fontsize=8.5, ha='center')

    # Exploit Breakdown Boxes
    exploits = [
        ("1. Hidden White Text", "18 White (#FFFFFF) text spans detected.\nExploited keywords: 'FastAPI, PyTorch, Docker, Kubernetes'", "#991b1b", 0.05),
        ("2. Micro-Font Stacking", "Font size: 1.5 pt (sub-human readable).\nDesigned to manipulate legacy tokenizers.", "#c2410c", 0.36),
        ("3. Homoglyph Spoofing", "Cyrillic homoglyphs: 'а' (U+0430), 'о' (U+043E)\nused to evade exact substring blacklists.", "#b45309", 0.67)
    ]

    for title, desc, color, x in exploits:
        box = patches.FancyBboxPatch((x, 0.15), 0.28, 0.42, transform=ax.transAxes, boxstyle="round,pad=0.03", facecolor='#1e293b', edgecolor=color, lw=1.8)
        ax.add_patch(box)
        ax.text(x + 0.14, 0.48, title, transform=ax.transAxes, color='white', fontsize=9, fontweight='bold', ha='center')
        ax.text(x + 0.02, 0.32, desc, transform=ax.transAxes, color='#cbd5e1', fontsize=7.5, va='center')

    plt.title("Resume Forensic Inspector - Adversarial Exploit Detection Dashboard", color='white', fontsize=11, fontweight='bold', pad=12)
    plt.savefig("diagrams/screenshot_forensic_inspector.png", bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Generated screenshot_forensic_inspector.png")

if __name__ == "__main__":
    generate_dfd_level_0()
    generate_dfd_level_1()
    generate_dfd_level_2()
    generate_er_diagram()
    generate_system_architecture()
    generate_ui_mockups()
    print("All diagrams generated successfully!")
