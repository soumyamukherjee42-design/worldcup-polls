"""
Home page - Tournament dashboard with hero and stats
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from src.config import Config
from src.storage import Storage
from src.fixtures import FixtureLoader
from src.ui import (
    inject_global_css, hero_section, metric_card, match_card,
    glass_container, tournament_card, progress_bar
)

# Initialize
config = Config()
storage = Storage(config)
storage.initialize_data_layer()
fixture_loader = FixtureLoader(config)
fixture_loader.ensure_fixtures_loaded(storage)

inject_global_css()
st.set_page_config(page_title="Home - World Cup 2026", layout="wide")

# Check authentication
if st.session_state.user_id is None:
    st.info("Please log in from the main page")
    st.stop()

# Hero Section
hero_section(
    "FIFA World Cup 2026",
    "Predict. Compete. Dominate the Leaderboard."
)

st.markdown("---")

# Tournament Stats
st.markdown('<h2 style="text-align: center;">📊 Tournament At A Glance</h2>', unsafe_allow_html=True)

try:
    tournament_stats = storage.get_tournament_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        tournament_card("👥", "Players", tournament_stats.get('Total Users', '0'))
    
    with col2:
        tournament_card("⚽", "Matches", tournament_stats.get('Total Matches', '0'))
    
    with col3:
        tournament_card("🎯", "Predictions", tournament_stats.get('Total Predictions', '0'))
    
    with col4:
        tournament_card("⭐", "Completed", tournament_stats.get('Completed Matches', '0'))
    
except Exception as e:
    st.warning(f"Could not load tournament stats: {e}")

st.markdown("---")

# Upcoming Matches Section
st.markdown('<h2 style="text-align: center;">🔜 Upcoming Matches</h2>', unsafe_allow_html=True)

try:
    matches = storage.get_all_matches()
    matches_df = pd.DataFrame(matches) if matches else pd.DataFrame()
    
    if matches_df.empty:
        st.info("No matches scheduled yet")
    else:
        # Filter active matches (scheduled or live)
        active_matches = matches_df[matches_df['status'].isin(['scheduled', 'live'])]
        
        if active_matches.empty:
            st.info("No upcoming matches at this time. Check back soon!")
        else:
            # Sort by date and time
            active_matches = active_matches.copy()
            active_matches['match_datetime'] = pd.to_datetime(
                active_matches['match_date'] + ' ' + active_matches['kickoff_time']
            )
            active_matches = active_matches.sort_values('match_datetime')
            
            st.markdown(f"**{len(active_matches)} matches coming up**")
            
            # Display top matches in a grid
            for idx, (_, match) in enumerate(active_matches.head(6).iterrows()):
                if idx % 2 == 0:
                    col1, col2 = st.columns(2)
                    current_col = col1
                else:
                    current_col = col2
                
                with current_col:
                    match_datetime = pd.to_datetime(
                        f"{match['match_date']} {match['kickoff_time']}"
                    )
                    
                    user_prediction = storage.get_prediction(match['match_id'], st.session_state.user_id)
                    
                    st.markdown(f"""
                    <div class="match-card">
                        <div style="
                            font-size: 0.7rem;
                            color: #00C896;
                            font-family: 'Montserrat', sans-serif;
                            font-weight: 700;
                            text-transform: uppercase;
                            letter-spacing: 1px;
                            margin-bottom: 0.5rem;
                        ">{match['stage']}</div>
                        <div style="text-align: center; margin: 1rem 0;">
                            <div class="team-name">{match['team_1']}</div>
                            <div class="vs-divider">vs</div>
                            <div class="team-name">{match['team_2']}</div>
                        </div>
                        <div style="
                            text-align: center;
                            margin-top: 1rem;
                            font-size: 0.8rem;
                            color: rgba(255, 255, 255, 0.6);
                        ">
                            {match_datetime.strftime('%m/%d %H:%M')} • {match['venue']}
                        </div>
                        {f'<div style="text-align: center; margin-top: 0.75rem;"><span class="stat-badge">✓ {user_prediction["predicted_winner"]}</span></div>' if user_prediction else ''}
                    </div>
                    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading matches: {e}")

