import string
import random
import os
import re

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
        filtered_usernames = [username.strip().lower() for username in usernames if len(username.strip()) >= 3 and re.match("^[A-Za-z]+$", username.strip())]
        # Shuffle the usernames
        random.shuffle(filtered_usernames)
        return filtered_usernames
    except FileNotFoundError:
        print(f"File '{filename}' not found. Generating random usernames.")
        char_length = int(input("Enter length of characters: ").strip())
        return [generate_random_username(char_length) for _ in range(1000)]
    
def create_indexed_usernames(usernames):
    return [(index, user) for index, user in enumerate(usernames)]