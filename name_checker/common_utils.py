from profanity_check import predict
import requests
import string
import random
import os
import re

def filter_vulgar_words(words):
    filtered_words = []
    for word in words:
        if not predict([word])[0]:
            filtered_words.append(word)
    return filtered_words

def generate_random_username(length):
    if length < 1:
        raise ValueError("Length must be at least 1")

    # Ensure the first character is a letter
    first_letter = random.choice(string.ascii_lowercase)

    # Generate the rest of the username
    remaining_length = length - 1
    remaining_characters = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=remaining_length))

    # Combine and return
    return first_letter + remaining_characters

def load_usernames():
    """Prompt the user for a file and load usernames."""
    file_name = input("Enter the filename with usernames (e.g., usernames.txt): ").strip()
    try:
        usernames = read_usernames_from_file(file_name)
        if not usernames:
            raise ValueError("The file is empty.")
        return usernames
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit()
    except ValueError as ve:
        print(ve)
        exit()

def read_usernames_from_file(filename):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, "wordlists", filename)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            usernames = file.readlines()
            print(f"Usernames to check: {len(usernames)}")
        
        # Filter and process usernames
        valid_usernames = [
            username.strip().lower()
            for username in usernames
            if 4 <= len(username.strip()) <= 12 and  # Enforce length limit
               re.match("^[A-Za-z]+$", username.strip()) and
               " " not in username.strip()
        ]
        
        # Filter out vulgar usernames
        sanitized_usernames = filter_vulgar_words(valid_usernames)

        # Shuffle the usernames
        random.shuffle(sanitized_usernames)
        return sanitized_usernames
    
    except FileNotFoundError:
        print(f"File '{filename}' not found. Generating random usernames.")
        char_length = int(input("Enter length of characters: ").strip())
        return [generate_random_username(char_length) for _ in range(10000)]
    
def create_indexed_usernames(usernames):
    return [(index, user) for index, user in enumerate(usernames)]

def _get_txt_files_recursive(owner: str, repo: str, path: str) -> list[dict]:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url)
    resp.raise_for_status()
    items = resp.json()

    txt_files = []
    for item in items:
        if item["type"] == "file" and item["name"].endswith(".txt"):
            txt_files.append(item)
        elif item["type"] == "dir":
            txt_files += _get_txt_files_recursive(owner, repo, item["path"])
    return txt_files


def load_github_usernames(owner: str, repo: str, base_path: str) -> list[str]:
    """
    Recursively loads .txt files from GitHub repo, prompts user for one,
    returns a shuffled and sanitized list of usernames.
    """
    txt_files = _get_txt_files_recursive(owner, repo, base_path)
    if not txt_files:
        raise RuntimeError("No .txt files found.")

    print("Available .txt files:")
    for idx, file in enumerate(txt_files, start=1):
        print(f"{idx}. {file['path']}")

    while True:
        choice = input(f"Select a file (1-{len(txt_files)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(txt_files):
            selected = txt_files[int(choice) - 1]
            break
        print("Invalid selection, try again.")

    raw_resp = requests.get(selected['download_url'])
    raw_resp.raise_for_status()
    usernames = raw_resp.text.splitlines()

    # Filter out vulgar usernames
    sanitized_usernames = filter_vulgar_words(usernames)

    return sanitized_usernames