import utils
import requests
import time
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
from cookie_manager import add_cookies


def check_with_requests(user, checks, proxy_config, max_retries=3, rate_limit_pause=60):
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
        try:
            # Dynamically replace all `{}` placeholders with `user`
            url = check['url'].format(*(user,) * check['url'].count("{}"))
        except IndexError as e:
            print(f"[!] Error formatting URL: {
                  check['url']}, user: {user}. Error: {e}")
            results.append({"url": check['url'], "status": "error"})
            continue

        detection_pattern = check['detection']
        retries = 0

        while retries < max_retries:  # Retry loop for handling failures
            try:
                proxy_url = f"http://{proxy_config['username']}:{
                    proxy_config['password']}@{proxy_config['server']}"

                proxies = {
                    "http": proxy_url,
                    "https": proxy_url
                }

                response = requests.get(
                    url, headers=utils.make_headers(), proxies=proxies)

                status_code = response.status_code

                # Handle rate limiting
                if status_code == 429:
                    retry_after = int(response.headers.get(
                        "Retry-After", rate_limit_pause))
                    print(f"[!] Rate limited for {url}. Retrying after {
                          retry_after} seconds...")
                    time.sleep(retry_after)
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
                print(f"[!] Error accessing {
                      url} (Attempt {retries}/{max_retries}): {e}")
                time.sleep(10)  # Wait before retrying

        if retries == max_retries:  # If max retries are reached, apply a rate-limit break
            print(f"[!] Max retries reached for {
                  url}. Taking a rate-limit break of {rate_limit_pause} seconds...")
            time.sleep(rate_limit_pause)
            results.append({"url": url, "status": "error"})
            break  # Exit the retry loop

    # If all checks pass, the username is available
    return {
        "user": user,
        "checks": results,
        "final_status": "available",
    }


def check_with_playwright(user, checks, max_retries=3, rate_limit_pause=60):
    """
    Check the availability of a resource using Playwright.

    Args:
        user (str): The user identifier being checked.
        checks (list): A list of checks containing URL and detection pattern.
        proxy_pool (list): A pool of proxy servers (optional).
        max_retries (int): The maximum number of retries.
        rate_limit_pause (int): Pause time in seconds for rate-limiting.

    Returns:
        dict: A dictionary containing the results and the final status.
    """
    results = []

    for check in checks:
        url = check['url'].format(user)
        detection_pattern = check['detection']
        retries = 0
        while retries < max_retries:  # Retry loop for handling failures
            try:
                with sync_playwright() as p:

                    # Display the actual proxy details
                    browser = p.chromium.launch(headless=True)
                    context = browser.new_context(locale='en-US')

                    # Add cookies if necessary
                    add_cookies(context, url)

                    page = context.new_page()

                    # Define a blocking function for resource types
                    def should_block(request):
                        allowed_types = ['document', 'xhr', 'fetch']
                        return request.resource_type not in allowed_types

                    # Route requests to block unwanted resource types
                    page.route("**/*", lambda route, request: route.abort()
                               if should_block(request) else route.continue_())

                    # Add stealth behaviors to the page
                    stealth_sync(page)

                    # Navigate to the URL
                    response = page.goto(url, wait_until="load", timeout=60000)
                    page_content = page.content()

                    # Check the response status and page content
                    if response.status == 404:
                        results.append({"url": url, "status": "available"})
                    elif detection_pattern in page_content:
                        results.append({"url": url, "status": "available"})
                    else:
                        results.append({"url": url, "status": "taken"})
                        return {  # Exit immediately if a check determines the username is taken
                            "user": user,
                            "checks": results,
                            "final_status": "taken",
                        }

                    # Close browser resources
                    context.close()
                    browser.close()
                    break  # Break out of retry loop on success

            except Exception as e:  # Catch Playwright-specific exceptions
                retries += 1
                print(f"[!] Error accessing {
                      url} (Attempt {retries}/{max_retries}): {e}")
                time.sleep(10)  # Wait before retrying
                continue

        if retries == max_retries:  # If max retries are reached, apply a rate-limit break
            print(f"[!] Max retries reached for {
                  url}. Taking a rate-limit break of {rate_limit_pause} seconds...")
            time.sleep(rate_limit_pause)
            results.append({"url": url, "status": "error"})
            break  # Exit the retry loop

    # If all checks pass, the username is available
    return {
        "user": user,
        "checks": results,
        "final_status": "available",
    }
