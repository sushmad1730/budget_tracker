# Personal Budget Tracker

A Python-based command-line application for tracking personal finances, managing expenses, and setting budget limits.

## Features

- ✓ Add income and expense transactions
- ✓ Track spending by categories
- ✓ View balance and monthly summaries
- ✓ Set budget limits for categories
- ✓ Get alerts when budgets are exceeded
- ✓ Detailed category breakdown reports
- ✓ SQLite database for data persistence
- ✓ Comprehensive logging

## Project Structure

```
SAMPLE_PROJECT/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── database.py          # Database operations
│   ├── budget.py            # Budget management logic
│   ├── cli.py               # Command-line interface
├── tests/
│   ├── __init__.py
│   ├── test_database.py     # Database tests
│   ├── test_budget.py       # Budget manager tests
├── data/                    # Data storage (created at runtime)
├── requirements.txt         # Project dependencies
├── README.md               # This file
└── .gitignore             # Git ignore rules
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or navigate to the project directory:
```bash
cd SAMPLE_PROJECT
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python -m src.cli
```

### Main Menu Options

1. **Add Income** - Record income transactions
2. **Add Expense** - Record expense transactions
3. **View Balance** - See total income, expenses, and balance
4. **View Monthly Summary** - Get summary for a specific month
5. **View Category Breakdown** - See spending by category
6. **Set Budget Limit** - Set spending limits for categories
7. **Check Budget Exceeded** - View budget overages
8. **Exit** - Close the application

### Example Workflow

```
1. Add Income
   Category: Salary
   Amount: 5000
   Description: Monthly salary

2. Add Expense
   Category: Food
   Amount: 300
   Description: Monthly groceries

3. View Balance
   Total Income: $5000.00
   Total Expenses: $300.00
   Balance: $4700.00

4. Set Budget Limit
   Category: Food
   Limit: 400
   Month: 2024-01

5. Check Budget Exceeded
   All budgets are within limits!
```

## Testing

Run unit tests using pytest:

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=src tests/
```

## Supported Categories

### Income Categories
- Salary
- Bonus
- Investment
- Freelance

### Expense Categories
- Food
- Transport
- Utilities
- Entertainment
- Healthcare
- Shopping
- Other

## Database

The application uses SQLite database stored at `data/budget.db`. 

### Tables

**transactions**
- id: Primary key
- date: Transaction date (YYYY-MM-DD)
- amount: Transaction amount
- category: Transaction category
- description: Transaction description
- type: Transaction type (income/expense)
- created_at: Creation timestamp

**budget_limits**
- id: Primary key
- category: Expense category
- limit_amount: Budget limit
- month: Month (YYYY-MM)

## Logging

The application maintains a log file at `budget_app.log` with all operations and errors.

## Development Notes

- All code includes type hints for better IDE support
- Follows PEP 8 code style guidelines
- Comprehensive docstrings for all modules and functions
- Error handling for all user inputs
- Database operations use parameterized queries to prevent SQL injection

## Future Enhancements (for DevOps)

Once you master development, these can be added during DevOps learning:
- Docker containerization
- CI/CD pipelines (GitHub Actions, Jenkins)
- API layer (REST API)
- Multiple environment configurations
- Database migrations
- Performance monitoring
- Health checks
- Automated testing in CI/CD

## License

Open source for educational purposes.

## Author

Developer
