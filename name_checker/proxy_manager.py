import os
from dotenv import load_dotenv

load_dotenv()

def get_proxy_domain():
    domain = os.getenv("PROXY_DOMAIN")
    if not domain:
        raise ValueError("PROXY_DOMAIN is not set in the .env file.")
    return domain

def get_proxy_port():
    port = os.getenv("PROXY_PORT")
    if not port:
        raise ValueError("PROXY_PORT is not set in the .env file.")
    return port

def get_proxy_username():
    username = os.getenv("PROXY_USERNAME")
    if not username:
        raise ValueError("PROXY_USERNAME is not set in the .env file.")
    return username

def get_proxy_password():
    password = os.getenv("PROXY_PASSWORD")
    if not password:
        raise ValueError("PROXY_PASSWORD is not set in the .env file.")
    return password

def get_proxy_config():
    """Returns the full proxy configuration as a dictionary."""
    return {
        "server": f"{get_proxy_domain()}:{get_proxy_port()}",
        "username": get_proxy_username(),
        "password": get_proxy_password()
    }
