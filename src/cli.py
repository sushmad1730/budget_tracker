"""
Command-line interface for the Budget Tracker application.
"""

import sys
import logging
from typing import Optional
from datetime import datetime
from src.database import Database
from src.budget import BudgetManager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("budget_app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CLI:
    """Command-line interface for budget tracker."""
    
    def __init__(self) -> None:
        """Initialize CLI."""
        self.db = Database("data/budget.db")
        self.manager = BudgetManager(self.db)
    
    def print_header(self, text: str) -> None:
        """Print formatted header."""
        print("\n" + "=" * 50)
        print(f"  {text}")
        print("=" * 50)
    
    def print_menu(self) -> None:
        """Print main menu."""
        self.print_header("PERSONAL BUDGET TRACKER")
        print("""
1. Add Income
2. Add Expense
3. View Balance
4. View Monthly Summary
5. View Category Breakdown
6. Set Budget Limit
7. Check Budget Exceeded
8. Exit
        """)
    
    def add_income(self) -> None:
        """Add income transaction."""
        try:
            print("\n--- Add Income ---")
            print(f"Valid categories: {', '.join(self.manager.get_valid_categories('income'))}")
            
            category = input("Enter category: ").strip()
            amount = float(input("Enter amount: "))
            description = input("Enter description: ").strip()
            date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            
            date = date_input if date_input else datetime.now().strftime("%Y-%m-%d")
            
            self.manager.add_income(amount, category, description, date)
            print("✓ Income added successfully!")
        
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error adding income: {e}")
            print(f"✗ An error occurred: {e}")
    
    def add_expense(self) -> None:
        """Add expense transaction."""
        try:
            print("\n--- Add Expense ---")
            print(f"Valid categories: {', '.join(self.manager.get_valid_categories('expense'))}")
            
            category = input("Enter category: ").strip()
            amount = float(input("Enter amount: "))
            description = input("Enter description: ").strip()
            date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            
            date = date_input if date_input else datetime.now().strftime("%Y-%m-%d")
            
            self.manager.add_expense(amount, category, description, date)
            print("✓ Expense added successfully!")
        
        except ValueError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error adding expense: {e}")
            print(f"✗ An error occurred: {e}")
    
    def view_balance(self) -> None:
        """View current balance."""
        try:
            balance_info = self.db.get_balance()
            
            self.print_header("Current Balance")
            print(f"Total Income:     ${balance_info['income']:.2f}")
            print(f"Total Expenses:   ${balance_info['expenses']:.2f}")
            print(f"Balance:          ${balance_info['balance']:.2f}")
        
        except Exception as e:
            logger.error(f"Error viewing balance: {e}")
            print(f"✗ Error: {e}")
    
    def view_monthly_summary(self) -> None:
        """View monthly summary."""
        try:
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (MM): "))
            
            summary = self.manager.get_monthly_summary(year, month)
            
            self.print_header(f"Monthly Summary - {summary['month']}")
            print(f"Income:           ${summary['income']:.2f}")
            print(f"Expenses:         ${summary['expenses']:.2f}")
            print(f"Balance:          ${summary['balance']:.2f}")
            print(f"Transactions:     {summary['transaction_count']}")
        
        except ValueError:
            print("✗ Invalid input for year or month")
        except Exception as e:
            logger.error(f"Error viewing monthly summary: {e}")
            print(f"✗ Error: {e}")
    
    def view_category_breakdown(self) -> None:
        """View spending by category."""
        try:
            print("\n--- Category Breakdown ---")
            print("1. Income")
            print("2. Expense")
            choice = input("Select type: ").strip()
            
            if choice == "1":
                trans_type = "income"
            elif choice == "2":
                trans_type = "expense"
            else:
                print("✗ Invalid choice")
                return
            
            breakdown = self.manager.get_category_breakdown(trans_type)
            
            self.print_header(f"Category Breakdown - {trans_type.capitalize()}")
            if breakdown:
                total = sum(breakdown.values())
                for category, amount in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
                    percentage = (amount / total * 100) if total > 0 else 0
                    print(f"{category:20} ${amount:10.2f} ({percentage:5.1f}%)")
                print(f"\n{'Total':20} ${total:10.2f}")
            else:
                print("No transactions found")
        
        except Exception as e:
            logger.error(f"Error viewing category breakdown: {e}")
            print(f"✗ Error: {e}")
    
    def set_budget_limit(self) -> None:
        """Set budget limit for a category."""
        try:
            print("\n--- Set Budget Limit ---")
            category = input("Enter expense category: ").strip()
            limit = float(input("Enter budget limit: "))
            month = input("Enter month (YYYY-MM): ").strip()
            
            self.db.set_budget_limit(category, limit, month)
            print("✓ Budget limit set successfully!")
        
        except ValueError:
            print("✗ Invalid input")
        except Exception as e:
            logger.error(f"Error setting budget limit: {e}")
            print(f"✗ Error: {e}")
    
    def check_budget_exceeded(self) -> None:
        """Check if budget limits are exceeded."""
        try:
            month = input("Enter month (YYYY-MM): ").strip()
            exceeded = self.manager.check_budget_exceeded(month)
            
            self.print_header(f"Budget Check - {month}")
            if exceeded:
                print("⚠ Budget Exceeded:")
                for item in exceeded:
                    print(f"\n  Category: {item['category']}")
                    print(f"  Limit:    ${item['limit']:.2f}")
                    print(f"  Spent:    ${item['spent']:.2f}")
                    print(f"  Exceeded: ${item['exceeded_by']:.2f}")
            else:
                print("✓ All budgets are within limits!")
        
        except Exception as e:
            logger.error(f"Error checking budget: {e}")
            print(f"✗ Error: {e}")
    
    def run(self) -> None:
        """Run the CLI application."""
        logger.info("Budget Tracker application started")
        
        while True:
            self.print_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == "1":
                self.add_income()
            elif choice == "2":
                self.add_expense()
            elif choice == "3":
                self.view_balance()
            elif choice == "4":
                self.view_monthly_summary()
            elif choice == "5":
                self.view_category_breakdown()
            elif choice == "6":
                self.set_budget_limit()
            elif choice == "7":
                self.check_budget_exceeded()
            elif choice == "8":
                print("\n✓ Thank you for using Budget Tracker!")
                logger.info("Budget Tracker application closed")
                sys.exit(0)
            else:
                print("✗ Invalid choice. Please try again.")


def main() -> None:
    """Main entry point."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
