"""Job Description analyzer extracting required/preferred skills, experience, and education."""

import re
from typing import Dict, Any, List
from src.skill_extractor import extract_skills_from_text


def analyze_job_description(jd_text: str) -> Dict[str, Any]:
    """Analyze Job Description text to extract structured requirements.
    
    Identifies:
    - Required skills
    - Preferred / nice-to-have skills
    - Minimum required years of experience
    - Minimum education requirement
    - Certifications
    """
    if not jd_text or not jd_text.strip():
        return {
            "required_skills": [],
            "preferred_skills": [],
            "all_skills": [],
            "min_experience_years": 0.0,
            "experience_text": "Not specified",
            "education_degree": "Not specified",
            "education_text": "Not specified",
            "certifications": [],
            "raw_text": ""
        }

    # 1. First extract all skills found anywhere in the JD
    extracted = extract_skills_from_text(jd_text)
    all_skills = extracted["skills"]
    lower_jd = jd_text.lower()

    # 2. Divide JD into Required vs Preferred sections
    lower_lines = [l.strip() for l in jd_text.split("\n")]
    current_section = "other"
    req_lines = []
    pref_lines = []

    for line in lower_lines:
        line_clean = line.strip().lower()
        if not line_clean:
            continue
            
        # Check if line is a section header
        if any(kw in line_clean for kw in ["required", "must have", "minimum qualifications", "basic qualifications", "core requirements"]) and any(h in line_clean for h in ["skill", "qualification", "requirement", ":"]):
            current_section = "required"
            continue
        elif any(kw in line_clean for kw in ["preferred", "nice to have", "good to have", "bonus", "plus", "desired", "desirable"]) and any(h in line_clean for h in ["skill", "qualification", "requirement", ":", "have"]):
            current_section = "preferred"
            continue
        elif any(kw in line_clean for kw in ["responsibilities", "about us", "about the role", "benefits", "perks", "who you are"]) and line_clean.endswith(":"):
            current_section = "other"
            continue

        if current_section == "required":
            req_lines.append(line)
        elif current_section == "preferred":
            pref_lines.append(line)

    req_text = "\n".join(req_lines)
    pref_text = "\n".join(pref_lines)

    required_skills: List[str] = []
    preferred_skills: List[str] = []

    if req_text or pref_text:
        req_extracted = extract_skills_from_text(req_text)["skills"]
        pref_extracted = extract_skills_from_text(pref_text)["skills"]
        required_skills = req_extracted
        preferred_skills = [s for s in pref_extracted if s not in required_skills]
        # Any remaining skills from the full text not in either
        remaining = [s for s in all_skills if s not in required_skills and s not in preferred_skills]
        required_skills.extend(remaining)
    else:
        # Heuristic fallback if no explicit headers found
        if len(all_skills) <= 5:
            required_skills = all_skills[:]
            preferred_skills = []
        else:
            split_idx = max(3, int(len(all_skills) * 0.65))
            required_skills = all_skills[:split_idx]
            preferred_skills = all_skills[split_idx:]

    # 3. Extract Experience Requirement (e.g. "3+ years", "2-4 years", "minimum 5 years")
    exp_years = 0.0
    exp_text = "Not specified (Entry level / Any)"

    exp_matches = re.findall(
        r"(\d+(?:\.\d+)?)\s*(?:\+|-\s*\d+)?\s*(?:years?|yrs?)(?:\s*(?:of)?\s*(?:relevant\s*|hands-on\s*)?experience)?",
        lower_jd
    )
    if exp_matches:
        try:
            exp_years = float(exp_matches[0])
            exp_text = f"{exp_years:g}+ years of experience"
        except ValueError:
            pass

    # 4. Extract Education Requirement
    edu_degree = "Not specified"
    edu_text = "Any relevant degree or practical experience"

    if re.search(r"\b(m\.?tech|master'?s?|m\.?s\b|mca)\b", lower_jd):
        edu_degree = "Master's Degree (M.Tech / M.S. / MCA)"
        edu_text = "Master's degree in Computer Science, Data Science, or related field"
    elif re.search(r"\b(b\.?tech|b\.?e\b|bachelor'?s?|b\.?s\b|bca)\b", lower_jd):
        edu_degree = "Bachelor's Degree (B.Tech / B.E. / B.S.)"
        edu_text = "Bachelor's degree in Computer Science, IT, or related engineering discipline"

    # 5. Extract Certifications required if any
    certs = []
    for cert_kw in ["AWS Certified", "Kubernetes", "CKA", "Azure", "GCP", "PMP"]:
        if cert_kw.lower() in lower_jd:
            certs.append(cert_kw)

    return {
        "required_skills": sorted(list(dict.fromkeys(required_skills))),
        "preferred_skills": sorted(list(dict.fromkeys(preferred_skills))),
        "all_skills": all_skills,
        "min_experience_years": exp_years,
        "experience_text": exp_text,
        "education_degree": edu_degree,
        "education_text": edu_text,
        "certifications": certs,
        "raw_text": jd_text
    }
