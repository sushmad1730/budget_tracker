"""
Budget management module for operations and analytics.
"""

from typing import Dict, List, Any
from datetime import datetime
from src.database import Database
import logging

logger = logging.getLogger(__name__)


class BudgetManager:
    """Manages budget operations and analytics."""
    
    def __init__(self, database: Database) -> None:
        """
        Initialize BudgetManager.
        
        Args:
            database: Database instance
        """
        self.db = database
        self.categories = {
            "income": ["Salary", "Bonus", "Investment", "Freelance"],
            "expense": [
                "Food",
                "Transport",
                "Utilities",
                "Entertainment",
                "Healthcare",
                "Shopping",
                "Other"
            ]
        }
    
    def add_income(
        self,
        amount: float,
        category: str,
        description: str,
        date: str = None
    ) -> None:
        """
        Add an income transaction.
        
        Args:
            amount: Income amount
            category: Income category
            description: Transaction description
            date: Transaction date (default: today)
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if category not in self.categories["income"]:
            raise ValueError(f"Invalid income category: {category}")
        
        if amount <= 0:
            raise ValueError("Income amount must be positive")
        
        self.db.add_transaction(date, amount, category, description, "income")
        logger.info(f"Income added: {category} - {amount}")
    
    def add_expense(
        self,
        amount: float,
        category: str,
        description: str,
        date: str = None
    ) -> None:
        """
        Add an expense transaction.
        
        Args:
            amount: Expense amount
            category: Expense category
            description: Transaction description
            date: Transaction date (default: today)
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if category not in self.categories["expense"]:
            raise ValueError(f"Invalid expense category: {category}")
        
        if amount <= 0:
            raise ValueError("Expense amount must be positive")
        
        self.db.add_transaction(date, amount, category, description, "expense")
        logger.info(f"Expense added: {category} - {amount}")
    
    def get_monthly_summary(self, year: int, month: int) -> Dict[str, Any]:
        """
        Get monthly budget summary.
        
        Args:
            year: Year (YYYY)
            month: Month (MM)
        
        Returns:
            Dictionary with monthly summary
        """
        month_str = f"{year:04d}-{month:02d}"
        transactions = self.db.get_transactions()
        
        month_transactions = [
            t for t in transactions
            if t["date"].startswith(month_str)
        ]
        
        income = sum(
            t["amount"] for t in month_transactions
            if t["type"] == "income"
        )
        expenses = sum(
            t["amount"] for t in month_transactions
            if t["type"] == "expense"
        )
        
        return {
            "month": month_str,
            "income": income,
            "expenses": expenses,
            "balance": income - expenses,
            "transaction_count": len(month_transactions)
        }
    
    def get_category_breakdown(
        self,
        transaction_type: str
    ) -> Dict[str, float]:
        """
        Get spending breakdown by category.
        
        Args:
            transaction_type: Type of transaction (income/expense)
        
        Returns:
            Dictionary with category breakdown
        """
        transactions = self.db.get_transactions(transaction_type=transaction_type)
        
        breakdown: Dict[str, float] = {}
        for transaction in transactions:
            category = transaction["category"]
            amount = transaction["amount"]
            breakdown[category] = breakdown.get(category, 0) + amount
        
        return breakdown
    
    def check_budget_exceeded(
        self,
        month: str
    ) -> List[Dict[str, Any]]:
        """
        Check if any budget limits are exceeded.
        
        Args:
            month: Month in YYYY-MM format
        
        Returns:
            List of exceeded budget categories
        """
        limits = self.db.get_budget_limits(month)
        exceeded = []
        
        for limit in limits:
            category = limit["category"]
            limit_amount = limit["limit_amount"]
            
            transactions = self.db.get_transactions(
                category=category,
                transaction_type="expense"
            )
            
            month_transactions = [
                t for t in transactions
                if t["date"].startswith(month)
            ]
            
            total_spent = sum(t["amount"] for t in month_transactions)
            
            if total_spent > limit_amount:
                exceeded.append({
                    "category": category,
                    "limit": limit_amount,
                    "spent": total_spent,
                    "exceeded_by": total_spent - limit_amount
                })
        
        return exceeded
    
    def get_valid_categories(self, transaction_type: str) -> List[str]:
        """
        Get valid categories for a transaction type.
        
        Args:
            transaction_type: Type of transaction (income/expense)
        
        Returns:
            List of valid categories
        """
        return self.categories.get(transaction_type, [])
