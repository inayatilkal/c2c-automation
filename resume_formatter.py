from lock_util import file_lock
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from client_config import OUTPUT_DIR


INPUT_FILE = OUTPUT_DIR / "customized_resume.txt"
OUTPUT_FILE = OUTPUT_DIR / "customized_resume.docx"


def generate_docx():

    if not INPUT_FILE.exists():
        print("Customized resume text file not found.")
        return

    resume_text = INPUT_FILE.read_text(encoding="utf-8")

    if not resume_text.strip():
        print("Resume file is empty.")
        return

    doc = Document()

    # Page settings
    section = doc.sections[0]
    section.top_margin = Inches(0.55)
    section.bottom_margin = Inches(0.55)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

    # Default font
    styles = doc.styles
    styles["Normal"].font.name = "Arial"
    styles["Normal"].font.size = Pt(9)
    styles["Normal"].paragraph_format.space_after = Pt(3)

    lines = resume_text.splitlines()

    headings = [
        "SUMMARY",
        "EDUCATION",
        "SKILLS",
        "PROJECTS",
        "CERTIFICATIONS",
        "ACHIEVEMENTS",
        "EXPERIENCE"
    ]

    for index, original_line in enumerate(lines):

        line = original_line.strip()

        if not line:
            continue

        # Candidate name
        if index == 0:
            paragraph = doc.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

            run = paragraph.add_run(line)
            run.bold = True
            run.font.name = "Arial"
            run.font.size = Pt(19)
            run.font.color.rgb = RGBColor(31, 78, 121)
            continue

        # Contact details
        if index == 1:
            paragraph = doc.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

            run = paragraph.add_run(line)
            run.font.size = Pt(8)
            continue

        # Section headings
        if line.upper().rstrip(":") in headings:
            paragraph = doc.add_paragraph()

            run = paragraph.add_run(line.upper())
            run.bold = True
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(31, 78, 121)

            paragraph.paragraph_format.space_before = Pt(8)
            paragraph.paragraph_format.space_after = Pt(4)
            continue

        # Bullet points
        if line.startswith(("*", "-", "•")):
            paragraph = doc.add_paragraph(style="List Bullet")
            paragraph.paragraph_format.space_after = Pt(2)

            text = line.lstrip("*-• ").strip()
            paragraph.add_run(text)
            continue

        # Regular content
        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(3)

        # Project titles and education lines
        if "|" in line and len(line) < 180:
            run = paragraph.add_run(line)
            run.bold = True
        else:
            paragraph.add_run(line)

    # Save document
        # Save document
    with file_lock():
        doc.save(OUTPUT_FILE)

    print("\nDOCX resume generated successfully!")
    print("Saved location:", OUTPUT_FILE)


if __name__ == "__main__":
    generate_docx()
