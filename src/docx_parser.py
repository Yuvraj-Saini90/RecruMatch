"""Robust DOCX text extraction using python-docx."""

import io
from typing import Dict, Any, Union
import docx


def extract_text_from_docx(file_input: Union[str, bytes, io.BytesIO]) -> Dict[str, Any]:
    """Extract text safely from a DOCX file, including both paragraphs and tables.
    
    Accepts a filepath, bytes, or BytesIO buffer (from Streamlit uploader).
    Returns a dictionary with success status, extracted text, paragraph count, and any error message.
    """
    result: Dict[str, Any] = {
        "success": False,
        "text": "",
        "paragraph_count": 0,
        "table_count": 0,
        "error": None
    }
    
    try:
        if isinstance(file_input, bytes):
            docx_source = io.BytesIO(file_input)
        elif hasattr(file_input, "read"):
            content = file_input.read()
            if hasattr(file_input, "seek"):
                file_input.seek(0)
            docx_source = io.BytesIO(content)
        else:
            docx_source = file_input

        doc = docx.Document(docx_source)
        
        extracted_chunks = []
        result["paragraph_count"] = len(doc.paragraphs)
        result["table_count"] = len(doc.tables)

        # 1. Extract regular paragraphs
        for para in doc.paragraphs:
            clean_para = para.text.strip()
            if clean_para:
                extracted_chunks.append(clean_para)

        # 2. Extract content from tables (skills & qualifications are often in tables)
        for table in doc.tables:
            for row in table.rows:
                row_texts = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_texts:
                    # De-duplicate adjacent identical cell values (merged cells)
                    unique_cells = []
                    for t in row_texts:
                        if not unique_cells or t != unique_cells[-1]:
                            unique_cells.append(t)
                    extracted_chunks.append(" | ".join(unique_cells))

        full_text = "\n\n".join(extracted_chunks).strip()
        
        if not full_text:
            result["error"] = "No readable text found in DOCX file (file may be blank)."
            return result

        result["text"] = full_text
        result["success"] = True
        return result

    except Exception as exc:
        result["error"] = f"Failed to parse DOCX document: {str(exc)}"
        return result
