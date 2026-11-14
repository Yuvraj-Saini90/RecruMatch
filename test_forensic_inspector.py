"""Comprehensive Test Suite for Resume Forensic Inspector.

Tests all detection mechanisms:
1. Hidden White Text (#FFFFFF) & Micro-Font Injections.
2. Homoglyph & Unicode Character Spoofing (Cyrillic/Greek in English words).
3. Zero-Width & Invisible Characters (U+200B, U+FEFF).
4. Clean Text Generation & Normalization.
5. Fraud Score Calibration.
"""

import io
import sys
import fitz  # PyMuPDF
from forensic_inspector import ResumeForensicInspector

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


import os

def create_synthetic_pdf(
    visible_lines: list,
    white_lines: list = None,
    micro_lines: list = None,
    zero_width_text: str = None
) -> bytes:
    """Create an in-memory PDF with specified visible and adversarial elements."""
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)  # Standard Letter size

    # Register TrueType Unicode font for UTF-8 and foreign script support
    fontname = None
    for candidate_font in ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf", "C:/Windows/Fonts/segoeui.ttf"]:
        if os.path.exists(candidate_font):
            page.insert_font(fontname="f0", fontfile=candidate_font)
            fontname = "f0"
            break

    y = 50
    # 1. Insert normal visible text (black color, standard size)
    for line in visible_lines:
        page.insert_text(
            fitz.Point(50, y),
            line,
            fontsize=11,
            color=(0, 0, 0),  # Black text
            fontname=fontname
        )
        y += 20

    # 2. Insert adversarial white text (color = (1, 1, 1) or #FFFFFF)
    if white_lines:
        for line in white_lines:
            page.insert_text(
                fitz.Point(50, y),
                line,
                fontsize=10,
                color=(1, 1, 1),  # Pure White text (#FFFFFF)
                fontname=fontname
            )
            y += 15

    # 3. Insert micro-font text (< 2.0 pt)
    if micro_lines:
        for line in micro_lines:
            page.insert_text(
                fitz.Point(50, y),
                line,
                fontsize=1.5,  # Micro-font text
                color=(0, 0, 0),
                fontname=fontname
            )
            y += 10

    # 4. Insert text with zero-width characters
    if zero_width_text:
        page.insert_text(
            fitz.Point(50, y),
            zero_width_text,
            fontsize=10,
            color=(0, 0, 0),
            fontname=fontname
        )

    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def test_clean_pdf():
    print("\n--- 1. Testing Clean Resume PDF ---")
    inspector = ResumeForensicInspector()
    clean_pdf = create_synthetic_pdf(
        visible_lines=[
            "John Doe - Senior Software Engineer",
            "Email: john.doe@email.com | Phone: 9876543210",
            "Experience: 5 years in Python, FastAPI, PostgreSQL, and Docker.",
            "Education: Bachelor of Technology in Computer Science."
        ]
    )

    result = inspector.inspect_pdf(clean_pdf)
    assert result["fraud_score"] == 0.0, f"Expected 0.0 fraud score, got {result['fraud_score']}"
    assert result["has_hidden_text"] is False
    assert result["has_homoglyphs"] is False
    assert result["has_zero_width_chars"] is False
    assert "FastAPI" in result["clean_text"]
    print("✅ Clean PDF: Fraud Score = 0.0%, Has Exploits = False - PASS")


def test_hidden_white_text_and_micro_font():
    print("\n--- 2. Testing Hidden / White Text & Micro-Font Injections ---")
    inspector = ResumeForensicInspector()
    adversarial_pdf = create_synthetic_pdf(
        visible_lines=[
            "Alice Smith - Junior Developer",
            "Skills: HTML, CSS, JavaScript"
        ],
        white_lines=[
            "HIDDEN_KEYWORDS: Kubernetes AWS Terraform PyTorch Machine_Learning Docker",
            "CRITICAL_REQUIREMENT: 10_YEARS_EXPERIENCE_SECRET_ATS_BOOST"
        ],
        micro_lines=[
            "MICRO_FONT_SKILL: Golang Rust Microservices"
        ]
    )

    result = inspector.inspect_pdf(adversarial_pdf)
    assert result["has_hidden_text"] is True, "Should detect hidden text"
    assert result["fraud_score"] >= 35.0, f"Fraud score should be penalized, got {result['fraud_score']}"
    assert len(result["hidden_keywords"]) >= 5, f"Should extract hidden keywords, got {len(result['hidden_keywords'])}"
    
    # Verify keywords extracted with bounding boxes
    sample = result["hidden_keywords"][0]
    assert "keyword" in sample
    assert "bbox" in sample
    assert "reasons" in sample

    # Verify that clean_text EXCLUDES the hidden keywords
    assert "Kubernetes" not in result["clean_text"], "Hidden text must NOT be present in clean_text"
    assert "MICRO_FONT_SKILL" not in result["clean_text"], "Micro font text must NOT be in clean_text"
    assert "Alice Smith" in result["clean_text"], "Visible text must be preserved"

    print(f"✅ Hidden Text Detected: Found {len(result['hidden_keywords'])} hidden tokens.")
    print(f"   Sample Token: '{sample['keyword']}' BBox: {sample['bbox']} Reasons: {sample['reasons']}")
    print(f"   Fraud Score Penalized: {result['fraud_score']}% - PASS")


