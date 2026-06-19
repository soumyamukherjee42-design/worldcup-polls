"""
FIFA World Cup 2026 Prediction Platform - Main Application
Enhanced Design Version
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

# FIFA World Cup 2026 Custom CSS - Enhanced Design
st.markdown("""
<style>
    /* Main color scheme - FIFA 2026 inspired */
    :root {
        --primary-color: #1a472a;  /* Dark green */
        --secondary-color: #ffb81c; /* Gold */
        --accent-color: #e53238;   /* Red */
        --light-bg: #f5f5f5;
        --card-bg: #ffffff;
    }
    
    /* Main container */
    .main {
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a472a 0%, #2d5a3d 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffb81c;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Header styling */
    h1, h2 {
        color: #1a472a;
        text-shadow: 1px 1px 1px rgba(0,0,0,0.1);
        border-bottom: 3px solid #ffb81c;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #1a472a;
        border-left: 4px solid #e53238;
        padding-left: 0.8rem;
    }
    
    /* Card styles */
    .metric-card {
        background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 100%);
        color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.8rem;
        border: 2px solid #ffb81c;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        padding: 1.2rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        border-left: 5px solid #e53238;
        border-right: 2px solid #ffb81c;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .prediction-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    .match-card {
        background: linear-gradient(to right, #ffffff 0%, #fafafa 100%);
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        border: 2px solid #e0e0e0;
        border-left: 4px solid #ffb81c;
        box-shadow: 0 3px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .match-card:hover {
        border-color: #ffb81c;
        box-shadow: 0 6px 20px rgba(255, 184, 28, 0.15);
        transform: translateX(4px);
    }
    
    /* Leaderboard header */
    .leaderboard-header {
        background: linear-gradient(135deg, #1a472a 0%, #e53238 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .leaderboard-header h2 {
        color: #ffb81c;
        border: none;
        margin: 0;
        font-size: 1.8rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #ffb81c 0%, #ffa500 100%);
        color: #1a472a;
        border: none;
        border-radius: 0.6rem;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Metrics styling */
    .stMetric {
        background: #ffffff;
        padding: 1.2rem;
        border-radius: 0.8rem;
        border: 1px solid #ffb81c;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .stMetric > div:first-child {
        color: #1a472a;
        font-weight: 600;
    }
    
    .stMetric > div:last-child {
        color: #e53238;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Table styling */
    .stDataFrame {
        border-radius: 0.8rem;
        overflow: hidden;
    }
    
    .stDataFrame table {
        font-size: 0.95rem;
    }
    
    [data-testid="stDataFrame"] thead {
        background: linear-gradient(90deg, #1a472a 0%, #2d5a3d 100%);
        color: #ffb81c;
        font-weight: 600;
    }
    
    [data-testid="stDataFrame"] tbody tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    
    [data-testid="stDataFrame"] tbody tr:hover {
        background-color: #fff3e0;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 0.8rem;
        border-left: 4px solid #ffb81c;
    }
    
    .stSuccess {
        background-color: #e8f5e9;
        border-left-color: #4caf50;
    }
    
    .stWarning {
        background-color: #fff3e0;
        border-left-color: #ffb81c;
    }
    
    .stError {
        background-color: #ffebee;
        border-left-color: #e53238;
    }
    
    .stInfo {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    
    /* Selectbox and inputs */
    .stSelectbox,
    .stTextInput,
    .stSlider {
        border-radius: 0.6rem;
    }
    
    .stSelectbox > div > div {
        border: 2px solid #ffb81c;
        border-radius: 0.6rem;
    }
    
    /* Divider */
    hr {
        border: 1px solid #ffb81c;
        margin: 2rem 0;
    }
    
    /* Column styling */
    .stColumn {
        background-color: transparent;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 3px solid #ffb81c;
    }
    
    .stTabs [aria-selected="true"] {
        color: #e53238 !important;
        border-bottom: 3px solid #e53238 !important;
    }
    
    /* Checkbox styling */
    .stCheckbox label {
        color: #1a472a;
        font-weight: 500;
    }
    
    /* Radio button styling */
    .stRadio label {
        color: #1a472a;
        font-weight: 500;
    }
    
    /* Custom team colors */
    .team-badge {
        background: linear-gradient(135deg, #e53238 0%, #ffb81c 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem;
    }
    
    /* Responsive improvements */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem 1rem;
        }
        
        h1, h2 {
            font-size: 1.5rem;
        }
        
        .metric-card {
            margin-bottom: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Authentication with Enhanced Design
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin: 1rem 0;">
        <h1 style="font-size: 2.5rem; margin: 0;">⚽</h1>
        <h2 style="color: #ffb81c; font-size: 1.5rem; margin: 0.5rem 0;">WORLD CUP</h2>
        <h3 style="color: #e53238; font-size: 1.3rem; margin: 0; border: none;">2026</h3>
        <p style="color: #ffffff; font-size: 0.9rem; margin-top: 0.5rem;">Predictor</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

if st.session_state.user_id is None:
    st.sidebar.subheader("🎬 Enter Tournament")
    username = st.sidebar.text_input(
        "Username", 
        key="login_username", 
        placeholder="Enter your username",
        help="Create your profile to start predicting"
    )
    
    if st.sidebar.button("⚡ Join Now", use_container_width=True, type="primary"):
        if username.strip():
            user = storage.get_or_create_user(username)
            st.session_state.user_id = user['user_id']
            st.session_state.user_name = user['user_name']
            st.success(f"🎉 Welcome to the tournament, {username}!")
            st.rerun()
        else:
            st.sidebar.error("Please enter a username")
else:
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, #ffb81c 0%, #e53238 100%); 
                padding: 1rem; border-radius: 0.8rem; text-align: center; 
                margin-bottom: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
        <p style="color: #1a472a; font-size: 0.9rem; margin: 0; font-weight: 600;">
            ✅ LOGGED IN
        </p>
        <p style="color: #1a472a; font-size: 1.2rem; margin: 0.5rem 0; font-weight: 700;">
            {st.session_state.user_name}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # User stats in sidebar
    user_predictions = storage.get_user_prediction_count(st.session_state.user_id)
    user_correct = storage.get_user_correct_predictions(st.session_state.user_id)
    user_points = storage.get_user_total_points(st.session_state.user_id)
    
    st.sidebar.subheader("📊 Your Stats")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("🎯 Predictions", user_predictions)
        st.metric("⭐ Points", user_points)
    with col2:
        accuracy = (user_correct / user_predictions * 100) if user_predictions > 0 else 0
        st.metric("✅ Correct", user_correct)
        st.metric("📈 Accuracy", f"{accuracy:.1f}%")
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("""
<p style="text-align: center; color: #ffb81c; font-size: 0.75rem; margin-top: 2rem;">
    ⚽ FIFA World Cup 2026 Prediction Platform<br>
    <span style="color: #ffffff;">v1.0 | Powered by Data</span>
</p>
""", unsafe_allow_html=True)

# Main page routing
if st.session_state.user_id is None:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h1 style="font-size: 3rem; margin: 0;">⚽ WORLD CUP 2026</h1>
            <h2 style="color: #e53238; margin: 1rem 0;">PREDICTION PLATFORM</h2>
            <p style="font-size: 1.1rem; color: #666;">
                Join millions of football fans and predict the future of the FIFA World Cup 2026!
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; font-size: 4rem;">
            ⚽🇺🇸🇨🇦🇲🇽
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a472a 0%, #2d5a3d 100%); 
                    padding: 1.5rem; border-radius: 0.8rem; text-align: center;
                    border: 2px solid #ffb81c; color: white;">
            <h3 style="color: #ffb81c; border: none; margin-top: 0;">🎯 PREDICT</h3>
            <p>Make predictions on all 64 matches of the tournament</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e53238 0%, #c41e3a 100%); 
                    padding: 1.5rem; border-radius: 0.8rem; text-align: center;
                    border: 2px solid #ffb81c; color: white;">
            <h3 style="color: #ffb81c; border: none; margin-top: 0;">🏆 COMPETE</h3>
            <p>Compete on global leaderboard with other fans</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffb81c 0%, #ffa500 100%); 
                    padding: 1.5rem; border-radius: 0.8rem; text-align: center;
                    border: 2px solid #1a472a; color: #1a472a;">
            <h3 style="color: #1a472a; border: none; margin-top: 0;">⭐ WIN</h3>
            <p>Earn points and climb the rankings</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📋 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Login
        👤 Create your account with just a username
        """)
    
    with col2:
        st.markdown("""
        #### 2️⃣ Predict
        🎯 Forecast match outcomes before kickoff
        """)
    
    with col3:
        st.markdown("""
        #### 3️⃣ Score
        ⭐ Earn points for correct predictions
        """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Scoring Rules")
        st.markdown("""
        - **Correct Winner**: `+3 points` 🟢
        - **Correct Draw**: `+2 points` 🟡
        - **Wrong**: `0 points` 🔴
        """)
    
    with col2:
        st.subheader("📅 Tournament Info")
        st.markdown("""
        - **Event**: FIFA World Cup 2026
        - **Hosts**: 🇺🇸 USA, 🇨🇦 Canada, 🇲🇽 Mexico
        - **Teams**: 32 nations
        - **Matches**: 64 games
        """)
    
    st.markdown("---")
    
    st.info("👈 **Click \"Join Now\" in the sidebar to start predicting!**")
else:
    # Pages are automatically loaded from the pages/ directory
    pass
