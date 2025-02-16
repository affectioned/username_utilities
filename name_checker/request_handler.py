import utils
import requests
import time
import httpx
from playwright.sync_api import sync_playwright
from cookie_manager import add_cookies
from playwright_stealth import stealth_sync


def check_with_httpx(user, checks, proxy_config, max_retries=3, rate_limit_pause=60):
    """
    Check the availability of a username by processing multiple URL checks using httpx.

    Args:
        user (str): The username to check.
        checks (list): A list of checks, each a dictionary with 'url', 'detection', and 'method' keys.
        proxy_config (dict): Proxy configuration with keys 'username', 'password', and 'server'.
        max_retries (int): Maximum number of retries for each request. Defaults to 3.
        rate_limit_pause (int): Time to pause (in seconds) after multiple consecutive failures. Defaults to 60.

    Returns:
        dict: A dictionary containing the availability status and details for each check.
    """
    results = []

    for check in checks:
        try:
            # Replace placeholders with `user`
            url = check['url'].format(*(user,) * check['url'].count("{}"))
        except IndexError as e:
            print(
                f"[!] Error formatting URL: {check['url']}, user: {user}. Error: {e}")
            results.append({"url": check['url'], "status": "error"})
            continue

        detection_pattern = check['detection']
        method = check['method']
        retries = 0

        while retries < max_retries:
            try:
                proxy_url = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['server']}"

                headers = utils.make_headers()

                # Prepare request arguments
                request_kwargs = {
                    "method": method,
                    "headers": headers,
                    "url": url,
                    "follow_redirects": True,
                }

                # Handle dynamic `data` or `json` payloads
                if "data" in check:
                    request_kwargs["data"] = {
                        key: value.format(
                            *(user,) * value.count("{}")) if isinstance(value, str) else value
                        for key, value in check["data"].items()
                    }
                elif "json" in check:
                    request_kwargs["json"] = {
                        key: value.format(
                            *(user,) * value.count("{}")) if isinstance(value, str) else value
                        for key, value in check["json"].items()
                    }

                with httpx.Client(proxy=proxy_url) as session:
                    response = session.request(**request_kwargs)
                    
                status_code = response.status_code

                # Handle rate limiting
                if status_code == 429:
                    retry_after = int(response.headers.get(
                        "Retry-After", rate_limit_pause))
                    print(
                        f"[!] Rate limited for {url}. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue

                # Process response
                if status_code == 404:
                    results.append({"url": url, "status": "available"})
                    break  # Proceed to next check
                elif status_code == 200 and detection_pattern in response.text:
                    results.append({"url": url, "status": "available"})
                    break
                else:
                    results.append({"url": url, "status": "taken"})
                    return {
                        "user": user,
                        "checks": results,
                        "final_status": "taken",
                    }

            except httpx.RequestError as e:
                retries += 1
                print(
                    f"[!] Error accessing {url} (Attempt {retries}/{max_retries}): {e}")
                time.sleep(10)

        if retries == max_retries:
            print(
                f"[!] Max retries reached for {url}. Taking a rate-limit break of {rate_limit_pause} seconds...")
            time.sleep(rate_limit_pause)
            results.append({"url": url, "status": "error"})
            break

    return {
        "user": user,
        "checks": results,
        "final_status": "available",
    }


def check_with_requests(user, checks, proxy_config, max_retries=3, rate_limit_pause=60):
    """
    Check the availability of a username by processing multiple URL checks.

    Args:
        user (str): The username to check.
        checks (list): A list of checks, each a dictionary with 'url' and 'detection'.
        proxy_config (dict): Proxy configuration with keys 'username', 'password', and 'server'.
        max_retries (int): Maximum number of retries for each request. Defaults to 3.
        rate_limit_pause (int): Time to pause (in seconds) after multiple consecutive failures. Defaults to 60.
    Returns:
        dict: A dictionary containing the availability status and details for each check.
    """
    results = []

    for check in checks:
        try:
            # Dynamically replace placeholders with `user`
            url = check['url'].format(*(user,) * check['url'].count("{}"))
        except IndexError as e:
            print(f"[!] Error formatting URL: {
                  check['url']}, user: {user}. Error: {e}")
            results.append({"url": check['url'], "status": "error"})
            continue

        detection_pattern = check['detection']
        method = check['method']
        retries = 0

        while retries < max_retries:  # Retry loop
            try:
                proxy_url = f"http://{proxy_config['username']}:{
                    proxy_config['password']}@{proxy_config['server']}"
                proxies = {"http": proxy_url, "https": proxy_url}

                headers = utils.make_headers()

                # Ensure Content-Type is set for Discord
                if "discord" in url:
                    headers["Content-Type"] = "application/json"

                # Handle `data` or `json` dynamically
                request_kwargs = {
                    "method": method,
                    "url": url,
                    "headers": headers,
                    "proxies": proxies,
                    "allow_redirects": True
                }

                if "data" in check:
                    request_kwargs["data"] = {
                        key: value.format(
                            *(user,) * value.count("{}")) if isinstance(value, str) else value
                        for key, value in check["data"].items()
                    }
                elif "json" in check:
                    request_kwargs["json"] = {
                        key: value.format(
                            *(user,) * value.count("{}")) if isinstance(value, str) else value
                        for key, value in check["json"].items()
                    }

                response = requests.request(**request_kwargs)

                status_code = response.status_code

                # Handle rate limiting
                if status_code == 429:
                    retry_after = int(response.headers.get(
                        "Retry-After", rate_limit_pause))
                    print(f"[!] Rate limited for {url}. Retrying after {
                          retry_after} seconds...")
                    time.sleep(retry_after)
                    continue

                # Process response
                if status_code == 404:
                    results.append({"url": url, "status": "available"})
                    break  # Move to the next check immediately
                elif status_code == 200 and detection_pattern in response.text:
                    results.append({"url": url, "status": "available"})
                    break
                else:
                    results.append({"url": url, "status": "taken"})
                    return {  # Exit if a check determines the username is taken
                        "user": user,
                        "checks": results,
                        "final_status": "taken",
                    }

            except requests.exceptions.RequestException as e:
                retries += 1
                print(f"[!] Error accessing {
                      url} (Attempt {retries}/{max_retries}): {e}")
                time.sleep(10)

        if retries == max_retries:
            print(f"[!] Max retries reached for {
                  url}. Taking a rate-limit break of {rate_limit_pause} seconds...")
            time.sleep(rate_limit_pause)
            results.append({"url": url, "status": "error"})
            break

    # If all checks pass, the username is available
    return {
        "user": user,
        "checks": results,
        "final_status": "available",
    }


