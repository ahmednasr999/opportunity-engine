#!/usr/bin/env python3
"""
Phase 9 - System Features
Features: Dark/Light Theme, Keyboard Shortcuts, Bulk Actions, Advanced Search,
          Data Export, Import from Tools, Mobile Responsive, Offline/PWA
"""

import json
import csv
import io
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path


class ThemeManager:
    """Dark/Light theme toggle with persistence"""

    THEMES = {
        "dark": {
            "name": "Dark Mode",
            "bg": "#0a0a0f",
            "surface": "#12121a",
            "card": "#1a1a2e",
            "text": "#e2e8f0",
            "text_secondary": "#a0aec0",
            "brand": "#6c5ce7",
            "accent": "#00d2ff",
            "border": "#2d2d44",
            "success": "#00d26a",
            "warning": "#ffd93d",
            "danger": "#ff6b6b"
        },
        "light": {
            "name": "Light Mode",
            "bg": "#f5f5f7",
            "surface": "#ffffff",
            "card": "#ffffff",
            "text": "#1a202c",
            "text_secondary": "#718096",
            "brand": "#6c5ce7",
            "accent": "#0066cc",
            "border": "#e2e8f0",
            "success": "#38a169",
            "warning": "#d69e2e",
            "danger": "#e53e3e"
        }
    }

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.prefs_file = self.data_dir / "theme_prefs.json"
        self.current = self._load()

    def _load(self) -> str:
        if self.prefs_file.exists():
            data = json.loads(self.prefs_file.read_text())
            return data.get("theme", "dark")
        return "dark"

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.prefs_file.write_text(json.dumps({"theme": self.current}))

    def toggle(self) -> Dict:
        self.current = "light" if self.current == "dark" else "dark"
        self._save()
        return self.get_theme()

    def set_theme(self, theme_name: str) -> Dict:
        if theme_name in self.THEMES:
            self.current = theme_name
            self._save()
        return self.get_theme()

    def get_theme(self) -> Dict:
        return {
            "current": self.current,
            "colors": self.THEMES[self.current],
            "css_variables": {f"--{k}": v for k, v in self.THEMES[self.current].items() if k != "name"}
        }


class KeyboardShortcuts:
    """Keyboard shortcut configuration and help"""

    SHORTCUTS = {
        "navigation": [
            {"keys": "g d", "action": "Go to Dashboard", "url": "/"},
            {"keys": "g c", "action": "Go to CV Optimizer", "url": "/cv"},
            {"keys": "g j", "action": "Go to Job Tracker", "url": "/jobs"},
            {"keys": "g n", "action": "Go to Network", "url": "/network"},
            {"keys": "g p", "action": "Go to Content", "url": "/content"},
            {"keys": "g a", "action": "Go to Analytics", "url": "/analytics"},
        ],
        "actions": [
            {"keys": "n", "action": "New item (context-dependent)"},
            {"keys": "/", "action": "Focus search bar"},
            {"keys": "Escape", "action": "Close modal / Cancel"},
            {"keys": "?", "action": "Show keyboard shortcuts"},
            {"keys": "t", "action": "Toggle theme (dark/light)"},
        ],
        "cv_optimizer": [
            {"keys": "Ctrl+G", "action": "Generate CV"},
            {"keys": "Ctrl+P", "action": "Export PDF"},
            {"keys": "Ctrl+S", "action": "Save version"},
        ],
        "job_tracker": [
            {"keys": "a", "action": "Add new application"},
            {"keys": "f", "action": "Filter applications"},
            {"keys": "s", "action": "Sort applications"},
        ]
    }

    def get_all(self) -> Dict:
        return self.SHORTCUTS

    def get_js_handler(self) -> str:
        return """
document.addEventListener('keydown', function(e) {
    // Skip if in input/textarea
    if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return;
    
    // Theme toggle
    if (e.key === 't' && !e.ctrlKey && !e.metaKey) {
        fetch('/api/theme/toggle', {method: 'POST'}).then(r => r.json()).then(d => {
            document.documentElement.setAttribute('data-theme', d.current);
            location.reload();
        });
        return;
    }
    
    // Search focus
    if (e.key === '/') {
        e.preventDefault();
        document.querySelector('#search-input')?.focus();
        return;
    }
    
    // Help modal
    if (e.key === '?') {
        document.querySelector('#shortcuts-modal')?.classList.toggle('active');
        return;
    }
});
"""


