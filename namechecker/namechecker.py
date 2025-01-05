import os
import re
import random
import string
import time
import winsound
import concurrent.futures
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


# Function to generate a random 8-character username
def generate_random_username(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def parse_cookies(file_path):
    cookies = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Skip comments and blank lines
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 7:
                cookies.append({
                    "name": parts[5],                # Cookie name
                    "value": parts[6],               # Cookie value
                    "domain": parts[0],              # Domain
                    "path": parts[2],                # Path
                    "secure": parts[3].lower() == "true",  # Secure flag
                    "expires": int(parts[4]) if parts[4].isdigit() else None,  # Expiry timestamp
                    "httpOnly": False,               # Assume httpOnly is False unless specified
                    "sameSite": "None"               # Adjust if necessary
                })
    return cookies

def add_cookies(context, url_format):
    # Define cookie configurations for supported websites
    cookie_config = {
        "www.instagram.com": os.path.join(os.path.dirname(__file__), "instagram", "cookies.txt"),
        "www.x.com": os.path.join(os.path.dirname(__file__), "x", "cookies.txt"),
    }

    for site, path in cookie_config.items():
        if site in url_format:
            try:
                cookies = parse_cookies(path)
                context.add_cookies(cookies)
            except FileNotFoundError:
                print(f"[!] Cookies file not found for {site}: {path}. Proceeding without cookies.")
            except Exception as e:
                print(f"[!] Error loading cookies for {site}: {e}")
            break

def create_context_with_language(browser, language="en-US"):
    return browser.new_context(
        extra_http_headers={"Accept-Language": language}
    )

def generate_dot_variations(word):
    variations = []
    for i in range(1, len(word)):  # Start from index 1 and stop before the last character
        variations.append(word[:i] + '.' + word[i:])
    return variations

def check(user, url_format, detection_type, current_index, total_count, *additional_args):
    with sync_playwright() as p:
        # Set headless=False for visible browser
        browser = p.chromium.launch(headless=True)
        context = create_context_with_language(browser, language="en-US")

        # print(url_format)

        add_cookies(context, url_format)

        page = context.new_page()

        # Optional: Use stealth to mimic real browser behavior
        stealth_sync(page)

        try:
            url = url_format.format(user, *additional_args)
            page.goto(url, timeout=60000, wait_until="load")
            page_content = page.content()

            if detection_type in page_content:
                winsound.Beep(100, 100)
                print(f"[{current_index + 1}/{total_count} | {((current_index + 1) / total_count) * 100:.2f}%] [+] Available: {user} at {url}")
                with open("hits.txt", "a", encoding="utf-8") as f:
                    f.write(f"{user} | Available at {url}\n")
            else:
                print(f"[{current_index + 1}/{total_count} | {((current_index + 1) / total_count) * 100:.2f}%] [-] Taken: {user}")

        except Exception as e:
            time.sleep(15)
            print(f"[!] Error checking {user}: {e}")

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
    [12] Minecraft
    [13] Github
    [14] Epic Games (Fortnite)
    [15] Xbox
    [16] Roblox
    [0] Exit
    """)

    choice = input("Enter your choice (1, 2, or 0 to exit): ")

    if choice == "1":
        return 'https://steamcommunity.com/id/{}', "The specified profile could not be found"
    elif choice == "2":
        return 'https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle={}.bsky.social', "Unable to resolve handle"
    elif choice == "3":
        return 'https://api.vrchat.cloud/api/1/auth/exists?username={}&displayName={}', '"userExists":false'
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
    elif choice == '12':
        return 'https://api.mojang.com/users/profiles/minecraft/{}', "Couldn't find any profile with name"
    elif choice == '13':
        return 'https://www.github.com/{}', "This is not the web page you are looking for"
    elif choice == '14':
        return 'https://fortnitetracker.com/profile/search?q={}', "We are unable to find your profile"
    elif choice == '15':
        return 'https://xboxgamertag.com/search/{}', "Gamertag doesn't exist"
    elif choice == '16':
        return 'https://auth.roblox.com/v1/usernames/validate?request.username={}&request.birthday=2002-09-09', "Username is valid"
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
            print(f"Usernames to check: {len(usernames)}")
        return [username.strip().lower() for username in usernames if len(username.strip()) >= 3 and re.match("^[A-Za-z]+$", username.strip())]
    except FileNotFoundError:
        print(f"File '{filename}' not found. Generating random usernames.")
        return [generate_random_username(8) for _ in range(1)]


# Main script execution
if __name__ == "__main__":
    url_format, detection_type = select_url_format()
    file_name = input(
        "Enter the filename with usernames (e.g., usernames.txt): ")
    usernames = read_usernames_from_file(file_name)

    max_workers = 2

    total_count = len(usernames)

    # Ask the user if they want to check with dot variations
    check_variations = input("Do you want to check with dot variations? (yes/no): ").strip().lower()
    if check_variations not in ["yes", "no", "y", "n"]:
        print("Invalid input. Please type 'yes' or 'no'.")
        exit()

    # Function to handle checking usernames with or without variations
    def process_username(index, username, total_count):
        if check_variations in ["yes", "y"]:
            # Generate and check dot variations
            variations = generate_dot_variations(username)
            for variation in variations:
                check(variation, url_format, detection_type, index, total_count, variation)
        else:
            # Check only the original username
            check(username, url_format, detection_type, index, total_count, username)

    # Prepare the data with indexes
    indexed_usernames = [(index, user) for index, user in enumerate(usernames)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(
            lambda args: process_username(args[0], args[1], total_count),
            indexed_usernames
        )

