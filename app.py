"""RecruMatch - Intelligent Resume Screening & Candidate Ranking System.

A transparent, explainable recruitment screening workspace designed for human
recruiters and hiring managers. Features multi-criteria qualification scoring,
spacy canonical skill extraction, resume tampering inspection, fair multi-criteria ranking,
and structured interview generation.
"""

import os
import glob
import io
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Internal domain engines
from src.config import (
    APP_TITLE, APP_SUBTITLE, PROJECT_INFO,
    DEFAULT_WEIGHTS, DEFAULT_THRESHOLDS, MATCH_CATEGORIES
)
from src.pdf_parser import extract_text_from_pdf
from src.docx_parser import extract_text_from_docx
from src.skill_extractor import extract_skills_from_text
from src.skill_dictionary import get_all_canonical_skills
from src.nlp_processor import parse_resume_content
from src.jd_analyzer import analyze_job_description
from src.similarity_engine import is_sbert_available
from src.scorer import generate_candidate_assessment, get_match_category
from src.ranking import rank_candidates, compute_dashboard_metrics
from src.export_utils import export_results_to_csv, generate_recruiter_markdown_report

# Advanced screening & security modules
from forensic_inspector import ResumeForensicInspector
from src.anonymizer import anonymize_candidate_profile, generate_dei_fairness_audit
from src.interview_generator import generate_interview_kit
from src.skill_graph import infer_implicit_competencies
from src.career_velocity import analyze_career_velocity

# Page configuration
st.set_page_config(
    page_title="RecruMatch • AI Candidate Screening & Forensic Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Load Design System CSS
def load_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_custom_css()


# Industry benchmark job templates
JD_PRESETS = {
    "Senior Python & ML Engineer": """Job Title: Senior Python & Machine Learning Engineer
Department: Engineering
Location: Hybrid / Remote

About the Role:
We are looking for an experienced Senior Python & Machine Learning Engineer to design, build, and deploy production machine learning pipelines and backend services.

Required Skills & Core Qualifications:
- Proficiency in Python, SQL, REST API design, and Algorithms.
- Practical experience with Machine Learning, Scikit-learn, and Pandas.
- Web backend development with FastAPI or Django.
- Containerization and version control using Docker, Git, and GitHub.
- Cloud infrastructure experience with AWS.

Preferred / Bonus Skills:
- PyTorch, TensorFlow, Deep Learning, and Natural Language Processing.
- PostgreSQL and Redis caching.
- Production orchestration with Kubernetes and CI/CD pipelines.

Experience & Education:
- Minimum 3+ years of professional software engineering and machine learning experience.
- Master's or Bachelor's Degree in Computer Science, Data Science, or related engineering discipline.
""",
    "Full Stack Web Developer": """Job Title: Full Stack Web Developer (React & Node.js)
Department: Product Engineering
Location: Full-time / Hybrid

About the Role:
We are seeking a versatile Full Stack Developer to build responsive, accessible web applications and reliable APIs.

Required Skills & Core Qualifications:
- Strong command of JavaScript, TypeScript, HTML, and CSS.
- Frontend proficiency in React, Next.js, and modern state management.
- Backend proficiency with Node.js, Express.js, and REST API development.
- Database design with PostgreSQL and SQL.
- Version control using Git and GitHub.

Preferred / Bonus Skills:
- Docker containerization and AWS infrastructure.
- Tailwind CSS, GraphQL, and Redis caching.

Experience & Education:
- 2+ years of relevant full-stack web development experience.
- Bachelor's Degree in Computer Science, Information Technology, or equivalent experience.
""",
    "Data Scientist & NLP Specialist": """Job Title: Data Scientist & NLP Specialist
Department: Applied AI
Location: Remote

About the Role:
Join our data science team to build natural language processing models, semantic search systems, and data pipelines.

Required Skills & Core Qualifications:
- Python programming and SQL querying.
- Extensive experience in Data Science, Machine Learning, Pandas, and NumPy.
- Practical expertise in Natural Language Processing (NLP), spaCy, and Scikit-learn.
- Grounding in linear algebra, statistics, and exploratory data analysis.
- Experience with Git version control.

Preferred / Bonus Skills:
- Deep learning with PyTorch or Hugging Face Transformers.
- Semantic vector search and LLM prompting.
- Deployment via Streamlit or FastAPI.

Experience & Education:
- 3+ years of practical experience in data science or NLP.
- Master's or Ph.D. in Computer Science, Statistics, or Computational Linguistics.
""",
    "Cloud DevOps & SRE Engineer": """Job Title: Cloud DevOps & Site Reliability Engineer (SRE)
Department: Platform Infrastructure
Location: Full-time / Remote

About the Role:
We are seeking a Cloud DevOps & SRE Engineer to manage multi-cloud infrastructure, maintain resilient CI/CD pipelines, and monitor container clusters.

Required Skills & Core Qualifications:
- Proficiency in AWS, Docker, Kubernetes, Linux, and Bash scripting.
- Infrastructure as Code (IaC) using Terraform or Ansible.
- CI/CD automation with Jenkins, GitHub Actions, or GitLab CI.
- System monitoring with Prometheus and Grafana.
- Version control using Git and GitHub.

Preferred / Bonus Skills:
- Scripting with Python or Go.
- Nginx reverse proxies, microservices networking, and security hardening.
- Production experience with high-load PostgreSQL databases.

Experience & Education:
- 3+ years of professional DevOps or Site Reliability engineering experience.
- Bachelor's Degree in Computer Science, Information Technology, or related field.
"""
}


# Initialize Session State
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "current_role_title" not in st.session_state:
    st.session_state.current_role_title = "Senior Python & ML Engineer"
if "jd_analysis" not in st.session_state:
    st.session_state.jd_analysis = None
if "uploaded_resumes" not in st.session_state:
    st.session_state.uploaded_resumes = []
if "ranked_candidates" not in st.session_state:
    st.session_state.ranked_candidates = []
if "selected_candidate_id" not in st.session_state:
    st.session_state.selected_candidate_id = None
if "nav_page" not in st.session_state or st.session_state.nav_page == "🎯 Candidate Pipeline":
    st.session_state.nav_page = "✨ Stitch Enterprise Workspace (index.html)"
if "sidebar_nav" in st.session_state and st.session_state.sidebar_nav == "🎯 Candidate Pipeline":
    st.session_state.sidebar_nav = "✨ Stitch Enterprise Workspace (index.html)"
if "weights" not in st.session_state:
    st.session_state.weights = DEFAULT_WEIGHTS.copy()
if "thresholds" not in st.session_state:
    st.session_state.thresholds = DEFAULT_THRESHOLDS.copy()
if "matching_method" not in st.session_state:
    st.session_state.matching_method = "TF-IDF"


def get_initials(name: str) -> str:
    """Generates two-letter uppercase initials for avatar chips."""
    parts = name.strip().split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}".upper()
    elif len(parts) == 1 and parts[0]:
        return parts[0][:2].upper()
    return "CD"


