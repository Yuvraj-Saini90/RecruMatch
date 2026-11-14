"""FastAPI REST API Server for Smart Resume Screening & Candidate Ranking Tool.

Academic REST Backend:
- Author: Yuvraj Saini
- Supervisor: Mr. Ashwini Kr. Verma
- Institution: Greater Noida Institute of Technology (GNIOT)

Provides decoupled REST API endpoints for resume ingestion, NLP parsing,
job description extraction, and explainable candidate ranking.
Auto-generated interactive Swagger UI documentation available at: /docs
"""

import os
import json
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.config import (
    APP_TITLE, APP_SUBTITLE, PROJECT_INFO,
    DEFAULT_WEIGHTS, DEFAULT_THRESHOLDS
)
from src.pdf_parser import extract_text_from_pdf
from src.docx_parser import extract_text_from_docx
from src.skill_extractor import extract_skills_from_text
from src.skill_dictionary import get_all_canonical_skills
from src.nlp_processor import parse_resume_content
from src.jd_analyzer import analyze_job_description
from src.similarity_engine import is_sbert_available
from src.scorer import generate_candidate_assessment
from src.ranking import rank_candidates, compute_dashboard_metrics

app = FastAPI(
    title="Smart Resume Screening & Candidate Ranking API",
    description="Explainable HR-Tech candidate screening REST API with deterministic multi-criteria scoring.",
    version="1.0.0",
    contact={
        "name": PROJECT_INFO.get("developer", "Yuvraj Saini"),
        "institution": PROJECT_INFO.get("institution", "GNIOT"),
        "supervisor": PROJECT_INFO.get("supervisor", "Mr. Ashwini Kr. Verma")
    }
)

# Enable CORS for cross-origin frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------
# PYDANTIC SCHEMAS
# -------------------------------------------------------------
class ParseJDRequest(BaseModel):
    jd_text: str = Field(..., description="Raw text of the job description to analyze.")


class HealthResponse(BaseModel):
    status: str
    app_title: str
    author: str
    supervisor: str
    institution: str
    sbert_available: bool
    canonical_skills_count: int


