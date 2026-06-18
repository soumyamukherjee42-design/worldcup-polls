"""
Predict page - Make predictions on matches
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from src.config import Config
from src.storage import Storage
from src.predictions import PredictionManager
from src.fixtures import FixtureLoader

# Initialize
config = Config()
storage = Storage(config)
storage.initialize_data_layer()
fixture_loader = FixtureLoader(config)
fixture_loader.ensure_fixtures_loaded(storage)
pred_manager = PredictionManager(config, storage)

st.set_page_config(page_title="Predict - World Cup 2026", layout="wide")

st.title("🎯 Make Your Predictions")
st.markdown("---")

# Check authentication
if st.session_state.user_id is None:
    st.info("Please log in from the Home page to make predictions")
    st.stop()

# Get active matches
try:
    all_matches = storage.get_all_matches()
    matches_df = pd.DataFrame(all_matches) if all_matches else pd.DataFrame()
    
    if matches_df.empty:
        st.warning("No matches available for prediction")
        st.stop()
    
    # Filter for active (scheduled) matches
    active_matches = matches_df[matches_df['status'] == 'scheduled'].copy()
    
    if active_matches.empty:
        st.info("No active matches available for prediction at this time")
        st.stop()
    
    # Sort by date and time
    active_matches['match_datetime'] = pd.to_datetime(
        active_matches['match_date'] + ' ' + active_matches['kickoff_time']
    )
    active_matches = active_matches.sort_values('match_datetime')
    
    st.subheader(f"📋 {len(active_matches)} Matches Available")
    
    # Display matches with prediction options
    for idx, (_, match) in enumerate(active_matches.iterrows()):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([1.5, 0.5, 1.5, 1, 1.5])
            
            match_datetime = pd.to_datetime(f"{match['match_date']} {match['kickoff_time']}")
            
            with col1:
                st.markdown(f"**{match['team_1']}**")
            
            with col2:
                st.write("vs")
            
            with col3:
                st.markdown(f"**{match['team_2']}**")
            
            with col4:
                st.caption(match_datetime.strftime("%m/%d %H:%M"))
            
            with col5:
                st.caption(f"📍 {match['venue']}")
            
            # Check if user already predicted
            user_prediction = storage.get_prediction(match['match_id'], st.session_state.user_id)
            
            can_predict, reason = pred_manager.can_predict(match['match_id'])
            
            col_pred1, col_pred2, col_pred3, col_pred4 = st.columns([1.5, 1.5, 1, 1])
            
            with col_pred1:
                if st.button(
                    f"{match['team_1']} ✓",
                    key=f"pred_{match['match_id']}_team1",
                    disabled=not can_predict or user_prediction is not None
                ):
                    if user_prediction is None:
                        success, msg, pred_id = pred_manager.make_prediction(
                            st.session_state.user_id,
                            match['match_id'],
                            match['team_1']
                        )
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
            
            with col_pred2:
                if st.button(
                    f"{match['team_2']} ✓",
                    key=f"pred_{match['match_id']}_team2",
                    disabled=not can_predict or user_prediction is not None
                ):
                    if user_prediction is None:
                        success, msg, pred_id = pred_manager.make_prediction(
                            st.session_state.user_id,
                            match['match_id'],
                            match['team_2']
                        )
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
            
            with col_pred3:
                if st.button(
                    "Draw",
                    key=f"pred_{match['match_id']}_draw",
                    disabled=not can_predict or user_prediction is not None
                ):
                    if user_prediction is None:
                        success, msg, pred_id = pred_manager.make_prediction(
                            st.session_state.user_id,
                            match['match_id'],
                            'draw'
                        )
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
            
            with col_pred4:
                if user_prediction:
                    st.info(f"✓ {user_prediction['predicted_winner']}")
                else:
                    if not can_predict:
                        st.caption(f"⏱️ {reason}")
            
            st.divider()
    
except Exception as e:
    st.error(f"Error loading matches: {e}")

st.markdown("---")

st.subheader("📌 Tips")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ⏰ **Don't Miss Kickoff**
    Predictions close automatically at match start
    """)

with col2:
    st.markdown("""
    🎯 **Strategic Thinking**
    Consider recent form and head-to-head records
    """)

with col3:
    st.markdown("""
    ⭐ **Maximize Points**
    Correct draws worth 2 points, winners worth 3
    """)
