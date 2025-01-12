import os
from itertools import cycle
from dotenv import load_dotenv

load_dotenv()


def create_proxy_pool():
    """
    Creates a single-item cycle for the Webshare rotating proxy using environment variables.

    Returns:
        itertools.cycle: A cycle with a single authenticated proxy for infinite iteration.
    """
    proxy_url = os.getenv("PROXY_URL")
    if not proxy_url:
        raise ValueError("PROXY_URL environment variable is not set.")
    return cycle([proxy_url])  # Create a single-item cycle


def get_next_proxy(proxy_pool):
    """
    Fetches the next proxy from the pool.

    Args:
        proxy_pool (itertools.cycle): The proxy pool.

    Returns:
        str: The next proxy.
    """
    return next(proxy_pool)
