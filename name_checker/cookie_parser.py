import requests
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

def get_cookies_from_website(url: str, headless: bool = True) -> requests.cookies.RequestsCookieJar:
    """
    Open a website using Playwright, parse cookies from headers, and return them in a format
    compatible with the requests library.

    Args:
        url (str): The URL of the website to open.
        headless (bool): Whether to run the browser in headless mode. Default is True.

    Returns:
        requests.cookies.RequestsCookieJar: A cookie jar containing the cookies.
    """
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        stealth_sync(page)

        # Open the URL
        page.goto(url, wait_until="load")

        # Extract cookies and convert to requests-compatible format
        playwright_cookies = context.cookies()
        cookie_jar = requests.cookies.RequestsCookieJar()
        for cookie in playwright_cookies:
            cookie_jar.set(cookie['name'], cookie['value'], domain=cookie.get('domain', ''), path=cookie.get('path', '/'))

        # Close the browser
        browser.close()

    return cookie_jar

def get_playwright_headers(url: str, headless: bool = True) -> dict:
    """
    Open a website using Playwright and return all request headers used by the browser.

    Args:
        url (str): The URL of the website to open.
        headless (bool): Whether to run the browser in headless mode. Default is True.

    Returns:
        dict: A dictionary containing all request headers.
    """
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        # Open the URL
        page.goto(url)

        # Extract headers from the request
        request_headers = {}

        def capture_request(route):
            nonlocal request_headers
            request_headers = route.request.headers
            route.continue_()

        context.route("**/*", capture_request)
        page.reload(wait_until="load")

        # Close the browser
        browser.close()

    return request_headers