"""
A11yScan — command-line entry point (Day 5).
"""

import sys
import textwrap

from fetch import fetch_page
import accessibility
import readability
import style


def print_section(title, description, issues):
    print(f"\n=== {title} ===")
    # Wrap the intro so it reads nicely in a terminal.
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

    soup, error = fetch_page(url)
    if error:
        print(f"\nCould not scan the page: {error}")
        sys.exit(1)

    print_section("Accessibility", accessibility.DESCRIPTION,
                  accessibility.check_accessibility(soup))
    print_section("Readability", readability.DESCRIPTION,
                  readability.check_readability(soup))
    print_section("Style guide", style.DESCRIPTION,
                  style.check_style(soup))


if __name__ == "__main__":
    main()
