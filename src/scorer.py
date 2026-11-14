"""Explainable scoring engine comparing candidate profiles against Job Description requirements."""

from typing import Dict, Any, List, Set, Optional
from src.config import DEFAULT_WEIGHTS, DEFAULT_THRESHOLDS, MATCH_CATEGORIES
from src.similarity_engine import compute_similarity


def compute_required_skills_score(candidate_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
    """Calculate match score for required skills.
    
    Formula: (Matched Required Skills / Total Required Skills) * 100
    """
    cand_set: Set[str] = set(candidate_skills)
    req_set: Set[str] = set(required_skills)
    
    if not req_set:
        return {
            "score": 100.0,
            "matched": [],
            "missing": [],
            "total_count": 0,
            "matched_count": 0,
            "display": "No specific required skills defined in JD (100%)"
        }
        
    matched = sorted(list(req_set.intersection(cand_set)))
    missing = sorted(list(req_set.difference(cand_set)))
    
    score = round((len(matched) / len(req_set)) * 100.0, 2)
    display = f"{len(matched)}/{len(req_set)} required skills matched ({score:g}%)"
    
    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "total_count": len(req_set),
        "matched_count": len(matched),
        "display": display
    }


def compute_preferred_skills_score(candidate_skills: List[str], preferred_skills: List[str]) -> Dict[str, Any]:
    """Calculate match score for preferred / nice-to-have skills."""
    cand_set: Set[str] = set(candidate_skills)
    pref_set: Set[str] = set(preferred_skills)
    
    if not pref_set:
        return {
            "score": 100.0,
            "matched": [],
            "missing": [],
            "total_count": 0,
            "matched_count": 0,
            "display": "No preferred skills defined (neutral 100%)"
        }
        
    matched = sorted(list(pref_set.intersection(cand_set)))
    missing = sorted(list(pref_set.difference(cand_set)))
    
    score = round((len(matched) / len(pref_set)) * 100.0, 2)
    display = f"{len(matched)}/{len(pref_set)} preferred skills matched ({score:g}%)"
    
    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "total_count": len(pref_set),
        "matched_count": len(matched),
        "display": display
    }


def compute_experience_score(candidate_exp: Dict[str, Any], jd_min_years: float) -> Dict[str, Any]:
    """Compare candidate detected experience against JD requirement."""
    cand_years = float(candidate_exp.get("years", 0.0))
    cand_summary = candidate_exp.get("summary", "Not detected")

    if jd_min_years <= 0.0:
        return {
            "score": 100.0,
            "required_years": 0.0,
            "candidate_years": cand_years,
            "explanation": f"Entry level / no minimum experience required (Candidate has: {cand_summary})"
        }

    if cand_years >= jd_min_years:
        score = 100.0
        explanation = f"Meets/exceeds requirement: {cand_years:g} yrs detected vs {jd_min_years:g}+ yrs required (100%)"
    elif cand_years > 0.0:
        # Partial match proportional to required years
        score = round(min(95.0, (cand_years / jd_min_years) * 100.0), 2)
        explanation = f"Partial match: {cand_years:g} yrs detected vs {jd_min_years:g}+ yrs required ({score:g}%)"
    else:
        # Experience not parsed or fresher
        score = 50.0
        explanation = f"Experience timeline not detected from resume ({jd_min_years:g}+ yrs required) - 50% baseline"

    return {
        "score": score,
        "required_years": jd_min_years,
        "candidate_years": cand_years,
        "explanation": explanation
    }


