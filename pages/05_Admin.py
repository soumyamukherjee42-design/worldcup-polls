"""
Admin page - Administrative functions
"""
import streamlit as st
import pandas as pd
from src.config import Config
from src.storage import Storage
from src.fixtures import FixtureLoader, create_sample_fixtures
from src.simulator import ResultSimulator
from src.leaderboard import LeaderboardManager

# Initialize
config = Config()
storage = Storage(config)
storage.initialize_data_layer()

st.set_page_config(page_title="Admin - World Cup 2026", layout="wide")

st.title("⚙️ Admin Console")
st.markdown("---")

# Simple auth - check if admin
admin_password = st.secrets.get("admin_password", "admin123")

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.warning("🔒 Admin Authentication Required")
    password = st.text_input("Enter admin password:", type="password")
    
    if st.button("Authenticate"):
        if password == admin_password:
            st.session_state.admin_authenticated = True
            st.success("Authenticated!")
            st.rerun()
        else:
            st.error("Invalid password")
    st.stop()

st.success("✅ Admin Mode Active")
st.markdown("---")

# Admin tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Database",
    "🎯 Fixtures",
    "🎮 Simulator",
    "🏆 Leaderboard",
    "🔧 Maintenance"
])

# ========== TAB 1: Database ==========
with tab1:
    st.subheader("Database Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Table Sizes")
        try:
            sizes = storage.get_database_size()
            for name, count in sizes.items():
                st.metric(name.capitalize(), count)
        except Exception as e:
            st.error(f"Error: {e}")
    
    with col2:
        st.subheader("🗄️ Data Preview")
        
        table_choice = st.selectbox(
            "Select table to preview",
            ["users", "matches", "predictions", "results", "points"]
        )
        
        try:
            if table_choice == "users":
                df = pd.read_csv(config.USER_MASTER_PATH)
            elif table_choice == "matches":
                df = pd.read_csv(config.MATCH_MASTER_PATH)
            elif table_choice == "predictions":
                df = pd.read_csv(config.PREDICTION_FACT_PATH)
            elif table_choice == "results":
                df = pd.read_csv(config.MATCH_RESULT_PATH)
            else:
                df = pd.read_csv(config.POINTS_FACT_PATH)
            
            st.dataframe(df.head(5), use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

# ========== TAB 2: Fixtures ==========
with tab2:
    st.subheader("Fixture Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Current Fixtures**")
        try:
            matches = storage.get_all_matches()
            st.metric("Total Matches", len(matches))
            
            if matches:
                matches_df = pd.DataFrame(matches)
                st.write(f"Status breakdown:")
                st.write(matches_df['status'].value_counts().to_dict())
        except Exception as e:
            st.error(f"Error: {e}")
    
    with col2:
        st.write("**Load Fixtures**")
        
        if st.button("Load Sample Fixtures"):
            try:
                fixtures_df = create_sample_fixtures()
                storage.load_fixtures(fixtures_df)
                st.success(f"Loaded {len(fixtures_df)} sample fixtures!")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("---")
    
    # Upload custom fixtures
    st.subheader("Upload Custom Fixtures")
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file:
        try:
            fixtures_df = pd.read_csv(uploaded_file)
            st.dataframe(fixtures_df)
            
            if st.button("Load Uploaded Fixtures"):
                fixture_loader = FixtureLoader(config)
                if fixture_loader.validate_fixtures(fixtures_df):
                    storage.load_fixtures(fixtures_df)
                    st.success(f"Loaded {len(fixtures_df)} fixtures!")
                else:
                    st.error("Fixture validation failed")
        except Exception as e:
            st.error(f"Error: {e}")

# ========== TAB 3: Simulator ==========
with tab3:
    st.subheader("Match Result Simulator")
    
    simulator = ResultSimulator(config, storage)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Auto-Simulate Completed Matches", use_container_width=True):
            try:
                count = simulator.auto_simulate_completed_matches()
                st.success(f"Simulated {count} matches")
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        if st.button("Bulk Simulate ALL Results", use_container_width=True):
            try:
                if st.checkbox("⚠️ Confirm bulk simulation"):
                    count = simulator.bulk_simulate_all_results()
                    st.success(f"Simulated {count} matches")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("---")
    
    st.subheader("Manual Result Entry")
    
    try:
        matches = storage.get_matches_by_status('scheduled')
        if matches:
            match_dict = {f"{m['team_1']} vs {m['team_2']}": m for m in matches}
            
            selected_match_str = st.selectbox(
                "Select match",
                list(match_dict.keys())
            )
            
            selected_match = match_dict[selected_match_str]
            
            winner = st.radio(
                "Winner",
                [selected_match['team_1'], selected_match['team_2'], 'draw']
            )
            
            if st.button("Save Result"):
                storage.save_match_result(selected_match['match_id'], winner)
                storage.update_match_status(selected_match['match_id'], 'completed')
                st.success("Result saved!")
        else:
            st.info("No scheduled matches")
    except Exception as e:
        st.error(f"Error: {e}")

# ========== TAB 4: Leaderboard ==========
with tab4:
    st.subheader("Leaderboard Management")
    
    leaderboard_mgr = LeaderboardManager(config, storage)
    
    if st.button("🔄 Refresh Leaderboard", use_container_width=True):
        try:
            leaderboard_mgr.refresh_all_gold_tables()
            st.success("Leaderboard refreshed!")
        except Exception as e:
            st.error(f"Error: {e}")
    
    st.markdown("---")
    
    st.subheader("Current Leaderboard")
    
    try:
        leaderboard = storage.get_leaderboard()
        if leaderboard:
            lb_df = pd.DataFrame(leaderboard)
            st.dataframe(
                lb_df[[
                    'rank', 'user_name', 'total_points',
                    'total_predictions', 'accuracy_percentage'
                ]],
                use_container_width=True
            )
        else:
            st.info("Leaderboard empty")
    except Exception as e:
        st.error(f"Error: {e}")

# ========== TAB 5: Maintenance ==========
with tab5:
    st.subheader("Maintenance & Reset")
    
    st.warning("⚠️ Dangerous operations - use with caution!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 View Statistics", use_container_width=True):
            try:
                stats = storage.get_tournament_stats()
                for key, value in stats.items():
                    st.metric(key, value)
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        st.subheader("🗑️ Reset Data")
        
        if st.checkbox("Enable reset"):
            if st.button("🔴 RESET ALL TABLES", use_container_width=True):
                try:
                    storage.reset_all_tables()
                    st.success("All tables reset!")
                except Exception as e:
                    st.error(f"Error: {e}")

st.markdown("---")
st.caption("Admin Console | Use with caution")
