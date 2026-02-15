"""
Expense Tracker - Personal finance tracking during job search
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
EXPENSE_FILE = os.path.join(DATA_DIR, 'expenses.json')

class ExpenseTracker:
    def __init__(self):
        self.expenses = self._load_expenses()
    
    def _load_expenses(self) -> List[Dict]:
        """Load expenses from JSON file"""
        if os.path.exists(EXPENSE_FILE):
            with open(EXPENSE_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def _save_expenses(self):
        """Save expenses to JSON file"""
        with open(EXPENSE_FILE, 'w') as f:
            json.dump(self.expenses, f, indent=2)
    
    def add_expense(self, amount: float, category: str, description: str, 
                    date: str = None, is_job_related: bool = False) -> Dict:
        """Add a new expense"""
        expense = {
            'id': f"exp-{len(self.expenses) + 1}",
            'amount': float(amount),
            'category': category,
            'description': description,
            'date': date or datetime.now().strftime('%Y-%m-%d'),
            'is_job_related': is_job_related,
            'created_at': datetime.now().isoformat()
        }
        self.expenses.append(expense)
        self._save_expenses()
        return expense
    
    def get_expenses(self, category: str = None, job_related_only: bool = False,
                     start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get filtered expenses"""
        result = self.expenses
        
        if category:
            result = [e for e in result if e['category'] == category]
        
        if job_related_only:
            result = [e for e in result if e['is_job_related']]
        
        if start_date:
            result = [e for e in result if e['date'] >= start_date]
        
        if end_date:
            result = [e for e in result if e['date'] <= end_date]
        
        return sorted(result, key=lambda x: x['date'], reverse=True)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get expense summary"""
        total = sum(e['amount'] for e in self.expenses)
        job_related = sum(e['amount'] for e in self.expenses if e['is_job_related'])
        personal = total - job_related
        
        by_category = {}
        for e in self.expenses:
            cat = e['category']
            by_category[cat] = by_category.get(cat, 0) + e['amount']
        
        this_month = datetime.now().strftime('%Y-%m')
        monthly = sum(e['amount'] for e in self.expenses if e['date'].startswith(this_month))
        
        return {
            'total_spent': round(total, 2),
            'job_related': round(job_related, 2),
            'personal': round(personal, 2),
            'by_category': {k: round(v, 2) for k, v in by_category.items()},
            'this_month': round(monthly, 2),
            'expense_count': len(self.expenses)
        }
    
    def delete_expense(self, expense_id: str) -> bool:
        """Delete an expense by ID"""
        original_count = len(self.expenses)
        self.expenses = [e for e in self.expenses if e['id'] != expense_id]
        if len(self.expenses) < original_count:
            self._save_expenses()
            return True
        return False
