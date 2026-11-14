"""Automated test suite for FastAPI REST API endpoints."""

import os
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert data["author"] == "Yuvraj Saini"
    assert data["canonical_skills_count"] > 100
    print("[PASS] Health endpoint passed!")

def test_skills():
    response = client.get("/api/skills")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["skills"]) > 100
    assert "Python" in data["skills"]
    print("[PASS] Skills taxonomy endpoint passed!")

def test_parse_jd():
    sample_jd = """
    Job Title: Senior Python & Machine Learning Engineer
    Required Skills: Python, SQL, Machine Learning, Pandas, Scikit-learn, Git
    Preferred Skills: Docker, AWS, FastAPI
    Experience: Minimum 4+ years of hands-on experience
    Education: Bachelor's degree in Computer Science
    """
    response = client.post("/api/parse-jd", json={"jd_text": sample_jd})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    req_skills = data["data"]["required_skills"]
    assert "Python" in req_skills
    assert "Machine Learning" in req_skills
    assert data["data"]["min_experience_years"] == 4.0
    print("[PASS] Parse JD endpoint passed!")

def test_screen_resumes():
    sample_dir = os.path.join(os.path.dirname(__file__), "data", "sample_resumes")
    files_to_test = [
        ("resumes", ("Aman_Verma_Senior_Python_Dev.pdf", open(os.path.join(sample_dir, "Aman_Verma_Senior_Python_Dev.pdf"), "rb"), "application/pdf")),
        ("resumes", ("Rahul_Kumar_Junior_Web_Dev.docx", open(os.path.join(sample_dir, "Rahul_Kumar_Junior_Web_Dev.docx"), "rb"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))
    ]

    jd_text = """
    Job Title: Senior Python & Machine Learning Engineer
    Required Skills: Python, SQL, Machine Learning, Pandas, Scikit-learn, Git
    Preferred Skills: Docker, AWS, FastAPI
    Experience: Minimum 4+ years of hands-on experience
    Education: Bachelor's degree in Computer Science
    """

    response = client.post(
        "/api/screen-resumes",
        data={"jd_text": jd_text, "matching_method": "tfidf"},
        files=files_to_test
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["processed_count"] == 2
    assert len(data["leaderboard"]) == 2
    top_cand = data["leaderboard"][0]
    assert "overall_score" in top_cand
    assert top_cand["candidate_name"] != "Not detected"
    print(f"[PASS] Screen Resumes endpoint passed! Top Candidate: {top_cand['candidate_name']} ({top_cand['overall_score']}%)")

if __name__ == "__main__":
    test_health()
    test_skills()
    test_parse_jd()
    test_screen_resumes()
    print("\n[ALL TESTS PASSED] FASTAPI REST ENDPOINTS VERIFIED SUCCESSFULLY!")