# -------------------------------------------------------------
# REST ENDPOINTS
# -------------------------------------------------------------
@app.get("/api/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """System health check and metadata endpoint."""
    return HealthResponse(
        status="operational",
        app_title=APP_TITLE,
        author=PROJECT_INFO.get("developer", "Yuvraj Saini"),
        supervisor=PROJECT_INFO.get("supervisor", "Mr. Ashwini Kr. Verma"),
        institution=PROJECT_INFO.get("institution", "GNIOT"),
        sbert_available=is_sbert_available(),
        canonical_skills_count=len(get_all_canonical_skills())
    )


@app.get("/api/skills", tags=["Skills"])
def list_canonical_skills():
    """Retrieve all normalized technical skills supported by the system taxonomy."""
    skills = sorted(list(get_all_canonical_skills()))
    return {
        "status": "success",
        "total_skills": len(skills),
        "skills": skills
    }


@app.post("/api/parse-jd", tags=["Job Description"])
def parse_job_description_endpoint(payload: ParseJDRequest):
    """Analyze a raw Job Description and extract structured requirements."""
    if not payload.jd_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description text cannot be empty."
        )

    analysis = analyze_job_description(payload.jd_text)
    return {
        "status": "success",
        "data": analysis
    }


@app.post("/api/screen-resumes", tags=["Candidate Screening"])
async def screen_resumes_endpoint(
    resumes: List[UploadFile] = File(..., description="Candidate resumes in PDF or DOCX format"),
    jd_text: Optional[str] = Form(None, description="Pasted Job Description text"),
    jd_file: Optional[UploadFile] = File(None, description="Optional Job Description file (.pdf, .docx, .txt)"),
    matching_method: str = Form("tfidf", description="Matching method: 'tfidf' or 'sbert'"),
    custom_weights_json: Optional[str] = Form(None, description="Optional JSON string of custom weights")
):
    """Screen a batch of resumes against a Job Description.
    
    Returns explainable qualification scores, detailed breakdown, and candidate rankings.
    """
    if not resumes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one candidate resume file is required."
        )

    # 1. Resolve Job Description text
    resolved_jd_text = ""
    if jd_text and jd_text.strip():
        resolved_jd_text = jd_text.strip()
    elif jd_file is not None:
        fname = jd_file.filename.lower()
        content = await jd_file.read()
        import io
        if fname.endswith(".pdf"):
            res = extract_text_from_pdf(io.BytesIO(content))
            if res["success"]:
                resolved_jd_text = res["text"]
        elif fname.endswith(".docx"):
            res = extract_text_from_docx(io.BytesIO(content))
            if res["success"]:
                resolved_jd_text = res["text"]
        elif fname.endswith(".txt"):
            try:
                resolved_jd_text = content.decode("utf-8")
            except Exception:
                resolved_jd_text = content.decode("latin-1", errors="ignore")

    if not resolved_jd_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A valid Job Description must be provided via 'jd_text' or 'jd_file'."
        )

    # 2. Parse weights if provided
    weights = DEFAULT_WEIGHTS.copy()
    if custom_weights_json:
        try:
            custom_weights = json.loads(custom_weights_json)
            weights.update(custom_weights)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid custom_weights_json. Must be a valid JSON object."
            )

    # 3. Analyze Job Description
    jd_analysis = analyze_job_description(resolved_jd_text)

    # 4. Ingest and parse each candidate resume
    candidate_profiles = []
    file_errors = []

    for resume_file in resumes:
        fname = resume_file.filename
        raw_bytes = await resume_file.read()
        import io
        file_stream = io.BytesIO(raw_bytes)

        if fname.lower().endswith(".pdf"):
            parse_res = extract_text_from_pdf(file_stream)
        elif fname.lower().endswith(".docx"):
            parse_res = extract_text_from_docx(file_stream)
        elif fname.lower().endswith(".txt"):
            try:
                txt_content = raw_bytes.decode("utf-8")
            except Exception:
                txt_content = raw_bytes.decode("latin-1", errors="ignore")
            parse_res = {"success": True, "text": txt_content}
        else:
            file_errors.append({"filename": fname, "error": "Unsupported file format. Must be .pdf, .docx, or .txt."})
            continue

        if not parse_res["success"]:
            file_errors.append({"filename": fname, "error": parse_res.get("error", "Extraction failed.")})
            continue

        raw_text = parse_res["text"]
        sk_info = extract_skills_from_text(raw_text)
        profile = parse_resume_content(raw_text)
        profile["skills"] = sk_info["skills"]
        profile["filename"] = fname
        profile["candidate_id"] = fname.replace(".", "_")
        candidate_profiles.append(profile)

    if not candidate_profiles:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"message": "Could not extract valid text from any uploaded resume.", "errors": file_errors}
        )

    # 5. Score and rank candidates
    assessments = [
        generate_candidate_assessment(
            p, jd_analysis,
            weights=weights,
            thresholds=DEFAULT_THRESHOLDS,
            matching_method=matching_method
        )
        for p in candidate_profiles
    ]

    ranked_candidates = rank_candidates(assessments)
    metrics = compute_dashboard_metrics(ranked_candidates, jd_analysis)

    return {
        "status": "success",
        "processed_count": len(ranked_candidates),
        "failed_files": file_errors,
        "job_description_criteria": {
            "required_skills": jd_analysis["required_skills"],
            "preferred_skills": jd_analysis["preferred_skills"],
            "min_experience_years": jd_analysis["min_experience_years"],
            "education_degree": jd_analysis["education_degree"]
        },
        "dashboard_metrics": metrics,
        "leaderboard": ranked_candidates
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
