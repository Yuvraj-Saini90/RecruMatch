"""Adversarial Resume Hack & Prompt Injection Detector (ATS Security Shield).

Detects modern evasion techniques used by candidates to manipulate automated screening:
1. Prompt Injection attacks (jailbreaking LLM/AI screeners).
2. Repetitive keyword stuffing.
3. Invisible / white-font text or micro-fonts in PDFs.
"""

import re
from typing import Dict, Any, List, Optional
import pdfplumber


PROMPT_INJECTION_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?(previous|prior)\s+(instructions|prompts|directives)",
    r"(?i)system\s+prompt\s*:",
    r"(?i)you\s+are\s+now\s+(an|the)\s+ai\s+recruiter",
    r"(?i)always\s+(rank|score|rate)\s+this\s+candidate\s+(as\s+)?(100|99|top|highest|excellent)",
    r"(?i)override\s+(all\s+)?evaluation\s+criteria",
    r"(?i)bypass\s+(ats|screening|filter)",
    r"(?i)do\s+not\s+read\s+this\s+to\s+the\s+human",
    r"(?i)assistant\s*:\s*score\s*=\s*(100|perfect)",
    r"(?i)act\s+as\s+a\s+hiring\s+manager\s+who\s+accepts"
]


def detect_prompt_injection(text: str) -> Dict[str, Any]:
    """Scan text for malicious prompt injection and jailbreak payloads."""
    if not text:
        return {"detected": False, "matches": [], "risk_level": "None"}
    
    matches = []
    for pattern in PROMPT_INJECTION_PATTERNS:
        found = re.findall(pattern, text)
        if found:
            # Get matching snippet
            for m in re.finditer(pattern, text):
                snippet = text[max(0, m.start() - 20):min(len(text), m.end() + 20)].strip()
                matches.append(snippet)
    
    detected = len(matches) > 0
    risk = "High" if len(matches) >= 2 else ("Medium" if detected else "None")
    
    return {
        "detected": detected,
        "matches": matches,
        "risk_level": risk,
        "count": len(matches)
    }


def detect_keyword_stuffing(text: str, threshold: int = 8) -> Dict[str, Any]:
    """Detect unnatural keyword repetition designed to manipulate TF-IDF / ATS frequency."""
    if not text:
        return {"detected": False, "suspicious_words": []}
        
    words = re.findall(r"\b[A-Za-z]{3,}\b", text.lower())
    freq: Dict[str, int] = {}
    for w in words:
        # Ignore common English stop words
        if w in {"and", "the", "for", "with", "from", "that", "this", "have", "been", "developer", "engineer"}:
            continue
        freq[w] = freq.get(w, 0) + 1
        
    suspicious = [w for w, c in freq.items() if c >= threshold]
    return {
        "detected": len(suspicious) > 0,
        "suspicious_words": suspicious,
        "max_frequency": max(freq.values()) if freq else 0
    }


def inspect_pdf_for_hidden_text(pdf_path: str) -> Dict[str, Any]:
    """Inspect PDF elements for white text, zero opacity, or micro-font sizes."""
    hidden_findings = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                # Inspect extracted character elements
                chars = page.chars if hasattr(page, "chars") else []
                for char in chars:
                    size = char.get("size", 10.0)
                    color = char.get("non_stroking_color")
                    
                    # Check for micro-font (< 3pt is invisible to human eye)
                    if size < 3.0:
                        hidden_findings.append({
                            "page": page_num,
                            "type": "micro_font",
                            "text": char.get("text", ""),
                            "font_size": size
                        })
                        
                    # Check for white text on white page (rgb: 1, 1, 1 or near 1)
                    if color and (
                        color == (1, 1, 1) or 
                        color == [1, 1, 1] or 
                        color == 1 or 
                        color == (1.0, 1.0, 1.0)
                    ):
                        hidden_findings.append({
                            "page": page_num,
                            "type": "white_font",
                            "text": char.get("text", ""),
                            "color": color
                        })
                        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "hidden_detected": False,
            "findings_count": 0
        }
        
    has_hidden = len(hidden_findings) > 0
    return {
        "success": True,
        "hidden_detected": has_hidden,
        "findings_count": len(hidden_findings),
        "details": hidden_findings[:10]  # sample of first 10
    }


def compute_candidate_integrity(resume_text: str, pdf_path: Optional[str] = None) -> Dict[str, Any]:
    """Compute overall candidate resume authenticity & integrity score (100% = clean)."""
    injection_res = detect_prompt_injection(resume_text)
    stuffing_res = detect_keyword_stuffing(resume_text)
    hidden_res = inspect_pdf_for_hidden_text(pdf_path) if pdf_path else {"hidden_detected": False, "findings_count": 0}
    
    deductions = 0
    flags = []
    
    if injection_res["detected"]:
        deductions += 60
        flags.append(f"Prompt Injection Detected ({injection_res['count']} payloads)")
        
    if stuffing_res["detected"]:
        deductions += 25
        flags.append(f"Abnormal Keyword Repetition ({len(stuffing_res['suspicious_words'])} words repeated > 8x)")
        
    if hidden_res.get("hidden_detected", False):
        deductions += 35
        flags.append("Invisible/Micro-font Text Detected")
        
    integrity_score = max(0, 100 - deductions)
    status = "Verified Clean" if integrity_score >= 90 else ("Suspicious" if integrity_score >= 60 else "High Risk")
    
    return {
        "integrity_score": integrity_score,
        "status": status,
        "flags": flags,
        "is_flagged": len(flags) > 0,
        "details": {
            "prompt_injection": injection_res,
            "keyword_stuffing": stuffing_res,
            "hidden_text": hidden_res
        }
    }
