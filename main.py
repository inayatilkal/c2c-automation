import email
from job_filter import filter_job_posts
from gmail_sender import send_emails
from rich.console import Console
from rich.panel import Panel
from resume_customizer import customize_resume
from resume_formatter import generate_docx
from client_config import OUTPUT_DIR
from followup_sender import send_followups
from imap_reply_detector import detect_replies
from analytics import create_dashboard
from linkedin_scraper import load_job_posts
from recruiter_extractor import extract_email
from linkedin_login import linkedin_login
from recruiter_extractor import (extract_recruiter_details, save_recruiters)

console = Console()

def show_menu():
    console.print(
        Panel(
            "[bold cyan]C2C RECRUITMENT AND OUTREACH AUTOMATION SYSTEM[/bold cyan]",
            border_style="blue"
        )
    )

    console.print("\n[bold yellow]MAIN MENU[/bold yellow]")
    console.print("1. LinkedIn Login")
    console.print("2. Search Job Posts")
    console.print("3. Filter Job Posts")
    console.print("4. Extract Recruiter Details")
    console.print("5. Customize Resume")
    console.print("6. Send Emails")
    console.print("7. Send Follow-up Emails")
    console.print("8. Check Email Replies")
    console.print("9. View Analytics")
    console.print("0. Exit")

def main():
    while True:
        show_menu()
        choice = console.input("\n[bold green]Enter your choice: [/bold green]")

        if choice == "0":
            console.print("[yellow]Exiting application...[/yellow]")
            break

        elif choice == "1":
            linkedin_login()

        elif choice == "2":
            print("\n===== SEARCH JOB POSTS =====")
            posts = load_job_posts()

            if not posts:
                print("No job posts found.")
            else:
                print("\n===== AVAILABLE JOB POSTS =====")

            for index, post in enumerate(posts, start=1):
                print("\n" + "=" * 60)
                print(f"Job Post {index}")
                print("=" * 60)

                print("Recruiter:", post.get("recruiter_name", "Unknown"))
                print("Location:", post.get("location", "Unknown"))
                print("Posted:", post.get("posted_hours_ago", "Unknown"), "hours ago")
                print("Post:", post.get("post_text", ""))
                email = post.get("recruiter_email") or extract_email(post.get("post_text", ""))
                print("Email:", email or "Not available")

        elif choice == "3":
            print("\n===== FILTER JOB POSTS =====")
            posts = load_job_posts()
            filtered_posts = filter_job_posts(posts)

            if filtered_posts:
                for post in filtered_posts:
                    print("\nRecruiter:", post["recruiter_name"])
                    print("Location:", post["location"])
                    print("Posted:", post["posted_hours_ago"], "hours ago")
                    print("Post:", post["post_text"])
            else:
                print("No matching job posts found.")

        elif choice == "4":
            print("\n===== EXTRACT RECRUITER DETAILS =====")
            posts = load_job_posts()
            filtered_posts = filter_job_posts(posts)
            recruiters = extract_recruiter_details(filtered_posts)

            save_recruiters(recruiters)

            for recruiter in recruiters:
                print("\nRecruiter:", recruiter["recruiter_name"])
                print("Email:", recruiter["recruiter_email"])

        elif choice == "5":
            print("\n===== RESUME CUSTOMIZATION WORKFLOW =====")
            result = customize_resume()

            if result:
                generate_docx()
            else:
                print("Resume customization was not completed. DOCX generation skipped.")

        elif choice == "6":
            send_emails()

        elif choice == "7":
            send_followups()

        elif choice == "8":
            detect_replies()
        
        elif choice == "9":
            create_dashboard()

        else:
            console.print("[red]Invalid choice. Try again.[/red]")

if __name__ == "__main__":
    main()
