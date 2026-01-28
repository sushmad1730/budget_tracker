"""
Unit tests for budget manager module.
"""

import pytest
import os
from src.database import Database
from src.budget import BudgetManager


@pytest.fixture
def setup_budget():
    """Setup budget manager with temporary database."""
    db_path = "test_budget_manager.db"
    db = Database(db_path)
    manager = BudgetManager(db)
    yield manager
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


def test_add_income(setup_budget):
    """Test adding income."""
    manager = setup_budget
    manager.add_income(1000.00, "Salary", "Monthly salary")
    
    transactions = manager.db.get_transactions(transaction_type="income")
    assert len(transactions) == 1
    assert transactions[0]["amount"] == 1000.00


def test_add_expense(setup_budget):
    """Test adding expense."""
    manager = setup_budget
    manager.add_expense(50.00, "Food", "Groceries")
    
    transactions = manager.db.get_transactions(transaction_type="expense")
    assert len(transactions) == 1
    assert transactions[0]["amount"] == 50.00


def test_invalid_income_category(setup_budget):
    """Test invalid income category."""
    manager = setup_budget
    
    with pytest.raises(ValueError):
        manager.add_income(1000.00, "Invalid", "Test")


def test_invalid_expense_category(setup_budget):
    """Test invalid expense category."""
    manager = setup_budget
    
    with pytest.raises(ValueError):
        manager.add_expense(50.00, "Invalid", "Test")


def test_negative_amount(setup_budget):
    """Test negative amount."""
    manager = setup_budget
    
    with pytest.raises(ValueError):
        manager.add_income(-100.00, "Salary", "Test")
    
    with pytest.raises(ValueError):
        manager.add_expense(-50.00, "Food", "Test")


def test_monthly_summary(setup_budget):
    """Test monthly summary calculation."""
    manager = setup_budget
    
    manager.add_income(1000.00, "Salary", "Monthly salary", "2024-01-15")
    manager.add_expense(50.00, "Food", "Groceries", "2024-01-16")
    manager.add_expense(30.00, "Transport", "Bus", "2024-01-16")
    
    summary = manager.get_monthly_summary(2024, 1)
    
    assert summary["income"] == 1000.00
    assert summary["expenses"] == 80.00
    assert summary["balance"] == 920.00
    assert summary["transaction_count"] == 3


def test_category_breakdown(setup_budget):
    """Test category breakdown."""
    manager = setup_budget
    
    manager.add_expense(50.00, "Food", "Groceries")
    manager.add_expense(30.00, "Food", "Restaurant")
    manager.add_expense(20.00, "Transport", "Bus")
    
    breakdown = manager.get_category_breakdown("expense")
    
    assert breakdown["Food"] == 80.00
    assert breakdown["Transport"] == 20.00


def test_check_budget_exceeded(setup_budget):
    """Test budget exceeded check."""
    manager = setup_budget
    
    manager.db.set_budget_limit("Food", 100.00, "2024-01")
    
    manager.add_expense(50.00, "Food", "Groceries", "2024-01-15")
    manager.add_expense(60.00, "Food", "Restaurant", "2024-01-16")
    
    exceeded = manager.check_budget_exceeded("2024-01")
    
    assert len(exceeded) == 1
    assert exceeded[0]["category"] == "Food"
    assert exceeded[0]["spent"] == 110.00
    assert exceeded[0]["exceeded_by"] == 10.00


def test_get_valid_categories(setup_budget):
    """Test getting valid categories."""
    manager = setup_budget
    
    income_cats = manager.get_valid_categories("income")
    expense_cats = manager.get_valid_categories("expense")
    
    assert "Salary" in income_cats
    assert "Food" in expense_cats
