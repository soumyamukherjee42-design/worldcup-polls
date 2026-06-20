"""
PostgreSQL Database operations and query execution engine
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
import uuid
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class Database:
    """Wrapper for PostgreSQL operations"""
    
    def __init__(self, db_path=None):
        """Initialize database connection handler using Streamlit Secrets"""
        self.db_url = st.secrets["database"]["URL"]
    
    def _get_connection(self):
        """Creates a connection using RealDictCursor so rows act like dictionaries"""
        return psycopg2.connect(self.db_url, cursor_factory=RealDictCursor)

    def _convert_query(self, query: str) -> str:
        """Converts SQLite '?' placeholders to PostgreSQL '%s' placeholders"""
        return query.replace('?', '%s')

    def execute(self, query: str, params: tuple = ()) -> bool:
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(self._convert_query(query), params)
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Execute error on query [{query}]: {e}")
            return False

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(self._convert_query(query), params)
                    result = cursor.fetchone()
                    return dict(result) if result else None
        except Exception as e:
            logger.error(f"Fetch_one error on query [{query}]: {e}")
            return None

    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(self._convert_query(query), params)
                    results = cursor.fetchall()
                    return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Fetch_all error on query [{query}]: {e}")
            return []

    def insert(self, table: str, data: Dict[str, Any]) -> Optional[str]:
        try:
            record_id = data.get(f"{table[:-1]}_id") or data.get('id') or str(uuid.uuid4())
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data)) # Postgres uses %s
            values = tuple(data.values())
            
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, values)
                conn.commit()
            return record_id
        except Exception as e:
            logger.error(f"Insert error in table [{table}]: {e}")
            return None

    def update(self, table: str, data: Dict[str, Any], where: str, where_params: tuple = ()) -> bool:
        try:
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            values = tuple(data.values()) + where_params
            
            query = f"UPDATE {table} SET {set_clause} WHERE {self._convert_query(where)}"
            
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, values)
                conn.commit()
            return True
        except Exception as e:
            logger.error(f"Update error in table [{table}]: {e}")
            return False

    def count(self, table: str, where: str = "", where_params: tuple = ()) -> int:
        try:
            query = f"SELECT COUNT(*) as count FROM {table}"
            if where:
                query += f" WHERE {self._convert_query(where)}"
            
            result = self.fetch_one(query, where_params)
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Count error in table [{table}]: {e}")
            return 0
