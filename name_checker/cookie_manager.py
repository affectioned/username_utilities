import os

def parse_cookies(file_path):
    cookies = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Skip comments and blank lines
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 7:
                cookies.append({
                    "name": parts[5],                # Cookie name
                    "value": parts[6],               # Cookie value
                    "domain": parts[0],              # Domain
                    "path": parts[2],                # Path
                    "secure": parts[3].lower() == "true",  # Secure flag
                    # Expiry timestamp
                    "expires": int(parts[4]) if parts[4].isdigit() else None,
                    "httpOnly": False,               # Assume httpOnly is False unless specified
                    "sameSite": "None"               # Adjust if necessary
                })
    return cookies


def add_cookies(context, url):
    # Define the base directory for the cookies
    base_cookies_dir = os.path.join(
        os.path.dirname(__file__), "put_cookies_here")

    # Updated cookie configuration
    cookie_config = {
        "www.instagram.com": os.path.join(base_cookies_dir, "instagram", "cookies.txt"),
        "www.x.com": os.path.join(base_cookies_dir, "x", "cookies.txt"),
    }

    # Extract domain from the URL
    for site in cookie_config:
        if site in url:
            path = cookie_config[site]
            try:
                cookies = parse_cookies(path)
                context.add_cookies(cookies)
            except FileNotFoundError:
                print(f"[!] Cookies file not found for {site}: {
                      path}. Proceeding without cookies.")
            except Exception as e:
                print(f"[!] Error loading cookies for {site}: {e}")
            return