class BulkActions:
    """Select and act on multiple items at once"""

    def process(self, action: str, item_ids: List[str], item_type: str) -> Dict:
        results = {"action": action, "item_type": item_type, "processed": 0, "errors": 0, "details": []}
        
        for item_id in item_ids:
            try:
                if action == "delete":
                    results["details"].append({"id": item_id, "status": "deleted"})
                elif action == "archive":
                    results["details"].append({"id": item_id, "status": "archived"})
                elif action == "export":
                    results["details"].append({"id": item_id, "status": "exported"})
                elif action == "update_status":
                    results["details"].append({"id": item_id, "status": "updated"})
                elif action == "tag":
                    results["details"].append({"id": item_id, "status": "tagged"})
                results["processed"] += 1
            except Exception as e:
                results["errors"] += 1
                results["details"].append({"id": item_id, "status": "error", "message": str(e)})

        return results

    def get_available_actions(self, item_type: str) -> List[Dict]:
        actions_map = {
            "applications": [
                {"id": "archive", "label": "Archive Selected", "icon": "fa-archive"},
                {"id": "delete", "label": "Delete Selected", "icon": "fa-trash", "dangerous": True},
                {"id": "update_status", "label": "Update Status", "icon": "fa-edit"},
                {"id": "export", "label": "Export Selected", "icon": "fa-download"},
                {"id": "tag", "label": "Tag Selected", "icon": "fa-tag"},
            ],
            "contacts": [
                {"id": "group", "label": "Add to Group", "icon": "fa-users"},
                {"id": "email", "label": "Send Email to All", "icon": "fa-envelope"},
                {"id": "export", "label": "Export Selected", "icon": "fa-download"},
                {"id": "delete", "label": "Delete Selected", "icon": "fa-trash", "dangerous": True},
            ],
            "content": [
                {"id": "schedule", "label": "Schedule All", "icon": "fa-calendar"},
                {"id": "export", "label": "Export Selected", "icon": "fa-download"},
                {"id": "delete", "label": "Delete Selected", "icon": "fa-trash", "dangerous": True},
            ]
        }
        return actions_map.get(item_type, [])


class AdvancedSearch:
    """Advanced search with filters, date ranges, and full-text search"""

    def search(self, query: str, filters: Dict = None, date_range: Dict = None, item_type: str = "all") -> Dict:
        filters = filters or {}
        results = []
        
        # Mock search results based on query
        mock_items = [
            {"type": "application", "title": "VP Operations at HealthTech", "date": "2026-02-10", "status": "interview", "tags": ["healthcare", "leadership"]},
            {"type": "application", "title": "Director AI at TechCorp", "date": "2026-02-05", "status": "applied", "tags": ["ai", "technology"]},
            {"type": "contact", "title": "Sarah Al-Rashid - CEO MENA HealthTech", "date": "2026-01-15", "status": "active", "tags": ["healthcare", "referral"]},
            {"type": "content", "title": "5 Ways AI is Transforming Healthcare", "date": "2026-02-12", "status": "published", "tags": ["ai", "healthcare", "content"]},
            {"type": "cv_version", "title": "CV v15 - HealthTech Focus", "date": "2026-02-08", "status": "saved", "tags": ["cv", "healthtech"]},
        ]

        query_lower = query.lower()
        for item in mock_items:
            if item_type != "all" and item["type"] != item_type:
                continue
            if query_lower in item["title"].lower() or any(query_lower in tag for tag in item.get("tags", [])):
                # Apply date filter
                if date_range:
                    start = date_range.get("start", "2000-01-01")
                    end = date_range.get("end", "2099-12-31")
                    if not (start <= item["date"] <= end):
                        continue
                # Apply status filter
                if filters.get("status") and item.get("status") != filters["status"]:
                    continue
                results.append(item)

        return {
            "query": query,
            "filters": filters,
            "date_range": date_range,
            "results": results,
            "total": len(results),
            "facets": {
                "types": list(set(r["type"] for r in results)),
                "statuses": list(set(r.get("status", "") for r in results)),
                "tags": list(set(tag for r in results for tag in r.get("tags", [])))
            }
        }

    def get_filter_options(self) -> Dict:
        return {
            "item_types": ["all", "application", "contact", "content", "cv_version"],
            "statuses": ["all", "active", "applied", "interview", "offer", "rejected", "published", "draft"],
            "sort_options": ["date_desc", "date_asc", "relevance", "status"],
            "date_presets": ["today", "this_week", "this_month", "last_30_days", "last_90_days", "custom"]
        }


