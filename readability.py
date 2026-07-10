"""
Readability checker.
 
Computes an Automated Readability Index (ARI) score from the page's
visible text:
 
    4.71 * (characters / words) + 0.5 * (words / sentences) - 21.43
 
ARI uses letter counts rather than syllable counts, so unlike formulas
such as Flesch-Kincaid it needs no approximations — counting letters
is exact.
"""
 
import copy
import re
 
# A short explanation shown above the results.
DESCRIPTION = (
    "Higher numbers mean harder text. Writing for a general audience usually "
    "aims for grade 8-10. The score is based on how long the sentences are and "
    "how many letters the words have."
)
 
 
def check_readability(soup):
    text = _visible_text(soup)
 
    words = _count_words(text)
    sentences = _count_sentences(text)
 
    # Add up the letters in every word.
    characters = 0
    for word in words:
        characters += _count_characters(word)
 
    if not words or not sentences:
        return ["Not enough readable text on the page to score."]
 
    grade = (
        4.71 * (characters / len(words))
        + 0.5 * (len(words) / sentences)
        - 21.43
    )
 
    return [
        f"Automated Readability Index: grade {grade:.1f} "
        f"(from {len(words)} words, {sentences} sentences, {characters} letters).",
    ]
 
 
def _visible_text(soup):
    """Return page text with <script> and <style> tags removed (their contents
    are code, not readable words)."""
    # Copy the page first so we don't change it for the other checks.
    page = copy.copy(soup)
    for tag in page.find_all(["script", "style", "noscript"]):
        tag.decompose()
    return page.get_text(separator=" ")
 
 
def _count_words(text):
    # re.findall finds every match in the text and returns them as a list.
    # [a-zA-Z'] means "any letter or an apostrophe"; + means "one or more",
    # so each run of letters (like "don't") counts as one word.
    return re.findall(r"[a-zA-Z']+", text)
 
 
def _count_sentences(text):
    # [.!?] means "a full stop, exclamation mark or question mark". We count
    # how many there are, but never return fewer than 1 (to avoid dividing by 0).
    sentences = re.findall(r"[.!?]+", text)
    return max(len(sentences), 1)
 
 
def _count_characters(word):
    """Count the letters in a word, skipping apostrophes (so "don't" is 4)."""
    return len(word.replace("'", ""))
