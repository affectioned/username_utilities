from playwright.sync_api import sync_playwright

def check_twitter_profile(username):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        page = context.new_page()
        url = f"https://x.com/{username}"

        try:
            # Navigate to the Twitter profile
            page.goto(url, timeout=60000)

            # Define selectors for profile and error elements
            profile_selector = "div[data-testid='primaryColumn']"
            error_selector = "div[data-testid='errorDetail']"

            # Check if the profile content is visible
            if page.locator(profile_selector).is_visible(timeout=10000):
                print(f"[+] Profile '{username}' exists.")
            # Check if the error message is visible
            elif page.locator(error_selector).is_visible(timeout=10000):
                print(f"[-] Profile '{username}' does not exist.")
            else:
                print(f"[!] Unable to determine status for '{username}'.")

        except Exception as e:
            print(f"[!] Error checking profile '{username}': {e}")

        browser.close()


if __name__ == "__main__":
    username = input("Enter the Twitter username to check: ").strip()
    check_twitter_profile(username)