def compute_education_score(candidate_edu: Dict[str, Any], jd_degree_text: str) -> Dict[str, Any]:
    """Compare candidate education credentials against JD education requirements."""
    cand_deg = candidate_edu.get("degree", "Not detected")
    cand_field = candidate_edu.get("field", "Not detected")
    cand_full = candidate_edu.get("details_summary", "Not detected")

    jd_deg_lower = jd_degree_text.lower() if jd_degree_text else ""

    if not jd_deg_lower or "not specified" in jd_deg_lower:
        return {
            "score": 100.0,
            "candidate_degree": cand_deg,
            "explanation": f"No mandatory degree specified in JD. Candidate: {cand_full}"
        }

    # Evaluate match levels
    is_master_req = any(m in jd_deg_lower for m in ["master", "m.tech", "m.s", "mca"])
    is_bachelor_req = any(b in jd_deg_lower for b in ["bachelor", "b.tech", "b.e", "b.s", "bca"])

    cand_deg_lower = cand_deg.lower()

    if is_master_req:
        if any(m in cand_deg_lower for m in ["master", "m.tech", "m.s", "mca", "ph.d"]):
            score = 100.0
            explanation = f"Meets Master's degree requirement: {cand_full}"
        elif any(b in cand_deg_lower for b in ["bachelor", "b.tech", "b.e", "b.s", "bca"]):
            score = 75.0
            explanation = f"Holds Bachelor's degree ({cand_deg}) against Master's requirement (75%)"
        else:
            score = 50.0
            explanation = f"Degree level not detected ({cand_deg}) against Master's requirement (50%)"
    elif is_bachelor_req:
        if any(d in cand_deg_lower for d in ["bachelor", "b.tech", "b.e", "b.s", "bca", "master", "m.tech", "mca", "ph.d"]):
            score = 100.0
            explanation = f"Meets Bachelor's requirement: {cand_full}"
        elif cand_deg_lower == "diploma":
            score = 70.0
            explanation = f"Holds Diploma against Bachelor's requirement (70%)"
        else:
            score = 60.0
            explanation = f"Education degree not detected against Bachelor's requirement (60%)"
    else:
        score = 100.0
        explanation = f"Education requirement satisfied ({cand_full})"

    return {
        "score": score,
        "candidate_degree": cand_deg,
        "explanation": explanation
    }


