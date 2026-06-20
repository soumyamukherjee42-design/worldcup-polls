"""
Database operations and query execution engine
"""
import sqlite3
import uuid
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class Database:
    """Wrapper for thread-safe SQLite operations"""
    
    def __init__(self, db_path: Path):
        """Initialize database connection handler"""
        self.db_path = db_path
    
    def _get_connection(self) -> sqlite3.Connection:
        """
        Creates a connection with highly-optimized concurrency settings.
        WAL mode is critical for Streamlit apps handling multiple users.
        """
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row  # Returns results as dict-like objects
        
        # Performance & Concurrency Pragmas
        conn.execute("PRAGMA journal_mode = WAL;")  # Write-Ahead Logging
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def execute(self, query: str, params: tuple = ()) -> bool:
        """Execute a query that alters data (INSERT/UPDATE/DELETE)"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Execute error on query [{query}]: {e}")
            return False

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch a single row as a dictionary"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                result = cursor.fetchone()
                return dict(result) if result else None
        except Exception as e:
            logger.error(f"Fetch_one error on query [{query}]: {e}")
            return None

    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch multiple rows as a list of dictionaries"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                results = cursor.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Fetch_all error on query [{query}]: {e}")
            return []

    def insert(self, table: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Dynamically insert a dictionary into a table.
        Returns the generated or provided ID.
        """
        try:
            # Ensure there's an ID (or generate one)
            record_id = data.get(f"{table[:-1]}_id") or data.get('id') or str(uuid.uuid4())
            
            # Map out column names and value placeholders (?, ?, ?)
            columns = ', '.join(data.keys())
            placeholders = ', '.join('?' * len(data))
            values = tuple(data.values())
            
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
                
            return record_id
        except Exception as e:
            logger.error(f"Insert error in table [{table}]: {e}")
            return None

    def update(self, table: str, data: Dict[str, Any], where: str, where_params: tuple = ()) -> bool:
        """Dynamically update records based on a dictionary"""
        try:
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            values = tuple(data.values()) + where_params
            
            query = f"UPDATE {table} SET {set_clause} WHERE {where}"
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, values)
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Update error in table [{table}]: {e}")
            return False

    def count(self, table: str, where: str = "", where_params: tuple = ()) -> int:
        """Count records matching a condition"""
        try:
            query = f"SELECT COUNT(*) as count FROM {table}"
            if where:
                query += f" WHERE {where}"
            
            result = self.fetch_one(query, where_params)
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Count error in table [{table}]: {e}")
            return 0
