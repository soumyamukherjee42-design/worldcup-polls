"""
Home page - Tournament dashboard
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from src.config import Config
from src.storage import Storage
from src.fixtures import FixtureLoader

# Initialize
config = Config()
storage = Storage(config)
storage.initialize_data_layer()
fixture_loader = FixtureLoader(config)
fixture_loader.ensure_fixtures_loaded(storage)

st.set_page_config(page_title="Home - World Cup 2026", layout="wide")

st.title("⚽ World Cup 2026 - Tournament Dashboard")
st.markdown("---")

# Check authentication
if st.session_state.user_id is None:
    st.info("Please log in from the Home page to view the dashboard")
    st.stop()

# Tournament Info Section
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Tournament", "FIFA 2026")

with col2:
    st.metric("Hosts", "USA, Canada, Mexico")

with col3:
    st.metric("Teams", "32")

with col4:
    st.metric("Matches", "64")

st.markdown("---")

# Tournament Stats
st.subheader("📊 Tournament Statistics")

try:
    tournament_stats = storage.get_tournament_stats()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Users", tournament_stats.get('Total Users', '0'))
    
    with col2:
        st.metric("Total Matches", tournament_stats.get('Total Matches', '0'))
    
    with col3:
        st.metric("Scheduled", tournament_stats.get('Scheduled Matches', '0'))
    
    with col4:
        st.metric("Completed", tournament_stats.get('Completed Matches', '0'))
    
    with col5:
        st.metric("Total Predictions", tournament_stats.get('Total Predictions', '0'))
    
    st.markdown("---")
except Exception as e:
    st.warning(f"Could not load tournament stats: {e}")

# Today's/Upcoming Matches
st.subheader("🔜 Upcoming Matches")

try:
    matches = storage.get_all_matches()
    matches_df = pd.DataFrame(matches)
    
    if matches_df.empty:
        st.info("No matches scheduled yet")
    else:
        # Filter active matches (scheduled or live)
        active_matches = matches_df[matches_df['status'].isin(['scheduled', 'live'])]
        
        if active_matches.empty:
            st.info("No upcoming matches")
        else:
            # Sort by date and time
            active_matches = active_matches.copy()
            active_matches['match_datetime'] = pd.to_datetime(
                active_matches['match_date'] + ' ' + active_matches['kickoff_time']
            )
            active_matches = active_matches.sort_values('match_datetime')
            
            for idx, match in active_matches.head(10).iterrows():
                col1, col2, col3, col4 = st.columns([2, 1, 2, 2])
                
                with col1:
                    st.write(f"**{match['team_1']} vs {match['team_2']}**")
                
                with col2:
                    st.write(match['stage'])
                
                with col3:
                    match_datetime = pd.to_datetime(
                        f"{match['match_date']} {match['kickoff_time']}"
                    )
                    st.write(match_datetime.strftime("%m/%d %H:%M"))
                
                with col4:
                    st.write(match['venue'])
except Exception as e:
    st.error(f"Error loading matches: {e}")

st.markdown("---")

# Leaderboard Preview
st.subheader("🏆 Top 10 Leaderboard")

try:
    leaderboard = storage.get_leaderboard(limit=10)
    
    if leaderboard:
        lb_df = pd.DataFrame(leaderboard)
        
        # Format display
        display_df = lb_df[[
            'rank', 'user_name', 'total_points', 'total_predictions',
            'correct_predictions', 'accuracy_percentage'
        ]].copy()
        
        display_df.columns = [
            'Rank', 'Player', 'Points', 'Predictions', 'Correct', 'Accuracy %'
        ]
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("Leaderboard will appear once users make predictions")
except Exception as e:
    st.error(f"Error loading leaderboard: {e}")

st.markdown("---")

# User's Stats
if st.session_state.user_id:
    st.subheader("👤 Your Statistics")
    
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        predictions = storage.get_user_prediction_count(st.session_state.user_id)
        correct = storage.get_user_correct_predictions(st.session_state.user_id)
        accuracy = (correct / predictions * 100) if predictions > 0 else 0
        points = storage.get_user_total_points(st.session_state.user_id)
        
        with col1:
            st.metric("Predictions", predictions)
        
        with col2:
            st.metric("Correct", correct)
        
        with col3:
            st.metric("Accuracy %", f"{accuracy:.1f}%")
        
        with col4:
            st.metric("Total Points", points)
        
        # User rank
        user_rank = storage.get_user_rank(st.session_state.user_id)
        if user_rank:
            st.success(f"Current Rank: **#{user_rank['rank']}** 🎯")
    
    except Exception as e:
        st.error(f"Error loading user stats: {e}")

st.markdown("---")

# Information
st.subheader("ℹ️ How to Play")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🎯 Make Predictions
    - Go to the **Predict** page
    - Choose matches you want to predict
    - Select the winner before kickoff
    - Earn points for correct predictions
    """)

with col2:
    st.markdown("""
    ### 📊 Track Your Performance
    - Visit **My Predictions** to see history
    - Check your accuracy and points
    - View match results
    - Learn from your predictions
    """)

with col3:
    st.markdown("""
    ### 🏆 Climb the Rankings
    - Check **Leaderboard** page
    - Compete globally
    - Earn badges for performance
    - Have fun! ⚽
    """)

st.markdown("---")

# Scoring Info
st.subheader("⭐ Scoring System")

score_col1, score_col2, score_col3 = st.columns(3)

with score_col1:
    st.success("**Correct Winner: +3 points**")

with score_col2:
    st.info("**Correct Draw: +2 points**")

with score_col3:
    st.error("**Wrong: 0 points**")
