
import json
from client_config import DATA_DIR

SAMPLE_FILE = DATA_DIR / "sample_posts.json"


def load_job_posts():
    try:
        with open(SAMPLE_FILE, "r", encoding="utf-8") as file:
            posts = json.load(file)

        print(f"Successfully loaded {len(posts)} sample posts.")
        return posts

    except FileNotFoundError:
        print("Sample posts file not found.")
        return []

    except json.JSONDecodeError:
        print("Invalid JSON format in sample posts.")
        return []


if __name__ == "__main__":
    posts = load_job_posts()

    for post in posts:
        print("\nRecruiter:", post["recruiter_name"])
        print("Location:", post["location"])
        print("Post:", post["post_text"])
