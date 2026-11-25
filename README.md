# Recruitment and Outreach Automation System

An AI-assisted, CLI-based recruitment and outreach automation system designed to help candidates identify US-based C2C (Corp-to-Corp) job opportunities, extract recruiter contact information, customize resumes for job descriptions, and manage email outreach.

## Project Overview

The system brings together job-post filtering, recruiter information extraction, AI-powered resume customization, email outreach, follow-up management, reply detection, and analytics in one Python application.

It currently supports sample job-post data for testing. Live LinkedIn scraping and persistent browser-session support are not yet implemented.

## Key Features

- **LinkedIn login:** Opens LinkedIn through Playwright for manual login.
- **Job-post processing:** Loads sample job-post data.
- **Job filtering:** Filters Java Developer opportunities by employment type, US location, and post age.
- **Recruiter extraction:** Extracts recruiter email addresses and saves details to CSV.
- **AI resume customization:** Uses Google Gemini to tailor resume content to a job description.
- **DOCX generation:** Creates an ATS-friendly Word resume.
- **Email outreach:** Prepares personalized emails and supports SMTP delivery with manual confirmation.
- **Follow-ups:** Identifies eligible follow-ups and supports threaded email replies.
- **Reply detection:** Checks Gmail inbox replies using IMAP.
- **Analytics:** Generates an HTML dashboard with outreach statistics.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming language | Python 3.12 |
| Browser automation | Playwright |
| AI integration | Google Gemini API |
| Data processing | Pandas, JSON, CSV |
| Resume processing | pypdf, python-docx |
| Email services | Gmail SMTP and IMAP |
| Configuration | python-dotenv |
| Dashboard | HTML, CSS, JavaScript |

## Project Structure

```text
c2c-automation/
├── clients/
├── data/
│   ├── sample_posts.json
│   ├── job_description.txt
│   ├── recruiters.csv
│   └── email_sent_history.csv
├── output/
├── scratch/
├── main.py
├── client_config.py
├── linkedin_login.py
├── linkedin_scraper.py
├── job_filter.py
├── recruiter_extractor.py
├── resume_customizer.py
├── resume_formatter.py
├── gmail_sender.py
├── followup_sender.py
├── imap_reply_detector.py
├── analytics.py
├── lock_util.py
├── requirements.txt
├── .env
└── README.md
```

Generated files, credentials, and temporary files should not be committed to version control.

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd c2c-automation
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Install Playwright Chromium

```bash
python -m playwright install chromium
```

## Environment Configuration

Create a `.env` file in the project root.

Add the following variables with your own credentials:

```env
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
GEMINI_API_KEY=your_gemini_api_key
```

Use a Gmail App Password where required. Never commit `.env` or expose API keys and passwords.

## Usage

Run the main application:

```bash
python main.py
```

### CLI Menu

| Option | Function |
|---|---|
| 1 | LinkedIn Login |
| 2 | Search Job Posts |
| 3 | Filter Job Posts |
| 4 | Extract Recruiter Details |
| 5 | Customize Resume |
| 6 | Send Emails |
| 7 | Send Follow-up Emails |
| 8 | Check Email Replies |
| 9 | View Analytics |
| 0 | Exit |

### Resume Customization

1. Select option 5.
2. Provide the path to your PDF resume.
3. Ensure `data/job_description.txt` contains the target job description.
4. The application uses Gemini to generate tailored resume content.
5. The generated text and DOCX are saved in `output/`.

### Email Outreach

Configure Gmail credentials in `.env`. Review each generated message and use the application's confirmation prompt before sending. Sample addresses are intentionally blocked.

### Analytics

Select option 9 to generate:

```text
output/analytics_dashboard.html
```

Open the HTML file in a browser to view outreach statistics.

## Data Storage

- `data/sample_posts.json`: Sample job-post records.
- `data/recruiters.csv`: Extracted recruiter information.
- `data/email_sent_history.csv`: Email outreach and follow-up history.
- `data/job_description.txt`: Job description used for resume customization.
- `output/`: Generated resumes and analytics dashboard.
- `scratch/`: Temporary processing files.

## Testing

Verify installed dependencies:

```bash
python -m pip check
```

Test module imports:

```bash
python -c "import resume_customizer, resume_formatter, gmail_sender, followup_sender, imap_reply_detector, analytics; print('Module imports successful')"
```

Test file locking:

```python
from lock_util import file_lock

with file_lock():
    print("File lock acquired successfully")
```

## Current Limitations

- Job-post search currently uses local sample JSON data rather than live LinkedIn search results.
- LinkedIn login is a manual diagnostic workflow; persistent session storage is not implemented.
- Resume customization creates new text and DOCX files; it does not preserve the original PDF formatting or generate a final PDF.
- Multi-candidate processing is not fully implemented.
- Email delivery and reply detection require valid Gmail configuration and real recruiter data.
- The current reply detector checks inbox messages and uses email threading headers for matching.

LinkedIn automation must comply with LinkedIn's terms and applicable usage restrictions. Review all recruiter details and messages before outreach.

## Future Improvements

- Implement compliant live job-source integrations.
- Add persistent browser-session management where permitted.
- Improve resume formatting and PDF export.
- Implement multi-candidate configuration and processing.
- Improve recruiter deduplication and historical data management.
- Add robust error handling, automated tests, and reporting.

## Security

- Keep API keys and email credentials in environment variables.
- Never commit `.env`, credentials, or private candidate information.
- Review generated emails before sending.
- Use legitimate recruiter contact information and comply with applicable platform policies.

## Author

Developed as a Python-based recruitment and outreach automation project.
