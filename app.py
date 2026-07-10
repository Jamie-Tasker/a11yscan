"""
A11yScan — Streamlit web app (Day 5).

Uses the shared, hardened fetch.py and reports fetch problems gracefully
in the UI instead of crashing.
"""

import streamlit as st

from fetch import fetch_page
import accessibility
import readability
import style


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
        soup, error = fetch_page(url)

        if error:
            st.error(error)
        else:
            show_section("Accessibility", accessibility.DESCRIPTION,
                         accessibility.check_accessibility(soup))
            show_section("Readability", readability.DESCRIPTION,
                         readability.check_readability(soup))
            show_section("Style guide", style.DESCRIPTION,
                         style.check_style(soup))
