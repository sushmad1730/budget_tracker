"""
Database module for managing budget transactions.
"""

import sqlite3
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Database:
    """Handles all database operations for budget tracking."""
    
    def __init__(self, db_path: str = "data/budget.db") -> None:
        """
        Initialize database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.connection: Optional[sqlite3.Connection] = None
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize database schema."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT,
                    type TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Create budget limits table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budget_limits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT UNIQUE NOT NULL,
                    limit_amount REAL NOT NULL,
                    month TEXT NOT NULL
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info(f"Database initialized at {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def add_transaction(
        self,
        date: str,
        amount: float,
        category: str,
        description: str,
        transaction_type: str
    ) -> None:
        """
        Add a transaction to the database.
        
        Args:
            date: Transaction date (YYYY-MM-DD)
            amount: Transaction amount
            category: Transaction category
            description: Transaction description
            transaction_type: Type of transaction (income/expense)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO transactions 
                (date, amount, category, description, type, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                date,
                amount,
                category,
                description,
                transaction_type,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"Transaction added: {category} - {amount}")
        except sqlite3.Error as e:
            logger.error(f"Error adding transaction: {e}")
            raise
    
    def get_transactions(
        self,
        category: Optional[str] = None,
        transaction_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve transactions from the database.
        
        Args:
            category: Filter by category (optional)
            transaction_type: Filter by type (income/expense) (optional)
        
        Returns:
            List of transaction dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM transactions WHERE 1=1"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            if transaction_type:
                query += " AND type = ?"
                params.append(transaction_type)
            
            query += " ORDER BY date DESC"
            
            cursor.execute(query, params)
            transactions = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            return transactions
        except sqlite3.Error as e:
            logger.error(f"Error retrieving transactions: {e}")
            raise
    
    def get_balance(self) -> Dict[str, float]:
        """
        Calculate total income, expenses, and balance.
        
        Returns:
            Dictionary with income, expenses, and balance
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT SUM(amount) FROM transactions WHERE type = 'income'"
            )
            income = cursor.fetchone()[0] or 0.0
            
            cursor.execute(
                "SELECT SUM(amount) FROM transactions WHERE type = 'expense'"
            )
            expenses = cursor.fetchone()[0] or 0.0
            
            conn.close()
            
            return {
                "income": income,
                "expenses": expenses,
                "balance": income - expenses
            }
        except sqlite3.Error as e:
            logger.error(f"Error calculating balance: {e}")
            raise
    
    def set_budget_limit(
        self,
        category: str,
        limit_amount: float,
        month: str
    ) -> None:
        """
        Set a budget limit for a category.
        
        Args:
            category: Category name
            limit_amount: Budget limit amount
            month: Month in YYYY-MM format
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO budget_limits 
                (category, limit_amount, month)
                VALUES (?, ?, ?)
            """, (category, limit_amount, month))
            
            conn.commit()
            conn.close()
            logger.info(f"Budget limit set: {category} - {limit_amount}")
        except sqlite3.Error as e:
            logger.error(f"Error setting budget limit: {e}")
            raise
    
    def get_budget_limits(self, month: str) -> List[Dict[str, Any]]:
        """
        Get all budget limits for a specific month.
        
        Args:
            month: Month in YYYY-MM format
        
        Returns:
            List of budget limit dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM budget_limits WHERE month = ?",
                (month,)
            )
            limits = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            return limits
        except sqlite3.Error as e:
            logger.error(f"Error retrieving budget limits: {e}")
            raise
