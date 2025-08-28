import json
import streamlit as st

# Load Bible data from JSON file
@st.cache_data
def load_bible_data():
    try:
        with open('bible_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Bible data file not found. Using minimal sample data.")
        return get_fallback_data()

def get_fallback_data():
    """Fallback data if JSON file is missing - keep this minimal"""
    return {
        "books": {
            "Genesis": {
                "chapters": {
                    "1": {
                        "verses": {
                            "1": {
                                "text": "In the beginning, God created the heavens and the earth.",
                                "simplified_example": "Before anything else existed, God made the entire universe."
                            }
                        }
                    }
                }
            }
        }
    }

# Load the data once
BIBLE_DATA = load_bible_data()

def get_books():
    """Return sorted list of available books"""
    if "books" in BIBLE_DATA:
        return sorted(BIBLE_DATA["books"].keys())
    return []

def get_chapters(book):
    """Return sorted list of available chapters for a given book"""
    if book in BIBLE_DATA.get("books", {}):
        chapters = BIBLE_DATA["books"][book]["chapters"]
        return sorted([int(chap) for chap in chapters.keys()])
    return []

def get_verses(book, chapter):
    """Return sorted list of available verses for a given book and chapter"""
    if (book in BIBLE_DATA.get("books", {}) and 
        str(chapter) in BIBLE_DATA["books"][book]["chapters"]):
        verses = BIBLE_DATA["books"][book]["chapters"][str(chapter)]["verses"]
        return sorted([int(verse) for verse in verses.keys()])
    return []

def get_verse_text(book, chapter, verse):
    """Return the original text for a specific verse"""
    if (book in BIBLE_DATA.get("books", {}) and 
        str(chapter) in BIBLE_DATA["books"][book]["chapters"] and
        str(verse) in BIBLE_DATA["books"][book]["chapters"][str(chapter)]["verses"]):
        return BIBLE_DATA["books"][book]["chapters"][str(chapter)]["verses"][str(verse)]["text"]
    return None

def get_simplified_example(book, chapter, verse):
    """Return a sample simplification for a verse if available"""
    if (book in BIBLE_DATA.get("books", {}) and 
        str(chapter) in BIBLE_DATA["books"][book]["chapters"] and
        str(verse) in BIBLE_DATA["books"][book]["chapters"][str(chapter)]["verses"]):
        return BIBLE_DATA["books"][book]["chapters"][str(chapter)]["verses"][str(verse)].get("simplified_example")
    return None
