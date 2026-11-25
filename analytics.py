
import csv
from html import escape
from datetime import datetime

from client_config import RECRUITERS_CSV, EMAIL_HISTORY_CSV, OUTPUT_DIR


DASHBOARD_FILE = OUTPUT_DIR / "analytics_dashboard.html"

TEST_DOMAINS = (
    "@example.com",
    "@example.org",
    "@example.net"
)


def load_csv(file_path):
    if not file_path.exists():
        return []

    with open(file_path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def is_test_contact(email):
    email = (email or "").strip().lower()
    return email.endswith(TEST_DOMAINS)


def calculate_analytics():

    recruiters = load_csv(RECRUITERS_CSV)
    history = load_csv(EMAIL_HISTORY_CSV)

    # Exclude fictional test contacts.
    real_recruiters = [
        r for r in recruiters
        if not is_test_contact(r.get("recruiter_email"))
    ]

    real_history = [
        r for r in history
        if not is_test_contact(r.get("recruiter_email"))
    ]

    sent_records = [
        r for r in real_history
        if r.get("status") == "SENT"
    ]

    initial_sent = len(sent_records)

    followups_sent = sum(
        int(r.get("followup_count") or 0)
        for r in sent_records
    )

    replies_received = sum(
        1 for r in sent_records
        if r.get("replied", "").strip().lower()
        in ["yes", "true", "1"]
    )

    response_rate = (
        replies_received / initial_sent * 100
        if initial_sent else 0
    )

    return {
        "total_recruiters": len(real_recruiters),
        "initial_sent": initial_sent,
        "followups_sent": followups_sent,
        "replies_received": replies_received,
        "response_rate": response_rate,
        "history": real_history
    }


def create_dashboard():

    data = calculate_analytics()

    total = data["total_recruiters"]
    sent = data["initial_sent"]
    followups = data["followups_sent"]
    replies = data["replies_received"]
    rate = data["response_rate"]

    maximum = max(sent, followups, replies, 1)

    def bar(value):
        width = value / maximum * 100
        return f"""
        <div class="bar-track">
            <div class="bar-fill" style="width:{width:.1f}%"></div>
        </div>
        """

    rows = ""

    for record in data["history"]:

        name = escape(record.get("recruiter_name", ""))
        email = escape(record.get("recruiter_email", ""))
        role = escape(record.get("role", ""))
        status = escape(record.get("status", ""))
        replied = escape(record.get("replied", "No"))

        rows += f"""
        <tr>
            <td>{name}</td>
            <td>{email}</td>
            <td>{role}</td>
            <td>{status}</td>
            <td>{replied}</td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
            <td colspan="5">No real outreach records available yet.</td>
        </tr>
        """

    generated_at = datetime.now().astimezone().strftime(
        "%d %b %Y, %I:%M %p"
    )

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>C2C Recruitment Analytics</title>

        <style>
            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 30px;
                font-family: Arial, sans-serif;
                background: #f1f5f9;
                color: #1e293b;
            }}

            .container {{
                max-width: 1100px;
                margin: auto;
            }}

            h1 {{
                color: #1e3a8a;
                margin-bottom: 8px;
            }}

            .subtitle {{
                color: #64748b;
                margin-bottom: 30px;
            }}

            .cards {{
                display: grid;
                grid-template-columns:
                    repeat(auto-fit, minmax(190px, 1fr));
                gap: 18px;
            }}

            .card {{
                background: white;
                padding: 24px;
                border-radius: 12px;
                box-shadow: 0 3px 12px #0000000c;
            }}

            .card h3 {{
                color: #64748b;
                font-size: 14px;
                margin: 0;
            }}

            .number {{
                font-size: 30px;
                font-weight: bold;
                margin-top: 14px;
                color: #2563eb;
            }}

            .section {{
                background: white;
                margin-top: 25px;
                padding: 24px;
                border-radius: 12px;
                overflow-x: auto;
            }}

            .chart-row {{
                display: grid;
                grid-template-columns: 130px 1fr 45px;
                align-items: center;
                gap: 12px;
                margin: 20px 0;
            }}

            .bar-track {{
                height: 13px;
                background: #e2e8f0;
                border-radius: 10px;
                overflow: hidden;
            }}

            .bar-fill {{
                height: 100%;
                background: #2563eb;
                border-radius: 10px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                min-width: 650px;
            }}

            th, td {{
                text-align: left;
                padding: 13px;
                border-bottom: 1px solid #e2e8f0;
                font-size: 14px;
            }}

            th {{
                background: #eff6ff;
                color: #1e40af;
            }}

            footer {{
                margin-top: 25px;
                color: #64748b;
                font-size: 13px;
            }}

            @media(max-width:600px) {{
                body {{ padding: 15px; }}
                .chart-row {{
                    grid-template-columns: 90px 1fr 30px;
                }}
            }}
        </style>
    </head>

    <body>
    <div class="container">

        <h1>C2C Recruitment Analytics</h1>
        <p class="subtitle">
            Recruitment and Outreach Automation Dashboard
        </p>

        <div class="cards">

            <div class="card">
                <h3>Total Recruiters</h3>
                <div class="number">{total}</div>
            </div>

            <div class="card">
                <h3>Initial Emails Sent</h3>
                <div class="number">{sent}</div>
            </div>

            <div class="card">
                <h3>Follow-ups Sent</h3>
                <div class="number">{followups}</div>
            </div>

            <div class="card">
                <h3>Replies Received</h3>
                <div class="number">{replies}</div>
            </div>

            <div class="card">
                <h3>Response Rate</h3>
                <div class="number">{rate:.1f}%</div>
            </div>

        </div>

        <div class="section">
            <h2>Outreach Overview</h2>

            <div class="chart-row">
                <span>Initial Emails</span>
                {bar(sent)}
                <strong>{sent}</strong>
            </div>

            <div class="chart-row">
                <span>Follow-ups</span>
                {bar(followups)}
                <strong>{followups}</strong>
            </div>

            <div class="chart-row">
                <span>Replies</span>
                {bar(replies)}
                <strong>{replies}</strong>
            </div>
        </div>

        <div class="section">
            <h2>Outreach History</h2>

            <table>
                <thead>
                    <tr>
                        <th>Recruiter</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Status</th>
                        <th>Replied</th>
                    </tr>
                </thead>

                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>

        <footer>
            Generated on: {generated_at}<br>
            Fictional example.com test contacts are excluded.
            Response rate = replies / initial emails sent.
        </footer>

    </div>
    </body>
    </html>
    """

    DASHBOARD_FILE.write_text(
        html_content,
        encoding="utf-8"
    )

    print("\n===== RECRUITMENT ANALYTICS =====")
    print("Total recruiters:", total)
    print("Initial emails sent:", sent)
    print("Follow-ups sent:", followups)
    print("Replies received:", replies)
    print(f"Response rate: {rate:.1f}%")

    print("\nDashboard generated successfully!")
    print("Saved to:", DASHBOARD_FILE)


if __name__ == "__main__":
    create_dashboard()