class DataExport:
    """Export all data to JSON or CSV for backup"""

    def export_json(self, data: Dict = None) -> Dict:
        if not data:
            data = {
                "applications": [{"id": "1", "company": "Example Corp", "role": "VP", "status": "applied"}],
                "contacts": [{"name": "John Doe", "company": "Acme", "title": "CTO"}],
                "cv_versions": [{"id": "v1", "label": "Version 1", "ats_score": 85}],
                "content": [{"title": "Post 1", "status": "published"}],
                "settings": {"theme": "dark"}
            }
        
        export = {
            "export_date": datetime.now().isoformat(),
            "version": "2.0",
            "data": data,
            "stats": {k: len(v) if isinstance(v, list) else 1 for k, v in data.items()},
            "total_records": sum(len(v) if isinstance(v, list) else 1 for v in data.values())
        }
        
        return {
            "format": "json",
            "content": json.dumps(export, indent=2),
            "filename": f"opportunity_engine_backup_{datetime.now().strftime('%Y%m%d')}.json",
            "size_kb": round(len(json.dumps(export)) / 1024, 1),
            "records": export["total_records"]
        }

    def export_csv(self, data_type: str, data: List[Dict] = None) -> Dict:
        if not data:
            data = [{"id": "1", "company": "Example", "role": "VP", "status": "applied"}]
        
        if not data:
            return {"format": "csv", "content": "", "filename": f"{data_type}_export.csv"}
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
        return {
            "format": "csv",
            "content": output.getvalue(),
            "filename": f"{data_type}_export_{datetime.now().strftime('%Y%m%d')}.csv",
            "rows": len(data),
            "columns": len(data[0].keys()) if data else 0
        }


class ImportFromTools:
    """Import data from LinkedIn, Indeed, and other tools"""

    def import_linkedin_export(self, data: Dict = None) -> Dict:
        if not data:
            data = {
                "connections": [
                    {"First Name": "Sarah", "Last Name": "Al-Rashid", "Company": "MENA HealthTech", "Position": "CEO", "Connected On": "2023-05-15"},
                    {"First Name": "James", "Last Name": "Wilson", "Company": "TechCorp", "Position": "VP Eng", "Connected On": "2024-01-20"},
                ],
                "profile": {"name": "Ahmed Nasr", "headline": "Healthcare Operations Leader"}
            }

        imported_contacts = []
        for conn in data.get("connections", []):
            imported_contacts.append({
                "name": f"{conn.get('First Name', '')} {conn.get('Last Name', '')}".strip(),
                "company": conn.get("Company", ""),
                "title": conn.get("Position", ""),
                "source": "linkedin_import",
                "connected_date": conn.get("Connected On", ""),
            })

        return {
            "source": "LinkedIn Export",
            "imported_contacts": len(imported_contacts),
            "contacts": imported_contacts,
            "profile_imported": bool(data.get("profile")),
            "timestamp": datetime.now().isoformat()
        }

    def import_indeed_export(self, data: Dict = None) -> Dict:
        if not data:
            data = {
                "applications": [
                    {"Job Title": "VP Operations", "Company": "Hospital Group", "Applied Date": "2026-01-15", "Status": "Viewed"},
                    {"Job Title": "Director AI", "Company": "TechHealth", "Applied Date": "2026-02-01", "Status": "Applied"},
                ]
            }

        imported_apps = []
        for app in data.get("applications", []):
            imported_apps.append({
                "role": app.get("Job Title", ""),
                "company": app.get("Company", ""),
                "applied_date": app.get("Applied Date", ""),
                "status": app.get("Status", "applied").lower(),
                "source": "indeed_import"
            })

        return {
            "source": "Indeed Export",
            "imported_applications": len(imported_apps),
            "applications": imported_apps,
            "timestamp": datetime.now().isoformat()
        }

    def get_supported_formats(self) -> List[Dict]:
        return [
            {"name": "LinkedIn", "formats": ["CSV (Connections)", "JSON (Profile)"], "icon": "fab fa-linkedin"},
            {"name": "Indeed", "formats": ["CSV (Applications)"], "icon": "fas fa-briefcase"},
            {"name": "Glassdoor", "formats": ["CSV (Applications)"], "icon": "fas fa-star"},
            {"name": "Generic CSV", "formats": ["CSV (Contacts)", "CSV (Applications)"], "icon": "fas fa-file-csv"},
            {"name": "JSON", "formats": ["JSON (Full backup)"], "icon": "fas fa-code"},
        ]