def apply_job_description(new_jd_text: str, role_title: str = "Custom Role"):
    """Atomically sets a new Job Description and recalculates candidate match scores."""
    new_jd_text = new_jd_text.strip()
    if not new_jd_text:
        return
    st.session_state.jd_text = new_jd_text
    st.session_state.current_role_title = role_title

    analysis = analyze_job_description(new_jd_text)
    st.session_state.jd_analysis = analysis

    # Re-score all candidates against the updated JD
    if st.session_state.uploaded_resumes:
        assessments = [
            generate_candidate_assessment(
                p, st.session_state.jd_analysis,
                weights=st.session_state.weights,
                thresholds=st.session_state.thresholds,
                matching_method=st.session_state.matching_method
            )
            for p in st.session_state.uploaded_resumes
        ]
        st.session_state.ranked_candidates = rank_candidates(assessments)
        if st.session_state.ranked_candidates:
            st.session_state.selected_candidate_id = st.session_state.ranked_candidates[0]["candidate_id"]


def load_demo_data():
    """Ingests the benchmark sample resumes and parses them through the complete screening pipeline."""
    base_dir = os.path.dirname(__file__)
    sample_jd_path = os.path.join(base_dir, "data", "sample_job_description.txt")
    if os.path.exists(sample_jd_path):
        with open(sample_jd_path, "r", encoding="utf-8") as f:
            demo_jd_text = f.read()
    else:
        demo_jd_text = JD_PRESETS["Senior Python & ML Engineer"]

    inspector = ResumeForensicInspector()
    sample_resumes = glob.glob(os.path.join(base_dir, "data", "sample_resumes", "*.*"))
    parsed_list = []

    for filepath in sample_resumes:
        fname = os.path.basename(filepath)
        forensic_report = None
        if fname.endswith(".pdf"):
            res = extract_text_from_pdf(filepath)
            try:
                forensic_report = inspector.inspect_pdf(filepath, filename=fname)
            except Exception:
                forensic_report = None
        elif fname.endswith(".docx"):
            res = extract_text_from_docx(filepath)
            try:
                forensic_report = inspector.inspect_docx(filepath, filename=fname)
            except Exception:
                forensic_report = None
        else:
            continue

        if res["success"]:
            # Clean text from forensic sanitizer ensures invisible keywords don't artificially inflate score
            text = forensic_report["clean_text"] if (forensic_report and forensic_report.get("clean_text")) else res["text"]
            sk_info = extract_skills_from_text(text)
            profile = parse_resume_content(text)
            profile["skills"] = sk_info["skills"]
            profile["filename"] = fname
            profile["candidate_id"] = fname.replace(".", "_")
            profile["forensic_report"] = forensic_report
            exp_yrs = float(profile.get("experience", {}).get("years", 0.0))
            profile["career_velocity"] = analyze_career_velocity(text, exp_yrs)
            profile["implicit_skills"] = infer_implicit_competencies(profile["skills"])
            parsed_list.append(profile)

    st.session_state.uploaded_resumes = parsed_list
    apply_job_description(demo_jd_text, role_title="Senior Python & ML Engineer")


# Initialize demo data on launch
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    load_demo_data()


