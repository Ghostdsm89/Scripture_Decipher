import json
import streamlit as st

# Load Bible data from JSON file
@st.cache_data
def load_bible_data():
    try:
        with open('bible_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            st.success("Bible data loaded successfully!")
            return data
    except FileNotFoundError:
        st.error("Bible data file not found. Using fallback data.")
        return get_fallback_data()
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON file: {e}. Using fallback data.")
        return get_fallback_data()
    except Exception as e:
        st.error(f"Unexpected error loading Bible data: {e}. Using fallback data.")
        return get_fallback_data()

def get_fallback_data():
    """Minimal fallback data if JSON file is missing or invalid"""
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
            },
            "John": {
                "chapters": {
                    "3": {
                        "verses": {
                            "16": {
                                "text": "For God so loved the world, that he gave his only Son, that whoever believes in him should not perish but have eternal life.",
                                "simplified_example": "God loved people so much that He sent His only Son Jesus. Anyone who believes in Him will live forever with God."
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
    return ["Genesis", "John"]  # Fallback books

def get_chapters(book):
    """Return sorted list of available chapters for a given book"""
    try:
        if book in BIBLE_DATA.get("books", {}):
            chapters = BIBLE_DATA["books"][book]["chapters"]
            return sorted([int(chap) for chap in chapters.keys()])
        return []  # Return empty list if book not found
    except KeyError:
        return []  # Return empty list if any key is missing

def get_verses(book, chapter):
    """Return sorted list of available verses for a given book and chapter"""
    try:
        if (book in BIBLE_DATA.get("books", {}) and 
            str(chapter) in BIBLE_DATA["books"][book]["chapters"]):
            verses = BIBLE_DATA["books"][book]["chapters"][str(chapter)]["verses"]
            return sorted([int(verse) for verse in verses.keys()])
        return []  # Return empty list if book or chapter not found
    except KeyError:
        return []  # Return empty list if any key is missing

def get_verse_text(book, chapter, verse):
    """Return the original text for a specific verse"""
    try:
        if (book in BIBLE_DATA.get("books", {}) and 
            str(chapter) in BIBLE_DATA["books"][book]["chapters"] and
            str(verse) in BIBLE_DATA["books"][book]["chapters"][str(chapter)]["verses"]):
            return BIBLE_DATA["books"][book]["chapters"][str(chapter)]["verses"][str(verse)]["text"]
        return None  # Return None if verse not found
    except KeyError:
        return None  # Return None if any key is missing

def get_simplified_example(book, chapter, verse):
    """Return a sample simplification for a verse if available"""
    try:
        if (book in BIBLE_DATA.get("books", {}) and 
            str(chapter) in BIBLE_DATA["books"][book]["chapters"] and
            str(verse) in BIBLE_DATA["books"][book]["chapters"][str(chapter)]["verses"]):
            return BIBLE_DATA["books"][book]["chapters"][str(chapter)]["verses"][str(verse)].get("simplified_example")
        return None  # Return None if verse not found
    except KeyError:
        return None  # Return None if any key is missing
