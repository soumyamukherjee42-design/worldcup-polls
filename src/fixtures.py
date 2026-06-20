import pandas as pd
from datetime import datetime, timezone, timedelta
import uuid
import logging

logger = logging.getLogger(__name__)

def create_sample_fixtures():
    """Generates sample fixtures for FIFA World Cup 2026."""
    
    # Calculate current US date so the 'Predict' page always has active matches to show today
    current_us_time = datetime.now(timezone.utc) - timedelta(hours=4)
    today_str = current_us_time.strftime('%Y-%m-%d')
    tomorrow_str = (current_us_time + timedelta(days=1)).strftime('%Y-%m-%d')

    fixtures = [
        # Matches happening TODAY
        {
            "match_id": str(uuid.uuid4()),
            "team_1": "USA",
            "team_2": "Australia",
            "match_date": today_str,
            "kickoff_time": "12:00:00",
            "stage": "Group D",
            "venue": "Seattle",
            "status": "scheduled"
        },
        {
            "match_id": str(uuid.uuid4()),
            "team_1": "Scotland",
            "team_2": "Morocco",
            "match_date": today_str,
            "kickoff_time": "18:00:00",
            "stage": "Group C",
            "venue": "Boston",
            "status": "scheduled"
        },
        # Matches happening TOMORROW
        {
            "match_id": str(uuid.uuid4()),
            "team_1": "Ecuador",
            "team_2": "Curaçao",
            "match_date": tomorrow_str,
            "kickoff_time": "19:00:00",
            "stage": "Group E",
            "venue": "Kansas City",
            "status": "scheduled"
        },
        {
            "match_id": str(uuid.uuid4()),
            "team_1": "Spain",
            "team_2": "Saudi Arabia",
            "match_date": tomorrow_str,
            "kickoff_time": "12:00:00",
            "stage": "Group H",
            "venue": "Atlanta",
            "status": "scheduled"
        }
    ]
    
    return pd.DataFrame(fixtures)


class FixtureLoader:
    def __init__(self, config):
        self.config = config

    def ensure_fixtures_loaded(self, storage):
        """Checks if matches exist in storage, and loads sample data if not."""
        try:
            matches = storage.get_all_matches()
            # If the matches table is completely empty, populate it
            if not matches or len(matches) == 0:
                logger.info("No matches found in database. Loading sample fixtures...")
                df = create_sample_fixtures()
                storage.load_fixtures(df)
        except Exception as e:
            logger.error(f"Error ensuring fixtures are loaded: {e}")
            
    def validate_fixtures(self, df):
        """Validates an uploaded fixture dataframe from the Admin panel."""
        required_cols = ['team_1', 'team_2', 'match_date', 'kickoff_time', 'stage', 'venue']
        for col in required_cols:
            if col not in df.columns:
                return False
        return True
