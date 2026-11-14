"""Robust PDF text extraction using pdfplumber."""

import io
from typing import Dict, Any, Union
import pdfplumber


def extract_text_from_pdf(file_input: Union[str, bytes, io.BytesIO]) -> Dict[str, Any]:
    """Extract text safely from a PDF file.
    
    Accepts a filepath, bytes, or BytesIO buffer (from Streamlit uploader).
    Returns a dictionary with success status, extracted text, page count, and any error message.
    """
    result: Dict[str, Any] = {
        "success": False,
        "text": "",
        "page_count": 0,
        "error": None
    }
    
    try:
        # Wrap bytes in BytesIO if needed
        if isinstance(file_input, bytes):
            pdf_source = io.BytesIO(file_input)
        elif hasattr(file_input, "read"):
            # Streamlit UploadedFile or file-like object
            content = file_input.read()
            if hasattr(file_input, "seek"):
                file_input.seek(0)
            pdf_source = io.BytesIO(content)
        else:
            pdf_source = file_input

        with pdfplumber.open(pdf_source) as pdf:
            pages_text = []
            result["page_count"] = len(pdf.pages)
            
            for page_idx, page in enumerate(pdf.pages):
                try:
                    text = page.extract_text(layout=True)
                    if not text:
                        text = page.extract_text()
                    if text and text.strip():
                        pages_text.append(text.strip())
                except Exception as page_err:
                    # Continue extracting other pages even if one fails
                    continue
            
            full_text = "\n\n".join(pages_text).strip()
            
            if not full_text:
                result["error"] = "No readable text found in PDF (file may be empty or scanned image)."
                return result

            result["text"] = full_text
            result["success"] = True
            return result

    except Exception as exc:
        result["error"] = f"Failed to parse PDF document: {str(exc)}"
        return result
