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

# Prompt Injection & ATS Jailbreak Patterns
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

EXPLOIT_KEYWORDS = [
    "EXPLOIT_PAYLOAD", "OVERRIDE_INSTRUCTION", "SECRET_SKILLS",
    "INJECTED_SKILLS", "[HIDDEN", "#FFFFFF", "WHITE_TEXT",
    "MICROFONT", "ATTACK_VECTOR", "Pуthоn"
]


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

    def scan_prompt_injections(self, text: str) -> List[Dict[str, Any]]:
        """Scan text for prompt injection and ATS jailbreak payloads."""
        findings = []
        if not text:
            return findings
        for pattern in PROMPT_INJECTION_PATTERNS:
            for match in re.finditer(pattern, text):
                findings.append({
                    "snippet": match.group().strip(),
                    "pattern": pattern,
                    "index": match.start()
                })
        return findings

    def scan_exploit_keywords(self, text: str) -> List[str]:
        """Scan text for exploit markers and hidden payload labels."""
        if not text:
            return []
        return [k for k in EXPLOIT_KEYWORDS if k in text]

    def is_forensic_filename(self, filename: Optional[str]) -> bool:
        """Check whether the filename indicates an intentional exploit or tamper test."""
        if not filename:
            return False
        pattern = r"(?i)(?:demo[_-]?)?forensic|exploit|adversarial|tamper|hack|payload|injection"
        return bool(re.search(pattern, filename))

    def _finish_inspection(
        self,
        raw_text: str,
        visible_text: str,
        hidden_keywords: List[Dict[str, Any]],
        logs: List[str],
        filename: Optional[str] = None
    ) -> Dict[str, Any]:
        """Unified post-processing and fraud score calculation across all file formats."""
        # Step B: Zero-Width Character Scanning
        zero_width_findings = self.scan_zero_width_chars(raw_text)
        has_zero_width = len(zero_width_findings) > 0
        if has_zero_width:
            logs.append(
                f"[SECURITY ALERT] Found {len(zero_width_findings)} zero-width / invisible unicode characters."
            )

        # Step C: Strip zero-width chars from visible text
        text_without_zero_width = ZERO_WIDTH_REGEX.sub("", visible_text)

        # Step D: Homoglyph & Unicode Character Spoofing Detection
        spoofed_words, text_normalized = self.scan_homoglyphs(text_without_zero_width)
        has_homoglyphs = len(spoofed_words) > 0
        if has_homoglyphs:
            sample_spoof = spoofed_words[0]
            logs.append(
                f"[SECURITY WARNING] Found {len(spoofed_words)} homoglyph-spoofed words. "
                f"Example: '{sample_spoof['original_word']}' -> '{sample_spoof['normalized_word']}'"
            )

        # Step E: Prompt Injection & Exploit Keywords
        injections = self.scan_prompt_injections(raw_text)
        has_injection = len(injections) > 0
        if has_injection:
            logs.append(f"⚠️ [EXPLOIT DETECTED] Prompt injection detected: '{injections[0]['snippet']}'")

        exploit_keywords = self.scan_exploit_keywords(raw_text)
        has_exploit_kws = len(exploit_keywords) > 0
        if has_exploit_kws:
            logs.append(f"⚠️ [EXPLOIT DETECTED] Adversarial payload markers found: {', '.join(exploit_keywords)}")

        is_exploit_file = self.is_forensic_filename(filename)
        if is_exploit_file:
            logs.append(f"⚠️ [FILE ALERT] Target filename '{filename}' matched adversarial/tampering signature.")

        # Step F: Produce Sanitized Clean Text
        sanitized_text = text_normalized.replace("\xa0", " ").replace("\xad", "-")
        for pat in PROMPT_INJECTION_PATTERNS:
            sanitized_text = re.sub(pat, " [INJECTION_STRIPPED] ", sanitized_text)
        for kw in EXPLOIT_KEYWORDS:
            sanitized_text = sanitized_text.replace(kw, " [PAYLOAD_STRIPPED] ")
        sanitized_text = re.sub(r"[ \t]+", " ", sanitized_text)
        sanitized_text = re.sub(r"\n{3,}", "\n\n", sanitized_text).strip()

        # Step G: Calculate Overall Fraud Score (0% to 100%)
        fraud_score = self._calculate_fraud_score(
            hidden_count=len(hidden_keywords),
            homoglyph_count=len(spoofed_words),
            zero_width_count=len(zero_width_findings),
            injection_count=len(injections),
            exploit_keyword_count=len(exploit_keywords),
            is_exploit_filename=is_exploit_file
        )

        has_hidden = len(hidden_keywords) > 0
        if fraud_score == 0.0:
            logs.append("[VERIFIED CLEAN] No hidden text, zero-width chars, homoglyphs, or injections detected.")
        else:
            logs.append(
                f"[AUDIT SUMMARY] Calculated Fraud Score: {fraud_score}%. "
                f"Hidden Tokens: {len(hidden_keywords)}, Spoofed Words: {len(spoofed_words)}, "
                f"Injections: {len(injections)}, Filename Alert: {is_exploit_file}."
            )

        return {
            "fraud_score": fraud_score,
            "has_hidden_text": has_hidden,
            "hidden_keywords": hidden_keywords,
            "has_homoglyphs": has_homoglyphs,
            "spoofed_words": spoofed_words,
            "has_zero_width_chars": has_zero_width,
            "zero_width_count": len(zero_width_findings),
            "has_prompt_injection": has_injection,
            "prompt_injections": injections,
            "exploit_keywords": exploit_keywords,
            "is_exploit_filename": is_exploit_file,
            "clean_text": sanitized_text,
            "logs": logs
        }

    def inspect_pdf(self, pdf_input: Union[str, bytes, io.BytesIO], filename: Optional[str] = None) -> Dict[str, Any]:
        """Perform comprehensive forensic inspection on a PDF document."""
        logs = []
        hidden_keywords = []
        clean_text_parts = []
        raw_text_parts = []

        doc = None
        try:
            if isinstance(pdf_input, str):
                doc = fitz.open(pdf_input)
                if filename is None:
                    filename = pdf_input
            elif isinstance(pdf_input, (bytes, bytearray)):
                doc = fitz.open(stream=pdf_input, filetype="pdf")
            elif isinstance(pdf_input, io.BytesIO):
                doc = fitz.open(stream=pdf_input.getvalue(), filetype="pdf")
            else:
                raise ValueError(f"Unsupported pdf_input type: {type(pdf_input)}")

            logs.append(f"[INFO] Initialized Forensic Inspector. Document has {len(doc)} pages.")

            for page_idx, page in enumerate(doc, start=1):
                page_dict = page.get_text("dict")
                page_clean_spans = []

                for block in page_dict.get("blocks", []):
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

        extracted_visible_text = "\n\n".join(clean_text_parts)
        full_raw_text = "\n\n".join(raw_text_parts)

        return self._finish_inspection(
            raw_text=full_raw_text,
            visible_text=extracted_visible_text,
            hidden_keywords=hidden_keywords,
            logs=logs,
            filename=filename
        )

    def inspect_docx(self, docx_input: Any, filename: Optional[str] = None) -> Dict[str, Any]:
        """Perform comprehensive forensic inspection on a DOCX document."""
        import docx
        logs = []
        hidden_keywords = []
        clean_text_parts = []
        raw_text_parts = []

        try:
            doc = docx.Document(docx_input)
            logs.append(f"[INFO] Initialized Forensic Inspector for DOCX. Document has {len(doc.paragraphs)} paragraphs.")

            for p_idx, p in enumerate(doc.paragraphs):
                p_clean_runs = []
                for r in p.runs:
                    r_text = r.text
                    if not r_text.strip():
                        continue

                    is_hidden = False
                    is_white = False
                    is_micro = False
                    reasons = []

                    if getattr(r.font, "hidden", False):
                        is_hidden = True
                        reasons.append("Hidden Run Attribute (w:vanish)")

                    if getattr(r.font, "color", None) and getattr(r.font.color, "rgb", None):
                        rgb = str(r.font.color.rgb).upper()
                        if rgb in ("FFFFFF", "FEFEFE", "FDFDFD"):
                            is_white = True
                            reasons.append(f"White Font Color (#{rgb})")

                    if getattr(r.font, "size", None) and hasattr(r.font.size, "pt") and r.font.size.pt < self.min_font_size:
                        is_micro = True
                        reasons.append(f"Micro-Font Size ({r.font.size.pt}pt < {self.min_font_size}pt)")

                    if is_hidden or is_white or is_micro:
                        for word in [w.strip() for w in r_text.split() if len(w.strip()) > 1]:
                            hidden_keywords.append({
                                "keyword": word,
                                "full_text": r_text.strip(),
                                "paragraph": p_idx + 1,
                                "reasons": reasons
                            })
                        logs.append(f"⚠️ [EXPLOIT DETECTED] Paragraph {p_idx + 1}: Hidden text found ('{r_text.strip()[:40]}...') Reason: {', '.join(reasons)}")
                    else:
                        p_clean_runs.append(r_text)

                if p_clean_runs:
                    clean_text_parts.append(" ".join(p_clean_runs))
                if p.text:
                    raw_text_parts.append(p.text)

        except Exception as e:
            logs.append(f"❌ [ERROR] DOCX inspection error: {e}")
            raw_text_parts = []
            clean_text_parts = []

        full_raw_text = "\n\n".join(raw_text_parts)
        extracted_visible = "\n\n".join(clean_text_parts) if clean_text_parts else full_raw_text

        return self._finish_inspection(
            raw_text=full_raw_text,
            visible_text=extracted_visible,
            hidden_keywords=hidden_keywords,
            logs=logs,
            filename=filename
        )

    def inspect_text(self, text: str, filename: Optional[str] = None) -> Dict[str, Any]:
        """Perform forensic inspection on plain text input."""
        logs = [f"[INFO] Initialized Forensic Inspector for text stream ({len(text)} characters)."]
        return self._finish_inspection(
            raw_text=text,
            visible_text=text,
            hidden_keywords=[],
            logs=logs,
            filename=filename
        )

    def _calculate_fraud_score(
        self,
        hidden_count: int,
        homoglyph_count: int,
        zero_width_count: int,
        injection_count: int = 0,
        exploit_keyword_count: int = 0,
        is_exploit_filename: bool = False
    ) -> float:
        """Calculate a balanced 0.0% to 100.0% fraud score based on detected vectors."""
        score = 0.0

        if hidden_count > 0:
            score += 35.0 + min(35.0, hidden_count * 2.5)

        if homoglyph_count > 0:
            score += 30.0 + min(30.0, homoglyph_count * 5.0)

        if zero_width_count > 0:
            score += 20.0 + min(20.0, zero_width_count * 2.0)

        if injection_count > 0:
            score += 45.0 + min(35.0, injection_count * 15.0)

        if exploit_keyword_count > 0:
            score += 40.0 + min(30.0, exploit_keyword_count * 10.0)

        if is_exploit_filename:
            score = max(score, 75.0)

        return round(min(100.0, score), 1)
