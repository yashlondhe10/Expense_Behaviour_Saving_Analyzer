from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from datetime import datetime
from models import db, User, Income, Expense, INCOME_CATEGORIES, EXPENSE_CATEGORIES
from ml_analyzer import ExpenseAnalyzer
from config import Config
from sqlalchemy import extract

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize database
db.init_app(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize ML analyzer
analyzer = ExpenseAnalyzer()

# Create tables and default user
# Create tables
with app.app_context():
    db.create_all()


@app.route('/')
@login_required
def index():
    """Render main page"""
    return render_template('index.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
            
        new_user = User(name=name, username=username)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error registering user: {str(e)}', 'error')
            
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/api/categories', methods=['GET'])
@login_required
def get_categories():
    """Get all income and expense categories"""
    return jsonify({
        'income_categories': INCOME_CATEGORIES,
        'expense_categories': EXPENSE_CATEGORIES
    })


@app.route('/api/income', methods=['POST'])
@login_required
def add_income():
    """Add new income record"""
    try:
        data = request.json
        
        # Parse date
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        income = Income(
            user_id=current_user.id,
            amount=float(data['amount']),
            category=data['category'],
            source=data.get('source', ''),
            date=date_obj,
            description=data.get('description', '')
        )
        
        db.session.add(income)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Income added successfully',
            'income': income.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error adding income: {str(e)}'
        }), 400


@app.route('/api/expense', methods=['POST'])
@login_required
def add_expense():
    """Add new expense record"""
    try:
        data = request.json
        
        # Parse date
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        expense = Expense(
            user_id=current_user.id,
            amount=float(data['amount']),
            category=data['category'],
            date=date_obj,
            description=data.get('description', '')
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Expense added successfully',
            'expense': expense.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error adding expense: {str(e)}'
        }), 400


@app.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions():
    """Get income and expense transactions"""
    try:
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        
        # Base queries
        income_query = Income.query.filter_by(user_id=current_user.id)
        expense_query = Expense.query.filter_by(user_id=current_user.id)
        
        # Apply date filter if provided
        if month and year:
            income_query = income_query.filter(extract('month', Income.date) == month, extract('year', Income.date) == year)
            expense_query = expense_query.filter(extract('month', Expense.date) == month, extract('year', Expense.date) == year)
            
        incomes = income_query.order_by(Income.date.desc()).all()
        expenses = expense_query.order_by(Expense.date.desc()).all()
        
        return jsonify({
            'success': True,
            'incomes': [inc.to_dict() for inc in incomes],
            'expenses': [exp.to_dict() for exp in expenses]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching transactions: {str(e)}'
        }), 400


@app.route('/api/analysis', methods=['GET'])
@login_required
def get_analysis():
    """Get financial behavior analysis"""
    try:
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        
        # Base queries
        income_query = Income.query.filter_by(user_id=current_user.id)
        expense_query = Expense.query.filter_by(user_id=current_user.id)
        
        # Apply date filter if provided
        if month and year:
            income_query = income_query.filter(extract('month', Income.date) == month, extract('year', Income.date) == year)
            expense_query = expense_query.filter(extract('month', Expense.date) == month, extract('year', Expense.date) == year)
            
        # Get records
        incomes = income_query.all()
        expenses = expense_query.all()
        
        # Perform ML analysis
        analysis = analyzer.analyze_financial_behavior(incomes, expenses)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error performing analysis: {str(e)}'
        }), 400


@app.route('/api/income/<int:income_id>', methods=['DELETE'])
@login_required
def delete_income(income_id):
    """Delete income record"""
    try:
        income = Income.query.filter_by(id=income_id, user_id=current_user.id).first_or_404()
        db.session.delete(income)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Income deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting income: {str(e)}'
        }), 400


@app.route('/api/expense/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    """Delete expense record"""
    try:
        expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
        db.session.delete(expense)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Expense deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting expense: {str(e)}'
        }), 400


if __name__ == '__main__':
    app.run(debug=True, port=5001)