st.markdown("---")

# Leaderboard Preview
st.markdown('<h2 style="text-align: center;">🏆 Leaderboard Preview</h2>', unsafe_allow_html=True)

try:
    leaderboard = storage.get_leaderboard(limit=5)
    
    if leaderboard:
        st.markdown("""
        <style>
        .leaderboard-mini {
            background: linear-gradient(135deg, rgba(0, 88, 184, 0.08) 0%, rgba(0, 200, 150, 0.03) 100%);
            border: 1px solid rgba(0, 88, 184, 0.2);
            border-radius: 12px;
            overflow: hidden;
        }
        .leaderboard-row {
            display: flex;
            align-items: center;
            padding: 1rem;
            border-bottom: 1px solid rgba(0, 88, 184, 0.1);
            transition: all 0.3s ease;
        }
        .leaderboard-row:last-child {
            border-bottom: none;
        }
        .leaderboard-row:hover {
            background: rgba(0, 88, 184, 0.08);
        }
        .leaderboard-rank {
            font-family: 'Montserrat', sans-serif;
            font-weight: 900;
            font-size: 1.2rem;
            min-width: 40px;
            background: linear-gradient(135deg, #0057B8 0%, #00C896 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .leaderboard-name {
            flex: 1;
            margin: 0 1.5rem;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: #ffffff;
        }
        .leaderboard-points {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: #00C896;
            min-width: 80px;
            text-align: right;
        }
        </style>
        <div class="leaderboard-mini">
        """, unsafe_allow_html=True)
        
        for rank, user in enumerate(leaderboard[:5], 1):
            medal = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else ""))
            st.markdown(f"""
            <div class="leaderboard-row">
                <div class="leaderboard-rank">{medal} {rank}</div>
                <div class="leaderboard-name">{user['user_name']}</div>
                <div class="leaderboard-points">{user['total_points']} pts</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("View Full Leaderboard →", use_container_width=True):
                st.switch_page("pages/04_Leaderboard.py")
    else:
        st.info("Leaderboard will appear once players make predictions")

except Exception as e:
    st.error(f"Error loading leaderboard: {e}")

st.markdown("---")

# Your Stats
if st.session_state.user_id:
    st.markdown('<h2 style="text-align: center;">👤 Your Performance</h2>', unsafe_allow_html=True)
    
    try:
        predictions = storage.get_user_prediction_count(st.session_state.user_id)
        correct = storage.get_user_correct_predictions(st.session_state.user_id)
        accuracy = (correct / predictions * 100) if predictions > 0 else 0
        points = storage.get_user_total_points(st.session_state.user_id)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            metric_card("Predictions", str(predictions))
        
        with col2:
            metric_card("Correct", str(correct))
        
        with col3:
            metric_card("Accuracy", f"{accuracy:.1f}%")
        
        with col4:
            metric_card("Points", str(points))
        
        # User rank
        user_rank = storage.get_user_rank(st.session_state.user_id)
        if user_rank:
            st.markdown(f"""
            <div style="
                text-align: center;
                padding: 1.5rem;
                background: linear-gradient(135deg, rgba(0, 200, 150, 0.15) 0%, rgba(0, 200, 150, 0.08) 100%);
                border: 2px solid rgba(0, 200, 150, 0.4);
                border-radius: 12px;
                margin-top: 2rem;
            ">
                <div style="
                    font-size: 1rem;
                    color: rgba(255, 255, 255, 0.8);
                    margin-bottom: 0.5rem;
                ">Your Global Rank</div>
                <div style="
                    font-family: 'Montserrat', sans-serif;
                    font-size: 2.5rem;
                    font-weight: 900;
                    color: #00C896;
                ">#{user_rank['rank']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error loading user stats: {e}")
