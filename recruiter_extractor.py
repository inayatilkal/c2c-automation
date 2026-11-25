
import re
import csv

from client_config import RECRUITERS_CSV


def extract_email(text):
    """Extract email addresses from post text."""

    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    emails = re.findall(pattern, text)

    return emails[0] if emails else ""


def extract_recruiter_details(posts):
    """Extract recruiter details from filtered job posts."""

    recruiters = []

    for post in posts:
        email = post.get("recruiter_email") or extract_email(
            post.get("post_text", "")
        )

        if not email:
            print(
                f"No email found for {post['recruiter_name']}"
            )
            continue

        recruiter = {
            "recruiter_name": post["recruiter_name"],
            "recruiter_email": email,
            "role": "Java Developer",
            "post_url": post["post_url"],
            "job_description": post["post_text"],
            "email_sent_status": "Pending",
            "timestamp": "",
        }

        recruiters.append(recruiter)

    return recruiters


def save_recruiters(recruiters):
    """Save recruiter details into CSV."""

    fieldnames = [
        "recruiter_name",
        "recruiter_email",
        "role",
        "post_url",
        "job_description",
        "email_sent_status",
        "timestamp",
    ]

    with open(
        RECRUITERS_CSV,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(recruiters)

    print(f"\nSaved {len(recruiters)} recruiters.")
    print(f"CSV location: {RECRUITERS_CSV}")


if __name__ == "__main__":
    from linkedin_scraper import load_job_posts
    from job_filter import filter_job_posts

    posts = load_job_posts()
    filtered_posts = filter_job_posts(posts)

    recruiters = extract_recruiter_details(filtered_posts)

    save_recruiters(recruiters)

    for recruiter in recruiters:
        print("\nRecruiter:", recruiter["recruiter_name"])
        print("Email:", recruiter["recruiter_email"])
