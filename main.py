"""
A11yScan — command-line entry point (Day 1).

Usage:
python main.py <url>

Day 1 only proves the plumbing: fetch a page and print its title.
The actual checks arrive on Days 2 and 3.
"""

import sys
import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    """Download a URL and return a parsed BeautifulSoup object.

    requests downloads the raw HTML; BeautifulSoup turns that HTML string
    into an object we can search (find tags, read attributes, get text).
    """
    # A User-Agent makes us look like a normal browser to polite servers.
    headers = {"User-Agent": "A11yScan/0.1 (learning project)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # turn a 404/500 into an exception
    return BeautifulSoup(response.text, "html.parser")


def main():
    # sys.argv is the list of command-line arguments; argv[0] is the script name.
    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"Scanning: {url}\n")

    soup = fetch_page(url)

    title = soup.title.string.strip() if soup.title and soup.title.string else "(no <title> found)"
    print(f"Page title: {title}")


if __name__ == "__main__":
    # This guard means the code only runs when the file is executed directly,
    # not when it's imported by another module (we'll rely on that on Day 4).
    main()
