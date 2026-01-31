import os

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///expense_analyzer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ML Classification Thresholds
    GOOD_SAVER_THRESHOLD = 30  # Savings rate > 30%
    AVERAGE_SAVER_MIN = 10     # Savings rate between 10-30%
    OVERSPENDER_THRESHOLD = 10  # Savings rate < 10%
    
    # Category spending thresholds (% of income)
    CATEGORY_THRESHOLDS = {
        'Dining & Restaurants': 15,
        'Entertainment': 10,
        'Shopping': 15,
        'Travel & Vacation': 10,
        'Personal Care': 5
    }
    
    # Essential vs Non-Essential categories
    ESSENTIAL_CATEGORIES = [
        'Food & Groceries',
        'Housing',
        'Utilities',
        'Transportation',
        'Healthcare',
        'Education',
        'Family & Dependents'
    ]
    
    NON_ESSENTIAL_CATEGORIES = [
        'Dining & Restaurants',
        'Entertainment',
        'Shopping',
        'Travel & Vacation',
        'Personal Care',
        'Gifts & Donations',
        'Subscriptions',
        'Others'
    ]
