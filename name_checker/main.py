import os
import re
import random
import string
import time
import winsound
import concurrent
import proxy_manager
import requests
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


def generate_random_username(length):
    if length < 1:
        raise ValueError("Length must be at least 1")

    # Ensure at least one letter
    guaranteed_letter = random.choice(string.ascii_lowercase)

    # Generate the rest of the username
    remaining_length = length - 1
    remaining_characters = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=remaining_length))

    # Combine the guaranteed letter with the rest and shuffle
    username = guaranteed_letter + remaining_characters
    # Shuffle to randomize position
    username = ''.join(random.sample(username, len(username)))

    return username


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
                    # Expiry timestamp
                    "expires": int(parts[4]) if parts[4].isdigit() else None,
                    "httpOnly": False,               # Assume httpOnly is False unless specified
                    "sameSite": "None"               # Adjust if necessary
                })
    return cookies


def add_cookies(context, url_format):
    # Define the base directory for the cookies
    base_cookies_dir = os.path.join(
        os.path.dirname(__file__), "put_cookies_here")

    # Updated cookie configuration
    cookie_config = {
        "www.instagram.com": os.path.join(base_cookies_dir, "instagram", "cookies.txt"),
        "www.x.com": os.path.join(base_cookies_dir, "x", "cookies.txt"),
    }

    # Extract domain from the URL
    for site in cookie_config:
        if site in url_format:
            path = cookie_config[site]
            try:
                cookies = parse_cookies(path)
                context.add_cookies(cookies)
            except FileNotFoundError:
                print(f"[!] Cookies file not found for {site}: {
                      path}. Proceeding without cookies.")
            except Exception as e:
                print(f"[!] Error loading cookies for {site}: {e}")
            return


def generate_variations(word, character):
    variations = []
    for i in range(1, len(word)):  # Start from index 1 and stop before the last character
        variations.append(word[:i] + character + word[i:])
    return variations


def check_username(user, url_format, detection_type, current_index, total_count, proxy_pool=None, *additional_args):
    """
    Checks a username using Playwright without proxies, or Requests with proxies if available.

    Args:
        user (str): The username to check.
        url_format (str): The URL format string.
        detection_type (str): The detection string to identify available usernames.
        current_index (int): The current index in the list of usernames.
        total_count (int): The total number of usernames.
        proxy_pool (itertools.cycle, optional): The proxy pool for Requests.
        *additional_args: Additional arguments for the URL format.

    Returns:
        None
    """
    try:
        # Construct the URL
        url = url_format.format(user, *additional_args)

        if proxy_pool:
            # Use Requests with proxies
            proxy = next(proxy_pool)
            proxies = {
                "http": proxy,
                "https": proxy
            }

            response = requests.get(url, proxies=proxies, timeout=10)
            if response.status_code == 404:
                winsound.Beep(500, 500)
                print(f"[{current_index + 1}/{total_count}] [+] Available: {user} at {url}")
                with open("hits.txt", "a", encoding="utf-8") as f:
                    f.write(f"{user} | Available at {url}\n")
            elif detection_type in response.text:
                winsound.Beep(500, 500)
                print(f"[{current_index + 1}/{total_count}] [+] Available: {user} at {url}")
                with open("hits.txt", "a", encoding="utf-8") as f:
                    f.write(f"{user} | Available at {url}\n")
            else:
                print(f"[{current_index + 1}/{total_count}] [-] Taken: {user}")
        else:
            # Use Playwright without proxies
            print(f"Using Playwright for: {url}")
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(locale='en-US')

                add_cookies(context, url_format)  # Add cookies if necessary
                page = context.new_page()

                def should_block(request):
                    allowed_types = ['document', 'stylesheet', 'script', 'xhr', 'fetch']
                    return request.resource_type not in allowed_types

                page.route("**/*", lambda route, request:
                           route.abort() if should_block(request) else route.continue_())

                stealth_sync(page)

                # Navigate to the URL
                response = page.goto(url, timeout=60000, wait_until="load")
                page_content = page.content()

                if response.status == 404:
                    winsound.Beep(500, 500)
                    print(f"[{current_index + 1}/{total_count}] [+] Available: {user} at {url}")
                    with open("hits.txt", "a", encoding="utf-8") as f:
                        f.write(f"{user} | Available at {url}\n")
                elif detection_type in page_content:
                    winsound.Beep(500, 500)
                    print(f"[{current_index + 1}/{total_count}] [+] Available: {user} at {url}")
                    with open("hits.txt", "a", encoding="utf-8") as f:
                        f.write(f"{user} | Available at {url}\n")
                else:
                    print(f"[{current_index + 1}/{total_count}] [-] Taken: {user}")

                # Close the browser
                browser.close()

    except Exception as e:
        time.sleep(15)
        print(f"[!] Error checking {user}: {e}")

