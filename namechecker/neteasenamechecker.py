import requests
import json
import os

# URL for username checking
url = "https://passport.mpsdk.easebar.com/oauth/register/email/check_account_name?lang=en_US"

# Headers extracted from the HAR file
headers = {
    "Host": "passport.mpsdk.easebar.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://passport.mpsdk.easebar.com",
    "Connection": "keep-alive",
    "Referer": "https://passport.mpsdk.easebar.com/account/register?client_id=drop&from=kp&hide_back=1&lang=en_US",
}

# Function to check a username
def check_username(username):
    payload = {"account_name": username}
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return "Available"
    elif response.status_code == 400:
        return "Taken"
    else:
        return f"Error: {response.status_code}"

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

# Check usernames and print results
results = {}
for username in usernames:
    try:
        status = check_username(username)
        results[username] = status
        if status == "Available":
            with open("hits.txt", "a", encoding="utf-8") as f:
                f.write(f"{username} | Available at {url}\n")
        print(f"Username '{username}': {status}")
    except requests.exceptions.RequestException as e:
        print(f"Error checking username '{username}': {e}")
    except Exception as e:
        print(f"Unexpected error for username '{username}': {e}")

# Save the results to a JSON file
output_file = os.path.join(script_dir, "username_check_results.json")
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4)
    print(f"Results saved to {output_file}")