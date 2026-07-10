"""
Accessibility checker.

Takes a parsed BeautifulSoup object and returns a list of human-readable
issue strings. Returning a plain list keeps each checker independent and
easy to test — main.py (and later the web app) just prints whatever it gets.
"""

# A short explanation shown above the results, so the reader knows what
# standard we're checking against. Kept next to the check it describes.
DESCRIPTION = (
    "Checks two common problems from the Web Content Accessibility Guidelines "
    "(WCAG) — the international standard for accessible websites. It flags "
    "images with no meaningful alt text (WCAG 1.1.1, 'Non-text Content'), so "
    "screen-reader users know what each image shows, and headings that skip a "
    "level (WCAG 1.3.1, 'Info and Relationships'), which breaks the page's "
    "structure. This is a small subset of WCAG, not a full audit."
)


def check_accessibility(soup):
    issues = []
    issues.extend(_check_image_alt_text(soup))
    issues.extend(_check_heading_order(soup))
    return issues


def _check_image_alt_text(soup):
    """Flag <img> tags with a missing or blank alt attribute."""
    problems = []
    for index, img in enumerate(soup.find_all("img"), start=1):
        alt = img.get("alt")
        src = img.get("src", "(no src)")
        if len(src) > 50:
            src = src[:47] + "..."
        if alt is None:
            problems.append(f"Image #{index} ({src}) has no alt attribute at all.")
        elif alt.strip() == "":
            problems.append(f"Image #{index} ({src}) has a blank alt attribute.")
    return problems


def _check_heading_order(soup):
    """Flag heading levels that jump (e.g. an <h2> followed by an <h4>)."""
    problems = []
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    previous_level = 0
    for heading in headings:
        current_level = int(heading.name[1])  # "h2" -> 2
        text = heading.get_text(strip=True)[:40]

        if previous_level and current_level > previous_level + 1:
            problems.append(
                f"Heading level jumps from h{previous_level} to h{current_level} "
                f"at \"{text}\" (a level was skipped)."
            )
        previous_level = current_level

    return problems
