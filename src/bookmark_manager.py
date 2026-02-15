"""
Bookmark Manager - Save and organize jobs, articles, contacts
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
BOOKMARK_FILE = os.path.join(DATA_DIR, 'bookmarks.json')

class BookmarkManager:
    CATEGORIES = ['job', 'article', 'contact', 'company', 'resource', 'other']
    
    def __init__(self):
        self.bookmarks = self._load_bookmarks()
    
    def _load_bookmarks(self) -> List[Dict]:
        """Load bookmarks from JSON file"""
        if os.path.exists(BOOKMARK_FILE):
            with open(BOOKMARK_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def _save_bookmarks(self):
        """Save bookmarks to JSON file"""
        with open(BOOKMARK_FILE, 'w') as f:
            json.dump(self.bookmarks, f, indent=2)
    
    def add_bookmark(self, title: str, url: str, category: str = 'other',
                     notes: str = '', tags: List[str] = None) -> Dict:
        """Add a new bookmark"""
        if category not in self.CATEGORIES:
            category = 'other'
        
        bookmark = {
            'id': f"bm-{len(self.bookmarks) + 1}",
            'title': title,
            'url': url,
            'category': category,
            'notes': notes,
            'tags': tags or [],
            'date_added': datetime.now().strftime('%Y-%m-%d'),
            'created_at': datetime.now().isoformat()
        }
        self.bookmarks.append(bookmark)
        self._save_bookmarks()
        return bookmark
    
    def get_bookmarks(self, category: str = None, tag: str = None,
                      search_query: str = None) -> List[Dict]:
        """Get filtered bookmarks"""
        result = sorted(self.bookmarks, 
                       key=lambda x: x['created_at'], 
                       reverse=True)
        
        if category:
            result = [b for b in result if b['category'] == category]
        
        if tag:
            result = [b for b in result if tag in b.get('tags', [])]
        
        if search_query:
            query = search_query.lower()
            result = [b for b in result 
                     if query in b['title'].lower() 
                     or query in b.get('notes', '').lower()
                     or any(query in t.lower() for t in b.get('tags', []))]
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """Get bookmark statistics"""
        by_category = {cat: 0 for cat in self.CATEGORIES}
        for b in self.bookmarks:
            by_category[b['category']] = by_category.get(b['category'], 0) + 1
        
        all_tags = []
        for b in self.bookmarks:
            all_tags.extend(b.get('tags', []))
        
        unique_tags = list(set(all_tags))
        
        # Recent (last 7 days)
        recent_count = len([b for b in self.bookmarks 
                          if (datetime.now() - datetime.fromisoformat(b['created_at'])).days <= 7])
        
        return {
            'total': len(self.bookmarks),
            'by_category': by_category,
            'unique_tags': len(unique_tags),
            'recent': recent_count
        }
    
    def delete_bookmark(self, bookmark_id: str) -> bool:
        """Delete a bookmark by ID"""
        original_count = len(self.bookmarks)
        self.bookmarks = [b for b in self.bookmarks if b['id'] != bookmark_id]
        if len(self.bookmarks) < original_count:
            self._save_bookmarks()
            return True
        return False
    
    def update_bookmark(self, bookmark_id: str, **updates) -> Optional[Dict]:
        """Update a bookmark"""
        for b in self.bookmarks:
            if b['id'] == bookmark_id:
                for key, value in updates.items():
                    if key in ['title', 'url', 'category', 'notes', 'tags']:
                        b[key] = value
                self._save_bookmarks()
                return b
        return None

# Singleton instance for easy import
bookmark_manager = BookmarkManager()
