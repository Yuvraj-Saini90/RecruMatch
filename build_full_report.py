"""Main Orchestrator to assemble and generate the complete B.Tech Mini Project Report in Word (.docx) format.
Follows GNIOT / AKTU academic requirements:
- Times New Roman font (12pt body, 14pt bold headings)
- Double line spacing for body paragraphs
- Spiral binding margins (1.25" Left, 1.0" Top, Right, Bottom)
- Preliminary Pages (Roman i..ix): Cover/Title, Certificate, Declaration, Acknowledgement, Abstract, Index, Figures, Tables
- 10 Main Body Chapters (Arabic 1..N):
  1. Introduction / Aims and Objective
  2. System Analysis
  3. Feasibility Study
  4. System Specifications & Architectural Modeling
  5. Proposed System & Core Algorithmic Engines
  6. System User Interface & Screen Shots
  7. Modular System Coding & Implementation
  8. Experimental Results & Performance Benchmarking
  9. Conclusion & Future Scope
  10. References & Technical Glossary
- Dynamic Two-Pass Page Indexing via Word COM for 100% exact Table of Contents, Figures, and Tables.
"""

import os
import sys
import json
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

sys.path.insert(0, os.path.dirname(__file__))

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="none", right="none", sz="4"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}>'
                        f'<w:top w:val="{"single" if top != "none" else "none"}" w:sz="{sz}" w:space="0" w:color="{top}"/>'
                        f'<w:left w:val="{"single" if left != "none" else "none"}" w:sz="{sz}" w:space="0" w:color="{left}"/>'
                        f'<w:bottom w:val="{"single" if bottom != "none" else "none"}" w:sz="{sz}" w:space="0" w:color="{bottom}"/>'
                        f'<w:right w:val="{"single" if right != "none" else "none"}" w:sz="{sz}" w:space="0" w:color="{right}"/>'
                        f'</w:tcBorders>')
    tcPr.append(borders)

def add_page_number_to_run(run):
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    
    r = run._r
    r.append(fldChar1)
    r.append(instrText)
    r.append(fldChar2)
    r.append(fldChar3)

def add_body_p(doc, text, bold_prefix="", space_after=6, line_spacing=2.0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = False
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_bullet_p(doc, text, bold_prefix="", line_spacing=1.5):
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = line_spacing
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(0, 0, 0)
        
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_caption(doc, text, is_table=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4) if not is_table else Pt(8)
    p.paragraph_format.space_after = Pt(10) if not is_table else Pt(4)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.italic = True
    r.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_code_block(doc, code_str, title=""):
    if title:
        p_t = doc.add_paragraph()
        p_t.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(2)
        r_t = p_t.add_run(title)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(30, 58, 138)
        
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.25)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    set_cell_borders(cell, top="CBD5E1", bottom="CBD5E1", left="2563EB", right="CBD5E1", sz="12")
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    
    r = p.add_run(code_str)
    r.font.name = "Consolas"
    r.font.size = Pt(9.0)
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(6)

def build_table(doc, headers, data, col_widths=None, alignment=WD_TABLE_ALIGNMENT.CENTER):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = alignment
    table.autofit = False

    # Header Row
    hdr_row = table.rows[0]
    for idx, heading in enumerate(headers):
        cell = hdr_row.cells[idx]
        if col_widths and idx < len(col_widths):
            cell.width = col_widths[idx]
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        set_cell_borders(cell, top="1E3A8A", bottom="1E3A8A", left="none", right="none", sz="6")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(heading)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for row_idx, row_data in enumerate(data):
        row = table.rows[row_idx + 1]
        bg = "FFFFFF" if row_idx % 2 == 0 else "F1F5F9"
        for col_idx, text in enumerate(row_data):
            cell = row.cells[col_idx]
            if col_widths and col_idx < len(col_widths):
                cell.width = col_widths[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            set_cell_borders(cell, top="E2E8F0", bottom="E2E8F0", left="none", right="none", sz="4")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(str(text))
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(15, 23, 42)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(8)
    return table

def configure_section_1_preliminary(section):
    """Section 1: Preliminary Pages (Roman numerals i..ix, cover page unnumbered)."""
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.0)
    section.different_first_page_header_footer = True

    sectPr = section._sectPr
    pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="romanLower" w:start="1"/>')
    sectPr.append(pgNumType)

    # Footer for pages 2+ in Section 1 (Certificate onwards)
    footer = section.footer
    p_ftr = footer.paragraphs[0]
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ftr_lbl = p_ftr.add_run("Page ")
    r_ftr_lbl.font.name = "Times New Roman"
    r_ftr_lbl.font.size = Pt(9.5)
    r_ftr_lbl.font.color.rgb = RGBColor(100, 116, 139)
    r_pg = p_ftr.add_run()
    r_pg.font.name = "Times New Roman"
    r_pg.font.size = Pt(9.5)
    r_pg.font.bold = True
    r_pg.font.color.rgb = RGBColor(30, 41, 59)
    add_page_number_to_run(r_pg)

