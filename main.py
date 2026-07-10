"""
A11yScan — command-line entry point (Day 2).

Now runs the accessibility checker after fetching the page.
"""

import sys
import textwrap
import requests
from bs4 import BeautifulSoup

import accessibility


def fetch_page(url):
    headers = {"User-Agent": "A11yScan/0.1 (learning project)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def print_section(title, description, issues):
    print(f"\n=== {title} ===")
    for line in textwrap.wrap(description, width=78):
        print(line)
    print()
    if not issues:
        print("  No problems found.")
    else:
        for issue in issues:
            print(f"  - {issue}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"Scanning: {url}")

    soup = fetch_page(url)

    print_section("Accessibility", accessibility.DESCRIPTION,
                  accessibility.check_accessibility(soup))


if __name__ == "__main__":
    main()
