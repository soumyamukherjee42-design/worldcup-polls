"""
Reusable UI components with premium FIFA World Cup 2026 styling
"""
import streamlit as st
from typing import Optional, List, Dict, Any
import time


def inject_global_css() -> None:
    """Inject global CSS styling."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #081B33 0%, #0a2847 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #081B33 0%, #0a2847 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #081B33 0%, #0f3a52 100%);
        border-right: 1px solid rgba(0, 88, 184, 0.2);
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    h1 {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #0057B8 0%, #00C896 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    h2 {
        font-size: 2.2rem;
        color: #ffffff;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    
    h3 {
        font-size: 1.5rem;
        color: #ffffff;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    body, p, span {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0057B8 0%, #00C896 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        padding: 0.75rem 2rem;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 24px rgba(0, 88, 184, 0.25);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(0, 88, 184, 0.35);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(0, 88, 184, 0.3);
        color: white;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        background: rgba(255, 255, 255, 0.12);
        border-color: #0057B8;
        box-shadow: 0 0 0 3px rgba(0, 88, 184, 0.1);
    }
    
    /* Dividers */
    hr, [data-testid="stHorizontalBlock"] {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 200, 150, 0.3), transparent);
        margin: 2rem 0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border-bottom: 2px solid rgba(0, 88, 184, 0.2);
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.6);
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        padding: 1rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #00C896;
        border-bottom: 3px solid #00C896;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.1) 0%, rgba(0, 200, 150, 0.05) 100%);
        border: 1px solid rgba(0, 88, 184, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.15) 0%, rgba(0, 200, 150, 0.1) 100%);
        border-color: rgba(0, 200, 150, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 88, 184, 0.15);
    }
    
    /* Tables */
    .stDataFrame {
        background: transparent;
    }
    
    [data-testid="stDataFrameContainer"] {
        background: transparent;
    }
    
    .dataframe {
        background: transparent !important;
        border: 1px solid rgba(0, 88, 184, 0.2) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    
    .dataframe thead {
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.2) 0%, rgba(0, 200, 150, 0.1) 100%);
        border-bottom: 2px solid rgba(0, 88, 184, 0.3);
    }
    
    .dataframe th {
        color: #00C896 !important;
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        padding: 1rem !important;
    }
    
    .dataframe td {
        color: #ffffff !important;
        padding: 0.75rem 1rem !important;
        border-bottom: 1px solid rgba(0, 88, 184, 0.1) !important;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(0, 88, 184, 0.08) !important;
    }
    
    /* Alerts */
    .stAlert {
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.1) 0%, rgba(0, 200, 150, 0.05) 100%);
        border: 1px solid rgba(0, 88, 184, 0.3);
        border-radius: 10px;
        padding: 1rem 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stAlertContainer"] {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Sidebar */
    .sidebar-content {
        padding: 1.5rem;
    }
    
    [data-testid="stSidebarContent"] {
        padding: 2rem 1.5rem;
    }
    
    /* Main content */
    [data-testid="stMainBlockContainer"] {
        padding: 2rem 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 88, 184, 0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #0057B8, #00C896);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #0064d4, #00e8a8);
    }
    
    /* Custom classes */
    .glass-container {
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.1) 0%, rgba(0, 200, 150, 0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 88, 184, 0.2);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-container:hover {
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.15) 0%, rgba(0, 200, 150, 0.1) 100%);
        border-color: rgba(0, 200, 150, 0.4);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 88, 184, 0.2);
    }
    
    .hero-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 3.5rem;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #0057B8 0%, #00C896 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    .match-card {
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.12) 0%, rgba(0, 200, 150, 0.06) 100%);
        border: 1px solid rgba(0, 88, 184, 0.25);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .match-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 200, 150, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .match-card:hover {
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.18) 0%, rgba(0, 200, 150, 0.12) 100%);
        border-color: rgba(0, 200, 150, 0.5);
        transform: translateY(-6px);
        box-shadow: 0 16px 40px rgba(0, 88, 184, 0.25);
    }
    
    .match-card:hover::before {
        left: 100%;
    }
    
    .team-name {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
    }
    
    .vs-divider {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        color: #00C896;
        text-align: center;
        margin: 1rem 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .prediction-button {
        background: linear-gradient(135deg, #0057B8 0%, #00C896 100%);
        border: none;
        border-radius: 10px;
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .prediction-button:hover:not(:disabled) {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 88, 184, 0.4);
    }
    
    .prediction-button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    .leaderboard-podium {
        display: flex;
        justify-content: center;
        align-items: flex-end;
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .podium-place {
        text-align: center;
        border-radius: 12px;
        padding: 1.5rem 1rem;
        flex: 1;
        max-width: 200px;
        transition: all 0.3s ease;
    }
    
    .podium-place:hover {
        transform: translateY(-8px);
    }
    
    .podium-gold {
        background: linear-gradient(135deg, rgba(255, 193, 7, 0.2) 0%, rgba(255, 152, 0, 0.15) 100%);
        border: 2px solid rgba(255, 193, 7, 0.5);
        order: 2;
        transform: scale(1.1);
    }
    
    .podium-silver {
        background: linear-gradient(135deg, rgba(192, 192, 192, 0.2) 0%, rgba(169, 169, 169, 0.15) 100%);
        border: 2px solid rgba(192, 192, 192, 0.5);
        order: 1;
        height: 80%;
    }
    
    .podium-bronze {
        background: linear-gradient(135deg, rgba(205, 127, 50, 0.2) 0%, rgba(184, 115, 51, 0.15) 100%);
        border: 2px solid rgba(205, 127, 50, 0.5);
        order: 3;
        height: 60%;
    }
    
    .medal {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .rank-number {
        font-family: 'Montserrat', sans-serif;
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #0057B8 0%, #00C896 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .stat-badge {
        display: inline-block;
        background: rgba(0, 200, 150, 0.2);
        border: 1px solid rgba(0, 200, 150, 0.5);
        border-radius: 20px;
        padding: 0.4rem 1rem;
        font-size: 0.8rem;
        font-weight: 600;
        color: #00C896;
        margin: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .countdown-timer {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.9rem;
        font-weight: 700;
        color: #FF6B6B;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .admin-card {
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.12) 0%, rgba(0, 200, 150, 0.06) 100%);
        border: 2px solid rgba(0, 88, 184, 0.25);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .admin-card:hover {
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.18) 0%, rgba(0, 200, 150, 0.12) 100%);
        border-color: rgba(0, 200, 150, 0.5);
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(0, 88, 184, 0.2);
    }
    
    .admin-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .admin-label {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .timeline-item {
        padding: 1.5rem;
        border-left: 3px solid rgba(0, 200, 150, 0.5);
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.08) 0%, rgba(0, 200, 150, 0.03) 100%);
        border-radius: 0 8px 8px 0;
    }
    
    .timeline-item.correct {
        border-left-color: #00C896;
        background: linear-gradient(135deg, rgba(0, 200, 150, 0.12) 0%, rgba(0, 200, 150, 0.05) 100%);
    }
    
    .timeline-item.incorrect {
        border-left-color: #FF6B6B;
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.12) 0%, rgba(255, 107, 107, 0.05) 100%);
    }
    
    .timeline-item.pending {
        border-left-color: rgba(0, 88, 184, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)


def hero_section(title: str, subtitle: str, cta_text: str = "", on_cta_click=None) -> None:
    """Create a premium hero section."""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f'<div class="hero-title">{title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-subtitle">{subtitle}</div>', unsafe_allow_html=True)
        
        if cta_text:
            col_btn, _ = st.columns([1, 2])
            with col_btn:
                if st.button(cta_text, key=f"cta_{int(time.time())}", use_container_width=True):
                    if on_cta_click:
                        on_cta_click()
    
    with col2:
        st.markdown("""
        <div style="
            height: 400px;
            background: linear-gradient(135deg, rgba(0, 88, 184, 0.1) 0%, rgba(0, 200, 150, 0.05) 100%);
            border-radius: 20px;
            border: 2px solid rgba(0, 88, 184, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 80px;
            animation: float 3s ease-in-out infinite;
        " style="animation: float 3s ease-in-out infinite;">
            ⚽
        </div>
        <style>
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        </style>
        """, unsafe_allow_html=True)


def metric_card(label: str, value: str, change: Optional[str] = None) -> None:
    """Create a glass-morphism metric card."""
    st.markdown(f"""
    <div class="glass-container" style="text-align: center; padding: 1.5rem;">
        <div style="
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.7);
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        ">{label}</div>
        <div style="
            font-size: 2.2rem;
            font-weight: 900;
            color: #ffffff;
            font-family: 'Montserrat', sans-serif;
            margin-bottom: 0.5rem;
        ">{value}</div>
        {f'<div style="color: #00C896; font-size: 0.85rem; font-weight: 600;">{change}</div>' if change else ''}
    </div>
    """, unsafe_allow_html=True)


def match_card(team_1: str, team_2: str, date_str: str, venue: str, stage: str,
               on_predict_team1=None, on_predict_team2=None, on_predict_draw=None,
               user_prediction: Optional[str] = None, can_predict: bool = True,
               lock_reason: str = "") -> None:
    """Create a match prediction card."""
    st.markdown(f"""
    <div class="match-card">
        <div style="margin-bottom: 1.5rem;">
            <div style="
                font-size: 0.75rem;
                color: #00C896;
                font-family: 'Montserrat', sans-serif;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                margin-bottom: 0.5rem;
            ">{stage}</div>
            <div style="
                font-size: 0.85rem;
                color: rgba(255, 255, 255, 0.6);
                margin-bottom: 1rem;
            ">{date_str} • {venue}</div>
        </div>
        
        <div style="text-align: center; margin: 1.5rem 0;">
            <div class="team-name">{team_1}</div>
            <div class="vs-divider">vs</div>
            <div class="team-name">{team_2}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Prediction buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🎯 {team_1}", key=f"pred_{team_1}_{int(time.time())}", 
                     disabled=not can_predict or user_prediction is not None, use_container_width=True):
            if on_predict_team1:
                on_predict_team1()
    
    with col2:
        if st.button("🤝 Draw", key=f"draw_{int(time.time())}", 
                     disabled=not can_predict or user_prediction is not None, use_container_width=True):
            if on_predict_draw:
                on_predict_draw()
    
    with col3:
        if st.button(f"🎯 {team_2}", key=f"pred_{team_2}_{int(time.time())}", 
                     disabled=not can_predict or user_prediction is not None, use_container_width=True):
            if on_predict_team2:
                on_predict_team2()
    
    if user_prediction:
        st.markdown(f"""
        <div style="
            text-align: center;
            margin-top: 1rem;
            padding: 0.75rem;
            background: rgba(0, 200, 150, 0.15);
            border: 1px solid rgba(0, 200, 150, 0.4);
            border-radius: 8px;
            color: #00C896;
            font-weight: 600;
        ">✓ Your prediction: <strong>{user_prediction}</strong></div>
        """, unsafe_allow_html=True)
    elif not can_predict:
        st.markdown(f"""
        <div style="
            text-align: center;
            margin-top: 1rem;
            padding: 0.75rem;
            background: rgba(255, 107, 107, 0.15);
            border: 1px solid rgba(255, 107, 107, 0.4);
            border-radius: 8px;
            color: #FF6B6B;
            font-weight: 600;
            animation: pulse 2s infinite;
        ">⏱️ {lock_reason}</div>
        """, unsafe_allow_html=True)


