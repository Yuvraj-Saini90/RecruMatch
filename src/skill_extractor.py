"""Skill extraction engine with boundary matching and taxonomy grouping."""

import re
from typing import Dict, List, Set, Any
from src.skill_dictionary import (
    SKILL_NORMALIZATION,
    SKILL_TAXONOMY,
    get_skill_category
)


def extract_skills_from_text(text: str) -> Dict[str, Any]:
    """Scan text to extract all technical skills and normalize to canonical taxonomy.
    
    Returns a dictionary with list of unique canonical skills and categorized groupings.
    """
    if not text:
        return {"skills": [], "categorized": {}, "total_count": 0}
        
    found_canonical: Set[str] = set()
    lower_text = text.lower()
    
    # 1. First, check multi-word and special symbol aliases from SKILL_NORMALIZATION
    # Sort terms by length descending to match longer phrases first (e.g. "machine learning" before "c")
    sorted_aliases = sorted(SKILL_NORMALIZATION.keys(), key=lambda x: len(x), reverse=True)
    
    for alias in sorted_aliases:
        canonical_name = SKILL_NORMALIZATION[alias]
        
        # Build safe regex pattern based on whether term contains special symbols
        if alias in ["c++", "cpp"]:
            pattern = r"(?:^|[\s,;/()\[\]])(?:c\+\+|cpp)(?:$|[\s,;/()\[\]])"
        elif alias in ["c#", "csharp"]:
            pattern = r"(?:^|[\s,;/()\[\]])(?:c#|csharp)(?:$|[\s,;/()\[\]])"
        elif alias in [".net", "dotnet"]:
            pattern = r"(?:^|[\s,;/()\[\]])(?:\.net|dotnet)(?:$|[\s,;/()\[\]])"
        elif alias in ["c", "r"]:
            # Single letter programming languages require strict context
            pattern = rf"(?:^|[\s,;/()\[\]]){re.escape(alias)}(?:$|[\s,;/()\[\]])"
            # Ensure it is surrounded by delimiters, and not just any isolated character
            if not re.search(rf"\b(?:programming in {alias}|language: {alias}|skills:.*?{alias})\b", lower_text) and not re.search(pattern, lower_text):
                continue
        elif "." in alias:
            # Terms with dots like node.js, react.js, vue.js
            pattern = r"(?:^|[\s,;/()\[\]])" + re.escape(alias) + r"(?:$|[\s,;/()\[\]])"
        else:
            # Standard word boundary matching
            escaped_alias = re.escape(alias)
            pattern = rf"\b{escaped_alias}\b"
            
        if re.search(pattern, lower_text):
            found_canonical.add(canonical_name)

    # 2. Check canonical taxonomy names directly as well
    for category, skill_list in SKILL_TAXONOMY.items():
        for skill in skill_list:
            if skill in found_canonical:
                continue
            skill_lower = skill.lower()
            if skill_lower in ["c++", "c#", ".net"]:
                continue
            pattern = rf"\b{re.escape(skill_lower)}\b"
            if re.search(pattern, lower_text):
                found_canonical.add(skill)

    # 3. Categorize extracted skills
    categorized: Dict[str, List[str]] = {}
    for skill in sorted(found_canonical):
        cat = get_skill_category(skill)
        categorized.setdefault(cat, []).append(skill)

    sorted_skills = sorted(list(found_canonical))
    
    return {
        "skills": sorted_skills,
        "categorized": categorized,
        "total_count": len(sorted_skills)
    }
