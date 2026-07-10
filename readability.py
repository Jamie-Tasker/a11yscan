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
 
