import winsound
import utils
import requests
import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from cookie_manager import add_cookies
from cookie_parser import get_cookies_from_website
from cookie_parser import get_playwright_headers

def check_availability_with_status_code(user, checks, proxy_pool=None, max_retries=3, rate_limit_pause=60):
    """
    Check the availability of a username by processing multiple URL checks.

    Args:
        user (str): The username to check.
        checks (list): A list of checks, each a dictionary with 'url' and 'detection'.
        proxy_pool (Iterator, optional): A pool of proxies for requests. Defaults to None.
        max_retries (int): Maximum number of retries for each request. Defaults to 3.
        rate_limit_pause (int): Time to pause (in seconds) after multiple consecutive failures. Defaults to 60.

    Returns:
        dict: A dictionary containing the availability status and details for each check.
    """
    results = []

    for check in checks:
        url = check['url'].format(user)
        detection_pattern = check['detection']
        retries = 0

        while retries < max_retries:  # Retry loop for handling failures
            try:
                # Use proxy if available
                proxies = None
                if proxy_pool:
                    proxy = next(proxy_pool)
                    proxies = {"http": proxy, "https": proxy}

                headers = get_playwright_headers(url, False)
                cookies = get_cookies_from_website(url, False)
                response = requests.get(url, headers=headers, cookies=cookies)


                status_code = response.status_code

                # Handle rate limiting
                if status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", rate_limit_pause))
                    print(f"[!] Rate limited for {url}. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                    if proxy_pool:  # Rotate proxy if possible
                        print(f"[!] Rotating proxy for {url}.")
                    continue

                # Determine result based on status code and detection pattern
                if status_code == 404:
                    results.append({"url": url, "status": "available"})
                elif status_code == 200 and detection_pattern in response.text:
                    results.append({"url": url, "status": "available"})
                else:
                    results.append({"url": url, "status": "taken"})
                    return {  # Exit immediately if a check determines the username is taken
                        "user": user,
                        "checks": results,
                        "final_status": "taken",
                    }
                break  # Exit the retry loop once the request is successful

            except requests.exceptions.RequestException as e:
                retries += 1
                print(f"[!] Error accessing {url} (Attempt {retries}/{max_retries}): {e}")
                time.sleep(10)  # Wait before retrying

        if retries == max_retries:  # If max retries are reached, apply a rate-limit break
            print(f"[!] Max retries reached for {url}. Taking a rate-limit break of {rate_limit_pause} seconds...")
            time.sleep(rate_limit_pause)
            results.append({"url": url, "status": "error"})
            break  # Exit the retry loop

    # If all checks pass, the username is available
    return {
        "user": user,
        "checks": results,
        "final_status": "available",
    }

def check_availability_with_playwright(url, url_format, user, current_index, total_count, detection_pattern):
    """
    Check the availability of a resource using Playwright.
    
    Args:
        url (str): The target URL to check.
        url_format (str): The URL format for adding cookies.
        user (str): The user identifier being checked.
        current_index (int): The current index in the check process.
        total_count (int): The total number of items being checked.
        detection_pattern (str): The detection pattern for availability.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(locale='en-US')

        # Add cookies if necessary
        add_cookies(context, url_format)
        page = context.new_page()

        # Define a blocking function for resource types
        def should_block(request):
            allowed_types = ['document', 'stylesheet', 'script', 'xhr', 'fetch']
            return request.resource_type not in allowed_types

        # Route requests to block unwanted resource types
        page.route("**/*", lambda route, request: route.abort() if should_block(request) else route.continue_())

        # Add stealth behaviors to the page
        stealth_sync(page)

        # Navigate to the URL
        response = page.goto(url, wait_until="load")  # Navigate without waiting for load
        page_content = page.content()

        # Check the response status and page content
        if response.status == 404:
            winsound.Beep(500, 500)
            utils.print_progress(current_index, total_count, f"[+] Available: {user} at {url}")
            utils.write_hits(user, url)
        elif detection_pattern in page_content:
            winsound.Beep(500, 500)
            utils.print_progress(current_index, total_count, f"[+] Available: {user} at {url}")
            utils.write_hits(user, url)
        else:
            utils.print_progress(current_index, total_count, f"[-] Taken: {user}")

        # Close the browser
        browser.close()