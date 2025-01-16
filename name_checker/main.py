import concurrent.futures
import utils
import username_utils
from platforms_config import platforms
from request_handler import check_availability_with_status_code
from request_handler import check_availability_with_playwright

def check_username(user, platform, total_count):
    """
    Check the availability of a username using HTTP requests or Playwright based on platform checks.

    Args:
        user (str): The username to check.
        platform (dict): The selected platform's information containing name and checks.
        total_count (int): The total number of usernames to check.
        proxy_pool (Iterator, optional): A pool of proxies for requests. Defaults to None.
    """
    try:
        result = ""
        if platform["name"] == "Epic Games" or "Instagram" or "Twitter" or "YouTube":
            result = check_availability_with_playwright(user, platform["checks"])
        else:
            result = check_availability_with_status_code(user, platform['checks'])

        # Log the result based on the final status
        if result["final_status"] == "available":
            utils.write_hits(result["user"], platform["name"])
            status = "[+] Available"
        else:
            status = "[-] Taken"

    except Exception as e:
        # Handle unexpected errors gracefully
        status = "[!] Error"
        print(f"[!] Error checking {user}: {e}")

    # Calculate percentage of processed usernames
    processed_count = len(username_utils.get_processed_usernames())
    percentage = (processed_count / total_count) * 100

    # Log progress at the end
    print(f"[{processed_count}/{total_count}] ({percentage:.2f}%) {status}: {user} on {platform['name']}")
    username_utils.mark_username_processed(user)

def select_platform():
    """
    Prompt the user to select a platform to check usernames, and return the corresponding checks.

    Returns:
        dict: The selected platform's information containing the name and checks.
    """
    print("\nChoose a platform to check usernames:")
    for key, platform_info in platforms.items():
        print(f"[{key}] {platform_info['name']}")

    choice = input("\nEnter your choice (e.g., xbox, roblox, telegram, or exit to exit): ").lower()

    if choice == "exit":
        print("Exiting...")
        exit(0)

    if choice in platforms:
        return platforms[choice]

    print("Invalid choice. Please try again.")
    return select_platform()


if __name__ == "__main__":
    # Select the platform to check usernames
    selected_platform = select_platform()
    print(f"- Selected platform: {selected_platform['name']}")
    print(f"- Checks to perform: {selected_platform['checks']}")

    # Load usernames to check
    usernames = username_utils.load_usernames()
    total_count = len(usernames)

    print("Starting username checks...")

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            # Submit tasks individually
            future_to_user = {
                executor.submit(
                    check_username, user, selected_platform, total_count
                ): user for user in usernames
            }

            for future in concurrent.futures.as_completed(future_to_user):
                user = future_to_user[future]
                try:
                    future.result()  # This raises any exception that occurred in the thread
                except Exception as e:
                    print(f"[!] Error occurred while checking {user}: {e}")

    except Exception as e:
        print(f"[!] An error occurred during execution: {e}")
    finally:
        print("All username checks completed.")