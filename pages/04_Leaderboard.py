"""
Leaderboard page - Global rankings with podium
"""
import streamlit as st
import pandas as pd
from src.config import Config
from src.storage import Storage
from src.ui import inject_global_css, leaderboard_podium, progress_bar

# Initialize
config = Config()
storage = Storage(config)
storage.initialize_data_layer()

inject_global_css()
st.set_page_config(page_title="Leaderboard - World Cup 2026", layout="wide")

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <div style="
        font-family: 'Montserrat', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #0057B8 0%, #00C896 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    ">🏆 Global Leaderboard</div>
    <div style="
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.7);
    ">Compete worldwide. Claim your throne.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

try:
    # Get leaderboard
    leaderboard = storage.get_leaderboard()
    
    if not leaderboard:
        st.info("Leaderboard will appear once players make predictions")
        st.stop()
    
    lb_df = pd.DataFrame(leaderboard)
    
    # Display Podium
    st.markdown('<h2 style="text-align: center;">🥇 Podium</h2>', unsafe_allow_html=True)
    
    if len(lb_df) >= 3:
        leaderboard_podium(lb_df.to_dict('records'))
    
    st.markdown("---")
    
    # Filters
    st.markdown('<h2>🔍 Rankings</h2>', unsafe_allow_html=True)
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        min_predictions = st.slider(
            "Minimum Predictions",
            min_value=0,
            max_value=int(lb_df['total_predictions'].max()),
            value=0
        )
    
    with filter_col2:
        sort_by = st.selectbox(
            "Sort By",
            options=['Total Points', 'Accuracy %', 'Total Predictions', 'Rank']
        )
    
    with filter_col3:
        search_name = st.text_input("Search player", placeholder="Type name...")
    
    # Apply filters
    filtered_df = lb_df[lb_df['total_predictions'] >= min_predictions].copy()
    
    if search_name:
        filtered_df = filtered_df[filtered_df['user_name'].str.contains(search_name, case=False, na=False)]
    
    # Apply sorting
    if sort_by == 'Total Points':
        filtered_df = filtered_df.sort_values('total_points', ascending=False)
    elif sort_by == 'Accuracy %':
        filtered_df = filtered_df.sort_values('accuracy_percentage', ascending=False)
    elif sort_by == 'Total Predictions':
        filtered_df = filtered_df.sort_values('total_predictions', ascending=False)
    else:
        filtered_df = filtered_df.sort_values('rank')
    
    filtered_df = filtered_df.reset_index(drop=True)
    
    st.markdown("---")
    
    # Display Rankings Table
    st.markdown(f"""
    <div style="
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.08) 0%, rgba(0, 200, 150, 0.03) 100%);
        border: 1px solid rgba(0, 88, 184, 0.2);
        border-radius: 12px;
        margin-bottom: 2rem;
    ">
        <strong>📊 {len(filtered_df)} Players in Rankings</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .ranking-table {
        width: 100%;
        border-collapse: collapse;
    }
    .ranking-header {
        background: linear-gradient(135deg, rgba(0, 88, 184, 0.15) 0%, rgba(0, 200, 150, 0.08) 100%);
        border-bottom: 2px solid rgba(0, 88, 184, 0.3);
        padding: 1rem;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        color: #00C896;
        text-align: left;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .ranking-cell {
        padding: 1rem;
        border-bottom: 1px solid rgba(0, 88, 184, 0.1);
        color: #ffffff;
    }
    .ranking-row {
        transition: all 0.3s ease;
    }
    .ranking-row:hover {
        background: rgba(0, 88, 184, 0.08);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Manual table rendering
    for idx, (_, row) in enumerate(filtered_df.iterrows()):
        rank = row['rank']
        medal = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else ""))
        
        col1, col2, col3, col4, col5, col6 = st.columns([0.5, 0.5, 2, 1, 1, 1.2])
        
        with col1:
            st.markdown(f"<div style='font-weight: 900; font-size: 1.1rem; background: linear-gradient(135deg, #0057B8 0%, #00C896 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>{medal}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<div style='font-weight: 900; font-size: 1.1rem; background: linear-gradient(135deg, #0057B8 0%, #00C896 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>#{rank}</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"<div style='font-family: Montserrat; font-weight: 700; color: white;'>{row['user_name']}</div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"<div style='text-align: center; color: #00C896; font-weight: 600;'>{row['total_points']} pts</div>", unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"<div style='text-align: center; color: rgba(255,255,255,0.8);'>{row['total_predictions']}</div>", unsafe_allow_html=True)
        
        with col6:
            st.markdown(f"""
            <div style='
                background: rgba(0, 200, 150, 0.2);
                border: 1px solid rgba(0, 200, 150, 0.4);
                border-radius: 6px;
                padding: 0.5rem 0.75rem;
                text-align: center;
                color: #00C896;
                font-weight: 600;
                font-size: 0.9rem;
            '>{row['accuracy_percentage']:.1f}%</div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # User's rank highlight
    if st.session_state.user_id:
        user_rank = storage.get_user_rank(st.session_state.user_id)
        if user_rank:
            st.markdown('<h2>👤 Your Position</h2>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(0, 88, 184, 0.1) 0%, rgba(0, 200, 150, 0.05) 100%);
                    border: 1px solid rgba(0, 88, 184, 0.2);
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                ">
                    <div style="font-size: 0.8rem; color: rgba(255, 255, 255, 0.6); text-transform: uppercase; font-weight: 600; margin-bottom: 0.5rem;">Rank</div>
                    <div style="font-size: 2rem; font-weight: 900; background: linear-gradient(135deg, #0057B8 0%, #00C896 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">#{user_rank['rank']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(0, 88, 184, 0.1) 0%, rgba(0, 200, 150, 0.05) 100%);
                    border: 1px solid rgba(0, 88, 184, 0.2);
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                ">
                    <div style="font-size: 0.8rem; color: rgba(255, 255, 255, 0.6); text-transform: uppercase; font-weight: 600; margin-bottom: 0.5rem;">Points</div>
                    <div style="font-size: 2rem; font-weight: 900; color: #00C896;">{user_rank['total_points']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(0, 88, 184, 0.1) 0%, rgba(0, 200, 150, 0.05) 100%);
                    border: 1px solid rgba(0, 88, 184, 0.2);
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                ">
                    <div style="font-size: 0.8rem; color: rgba(255, 255, 255, 0.6); text-transform: uppercase; font-weight: 600; margin-bottom: 0.5rem;">Accuracy</div>
                    <div style="font-size: 2rem; font-weight: 900; color: #00C896;">{user_rank['accuracy_percentage']:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(0, 88, 184, 0.1) 0%, rgba(0, 200, 150, 0.05) 100%);
                    border: 1px solid rgba(0, 88, 184, 0.2);
                    border-radius: 12px;
                    padding: 1.5rem;
                    text-align: center;
                ">
                    <div style="font-size: 0.8rem; color: rgba(255, 255, 255, 0.6); text-transform: uppercase; font-weight: 600; margin-bottom: 0.5rem;">Predictions</div>
                    <div style="font-size: 2rem; font-weight: 900; color: #00C896;">{user_rank['total_predictions']}</div>
                </div>
                """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading leaderboard: {e}")
