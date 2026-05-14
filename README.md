# Expense-Behaviour-Saving-Analyzer

A web-based personal finance management application with machine learning-powered expense analysis. Track your income and expenses, get intelligent financial insights, and understand your spending patterns.

## Features

- **User Authentication**: Secure login and registration system
- **Income & Expense Tracking**: Record and categorize your financial transactions
- **ML-Powered Analytics**: AI-driven financial behavior analysis and classification
- **Financial Insights**: 
  - Savings rate analysis
  - Essential vs. non-essential spending breakdown
  - Category-wise expense tracking
  - Financial behavior classification (Good Saver, Average Saver, Overspender)
- **Budget Monitoring**: Configurable spending thresholds by category
- **Responsive UI**: Clean, user-friendly web interface
- **Data Persistence**: SQLite database for reliable data storage

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQL
- **Authentication**: Flask-Login
- **ML Analysis**: NumPy-based expense analyzer
- **API Support**: CORS enabled for cross-origin requests

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download the project:
```bash
cd finance2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5001
```

## Project Structure

```
finance2/
├── app.py                 # Main Flask application
├── models.py             # Database models (User, Income, Expense)
├── ml_analyzer.py        # ML-based financial behavior analyzer
├── config.py             # Application configuration
├── requirements.txt      # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css    # Application styling
│   └── js/
│       └── app.js       # Frontend JavaScript logic
├── templates/
│   ├── index.html       # Main dashboard
│   ├── login.html       # Login page
│   └── register.html    # Registration page
└── instance/            # Instance-specific files
```

## Configuration

Key configuration settings in `config.py`:

- **Database**: SQL database at `expense_analyzer.db`
- **Savings Rate Classification**:
  - Good Saver: > 30% savings rate
  - Average Saver: 10-30% savings rate
  - Overspender: < 10% savings rate

- **Category Spending Thresholds** (% of income):
  - Dining & Restaurants: 15%
  - Entertainment: 10%
  - Shopping: 15%
  - Travel & Vacation: 10%
  - Personal Care: 5%

- **Essential Categories**:
  - Food & Groceries, Housing, Utilities, Transportation, Healthcare, Education, Family & Dependents

- **Non-Essential Categories**:
  - Dining & Restaurants, Entertainment, Shopping, Travel & Vacation, Personal Care, Gifts & Donations, Subscriptions, Others

## Usage

### User Registration
1. Click on "Register" on the login page
2. Enter your username, name, and password
3. Submit to create your account

### Recording Transactions

**Income**:
1. Navigate to the dashboard
2. Click "Add Income"
3. Select category, enter amount, source, and description
4. Save

**Expenses**:
1. Click "Add Expense"
2. Select category, enter amount, and description
3. Save

### Viewing Analytics

The dashboard displays:
- Total income and expenses
- Current savings rate
- Essential vs. non-essential spending breakdown
- Category-wise expense distribution
- Financial behavior classification with personalized insights

## API Endpoints

The application provides RESTful endpoints for:
- User authentication (login/logout)
- Income management (create, read, update, delete)
- Expense management (create, read, update, delete)
- Financial analytics and behavior analysis
- Category suggestions based on spending patterns

## Dependencies

- Flask==3.0.0 - Web framework
- Flask-SQLAlchemy==3.1.1 - ORM
- Flask-CORS==4.0.0 - Cross-Origin Resource Sharing
- Flask-Login==0.6.3 - User session management
- Werkzeug==3.0.1 - Security utilities
- NumPy - Numerical computing for ML analysis

## Database Models

### User
- id, username (unique), name, password_hash, created_at
- Relationships: incomes, expenses

### Income
- id, user_id, amount, category, source, date, description, created_at

### Expense
- id, user_id, amount, category, date, description, created_at

## Security Notes

- Change the `SECRET_KEY` in `config.py` for production
- Passwords are hashed using Werkzeug security utilities
- Use environment variables for sensitive configuration in production
- CORS is enabled for local development; configure appropriately for production

## Future Enhancements

- Budget goal setting and tracking
- Expense forecasting using advanced ML models
- Mobile app support
- Data export (CSV, PDF)
- Multi-currency support
- Recurring transaction templates
- Financial recommendations engine

## License

This project is provided as-is for personal use and educational purposes.
