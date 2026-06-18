"""
FIFA World Cup 2026 Prediction Platform - Main Application
"""
import os
import logging
import streamlit as st
from pathlib import Path
from src.config import Config
from src.storage import Storage
from src.scheduler import start_background_tasks

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="World Cup 2026 Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize config and storage
config = Config()
storage = Storage(config)
storage.initialize_data_layer()

# Start background scheduler (runs once per session)
if 'scheduler_started' not in st.session_state:
    start_background_tasks()
    st.session_state.scheduler_started = True

# Session state initialization
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF6B6B;
    }
    .prediction-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #4ECDC4;
    }
    .match-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .leaderboard-header {
        background-color: #1f77b4;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Authentication
st.sidebar.title("⚽ World Cup 2026")
st.sidebar.markdown("---")

if st.session_state.user_id is None:
    st.sidebar.subheader("Login / Register")
    username = st.sidebar.text_input("Username", key="login_username", placeholder="Enter your username")
    
    if st.sidebar.button("Enter Tournament", use_container_width=True, type="primary"):
        if username.strip():
            user = storage.get_or_create_user(username)
            st.session_state.user_id = user['user_id']
            st.session_state.user_name = user['user_name']
            st.success(f"Welcome, {username}! 🎉")
            st.rerun()
        else:
            st.sidebar.error("Please enter a username")
else:
    st.sidebar.success(f"Logged in as: **{st.session_state.user_name}**")
    
    # User stats in sidebar
    user_predictions = storage.get_user_prediction_count(st.session_state.user_id)
    user_correct = storage.get_user_correct_predictions(st.session_state.user_id)
    user_points = storage.get_user_total_points(st.session_state.user_id)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Predictions", user_predictions)
        st.metric("Correct", user_correct)
    with col2:
        accuracy = (user_correct / user_predictions * 100) if user_predictions > 0 else 0
        st.metric("Accuracy", f"{accuracy:.1f}%")
        st.metric("Points", user_points)
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("FIFA World Cup 2026 Prediction Platform | v1.0")

# Main page routing
if st.session_state.user_id is None:
    st.info("👈 Please log in using the sidebar to begin")
    st.markdown("""
    # Welcome to World Cup 2026 Predictor ⚽
    
    Predict match outcomes, compete on the leaderboard, and test your football knowledge!
    
    ## How It Works:
    
    1. **Login**: Enter your username to register
    2. **Predict**: Make predictions on upcoming matches
    3. **Track**: View your prediction history and accuracy
    4. **Compete**: Climb the global leaderboard
    
    ## Scoring System:
    - **Correct Winner**: +3 points
    - **Correct Draw**: +2 points
    - **Wrong Prediction**: 0 points
    
    ## Tournament Details:
    - **Event**: FIFA World Cup 2026
    - **Location**: USA, Canada, Mexico
    - **Dates**: June - July 2026
    - **Teams**: 32 teams
    
    Good luck! 🍀
    """)
else:
    # Pages are automatically loaded from the pages/ directory
    pass
