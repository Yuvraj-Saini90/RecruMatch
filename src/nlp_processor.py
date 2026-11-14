"""NLP extraction engine using spaCy and domain-specific rules for resume parsing."""

import re
from typing import Dict, Any, List, Optional
import spacy

from src.skill_dictionary import SKILL_NORMALIZATION

# Global cache for spaCy NLP model
_nlp_model = None


def get_spacy_model():
    """Load and cache the spaCy English model with safe fallback."""
    global _nlp_model
    if _nlp_model is None:
        try:
            _nlp_model = spacy.load("en_core_web_sm")
        except Exception:
            try:
                # Blank model as fallback if en_core_web_sm fails
                _nlp_model = spacy.blank("en")
            except Exception:
                _nlp_model = None
    return _nlp_model


def extract_candidate_name(text: str, nlp_model=None) -> str:
    """Extract candidate name from the top section of the resume."""
    if not text:
        return "Not detected"

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if not lines:
        return "Not detected"

    forbidden_titles = {
        "resume", "curriculum vitae", "cv", "profile", "contact",
        "contact information", "summary", "professional summary",
        "objective", "career objective", "experience", "education",
        "skills", "technical skills", "projects", "certifications",
        "personal details", "phone", "email", "address", "portfolio",
        "work experience", "employment history", "qualifications"
    }
    
    forbidden_prefixes = (
        "skills:", "skills :", "summary:", "experience:", "education:",
        "projects:", "profile:", "objective:", "certifications:", "contact:",
        "work:", "technical:", "role:", "job:", "declaration:"
    )

    invalid_chars = set(";:•*▪▫-|/\\@()[]{}<>=_#0123456789")

    # Strategy 1: Check lines 1 to 5 for title-case clean names
    for line in lines[:5]:
        clean = re.sub(r"\s+", " ", line).strip()
        lower = clean.lower()

        # Skip headers, emails, phones, URLs, and lines with invalid characters
        if lower in forbidden_titles or any(lower.startswith(p) for p in forbidden_prefixes):
            continue
        if any(w in lower for w in ["curriculum", "resume", "github.com", "linkedin.com", "@", "http", "www."]):
            continue
        if any(ch in invalid_chars for ch in clean):
            continue
        if lower in SKILL_NORMALIZATION:
            continue

        # If line has 2-4 words, starts with capital letters, and only contains letters
        words = clean.split()
        if 2 <= len(words) <= 4:
            if all(w.isalpha() and w[0].isupper() for w in words):
                return clean

    # Strategy 2: Use spaCy NER PERSON tag on the first 500 characters
    if nlp_model is not None:
        try:
            top_slice = "\n".join(lines[:6])
            doc = nlp_model(top_slice)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    candidate = ent.text.strip()
                    cand_lower = candidate.lower()
                    words = candidate.split()
                    if (
                        cand_lower not in forbidden_titles
                        and not any(cand_lower.startswith(p) for p in forbidden_prefixes)
                        and not any(ch in invalid_chars for ch in candidate)
                        and 1 <= len(words) <= 4
                        and all(w.isalpha() and w[0].isupper() for w in words)
                        and cand_lower not in SKILL_NORMALIZATION
                    ):
                        return candidate
        except Exception:
            pass

    # Strategy 3: Strict check on first line (must be 2-4 capitalized words, no punctuation/digits)
    first_line = lines[0].strip()
    clean_first = re.sub(r"\s+", " ", first_line)
    words = clean_first.split()
    if 2 <= len(words) <= 4 and clean_first.lower() not in forbidden_titles:
        if not any(clean_first.lower().startswith(p) for p in forbidden_prefixes):
            if not any(ch in invalid_chars for ch in clean_first):
                if clean_first.lower() not in SKILL_NORMALIZATION:
                    if all(w.isalpha() and w[0].isupper() for w in words):
                        return clean_first

    return "Not detected"


def extract_contact_info(text: str) -> Dict[str, str]:
    """Extract email, phone number, and links/profiles."""
    info = {
        "email": "Not detected",
        "phone": "Not detected",
        "linkedin": "Not detected",
        "github": "Not detected"
    }
    if not text:
        return info

    # Email extraction
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    email_match = re.search(email_pattern, text)
    if email_match:
        info["email"] = email_match.group(0).strip()

    # Phone extraction (Indian + international + standard dashes/spaces)
    phone_pattern = r"(?:(?:\+91|91|0)?[ -]?)?(?:[6-9]\d{9}|\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4}|\+?\d{1,3}[ -]?\d{3,4}[ -]?\d{4,6})"
    phone_matches = re.finditer(phone_pattern, text)
    for match in phone_matches:
        cand_phone = match.group(0).strip()
        digits_only = re.sub(r"\D", "", cand_phone)
        if 10 <= len(digits_only) <= 13:
            info["phone"] = cand_phone
            break

    # LinkedIn / GitHub
    linkedin_match = re.search(r"(?:https?://)?(?:www\.)?linkedin\.com/in/([A-Za-z0-9_-]+)", text, re.IGNORECASE)
    if linkedin_match:
        info["linkedin"] = f"linkedin.com/in/{linkedin_match.group(1)}"

    github_match = re.search(r"(?:https?://)?(?:www\.)?github\.com/([A-Za-z0-9_-]+)", text, re.IGNORECASE)
    if github_match:
        info["github"] = f"github.com/{github_match.group(1)}"

    return info


