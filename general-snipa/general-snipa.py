import os
import re
import random
import string
import concurrent.futures
from playwright.sync_api import sync_playwright


# Function to generate a random 8-character username
def generate_random_username():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))


# Function to parse cookies from a Netscape-formatted cookies.txt file
def parse_cookies(file_path):
    cookies = []
    with open(file_path, "r") as f:
        for line in f:
            # Skip comments and blank lines
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 7:
                cookies.append({
                    "name": parts[5],
                    "value": parts[6],
                    "domain": parts[0],
                    "path": parts[2],
                    "secure": parts[3].lower() == "true",
                    "httpOnly": False,  # Assume httpOnly is False unless specified
                    "sameSite": "None"  # Adjust if necessary
                })
    return cookies

# Main check function
def check(users, url_format, detection_type):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=False for visible browser
        context = browser.new_context()

        if "instagram.com" in url_format:
            # Instagram-specific behavior: Use cookies
            cookie_path = os.path.join("general-snipa", "instagram", "cookies.txt")
            cookies = parse_cookies(cookie_path)
            context.add_cookies(cookies)
        elif "youtube.com" in url_format:
            cookie_path = os.path.join("general-snipa", "youtube", "cookies.firefox-private.txt")
            cookies = parse_cookies(cookie_path)
            context.add_cookies(cookies)
        elif "x.com" in url_format:
            cookie_path = os.path.join("general-snipa", "youtube", "cookies.firefox-private.txt")
            cookies = parse_cookies(cookie_path)
            context.add_cookies(cookies)

        page = context.new_page()

        # Construct the URL
        url = url_format.format(users)

        try:
            # Navigate to the URL with extended wait conditions
            page.goto(url, timeout=60000, wait_until="domcontentloaded")

            # Check the page content
            page_content = page.content()

            if detection_type in page_content:
                print(f"[+] Available {users} at {url}")
                with open("hits.txt", "a", encoding="utf-8") as f:
                    f.write(f"{users} | Available at {url}\n")
            else:
                print(f"[-] Taken {users} at {url}")

        except Exception as e:
            print(f"[!] Error checking {users} at {url}: {e}")

        # Close the browser after use
        browser.close()


# Function to select URL format and detection type
def select_url_format():
    print("""
    Choose a platform to check usernames:
    [1] Steam
    [2] Bluesky
    [3] VRChat
    [4] Twitch
    [5] Snapchat
    [6] SoundCloud
    [7] Apple Music
    [8] X (FEED IT COOKIES)
    [9] Steam Groups
    [10] YouTube (FEED IT COOKIES)
    [11] Instagram (FEED IT COOKIES)
    [0] Exit
    """)
    
    choice = input("Enter your choice (1, 2, or 0 to exit): ")

    if choice == "1":
        return 'https://steamcommunity.com/id/{}', "The specified profile could not be found"
    elif choice == "2":
        return 'https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle={}.bsky.social', "Unable to resolve handle"
    elif choice == "3":
        return 'https://vrchat.com/api/1/auth/exists?username={}', '{"nameOk":true,"userExists":true}'
    elif choice == "4":
        return 'https://www.twitch.tv/{}', "Sorry. Unless you've got a time machine, that content is unavailable"
    elif choice == "5":
        return 'https://www.snapchat.com/add/{}', "This content was not found"
    elif choice == '6':
        return 'https://soundcloud.com/{}', "We can’t find that user."
    elif choice == '7':
        return 'https://music.apple.com/profile/{}', "The page you're looking for can't be found."
    elif choice == '8':
        return 'https://x.com/{}', "This account doesn’t exist"
    elif choice == '9':
        return 'https://steamcommunity.com/groups/{}', "No group could be retrieved for the given URL."
    elif choice == '10':
        return 'https://www.youtube.com/@{}', "error?src=404&amp"
    elif choice == '11':
        return 'https://www.instagram.com/{}', "Sorry, this page isn't available."
    elif choice == "0":
        print("Exiting...")
        exit(0)
    else:
        print("Invalid choice. Please try again.")
        return select_url_format()  # Recursively ask again


# Read usernames from a file or generate random ones
def read_usernames_from_file(filename):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            usernames = file.readlines()
            print(f"Usernames to check: {len(usernames)}" )
        return [username.strip().lower() for username in usernames if len(username.strip()) >= 3 and re.match("^[A-Za-z]+$", username.strip())]
    except FileNotFoundError:
        print(f"File '{filename}' not found. Generating random usernames.")
        return [generate_random_username() for _ in range(1)]


# Main script execution
if __name__ == "__main__":
    url_format, detection_type = select_url_format()
    file_name = input("Enter the filename with usernames (e.g., usernames.txt): ")
    usernames = read_usernames_from_file(file_name)

    max_workers = 2
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        executor.map(lambda user: check(user, url_format, detection_type), usernames)