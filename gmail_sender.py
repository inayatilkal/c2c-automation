
import os
import csv
from dotenv import load_dotenv
from client_config import RECRUITERS_CSV
import smtplib
import ssl
from datetime import datetime
from email.message import EmailMessage
from email.utils import make_msgid
from client_config import EMAIL_HISTORY_CSV

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def create_email(recruiter):

    recruiter_name = recruiter["recruiter_name"]
    role = recruiter["role"]

    subject = f"Interest in {role} - C2C Opportunity"

    body = f"""Hello {recruiter_name},

I came across your job posting for {role}.

I am interested in learning more about this opportunity.
Please let me know if you are accepting candidate profiles.

Thank you for your time.

Best regards,
{GMAIL_ADDRESS}
"""

    return subject, body


def preview_emails():

    if not RECRUITERS_CSV.exists():
        print("Recruiter CSV file not found.")
        return

    with open(
        RECRUITERS_CSV,
        "r",
        encoding="utf-8"
    ) as file:

        recruiters = list(csv.DictReader(file))

    if not recruiters:
        print("No recruiter records found.")
        return

    for recruiter in recruiters:

        subject, body = create_email(recruiter)

        print("\n" + "=" * 60)
        print("TO:", recruiter["recruiter_email"])
        print("FROM:", GMAIL_ADDRESS)
        print("SUBJECT:", subject)
        print("=" * 60)
        print(body)


HISTORY_FIELDS = [
    "recruiter_name",
    "recruiter_email",
    "role",
    "post_url",
    "candidate",
    "status",
    "timestamp",
    "subject",
    "message_id",
    "followup_count",
    "last_followup_at",
    "replied"
]


def already_sent(email, post_url):
    if not EMAIL_HISTORY_CSV.exists():
        return False

    with open(EMAIL_HISTORY_CSV, "r", newline="", encoding="utf-8") as file:
        records = csv.DictReader(file)

        for record in records:
            same_email = record["recruiter_email"].lower() == email.lower()
            same_post = record["post_url"] == post_url
            was_sent = record["status"] == "SENT"

            if same_email and same_post and was_sent:
                return True

    return False


def save_email_history(recruiter, candidate, status, subject, message_id):
    file_exists = EMAIL_HISTORY_CSV.exists()

    with open(EMAIL_HISTORY_CSV, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HISTORY_FIELDS)

        if not file_exists or EMAIL_HISTORY_CSV.stat().st_size == 0:
            writer.writeheader()

        writer.writerow({
            "recruiter_name": recruiter["recruiter_name"],
            "recruiter_email": recruiter["recruiter_email"],
            "role": recruiter["role"],
            "post_url": recruiter.get("post_url", ""),
            "candidate": candidate,
            "status": status,
            "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
            "subject": subject,
            "message_id": message_id,
            "followup_count": 0,
            "last_followup_at": "",
            "replied": "No"
        })


def send_emails():
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("Gmail configuration missing.")
        return

    with open(RECRUITERS_CSV, "r", newline="", encoding="utf-8") as file:
        recruiters = list(csv.DictReader(file))

    if not recruiters:
        print("No recruiter records found.")
        return

    candidate = "Your Name"  # Replace with your actual candidate name.

    print("\nEmail sending requires individual approval.")
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)

            for recruiter in recruiters:
                recipient = recruiter["recruiter_email"].strip()
                post_url = recruiter.get("post_url", "")

                # Block fictional test contacts.
                if recipient.lower().endswith(
                    ("@example.com", "@example.org", "@example.net")
                ):
                    print(f"Skipping fictional test address: {recipient}")
                    continue

                if already_sent(recipient, post_url):
                    print(f"Skipping duplicate: {recipient}")
                    continue

                subject, body = create_email(recruiter)

                message = EmailMessage()
                message["From"] = GMAIL_ADDRESS
                message["To"] = recipient
                message["Subject"] = subject
                message["Message-ID"] = make_msgid()
                message.set_content(body.replace("Your Name", candidate))

                print("\n" + "=" * 50)
                print("Recipient:", recipient)
                print("Subject:", subject)
                print(body)
                print("=" * 50)

                confirmation = input(
                    "Type SEND to send this email, or press Enter to skip: "
                )

                if confirmation.strip() != "SEND":
                    print("Email skipped.")
                    continue

                try:
                    server.send_message(message)

                    save_email_history(
                        recruiter,
                        candidate,
                        "SENT",
                        subject,
                        message["Message-ID"]
                    )

                    print("Email sent successfully!")

                except Exception as error:
                    print("Email sending failed:", error)

    except Exception as error:
        print("Gmail connection error:", error)



def test_smtp_connection():
    try:
        context = ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls(context=context)
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)

        print("\nGmail SMTP authentication successful!")

    except Exception as error:
        print("\nGmail SMTP authentication failed.")
        print("Error:", error)

if __name__ == "__main__":

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("Gmail configuration missing. Check your .env file.")
    else:
        print("Gmail configuration loaded successfully.")
        preview_emails()
        test_smtp_connection()
        choice = input("\nDo you want to start email sending? (yes/no): ")

        if choice.lower() == "yes":
            send_emails()
