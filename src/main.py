import streamlit as st

# Define pages
chat_page = st.Page("chat.py", title="Chat", icon="💬")
stats_page = st.Page("stats.py", title="Stats", icon="📊")
help_page = st.Page("help.py", title="Help", icon="❓")

# Set up navigation
pages = st.navigation([chat_page, stats_page, help_page], position="top")

# Run the selected page
pages.run()
