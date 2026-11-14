"""Career Velocity & Job Stability Analyzer (Temporal Resume Profiler).

Evaluates candidate retention risk, average company tenure duration,
and career growth trajectory (e.g. progression from Junior to Senior/Lead).
"""

import re
from typing import Dict, Any, List


SENIORITY_HIERARCHY = {
    "intern": 1,
    "trainee": 1,
    "associate": 2,
    "junior": 2,
    "developer": 3,
    "engineer": 3,
    "analyst": 3,
    "consultant": 3,
    "specialist": 3,
    "senior": 4,
    "sr": 4,
    "lead": 5,
    "principal": 6,
    "staff": 6,
    "manager": 6,
    "architect": 7,
    "director": 8,
    "head": 8,
    "vp": 9
}


def analyze_career_velocity(resume_text: str, detected_years: float = 0.0) -> Dict[str, Any]:
    """Analyze career growth velocity, average tenure, and promotion progression."""
    lines = resume_text.splitlines()
    detected_titles = []
    
    # Scan lines for job title keywords
    for line in lines:
        clean = line.strip().lower()
        if len(clean) > 80:
            continue
        for title_key, rank in SENIORITY_HIERARCHY.items():
            pattern = rf"\b{title_key}\b"
            if re.search(pattern, clean):
                detected_titles.append((title_key.title(), rank))
                break

    # Determine progression
    # Resumes are commonly reverse-chronological (most recent senior role at top)
    ranks = [r for _, r in detected_titles]
    is_ascending = False
    if len(ranks) >= 2:
        # Reverse-chronological: first listed role rank >= last listed role rank
        # Forward-chronological: first listed role rank <= last listed role rank
        is_reverse_chrono_ascending = ranks[0] >= ranks[-1]
        is_forward_chrono_ascending = ranks[-1] >= ranks[0]
        is_ascending = is_reverse_chrono_ascending or is_forward_chrono_ascending
    
    # Calculate stability score
    # High churn if > 4 titles in < 2 years; Stable if average tenure >= 1.5 years
    title_count = max(1, len(detected_titles))
    avg_tenure_years = round(detected_years / title_count, 1) if detected_years > 0 else 1.5
    
    if avg_tenure_years >= 2.0:
        stability_rating = "High Stability (Loyal / Long Tenure)"
        stability_score = 95.0
    elif avg_tenure_years >= 1.0:
        stability_rating = "Healthy Industry Average (1-2 yrs/role)"
        stability_score = 85.0
    elif avg_tenure_years >= 0.6:
        stability_rating = "Moderate Churn (Frequent Shifts)"
        stability_score = 65.0
    else:
        stability_rating = "High Flight Risk (< 8 months avg tenure)"
        stability_score = 45.0
        
    velocity_label = "Ascending (Promotions / Increasing Seniority)" if is_ascending else "Steady / Lateral Progression"
    
    return {
        "detected_years": detected_years,
        "role_transitions_count": len(detected_titles),
        "detected_roles": [t for t, _ in detected_titles[:5]],
        "average_tenure_years": avg_tenure_years,
        "stability_score": stability_score,
        "stability_rating": stability_rating,
        "career_velocity": velocity_label,
        "is_ascending": is_ascending
    }
