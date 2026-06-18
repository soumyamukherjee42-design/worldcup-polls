"""
Job to refresh match results
Run periodically or manually
"""
import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.storage import Storage
from src.simulator import ResultSimulator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Refresh match results."""
    logger.info("Starting result refresh job")
    
    config = Config()
    storage = Storage(config)
    storage.initialize_data_layer()
    
    simulator = ResultSimulator(config, storage)
    
    # Auto-simulate completed matches
    count = simulator.auto_simulate_completed_matches()
    logger.info(f"Refreshed {count} match results")


if __name__ == "__main__":
    main()
