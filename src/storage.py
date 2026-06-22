"""
Complete storage module for FIFA World Cup Polls.

Handles all database operations including:
- User management
- Match management
- Predictions and voting
- Results and scoring
- Leaderboard and statistics
"""

import sqlite3
import logging
from datetime import datetime, timezone
from typing import List, Dict, Optional
import uuid

logger = logging.getLogger(__name__)


class Storage:
    """Complete database storage handler."""
    
    def __init__(self, db_path: str = "database.db"):
        """Initialize storage with database path."""
        self.db_path = db_path
        self.conn = None
        self._init_db()
    
    def _init_db(self):
        """Initialize database connection and create tables."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON")
            self._create_tables()
            logger.info(f"Database initialized: {self.db_path}")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def _create_tables(self):
        """Create all database tables."""
        cursor = self.conn.cursor()
        
        try:
            # Users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                user_name TEXT UNIQUE NOT NULL,
                email TEXT,
                country TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Matches table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                match_id TEXT PRIMARY KEY,
                team_1 TEXT NOT NULL,
                team_2 TEXT NOT NULL,
                stage TEXT NOT NULL,
                match_date TEXT NOT NULL,
                kickoff_time TEXT NOT NULL,
                venue TEXT,
                status TEXT DEFAULT 'scheduled',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Predictions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                prediction_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                match_id TEXT NOT NULL,
                predicted_winner TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                points INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(match_id) REFERENCES matches(match_id),
                UNIQUE(user_id, match_id)
            )
            """)
            
            # Results table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS results (
                result_id TEXT PRIMARY KEY,
                match_id TEXT NOT NULL UNIQUE,
                actual_winner TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(match_id) REFERENCES matches(match_id)
            )
            """)
            
            # Create indexes for better query performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_matches_status ON matches(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_user ON predictions(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_match ON predictions(match_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_results_match ON results(match_id)")
            
            self.conn.commit()
            logger.info("Database tables created successfully")
        
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            self.conn.rollback()
            raise
    
    # ============ USER METHODS ============
    
    def get_or_create_user(self, user_id: str, user_name: str, email: str = "", country: str = ""):
        """
        Get existing user or create new one.
        
        Args:
            user_id: Unique user identifier
            user_name: Display name
            email: Email address
            country: Country/team preference
        
        Returns:
            User dictionary or None
        """
        try:
            cursor = self.conn.cursor()
            
            # Check if user exists
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            
            if user:
                return dict(user)
            
            # Create new user
            cursor.execute("""
            INSERT INTO users (user_id, user_name, email, country)
            VALUES (?, ?, ?, ?)
            """, (user_id, user_name, email, country))
            
            self.conn.commit()
            logger.info(f"User created: {user_id} - {user_name}")
            
            return self.get_user(user_id)
        
        except sqlite3.IntegrityError as e:
            logger.error(f"User name already exists: {user_name}")
            return None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
        
        Returns:
            User dictionary or None
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            return dict(user) if user else None
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def get_all_users(self) -> List[Dict]:
        """
        Get all users.
        
        Returns:
            List of user dictionaries
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY user_name")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
    
    # ============ MATCH METHODS ============
    
    def create_match(self, match_id: str, team_1: str, team_2: str, stage: str,
                    match_date: str, kickoff_time: str, venue: str = "") -> bool:
        """
        Create a new match.
        
        Args:
            match_id: Unique match identifier
            team_1: First team name
            team_2: Second team name
            stage: Tournament stage
            match_date: Date in YYYY-MM-DD format
            kickoff_time: Time in HH:MM format
            venue: Match venue
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            INSERT OR IGNORE INTO matches 
            (match_id, team_1, team_2, stage, match_date, kickoff_time, venue, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'scheduled')
            """, (match_id, team_1, team_2, stage, match_date, kickoff_time, venue))
            
            self.conn.commit()
            logger.info(f"Match created: {team_1} vs {team_2} on {match_date}")
            return True
        except Exception as e:
            logger.error(f"Error creating match: {e}")
            return False
    
    def get_match(self, match_id: str) -> Optional[Dict]:
        """
        Get match by ID.
        
        Args:
            match_id: Match ID
        
        Returns:
            Match dictionary or None
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM matches WHERE match_id = ?", (match_id,))
            match = cursor.fetchone()
            return dict(match) if match else None
        except Exception as e:
            logger.error(f"Error getting match: {e}")
            return None
    
    def get_all_matches(self) -> List[Dict]:
        """
        Get all matches.
        
        Returns:
            List of match dictionaries ordered by date and time
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            SELECT * FROM matches 
            ORDER BY match_date, kickoff_time
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting all matches: {e}")
            return []
    
    def get_matches_by_date(self, match_date: str) -> List[Dict]:
        """
        Get matches for a specific date.
        
        Args:
            match_date: Date in YYYY-MM-DD format
        
        Returns:
            List of matches for that date
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            SELECT * FROM matches 
            WHERE match_date = ? 
            ORDER BY kickoff_time
            """, (match_date,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting matches by date: {e}")
            return []
    
    def update_match_status(self, match_id: str, status: str) -> bool:
        """
        Update match status (scheduled/completed/cancelled).
        
        Args:
            match_id: Match ID
            status: New status
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE matches SET status = ? WHERE match_id = ?",
                (status, match_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating match status: {e}")
            return False
    
    # ============ PREDICTION METHODS ============
    
    def create_prediction(self, prediction_id: str, user_id: str, match_id: str,
                         predicted_winner: str, timestamp: str = None) -> bool:
        """
        Create a new prediction.
        
        Args:
            prediction_id: Unique prediction ID
            user_id: User ID
            match_id: Match ID
            predicted_winner: Predicted winner (team name or 'draw')
            timestamp: Timestamp (auto-generated if None)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if timestamp is None:
                timestamp = datetime.now(timezone.utc).isoformat()
            
            cursor = self.conn.cursor()
            cursor.execute("""
            INSERT INTO predictions 
            (prediction_id, user_id, match_id, predicted_winner, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """, (prediction_id, user_id, match_id, predicted_winner, timestamp))
            
            self.conn.commit()
            logger.info(f"Prediction created: {user_id} predicted {predicted_winner} for {match_id}")
            return True
        
        except sqlite3.IntegrityError:
            logger.warning(f"User already predicted for this match: {user_id} - {match_id}")
            return False
        except Exception as e:
            logger.error(f"Error creating prediction: {e}")
            return False
    
    def get_prediction(self, match_id: str, user_id: str) -> Optional[Dict]:
        """
        Get a specific prediction.
        
        Args:
            match_id: Match ID
            user_id: User ID
        
        Returns:
            Prediction dictionary or None
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            SELECT * FROM predictions 
            WHERE match_id = ? AND user_id = ?
            """, (match_id, user_id))
            pred = cursor.fetchone()
            return dict(pred) if pred else None
        except Exception as e:
            logger.error(f"Error getting prediction: {e}")
            return None
    
    def get_user_predictions(self, user_id: str) -> List[Dict]:
        """
        Get all predictions for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of prediction dictionaries
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            SELECT * FROM predictions 
            WHERE user_id = ? 
            ORDER BY timestamp DESC
            """, (user_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting user predictions: {e}")
            return []
    
    def get_match_predictions(self, match_id: str) -> List[Dict]:
        """
        Get all predictions for a match.
        
        Args:
            match_id: Match ID
        
        Returns:
            List of prediction dictionaries
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
            SELECT * FROM predictions 
            WHERE match_id = ?
            ORDER BY timestamp
            """, (match_id,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting match predictions: {e}")
            return []
    
    def update_prediction_points(self, prediction_id: str, points: int) -> bool:
        """
        Update points for a prediction.
        
        Args:
            prediction_id: Prediction ID
            points: Points to award
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE predictions SET points = ? WHERE prediction_id = ?",
                (points, prediction_id)
            )
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating prediction points: {e}")
            return False
    
    def delete_prediction(self, prediction_id: str) -> bool:
        """
        Delete a prediction (admin only).
        
        Args:
            prediction_id: Prediction ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM predictions WHERE prediction_id = ?", (prediction_id,))
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting prediction: {e}")
            return False
    
    # ============ RESULT METHODS ============
    
    def save_result(self, match_id: str, actual_winner: str) -> bool:
        """
        Save match result.
        
        Args:
            match_id: Match ID
            actual_winner: Actual winner (team name or 'draw')
        
        Returns:
            True if successful, False otherwise
        """
        try:
            result_id = str(uuid.uuid4())
            timestamp = datetime.now(timezone.utc).isoformat()
            
            cursor = self.conn.cursor()
            
            # Save result
            cursor.execute("""
            INSERT OR REPLACE INTO results 
            (result_id, match_id, actual_winner, timestamp)
            VALUES (?, ?, ?, ?)
            """, (result_id, match_id, actual_winner, timestamp))
            
            # Update match status to completed
            cursor.execute(
                "UPDATE matches SET status = 'completed' WHERE match_id = ?",
                (match_id,)
            )
            
            self.conn.commit()
            logger.info(f"Result saved: {match_id} = {actual_winner}")
            return True
        except Exception as e:
            logger.error(f"Error saving result: {e}")
            return False
    
    def get_result(self, match_id: str) -> Optional[Dict]:
        """
        Get match result.
        
        Args:
            match_id: Match ID
        
        Returns:
            Result dictionary or None
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT * FROM results WHERE match_id = ?",
                (match_id,)
            )
            result = cursor.fetchone()
            return dict(result) if result else None
        except Exception as e:
            logger.error(f"Error getting result: {e}")
            return None
    
    # ============ STATISTICS METHODS ============
    
    def get_user_stats(self, user_id: str) -> Dict:
        """
        Get comprehensive user statistics.
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary with total_predictions, correct_predictions, accuracy, total_points
        """
        try:
            predictions = self.get_user_predictions(user_id)
            
            if not predictions:
                return {
                    'total_predictions': 0,
                    'correct_predictions': 0,
                    'accuracy': 0.0,
                    'total_points': 0
                }
            
            total = len(predictions)
            correct = 0
            total_points = 0
            
            for pred in predictions:
                result = self.get_result(pred['match_id'])
                
                if result:
                    # Check if prediction is correct
                    if result['actual_winner'] == pred['predicted_winner']:
                        correct += 1
                        # Award points: 3 for winner, 2 for draw
                        if pred['predicted_winner'] == 'draw':
                            total_points += 2
                        else:
                            total_points += 3
            
            accuracy = (correct / total * 100) if total > 0 else 0.0
            
            return {
                'total_predictions': total,
                'correct_predictions': correct,
                'accuracy': round(accuracy, 2),
                'total_points': total_points
            }
        
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {
                'total_predictions': 0,
                'correct_predictions': 0,
                'accuracy': 0.0,
                'total_points': 0
            }
    
    # ============ LEADERBOARD METHODS ============
    
    def get_leaderboard(self, limit: int = 100) -> List[Dict]:
        """
        Get leaderboard with user rankings.
        
        Args:
            limit: Maximum number of users to return
        
        Returns:
            List of leaderboard entries sorted by points
        """
        try:
            users = self.get_all_users()
            leaderboard = []
            
            for user in users:
                stats = self.get_user_stats(user['user_id'])
                leaderboard.append({
                    'rank': 0,  # Will be set below
                    'user_id': user['user_id'],
                    'user_name': user['user_name'],
                    'email': user.get('email', ''),
                    'country': user.get('country', ''),
                    'total_predictions': stats['total_predictions'],
                    'correct_predictions': stats['correct_predictions'],
                    'accuracy': stats['accuracy'],
                    'total_points': stats['total_points']
                })
            
            # Sort by points (descending), then by accuracy
            leaderboard.sort(
                key=lambda x: (x['total_points'], x['accuracy']),
                reverse=True
            )
            
            # Add ranks
            for rank, entry in enumerate(leaderboard[:limit], 1):
                entry['rank'] = rank
            
            return leaderboard[:limit]
        
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []
    
    def get_user_rank(self, user_id: str) -> Optional[int]:
        """
        Get user's leaderboard rank.
        
        Args:
            user_id: User ID
        
        Returns:
            Rank (1-based) or None if user not found
        """
        try:
            leaderboard = self.get_leaderboard(1000)
            for entry in leaderboard:
                if entry['user_id'] == user_id:
                    return entry['rank']
            return None
        except Exception as e:
            logger.error(f"Error getting user rank: {e}")
            return None
    
    # ============ ADMIN METHODS ============
    
    def count_table(self, table_name: str) -> int:
        """
        Count rows in a table.
        
        Args:
            table_name: Table name (users, matches, predictions, results)
        
        Returns:
            Row count
        """
        try:
            valid_tables = ['users', 'matches', 'predictions', 'results']
            if table_name not in valid_tables:
                logger.warning(f"Invalid table name: {table_name}")
                return 0
            
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            result = cursor.fetchone()
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Error counting table {table_name}: {e}")
            return 0
    
    def clear_predictions(self) -> bool:
        """
        Clear all predictions (admin only).
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM predictions")
            self.conn.commit()
            logger.warning("All predictions cleared by admin")
            return True
        except Exception as e:
            logger.error(f"Error clearing predictions: {e}")
            return False
    
    def clear_results(self) -> bool:
        """
        Clear all results (admin only).
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM results")
            # Reset match statuses
            cursor.execute("UPDATE matches SET status = 'scheduled'")
            self.conn.commit()
            logger.warning("All results cleared by admin")
            return True
        except Exception as e:
            logger.error(f"Error clearing results: {e}")
            return False
    
    def clear_all_data(self) -> bool:
        """
        Clear all data from database (admin only).
        WARNING: This is irreversible!
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM predictions")
            cursor.execute("DELETE FROM results")
            cursor.execute("DELETE FROM matches")
            cursor.execute("DELETE FROM users")
            self.conn.commit()
            logger.warning("ALL DATA CLEARED BY ADMIN - THIS IS IRREVERSIBLE!")
            return True
        except Exception as e:
            logger.error(f"Error clearing all data: {e}")
            return False
    
    def get_database_stats(self) -> Dict:
        """
        Get overall database statistics.
        
        Returns:
            Dictionary with counts of all tables
        """
        try:
            return {
                'users': self.count_table('users'),
                'matches': self.count_table('matches'),
                'predictions': self.count_table('predictions'),
                'results': self.count_table('results')
            }
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {}
    
    def process_match_result(self, match_id: str, actual_winner: str) -> int:
        """
        Process a match result and award points to users.
        
        Args:
            match_id: Match ID
            actual_winner: Actual winner
        
        Returns:
            Number of predictions processed
        """
        try:
            # Save result
            if not self.save_result(match_id, actual_winner):
                return 0
            
            # Get all predictions for this match
            predictions = self.get_match_predictions(match_id)
            processed = 0
            
            # Update points for each prediction
            for pred in predictions:
                points = 0
                if pred['predicted_winner'] == actual_winner:
                    points = 2 if actual_winner == 'draw' else 3
                
                self.update_prediction_points(pred['prediction_id'], points)
                processed += 1
            
            logger.info(f"Processed {processed} predictions for match {match_id}")
            return processed
        
        except Exception as e:
            logger.error(f"Error processing match result: {e}")
            return 0
    
    # ============ UTILITY METHODS ============
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def commit(self):
        """Commit pending transactions."""
        try:
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error committing transaction: {e}")
    
    def rollback(self):
        """Rollback pending transactions."""
        try:
            self.conn.rollback()
        except Exception as e:
            logger.error(f"Error rolling back transaction: {e}")


# Global storage instance
_storage = None


def get_storage(db_path: str = "database.db") -> Storage:
    """
    Get or create global storage instance.
    
    Args:
        db_path: Path to database file
    
    Returns:
        Storage instance
    """
    global _storage
    
    if _storage is None:
        _storage = Storage(db_path)
    
    return _storage


def reset_storage():
    """Reset global storage instance."""
    global _storage
    if _storage:
        _storage.close()
    _storage = None
