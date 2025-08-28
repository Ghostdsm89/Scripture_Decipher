import streamlit as st
import sqlite3
from data import get_books, get_chapters, get_verses, get_verse_text, get_simplified_example

# Set up the page
st.set_page_config(
    page_title="Scripture Decipher",
    page_icon="📖",
    layout="wide"
)

# Initialize database
def init_db():
    conn = sqlite3.connect('scripture_decipher.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS simplified_verses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  book TEXT NOT NULL,
                  chapter INTEGER NOT NULL,
                  verse INTEGER NOT NULL,
                  original_text TEXT NOT NULL,
                  simplified_text TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Add a new simplified verse to the database
def add_simplified_verse(book, chapter, verse, original_text, simplified_text):
    conn = sqlite3.connect('scripture_decipher.db')
    c = conn.cursor()
    c.execute("INSERT INTO simplified_verses (book, chapter, verse, original_text, simplified_text) VALUES (?, ?, ?, ?, ?)",
              (book, chapter, verse, original_text, simplified_text))
    conn.commit()
    conn.close()

# Get all simplified verses from the database
def get_all_simplified_verses():
    conn = sqlite3.connect('scripture_decipher.db')
    c = conn.cursor()
    c.execute("SELECT * FROM simplified_verses ORDER BY created_at DESC")
    verses = c.fetchall()
    conn.close()
    return verses

# Delete a simplified verse from the database
def delete_simplified_verse(verse_id):
    conn = sqlite3.connect('scripture_decipher.db')
    c = conn.cursor()
    c.execute("DELETE FROM simplified_verses WHERE id = ?", (verse_id,))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Minimal CSS for custom components only
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #2c5c2c;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #3a6349;
        border-bottom: 3px solid #4a7c59;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    .scripture-box {
        background-color: #f0f7f0;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #4a7c59;
        color: #2c5c2c;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .simplified-box {
        background-color: #e8f4f8;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #5c8da5;
        color: #2c3e50;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border: 1px solid #c3e6cb;
        font-weight: 500;
    }
    .warning-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
        border: 1px solid #f5c6cb;
        font-weight: 500;
    }
    .delete-btn {
        background-color: #dc3545 !important;
        color: white !important;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 0.9rem;
        margin-top: 10px;
    }
    .delete-btn:hover {
        background-color: #c82333 !important;
        transform: translateY(-1px);
    }
    .footer {
        text-align: center;
        color: #6c757d;
        padding: 20px;
        margin-top: 30px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<h1 class="main-header">📖 Scripture Decipher</h1>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <p style="font-size: 1.2rem;">Making Bible scriptures easier to understand for everyone</p>
</div>
""", unsafe_allow_html=True)

# Create tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Simplify Scripture", "View Saved Verses", "About"])

with tab1:
    st.markdown('<h2 class="sub-header">Simplify a Bible Verse</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Book selection using the module
        books = get_books()
        selected_book = st.selectbox("Select Book", books)
        
        # Chapter selection based on book
        if selected_book:
            chapters = get_chapters(selected_book)
            selected_chapter = st.selectbox("Select Chapter", chapters)
        
        # Verse selection based on chapter
        if selected_chapter:
            verses = get_verses(selected_book, selected_chapter)
            selected_verse = st.selectbox("Select Verse", verses)
    
    with col2:
        # Display original verse using the module
        if selected_book and selected_chapter and selected_verse:
            original_text = get_verse_text(selected_book, selected_chapter, selected_verse)
            if original_text:
                st.markdown("### Original Scripture")
                st.markdown(f'<div class="scripture-box">{selected_book} {selected_chapter}:{selected_verse} - "{original_text}"</div>', unsafe_allow_html=True)
                
                # Input for simplified version
                simplified_text = st.text_area(
                    "Simplified Version",
                    placeholder="Enter your simplified version of this verse here...",
                    height=150
                )
                
                # Get sample simplification using the module
                sample_simplification = get_simplified_example(selected_book, selected_chapter, selected_verse)
                if sample_simplification:
                    with st.expander("See example simplification"):
                        st.info(sample_simplification)
                
                # Save button
                if st.button("Save Simplified Verse") and simplified_text:
                    add_simplified_verse(
                        selected_book, selected_chapter, selected_verse,
                        original_text, simplified_text
                    )
                    st.markdown('<div class="success-box">Simplified verse saved successfully!</div>', unsafe_allow_html=True)
                    st.rerun()

with tab2:
    st.markdown('<h2 class="sub-header">Saved Simplified Verses</h2>', unsafe_allow_html=True)
    
    # Get all saved verses from database
    saved_verses = get_all_simplified_verses()
    
    if not saved_verses:
        st.info("No simplified verses saved yet. Use the 'Simplify Scripture' tab to get started.")
    else:
        # Get unique books for filtering
        unique_books = sorted(list(set(verse[1] for verse in saved_verses)))
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_book = st.selectbox("Filter by Book", ["All"] + unique_books, key="filter_book")
        with col2:
            sort_order = st.selectbox("Sort Order", ["Newest First", "Oldest First"])
        with col3:
            items_per_page = st.selectbox("Items per page", [5, 10, 20], index=0)
        
        # Filter and sort verses
        filtered_verses = saved_verses
        if filter_book != "All":
            filtered_verses = [v for v in saved_verses if v[1] == filter_book]
        
        if sort_order == "Oldest First":
            filtered_verses = sorted(filtered_verses, key=lambda x: x[6])
        else:
            filtered_verses = sorted(filtered_verses, key=lambda x: x[6], reverse=True)
        
        # Pagination
        total_verses = len(filtered_verses)
        if total_verses > 0:
            total_pages = (total_verses - 1) // items_per_page + 1
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
            start_idx = (page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_verses)
            
            st.write(f"Showing {start_idx + 1}-{end_idx} of {total_verses} verse{'s' if total_verses != 1 else ''}")
            
            # Display verses for current page
            for verse in filtered_verses[start_idx:end_idx]:
                verse_id, book, chapter, verse_num, original_text, simplified_text, created_at = verse
                
                with st.expander(f"{book} {chapter}:{verse_num} - {created_at.split()[0]}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Original:**")
                        st.markdown(f'<div class="scripture-box">{original_text}</div>', unsafe_allow_html=True)
                    with col2:
                        st.write("**Simplified:**")
                        st.markdown(f'<div class="simplified-box">{simplified_text}</div>', unsafe_allow_html=True)
                    
                    # Delete button with confirmation
                    st.markdown("---")
                    if st.button("🗑️ Delete This Verse", key=f"delete_{verse_id}", use_container_width=True, 
                                type="secondary", help="Permanently delete this simplified verse"):
                        # Use a unique key for the confirmation dialog
                        if st.session_state.get(f"confirm_delete_{verse_id}", False):
                            delete_simplified_verse(verse_id)
                            st.markdown('<div class="warning-box">Verse deleted successfully!</div>', unsafe_allow_html=True)
                            st.rerun()
                        else:
                            st.session_state[f"confirm_delete_{verse_id}"] = True
                            st.warning("Are you sure you want to delete this verse? This action cannot be undone.")
                            if st.button("✅ Yes, Delete Permanently", key=f"confirm_{verse_id}", use_container_width=True):
                                delete_simplified_verse(verse_id)
                                st.markdown('<div class="warning-box">Verse deleted successfully!</div>', unsafe_allow_html=True)
                                st.rerun()
                            if st.button("❌ Cancel", key=f"cancel_{verse_id}", use_container_width=True):
                                st.session_state[f"confirm_delete_{verse_id}"] = False
                                st.rerun()
        
        # Statistics
        st.markdown("---")
        st.subheader("Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Verses Simplified", total_verses)
        
        with col2:
            if total_verses > 0:
                books_count = {}
                for verse in saved_verses:
                    book = verse[1]
                    books_count[book] = books_count.get(book, 0) + 1
                most_common_book = max(books_count, key=books_count.get)
                st.metric("Most Common Book", most_common_book)
        
        with col3:
            if total_verses > 0:
                earliest = min([verse[6] for verse in saved_verses])
                st.metric("First Simplification", earliest.split()[0])

with tab3:
    st.markdown('<h2 class="sub-header">About Scripture Decipher</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="scripture-box">
    <h3>Our Mission</h3>
    <p>Scripture Decipher is designed to make the Bible more accessible and understandable for people of all backgrounds and reading levels. We believe that everyone should be able to engage with God's Word in a way that resonates with them.</p>
    
    <h3>Now with Expanded Scriptures!</h3>
    <p>We've expanded our library to include verses from across the entire Bible. You can now find and simplify passages from:</p>
    <ul>
        <li>Old Testament: Genesis, Exodus, Psalms, Proverbs, Isaiah</li>
        <li>New Testament: Matthew, John, Romans, Philippians, Hebrews, James, 1 John</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### How It Works
        1. Select a book, chapter, and verse from our expanded library
        2. Read the original text
        3. Create your simplified version that's easier to understand
        4. Save it to your personal database
        5. Review all your simplified verses anytime
        """)
    
    with col2:
        st.markdown("""
        ### Benefits
        - Helps with personal Bible study and devotionals
        - Useful for teaching, sermons, and small groups
        - Creates a personal repository of understood scriptures
        - Great for new believers, children, or those new to the Bible
        - Perfect for ESL readers or those with reading difficulties
        """)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center;">
        <p>Created with ❤️ for the Hugging Face community</p>
        <p><small>Now featuring an expanded scripture library with easy-to-manage data modules</small></p>
    </div>
    """, unsafe_allow_html=True)

# Add footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Scripture Decipher • Making the Bible accessible to all</p>
    <p><small>Expanded scripture library now available</small></p>
</div>
""", unsafe_allow_html=True)