def get_match_category(overall_score: float, thresholds: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """Determine category tier badge and visual metadata."""
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    if overall_score >= thresholds.get("excellent", 80.0):
        key = "excellent"
    elif overall_score >= thresholds.get("good", 60.0):
        key = "good"
    elif overall_score >= thresholds.get("moderate", 40.0):
        key = "moderate"
    else:
        key = "low"

    cat = MATCH_CATEGORIES[key]
    return {
        "category_key": key,
        "label": cat["label"],
        "color": cat["color"],
        "bg_color": cat["bg_color"],
        "badge_class": cat["badge_class"]
    }


def generate_candidate_assessment(
    candidate_profile: Dict[str, Any],
    jd_analysis: Dict[str, Any],
    weights: Optional[Dict[str, float]] = None,
    thresholds: Optional[Dict[str, float]] = None,
    matching_method: str = "TF-IDF"
) -> Dict[str, Any]:
    """Compute complete explainable score and structured audit trail for a candidate."""
    if weights is None:
        weights = DEFAULT_WEIGHTS
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    cand_skills = candidate_profile.get("skills", [])
    raw_resume_text = candidate_profile.get("raw_text", "")
    raw_jd_text = jd_analysis.get("raw_text", "")

    # 1. Component Scores
    req_res = compute_required_skills_score(cand_skills, jd_analysis.get("required_skills", []))
    pref_res = compute_preferred_skills_score(cand_skills, jd_analysis.get("preferred_skills", []))
    exp_res = compute_experience_score(candidate_profile.get("experience", {}), jd_analysis.get("min_experience_years", 0.0))
    edu_res = compute_education_score(candidate_profile.get("education", {}), jd_analysis.get("education_degree", ""))
    sim_res = compute_similarity(raw_jd_text, raw_resume_text, method=matching_method)

    # 2. Weighted Overall Score Calculation
    w_req = weights.get("required_skills", 0.40)
    w_pref = weights.get("preferred_skills", 0.15)
    w_exp = weights.get("experience", 0.15)
    w_edu = weights.get("education", 0.10)
    w_sim = weights.get("similarity", 0.20)

    # Ensure weight normalization
    total_w = w_req + w_pref + w_exp + w_edu + w_sim
    if total_w <= 0:
        total_w = 1.0

    raw_overall = (
        (w_req * req_res["score"]) +
        (w_pref * pref_res["score"]) +
        (w_exp * exp_res["score"]) +
        (w_edu * edu_res["score"]) +
        (w_sim * sim_res["score"])
    ) / total_w

    overall_score = round(max(0.0, min(100.0, raw_overall)), 1)
    category = get_match_category(overall_score, thresholds)

    # 3. Dynamic Strengths and Gaps Detection
    strengths: List[str] = []
    gaps: List[str] = []

    # Required skills strengths / gaps
    if req_res["matched_count"] > 0:
        if req_res["score"] >= 80.0:
            strengths.append(f"Strong required skills alignment ({req_res['matched_count']}/{req_res['total_count']} matched: {', '.join(req_res['matched'][:4])})")
        else:
            strengths.append(f"Verified required skills: {', '.join(req_res['matched'][:4])}")
    
    if req_res["missing"]:
        gaps.append(f"Missing required skills: {', '.join(req_res['missing'])}")

    # Preferred skills strengths
    if pref_res["matched"]:
        strengths.append(f"Bonus skills detected: {', '.join(pref_res['matched'][:3])}")

    # Experience strengths / gaps
    if exp_res["score"] >= 100.0:
        strengths.append(f"Meets or exceeds target experience ({candidate_profile.get('experience', {}).get('summary', 'Experienced')})")
    elif exp_res["candidate_years"] > 0 and exp_res["candidate_years"] < jd_analysis.get("min_experience_years", 0.0):
        gaps.append(f"Lower experience than preferred ({exp_res['candidate_years']:g} yrs vs {jd_analysis.get('min_experience_years', 0.0):g}+ yrs)")

    # Education strengths / gaps
    if edu_res["score"] == 100.0 and candidate_profile.get("education", {}).get("degree") != "Not detected":
        strengths.append(f"Qualifies for education criterion ({candidate_profile.get('education', {}).get('details_summary', '')})")
    elif edu_res["score"] < 75.0:
        gaps.append(f"Education match gap: {edu_res['explanation']}")

    # Similarity strength
    if sim_res["score"] >= 70.0:
        strengths.append(f"High resume-to-JD semantic resonance ({sim_res['score']:g}%)")

    # 4. Deterministic Recruiter Narrative
    explanation_points = [
        f"• **Required Skills ({w_req*100:.0f}% weight)**: {req_res['display']}.",
        f"• **Preferred Skills ({w_pref*100:.0f}% weight)**: {pref_res['display']}.",
        f"• **Experience ({w_exp*100:.0f}% weight)**: {exp_res['explanation']}.",
        f"• **Education ({w_edu*100:.0f}% weight)**: {edu_res['explanation']}.",
        f"• **Text Similarity ({w_sim*100:.0f}% weight)**: {sim_res['score']:g}% via {sim_res['method_used']}."
    ]
    explanation_summary = "\n\n".join(explanation_points)

    return {
        "candidate_id": candidate_profile.get("candidate_id", ""),
        "candidate_name": candidate_profile.get("candidate_name", "Not detected"),
        "filename": candidate_profile.get("filename", ""),
        "overall_score": overall_score,
        "category": category,
        "required_skills_result": req_res,
        "preferred_skills_result": pref_res,
        "experience_result": exp_res,
        "education_result": edu_res,
        "similarity_result": sim_res,
        "strengths": strengths,
        "gaps": gaps,
        "explanation_summary": explanation_summary,
        "weights_used": weights,
        "candidate_profile": candidate_profile
    }
