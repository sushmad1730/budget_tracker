"""
Unit tests for database module.
"""

import pytest
import os
from src.database import Database


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    db_path = "test_budget.db"
    db = Database(db_path)
    yield db
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


def test_database_initialization(temp_db):
    """Test database initialization."""
    assert os.path.exists(temp_db.db_path)


def test_add_transaction(temp_db):
    """Test adding a transaction."""
    temp_db.add_transaction(
        date="2024-01-15",
        amount=500.00,
        category="Salary",
        description="Monthly salary",
        transaction_type="income"
    )
    
    transactions = temp_db.get_transactions()
    assert len(transactions) == 1
    assert transactions[0]["amount"] == 500.00
    assert transactions[0]["category"] == "Salary"


def test_get_transactions_filter_by_type(temp_db):
    """Test filtering transactions by type."""
    temp_db.add_transaction(
        date="2024-01-15",
        amount=500.00,
        category="Salary",
        description="Monthly salary",
        transaction_type="income"
    )
    
    temp_db.add_transaction(
        date="2024-01-16",
        amount=50.00,
        category="Food",
        description="Groceries",
        transaction_type="expense"
    )
    
    income_trans = temp_db.get_transactions(transaction_type="income")
    expense_trans = temp_db.get_transactions(transaction_type="expense")
    
    assert len(income_trans) == 1
    assert len(expense_trans) == 1


def test_get_balance(temp_db):
    """Test balance calculation."""
    temp_db.add_transaction(
        date="2024-01-15",
        amount=1000.00,
        category="Salary",
        description="Monthly salary",
        transaction_type="income"
    )
    
    temp_db.add_transaction(
        date="2024-01-16",
        amount=200.00,
        category="Food",
        description="Groceries",
        transaction_type="expense"
    )
    
    balance = temp_db.get_balance()
    assert balance["income"] == 1000.00
    assert balance["expenses"] == 200.00
    assert balance["balance"] == 800.00


def test_set_budget_limit(temp_db):
    """Test setting budget limits."""
    temp_db.set_budget_limit("Food", 300.00, "2024-01")
    
    limits = temp_db.get_budget_limits("2024-01")
    assert len(limits) == 1
    assert limits[0]["category"] == "Food"
    assert limits[0]["limit_amount"] == 300.00


def test_get_budget_limits_empty(temp_db):
    """Test getting budget limits for a month with no limits."""
    limits = temp_db.get_budget_limits("2024-01")
    assert len(limits) == 0
