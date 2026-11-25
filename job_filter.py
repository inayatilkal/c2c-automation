
from client_config import POST_AGE_HOURS

ROLE_KEYWORDS = ["java developer"]

EMPLOYMENT_KEYWORDS = [
    "c2c",
    "corp to corp",
    "bench",
    "w2",
    "full-time",
    "full time",
    "hotlist"
]

def filter_job_posts(posts):
    filtered_posts = []

    for post in posts:
        text = post["post_text"].lower()
        location = post["location"].lower()

        is_java_role = any(
            keyword in text for keyword in ROLE_KEYWORDS
        )

        is_employment_type = any(
            keyword in text for keyword in EMPLOYMENT_KEYWORDS
        )

        is_us_location = (
            location in ["united states", "usa", "us"]
        )

        is_recent = (
            0 <= post["posted_hours_ago"] <= POST_AGE_HOURS
        )

        if (
            is_java_role
            and is_employment_type
            and is_us_location
            and is_recent
        ):
            filtered_posts.append(post)

    print(f"\nMatching job posts: {len(filtered_posts)}")
    return filtered_posts


if __name__ == "__main__":
    from linkedin_scraper import load_job_posts

    posts = load_job_posts()
    results = filter_job_posts(posts)

    for post in results:
        print("\nRecruiter:", post["recruiter_name"])
        print("Post:", post["post_text"])