def check_with_playwright(user, checks, proxy_config, max_retries=3, rate_limit_pause=60):
    """
    Check the availability of a resource using Playwright, handling rate limits.

    Args:
        user (str): The user identifier being checked.
        checks (list): A list of checks containing URL and detection pattern.
        proxy_config (dict): Proxy settings for Playwright.
        max_retries (int): Maximum retries before marking a check as failed.
        rate_limit_pause (int): Default time to wait when rate-limited.

    Returns:
        dict: A dictionary containing the results and final status.
    """
    results = []

    for check in checks:
        url = check['url'].format(user)
        detection_pattern = check['detection']
        retries = 0

        while retries < max_retries:  # Retry loop
            try:
                with sync_playwright() as playwright:
                    chromium = playwright.chromium  # or "firefox" or "webkit".
                    browser = chromium.launch(
                        headless=True, proxy=proxy_config)
                    context = browser.new_context(locale='en-US')

                    # Add cookies if necessary
                    add_cookies(context, url)

                    page = context.new_page()

                    stealth_sync(page)

                    # Navigate to the URL
                    response = page.goto(url, wait_until="load", timeout=60000)
                    page_content = page.content()

                    # Handle rate limiting (429 Too Many Requests)
                    if response.status == 429:
                        retry_after = int(response.headers.get(
                            "Retry-After", rate_limit_pause))
                        print(
                            f"[!] Rate limited for {url}. Retrying after {retry_after} seconds...")
                        time.sleep(retry_after)
                        continue  # Retry after waiting

                    # Handle normal responses
                    if response.status == 404:
                        results.append({"url": url, "status": "available"})
                    elif detection_pattern in page_content:
                        results.append({"url": url, "status": "available"})
                    else:
                        results.append({"url": url, "status": "taken"})
                        return {
                            "user": user,
                            "checks": results,
                            "final_status": "taken",
                        }

                    context.close()
                    browser.close()
                    break  # Exit retry loop on success

            except Exception as e:
                retries += 1
                print(
                    f"[!] Error accessing {url} (Attempt {retries}/{max_retries}): {e}")
                time.sleep(10)  # Wait before retrying

        if retries == max_retries:
            print(f"[!] Max retries reached for {url}. Skipping...")
            results.append({"url": url, "status": "error"})

    return {
        "user": user,
        "checks": results,
        "final_status": "available" if all(r["status"] == "available" for r in results) else "error",
    }
