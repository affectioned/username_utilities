import concurrent.futures
import utils
import common_utils
from platforms_config import platforms
from request_handler import check_with_playwright
from request_handler import check_with_requests
from proxy_manager import get_proxy_config
from tqdm import tqdm  # Import tqdm for progress bar


def check_username(user, platform, pbar):
    """
    Check the availability of a username using HTTP requests or Playwright based on platform checks.

    Args:
        user (str): The username to check.
        platform (dict): The selected platform's information containing name and checks.
        pbar (tqdm.tqdm): A tqdm progress bar instance to update progress.
    """
    try:
        result = ""
        proxy_config = get_proxy_config()
        if platform["name"] in ["Epic Games", "Instagram", "YouTube"]:
            result = check_with_playwright(user, platform["checks"], proxy_config)
        else:
            result = check_with_requests(user, platform["checks"], proxy_config)

        # Log the result only if the username is available
        if result["final_status"] == "available":
            utils.write_hits(result["user"], platform["name"])
            pbar.write(f"[+] Available: {user} on {platform['name']}")  # Log available usernames

    except Exception as e:
        # Handle unexpected errors gracefully
        pbar.write(f"[!] Error checking {user}: {e}")  # Log errors

    # Update the progress bar
    pbar.update(1)


def select_platform():
    """
    Prompt the user to select a platform to check usernames, and return the corresponding checks.

    Returns:
        dict: The selected platform's information containing the name and checks.
    """
    print("\nChoose a platform to check usernames:")
    for key, platform_info in platforms.items():
        print(f"[{key}] {platform_info['name']}")

    choice = input(
        "\nEnter your choice (e.g., xbox, roblox, telegram, or exit to exit): ").lower()

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
    usernames = common_utils.load_usernames()
    total_count = len(usernames)

    print("Starting username checks...")

    try:
        with tqdm(total=total_count, desc="Checking usernames", unit="user") as pbar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                # Submit tasks individually
                future_to_user = {
                    executor.submit(
                        check_username, user, selected_platform, pbar
                    ): user for user in usernames
                }

                for future in concurrent.futures.as_completed(future_to_user):
                    user = future_to_user[future]
                    try:
                        future.result()  # This raises any exception that occurred in the thread
                    except Exception as e:
                        pbar.write(f"[!] Error occurred while checking {user}: {e}")

    except Exception as e:
        print(f"[!] An error occurred during execution: {e}")
    finally:
        print("All username checks completed.")