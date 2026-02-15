#!/usr/bin/env python3
"""
Notification Hub - Smart alerts with batching, priority, and DND
Central notification management for all tools
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
import time

@dataclass
class Notification:
    """A notification"""
    id: str
    title: str
    message: str
    priority: str  # critical, high, normal, low
    category: str  # job, network, content, system
    source: str    # Which tool generated it
    timestamp: str
    read: bool
    action_required: bool
    action_url: str
    dismiss_after: int  # Auto-dismiss after minutes (0 = never)


class NotificationHub:
    """Central notification management"""
    
    def __init__(self, data_dir: str = "/root/.openclaw/workspace/tools/cv-optimizer/data"):
        self.data_dir = Path(data_dir)
        self.notifications_file = self.data_dir / "notifications.json"
        self.settings_file = self.data_dir / "notification_settings.json"
        self.notifications: List[Dict] = []
        self.settings = self._load_settings()
        self.load()
    
    def _load_settings(self) -> Dict:
        """Load notification settings"""
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        
        # Default settings
        return {
            "dnd_enabled": False,
            "dnd_start": "22:00",
            "dnd_end": "08:00",
            "batch_notifications": True,
            "batch_interval_minutes": 60,
            "min_priority": "normal",  # Filter below this
            "channels": {
                "dashboard": True,
                "email": False,
                "telegram": False
            },
            "category_settings": {
                "job": {"enabled": True, "min_priority": "normal"},
                "network": {"enabled": True, "min_priority": "normal"},
                "content": {"enabled": True, "min_priority": "low"},
                "system": {"enabled": True, "min_priority": "high"}
            }
        }
    
    def save_settings(self):
        """Save notification settings"""
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def load(self):
        """Load notifications"""
        if self.notifications_file.exists():
            with open(self.notifications_file, 'r') as f:
                self.notifications = json.load(f)
    
    def save(self):
        """Save notifications"""
        with open(self.notifications_file, 'w') as f:
            json.dump(self.notifications[-500:], f, indent=2)  # Keep last 500
    
    def is_dnd_active(self) -> bool:
        """Check if Do Not Disturb is active"""
        if not self.settings.get("dnd_enabled", False):
            return False
        
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        dnd_start = self.settings.get("dnd_start", "22:00")
        dnd_end = self.settings.get("dnd_end", "08:00")
        
        # Handle overnight DND (e.g., 22:00 - 08:00)
        if dnd_start > dnd_end:
            return current_time >= dnd_start or current_time < dnd_end
        else:
            return dnd_start <= current_time < dnd_end
    
    def should_notify(self, priority: str, category: str) -> bool:
        """Check if notification should be sent based on settings"""
        # Always notify critical
        if priority == "critical":
            return True
        
        # Check DND
        if self.is_dnd_active() and priority != "critical":
            return False
        
        # Check category settings
        cat_settings = self.settings.get("category_settings", {}).get(category, {})
        if not cat_settings.get("enabled", True):
            return False
        
        min_priority = cat_settings.get("min_priority", "normal")
        priority_levels = {"low": 1, "normal": 2, "high": 3, "critical": 4}
        
        return priority_levels.get(priority, 2) >= priority_levels.get(min_priority, 2)
    
    def send(self, 
             title: str,
             message: str,
             priority: str = "normal",
             category: str = "system",
             source: str = "system",
             action_required: bool = False,
             action_url: str = "",
             dismiss_after: int = 0) -> Optional[Dict]:
        """Send a notification"""
        
        # Check if should notify
        if not self.should_notify(priority, category):
            return None
        
        notification = {
            "id": f"notif_{int(time.time())}_{len(self.notifications)}",
            "title": title,
            "message": message,
            "priority": priority,
            "category": category,
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "read": False,
            "action_required": action_required,
            "action_url": action_url,
            "dismiss_after": dismiss_after
        }
        
        self.notifications.append(notification)
        self.save()
        
        # In a real system, this would also:
        # - Send to Telegram/WhatsApp if configured
        # - Send email if configured
        # - Show browser notification if dashboard open
        
        return notification
    
    def mark_read(self, notification_id: str):
        """Mark notification as read"""
        for notif in self.notifications:
            if notif.get('id') == notification_id:
                notif['read'] = True
                self.save()
                return True
        return False
    
    def mark_all_read(self):
        """Mark all notifications as read"""
        for notif in self.notifications:
            notif['read'] = True
        self.save()
    
    def get_unread(self, limit: int = 50) -> List[Dict]:
        """Get unread notifications"""
        unread = [n for n in self.notifications if not n.get('read', False)]
        return sorted(unread, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_all(self, limit: int = 100) -> List[Dict]:
        """Get all notifications"""
        return sorted(self.notifications, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_by_category(self, category: str) -> List[Dict]:
        """Get notifications by category"""
        return [n for n in self.notifications if n.get('category') == category]
    
    def get_by_priority(self, priority: str) -> List[Dict]:
        """Get notifications by priority"""
        return [n for n in self.notifications if n.get('priority') == priority]
    
    def get_action_required(self) -> List[Dict]:
        """Get notifications requiring action"""
        return [n for n in self.notifications if n.get('action_required') and not n.get('read')]
    
    def clear_old(self, days: int = 30):
        """Clear notifications older than X days"""
        cutoff = datetime.now() - timedelta(days=days)
        self.notifications = [
            n for n in self.notifications 
            if datetime.fromisoformat(n['timestamp']) > cutoff
        ]
        self.save()
    
    # Smart notifications for specific events
    
    def notify_job_added(self, company: str, title: str, ats_score: int):
        """Notify when job is added"""
        priority = "high" if ats_score >= 85 else "normal"
        
        self.send(
            title=f"✅ Job Application Added",
            message=f"{title} at {company} added to tracker. ATS Score: {ats_score}/100",
            priority=priority,
            category="job",
            source="job_tracker"
        )
    
    def notify_interview_scheduled(self, company: str, date: str, time: str):
        """Notify when interview is scheduled"""
        self.send(
            title=f"🤝 Interview Scheduled",
            message=f"Interview with {company} on {date} at {time}. Check calendar for prep reminders.",
            priority="critical",
            category="job",
            source="calendar",
            action_required=True
        )
    
    def notify_offer_received(self, company: str, salary: str = ""):
        """Notify when offer is received"""
        msg = f"🎉 Offer received from {company}!"
        if salary:
            msg += f" Salary: {salary}"
        
        self.send(
            title="🎉 JOB OFFER RECEIVED!",
            message=msg,
            priority="critical",
            category="job",
            source="job_tracker",
            action_required=True
        )
    
    def notify_follow_up_due(self, company: str, days_overdue: int):
        """Notify when follow-up is due"""
        emoji = "🔴" if days_overdue > 0 else "🟡"
        status = f"{days_overdue} days overdue" if days_overdue > 0 else "Due today"
        
        self.send(
            title=f"{emoji} Follow-up Due: {company}",
            message=f"Follow-up with {company} is {status}. Send status check email.",
            priority="high" if days_overdue > 0 else "normal",
            category="job",
            source="job_tracker",
            action_required=True
        )
    
    def notify_network_warm_intro(self, company: str, contact_name: str):
        """Notify about potential warm intro"""
        self.send(
            title=f"🌡️ Warm Intro Available: {company}",
            message=f"{contact_name} can introduce you to {company}. Reach out!",
            priority="high",
            category="network",
            source="network_mapper",
            action_required=True
        )
    
    def notify_content_generated(self, content_type: str, word_count: int):
        """Notify when content is generated"""
        self.send(
            title=f"✍️ Content Ready: {content_type}",
            message=f"{content_type} content generated ({word_count} words). Ready to review and post.",
            priority="low",
            category="content",
            source="content_factory"
        )
    
    def notify_ats_low(self, company: str, score: int, suggestions: List[str]):
        """Notify when ATS score is low"""
        sugg_text = "\n".join([f"• {s}" for s in suggestions[:3]])
        
        self.send(
            title=f"🟡 Low ATS Score: {company}",
            message=f"ATS Score: {score}/100. Suggestions:\n{sugg_text}",
            priority="high",
            category="job",
            source="cv_optimizer",
            action_required=True
        )
    
    def notify_weekly_summary(self, stats: Dict):
        """Weekly summary notification"""
        self.send(
            title="📊 Weekly Summary",
            message=f"Apps: {stats.get('applications', 0)} | Interviews: {stats.get('interviews', 0)} | Offers: {stats.get('offers', 0)}",
            priority="normal",
            category="system",
            source="analytics"
        )
    
    def get_stats(self) -> Dict:
        """Get notification stats"""
        total = len(self.notifications)
        unread = len([n for n in self.notifications if not n.get('read')])
        action_required = len(self.get_action_required())
        
        by_priority = {}
        for priority in ["critical", "high", "normal", "low"]:
            by_priority[priority] = len(self.get_by_priority(priority))
        
        by_category = {}
        for category in ["job", "network", "content", "system"]:
            by_category[category] = len(self.get_by_category(category))
        
        return {
            "total": total,
            "unread": unread,
            "action_required": action_required,
            "by_priority": by_priority,
            "by_category": by_category,
            "dnd_active": self.is_dnd_active()
        }
    
    def print_notifications(self, limit: int = 20):
        """Print recent notifications"""
        notifications = self.get_unread(limit)
        
        print("\n" + "=" * 60)
        print("🔔 NOTIFICATIONS")
        print("=" * 60)
        
        if not notifications:
            print("\nNo unread notifications. 🎉")
            return
        
        for notif in notifications:
            priority_emoji = {
                "critical": "🔴",
                "high": "🟠",
                "normal": "🔵",
                "low": "⚪"
            }.get(notif.get('priority'), "⚪")
            
            category_emoji = {
                "job": "💼",
                "network": "🌐",
                "content": "✍️",
                "system": "⚙️"
            }.get(notif.get('category'), "📌")
            
            print(f"\n{priority_emoji} {category_emoji} {notif['title']}")
            print(f"   {notif['message'][:100]}...")
            print(f"   Source: {notif.get('source', 'system')} | {notif['timestamp'][:16]}")
            
            if notif.get('action_required'):
                print(f"   ⚠️  Action Required")


def main():
    """CLI interface"""
    import sys
    
    hub = NotificationHub()
    
    if len(sys.argv) < 2:
        hub.print_notifications()
        return
    
    command = sys.argv[1]
    
    if command == "test":
        # Send test notifications
        hub.notify_job_added("Test Corp", "VP Test", 85)
        hub.notify_follow_up_due("Example Inc", 2)
        hub.notify_content_generated("LinkedIn", 150)
        print("✅ Test notifications sent")
    
    elif command == "stats":
        stats = hub.get_stats()
        print(f"\n📊 Notification Stats")
        print(f"Total: {stats['total']} | Unread: {stats['unread']} | Action Required: {stats['action_required']}")
        print(f"DND Active: {stats['dnd_active']}")
        print(f"\nBy Priority:")
        for p, c in stats['by_priority'].items():
            print(f"  {p}: {c}")
    
    elif command == "clear":
        hub.mark_all_read()
        print("✅ All notifications marked as read")
    
    elif command == "dnd":
        if len(sys.argv) > 2:
            action = sys.argv[2]
            if action == "on":
                hub.settings["dnd_enabled"] = True
                print("✅ Do Not Disturb enabled")
            elif action == "off":
                hub.settings["dnd_enabled"] = False
                print("✅ Do Not Disturb disabled")
            hub.save_settings()
        else:
            print(f"DND Status: {'On' if hub.is_dnd_active() else 'Off'}")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
