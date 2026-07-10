"""
House style checker.

Each rule is a (pattern, message) pair. Add or edit rules freely.
"""

import copy
import re

# A short explanation shown above the results.
DESCRIPTION = (
    "Checks the text against the University of Cambridge digital style guide "
    "(cam.ac.uk/brand-resources/content/style-guide). It flags concrete rules a "
    "program can check — for example writing 'and' not '&', avoiding 'Oxbridge', "
    "not using 'click here' as link text, and leaving 'st/nd/rd/th' off dates. "
    "Rules that need human judgement (using the active voice, sentence case, or "
    "explaining abbreviations on first use) are not checked automatically."
)

# Each rule is a (regex pattern, explanation) pair, drawn from the Cambridge
# style guide. re.IGNORECASE (further down) means capitals don't matter.
STYLE_RULES = [
    (r"\w\s*&\s*\w", "Avoid using '&' — always write 'and'."),
    (r"\bOxbridge\b", "Do not write 'Oxbridge' — write 'the Universities of Oxford and Cambridge'."),
    (r"\bCambridge University\b", "Avoid 'Cambridge University' unless it is part of a proper noun — use 'the University of Cambridge'."),
    (r"\bclick here\b", "Never use 'click here' as link text — describe where the link goes."),
    (r"\bread more\b", "Never use 'read more' as link text — describe where the link goes."),
    (r"\blog\s?in\b", "Use 'sign in' instead of 'log in' where possible."),
    (r"\bphone\b", "Use 'Telephone', not 'Phone'."),
    (r"\b\d{1,2}(st|nd|rd|th)\b", "Do not use 'st', 'nd', 'rd' or 'th' in dates — write '8 August 2021'."),
    (r"\b\d+\+", "Do not use the plus sign with numbers (e.g. '40+') — write 'aged 40 years and over'."),
    (r"\bhttps?://", "Do not include 'http://' or 'https://' when writing a URL — use 'www.cam.ac.uk'."),
    (r"\b\d{3,4}\s?hrs\b", "Use the 12-hour clock (e.g. '5:30pm'), not the 24-hour clock."),
    (r"[A-Za-z];", "Do not use semicolons — they can be misread."),
    (r"[A-Za-z]!", "Do not use exclamation marks unless they appear in a direct quote."),
    (r"\b\w+'ve\b", "Avoid contractions such as 'should've' — write the words in full."),
    (r"\b(can't|don't|won't|isn't|aren't|didn't|doesn't|couldn't|wouldn't|shouldn't)\b",
     "Avoid contractions such as 'can't' and 'don't' — write the words in full."),
]


def _content_text(soup):
    """Return the page's main body text, with navigation, header and footer
    regions removed so menus and footer links don't create false style hits.
    """
    page = copy.copy(soup)

    # Remove whole regions that are usually menus and footers, not body text.
    for tag in page.find_all(["script", "style", "noscript", "nav", "header", "footer", "aside"]):
        tag.decompose()

    # Also remove anything labelled as navigation/footer with a "role" attribute.
    for role in ("navigation", "banner", "contentinfo", "search"):
        for tag in page.find_all(role=role):
            tag.decompose()

    return page.get_text(separator=" ")


def check_style(soup):
    text = _content_text(soup)
    issues = []

    for pattern, message in STYLE_RULES:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            issues.append(f"{message} (found {len(matches)} time(s))")

    return issues
