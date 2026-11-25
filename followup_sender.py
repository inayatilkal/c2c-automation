
import os
import csv
import ssl
import smtplib

from datetime import datetime, timedelta
from email.message import EmailMessage
from email.utils import make_msgid
from dotenv import load_dotenv

from client_config import EMAIL_HISTORY_CSV, FOLLOWUP_DAYS

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def load_email_history():
    if not EMAIL_HISTORY_CSV.exists():
        print("Email history file not found.")
        return []

    with open(
        EMAIL_HISTORY_CSV,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        return list(csv.DictReader(file))


def is_eligible_for_followup(record):

    # Only consider successfully sent initial emails.
    if record.get("status") != "SENT":
        return False

    # Skip recruiters who have replied.
    if record.get("replied", "").strip().lower() in [
        "yes", "true", "1"
    ]:
        return False

    # Send only one follow-up.
    if int(record.get("followup_count") or 0) >= 1:
        return False

    # Original email must have a Message-ID for threading.
    if not record.get("message_id", "").strip():
        return False

    timestamp = record.get("timestamp", "").strip()

    if not timestamp:
        return False

    try:
        sent_at = datetime.fromisoformat(timestamp)

        if sent_at.tzinfo is None:
            sent_at = sent_at.astimezone()

        current_time = datetime.now().astimezone()

        return current_time - sent_at >= timedelta(days=FOLLOWUP_DAYS)

    except (ValueError, TypeError):
        print("Invalid timestamp for:", record.get("recruiter_email"))
        return False


def create_followup_email(record):

    recruiter_name = record.get("recruiter_name", "Recruiter")
    candidate = record.get("candidate", "Candidate")
    original_subject = record.get("subject", "Job Opportunity")

    message = EmailMessage()

    message["From"] = GMAIL_ADDRESS
    message["To"] = record["recruiter_email"]
    message["Subject"] = (
        original_subject
        if original_subject.lower().startswith("re:")
        else f"Re: {original_subject}"
    )

    # Keep the follow-up in the original email thread.
    original_message_id = record["message_id"].strip()

    message["In-Reply-To"] = original_message_id
    message["References"] = original_message_id
    message["Message-ID"] = make_msgid()

    body = f"""Hello {recruiter_name},

I wanted to follow up on my previous email regarding the
{record.get('role', 'job')} opportunity.

I remain interested in this position. Please let me know
if you are currently accepting candidate profiles.

Thank you for your time.

Best regards,
{candidate}
"""

    message.set_content(body)

    return message


def update_history(records):

    temporary_file = EMAIL_HISTORY_CSV.with_name(
        EMAIL_HISTORY_CSV.name + ".tmp"
    )

    fieldnames = list(records[0].keys()) if records else []

    with open(
        temporary_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        writer.writeheader()
        writer.writerows(records)

    temporary_file.replace(EMAIL_HISTORY_CSV)


def send_followups():

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("Gmail configuration missing. Check your .env file.")
        return

    records = load_email_history()

    if not records:
        print("No email history records found.")
        return

    eligible_records = [
        record for record in records
        if is_eligible_for_followup(record)
    ]

    if not eligible_records:
        print(
            f"No follow-ups currently due. "
            f"Follow-up period: {FOLLOWUP_DAYS} days."
        )
        return

    print("\nEligible follow-ups:", len(eligible_records))

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls(context=context)
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)

            for record in eligible_records:

                recipient = record["recruiter_email"].strip()

                # Block fictional sample addresses.
                if recipient.lower().endswith(
                    ("@example.com", "@example.org", "@example.net")
                ):
                    print("Skipping fictional address:", recipient)
                    continue

                message = create_followup_email(record)

                print("\n" + "=" * 50)
                print("TO:", recipient)
                print("SUBJECT:", message["Subject"])
                print(message.get_content())
                print("=" * 50)

                confirmation = input(
                    "Type SEND to send this follow-up, "
                    "or press Enter to skip: "
                )

                if confirmation.strip() != "SEND":
                    print("Follow-up skipped.")
                    continue

                try:
                    server.send_message(message)

                    # Update history only after successful sending.
                    record["followup_count"] = str(
                        int(record.get("followup_count") or 0) + 1
                    )

                    record["last_followup_at"] = (
                        datetime.now().astimezone().isoformat(
                            timespec="seconds"
                        )
                    )

                    update_history(records)

                    print("Follow-up sent successfully!")

                except Exception as error:
                    print("Follow-up sending failed:", error)

    except Exception as error:
        print("Gmail connection error:", error)


if __name__ == "__main__":
    send_followups()
