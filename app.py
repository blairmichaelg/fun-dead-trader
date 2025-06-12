import streamlit as st
import sys
import os

# Add the parent directory of trader_companion_app to the Python path
# This is necessary for Streamlit to correctly import modules within the project structure
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

st.set_page_config(
    page_title="Trader Companion MVP",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("👋 Welcome to Your Trader Companion!")
st.markdown(
    """
    This is the Minimum Viable Product (MVP) for your Trader Companion app.
    Use the sidebar to navigate to different tools.
    """
)
