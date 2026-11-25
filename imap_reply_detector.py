
import os
import csv
import imaplib
import re

from email import message_from_bytes
from email.utils import parseaddr
from dotenv import load_dotenv

from client_config import EMAIL_HISTORY_CSV

load_dotenv()

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def load_history():

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


def save_history(records):

    if not records:
        return

    temporary_file = EMAIL_HISTORY_CSV.with_name(
        EMAIL_HISTORY_CSV.name + ".tmp"
    )

    with open(
        temporary_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=list(records[0].keys())
        )

        writer.writeheader()
        writer.writerows(records)

    temporary_file.replace(EMAIL_HISTORY_CSV)


def extract_message_ids(value):

    if not value:
        return []

    return [
        message_id.lower()
        for message_id in re.findall(r"<[^>]+>", value)
    ]


def check_recruiter_reply(mail, record):

    recruiter_email = record["recruiter_email"].strip().lower()
    original_message_id = record.get("message_id", "").strip().lower()

    if not original_message_id:
        return False

    try:
        status, data = mail.search(
            None,
            "FROM",
            f'"{recruiter_email}"'
        )

        if status != "OK":
            return False

        email_ids = data[0].split()

        for email_id in email_ids:

            status, response = mail.fetch(
                email_id,
                "(BODY.PEEK[HEADER.FIELDS "
                "(FROM MESSAGE-ID IN-REPLY-TO REFERENCES)])"
            )

            if status != "OK":
                continue

            for part in response:

                if not isinstance(part, tuple):
                    continue

                msg = message_from_bytes(part[1])

                sender = parseaddr(
                    msg.get("From", "")
                )[1].lower()

                if sender != recruiter_email:
                    continue

                in_reply_to = extract_message_ids(
                    msg.get("In-Reply-To", "")
                )

                references = extract_message_ids(
                    msg.get("References", "")
                )

                related_ids = in_reply_to + references

                if original_message_id in related_ids:
                    return True

        return False

    except Exception as error:
        print(
            f"Error checking {recruiter_email}: {error}"
        )
        return False


def detect_replies():

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("Gmail configuration missing.")
        return

    records = load_history()

    if not records:
        print("No email history records found.")
        return

    updated_count = 0

    try:
        print("\nConnecting to Gmail IMAP...")

        mail = imaplib.IMAP4_SSL(
            "imap.gmail.com",
            993
        )

        mail.login(
            GMAIL_ADDRESS,
            GMAIL_APP_PASSWORD
        )

        status, _ = mail.select("INBOX", readonly=True)

        if status != "OK":
            print("Could not open Gmail inbox.")
            mail.logout()
            return

        print("Gmail IMAP connection successful!")

        for record in records:

            if record.get("status") != "SENT":
                continue

            if record.get("replied", "").strip().lower() in [
                "yes", "true", "1"
            ]:
                continue

            if check_recruiter_reply(mail, record):

                record["replied"] = "Yes"
                updated_count += 1

                print(
                    "Recruiter replied:",
                    record["recruiter_email"]
                )

        mail.logout()

        if updated_count:
            save_history(records)

        print("\n===== REPLY DETECTION SUMMARY =====")
        print("New replies detected:", updated_count)
        print("Reply detection completed.")

    except Exception as error:
        print("\nIMAP connection failed:", error)


if __name__ == "__main__":
    detect_replies()
