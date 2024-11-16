from playwright.sync_api import sync_playwright
import random
import string

# Function to generate a random 4-character username
def generate_random_username():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=4))

# Function to check if the username is available on Fortnite Tracker using Playwright
def check(users):
    with sync_playwright() as p:
        # Launch a browser in non-headless mode (visible)
        browser = p.chromium.launch(headless=False)  # Change headless to False
        page = browser.new_page()
        
        # Navigate to the Fortnite Tracker search page
        url = f'https://fortnitetracker.com/profile/search?q={users}'
        page.goto(url)
        
        # Wait for the page to load completely
        page.wait_for_selector("body")  # This waits for the body of the page to load

        # Get the HTML content of the page
        page_content = page.content()
        
        # Print the response for debugging purposes
        print(f"Response for {users}:")

        # Check for the string indicating the username is free
        if "We are unable to find your profile" in page_content:
            print(f"[+] Available {users}")
        else:
            print(f"[+] Taken {users}")

        # Close the browser after printing the content
        browser.close()

# Generate 10 random usernames for demonstration
random_usernames = [generate_random_username() for _ in range(500)]

# Check the availability of each username using Playwright
for username in random_usernames:
    check(username)