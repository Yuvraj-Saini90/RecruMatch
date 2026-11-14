"""End-to-end unit and verification test for resume screening pipeline."""

import os
import glob
from src.pdf_parser import extract_text_from_pdf
from src.docx_parser import extract_text_from_docx
from src.skill_extractor import extract_skills_from_text
from src.nlp_processor import parse_resume_content
from src.jd_analyzer import analyze_job_description
from src.scorer import generate_candidate_assessment
from src.ranking import rank_candidates, compute_dashboard_metrics
from src.export_utils import export_results_to_csv, generate_recruiter_markdown_report


def run_test():
    print("=== Testing Pipeline ===")
    base_dir = r"c:\Users\Yoru\OneDrive\Desktop\M_P"
    jd_file = os.path.join(base_dir, "data", "sample_job_description.txt")
    with open(jd_file, "r", encoding="utf-8") as f:
        jd_text = f.read()

    print("\n1. Analyzing Job Description...")
    jd_analysis = analyze_job_description(jd_text)
    print(f"Required Skills ({len(jd_analysis['required_skills'])}): {jd_analysis['required_skills']}")
    print(f"Preferred Skills ({len(jd_analysis['preferred_skills'])}): {jd_analysis['preferred_skills']}")
    print(f"Min Experience: {jd_analysis['min_experience_years']} years")
    print(f"Target Education: {jd_analysis['education_degree']}")

    resume_files = glob.glob(os.path.join(base_dir, "data", "sample_resumes", "*.*"))
    print(f"\n2. Found {len(resume_files)} resumes.")

    profiles = []
    for filepath in resume_files:
        filename = os.path.basename(filepath)
        print(f"\nParsing: {filename}")
        
        if filepath.endswith(".pdf"):
            parse_res = extract_text_from_pdf(filepath)
        elif filepath.endswith(".docx"):
            parse_res = extract_text_from_docx(filepath)
        else:
            continue

        assert parse_res["success"], f"Failed to parse {filename}: {parse_res['error']}"
        raw_text = parse_res["text"]
        print(f"Extracted {len(raw_text)} chars of text.")

        # Skills
        sk_res = extract_skills_from_text(raw_text)
        print(f"Found {sk_res['total_count']} skills: {sk_res['skills']}")

        # NLP
        profile = parse_resume_content(raw_text)
        profile["skills"] = sk_res["skills"]
        profile["filename"] = filename
        profile["candidate_id"] = filename.replace(".", "_")
        print(f"Candidate: {profile['candidate_name']} | Email: {profile['email']} | Phone: {profile['phone']}")
        print(f"Experience: {profile['experience']['summary']}")
        print(f"Education: {profile['education']['details_summary']}")

        profiles.append(profile)

    print("\n3. Scoring Candidates...")
    assessments = []
    for p in profiles:
        assessment = generate_candidate_assessment(p, jd_analysis)
        assessments.append(assessment)

    ranked = rank_candidates(assessments)

    print("\n=== Candidate Ranking Results ===")
    for c in ranked:
        print(f"Rank #{c['rank']}: {c['candidate_name']} ({c['filename']}) - Score: {c['overall_score']}% ({c['category']['label']})")
        print(f"   Required: {c['required_skills_result']['score']}% | Pref: {c['preferred_skills_result']['score']}% | Exp: {c['experience_result']['score']}% | Edu: {c['education_result']['score']}% | Sim: {c['similarity_result']['score']}%")
        print(f"   Matched: {c['required_skills_result']['matched']}")
        print(f"   Missing: {c['required_skills_result']['missing']}")

    metrics = compute_dashboard_metrics(ranked, jd_analysis)
    print(f"\nDashboard Metrics: Total={metrics['total_candidates']}, Avg={metrics['average_score']}%, Strong Matches={metrics['strong_matches_count']}")

    csv_data = export_results_to_csv(ranked)
    assert len(csv_data) > 100, "CSV export failed"
    print("\nCSV export generated successfully.")

    report_md = generate_recruiter_markdown_report(ranked, jd_analysis)
    assert len(report_md) > 100, "Report markdown generation failed"
    print("Report markdown generated successfully.")

    print("\nALL BACKEND PIPELINE TESTS PASSED!")


if __name__ == "__main__":
    run_test()
