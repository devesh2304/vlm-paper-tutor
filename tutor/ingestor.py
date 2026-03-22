import os
from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption

def ingest_paper(pdf_path: str) -> dict:
    """
    Parse a research paper PDF and extract:
    - Full text by section
    - Figure captions
    - Tables
    - Citations
    """
    print(f"Ingesting: {pdf_path}")

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = True

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options
            )
        }
    )

    result = converter.convert(pdf_path)
    doc = result.document

    # extract sections
    sections = []
    current_section = {"title": "Introduction", "content": ""}

    for item, _ in doc.iterate_items():
        item_type = type(item).__name__

        if item_type == "SectionHeaderItem":
            if current_section["content"].strip():
                sections.append(current_section)
            current_section = {
                "title": item.text if hasattr(item, 'text') else "Section",
                "content": ""
            }
        elif item_type == "TextItem":
            current_section["content"] += item.text + " "

    if current_section["content"].strip():
        sections.append(current_section)

    # extract figures
    figures = []
    for item, _ in doc.iterate_items():
        if type(item).__name__ == "PictureItem":
            caption = ""
            if hasattr(item, 'caption') and item.caption:
                caption = str(item.caption)
            figures.append({
                "caption": caption,
                "page": getattr(item, 'page_no', 0)
            })

    # extract tables
    tables = []
    for item, _ in doc.iterate_items():
        if type(item).__name__ == "TableItem":
            tables.append({
                "content": item.export_to_markdown() if hasattr(item, 'export_to_markdown') else "",
                "page": getattr(item, 'page_no', 0)
            })

    paper_data = {
        "path": pdf_path,
        "title": Path(pdf_path).stem,
        "sections": sections,
        "figures": figures,
        "tables": tables,
        "total_sections": len(sections),
        "total_figures": len(figures),
        "total_tables": len(tables)
    }

    print(f"Extracted: {len(sections)} sections, {len(figures)} figures, {len(tables)} tables")
    return paper_data