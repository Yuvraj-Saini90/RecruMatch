"""Text preprocessing utilities preserving domain-specific technical vocabulary."""

import re
import unicodedata


def normalize_whitespace(text: str) -> str:
    """Normalize tabs, multiple spaces, and special line break characters."""
    if not text:
        return ""
    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)
    # Convert bullet points and symbols to standard space or newlines
    text = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219\uf0b7\uf0a7\u25cf\u25cb]", "\n• ", text)
    # Replace multiple horizontal spaces with a single space
    text = re.sub(r"[ \t]+", " ", text)
    # Collapse multiple consecutive newlines (more than 2) into 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_text_for_nlp(text: str) -> str:
    """Clean resume or JD text while strictly preserving tech tokens like C++, C#, .NET, Node.js."""
    if not text:
        return ""
    
    normalized = normalize_whitespace(text)
    
    # We do NOT strip punctuation aggressively here because we need to preserve
    # emails, phone numbers, and technical terms like C++, C#, .NET, Node.js, React.js
    return normalized


def clean_text_for_similarity(text: str) -> str:
    """Clean and standardize text for TF-IDF / SBERT vector representations.
    
    Protects important multi-symbol technical tokens before general cleaning.
    """
    if not text:
        return ""
    
    t = text.lower()
    
    # Protect special tech tokens before generic punctuation removal
    token_map = {
        "c++": " cpp_language ",
        "c#": " csharp_language ",
        ".net": " dotnet_framework ",
        "node.js": " nodejs ",
        "react.js": " reactjs ",
        "vue.js": " vuejs ",
        "next.js": " nextjs ",
        "express.js": " expressjs ",
        "ci/cd": " cicd_pipeline ",
    }
    
    for term, placeholder in token_map.items():
        t = t.replace(term, placeholder)
        
    # Replace non-alphanumeric (except underscores and hyphens) with space
    t = re.sub(r"[^a-z0-9_\-\s]", " ", t)
    
    # Restore token replacements back to clear single tokens
    restore_map = {
        "cpp_language": "cplusplus",
        "csharp_language": "csharp",
        "dotnet_framework": "dotnet",
        "nodejs": "nodejs",
        "reactjs": "reactjs",
        "vuejs": "vuejs",
        "nextjs": "nextjs",
        "expressjs": "expressjs",
        "cicd_pipeline": "cicd",
    }
    for placeholder, clean_term in restore_map.items():
        t = t.replace(placeholder, clean_term)
        
    t = re.sub(r"\s+", " ", t)
    return t.strip()
