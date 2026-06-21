"""
Prediction management module with timezone support.

Handles checking if predictions can be made, creating predictions,
and managing prediction logic with proper ET/IST timezone handling.
"""

import logging
from datetime import datetime, timezone, timedelta
import uuid

logger = logging.getLogger(__name__)


class PredictionManager:
    """Manages poll predictions with timezone awareness."""
    
    def __init__(self, config, storage):
        """
        Initialize prediction manager.
        
        Args:
            config: Configuration object
            storage: Storage/database object
        """
        self.config = config
        self.storage = storage
    
    def can_predict(self, match_id: str) -> tuple:
        """
        Check if a prediction can be made for a match.
        
        Args:
            match_id: Match ID to check
        
        Returns:
            Tuple of (can_predict: bool, reason: str)
        """
        try:
            # Get match from storage
            match = self.storage.get_match(match_id)
            
            if not match:
                return False, "Match not found"
            
            # Check if match is scheduled
            if isinstance(match, dict):
                status = match.get('status', '').lower()
            else:
                status = getattr(match, 'status', 'scheduled').lower()
            
            if status != 'scheduled':
                return False, f"Match is {status.upper()}"
            
            # Get match datetime
            try:
                if isinstance(match, dict):
                    # Handle dictionary response
                    match_date = match.get('match_date')
                    kickoff_time = match.get('kickoff_time')
                    
                    if not match_date or not kickoff_time:
                        return True, ""  # Allow prediction if time info missing
                    
                    # Parse ET datetime
                    try:
                        dt_str = f"{match_date} {kickoff_time}"
                        match_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                    except ValueError:
                        try:
                            match_dt = datetime.strptime(str(match_date), "%Y-%m-%d")
                        except ValueError:
                            return True, ""  # Allow prediction if parsing fails
                else:
                    # Handle object response
                    if hasattr(match, 'match_datetime'):
                        match_dt = match.match_datetime
                    elif hasattr(match, 'end_at'):
                        match_dt = match.end_at
                    else:
                        return True, ""  # Allow prediction if no time info
            
            except Exception as e:
                logger.warning(f"Error parsing match datetime: {e}")
                return True, ""  # Allow prediction if parsing fails
            
            # Convert to IST if needed (assume ET input)
            try:
                from src.worldcup_polls.timezone_utils import TimezoneConverter
                ist_match_dt = TimezoneConverter.et_to_ist(match_dt)
            except ImportError:
                # Fallback: add 9.5 hours for ET to IST
                ist_match_dt = match_dt + timedelta(hours=9, minutes=30)
            except Exception as e:
                logger.warning(f"Error converting timezone: {e}")
                ist_match_dt = match_dt
            
            # Compare with current time
            now = datetime.now()
            
            if now >= ist_match_dt:
                return False, "Match has started"
            
            return True, ""
        
        except Exception as e:
            logger.error(f"Error in can_predict: {e}")
            return True, ""  # Allow prediction if error occurs
    
    def make_prediction(self, user_id: str, match_id: str, predicted_winner: str) -> tuple:
        """
        Create a prediction for a match.
        
        Args:
            user_id: User ID
            match_id: Match ID
            predicted_winner: Predicted winner (team name or 'draw')
        
        Returns:
            Tuple of (success: bool, message: str, prediction_id: str or None)
        """
        try:
            # Validate inputs
            if not user_id or not match_id or not predicted_winner:
                return False, "Missing required fields", None
            
            # Check if can predict
            can_pred, reason = self.can_predict(match_id)
            if not can_pred:
                return False, reason, None
            
            # Check if already predicted
            existing = self.storage.get_prediction(match_id, user_id)
            if existing:
                return False, "You have already predicted for this match", None
            
            # Create prediction
            prediction_id = str(uuid.uuid4())
            
            try:
                success = self.storage.create_prediction(
                    prediction_id=prediction_id,
                    user_id=user_id,
                    match_id=match_id,
                    predicted_winner=predicted_winner,
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                
                if success:
                    logger.info(
                        f"Prediction created: user={user_id}, match={match_id}, "
                        f"winner={predicted_winner}"
                    )
                    return True, f"✅ Predicted {predicted_winner}!", prediction_id
                else:
                    return False, "Failed to save prediction", None
            
            except Exception as e:
                logger.error(f"Error creating prediction in storage: {e}")
                return False, "Error saving prediction", None
        
        except Exception as e:
            logger.error(f"Error in make_prediction: {e}")
            return False, "An error occurred", None
    
    def get_user_predictions(self, user_id: str):
        """
        Get all predictions for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            List of predictions
        """
        try:
            return self.storage.get_user_predictions(user_id)
        except Exception as e:
            logger.error(f"Error getting user predictions: {e}")
            return []
    
    def get_match_predictions(self, match_id: str):
        """
        Get all predictions for a match.
        
        Args:
            match_id: Match ID
        
        Returns:
            List of predictions
        """
        try:
            return self.storage.get_match_predictions(match_id)
        except Exception as e:
            logger.error(f"Error getting match predictions: {e}")
            return []
    
    def get_prediction_stats(self, user_id: str) -> dict:
        """
        Get prediction statistics for a user.
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary with statistics
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
                # Check if match has result
                result = self.storage.get_match_result(pred.get('match_id'))
                
                if result:
                    actual_winner = result.get('actual_winner')
                    predicted = pred.get('predicted_winner')
                    
                    if actual_winner == predicted:
                        correct += 1
                        # Award points
                        if predicted == 'draw':
                            total_points += 2
                        else:
                            total_points += 3
            
            accuracy = (correct / total * 100) if total > 0 else 0.0
            
            return {
                'total_predictions': total,
                'correct_predictions': correct,
                'accuracy': accuracy,
                'total_points': total_points
            }
        
        except Exception as e:
            logger.error(f"Error getting prediction stats: {e}")
            return {
                'total_predictions': 0,
                'correct_predictions': 0,
                'accuracy': 0.0,
                'total_points': 0
            }
    
    def process_match_result(self, match_id: str, actual_winner: str) -> bool:
        """
        Process result for a match and award points.
        
        Args:
            match_id: Match ID
            actual_winner: Actual winner
        
        Returns:
            Success status
        """
        try:
            # Get all predictions for match
            predictions = self.get_match_predictions(match_id)
            
            for pred in predictions:
                user_id = pred.get('user_id')
                predicted = pred.get('predicted_winner')
                
                # Calculate points
                if predicted == actual_winner:
                    if predicted == 'draw':
                        points = 2
                    else:
                        points = 3
                else:
                    points = 0
                
                # Update prediction with points (if storage supports it)
                try:
                    if hasattr(self.storage, 'update_prediction_points'):
                        self.storage.update_prediction_points(
                            pred.get('prediction_id'),
                            points
                        )
                except:
                    pass  # Storage may not support this
            
            logger.info(f"Processed results for match {match_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error processing match result: {e}")
            return False


class PredictionValidator:
    """Validates prediction data."""
    
    @staticmethod
    def validate_winner(winner: str) -> bool:
        """
        Validate predicted winner.
        
        Args:
            winner: Predicted winner
        
        Returns:
            True if valid, False otherwise
        """
        if not winner:
            return False
        
        # Allow team names and 'draw'
        return isinstance(winner, str) and len(winner.strip()) > 0
    
    @staticmethod
    def validate_match_id(match_id: str) -> bool:
        """
        Validate match ID.
        
        Args:
            match_id: Match ID
        
        Returns:
            True if valid, False otherwise
        """
        if not match_id:
            return False
        
        return isinstance(match_id, str) and len(match_id.strip()) > 0
    
    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        """
        Validate user ID.
        
        Args:
            user_id: User ID
        
        Returns:
            True if valid, False otherwise
        """
        if not user_id:
            return False
        
        return isinstance(user_id, str) and len(user_id.strip()) > 0
