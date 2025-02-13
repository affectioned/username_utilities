import os
import requests
from playwright.sync_api import sync_playwright
from fake_headers import Headers
from dotenv import load_dotenv

load_dotenv()


def write_hits(user, platform_name):
    """
    Writes the available username to a file and sends a styled webhook message.

    Args:
        user (str): The username that is available.
        platform_name (str): The name of the platform where the username is available.
    """
    with open("hits.txt", "a", encoding="utf-8") as f:
        f.write(f"{user} | Available at {platform_name}\n")


def debug_playwright_response(url, proxy_config):
    try:
        with sync_playwright() as playwright:

            chromium = playwright.chromium # or "firefox" or "webkit".
            browser = chromium.launch(headless=False, proxy=proxy_config)
            context = browser.new_context(locale='en-US')
            page = context.new_page()

            # Navigate to the URL
            response = page.goto(url, wait_until="load", timeout=60000)
            page_content = page.content()

            print(f"URL: {url}")
            print(f"Headers: {response.all_headers()}")
            print(f"Status Code: {response.status}")
            print(f"Status Text: {page_content}")
            print(f"Response: {response}")

            output_file = "response_output.txt"

            # Save response text to a file
            if os.path.exists(output_file):
                os.remove(output_file)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(page_content)
            print(f"Response text saved to {output_file}")

            return page_content

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")

def debug_requests_endpoint(
    url,
    method="GET",
    data=None,
    headers=None,
    cookies=None,
    params=None,
    json=None
):
    """
    Debug a requests endpoint with improved error handling and logging.

    Args:
        url (str): The URL to request.
        method (str): HTTP method to use (GET, POST, PUT, DELETE, etc.).
        headers (dict): Additional headers for the request.
        params (dict): Query parameters for the request.
        data (dict): Form-encoded data for the request body.
        json (dict): JSON payload for the request body.
    """
    # Ensure headers exist and enforce English language preference
    headers = headers or make_headers()

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            cookies=cookies,
            params=params,
            data=data,
            json=json,
        )

        # Log request details
        print(f"Request Method: {method}")
        print(f"URL: {response.url}")
        print(f"Headers: {response.request.headers}")
        if data:
            print(f"Form Data: {data}")
        if json:
            print(f"JSON Payload: {json}")

        # Log response details
        print("\nResponse Details:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        print(f"Elapsed Time: {response.elapsed}")
        print(f"Content-Length: {len(response.text)}")
        print("Response Text:")
        print(response.text)

        # Attempt to parse JSON if applicable
        if response.headers.get('Content-Type', '').startswith('application/json'):
            try:
                print("Response JSON:")
                print(response.json())
            except ValueError:
                print("Invalid JSON in response.")

        output_file = "response_output.txt"

        # Save response text to a file
        if os.path.exists(output_file):
            os.remove(output_file)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Response text saved to {output_file}")

        return response

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")


def make_headers():
    header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate only Windows platform
        headers=True  # Generate misc headers
    )
    generated_headers = header.generate()
    return generated_headers


def print_progress(current_index, total_count, message):
    percentage = (current_index + 1) / total_count * 100
    print(f"[{current_index + 1}/{total_count}] ({percentage:.2f}%) {message}")


def debug_page_content(page_content):
    with open("debug.html", "w", encoding="utf-8") as file:
        file.write(page_content)
    print("Page content saved to: debug.html")
    exit
