import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
from config import Config

class ExpenseAnalyzer:
    """ML-based expense behavior analyzer"""
    
    def __init__(self):
        self.config = Config()
    
    def analyze_financial_behavior(self, incomes, expenses):
        """
        Analyze financial behavior and classify user
        
        Args:
            incomes: List of income records
            expenses: List of expense records
            
        Returns:
            dict: Analysis results with classification, metrics, and insights
        """
        # Calculate basic metrics
        total_income = sum(inc.amount for inc in incomes)
        total_expenses = sum(exp.amount for exp in expenses)
        total_savings = total_income - total_expenses
        
        # Avoid division by zero
        if total_income == 0:
            return self._generate_no_data_response()
        
        savings_rate = (total_savings / total_income) * 100
        expense_ratio = (total_expenses / total_income) * 100
        
        # Category-wise analysis
        category_breakdown = self._analyze_categories(expenses, total_income)
        
        # Essential vs Non-Essential
        essential_spending = self._calculate_essential_spending(expenses)
        non_essential_spending = total_expenses - essential_spending
        
        essential_ratio = (essential_spending / total_income * 100) if total_income > 0 else 0
        non_essential_ratio = (non_essential_spending / total_income * 100) if total_income > 0 else 0
        
        # Classify behavior
        classification = self._classify_behavior(
            savings_rate, 
            expense_ratio, 
            essential_ratio, 
            non_essential_ratio
        )
        
        # Generate insights and recommendations
        insights = self._generate_insights(
            classification,
            savings_rate,
            category_breakdown,
            essential_ratio,
            non_essential_ratio,
            total_income
        )
        
        # Trend analysis
        trend = self._analyze_trend(expenses)
        
        return {
            'classification': classification,
            'metrics': {
                'total_income': total_income,
                'total_expenses': total_expenses,
                'total_savings': total_savings,
                'savings_rate': round(savings_rate, 2),
                'expense_ratio': round(expense_ratio, 2),
                'essential_spending': essential_spending,
                'non_essential_spending': non_essential_spending,
                'essential_ratio': round(essential_ratio, 2),
                'non_essential_ratio': round(non_essential_ratio, 2)
            },
            'category_breakdown': category_breakdown,
            'insights': insights,
            'trend': trend
        }
    
    def _classify_behavior(self, savings_rate, expense_ratio, essential_ratio, non_essential_ratio):
        """
        Classify financial behavior based on multiple features
        
        Returns:
            dict: Classification with label, description, and color
        """
        # Good Saver criteria
        if savings_rate >= self.config.GOOD_SAVER_THRESHOLD and non_essential_ratio < 20:
            return {
                'label': 'Good Saver',
                'description': 'Excellent financial discipline! You maintain healthy savings and control discretionary spending.',
                'color': '#10b981',  # Green
                'emoji': '🌟'
            }
        
        # Average Saver criteria
        elif savings_rate >= self.config.AVERAGE_SAVER_MIN and savings_rate < self.config.GOOD_SAVER_THRESHOLD:
            return {
                'label': 'Average Saver',
                'description': 'Good progress! You save regularly but have room for improvement.',
                'color': '#f59e0b',  # Orange
                'emoji': '👍'
            }
        
        # Overspender criteria
        else:
            return {
                'label': 'Overspender',
                'description': 'Attention needed! Your expenses are high relative to income. Focus on reducing non-essential spending.',
                'color': '#ef4444',  # Red
                'emoji': '⚠️'
            }
    
    def _analyze_categories(self, expenses, total_income):
        """Analyze spending by category"""
        category_totals = defaultdict(float)
        
        for expense in expenses:
            category_totals[expense.category] += expense.amount
        
        # Calculate percentages and identify high-risk categories
        breakdown = []
        alerts = []
        
        for category, amount in category_totals.items():
            percentage = (amount / total_income * 100) if total_income > 0 else 0
            
            item = {
                'category': category,
                'amount': amount,
                'percentage': round(percentage, 2)
            }
            
            # Check if category exceeds threshold
            if category in self.config.CATEGORY_THRESHOLDS:
                threshold = self.config.CATEGORY_THRESHOLDS[category]
                if percentage > threshold:
                    item['alert'] = True
                    alerts.append({
                        'category': category,
                        'percentage': round(percentage, 2),
                        'threshold': threshold
                    })
            
            breakdown.append(item)
        
        # Sort by amount descending
        breakdown.sort(key=lambda x: x['amount'], reverse=True)
        
        return {
            'categories': breakdown,
            'alerts': alerts
        }
    
    def _calculate_essential_spending(self, expenses):
        """Calculate total essential spending"""
        essential_total = 0
        
        for expense in expenses:
            if expense.category in self.config.ESSENTIAL_CATEGORIES:
                essential_total += expense.amount
        
        return essential_total
    
    def _generate_insights(self, classification, savings_rate, category_breakdown, 
                          essential_ratio, non_essential_ratio, total_income):
        """Generate actionable insights and recommendations"""
        insights = []
        recommendations = []
        
        # Savings rate insights
        if savings_rate < 10:
            insights.append("Your savings rate is critically low. Immediate action needed!")
            recommendations.append("Try to save at least 10-20% of your income each month.")
        elif savings_rate < 20:
            insights.append("Your savings rate is below the recommended 20% benchmark.")
            recommendations.append("Aim to increase your savings rate to at least 20%.")
        elif savings_rate >= 30:
            insights.append("Excellent savings rate! You're building wealth effectively.")
            recommendations.append("Consider investing your savings for long-term growth.")
        
        # Essential vs Non-Essential insights
        if non_essential_ratio > 30:
            insights.append(f"Non-essential spending is {non_essential_ratio:.1f}% of income - too high!")
            recommendations.append("Reduce discretionary spending on dining, entertainment, and shopping.")
        elif non_essential_ratio > 20:
            insights.append("Non-essential spending could be optimized.")
            recommendations.append("Review your discretionary expenses and identify areas to cut back.")
        
        # Category-specific alerts
        if category_breakdown['alerts']:
            for alert in category_breakdown['alerts']:
                insights.append(
                    f"{alert['category']} spending ({alert['percentage']:.1f}%) exceeds recommended threshold ({alert['threshold']}%)."
                )
                recommendations.append(f"Reduce {alert['category']} expenses to below {alert['threshold']}% of income.")
        
        # Top spending categories
        if category_breakdown['categories']:
            top_category = category_breakdown['categories'][0]
            insights.append(f"Your highest expense category is {top_category['category']} (₹{top_category['amount']:,.2f}).")
        
        # General recommendations based on classification
        if classification['label'] == 'Good Saver':
            recommendations.append("Maintain your excellent habits and explore investment opportunities.")
            recommendations.append("Consider setting up an emergency fund (6 months of expenses).")
        elif classification['label'] == 'Average Saver':
            recommendations.append("Track your expenses daily to identify saving opportunities.")
            recommendations.append("Set specific savings goals and automate your savings.")
        else:  # Overspender
            recommendations.append("Create a strict budget and stick to it.")
            recommendations.append("Eliminate or reduce non-essential expenses immediately.")
            recommendations.append("Consider the 50/30/20 rule: 50% needs, 30% wants, 20% savings.")
        
        return {
            'insights': insights,
            'recommendations': recommendations
        }
    
    def _analyze_trend(self, expenses):
        """Analyze spending trend over time"""
        if len(expenses) < 2:
            return {'trend': 'insufficient_data', 'message': 'Need more data to analyze trends'}
        
        # Group expenses by month
        monthly_expenses = defaultdict(float)
        
        for expense in expenses:
            month_key = expense.date.strftime('%Y-%m')
            monthly_expenses[month_key] += expense.amount
        
        if len(monthly_expenses) < 2:
            return {'trend': 'stable', 'message': 'Single month data available'}
        
        # Calculate trend
        sorted_months = sorted(monthly_expenses.items())
        recent_months = sorted_months[-3:] if len(sorted_months) >= 3 else sorted_months
        
        amounts = [amount for _, amount in recent_months]
        
        # Simple trend detection
        if len(amounts) >= 2:
            avg_change = (amounts[-1] - amounts[0]) / len(amounts)
            
            if avg_change > 0:
                trend = 'increasing'
                message = '⚠️ Your expenses are trending upward'
            elif avg_change < 0:
                trend = 'decreasing'
                message = '✅ Your expenses are trending downward'
            else:
                trend = 'stable'
                message = 'Your expenses are relatively stable'
        else:
            trend = 'stable'
            message = 'Insufficient data for trend analysis'
        
        return {
            'trend': trend,
            'message': message,
            'monthly_data': [{'month': month, 'amount': amount} for month, amount in sorted_months]
        }
    
    def _generate_no_data_response(self):
        """Generate response when no data is available"""
        return {
            'classification': {
                'label': 'No Data',
                'description': 'Start by adding your income and expense records.',
                'color': '#6b7280',
                'emoji': '📊'
            },
            'metrics': {
                'total_income': 0,
                'total_expenses': 0,
                'total_savings': 0,
                'savings_rate': 0,
                'expense_ratio': 0,
                'essential_spending': 0,
                'non_essential_spending': 0,
                'essential_ratio': 0,
                'non_essential_ratio': 0
            },
            'category_breakdown': {'categories': [], 'alerts': []},
            'insights': {
                'insights': ['No financial data available yet.'],
                'recommendations': [
                    'Start by recording your income sources.',
                    'Track all your expenses by category.',
                    'Review your analysis regularly to improve financial health.'
                ]
            },
            'trend': {'trend': 'no_data', 'message': 'No data available'}
        }
