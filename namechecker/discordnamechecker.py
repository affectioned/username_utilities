import requests
import time
import os

# Discord API endpoint for checking username availability
URL = "https://discord.com/api/v9/unique-username/username-attempt-unauthed"

# Prompt the user for the name of the text file
file_name = input("Enter the name of the text file (e.g., usernames.txt): ").strip()

# Get the path of the script directory and the text file
script_dir = os.path.dirname(os.path.abspath(__file__))
usernames_file = os.path.join(script_dir, file_name)

# Read usernames from the text file
if not os.path.exists(usernames_file):
    print(f"File '{file_name}' not found in the script directory. Please check the file name and try again.")
    exit()

with open(usernames_file, "r", encoding="utf-8") as file:
    usernames = [line.strip() for line in file if line.strip()]

if not usernames:
    print(f"The file '{file_name}' is empty. Please provide a valid file with usernames.")
    exit()

# File to log available usernames
available_usernames_file = os.path.join(script_dir, "available_usernames.txt")

# Function to check username availability
def check_username(username):
    payload = {"username": username}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    
    try:
        response = requests.post(URL, json=payload, headers=headers)
        if response.status_code == 429:  # Rate limited
            retry_after = int(response.headers.get("Retry-After", 5))
            print(f"Rate limited. Sleeping for {retry_after} seconds...")
            time.sleep(retry_after)
            return None
        
        response.raise_for_status()
        data = response.json()
        
        if data.get("taken") is True:
            print(f"Username '{username}' is already taken.")
        elif data.get("taken") is False:
            print(f"Username '{username}' is available.")
            return username  # Return available username
        else:
            print(f"Unexpected response for username '{username}': {data}")
    except requests.exceptions.RequestException as e:
        print(f"Error checking username '{username}': {e}")
    return None

# Process usernames at a rate of 2 per second and save available usernames
available_usernames = []
for i, username in enumerate(usernames):
    available = check_username(username)
    if available:
        available_usernames.append(available)
    if (i + 1) % 2 == 0:  # Pause after every 2 requests
        time.sleep(1)

# Save available usernames to a file
if available_usernames:
    with open(available_usernames_file, "w", encoding="utf-8") as log_file:
        log_file.write("\n".join(available_usernames))
    print(f"Available usernames saved to '{available_usernames_file}'.")
else:
    print("No available usernames found.")