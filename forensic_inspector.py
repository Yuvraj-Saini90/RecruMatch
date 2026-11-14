"""Resume Forensic Inspector (Adversarial ATS Exploit & Fraud Detector).

Analyzes uploaded PDF resumes for adversarial ATS evasion techniques:
1. Hidden / White Text & Micro-Font Injections.
2. Homoglyph & Unicode Character Spoofing (Cyrillic/Greek disguised in English words).
3. Zero-Width & Invisible Characters (U+200B - U+200D, U+FEFF).
4. Generates an overall Fraud Score (0-100%) and a Sanitized Clean Text payload.
"""

import io
import re
import unicodedata
from typing import Dict, Any, List, Union, Optional, Tuple
import fitz  # PyMuPDF


# Standard homoglyph mapping: Non-Latin characters visually resembling Latin ASCII
HOMOGLYPH_LOOKUP: Dict[str, str] = {
    # Cyrillic small letters
    "\u0430": "a", "\u0435": "e", "\u043e": "o", "\u0440": "p",
    "\u0441": "c", "\u0443": "y", "\u0445": "x", "\u0456": "i",
    "\u0458": "j", "\u0455": "s", "\u0432": "b", "\u0442": "t",
    "\u0501": "d", "\u051b": "q",
    # Cyrillic capital letters
    "\u0410": "A", "\u0412": "B", "\u0421": "C", "\u0415": "E",
    "\u041d": "H", "\u041e": "O", "\u0420": "P", "\u0422": "T",
    "\u0423": "Y", "\u0425": "X", "\u0406": "I", "\u0405": "S",
    # Greek small letters
    "\u03b1": "a", "\u03b2": "b", "\u03b5": "e", "\u03b7": "n",
    "\u03b9": "i", "\u03ba": "k", "\u03bf": "o", "\u03c1": "p",
    "\u03c4": "t", "\u03c5": "u", "\u03c7": "x",
    # Greek capital letters
    "\u0391": "A", "\u0392": "B", "\u0395": "E", "\u0397": "H",
    "\u0399": "I", "\u039a": "K", "\u039f": "O", "\u03a1": "P",
    "\u03a4": "T", "\u03a5": "Y", "\u03a7": "X"
}

# Regex for zero-width and invisible unicode characters
ZERO_WIDTH_REGEX = re.compile(r"[\u200B-\u200D\uFEFF\u200E\u200F\u2060]")


