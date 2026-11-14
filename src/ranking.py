"""Candidate ranking, sorting, and aggregate recruiter analytics."""

from typing import List, Dict, Any
import pandas as pd


def rank_candidates(
    candidate_assessments: List[Dict[str, Any]],
    sort_by: str = "overall_score",
    ascending: bool = False
) -> List[Dict[str, Any]]:
    """Rank candidates based on the specified metric and assign rank numbers.
    
    Supported sort metrics: 'overall_score', 'required_skills', 'experience', 'similarity'
    """
    if not candidate_assessments:
        return []

    def get_sort_key(item: Dict[str, Any]):
        if sort_by == "required_skills":
            return item.get("required_skills_result", {}).get("score", 0.0)
        elif sort_by == "experience":
            return item.get("experience_result", {}).get("score", 0.0)
        elif sort_by == "similarity":
            return item.get("similarity_result", {}).get("score", 0.0)
        else:
            return item.get("overall_score", 0.0)

    sorted_list = sorted(candidate_assessments, key=get_sort_key, reverse=(not ascending))

    # Assign rank integers
    for rank_idx, cand in enumerate(sorted_list, start=1):
        cand["rank"] = rank_idx

    return sorted_list


def compute_dashboard_metrics(
    ranked_candidates: List[Dict[str, Any]],
    jd_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate aggregate summary statistics and chart data for the recruiter dashboard."""
    if not ranked_candidates:
        return {
            "total_candidates": 0,
            "average_score": 0.0,
            "top_candidate": None,
            "strong_matches_count": 0,
            "score_distribution": {"Low (<40%)": 0, "Moderate (40-60%)": 0, "Good (60-80%)": 0, "Excellent (80%+)": 0},
            "skill_coverage": {},
            "skill_gaps": {}
        }

    scores = [c["overall_score"] for c in ranked_candidates]
    total_count = len(ranked_candidates)
    avg_score = round(sum(scores) / total_count, 1) if total_count > 0 else 0.0
    top_cand = ranked_candidates[0] if ranked_candidates else None
    strong_matches = sum(1 for c in ranked_candidates if c["category"]["category_key"] == "excellent")

    # Score distribution buckets
    distribution = {
        "Low (<40%)": sum(1 for s in scores if s < 40.0),
        "Moderate (40-60%)": sum(1 for s in scores if 40.0 <= s < 60.0),
        "Good (60-80%)": sum(1 for s in scores if 60.0 <= s < 80.0),
        "Excellent (80%+)": sum(1 for s in scores if s >= 80.0),
    }

    # Skill coverage (which skills appear most frequently across all uploaded resumes)
    skill_freq: Dict[str, int] = {}
    for c in ranked_candidates:
        c_skills = c.get("candidate_profile", {}).get("skills", [])
        for sk in c_skills:
            skill_freq[sk] = skill_freq.get(sk, 0) + 1

    sorted_coverage = dict(sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)[:10])

    # Required Skill Gaps (which required skills are most frequently missing across candidates)
    missing_freq: Dict[str, int] = {}
    for c in ranked_candidates:
        missing_skills = c.get("required_skills_result", {}).get("missing", [])
        for sk in missing_skills:
            missing_freq[sk] = missing_freq.get(sk, 0) + 1

    sorted_gaps = dict(sorted(missing_freq.items(), key=lambda x: x[1], reverse=True)[:10])

    return {
        "total_candidates": total_count,
        "average_score": avg_score,
        "top_candidate": top_cand,
        "strong_matches_count": strong_matches,
        "score_distribution": distribution,
        "skill_coverage": sorted_coverage,
        "skill_gaps": sorted_gaps
    }
