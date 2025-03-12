import requests
import string
import random
import os
import re

def filter_vulgar_words(words):
    """
    Filters out vulgar words from a list of words using an online vulgar words list.

    Parameters:
    words (list): A list of words to filter.

    Returns:
    list: A filtered list of words without vulgarisms.
    """
    # URL of the vulgar words list
    vulgar_words_url = "https://www.cs.cmu.edu/~biglou/resources/bad-words.txt"
    
    try:
        # Fetch the list of vulgar words
        response = requests.get(vulgar_words_url)
        response.raise_for_status()  # Raise an error for unsuccessful requests
        vulgarisms = set(response.text.splitlines())
        
        # Filter out words that match any vulgarism (case-insensitive)
        filtered_words = [word for word in words if word.lower() not in vulgarisms]
        
        return filtered_words
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching vulgar words list: {e}")
        return words  # Return the original list if fetching fails

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
        return [generate_random_username(char_length) for _ in range(500)]
    
def create_indexed_usernames(usernames):
    return [(index, user) for index, user in enumerate(usernames)]