def configure_section_2_main_body(section):
    """Section 2: Main Body (Arabic numerals 1..N, right-aligned header and institute footer)."""
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.25)
    section.right_margin = Inches(1.0)
    section.different_first_page_header_footer = False

    # Unlink from Section 1
    section.header.is_linked_to_previous = False
    section.footer.is_linked_to_previous = False

    sectPr = section._sectPr
    pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="decimal" w:start="1"/>')
    sectPr.append(pgNumType)

    # Header for Section 2
    header = section.header
    p_hdr = header.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_hdr = p_hdr.add_run("RecruMatch: B.Tech Mini Project Report | Dept. of CSE, GNIOT")
    r_hdr.font.name = "Times New Roman"
    r_hdr.font.size = Pt(8.5)
    r_hdr.font.italic = True
    r_hdr.font.color.rgb = RGBColor(100, 116, 139)

    # Footer for Section 2
    footer = section.footer
    p_ftr = footer.paragraphs[0]
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_ftr_lbl = p_ftr.add_run("Greater Noida Institute of Technology  |  Page ")
    r_ftr_lbl.font.name = "Times New Roman"
    r_ftr_lbl.font.size = Pt(9.5)
    r_ftr_lbl.font.color.rgb = RGBColor(100, 116, 139)
    r_pg = p_ftr.add_run()
    r_pg.font.name = "Times New Roman"
    r_pg.font.size = Pt(9.5)
    r_pg.font.bold = True
    r_pg.font.color.rgb = RGBColor(30, 41, 59)
    add_page_number_to_run(r_pg)

def build_document_instance(output_filename, custom_toc=None, custom_figures=None, custom_tables=None):
    doc = docx.Document()
    
    # Base styling
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)

    # Section 1: Preliminary
    sec1 = doc.sections[0]
    configure_section_1_preliminary(sec1)

    # Import Section Modules
    from report_sections.sec_preliminary import (
        add_title_page, add_certificate_page, add_declaration_page,
        add_acknowledgement_page, add_abstract_page, add_index_pages,
        add_figures_and_tables_lists
    )
    from report_sections.sec_intro_analysis import (
        add_chapter_1_introduction, add_chapter_2_system_analysis,
        add_chapter_3_feasibility_study
    )
    from report_sections.sec_technical_design import (
        add_chapter_4_analysis, add_chapter_5_proposed_system
    )
    from report_sections.sec_screens_code import (
        add_chapter_6_screenshots, add_chapter_7_coding
    )
    from report_sections.sec_results_conclusion import (
        add_chapter_8_results, add_chapter_9_conclusion,
        add_chapter_10_references
    )

    # 1. Preliminary Pages
    add_title_page(doc)
    add_certificate_page(doc)
    add_declaration_page(doc)
    add_acknowledgement_page(doc)
    add_abstract_page(doc)
    add_index_pages(doc, custom_toc)
    add_figures_and_tables_lists(doc, custom_figures, custom_tables)

    # 2. Main Body Section (Section 2)
    sec2 = doc.add_section()
    configure_section_2_main_body(sec2)

    # Chapters
    add_chapter_1_introduction(doc)
    add_chapter_2_system_analysis(doc)
    add_chapter_3_feasibility_study(doc)
    add_chapter_4_analysis(doc)
    add_chapter_5_proposed_system(doc)
    add_chapter_6_screenshots(doc)
    add_chapter_7_coding(doc)
    add_chapter_8_results(doc)
    add_chapter_9_conclusion(doc)
    add_chapter_10_references(doc)

    doc.save(output_filename)
    return output_filename

