"""
Database Connection & Persistence Session Management
Author: Ravi Ranjan Singh
"""

from typing import Dict, Any, List

class InMemoryDatabase:
    """
    In-memory database store for high-speed local dev and execution.
    Exposes identical interface to relational ORM sessions.
    """
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.workouts: List[Dict[str, Any]] = []
        self.telemetry_logs: List[Dict[str, Any]] = []

db = InMemoryDatabase()

def get_db():
    return db
