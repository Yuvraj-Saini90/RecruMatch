"""Comprehensive test script to audit all operational and edge cases."""

import io
import os
from src.pdf_parser import extract_text_from_pdf
from src.docx_parser import extract_text_from_docx
from src.skill_extractor import extract_skills_from_text
from src.nlp_processor import parse_resume_content
from src.jd_analyzer import analyze_job_description
from src.scorer import generate_candidate_assessment
from src.ranking import rank_candidates, compute_dashboard_metrics
from src.export_utils import export_results_to_csv, generate_recruiter_markdown_report


def run_audit():
    results = {}

    # Case 1: Single Resume flow
    print("--- Testing Single Resume Flow ---")
    single_text = """John Doe
    Email: john.doe@email.com | Phone: 9876543210
    Education: B.Tech in Computer Science from XYZ University 2022
    Experience: 2 years as Python Developer
    Skills: Python, Django, SQL, Git
    """
    p_single = parse_resume_content(single_text)
    p_single["skills"] = extract_skills_from_text(single_text)["skills"]
    p_single["filename"] = "john_doe.pdf"
    p_single["candidate_id"] = "john_1"

    jd_single = analyze_job_description("Looking for Python and SQL developer with 1+ year experience. B.Tech required.")
    ass_single = generate_candidate_assessment(p_single, jd_single)
    ranked_single = rank_candidates([ass_single])
    metrics_single = compute_dashboard_metrics(ranked_single, jd_single)
    results["single_resume"] = len(ranked_single) == 1 and metrics_single["total_candidates"] == 1
    print(f"Single Resume: Success={results['single_resume']}, Score={ass_single['overall_score']}%")

    # Case 2: Multiple Resumes (4 demo resumes)
    print("\n--- Testing Multiple Resumes Flow ---")
    base_dir = r"c:\Users\Yoru\OneDrive\Desktop\M_P"
    resumes_dir = os.path.join(base_dir, "data", "sample_resumes")
    profiles = []
    for f in os.listdir(resumes_dir):
        path = os.path.join(resumes_dir, f)
        if f.endswith(".pdf"):
            res = extract_text_from_pdf(path)
        elif f.endswith(".docx"):
            res = extract_text_from_docx(path)
        else:
            continue
        if res["success"]:
            prof = parse_resume_content(res["text"])
            prof["skills"] = extract_skills_from_text(res["text"])["skills"]
            prof["filename"] = f
            prof["candidate_id"] = f.replace(".", "_")
            profiles.append(prof)
    
    with open(os.path.join(base_dir, "data", "sample_job_description.txt"), "r", encoding="utf-8") as jf:
        real_jd = analyze_job_description(jf.read())
    
    ranked_multi = rank_candidates([generate_candidate_assessment(p, real_jd) for p in profiles])
    metrics_multi = compute_dashboard_metrics(ranked_multi, real_jd)
    results["multiple_resumes"] = len(ranked_multi) >= 4 and metrics_multi["top_candidate"] is not None
    print(f"Multiple Resumes: Success={results['multiple_resumes']}, Count={len(ranked_multi)}")

    # Case 3: Different Job Descriptions
    print("\n--- Testing Diverse JDs ---")
    # 3a: Completely unstructured/short JD
    jd_unstructured = analyze_job_description("Need a React frontend developer")
    ass_react = generate_candidate_assessment(profiles[0], jd_unstructured)
    results["unstructured_jd"] = ass_react["overall_score"] is not None
    print(f"Unstructured JD: Score={ass_react['overall_score']}%, ReqSkills={jd_unstructured['required_skills']}")

    # 3b: JD with zero skills mentioned
    jd_no_skills = analyze_job_description("Hiring an office assistant with good communication and punctuality.")
    ass_no_skills = generate_candidate_assessment(profiles[0], jd_no_skills)
    results["no_skills_jd"] = ass_no_skills["overall_score"] is not None
    print(f"No Skills in JD: Score={ass_no_skills['overall_score']}%, ReqScore={ass_no_skills['required_skills_result']['score']}%")

    # 3c: JD with 10+ years experience requirement
    jd_high_exp = analyze_job_description("Senior Principal Architect. Minimum 10+ years of professional experience required.")
    ass_high_exp = generate_candidate_assessment(profiles[0], jd_high_exp)
    results["high_exp_jd"] = ass_high_exp["experience_result"]["score"] < 100.0
    print(f"High Exp JD: CandExp={ass_high_exp['experience_result']['candidate_years']}, ExpScore={ass_high_exp['experience_result']['score']}%")

    # Case 4: Edge Cases / Corrupted / Empty files
    print("\n--- Testing Corrupted / Empty files ---")
    corrupt_pdf = extract_text_from_pdf(io.BytesIO(b"%PDF-1.4 truncated corrupt content"))
    results["corrupt_pdf_handled"] = not corrupt_pdf["success"] and corrupt_pdf["error"] is not None

    corrupt_docx = extract_text_from_docx(io.BytesIO(b"PK corrupt docx binary"))
    results["corrupt_docx_handled"] = not corrupt_docx["success"] and corrupt_docx["error"] is not None

    zero_byte_pdf = extract_text_from_pdf(io.BytesIO(b""))
    results["zero_byte_pdf"] = not zero_byte_pdf["success"]

    # Case 5: Resumes with unusual or missing content
    print("\n--- Testing Unusual Resume Content ---")
    # 5a: Resume with no name detected (only skills)
    no_name_text = "skills: python, java, sql. experience: 2 years."
    prof_no_name = parse_resume_content(no_name_text)
    results["no_name"] = prof_no_name["candidate_name"] == "Not detected"

    # 5b: Single word name or all-caps name
    single_word_text = "CHER\nEmail: cher@music.com\nSkills: Python"
    prof_single_word = parse_resume_content(single_word_text)
    print(f"Single word name detection: '{prof_single_word['candidate_name']}'")

    # 5c: Resume with zero skills
    zero_skill_text = "Jane Smith\nHistory major with extensive background in medieval literature and latin translation."
    prof_zero_sk = parse_resume_content(zero_skill_text)
    prof_zero_sk["skills"] = extract_skills_from_text(zero_skill_text)["skills"]
    ass_zero_sk = generate_candidate_assessment(prof_zero_sk, real_jd)
    results["zero_skills"] = ass_zero_sk["overall_score"] < 40.0
    print(f"Zero skill candidate score: {ass_zero_sk['overall_score']}% (Category: {ass_zero_sk['category']['label']})")

    # 5d: Scanned/Image PDF limitation check
    print("\n[NOTE] Scanned image PDFs cannot be parsed via pdfplumber without OCR (pytesseract/pdf2image).")

    print("\n--- SUMMARY OF AUDIT RUN ---")
    for k, v in results.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    run_audit()
