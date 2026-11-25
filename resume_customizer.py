from lock_util import file_lock
import os
from pathlib import Path
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai
from client_config import OUTPUT_DIR, DATA_DIR

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def extract_resume_text(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text if text.strip() else None

    except Exception as error:
        print("PDF extraction error:", error)
        return None


def customize_resume():

    print("\n===== AI RESUME CUSTOMIZATION =====")

    if not API_KEY:
        print("Gemini API key missing. Check your .env file.")
        return

    pdf_path = input("Enter your PDF resume path: ").strip().strip('"')
    path = Path(pdf_path)

    if not path.exists() or path.suffix.lower() != ".pdf":
        print("Invalid PDF file.")
        return

    resume_text = extract_resume_text(path)

    if not resume_text:
        print("Could not extract resume text.")
        return

    job_description_file = DATA_DIR / "job_description.txt"

    if not job_description_file.exists():
        print("Job description file not found:", job_description_file)
        return

    job_description = job_description_file.read_text(
        encoding="utf-8"
        ).strip()

    if not job_description:
        print("Job description file is empty.")
        return

    print("\nJob description loaded successfully!")

    prompt = f"""
You are an expert technical resume writer.

Customize the candidate's resume for the supplied job description.

STRICT RULES:
1. Never invent qualifications, experience, skills, or achievements.
2. Preserve factual details and metrics from the original resume.
3. Do not claim professional experience if the candidate is a student.
4. Highlight relevant Java, DSA, OOP and software development skills
   only when supported by the original resume.
5. Do not add unsupported C2C employment experience.
6. Use clear, professional, ATS-friendly formatting.
7. Return the complete tailored resume as plain text.

ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    try:
        client = genai.Client(api_key=API_KEY)

        print("\nContacting Gemini AI...")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        customized_text = response.text

        if not customized_text:
            print("Gemini returned an empty response.")
            return

        output_file = OUTPUT_DIR / "customized_resume.txt"

        with file_lock():
            output_file.write_text(
            customized_text,
            encoding="utf-8"
        )

        print("\nResume customized successfully!")
        print("Saved to:", output_file)

        print("\n===== CUSTOMIZED RESUME PREVIEW =====")
        print(customized_text[:2000])

    except Exception as error:
        print("\nGemini customization failed:", error)


if __name__ == "__main__":
    customize_resume()
