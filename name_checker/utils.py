import requests

def write_hits(user, url):
    with open("hits.txt", "a", encoding="utf-8") as f:
        f.write(f"{user} | Available at {url}\n")

def debug_requests_endpoint(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    print("Response JSON:", response.json() if response.headers.get('Content-Type') == 'application/json' else "No JSON")
    exit

import random

def make_headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",  # Always English
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    return headers

def generate_variations(word, character):
    variations = []
    for i in range(1, len(word)):  # Start from index 1 and stop before the last character
        variations.append(word[:i] + character + word[i:])
    return variations

def print_progress(current_index, total_count, message):
    percentage = (current_index + 1) / total_count * 100
    print(f"[{current_index + 1}/{total_count}] ({percentage:.2f}%) {message}")

def debug_page_content(page_content):
    with open("debug.html", "w", encoding="utf-8") as file:
        file.write(page_content)
    print("Page content saved to: debug.html")
    exit