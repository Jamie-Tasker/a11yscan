"""
fetch.py — shared page fetching (Day 5).

We move fetch_page here so BOTH main.py and app.py use one version.

fetch_page returns TWO values: the page and an error message.
- On success: (page, None)
- On failure: (None, "a friendly message explaining what went wrong")

The caller checks whether the error is None to decide what to do. This
avoids more advanced error-handling techniques.
"""

import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return None, "URL must start with http:// or https://"

    headers = {"User-Agent": "A11yScan/1.0 (learning project)"}

    # try/except catches problems like the site being down or too slow.
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        return None, "The site took too long to respond (timed out)."
    except requests.exceptions.RequestException as error:
        return None, f"Could not reach the site: {error}"

    # 403/429 usually means the site is blocking automated scraping — say so
    # honestly rather than trying to work around it.
    if response.status_code == 401 or response.status_code == 403 or response.status_code == 429:
        return None, (
            f"The site returned {response.status_code} — it is likely blocking "
            "automated scraping. Try a different page."
        )

    if response.status_code != 200:
        return None, f"The site returned HTTP {response.status_code}."

    content_type = response.headers.get("Content-Type", "")
    if "html" not in content_type.lower():
        return None, f"That URL is not an HTML page (Content-Type: {content_type})."

    page = BeautifulSoup(response.text, "html.parser")
    return page, None