def extract_education(text: str) -> Dict[str, Any]:
    """Extract education degree, major/field, institution, and graduation year."""
    edu = {
        "degree": "Not detected",
        "field": "Not detected",
        "institution": "Not detected",
        "year": "Not detected",
        "details_summary": "Not detected"
    }
    if not text:
        return edu

    degree_patterns = [
        (r"\b(b\.?tech(?:nology)?|b\.?e\.?|bachelor of technology|bachelor of engineering)\b", "B.Tech"),
        (r"\b(m\.?tech(?:nology)?|m\.?e\.?|master of technology|master of engineering)\b", "M.Tech"),
        (r"\b(b\.?s\.?c?|bachelor of science|b\.?s\b)\b", "B.S. / B.Sc"),
        (r"\b(m\.?s\.?c?|master of science|m\.?s\b)\b", "M.S. / M.Sc"),
        (r"\b(bca|bachelor of computer applications)\b", "BCA"),
        (r"\b(mca|master of computer applications)\b", "MCA"),
        (r"\b(mba|master of business administration)\b", "MBA"),
        (r"\b(ph\.?d\.?|doctor of philosophy|doctorate)\b", "Ph.D."),
        (r"\b(bachelor'?s?(?: degree)?)\b", "Bachelor's Degree"),
        (r"\b(master'?s?(?: degree)?)\b", "Master's Degree"),
        (r"\b(diploma)\b", "Diploma"),
    ]

    for pattern, name in degree_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            edu["degree"] = name
            break

    field_patterns = [
        (r"\b(computer science and engineering|computer science & engineering|cse)\b", "Computer Science & Engineering"),
        (r"\b(computer science|cs)\b", "Computer Science"),
        (r"\b(information technology|it)\b", "Information Technology"),
        (r"\b(artificial intelligence|ai)\b", "Artificial Intelligence"),
        (r"\b(data science)\b", "Data Science"),
        (r"\b(software engineering)\b", "Software Engineering"),
        (r"\b(electronics and communication|ece)\b", "Electronics & Communication"),
        (r"\b(electrical engineering|mechanical engineering|civil engineering)\b", "Engineering"),
    ]

    for pattern, name in field_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            edu["field"] = name
            break

    # Institution patterns
    inst_match = re.search(
        r"(?:at|from|institute|university|college)?\s*([A-Z][A-Za-z0-9&.\s]+(?:University|Institute of Technology|Engineering College|Institute|College|Academy|IIT|NIT|GNIOT|BITS))",
        text,
        re.IGNORECASE
    )
    if inst_match:
        edu["institution"] = inst_match.group(1).strip()
    elif "gniot" in text.lower():
        edu["institution"] = "GNIOT Greater Noida"

    # Graduation Year (1990 - 2030)
    year_match = re.findall(r"\b(20[0-2][0-9]|199[0-9])\b", text)
    if year_match:
        # Highest year mentioned is usually the graduation or current year
        years = [int(y) for y in year_match]
        edu["year"] = str(max(years))

    if edu["degree"] != "Not detected":
        parts = [edu["degree"]]
        if edu["field"] != "Not detected":
            parts.append(f"in {edu['field']}")
        if edu["institution"] != "Not detected":
            parts.append(f"- {edu['institution']}")
        if edu["year"] != "Not detected":
            parts.append(f"({edu['year']})")
        edu["details_summary"] = " ".join(parts)

    return edu