def glass_container(content_func, title: str = "") -> None:
    """Create a glass-morphism container."""
    st.markdown(f'<div class="glass-container">', unsafe_allow_html=True)
    if title:
        st.markdown(f'<h3 style="margin-top: 0;">{title}</h3>', unsafe_allow_html=True)
    content_func()
    st.markdown('</div>', unsafe_allow_html=True)


def leaderboard_podium(leaderboard_data: List[Dict[str, Any]]) -> None:
    """Create a premium leaderboard podium."""
    if len(leaderboard_data) < 3:
        st.warning("Not enough users for podium")
        return
    
    # Get top 3
    top3 = leaderboard_data[:3]
    
    # Sort to display: silver, gold, bronze (1st, 2nd, 3rd in visual order)
    order = [1, 0, 2]  # Reorder for visual podium
    
    st.markdown('<div class="leaderboard-podium">', unsafe_allow_html=True)
    
    medals = ['🥈', '🥇', '🥉']
    classes = ['podium-silver', 'podium-gold', 'podium-bronze']
    positions = ['2nd', '1st', '3rd']
    
    for idx, visual_idx in enumerate(order):
        user = top3[visual_idx]
        medal = medals[visual_idx]
        podium_class = classes[visual_idx]
        
        st.markdown(f"""
        <div class="podium-place {podium_class}">
            <div class="medal">{medal}</div>
            <div class="rank-number">#{visual_idx + 1}</div>
            <div style="
                font-family: 'Montserrat', sans-serif;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 0.5rem;
            ">{user['user_name']}</div>
            <div style="
                font-size: 0.85rem;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 0.5rem;
            ">{user['total_points']} points</div>
            <div class="stat-badge">{user['accuracy_percentage']:.1f}% accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


def stat_badge(text: str, color: str = "accent") -> None:
    """Create a stat badge."""
    color_map = {
        "accent": "#00C896",
        "primary": "#0057B8",
        "warning": "#FF6B6B",
        "info": "#4ECDC4"
    }
    badge_color = color_map.get(color, color)
    
    st.markdown(f"""
    <span class="stat-badge" style="
        background: rgba({int(badge_color[1:3], 16)}, {int(badge_color[3:5], 16)}, {int(badge_color[5:7], 16)}, 0.2);
        border-color: rgba({int(badge_color[1:3], 16)}, {int(badge_color[3:5], 16)}, {int(badge_color[5:7], 16)}, 0.5);
        color: {badge_color};
    ">{text}</span>
    """, unsafe_allow_html=True)


def admin_action_card(icon: str, title: str, description: str, button_text: str, on_click=None) -> None:
    """Create an admin action card."""
    st.markdown(f"""
    <div class="admin-card">
        <div class="admin-icon">{icon}</div>
        <div class="admin-label">{title}</div>
        <div style="color: rgba(255, 255, 255, 0.7); margin-bottom: 1rem; font-size: 0.9rem;">
            {description}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(button_text, key=f"admin_{title.lower().replace(' ', '_')}", use_container_width=True):
        if on_click:
            on_click()


def timeline_prediction(team_1: str, team_2: str, prediction: str, result: Optional[str] = None,
                       points: Optional[int] = None, date_str: str = "") -> None:
    """Create a timeline prediction item."""
    if result and result == prediction:
        status_class = "timeline-item correct"
        status_icon = "✅"
    elif result:
        status_class = "timeline-item incorrect"
        status_icon = "❌"
    else:
        status_class = "timeline-item pending"
        status_icon = "⏳"
    
    st.markdown(f"""
    <div class="{status_class}">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
            <div style="flex: 1;">
                <div style="
                    font-family: 'Montserrat', sans-serif;
                    font-weight: 700;
                    font-size: 1rem;
                    color: #ffffff;
                ">{team_1} vs {team_2}</div>
                <div style="
                    font-size: 0.85rem;
                    color: rgba(255, 255, 255, 0.6);
                ">{date_str}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.2rem; margin-bottom: 0.25rem;">{status_icon}</div>
            </div>
        </div>
        <div style="margin-top: 0.75rem;">
            <span class="stat-badge">Predicted: {prediction}</span>
            {f'<span class="stat-badge">Result: {result}</span>' if result else ''}
            {f'<span class="stat-badge" style="background: rgba(0, 200, 150, 0.2); color: #00C896;">+{points} pts</span>' if points else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)


def progress_bar(value: float, max_value: float = 100, label: str = "") -> None:
    """Create an animated progress bar."""
    percentage = (value / max_value) * 100
    st.markdown(f"""
    <div style="margin: 1rem 0;">
        {f'<div style="font-size: 0.9rem; font-weight: 600; margin-bottom: 0.5rem; color: rgba(255, 255, 255, 0.8);">{label}</div>' if label else ''}
        <div style="
            width: 100%;
            height: 8px;
            background: rgba(0, 88, 184, 0.1);
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid rgba(0, 88, 184, 0.2);
        ">
            <div style="
                height: 100%;
                width: {percentage}%;
                background: linear-gradient(90deg, #0057B8 0%, #00C896 100%);
                border-radius: 10px;
                transition: width 0.3s ease;
            "></div>
        </div>
        <div style="
            font-size: 0.8rem;
            color: #00C896;
            margin-top: 0.25rem;
            font-weight: 600;
        ">{value:.1f}/{max_value:.1f}</div>
    </div>
    """, unsafe_allow_html=True)


def tournament_card(emoji: str, title: str, value: str) -> None:
    """Create a tournament stat card."""
    st.markdown(f"""
    <div class="glass-container" style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{emoji}</div>
        <div style="
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.7);
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        ">{title}</div>
        <div style="
            font-size: 2rem;
            font-weight: 900;
            background: linear-gradient(135deg, #0057B8 0%, #00C896 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">{value}</div>
    </div>
    """, unsafe_allow_html=True)