def select_url_format():
    # Define platforms, URL formats, and detection types in a dictionary
    platforms = {
        "steam": ("Steam", "https://steamcommunity.com/id/{}", "The specified profile could not be found"),
        "bluesky": ("Bluesky", "https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle={}.bsky.social", "Unable to resolve handle"),
        "vrchat": ("VRChat", "https://api.vrchat.cloud/api/1/auth/exists?username={}&displayName=", '"userExists":false'),
        "twitch": ("Twitch", "https://www.twitch.tv/{}", "Sorry. Unless you've got a time machine, that content is unavailable"),
        "snapchat": ("Snapchat", "https://www.snapchat.com/add/{}", "This content was not found"),
        "soundcloud": ("SoundCloud", "https://soundcloud.com/{}", "We can’t find that user."),
        "apple_music": ("Apple Music", "https://music.apple.com/profile/{}", "The page you're looking for can't be found."),
        "x": ("X (Feed it Cookies)", "https://x.com/{}", "This account doesn’t exist"),
        "steam_groups": ("Steam Groups", "https://steamcommunity.com/groups/{}", "No group could be retrieved for the given URL."),
        "youtube": ("YouTube (Feed it Cookies)", "https://www.youtube.com/@{}", "error?src=404&amp"),
        "instagram": ("Instagram (Feed it Cookies)", "https://www.instagram.com/{}", "Sorry, this page isn't available."),
        "minecraft": ("Minecraft", "https://api.mojang.com/users/profiles/minecraft/{}", "Couldn't find any profile with name"),
        "github": ("Github", "https://www.github.com/{}", "This is not the web page you are looking for"),
        "epic_games": ("Epic Games (Fortnite)", "https://fortnitetracker.com/profile/search?q=", "We are unable to find your profile"),
        "xbox": ("Xbox", "https://xboxgamertag.com/search/{}", "Gamertag doesn't exist"),
        "roblox": ("Roblox", "https://auth.roblox.com/v1/usernames/validate?request.username={}&request.birthday=2002-09-09", "Username is valid"),
        "pinterest": ("Pinterest", "https://www.pinterest.com/{}", '!--><template id="B:0"></template><!--/$--><!--$--><title></title'),
        "exit": ("Exit", None, None)
    }

    # Print menu dynamically
    print("\nChoose a platform to check usernames:")
    for key, (name, _, _) in platforms.items():
        print(f"[{key}] {name}")

    # Get user input
    choice = input(
        "\nEnter your choice (e.g., steam, bluesky, or exit to exit): ").lower()

    # Handle exit case
    if choice == "exit":
        print("Exiting...")
        exit(0)

    # Validate user input
    if choice in platforms:
        _, url_format, detection_type = platforms[choice]
        return url_format, detection_type
    else:
        print("Invalid choice. Please try again.")
        return select_url_format()  # Recursively ask again


# Read usernames from a file or generate random ones
def read_usernames_from_file(filename):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, "wordlists", filename)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            usernames = file.readlines()
            print(f"Usernames to check: {len(usernames)}")
        return [username.strip().lower() for username in usernames if len(username.strip()) >= 3 and re.match("^[A-Za-z]+$", username.strip())]
    except FileNotFoundError:
        print(f"File '{filename}' not found. Generating random usernames.")
        char_length = int(input("Enter length of characters: ").strip())
        return [generate_random_username(char_length) for _ in range(500)]


def process_username(index, username, total_count, variation, proxy_pool):
    if check_variations in ["yes", "y"]:
        # Generate and check dot variations
        variations = generate_variations(username, variation)
        for variation_applied in variations:
            check_username(variation_applied, url_format, detection_type,
                           index, total_count, proxy_pool, variation_applied)
    else:
        # Check only the original username
        check_username(username, url_format, detection_type,
                       index, total_count, proxy_pool, username)


if __name__ == "__main__":
    url_format, detection_type = select_url_format()
    print(f"Selected URL: {url_format}")
    print(f"Detection Type: {detection_type}")

    # File input and username loading
    file_name = input(
        "Enter the filename with usernames (e.g., usernames.txt): ").strip()
    usernames = read_usernames_from_file(file_name)

    # Concurrency setup
    max_workers = 2
    total_count = len(usernames)

    # Platform-specific variation handling
    variation = "."
    if "roblox" or "soundcloud" in url_format:
        variation = "_"

    check_variations = input(
        "Do you want to check with platform-supported variations? (y/n): ").strip().lower()
    if check_variations not in ["yes", "no", "y", "n"]:
        print("Invalid input. Please type 'yes' or 'no'.")
        exit()

    # Prepare indexed usernames
    indexed_usernames = [(index, user) for index, user in enumerate(usernames)]

    # Create a proxy pool
    proxy_pool = proxy_manager.create_proxy_pool()

    # Execute checks concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(
            lambda args: process_username(
                args[0], args[1], total_count, variation, proxy_pool),
            indexed_usernames
        )
