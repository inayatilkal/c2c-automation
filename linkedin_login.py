
from playwright.sync_api import sync_playwright


def linkedin_login():
    print("\n===== LINKEDIN LOGIN =====")

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            print("Opening LinkedIn...")
            page.goto(
                "https://www.linkedin.com/login",
                wait_until="domcontentloaded"
            )

            print("\nLog in manually in the opened browser.")
            print("Wait until your LinkedIn home page is visible.")

            input("\nAfter login, press Enter here...")

            page.wait_for_timeout(3000)

            print("\n===== LOGIN DIAGNOSTICS =====")
            print("Current URL:", page.url)
            print("Page title:", page.title())

            if (
                "linkedin.com" in page.url
                and "/login" not in page.url
                and "/checkpoint" not in page.url
            ):
                print("\nLogin page has been left.")
            else:
                print("\nBrowser is still on a login or verification page.")

            input("\nPress Enter to close browser...")
            browser.close()

    except Exception as error:
        print("\nLinkedIn error:", error)


if __name__ == "__main__":
    linkedin_login()
