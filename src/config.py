"""Configuration constants and default settings for the Smart Resume Screening Tool."""

from typing import Dict, Any

# Application Metadata
APP_TITLE = "Smart Resume Screening and Candidate Ranking Tool"
APP_SUBTITLE = "AI-assisted candidate screening with transparent, explainable matching"
APP_VERSION = "1.0.0"

# Academic Project Info
PROJECT_INFO = {
    "project_name": "Smart Resume Screening and Candidate Ranking Tool",
    "project_type": "B.Tech CSE Academic Project",
    "developer": "Yuvraj Saini",
    "supervisor": "Mr. Ashwini Kr. Verma",
    "department": "Department of Computer Science & Engineering",
    "institution": "GNIOT Engineering Institute, Greater Noida, India",
}

# Default Scoring Weights (must sum to 1.0 or 100%)
DEFAULT_WEIGHTS: Dict[str, float] = {
    "required_skills": 0.40,
    "preferred_skills": 0.15,
    "experience": 0.15,
    "education": 0.10,
    "similarity": 0.20,
}

# Score Tier Thresholds
DEFAULT_THRESHOLDS: Dict[str, float] = {
    "excellent": 80.0,
    "good": 60.0,
    "moderate": 40.0,
}

# Match Categories and UI Display
MATCH_CATEGORIES = {
    "excellent": {
        "label": "Excellent Match",
        "color": "#10b981",  # Emerald Green
        "bg_color": "#ecfdf5",
        "badge_class": "badge-excellent",
    },
    "good": {
        "label": "Good Match",
        "color": "#3b82f6",  # Indigo/Blue
        "bg_color": "#eff6ff",
        "badge_class": "badge-good",
    },
    "moderate": {
        "label": "Moderate Match",
        "color": "#f59e0b",  # Amber
        "bg_color": "#fffbeb",
        "badge_class": "badge-moderate",
    },
    "low": {
        "label": "Low Match",
        "color": "#ef4444",  # Red / Slate
        "bg_color": "#fef2f2",
        "badge_class": "badge-low",
    },
}

# Supported Resume Upload Formats
SUPPORTED_EXTENSIONS = [".pdf", ".docx"]

# Max Upload Size in MB (guideline)
MAX_FILE_SIZE_MB = 10
