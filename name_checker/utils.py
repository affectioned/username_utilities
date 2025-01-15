import requests
import os
from dotenv import load_dotenv

load_dotenv()

def write_hits(user, platform_name):
    """
    Writes the available username to a file and sends a styled webhook message.

    Args:
        user (str): The username that is available.
        platform_name (str): The name of the platform where the username is available.
    """
    with open("hits.txt", "a", encoding="utf-8") as f:
        f.write(f"{user} | Available at {platform_name}\n")

    send_webhook(
        title=f"Username Available: {user}",
        description=f"The username **{user}** is available on **{platform_name}**.",
        color=0x00FF00,  # Green color for success
        footer="*Note: Availability might also mean the username is banned or locked.*"
    )

def debug_requests_endpoint(
    url,
    method="GET",
    headers=None,
    cookies=None,
    params=None,
    data=None,
    json=None,
    exit_on_complete=True,
):
    """
    Debug a requests endpoint with improved error handling and logging.
    
    Args:
        url (str): The URL to request.
        method (str): HTTP method to use (GET, POST, PUT, DELETE, etc.).
        headers (dict): Additional headers for the request.
        params (dict): Query parameters for the request.
        data (dict): Form-encoded data for the request body.
        json (dict): JSON payload for the request body.
        exit_on_complete (bool): Whether to exit the program after debugging.
    """
    # Use utility function for headers if not provided
    headers = headers or make_headers()

    try:
        # Make the request
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            cookies=cookies,
            params=params,
            data=data,
            json=json,
        )
        
        # Log request details
        print(f"Request Method: {method}")
        print(f"URL: {response.url}")
        print(f"Headers: {response.request.headers}")
        if data:
            print(f"Form Data: {data}")
        if json:
            print(f"JSON Payload: {json}")

        # Log response details
        print("\nResponse Details:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Elapsed Time: {response.elapsed}")
        print("Response Text:")
        print(response.text)

        # Attempt to parse JSON if applicable
        if response.headers.get('Content-Type', '').startswith('application/json'):
            try:
                print("Response JSON:")
                print(response.json())
            except ValueError:
                print("Invalid JSON in response.")

        # Save response text to a file
        with open("response_output.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Response text saved to response_output.txt")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
    finally:
        if exit_on_complete:
            exit()

def make_headers():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0) Gecko/20100101 Firefox/134.0",
        "Upgrade-Insecure-Requests": "1",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,en-CH;q=0.8",
        'DNT': '1',  # Do Not Track
        'Sec-GPC': '1',  # Global Privacy Control
    }

    return headers

def generate_variations(word, url_format):
    # Platform-specific variation handling
    character = "."
    if "roblox" or "soundcloud" in url_format:
        character = "_"
    variations = []
    for i in range(1, len(word)):  # Start from index 1 and stop before the last character
        variations.append(word[:i] + character + word[i:])
    return variations

def validate_variation_choice():
    check_variations = input("Do you want to check with platform-supported variations? (y/n): ").strip().lower()
    if check_variations not in ["yes", "no", "y", "n"]:
        print("Invalid input. Please type 'yes' or 'no'.")
        exit()
    return check_variations in ["yes", "y"]

def print_progress(current_index, total_count, message):
    percentage = (current_index + 1) / total_count * 100
    print(f"[{current_index + 1}/{total_count}] ({percentage:.2f}%) {message}")

def debug_page_content(page_content):
    with open("debug.html", "w", encoding="utf-8") as file:
        file.write(page_content)
    print("Page content saved to: debug.html")
    exit

def send_webhook(title, description, color=0x7289DA, footer=None, platform_name=None, user=None):
    """
    Sends a styled webhook to a Discord channel.

    Args:
        title (str): The title of the embed.
        description (str): The description of the embed.
        color (int): The color of the embed (default is Discord blue).
        footer (str, optional): Text to display in the footer of the embed.
        platform_name (str, optional): The platform where the username is available.
        user (str, optional): The username being checked.
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("DISCORD_WEBHOOK_URL environment variable is not set.")

    embed = {
        "title": title,
        "description": description,
        "color": color,
        "fields": [
            {"name": "Platform", "value": platform_name, "inline": True},
            {"name": "Username", "value": user, "inline": True},
        ],
    }

    if footer:
        embed["footer"] = {"text": footer}

    payload = {
        "embeds": [embed]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, json=payload, headers=headers)
    if not response.ok:
        print(f"[!] Failed to send webhook: {response.status_code} - {response.text}")
    return response