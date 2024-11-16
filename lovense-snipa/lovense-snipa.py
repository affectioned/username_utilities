import requests
import time
import random
import os

def check_username(username):
    url = "https://www.lovense.com/ajaxCheckIdentityRegisted"
    payload = {"identity": username}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.lovense.com",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        
        # Check for rate limit HTML response
        if "<!DOCTYPE html><html lang=\"en-US\"><head><title>Just a moment...</title>" in response.text:
            return "rate_limited", username
        
        # Check for IP restriction JSON response
        try:
            response_data = response.json()
            if response_data.get("result") == False and response_data.get("code") == 50500:
                return "ip_restricted", username
            
            # Log only if the username is available
            if not (response_data.get("result") and response_data.get("code") == 2001):
                return f"Username '{username}' is available."
        
        except ValueError:
            # Handle cases where the response is not valid JSON
            return f"Invalid JSON response for '{username}': {response.text}"
    
    except requests.exceptions.RequestException as e:
        return f"An error occurred with '{username}': {e}"

def log_result(log_filename, result):
    """Helper function to safely write a log entry."""
    try:
        with open(log_filename, "a") as log_file:
            log_file.write(result + "\n")
            log_file.flush()  # Ensure the result is written immediately
    except IOError as e:
        print(f"Failed to write to log file '{log_filename}': {e}")

def check_usernames_from_file(filename, log_filename):
    # Ensure the log file exists by opening it in append mode at the start
    open(log_filename, "a").close()

    try:
        with open(filename, "r") as file:
            usernames = [line.strip() for line in file.readlines()]
            total_usernames = len(usernames)
            
            i = 0
            while i < total_usernames:
                username = usernames[i]
                
                # Skip usernames that don't meet length requirements
                if not (6 <= len(username) <= 20):
                    i += 1
                    continue

                # Display progress
                print(f"Checking username {i + 1} of {total_usernames}: {username}")
                
                result = check_username(username)
                
                # Handle rate limiting for HTML response (15-minute pause)
                if isinstance(result, tuple) and result[0] == "rate_limited":
                    print(f"Rate limited on '{username}' (HTML response). Pausing for 1 minute...")
                    time.sleep(60)  # Sleep for 1 minutes
                    continue  # Retry the same username after pause

                # Handle IP restriction JSON response (30-minute pause)
                if isinstance(result, tuple) and result[0] == "ip_restricted":
                    print(f"IP restricted on '{username}'. Pausing for 30 minutes...")
                    time.sleep(1800)  # Sleep for 30 minutes
                    continue  # Retry the same username after pause

                # Log only if the result is not None (i.e., username is available or an error occurred)
                if isinstance(result, str):
                    print(result)
                    log_result(log_filename, result)  # Log the result
                
                # Random delay between 10 and 20 seconds
                time.sleep(random.randint(10, 20))
                
                i += 1  # Move to the next username
    
    except FileNotFoundError:
        error_message = f"The file '{filename}' was not found."
        print(error_message)
        log_result(log_filename, error_message)

if __name__ == "__main__":
    check_usernames_from_file("usernames.txt", "check_usernames_log.txt")