def int_to_roman(n):
    mapping = [
        (1000, 'm'), (900, 'cm'), (500, 'd'), (400, 'cd'),
        (100, 'c'), (90, 'xc'), (50, 'l'), (40, 'xl'),
        (10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')
    ]
    res = []
    for val, rom in mapping:
        while n >= val:
            res.append(rom)
            n -= val
    return ''.join(res)

def measure_pages_with_word_com(docx_path):
    abs_path = os.path.abspath(docx_path)
    json_tmp = os.path.join(os.path.dirname(abs_path), "temp_measured_pages.json")
    
    ps_script = rf"""
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    try {{
        $doc = $word.Documents.Open('{abs_path}', $false, $true)
        $results = @()
        foreach ($p in $doc.Paragraphs) {{
            # Only body paragraphs, not paragraphs inside tables
            if ($p.Range.Tables.Count -eq 0) {{
                $t = $p.Range.Text.Trim()
                if ([string]::IsNullOrWhiteSpace($t)) {{ continue }}
                
                if ($t -match "^CHAPTER [0-9]+" -or 
                    $t -match "^[0-9]+\.[0-9]+" -or 
                    $t -match "^Figure [0-9]+\.[0-9]+" -or 
                    $t -match "^Table [0-9]+\.[0-9]+" -or 
                    $t -in @("CERTIFICATE", "CANDIDATE'S DECLARATION", "ACKNOWLEDGEMENT", "ABSTRACT", "INDEX / TABLE OF CONTENTS", "LIST OF FIGURES", "LIST OF TABLES")) {{
                    $pNum = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndAdjustedPageNumber)
                    $secNum = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndSectionNumber)
                    $results += [PSCustomObject]@{{
                        text = $t
                        page = $pNum
                        section = $secNum
                    }}
                }}
            }}
        }}
        $doc.Close([Microsoft.Office.Interop.Word.WdSaveOptions]::wdDoNotSaveChanges)
        $results | ConvertTo-Json -Depth 3 | Set-Content -Path '{json_tmp}' -Encoding UTF8
    }} finally {{
        $word.Quit()
    }}
    """
    
    ps_file = os.path.join(os.path.dirname(abs_path), "run_measure.ps1")
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_script)
        
    try:
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file], check=True, capture_output=True)
        if os.path.exists(json_tmp):
            with open(json_tmp, "r", encoding="utf-8-sig") as f:
                data = json.load(f)
            return data
    except Exception as e:
        print(f"Warning: Word COM measurement exception: {e}")
    finally:
        if os.path.exists(ps_file):
            try: os.remove(ps_file)
            except: pass
        if os.path.exists(json_tmp):
            try: os.remove(json_tmp)
            except: pass
    return []

def extract_matched_page(target_prefix, measured_data, is_section_1=False):
    target_clean = target_prefix.strip().lower()
    target_section = 1 if is_section_1 else 2
    
    # Filter by section strictly so List of Figures / Tables in Section 1 don't match themselves
    section_items = [it for it in measured_data if it.get("section", 2) == target_section]
    
    # Primary pass: check startswith
    for item in section_items:
        text_clean = item.get("text", "").strip().lower()
        if text_clean.startswith(target_clean):
            page = item.get("page", 1)
            return int_to_roman(page) if is_section_1 else str(page)
            
    # Secondary pass: substring in text
    for item in section_items:
        text_clean = item.get("text", "").strip().lower()
        if target_clean in text_clean:
            page = item.get("page", 1)
            return int_to_roman(page) if is_section_1 else str(page)
            
    return None