# -------------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------------
with st.sidebar:
    # Clean Brand Block
    st.markdown(
        """
        <div class="brand-block">
            <div class="brand-icon">RM</div>
            <div>
                <div class="brand-text-title">RecruMatch</div>
                <div class="brand-text-subtitle">Candidate Screening & Ranking</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Active Pipeline Counter
    resumes_count = len(st.session_state.ranked_candidates)
    if resumes_count > 0:
        st.markdown(f"<div class='status-indicator ready'>● {resumes_count} Applicants Evaluated</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='status-indicator' style='background: #1e293b; color: #94a3b8;'>○ Ready for Resumes</div>", unsafe_allow_html=True)

    # Clean Navigation Menu
    nav_options = [
        "✨ Stitch Enterprise Workspace (index.html)",
        "🎯 Candidate Pipeline (Native)",
        "👤 Candidate Inspector",
        "📄 Job Requisitions",
        "📥 Resume Ingestion",
        "⚙️ Scoring Preferences"
    ]

    default_nav_idx = nav_options.index(st.session_state.nav_page) if st.session_state.nav_page in nav_options else 0
    menu_selection = st.radio(
        "Navigation",
        nav_options,
        index=default_nav_idx,
        label_visibility="collapsed",
        key="sidebar_nav"
    )
    st.session_state.nav_page = menu_selection

    st.markdown("<hr style='margin: 14px 0 10px 0; border: none; border-top: 1px solid #1e293b;'>", unsafe_allow_html=True)

    # Target Role Pill in Sidebar
    curr_role = st.session_state.get("current_role_title", "Senior Python & ML Engineer")
    st.caption("Active Target Role:")
    st.markdown(f"**{curr_role}**")

    # Quick Workspace Actions
    st.markdown("<hr style='margin: 10px 0 14px 0; border: none; border-top: 1px solid #1e293b;'>", unsafe_allow_html=True)
    if st.button("Load Sample Data", use_container_width=True, key="btn_load_demo"):
        load_demo_data()
        st.session_state.nav_page = "🎯 Candidate Pipeline (Native)"
        st.rerun()

    if st.session_state.ranked_candidates:
        if st.button("Clear Workspace", use_container_width=True, key="btn_clear_data"):
            st.session_state.uploaded_resumes = []
            st.session_state.ranked_candidates = []
            st.session_state.selected_candidate_id = None
            st.rerun()

    # System Architecture Note
    st.markdown(
        """
        <div style="font-size: 11px; color: #64748b; margin-top: 24px; line-height: 1.5; border-top: 1px solid #1e293b; padding-top: 12px;">
            <b style="color: #94a3b8;">RecruMatch Platform</b><br>
            • Multi-format PDF & DOCX parsing<br>
            • spaCy canonical skill taxonomy<br>
            • Explainable multi-criteria scoring<br>
            • 100% offline & privacy-first
        </div>
        """,
        unsafe_allow_html=True
    )


# =============================================================
# VIEW 0: STITCH ENTERPRISE WORKSPACE (INDEX.HTML)
# =============================================================
if menu_selection == "✨ Stitch Enterprise Workspace (index.html)":
    import streamlit.components.v1 as components
    st.markdown("""
        <style>
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100vw !important;
            width: 100vw !important;
        }
        [data-testid="stCustomComponentV1"] {
            width: 100% !important;
            height: calc(100vh - 55px) !important;
            min-height: 850px !important;
        }
        iframe {
            border: none !important;
            border-radius: 0px !important;
            width: 100% !important;
            height: 100% !important;
            min-height: 850px !important;
            display: block !important;
        }
        </style>
    """, unsafe_allow_html=True)

    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            html_code = f.read()
        components.html(html_code, height=1200, scrolling=True)
    else:
        st.error("index.html not found.")

# =============================================================
# VIEW 1: CANDIDATE PIPELINE (LEADERBOARD & OVERVIEW)
# =============================================================
elif menu_selection == "🎯 Candidate Pipeline (Native)":
    # Top Context Bar
    role_name = st.session_state.get("current_role_title", "Senior Python & ML Engineer")
    analysis = st.session_state.get("jd_analysis")
    req_count = len(analysis.get("required_skills", [])) if analysis else 0
    exp_target = analysis.get("min_experience_years", 0) if analysis else 0

    col_ctx1, col_ctx2 = st.columns([3, 1.2])
    with col_ctx1:
        st.markdown(
            f"""
            <div class="context-bar">
                <div>
                    <div class="context-bar-label">Active Target Role</div>
                    <div class="context-bar-title">{role_name}</div>
                </div>
                <div class="context-bar-meta">
                    <span><b>{req_count}</b> mandatory skills</span>
                    <span>•</span>
                    <span><b>{exp_target:g}+</b> yrs experience</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_ctx2:
        preset_names = list(JD_PRESETS.keys())
        curr_idx = preset_names.index(role_name) if role_name in preset_names else 0
        selected_role = st.selectbox(
            "Switch Role Template:",
            options=preset_names,
            index=curr_idx,
            label_visibility="collapsed",
            key="pipeline_role_switch"
        )
        if selected_role != role_name:
            apply_job_description(JD_PRESETS[selected_role], selected_role)
            st.rerun()

    if not st.session_state.ranked_candidates:
        st.info("No candidates in the evaluation pipeline. Use **Resume Ingestion** to upload resumes, or click **Load Sample Data** in the sidebar.")
    else:
        # Compute pipeline metrics
        metrics = compute_dashboard_metrics(
            st.session_state.ranked_candidates,
            st.session_state.jd_analysis if st.session_state.jd_analysis else {}
        )

        # 4 Clean KPI Metric Cards
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Applicants", metrics["total_candidates"], help="Resumes parsed in the current pipeline")
        k2.metric("Average Score", f"{metrics['average_score']}%", help="Weighted average across all candidates")
        k3.metric("Qualified (≥60%)", metrics["strong_matches_count"], help="Candidates meeting the good/excellent threshold")
        
        # Tampering Risk Metric
        tamper_count = sum(
            1 for c in st.session_state.ranked_candidates 
            if (c.get("candidate_profile", {}).get("forensic_report") or {}).get("fraud_score", 0.0) >= 30.0
        )
        k4.metric("Tampering Notices", tamper_count, help="Resumes flagged for hidden text, micro-fonts, or homoglyphs")

        st.markdown("<br>", unsafe_allow_html=True)

        # Search, Filter, and Sorting Controls
        fc1, fc2, fc3 = st.columns([2, 1.3, 1.3])
        with fc1:
            search_name = st.text_input("Search applicant by name:", placeholder="Filter candidates...", label_visibility="collapsed")
        with fc2:
            tier_choice = st.selectbox(
                "Filter by Match Tier:",
                options=["All Tiers", "Excellent Match", "Good Match", "Moderate Match", "Low Match"],
                label_visibility="collapsed"
            )
        with fc3:
            sort_field = st.selectbox(
                "Sort Pipeline By:",
                options=["overall_score", "required_skills", "experience", "similarity"],
                format_func=lambda x: {
                    "overall_score": "Sort: Overall Match (%)",
                    "required_skills": "Sort: Required Skills",
                    "experience": "Sort: Experience Alignment",
                    "similarity": "Sort: Text Similarity"
                }[x],
                label_visibility="collapsed"
            )

        # Filter and sort candidate list
        ranked_list = rank_candidates(st.session_state.ranked_candidates, sort_by=sort_field)
        filtered_list = []
        for c in ranked_list:
            if tier_choice != "All Tiers" and c.get("category", {}).get("label") != tier_choice:
                continue
            if search_name and search_name.lower() not in c.get("candidate_name", "").lower():
                continue
            filtered_list.append(c)

        st.caption(f"Showing {len(filtered_list)} of {len(ranked_list)} candidate(s)")

        # Render Candidate Leaderboard Cards
        for c in filtered_list:
            cat = c.get("category", {})
            tier_class = f"tier-{cat.get('category_key', 'moderate')}"
            tier_label = cat.get("label", "Moderate Match")
            rank_num = c.get("rank", 1)

            display_name = c.get("candidate_name", "Candidate")
            display_email = c.get("candidate_profile", {}).get("email", "Not listed")
            avatar_text = get_initials(display_name)

            # Forensic status
            f_report = c.get("candidate_profile", {}).get("forensic_report") or {}
            fraud_score = f_report.get("fraud_score", 0.0)
            if fraud_score >= 30.0:
                security_badge = f"<span class='security-flagged'>⚠️ Tampering Risk: {fraud_score:g}%</span>"
            else:
                security_badge = "<span class='security-clean'>✓ Verified Document</span>"

            req_res = c.get("required_skills_result", {})
            exp_res = c.get("experience_result", {})
            cand_score = c.get("overall_score", 0)

            with st.container():
                st.markdown(
                    f"""
                    <div class="candidate-row-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div class="candidate-avatar-chip">{avatar_text}</div>
                                <div>
                                    <div class="candidate-name-header">
                                        <span>#{rank_num} {display_name}</span>
                                        {security_badge}
                                    </div>
                                    <div class="candidate-sub-meta">
                                        <span>{c.get('filename')}</span> &bull; <span>{display_email}</span> &bull; <span>{exp_res.get('candidate_years', 0):g} yrs experience</span>
                                    </div>
                                </div>
                            </div>
                            <div style="display: flex; align-items: center; gap: 14px;">
                                <div style="text-align: right;">
                                    <div style="font-size: 22px; font-weight: 700; color: var(--text-main);">{cand_score}%</div>
                                    <span class="tier-pill {tier_class}">{tier_label}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Action row beneath card
                ca1, ca2, ca3 = st.columns([2.5, 1.5, 1])
                with ca1:
                    matched_skills = req_res.get("matched", [])
                    if matched_skills:
                        chips = " ".join([f"<span class='skill-chip matched'>✓ {s}</span>" for s in matched_skills[:5]])
                        rem = len(matched_skills) - 5
                        if rem > 0:
                            chips += f" <span class='skill-chip'>+{rem} more</span>"
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.caption("No mandatory skills matched")
                with ca2:
                    st.caption(f"Mandatory: {req_res.get('matched_count', 0)}/{req_res.get('total_count', 0)} matched ({req_res.get('score', 0)}%)")
                with ca3:
                    if st.button("Inspect Profile", key=f"btn_inspect_{c.get('candidate_id')}", use_container_width=True):
                        st.session_state.selected_candidate_id = c.get("candidate_id")
                        st.session_state.nav_page = "👤 Candidate Inspector"
                        st.rerun()

                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

        # Export Actions
        st.markdown("<hr style='margin: 20px 0 12px 0; border: none; border-top: 1px solid #1e293b;'>", unsafe_allow_html=True)
        exp_col1, exp_col2, exp_col3 = st.columns([1.5, 1.5, 2])
        with exp_col1:
            csv_data = export_results_to_csv(st.session_state.ranked_candidates)
            st.download_button(
                "Export Ranking (CSV)",
                data=csv_data,
                file_name="recrumatch_candidates.csv",
                mime="text/csv",
                use_container_width=True
            )
        with exp_col2:
            report_md = generate_recruiter_markdown_report(
                st.session_state.ranked_candidates,
                st.session_state.jd_analysis if st.session_state.jd_analysis else {}
            )
            st.download_button(
                "Export Recruiter Report (Markdown)",
                data=report_md,
                file_name="recrumatch_recruiter_report.md",
                mime="text/markdown",
                use_container_width=True
            )


# =============================================================
# VIEW 2: CANDIDATE INSPECTOR (DEEP-DIVE PROFILE)
# =============================================================
elif menu_selection == "👤 Candidate Inspector":
    if not st.session_state.ranked_candidates:
        st.info("No candidates evaluated yet. Please upload resumes or load sample data.")
    else:
        # Candidate Selector Bar
        cand_lookup = {c["candidate_id"]: f"#{c['rank']} - {c['candidate_name']} ({c['overall_score']}%)" for c in st.session_state.ranked_candidates}
        cand_ids = list(cand_lookup.keys())
        curr_cand_id = st.session_state.selected_candidate_id if st.session_state.selected_candidate_id in cand_ids else cand_ids[0]
        curr_idx = cand_ids.index(curr_cand_id)

        col_nav_s, col_nav_prev, col_nav_next = st.columns([3, 1, 1])
        with col_nav_s:
            chosen_id = st.selectbox(
                "Select Candidate to Inspect:",
                options=cand_ids,
                format_func=lambda x: cand_lookup[x],
                index=curr_idx,
                label_visibility="collapsed"
            )
            if chosen_id != st.session_state.selected_candidate_id:
                st.session_state.selected_candidate_id = chosen_id
                st.rerun()
        with col_nav_prev:
            if st.button("Previous Candidate", disabled=(curr_idx <= 0), use_container_width=True):
                st.session_state.selected_candidate_id = cand_ids[curr_idx - 1]
                st.rerun()
        with col_nav_next:
            if st.button("Next Candidate", disabled=(curr_idx >= len(cand_ids) - 1), use_container_width=True):
                st.session_state.selected_candidate_id = cand_ids[curr_idx + 1]
                st.rerun()

        # Selected Candidate Assessment
        cand = next((c for c in st.session_state.ranked_candidates if c["candidate_id"] == st.session_state.selected_candidate_id), None)
        if cand:
            prof = cand.get("candidate_profile", {})
            cat = cand.get("category", {})
            tier_class = f"tier-{cat.get('category_key', 'moderate')}"
            tier_label = cat.get("label", "Moderate Match")

            # Header Profile Card
            c_name = cand.get("candidate_name", "Candidate")
            c_email = prof.get("email", "Not listed")
            c_phone = prof.get("phone", "Not listed")
            avatar_text = get_initials(c_name)

            st.markdown(
                f"""
                <div class="panel-card" style="margin-top: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
                        <div style="display: flex; align-items: center; gap: 14px;">
                            <div class="candidate-avatar-chip" style="width: 44px; height: 44px; font-size: 16px;">{avatar_text}</div>
                            <div>
                                <h3 style="margin: 0; font-size: 20px; font-weight: 700; color: var(--text-main);">{c_name}</h3>
                                <div style="font-size: 12px; color: var(--text-muted); margin-top: 3px;">
                                    <span>{cand.get('filename')}</span> &bull; <span>{c_email}</span> &bull; <span>{c_phone}</span>
                                </div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 28px; font-weight: 700; color: var(--text-main); line-height: 1;">{cand.get('overall_score')}%</div>
                            <span class="tier-pill {tier_class}" style="margin-top: 4px;">{tier_label}</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Profile Detail Tabs
            tab_overview, tab_skills, tab_velocity, tab_security, tab_interview, tab_raw = st.tabs([
                "Match Overview",
                "Skills & Inferred Graph",
                "Career Trajectory",
                "Document Security Audit",
                "Interview Kit",
                "Resume Text"
            ])

            # Tab 1: Match Overview
            with tab_overview:
                col_ov1, col_ov2 = st.columns([1.4, 1])
                with col_ov1:
                    st.markdown("##### Candidate Evaluation Summary")
                    st.markdown(
                        f"""
                        <div style="background: #0b1120; border: 1px solid #1e293b; border-radius: 6px; padding: 12px 14px; font-size: 13px; color: #cbd5e1; line-height: 1.6; margin-bottom: 14px;">
                            {cand.get('explanation_summary', 'Evaluation summary available upon scoring.')}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown("##### Key Strengths")
                    for s in cand.get("strengths", []):
                        st.markdown(f"✓ **{s}**")
                    if not cand.get("strengths"):
                        st.caption("No standout strengths detected")

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("##### Qualification Gaps")
                    for g in cand.get("gaps", []):
                        st.markdown(f"✗ **{g}**")
                    if not cand.get("gaps"):
                        st.caption("No significant qualification gaps identified")

                with col_ov2:
                    st.markdown("##### 5-Axis Qualification Radar")
                    req_score = cand.get("required_skills_result", {}).get("score", 0)
                    pref_score = cand.get("preferred_skills_result", {}).get("score", 0)
                    exp_score = cand.get("experience_result", {}).get("score", 0)
                    edu_score = cand.get("education_result", {}).get("score", 0)
                    sim_score = cand.get("similarity_result", {}).get("score", 0)

                    radar_fig = go.Figure()
                    radar_fig.add_trace(go.Scatterpolar(
                        r=[req_score, pref_score, exp_score, edu_score, sim_score],
                        theta=["Required Skills", "Preferred Skills", "Experience", "Education", "Text Similarity"],
                        fill='toself',
                        fillcolor='rgba(139, 92, 246, 0.2)',
                        line=dict(color='#8b5cf6', width=2),
                        marker=dict(color='#8b5cf6', size=5)
                    ))
                    radar_fig.update_layout(
                        polar=dict(
                            bgcolor="rgba(0,0,0,0)",
                            radialaxis=dict(visible=True, range=[0, 100], color="#64748b", gridcolor="#1e293b"),
                            angularaxis=dict(color="#94a3b8", gridcolor="#1e293b")
                        ),
                        showlegend=False,
                        margin=dict(l=30, r=30, t=20, b=20),
                        height=280,
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(family="Inter", size=11, color="#94a3b8")
                    )
                    st.plotly_chart(radar_fig, use_container_width=True)

            # Tab 2: Skills & Graph Reasoning
            with tab_skills:
                req_res = cand.get("required_skills_result", {})
                pref_res = cand.get("preferred_skills_result", {})

                st.markdown("##### Mandatory Skills Breakdown")
                if req_res.get("matched"):
                    st.markdown("**Matched:** " + " ".join([f"<span class='skill-chip matched'>✓ {s}</span>" for s in req_res.get("matched")]), unsafe_allow_html=True)
                if req_res.get("missing"):
                    st.markdown("**Missing:** " + " ".join([f"<span class='skill-chip missing'>✗ {s}</span>" for s in req_res.get("missing")]), unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("##### Inferred Competencies (Skill Dependency Graph)")
                st.caption("Skills the candidate likely possesses by implication, derived via ontology dependency graphs:")
                implicit = cand.get("candidate_profile", {}).get("implicit_skills") or infer_implicit_competencies(prof.get("skills", []))
                if implicit:
                    for imp in implicit[:6]:
                        conf = int(imp.get("confidence", 0.9) * 100)
                        st.markdown(f"• **{imp.get('inferred_skill')}** ({conf}% confidence) — derived from *{', '.join(imp.get('derived_from', []))}*")
                else:
                    st.caption("No implicit skills inferred")

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("##### All Extracted Skills")
                all_skills = prof.get("skills", [])
                st.markdown(" ".join([f"<span class='skill-chip'>{s}</span>" for s in all_skills]), unsafe_allow_html=True)

            # Tab 3: Career Trajectory
            with tab_velocity:
                vel = prof.get("career_velocity")
                if not vel:
                    vel = analyze_career_velocity(prof.get("raw_text", ""), prof.get("experience", {}).get("years", 0.0))

                vc1, vc2 = st.columns(2)
                with vc1:
                    st.markdown("##### Progression Trajectory")
                    st.markdown(f"**Status:** `{vel.get('trajectory', 'Stable Progression')}`")
                    st.markdown(f"**Role Tenure Average:** `{vel.get('average_tenure_years', 2.0)} years`")
                    st.markdown(f"**Stability Rating:** `{vel.get('stability_score', 80)} / 100`")
                with vc2:
                    st.markdown("##### Detected Trajectory Signals")
                    signals = vel.get("signals", ["Consistent professional tenure"])
                    for sig in signals:
                        st.markdown(f"• {sig}")

            # Tab 4: Document Security Audit
            with tab_security:
                f_rep = prof.get("forensic_report")
                if f_rep:
                    f_score = f_rep.get("fraud_score", 0.0)
                    hidden_kw = f_rep.get("hidden_keywords", [])
                    spoofed = f_rep.get("spoofed_words", [])
                    zw_chars = f_rep.get("zero_width_count", 0)

                    if f_score >= 30.0:
                        st.warning(f"⚠️ **Tampering Risk Flagged ({f_score:g}%)**: Hidden keyword injections or character substitutions were detected in this document.")
                    else:
                        st.success(f"✓ **Clean Document Verified ({f_score:g}%)**: No hidden white-text, micro-fonts, or homoglyphs detected.")

                    sm1, sm2, sm3 = st.columns(3)
                    sm1.metric("Risk Score", f"{f_score:g}%")
                    sm2.metric("Hidden Spans", len(hidden_kw))
                    sm3.metric("Homoglyphs", len(spoofed))

                    if hidden_kw:
                        st.markdown("##### Detected Hidden Spans (#FFFFFF or <2pt font)")
                        for item in hidden_kw[:6]:
                            st.markdown(f"• **\"{item.get('keyword')}\"** (Page {item.get('page')}) — {item.get('font_size')}pt font")

                    if spoofed:
                        st.markdown("##### Detected Character Substitutions (Homoglyphs)")
                        for s_item in spoofed[:6]:
                            st.markdown(f"• Word: `{s_item.get('original_word')}` → Normalized: `{s_item.get('normalized_word')}`")

                    with st.expander("Inspection Logs"):
                        for line in f_rep.get("logs", []):
                            st.text(f"• {line}")
                else:
                    st.info("Document security audit is supported for uploaded PDF resumes. This document is either DOCX format or clean.")

            # Tab 5: Interview Kit
            with tab_interview:
                kit = generate_interview_kit(cand, st.session_state.jd_analysis or {})
                st.markdown("##### Technical Verification Questions")
                st.caption("Tailored to probe candidate's claimed proficiencies:")
                for idx, q in enumerate(kit.get("verification_questions", []), 1):
                    st.markdown(f"**{idx}. [{q.get('skill').title()}]** {q.get('question')}")
                    st.caption(f"Look for: {q.get('look_for')}")

                gap_qs = kit.get("gap_probe_questions", [])
                if gap_qs:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("##### Qualification Gap Probe Questions")
                    st.caption("Questions to test capacity to bridge missing requirements:")
                    for idx, q in enumerate(gap_qs, 1):
                        st.markdown(f"**{idx}. [{q.get('missing_skill').title()}]** {q.get('question')}")
                        st.caption(f"Look for: {q.get('look_for')}")

                scenario = kit.get("seniority_scenario", {})
                if scenario:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("##### Problem Solving Scenario")
                    st.markdown(f"**Scenario:** {scenario.get('question')}")
                    st.caption(f"Evaluation Criteria: {scenario.get('evaluation_criteria')}")

            # Tab 6: Raw Text
            with tab_raw:
                st.markdown("##### Extracted Resume Text")
                st.text_area("Parsed Text Content", value=prof.get("raw_text", ""), height=300, disabled=True)


# =============================================================
# VIEW 3: JOB REQUISITIONS (TEMPLATES & CUSTOM CRITERIA)
# =============================================================
elif menu_selection == "📄 Job Requisitions":
    st.markdown("### Job Requisition & Criteria Management")
    st.caption("Select an industry role template, paste custom job requirements, or adjust qualification criteria.")

    tab_templates, tab_custom, tab_fine_tune = st.tabs([
        "Role Templates",
        "Paste Custom Job Description",
        "Fine-Tune Active Criteria"
    ])

    with tab_templates:
        col_t1, col_t2 = st.columns(2)
        for idx, (role_name, desc_text) in enumerate(JD_PRESETS.items()):
            col = col_t1 if idx % 2 == 0 else col_t2
            with col:
                st.markdown(
                    f"""
                    <div class="panel-card">
                        <div style="font-size: 15px; font-weight: 700; color: var(--text-main); margin-bottom: 6px;">{role_name}</div>
                        <div style="font-size: 12px; color: var(--text-muted); line-height: 1.5; max-height: 80px; overflow: hidden; margin-bottom: 12px;">
                            {desc_text[:220]}...
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button(f"Apply Role: {role_name}", key=f"btn_apply_role_{idx}", use_container_width=True):
                    apply_job_description(desc_text, role_title=role_name)
                    st.success(f"Applied '{role_name}' and updated applicant leaderboard.")
                    st.rerun()

    with tab_custom:
        custom_jd = st.text_area(
            "Paste Job Description:",
            value=st.session_state.jd_text,
            height=240,
            placeholder="Paste role requirements, mandatory skills, and experience criteria..."
        )
        if st.button("Analyze & Apply Job Description", type="primary"):
            if custom_jd.strip():
                apply_job_description(custom_jd, role_title="Custom Role Specification")
                st.success("Custom job description analyzed and applied.")
                st.rerun()
            else:
                st.error("Please enter job description text before applying.")

    with tab_fine_tune:
        analysis = st.session_state.jd_analysis
        if not analysis:
            st.info("No active job description loaded.")
        else:
            all_canonical = sorted(list(get_all_canonical_skills()))
            skill_options = sorted(list(set(all_canonical + analysis.get("required_skills", []) + analysis.get("preferred_skills", []))))

            ce1, ce2 = st.columns(2)
            with ce1:
                new_req = st.multiselect(
                    "Mandatory Skills (Highest Weight - 40%):",
                    options=skill_options,
                    default=analysis.get("required_skills", [])
                )
                new_pref = st.multiselect(
                    "Preferred Skills (15% Weight):",
                    options=skill_options,
                    default=analysis.get("preferred_skills", [])
                )
            with ce2:
                new_exp = st.number_input(
                    "Target Experience (Years):",
                    min_value=0.0,
                    max_value=25.0,
                    value=float(analysis.get("min_experience_years", 0.0)),
                    step=0.5
                )
                edu_opts = ["Not specified", "Bachelor's", "Master's", "Ph.D.", "Associate"]
                curr_edu = analysis.get("education_degree", "Not specified")
                edu_idx = edu_opts.index(curr_edu) if curr_edu in edu_opts else 0
                new_edu = st.selectbox("Education Level:", options=edu_opts, index=edu_idx)

            if st.button("Save Criteria & Re-Score Applicants", type="primary"):
                st.session_state.jd_analysis["required_skills"] = new_req
                st.session_state.jd_analysis["preferred_skills"] = new_pref
                st.session_state.jd_analysis["min_experience_years"] = new_exp
                st.session_state.jd_analysis["education_degree"] = new_edu
                st.session_state.jd_analysis["all_skills"] = list(dict.fromkeys(new_req + new_pref))

                if st.session_state.uploaded_resumes:
                    assessments = [
                        generate_candidate_assessment(
                            p, st.session_state.jd_analysis,
                            weights=st.session_state.weights,
                            thresholds=st.session_state.thresholds,
                            matching_method=st.session_state.matching_method
                        )
                        for p in st.session_state.uploaded_resumes
                    ]
                    st.session_state.ranked_candidates = rank_candidates(assessments)
                st.success("Criteria updated and candidate scores recalculated.")
                st.rerun()


# =============================================================
# VIEW 4: RESUME INGESTION (UPLOAD & BATCH PARSING)
# =============================================================
elif menu_selection == "📥 Resume Ingestion":
    st.markdown("### Resume Ingestion & Batch Screening")
    st.caption("Upload multiple candidate resumes in PDF, DOCX, or TXT format to evaluate against the active role criteria.")

    uploaded_files = st.file_uploader(
        "Select candidate resumes:",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Supported formats: .pdf, .docx, .txt"
    )

    if uploaded_files:
        st.markdown(f"##### Upload Queue ({len(uploaded_files)} files)")
        new_profiles = []
        inspector = ResumeForensicInspector()

        for file in uploaded_files:
            fname = file.name
            forensic_report = None

            if fname.lower().endswith(".pdf"):
                try:
                    file_bytes = file.read()
                    file.seek(0)
                    forensic_report = inspector.inspect_pdf(file_bytes, filename=fname)
                    file.seek(0)
                except Exception:
                    file.seek(0)
                parse_res = extract_text_from_pdf(file)
            elif fname.lower().endswith(".docx"):
                try:
                    forensic_report = inspector.inspect_docx(file, filename=fname)
                    file.seek(0)
                except Exception:
                    file.seek(0)
                parse_res = extract_text_from_docx(file)
            elif fname.lower().endswith(".txt"):
                try:
                    txt = file.read().decode("utf-8")
                except Exception:
                    file.seek(0)
                    txt = file.read().decode("latin-1", errors="ignore")
                forensic_report = inspector.inspect_text(txt, filename=fname)
                parse_res = {"success": True, "text": txt}
            else:
                parse_res = {"success": False, "error": "Unsupported file format."}

            if parse_res["success"]:
                clean_text = forensic_report["clean_text"] if (forensic_report and forensic_report.get("clean_text")) else parse_res["text"]
                sk_info = extract_skills_from_text(clean_text)
                profile = parse_resume_content(clean_text)
                if not profile.get("candidate_name") or profile.get("candidate_name") in ("Not detected", "Candidate", "Unknown"):
                    import re
                    base = fname.rsplit(".", 1)[0]
                    base = re.sub(r"[_\-]+", " ", base)
                    base = re.sub(r"\b(resume|cv|senior|junior|lead|dev|developer|engineer|scientist|analyst|fullstack|backend|frontend|python|java|cloud|devops|data|adversarial|exploit|clean)\b", "", base, flags=re.IGNORECASE)
                    cleaned = " ".join(base.split()).strip()
                    if len(cleaned) >= 2:
                        profile["candidate_name"] = cleaned.title()
                    else:
                        profile["candidate_name"] = f"Candidate {len(new_profiles) + 1}"
                profile["skills"] = sk_info["skills"]
                profile["filename"] = fname
                profile["candidate_id"] = fname.replace(".", "_")
                profile["forensic_report"] = forensic_report
                exp_yrs = float(profile.get("experience", {}).get("years", 0.0))
                profile["career_velocity"] = analyze_career_velocity(clean_text, exp_yrs)
                profile["implicit_skills"] = infer_implicit_competencies(profile["skills"])
                new_profiles.append(profile)

                f_score = forensic_report.get("fraud_score", 0.0) if forensic_report else 0.0
                status_badge = f"<span class='security-flagged'>⚠️ Tampering: {f_score:g}%</span>" if f_score >= 30.0 else "<span class='security-clean'>✓ Clean Document</span>"

                st.markdown(
                    f"""
                    <div class="panel-card" style="margin-bottom: 8px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <b>{fname}</b> &bull; <span style="color: var(--text-muted); font-size: 12px;">Candidate: {profile.get('candidate_name', 'Unknown')}</span>
                            &nbsp; {status_badge}
                        </div>
                        <div style="font-size: 12px; color: #34d399;">{sk_info['total_count']} skills extracted</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error(f"Failed to parse {fname}: {parse_res.get('error')}")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Screen & Rank Uploaded Resumes", type="primary", use_container_width=True):
            if new_profiles:
                st.session_state.uploaded_resumes = new_profiles
                if not st.session_state.jd_analysis:
                    st.session_state.jd_analysis = analyze_job_description(st.session_state.jd_text or "")

                assessments = [
                    generate_candidate_assessment(
                        p, st.session_state.jd_analysis,
                        weights=st.session_state.weights,
                        thresholds=st.session_state.thresholds,
                        matching_method=st.session_state.matching_method
                    )
                    for p in new_profiles
                ]
                st.session_state.ranked_candidates = rank_candidates(assessments)
                st.session_state.nav_page = "🎯 Candidate Pipeline"
                st.success(f"Successfully screened and ranked {len(st.session_state.ranked_candidates)} candidates.")
                st.rerun()
    else:
        st.info("Drop resumes above, or click **Load Sample Data** in the sidebar to test sample applicants.")


# =============================================================
# VIEW 5: SCORING PREFERENCES (WEIGHTS & THRESHOLDS)
# =============================================================
elif menu_selection == "⚙️ Scoring Preferences":
    st.markdown("### Evaluation Weights & Threshold Preferences")
    st.caption("Adjust the mathematical scoring weights and tier thresholds to reflect role seniority and hiring priorities.")

    curr_w = st.session_state.weights
    curr_th = st.session_state.thresholds

    col_sw1, col_sw2 = st.columns(2)
    with col_sw1:
        st.markdown("##### Evaluation Component Weights")
        w_req = st.slider("Required Skills Weight (%)", 0, 100, int(curr_w.get("required_skills", 0.40) * 100), step=5)
        w_pref = st.slider("Preferred Skills Weight (%)", 0, 100, int(curr_w.get("preferred_skills", 0.15) * 100), step=5)
        w_exp = st.slider("Experience Alignment Weight (%)", 0, 100, int(curr_w.get("experience", 0.15) * 100), step=5)
        w_edu = st.slider("Education Degree Weight (%)", 0, 100, int(curr_w.get("education", 0.10) * 100), step=5)
        w_sim = st.slider("Text Similarity Weight (%)", 0, 100, int(curr_w.get("similarity", 0.20) * 100), step=5)

        total_w = w_req + w_pref + w_exp + w_edu + w_sim
        if total_w == 100:
            st.caption("✓ Total Weight: 100% (Balanced)")
        else:
            st.caption(f"Current Total: {total_w}% (Will be normalized to 100% on save)")

    with col_sw2:
        st.markdown("##### Match Tier Cutoff Thresholds")
        th_exc = st.slider("Excellent Match Cutoff (%)", 60, 95, int(curr_th.get("excellent", 80.0)), step=5)
        th_good = st.slider("Good Match Cutoff (%)", 40, 80, int(curr_th.get("good", 60.0)), step=5)
        th_mod = st.slider("Moderate Match Cutoff (%)", 20, 60, int(curr_th.get("moderate", 40.0)), step=5)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("##### Text Similarity Algorithm")
        sbert_ok = is_sbert_available()
        algo_choice = st.radio(
            "Vector Engine:",
            options=["TF-IDF (Cosine - Fast & Offline)", "Sentence-Transformers / SBERT (Semantic)"] if sbert_ok else ["TF-IDF (Cosine - Fast & Offline)"],
            index=0
        )

    st.markdown("<hr style='margin: 18px 0; border: none; border-top: 1px solid #1e293b;'>", unsafe_allow_html=True)
    btn_s1, btn_s2 = st.columns([1.5, 1])
    with btn_s1:
        if st.button("Save Preferences & Re-Score", type="primary", use_container_width=True):
            norm = (total_w / 100.0) if total_w > 0 else 1.0
            new_weights = {
                "required_skills": (w_req / 100.0) / norm,
                "preferred_skills": (w_pref / 100.0) / norm,
                "experience": (w_exp / 100.0) / norm,
                "education": (w_edu / 100.0) / norm,
                "similarity": (w_sim / 100.0) / norm,
            }
            new_thresholds = {
                "excellent": float(th_exc),
                "good": float(th_good),
                "moderate": float(th_mod),
            }
            st.session_state.weights = new_weights
            st.session_state.thresholds = new_thresholds
            st.session_state.matching_method = "SBERT" if "SBERT" in algo_choice and sbert_ok else "TF-IDF"

            if st.session_state.uploaded_resumes and st.session_state.jd_analysis:
                assessments = [
                    generate_candidate_assessment(
                        p, st.session_state.jd_analysis,
                        weights=new_weights,
                        thresholds=new_thresholds,
                        matching_method=st.session_state.matching_method
                    )
                    for p in st.session_state.uploaded_resumes
                ]
                st.session_state.ranked_candidates = rank_candidates(assessments)
            st.success("Preferences saved and applicant ranking recomputed.")
            st.rerun()

    with btn_s2:
        if st.button("Reset to Default Weights", use_container_width=True):
            st.session_state.weights = DEFAULT_WEIGHTS.copy()
            st.session_state.thresholds = DEFAULT_THRESHOLDS.copy()
            st.session_state.matching_method = "TF-IDF"
            if st.session_state.uploaded_resumes and st.session_state.jd_analysis:
                assessments = [
                    generate_candidate_assessment(
                        p, st.session_state.jd_analysis,
                        weights=DEFAULT_WEIGHTS,
                        thresholds=DEFAULT_THRESHOLDS,
                        matching_method="TF-IDF"
                    )
                    for p in st.session_state.uploaded_resumes
                ]
                st.session_state.ranked_candidates = rank_candidates(assessments)
            st.info("Reset weights to 40/15/15/10/20 default balance.")
            st.rerun()
