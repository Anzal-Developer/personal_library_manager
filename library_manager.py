import streamlit as st
import json
import os

# File to save/load library
LIBRARY_FILE = "library.txt"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Add a book to the library
def add_book(library):
    st.subheader("📖 Add a Book")
    with st.form(key="add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", min_value=0, max_value=9999, step=1)
        genre = st.text_input("Genre")
        read_status = st.checkbox("Have you read this book?")
        submit = st.form_submit_button("Add Book ✅")

        if submit and title and author and genre:
            book = {
                "title": title,
                "author": author,
                "year": int(year),
                "genre": genre,
                "read": read_status
            }
            library.append(book)
            st.success(f"✅ '{title}' added successfully!")
            return True
    return False

# Remove a book from the library
def remove_book(library):
    st.subheader("🗑️ Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book ❌"):
        for book in library[:]:
            if book["title"].lower() == title.lower():
                library.remove(book)
                st.success(f"✅ '{title}' removed successfully!")
                return True
        st.error(f"❌ '{title}' not found in library.")
    return False

# Search for a book
def search_book(library):
    st.subheader("🔍 Search for a Book")
    search_by = st.radio("Search by:", ("Title", "Author"))
    search_term = st.text_input(f"Enter the {search_by.lower()} to search")
    
    if search_term:
        if search_by == "Title":
            matches = [book for book in library if search_term.lower() in book["title"].lower()]
        else:
            matches = [book for book in library if search_term.lower() in book["author"].lower()]
        
        if matches:
            st.write("Matching Books:")
            for i, book in enumerate(matches, 1):
                status = "Read" if book["read"] else "Unread"
                st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            st.warning("❌ No matches found.")

# Display all books
def display_books(library):
    st.subheader("📚 Your Library")
    if not library:
        st.info("📖 Your library is empty!")
        return
    for i, book in enumerate(library, 1):
        status = "Read" if book["read"] else "Unread"
        st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

# Display statistics
def display_stats(library):
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    if total_books == 0:
        st.info("📊 Library is empty. No stats to show!")
        return
    read_books = sum(1 for book in library if book["read"])
    percentage_read = (read_books / total_books) * 100
    st.write(f"📚 Total books: {total_books}")
    st.write(f"📈 Percentage read: {percentage_read:.1f}%")
    st.progress(int(percentage_read))  # Progress bar for visual appeal

# Main Streamlit app
def main():
    st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="wide")
    
    # Header
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📚 Personal Library Manager</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Manage your book collection with ease! ✨</p>", unsafe_allow_html=True)

    # Initialize session state for library
    if " library" not in st.session_state:
        st.session_state.library = load_library()

    # Sidebar menu
    menu = st.sidebar.selectbox(
        "Menu",
        ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"],
        format_func=lambda x: f"➡️ {x}"
    )

    # Handle menu options
    if menu == "Add a Book":
        if add_book(st.session_state.library):
            save_library(st.session_state.library)
    elif menu == "Remove a Book":
        if remove_book(st.session_state.library):
            save_library(st.session_state.library)
    elif menu == "Search for a Book":
        search_book(st.session_state.library)
    elif menu == "Display All Books":
        display_books(st.session_state.library)
    elif menu == "Display Statistics":
        display_stats(st.session_state.library)

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: grey;'>Built with Streamlit ❤️ | © 2025</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()