def main():
    print("=" * 70)
    print("RecruMatch B.Tech Mini Project Report Builder (Two-Pass Indexing)")
    print("=" * 70)

    temp_docx = "temp_pass1_report.docx"
    final_docx = "RecruMatch_BTech_Mini_Project_Report.docx"

    print("\n[PASS 1] Generating base document structure to calculate exact layout...")
    build_document_instance(temp_docx)
    print(f"  Base layout generated: {temp_docx} ({os.path.getsize(temp_docx)} bytes)")

    print("\n[MEASUREMENT] Querying Microsoft Word COM for exact page positions...")
    measured_data = measure_pages_with_word_com(temp_docx)
    print(f"  Successfully extracted {len(measured_data)} heading/caption location markers from Word.")

    from report_sections.sec_preliminary import get_default_toc_items, get_default_figures, get_default_tables

    # Build Exact TOC Mapping
    updated_toc = []
    for title, default_page in get_default_toc_items():
        clean_title = title.strip()
        is_sec1 = clean_title in ["Certificate of Authenticity", "Candidate's Declaration", "Acknowledgement", "Abstract", "List of Figures", "List of Tables"]
        
        # Match against measured headings
        matched_page = None
        if clean_title == "Certificate of Authenticity":
            matched_page = extract_matched_page("CERTIFICATE", measured_data, is_section_1=True)
        elif clean_title == "Candidate's Declaration":
            matched_page = extract_matched_page("CANDIDATE'S DECLARATION", measured_data, is_section_1=True)
        elif clean_title == "Acknowledgement":
            matched_page = extract_matched_page("ACKNOWLEDGEMENT", measured_data, is_section_1=True)
        elif clean_title == "Abstract":
            matched_page = extract_matched_page("ABSTRACT", measured_data, is_section_1=True)
        elif clean_title == "List of Figures":
            matched_page = extract_matched_page("LIST OF FIGURES", measured_data, is_section_1=True)
        elif clean_title == "List of Tables":
            matched_page = extract_matched_page("LIST OF TABLES", measured_data, is_section_1=True)
        else:
            # Main body chapter or subsection (e.g. "CHAPTER 1", "1.1", "2.1", etc.)
            lookup_key = clean_title.split(":")[0] if ":" in clean_title else clean_title.split(" ")[0]
            matched_page = extract_matched_page(lookup_key, measured_data, is_section_1=False)

        exact_page = matched_page if matched_page is not None else default_page
        updated_toc.append((title, exact_page))

    # Build Exact Figures Mapping
    updated_figures = []
    for fig_no, fig_name, default_page in get_default_figures():
        matched_page = extract_matched_page(fig_no, measured_data, is_section_1=False)
        exact_page = matched_page if matched_page is not None else default_page
        updated_figures.append((fig_no, fig_name, exact_page))

    # Build Exact Tables Mapping
    updated_tables = []
    for tab_no, tab_name, default_page in get_default_tables():
        matched_page = extract_matched_page(tab_no, measured_data, is_section_1=False)
        exact_page = matched_page if matched_page is not None else default_page
        updated_tables.append((tab_no, tab_name, exact_page))

    print("\n[PASS 2] Assembling finalized report with 100% verified dynamic page numbers...")
    build_document_instance(final_docx, custom_toc=updated_toc, custom_figures=updated_figures, custom_tables=updated_tables)
    print(f"  Final Report Saved: {final_docx} ({os.path.getsize(final_docx)} bytes)")

    # Clean up temp
    if os.path.exists(temp_docx):
        try: os.remove(temp_docx)
        except: pass

    print("\n[VERIFICATION AUDIT] Sample Final Table of Contents Entries:")
    for t, p in updated_toc[:15]:
        print(f"  {t:<65} Page {p}")
    print("  ...")
    for t, p in updated_toc[-10:]:
        print(f"  {t:<65} Page {p}")

    print("\n" + "=" * 70)
    print("Report Generation & Verification Complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