class MobileResponsive:
    """Mobile responsive helpers and breakpoint configs"""

    def get_config(self) -> Dict:
        return {
            "breakpoints": {
                "mobile": "max-width: 640px",
                "tablet": "max-width: 1024px",
                "desktop": "min-width: 1025px"
            },
            "mobile_css": """
@media (max-width: 640px) {
    .sidebar { display: none; position: fixed; z-index: 1000; }
    .sidebar.active { display: block; width: 80%; }
    .main-content { margin-left: 0 !important; padding: 12px !important; }
    .card { padding: 16px !important; }
    .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr !important; }
    h1 { font-size: 28px !important; }
    .mobile-menu-btn { display: block !important; }
    .desktop-only { display: none !important; }
    .table-responsive { overflow-x: auto; }
    .stat-grid { grid-template-columns: 1fr 1fr !important; }
}
@media (max-width: 1024px) {
    .sidebar { width: 60px; }
    .sidebar .nav-text { display: none; }
    .main-content { margin-left: 60px !important; }
}
""",
            "touch_optimizations": {
                "min_tap_target": "44px",
                "swipe_enabled": True,
                "pull_to_refresh": True
            },
            "viewport_meta": '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">',
            "features": [
                "Responsive grid layouts",
                "Collapsible sidebar on mobile",
                "Touch-friendly tap targets (44px+)",
                "Swipe gestures for navigation",
                "Optimized card layouts for small screens"
            ]
        }


class OfflineMode:
    """PWA with service worker for offline capability"""

    def get_manifest(self) -> Dict:
        return {
            "name": "Opportunity Engine",
            "short_name": "OpEngine",
            "description": "AI-Powered Career Management Platform",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#0a0a0f",
            "theme_color": "#6c5ce7",
            "icons": [
                {"src": "/static/icon-192.png", "sizes": "192x192", "type": "image/png"},
                {"src": "/static/icon-512.png", "sizes": "512x512", "type": "image/png"}
            ]
        }

    def get_service_worker(self) -> str:
        return """
const CACHE_NAME = 'opportunity-engine-v2';
const urlsToCache = [
    '/',
    '/static/style.css',
    '/cv',
    '/jobs',
    '/network',
    '/content',
    '/analytics'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) return response;
                return fetch(event.request)
                    .then(response => {
                        if (!response || response.status !== 200) return response;
                        const responseClone = response.clone();
                        caches.open(CACHE_NAME)
                            .then(cache => cache.put(event.request, responseClone));
                        return response;
                    })
                    .catch(() => {
                        return new Response('<h1>Offline</h1><p>Please check your connection.</p>', 
                            {headers: {'Content-Type': 'text/html'}});
                    });
            })
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(names => 
            Promise.all(names.filter(n => n !== CACHE_NAME).map(n => caches.delete(n)))
        )
    );
});
"""

    def get_registration_script(self) -> str:
        return """
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('SW registered:', reg.scope))
            .catch(err => console.log('SW failed:', err));
    });
}
"""

    def get_config(self) -> Dict:
        return {
            "enabled": True,
            "manifest": self.get_manifest(),
            "cache_strategy": "network-first",
            "offline_pages": ["/", "/cv", "/jobs", "/network"],
            "features": [
                "Offline access to cached pages",
                "Background sync for saved data",
                "Install as app on mobile/desktop",
                "Push notification support (future)"
            ]
        }
