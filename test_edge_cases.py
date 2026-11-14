"""Verification script for edge cases and error resilience."""

import os
import io
from src.pdf_parser import extract_text_from_pdf
from src.docx_parser import extract_text_from_docx
from src.skill_extractor import extract_skills_from_text
from src.nlp_processor import parse_resume_content
from src.jd_analyzer import analyze_job_description
from src.scorer import generate_candidate_assessment
from src.ranking import rank_candidates


def test_edge_cases():
    print("=== Testing Edge Cases & Robustness ===")

    # 1. Empty / Corrupted PDF
    empty_pdf = io.BytesIO(b"")
    pdf_res = extract_text_from_pdf(empty_pdf)
    assert not pdf_res["success"], "Empty PDF should not report success"
    assert pdf_res["error"] is not None
    print("[PASS] Empty/corrupted PDF handled safely without crashing.")

    # 2. Corrupted DOCX
    corrupted_docx = io.BytesIO(b"This is not a zip or docx file")
    docx_res = extract_text_from_docx(corrupted_docx)
    assert not docx_res["success"], "Corrupted DOCX should not report success"
    assert docx_res["error"] is not None
    print("[PASS] Corrupted DOCX handled safely without crashing.")

    # 3. Resume with zero skills / blank text
    blank_profile = parse_resume_content("")
    blank_profile["skills"] = []
    blank_profile["filename"] = "blank_resume.pdf"
    blank_profile["candidate_id"] = "blank_1"
    assert blank_profile["candidate_name"] == "Not detected"
    print("[PASS] Blank resume handled cleanly with 'Not detected' values.")

    # 4. Completely empty Job Description
    empty_jd = analyze_job_description("")
    assert empty_jd["required_skills"] == []
    print("[PASS] Empty Job Description handled safely.")

    # 5. Score blank profile against empty JD
    assessment = generate_candidate_assessment(blank_profile, empty_jd)
    assert assessment["overall_score"] is not None
    print(f"[PASS] Blank candidate vs Empty JD evaluated safely (Score: {assessment['overall_score']}%).")

    # 6. Candidate with no experience mentioned against 5+ yrs requirement
    strict_jd = analyze_job_description("Required Skills: Python, SQL\nMinimum 5 years experience required.\nBachelor's in Computer Science.")
    assessment_strict = generate_candidate_assessment(blank_profile, strict_jd)
    assert assessment_strict["overall_score"] is not None
    print(f"[PASS] Blank candidate vs strict JD evaluated safely (Score: {assessment_strict['overall_score']}%).")

    # 7. Ranking with empty list
    empty_ranked = rank_candidates([])
    assert empty_ranked == []
    print("[PASS] Empty candidate list ranking handled safely.")

    print("\nALL EDGE CASE TESTS PASSED!")


if __name__ == "__main__":
    test_edge_cases()