def test_homoglyph_spoofing():
    print("\n--- 3. Testing Homoglyph & Unicode Character Spoofing ---")
    inspector = ResumeForensicInspector()
    
    # Create text with Cyrillic replacements:
    # 'Pуthоn' -> 'у' is Cyrillic \u0443, 'о' is Cyrillic \u043e
    # 'Dоckеr' -> 'о' is Cyrillic \u043e, 'е' is Cyrillic \u0435
    # 'АWS' -> 'А' is Cyrillic \u0410
    spoofed_lines = [
        "Software Engineer with 4 years building APIs.",
        "Skills: P\u0443th\u043en, D\u043eck\u0435r, \u0410WS, PostgreSQL"
    ]
    
    pdf_bytes = create_synthetic_pdf(visible_lines=spoofed_lines)
    result = inspector.inspect_pdf(pdf_bytes)

    assert result["has_homoglyphs"] is True, "Should detect homoglyph characters"
    assert len(result["spoofed_words"]) >= 2, f"Expected spoofed words, got {len(result['spoofed_words'])}"
    
    spoof_names = [s["original_word"] for s in result["spoofed_words"]]
    normalized_names = [s["normalized_word"] for s in result["spoofed_words"]]
    
    print(f"✅ Spoofed Words Detected: {spoof_names}")
    print(f"   Normalized Counterparts: {normalized_names}")
    
    # Verify clean_text has normalized them to valid ASCII
    assert "Python" in result["clean_text"], "clean_text should contain normalized 'Python'"
    assert "Docker" in result["clean_text"], "clean_text should contain normalized 'Docker'"
    assert "AWS" in result["clean_text"], "clean_text should contain normalized 'AWS'"
    
    sample_detail = result["spoofed_words"][0]["details"][0]
    print(f"   Unicode Info: Hex={sample_detail['unicode_hex']}, Name={sample_detail['unicode_name']}, Script={sample_detail['script']} - PASS")


def test_zero_width_invisible_characters():
    print("\n--- 4. Testing Zero-Width & Invisible Characters ---")
    inspector = ResumeForensicInspector()
    
    # Insert zero-width spaces (\u200B) and zero-width joiners (\u200D) into keywords
    # e.g., P\u200By\u200Bt\u200Bh\u200Bo\u200Bn
    zero_width_payload = (
        "Proficient in P\u200By\u200Bt\u200Bh\u200Bo\u200Bn and J\u200CavaScript.\uFEFF"
    )
    pdf_bytes = create_synthetic_pdf(
        visible_lines=["Robert Vance - Developer"],
        zero_width_text=zero_width_payload
    )

    result = inspector.inspect_pdf(pdf_bytes)
    assert result["has_zero_width_chars"] is True
    assert result["zero_width_count"] >= 5, f"Expected >= 5 zero-width tokens, got {result['zero_width_count']}"
    
    # Ensure zero-width chars are removed in clean_text
    assert "\u200B" not in result["clean_text"]
    assert "\u200C" not in result["clean_text"]
    assert "\uFEFF" not in result["clean_text"]
    assert "Python" in result["clean_text"]
    
    print(f"✅ Zero-Width Detected: {result['zero_width_count']} invisible characters found and stripped.")
    print(f"   Sanitized Text Output: '{result['clean_text']}' - PASS")


def test_combined_adversarial_pdf():
    print("\n--- 5. Testing Multi-Vector Adversarial Attack ---")
    inspector = ResumeForensicInspector()
    
    # Combined attack: White text + Homoglyph spoofing + Zero-width characters
    multi_attack_pdf = create_synthetic_pdf(
        visible_lines=[
            "Hacker Candidate - Testing ATS System",
            "Legitimate Skills: P\u0443th\u043en, SQL"  # Homoglyph
        ],
        white_lines=[
            "SECRET_SKILLS: Kubernetes Docker Cloud Microservices DeepLearning"  # White font
        ],
        micro_lines=[
            "TINY: PyTorch TensorFlow"  # Micro font
        ],
        zero_width_text="H\u200Bi\u200Bd\u200Bd\u200Be\u200Bn Payload\uFEFF"  # Zero-width
    )

    result = inspector.inspect_pdf(multi_attack_pdf)
    assert result["has_hidden_text"] is True
    assert result["has_homoglyphs"] is True
    assert result["has_zero_width_chars"] is True
    assert result["fraud_score"] >= 80.0, f"Combined attack should receive high fraud score, got {result['fraud_score']}"
    
    print(f"🚨 Multi-Vector Attack Caught: Fraud Score = {result['fraud_score']}%")
    print("   Audit Logs for UI Display:")
    for log in result["logs"]:
        print(f"   | {log}")
    print("✅ Multi-Vector Defense - PASS")


if __name__ == "__main__":
    print("==================================================")
    print("RUNNING RESUME FORENSIC INSPECTOR TEST SUITE")
    print("==================================================")
    test_clean_pdf()
    test_hidden_white_text_and_micro_font()
    test_homoglyph_spoofing()
    test_zero_width_invisible_characters()
    test_combined_adversarial_pdf()
    print("\n==================================================")
    print("ALL FORENSIC INSPECTOR TESTS PASSED (100% SUCCESS)!")
    print("==================================================")
