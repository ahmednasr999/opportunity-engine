"""
Search Aggregator - Unified search across all tools and data
"""
import json
import os
from typing import Dict, List, Any
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

class SearchAggregator:
    """Search across all Opportunity Engine data sources"""
    
    def __init__(self):
        self.data_dir = DATA_DIR
    
    def search_all(self, query: str, limit: int = 20) -> Dict[str, List[Dict]]:
        """Search across all data sources"""
        query_lower = query.lower()
        results = {
            'jobs': [],
            'contacts': [],
            'bookmarks': [],
            'expenses': [],
            'cvs': [],
            'content': []
        }
        
        # Search jobs
        jobs_file = os.path.join(self.data_dir, 'jobs.json')
        if os.path.exists(jobs_file):
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
                for job in jobs:
                    if (query_lower in job.get('company', '').lower() or
                        query_lower in job.get('title', '').lower() or
                        query_lower in job.get('status', '').lower()):
                        results['jobs'].append({
                            'type': 'job',
                            'title': f"{job['title']} at {job['company']}",
                            'status': job.get('status', 'unknown'),
                            'url': f"/job-tracker",
                            'data': job
                        })
        
        # Search contacts
        contacts_file = os.path.join(self.data_dir, 'contacts.json')
        if os.path.exists(contacts_file):
            with open(contacts_file, 'r') as f:
                contacts = json.load(f)
                for contact in contacts:
                    if (query_lower in contact.get('name', '').lower() or
                        query_lower in contact.get('company', '').lower() or
                        query_lower in contact.get('title', '').lower()):
                        results['contacts'].append({
                            'type': 'contact',
                            'title': contact['name'],
                            'subtitle': f"{contact.get('title', '')} at {contact.get('company', '')}",
                            'url': '/network',
                            'data': contact
                        })
        
        # Search bookmarks
        bookmarks_file = os.path.join(self.data_dir, 'bookmarks.json')
        if os.path.exists(bookmarks_file):
            with open(bookmarks_file, 'r') as f:
                bookmarks = json.load(f)
                for bm in bookmarks:
                    if (query_lower in bm.get('title', '').lower() or
                        query_lower in ' '.join(bm.get('tags', [])).lower() or
                        query_lower in bm.get('notes', '').lower()):
                        results['bookmarks'].append({
                            'type': 'bookmark',
                            'title': bm['title'],
                            'category': bm.get('category', 'other'),
                            'url': bm.get('url', '#'),
                            'data': bm
                        })
        
        # Search expenses
        expenses_file = os.path.join(self.data_dir, 'expenses.json')
        if os.path.exists(expenses_file):
            with open(expenses_file, 'r') as f:
                expenses = json.load(f)
                for exp in expenses:
                    if (query_lower in exp.get('description', '').lower() or
                        query_lower in exp.get('category', '').lower()):
                        results['expenses'].append({
                            'type': 'expense',
                            'title': exp['description'],
                            'amount': exp.get('amount', 0),
                            'date': exp.get('date', ''),
                            'url': '/expenses',
                            'data': exp
                        })
        
        # Search generated CVs
        cvs_file = os.path.join(self.data_dir, 'generated_cvs.json')
        if os.path.exists(cvs_file):
            with open(cvs_file, 'r') as f:
                cvs = json.load(f)
                for cv in cvs:
                    if (query_lower in cv.get('company', '').lower() or
                        query_lower in cv.get('title', '').lower()):
                        results['cvs'].append({
                            'type': 'cv',
                            'title': f"CV for {cv.get('title', 'Unknown')}",
                            'company': cv.get('company', ''),
                            'ats_score': cv.get('ats_score', 0),
                            'url': '/cv-optimizer',
                            'data': cv
                        })
        
        # Limit results per category
        for key in results:
            results[key] = results[key][:limit]
        
        return results
    
    def get_stats(self) -> Dict[str, int]:
        """Get total counts across all data sources"""
        stats = {}
        
        files = {
            'jobs': 'jobs.json',
            'contacts': 'contacts.json',
            'bookmarks': 'bookmarks.json',
            'expenses': 'expenses.json',
            'cvs': 'generated_cvs.json',
            'calendar': 'calendar_events.json',
            'notifications': 'notifications.json'
        }
        
        for key, filename in files.items():
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    stats[key] = len(data)
            else:
                stats[key] = 0
        
        return stats