class ResumeForensicInspector:
    """Security inspector for detecting adversarial exploits and fraud in PDF resumes."""

    def __init__(
        self,
        min_font_size: float = 2.0,
        white_color_threshold: int = 16777210,
        white_rgb_cutoff: int = 248
    ):
        """Initialize the forensic inspector with detection thresholds.
        
        Args:
            min_font_size: Font size in pt below which text is considered micro-font.
            white_color_threshold: sRGB integer near or equal to 0xFFFFFF (16777215).
            white_rgb_cutoff: Minimum R, G, B channel value (0-255) considered white.
        """
        self.min_font_size = min_font_size
        self.white_color_threshold = white_color_threshold
        self.white_rgb_cutoff = white_rgb_cutoff

    def is_white_color(self, color_val: Any) -> bool:
        """Check whether a color value represents white or near-white color."""
        if color_val is None:
            return False

        # Integer color representation (standard PyMuPDF sRGB int)
        if isinstance(color_val, int):
            if color_val >= self.white_color_threshold:
                return True
            # Extract RGB channels from integer
            r = (color_val >> 16) & 255
            g = (color_val >> 8) & 255
            b = color_val & 255
            return (r >= self.white_rgb_cutoff and 
                    g >= self.white_rgb_cutoff and 
                    b >= self.white_rgb_cutoff)

        # Tuple or list representation (e.g. (1.0, 1.0, 1.0) or (255, 255, 255))
        if isinstance(color_val, (tuple, list)) and len(color_val) >= 3:
            r, g, b = color_val[:3]
            if isinstance(r, float) and r <= 1.0:
                return r >= 0.98 and g >= 0.98 and b >= 0.98
            return r >= self.white_rgb_cutoff and g >= self.white_rgb_cutoff and b >= self.white_rgb_cutoff

        # String hex representation (e.g. '#FFFFFF' or '0xFFFFFF')
        if isinstance(color_val, str):
            c_str = color_val.strip().upper().replace("#", "").replace("0X", "")
            return c_str in ("FFFFFF", "FFFFFE", "FEFEFE")

        return False

    def scan_zero_width_chars(self, text: str) -> List[Dict[str, Any]]:
        """Find all zero-width and invisible unicode characters in text."""
        findings = []
        if not text:
            return findings

        for match in ZERO_WIDTH_REGEX.finditer(text):
            ch = match.group()
            code_point = f"U+{ord(ch):04X}"
            try:
                name = unicodedata.name(ch)
            except ValueError:
                name = "INVISIBLE_UNICODE_CHARACTER"

            findings.append({
                "char": ch,
                "index": match.start(),
                "unicode_hex": code_point,
                "name": name
            })
        return findings

    def scan_homoglyphs(self, text: str) -> Tuple[List[Dict[str, Any]], str]:
        """Detect foreign script homoglyphs substituted inside English words.
        
        Returns:
            Tuple of (detected_spoofs_list, normalized_text)
        """
        spoofed_words = []
        if not text:
            return spoofed_words, ""

        # Normalize with lookup map while tracking spoofed tokens
        normalized_chars = []
        # Tokenize by whitespace and word boundaries
        words = text.split()

        for word in words:
            word_spoofs = []
            has_latin = any(c.isascii() and c.isalpha() for c in word)
            
            for idx, ch in enumerate(word):
                if ch in HOMOGLYPH_LOOKUP:
                    # If the word contains Latin characters or is predominantly alphanumeric
                    sub = HOMOGLYPH_LOOKUP[ch]
                    try:
                        u_name = unicodedata.name(ch)
                    except ValueError:
                        u_name = "UNKNOWN_SCRIPT_CHARACTER"

                    script = "Cyrillic" if "CYRILLIC" in u_name else ("Greek" if "GREEK" in u_name else "Foreign Script")
                    
                    word_spoofs.append({
                        "spoofed_char": ch,
                        "normalized_char": sub,
                        "unicode_hex": f"U+{ord(ch):04X}",
                        "unicode_name": u_name,
                        "script": script,
                        "char_index_in_word": idx
                    })

            if word_spoofs and (has_latin or len(word_spoofs) < len(word)):
                # Word has been spoofed with mixed characters
                normalized_word = "".join(HOMOGLYPH_LOOKUP.get(c, c) for c in word)
                spoofed_words.append({
                    "original_word": word,
                    "normalized_word": normalized_word,
                    "spoof_count": len(word_spoofs),
                    "details": word_spoofs
                })

        # Produce fully normalized text
        clean_chars = [HOMOGLYPH_LOOKUP.get(ch, ch) for ch in text]
        normalized_text = "".join(clean_chars)
        return spoofed_words, normalized_text

    def inspect_pdf(self, pdf_input: Union[str, bytes, io.BytesIO]) -> Dict[str, Any]:
        """Perform comprehensive forensic inspection on a PDF document.
        
        Args:
            pdf_input: File path (str), raw PDF bytes (bytes), or BytesIO stream.
            
        Returns:
            Structured dictionary with fraud_score, detection flags, clean_text, and logs.
        """
        logs = []
        hidden_keywords = []
        clean_text_parts = []
        raw_text_parts = []

        doc = None
        try:
            if isinstance(pdf_input, str):
                doc = fitz.open(pdf_input)
            elif isinstance(pdf_input, (bytes, bytearray)):
                doc = fitz.open(stream=pdf_input, filetype="pdf")
            elif isinstance(pdf_input, io.BytesIO):
                doc = fitz.open(stream=pdf_input.getvalue(), filetype="pdf")
            else:
                raise ValueError(f"Unsupported pdf_input type: {type(pdf_input)}")

            logs.append(f"[INFO] Initialized Forensic Inspector. Document has {len(doc)} pages.")

            # Step A: Hidden / White Text & Micro-Font Detection via Text Dict
            for page_idx, page in enumerate(doc, start=1):
                page_dict = page.get_text("dict")
                page_clean_spans = []

                for block in page_dict.get("blocks", []):
                    # Process text blocks (type 0 is text)
                    if block.get("type") == 0:
                        for line in block.get("lines", []):
                            line_spans = []
                            for span in line.get("spans", []):
                                span_text = span.get("text", "")
                                if not span_text.strip():
                                    continue

                                color = span.get("color")
                                size = span.get("size", 10.0)
                                bbox = span.get("bbox", [])

                                is_white = self.is_white_color(color)
                                is_micro = size < self.min_font_size

                                if is_white or is_micro:
                                    reason = []
                                    if is_white:
                                        reason.append("White/Near-White Color (#FFFFFF)")
                                    if is_micro:
                                        reason.append(f"Micro-Font Size ({size:.1f}pt < {self.min_font_size}pt)")

                                    # Extract individual keywords
                                    words = [w.strip() for w in span_text.split() if len(w.strip()) > 1]
                                    for word in words:
                                        hidden_keywords.append({
                                            "keyword": word,
                                            "full_text": span_text.strip(),
                                            "page": page_idx,
                                            "bbox": [round(coord, 1) for coord in bbox],
                                            "font_size": round(size, 2),
                                            "color_int": color,
                                            "reasons": reason
                                        })

                                    logs.append(
                                        f"⚠️ [EXPLOIT DETECTED] Page {page_idx}: Hidden text found "
                                        f"('{span_text.strip()[:40]}...') Reason: {', '.join(reason)} "
                                        f"BBox: {[round(c, 1) for c in bbox]}"
                                    )
                                else:
                                    # Legitimate visible span
                                    line_spans.append(span_text)

                            if line_spans:
                                page_clean_spans.append(" ".join(line_spans))

                clean_text_parts.append("\n".join(page_clean_spans))
                raw_text_parts.append(page.get_text())

        except Exception as e:
            logs.append(f"❌ [ERROR] Forensic inspection failed: {str(e)}")
            return {
                "fraud_score": 100.0,
                "has_hidden_text": False,
                "hidden_keywords": [],
                "has_homoglyphs": False,
                "spoofed_words": [],
                "has_zero_width_chars": False,
                "zero_width_count": 0,
                "clean_text": "",
                "logs": logs,
                "error": str(e)
            }
        finally:
            if doc:
                doc.close()

        # Concatenate extracted content
        extracted_visible_text = "\n\n".join(clean_text_parts)
        full_raw_text = "\n\n".join(raw_text_parts)

        # Step B: Zero-Width Character Scanning (scanned on raw text to catch all invisible payload tokens)
        zero_width_findings = self.scan_zero_width_chars(full_raw_text)
        has_zero_width = len(zero_width_findings) > 0
        if has_zero_width:
            logs.append(
                f"[SECURITY ALERT] Found {len(zero_width_findings)} zero-width / invisible unicode "
                f"characters (e.g. {zero_width_findings[0]['unicode_hex']} {zero_width_findings[0]['name']})."
            )

        # Step C: Strip zero-width chars from visible text so word boundaries are intact
        text_without_zero_width = ZERO_WIDTH_REGEX.sub("", extracted_visible_text)

        # Step D: Homoglyph & Unicode Character Spoofing Detection
        spoofed_words, text_normalized = self.scan_homoglyphs(text_without_zero_width)
        has_homoglyphs = len(spoofed_words) > 0
        if has_homoglyphs:
            sample_spoof = spoofed_words[0]
            logs.append(
                f"[SECURITY WARNING] Found {len(spoofed_words)} homoglyph-spoofed words. "
                f"Example: '{sample_spoof['original_word']}' -> '{sample_spoof['normalized_word']}' "
                f"({sample_spoof['details'][0]['script']} {sample_spoof['details'][0]['unicode_hex']})."
            )

        # Step E: Produce Final Clean Text
        # Replace non-breaking spaces and soft hyphens
        normalized_whitespace = text_normalized.replace("\xa0", " ").replace("\xad", "-")
        # Normalize excessive whitespace
        sanitized_text = re.sub(r"[ \t]+", " ", normalized_whitespace)
        sanitized_text = re.sub(r"\n{3,}", "\n\n", sanitized_text).strip()

        # Step F: Calculate Overall Fraud Score (0% to 100%)
        fraud_score = self._calculate_fraud_score(
            hidden_count=len(hidden_keywords),
            homoglyph_count=len(spoofed_words),
            zero_width_count=len(zero_width_findings)
        )

        has_hidden = len(hidden_keywords) > 0
        if fraud_score == 0.0:
            logs.append("[VERIFIED CLEAN] No hidden text, zero-width chars, or homoglyphs detected.")
        else:
            logs.append(
                f"[AUDIT SUMMARY] Calculated Fraud Score: {fraud_score}%. "
                f"Hidden Tokens: {len(hidden_keywords)}, Spoofed Words: {len(spoofed_words)}, "
                f"Invisible Chars: {len(zero_width_findings)}."
            )

        return {
            "fraud_score": fraud_score,
            "has_hidden_text": has_hidden,
            "hidden_keywords": hidden_keywords,
            "has_homoglyphs": has_homoglyphs,
            "spoofed_words": spoofed_words,
            "has_zero_width_chars": has_zero_width,
            "zero_width_count": len(zero_width_findings),
            "clean_text": sanitized_text,
            "logs": logs
        }

    def _calculate_fraud_score(
        self,
        hidden_count: int,
        homoglyph_count: int,
        zero_width_count: int
    ) -> float:
        """Calculate a balanced 0.0% to 100.0% fraud score based on detected vectors."""
        score = 0.0

        # Hidden text penalty (high severity: deliberate attempt to keyword-stuff ATS)
        if hidden_count > 0:
            score += 35.0 + min(35.0, hidden_count * 2.5)

        # Homoglyph spoofing penalty (high severity: deliberate font/script obfuscation)
        if homoglyph_count > 0:
            score += 30.0 + min(30.0, homoglyph_count * 5.0)

        # Zero-width character penalty (medium-high severity: keyword splitting / payload injection)
        if zero_width_count > 0:
            score += 20.0 + min(20.0, zero_width_count * 2.0)

        return round(min(100.0, score), 1)
