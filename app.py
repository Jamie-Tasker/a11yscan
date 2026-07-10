"""
A11yScan — Streamlit web app (Day 4).

Streamlit re-runs this whole script top to bottom on every interaction
(every time a button is clicked or a box is typed in) and redraws the
page from the current values. You write normal top-to-bottom Python and
Streamlit turns each st.* call into a piece of the web page.

Crucially, this imports the SAME checker modules the CLI uses. No logic
is duplicated; we've only added a face.
"""

import requests
import streamlit as st
from bs4 import BeautifulSoup

import accessibility
import readability
import style


def fetch_page(url):
    headers = {"User-Agent": "A11yScan/0.1 (learning project)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def show_section(title, description, issues):
    st.subheader(title)
    st.caption(description)  # the intro paragraph, in smaller grey text
    if not issues:
        st.success("No problems found.")
    else:
        for issue in issues:
            st.write(f"- {issue}")


st.title("A11yScan")
st.write("Enter a webpage URL to check its accessibility, readability and style.")

url = st.text_input("URL", placeholder="https://example.com")

if st.button("Scan") and url:
    with st.spinner("Fetching and analysing the page..."):
        soup = fetch_page(url)
        show_section("Accessibility", accessibility.DESCRIPTION,
                     accessibility.check_accessibility(soup))
        show_section("Readability", readability.DESCRIPTION,
                     readability.check_readability(soup))
        show_section("Style guide", style.DESCRIPTION,
                     style.check_style(soup))