def extract_experience_details(text: str) -> Dict[str, Any]:
    """Extract total years of experience, detected job titles, and employers."""
    exp = {
        "years": 0.0,
        "years_text": "Not detected",
        "titles": [],
        "companies": [],
        "summary": "Not detected"
    }
    if not text:
        return exp

    lower = text.lower()

    # 1. Look for explicit mentions like "X years of experience", "X+ yrs", etc.
    exp_patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s*(?:of)?\s*(?:total\s*)?experience)?",
        r"experience\s*:\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)",
        r"total experience\s*:\s*(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)",
    ]

    explicit_years = []
    for pat in exp_patterns:
        matches = re.findall(pat, lower)
        for m in matches:
            try:
                val = float(m)
                if 0.5 <= val <= 35:
                    explicit_years.append(val)
            except ValueError:
                pass

    if explicit_years:
        max_exp = max(explicit_years)
        exp["years"] = max_exp
        exp["years_text"] = f"{max_exp:g} years"
    else:
        # 2. Check for date spans like "2020 - 2023" or "2021 - Present"
        date_spans = re.findall(r"\b(201\d|202\d)\s*(?:-|to)\s*(201\d|202\d|present)\b", lower)
        calculated_years = 0.0
        current_year = 2026

        for start_str, end_str in date_spans:
            try:
                start = int(start_str)
                end = current_year if "present" in end_str else int(end_str)
                diff = end - start
                if 0 <= diff <= 25:
                    calculated_years += diff
            except ValueError:
                pass

        if calculated_years > 0:
            exp["years"] = calculated_years
            exp["years_text"] = f"~{calculated_years:g} years (computed from career timeline)"
        elif any(w in lower for w in ["fresher", "intern", "entry level", "student", "final year"]):
            exp["years"] = 0.5
            exp["years_text"] = "Fresher / Entry level (~0.5 yr)"

    # Common job titles
    common_roles = [
        "Software Engineer", "Senior Software Engineer", "Backend Developer",
        "Frontend Developer", "Full Stack Developer", "Data Scientist",
        "Machine Learning Engineer", "DevOps Engineer", "Cloud Engineer",
        "Python Developer", "Java Developer", "Software Development Engineer",
        "System Engineer", "Data Analyst", "AI Engineer", "Intern", "Graduate Trainee"
    ]
    detected_roles = []
    for role in common_roles:
        if re.search(rf"\b{re.escape(role)}\b", text, re.IGNORECASE):
            detected_roles.append(role)
    exp["titles"] = detected_roles

    if exp["years_text"] != "Not detected":
        exp["summary"] = f"{exp['years_text']}" + (f" ({', '.join(detected_roles[:2])})" if detected_roles else "")

    return exp


def extract_certifications(text: str) -> List[str]:
    """Extract professional certifications from resume."""
    if not text:
        return []

    cert_catalog = [
        "AWS Certified Solutions Architect", "AWS Certified Cloud Practitioner",
        "AWS Certified Developer", "Google Cloud Certified Professional Data Engineer",
        "Google Cloud Associate Cloud Engineer", "Microsoft Certified: Azure Fundamentals",
        "Microsoft Certified: Azure Developer", "Certified Kubernetes Administrator (CKA)",
        "TensorFlow Developer Certificate", "Oracle Certified Java Programmer",
        "Project Management Professional (PMP)", "Certified Scrum Master (CSM)",
        "Docker Certified Associate", "CompTIA Security+", "Cisco CCNA",
        "Meta Front-End Developer", "Deep Learning Specialization", "Machine Learning Specialization"
    ]
    
    found_certs = []
    for cert in cert_catalog:
        # Check either full name or core distinctive phrases
        if re.search(rf"\b{re.escape(cert)}\b", text, re.IGNORECASE):
            found_certs.append(cert)
            
    # Also check generic certifications section
    cert_section = re.search(r"(?:certifications|certificates|licenses)\s*:?\s*\n(.*?)(?:\n\s*\n|\Z)", text, re.IGNORECASE | re.DOTALL)
    if cert_section:
        sec_text = cert_section.group(1).strip()
        lines = [l.strip(" •-*") for l in sec_text.split("\n") if l.strip()]
        for line in lines[:4]:
            if line and len(line) < 80 and line not in found_certs:
                found_certs.append(line)

    return list(dict.fromkeys(found_certs))


def extract_projects(text: str) -> List[str]:
    """Extract project titles or summaries from the resume."""
    if not text:
        return []

    projects = []
    proj_section = re.search(
        r"(?:academic projects|key projects|projects|personal projects)\s*:?\s*\n(.*?)(?:\n\s*(?:education|experience|skills|certifications|achievements)\b|\Z)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if proj_section:
        content = proj_section.group(1).strip()
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        for line in lines:
            # Look for project title lines (bulleted or bold-like short headings)
            clean_line = re.sub(r"^[\s•\-*#\d.]+", "", line).strip()
            if 4 <= len(clean_line) <= 70 and not clean_line.lower().startswith(("developed", "created", "built", "implemented", "used", "worked")):
                projects.append(clean_line)
                if len(projects) >= 4:
                    break

    return projects


def parse_resume_content(raw_text: str) -> Dict[str, Any]:
    """Parse entire resume content into structured fields."""
    nlp = get_spacy_model()
    
    name = extract_candidate_name(raw_text, nlp_model=nlp)
    contacts = extract_contact_info(raw_text)
    education = extract_education(raw_text)
    experience = extract_experience_details(raw_text)
    certifications = extract_certifications(raw_text)
    projects = extract_projects(raw_text)

    return {
        "candidate_name": name,
        "email": contacts["email"],
        "phone": contacts["phone"],
        "linkedin": contacts["linkedin"],
        "github": contacts["github"],
        "education": education,
        "experience": experience,
        "certifications": certifications,
        "projects": projects,
        "raw_text": raw_text
    }
