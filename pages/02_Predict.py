"""
Predict page - Make predictions on matches.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Predict", layout="wide")

# Session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# Header
st.markdown("""
<h1 style="text-align: center;">🎯 MAKE YOUR PREDICTIONS</h1>
<p style="text-align: center; color: #e53238; font-size: 1rem;">
    Choose the winner before the match starts and earn points!
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Auth check
if st.session_state.user_id is None:
    st.warning("⚠️ You are not logged in.")
    st.info("👈 Please go to **Home** to log in.")
    st.stop()

st.info("⏰ **All times in IST (Indian Standard Time)**")

# Import
try:
    from src.storage import get_storage
    from src.predictions import PredictionManager
    from src.config import Config

    config = Config()
    storage = get_storage()
    pred_manager = PredictionManager(config, storage)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

try:
    # Current IST time — used to hide matches that have already kicked off
    IST = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(IST)
    today_ist_str  = now_ist.strftime('%Y-%m-%d')
    now_ist_time   = now_ist.strftime('%H:%M:%S')

    matches = storage.get_all_matches()

    if not matches:
        st.warning("📭 No matches in database")
        st.stop()

    # Keep only scheduled matches whose IST kickoff hasn't passed yet.
    # match_date_ist and kickoff_time_ist come directly from the DB.
    def is_upcoming(m):
        if m.get('status', '').lower() != 'scheduled':
            return False
        d = str(m.get('match_date_ist') or '')
        t = str(m.get('kickoff_time_ist') or '00:00').strip()
        if len(t) == 5:          # HH:MM → HH:MM:SS for string comparison
            t += ':00'
        if d > today_ist_str:
            return True
        if d == today_ist_str and t >= now_ist_time:
            return True
        return False

    active = [m for m in matches if is_upcoming(m)]

    if not active:
        st.info("⏰ No upcoming matches available for prediction")
        st.stop()

    # Group by IST date (comes from DB, no Python computation)
    dates = sorted(set(str(m['match_date_ist']) for m in active))

    selected_date = st.selectbox(
        "📅 Select Date (IST)",
        dates,
        format_func=lambda d: pd.to_datetime(d).strftime('%B %d, %Y')
    )

    day_matches = [m for m in active if str(m['match_date_ist']) == selected_date]

    if not day_matches:
        st.info("No matches on this date")
        st.stop()

    st.subheader(f"📋 {len(day_matches)} Matches on {pd.to_datetime(selected_date).strftime('%B %d, %Y')} (IST)")
    st.markdown("")

    for match in day_matches:
        # kickoff_time_ist is pre-stored in DB (HH:MM, 24-hour IST)
        kickoff_display = str(match.get('kickoff_time_ist', match['kickoff_time'])) + ' IST'

        pred = storage.get_prediction(match['match_id'], st.session_state.user_id)

        st.caption(f"📅 {pd.to_datetime(selected_date).strftime('%B %d, %Y')} | 🕐 {kickoff_display} | {match['stage']}")

        if pred:
            st.success(f"✅ Your prediction: **{pred['predicted_winner']}**")
        else:
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button(f"🎯 {match['team_1']}", key=f"p_{match['match_id']}_1", use_container_width=True):
                    success, msg, _ = pred_manager.make_prediction(
                        st.session_state.user_id, match['match_id'], match['team_1']
                    )
                    if success:
                        st.success("✅ Prediction saved!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"Error: {msg}")

            with col2:
                if st.button("🤝 DRAW", key=f"p_{match['match_id']}_draw", use_container_width=True):
                    success, msg, _ = pred_manager.make_prediction(
                        st.session_state.user_id, match['match_id'], 'draw'
                    )
                    if success:
                        st.success("✅ Prediction saved!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"Error: {msg}")

            with col3:
                if st.button(f"🎯 {match['team_2']}", key=f"p_{match['match_id']}_2", use_container_width=True):
                    success, msg, _ = pred_manager.make_prediction(
                        st.session_state.user_id, match['match_id'], match['team_2']
                    )
                    if success:
                        st.success("✅ Prediction saved!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"Error: {msg}")

        st.markdown("---")

except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    st.error(f"Error: {str(e)}")
