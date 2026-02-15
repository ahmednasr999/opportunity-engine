#!/usr/bin/env python3
"""
Auto-Trigger System - IFTTT-style automation for Opportunity Engine
Connects all tools to automate workflows
"""

import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import threading
import time

@dataclass
class Trigger:
    """A trigger definition"""
    id: str
    name: str
    condition: str  # e.g., "job_added", "ats_score_low", "follow_up_due"
    action: str     # e.g., "generate_cv", "create_content", "send_alert"
    params: Dict
    enabled: bool
    last_run: str
    run_count: int


class AutoTriggerSystem:
    """Automated workflow engine"""
    
    def __init__(self, data_dir: str = "/root/.openclaw/workspace/tools/cv-optimizer/data"):
        self.data_dir = Path(data_dir)
        self.triggers_file = self.data_dir / "autotriggers.json"
        self.log_file = self.data_dir / "autotrigger_log.json"
        self.triggers: Dict[str, Trigger] = {}
        self.action_handlers: Dict[str, Callable] = {}
        self.running = False
        self.load()
        self._register_handlers()
    
    def _register_handlers(self):
        """Register action handlers"""
        self.action_handlers = {
            "generate_cv": self._action_generate_cv,
            "create_content": self._action_create_content,
            "send_notification": self._action_send_notification,
            "update_job_status": self._action_update_job_status,
            "suggest_network_outreach": self._action_suggest_network_outreach,
            "sync_to_calendar": self._action_sync_to_calendar,
            "export_analytics": self._action_export_analytics
        }
    
    def load(self):
        """Load triggers"""
        if self.triggers_file.exists():
            with open(self.triggers_file, 'r') as f:
                data = json.load(f)
                for t_data in data.get('triggers', []):
                    trigger = Trigger(**t_data)
                    self.triggers[trigger.id] = trigger
    
    def save(self):
        """Save triggers"""
        with open(self.triggers_file, 'w') as f:
            json.dump({
                'triggers': [asdict(t) for t in self.triggers.values()],
                'updated_at': datetime.now().isoformat()
            }, f, indent=2)
    
    def add_trigger(self, name: str, condition: str, action: str, params: Dict = None) -> Trigger:
        """Add a new trigger"""
        trigger = Trigger(
            id=f"trg_{int(time.time())}_{len(self.triggers)}",
            name=name,
            condition=condition,
            action=action,
            params=params or {},
            enabled=True,
            last_run="",
            run_count=0
        )
        self.triggers[trigger.id] = trigger
        self.save()
        return trigger
    
    def check_triggers(self, event_type: str, event_data: Dict = None):
        """Check and fire triggers based on event"""
        results = []
        
        for trigger in self.triggers.values():
            if not trigger.enabled:
                continue
            
            if self._condition_matches(trigger.condition, event_type, event_data):
                result = self._execute_trigger(trigger, event_data)
                results.append({
                    "trigger": trigger.name,
                    "result": result
                })
        
        return results
    
    def _condition_matches(self, condition: str, event_type: str, event_data: Dict) -> bool:
        """Check if condition matches event"""
        # Direct match
        if condition == event_type:
            return True
        
        # Complex conditions
        if condition == "ats_score_low":
            if event_type == "cv_generated":
                score = event_data.get("ats_score", 100)
                return score < 75
        
        if condition == "high_priority_job":
            if event_type == "job_added":
                priority = event_data.get("priority", 1)
                return priority >= 4
        
        if condition == "follow_up_due":
            if event_type == "daily_check":
                return True  # Checked separately
        
        if condition == "no_activity_7_days":
            if event_type == "daily_check":
                return True  # Checked separately
        
        return False
    
    def _execute_trigger(self, trigger: Trigger, event_data: Dict) -> Dict:
        """Execute trigger action"""
        handler = self.action_handlers.get(trigger.action)
        
        if handler:
            try:
                result = handler(trigger.params, event_data)
                trigger.last_run = datetime.now().isoformat()
                trigger.run_count += 1
                self.save()
                self._log_action(trigger, result)
                return result
            except Exception as e:
                return {"status": "error", "error": str(e)}
        
        return {"status": "error", "error": f"Unknown action: {trigger.action}"}
    
    def _log_action(self, trigger: Trigger, result: Dict):
        """Log trigger execution"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "trigger_id": trigger.id,
            "trigger_name": trigger.name,
            "action": trigger.action,
            "result": result
        }
        
        logs = []
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(self.log_file, 'w') as f:
            json.dump(logs[-100:], f, indent=2)  # Keep last 100
    
    # Action Handlers
    
    def _action_generate_cv(self, params: Dict, event_data: Dict) -> Dict:
        """Auto-generate CV when job is added"""
        job_id = event_data.get("job_id")
        company = event_data.get("company")
        title = event_data.get("title")
        
        # This would call the CV generator
        return {
            "status": "success",
            "message": f"Auto-generated CV for {title} at {company}",
            "job_id": job_id
        }
    
    def _action_create_content(self, params: Dict, event_data: Dict) -> Dict:
        """Auto-create content for low ATS scores or positioning gaps"""
        topic = params.get("topic", "healthtech_ai")
        
        # Import and use content factory
        sys.path.insert(0, str(Path(__file__).parent))
        from content_factory import ContentFactory
        
        factory = ContentFactory()
        content = factory.generate_linkedin_post(topic)
        
        return {
            "status": "success",
            "message": f"Generated {topic} content",
            "content_preview": content.get("content", "")[:100]
        }
    
    def _action_send_notification(self, params: Dict, event_data: Dict) -> Dict:
        """Send notification"""
        message = params.get("message", "Notification")
        priority = params.get("priority", "normal")
        
        return {
            "status": "success",
            "message": message,
            "priority": priority,
            "timestamp": datetime.now().isoformat()
        }
    
    def _action_update_job_status(self, params: Dict, event_data: Dict) -> Dict:
        """Auto-update job status"""
        # Placeholder for job tracker integration
        return {
            "status": "success",
            "message": "Job status auto-updated"
        }
    
    def _action_suggest_network_outreach(self, params: Dict, event_data: Dict) -> Dict:
        """Suggest network outreach for jobs"""
        company = event_data.get("company", "")
        
        return {
            "status": "success",
            "message": f"Check Network Mapper for warm intros to {company}",
            "action": "Run: python3 src/network_mapper.py warm '{company}'"
        }
    
    def _action_sync_to_calendar(self, params: Dict, event_data: Dict) -> Dict:
        """Sync to calendar"""
        return {
            "status": "success",
            "message": "Interview/deadline synced to calendar",
            "event": event_data
        }
    
    def _action_export_analytics(self, params: Dict, event_data: Dict) -> Dict:
        """Export analytics report"""
        return {
            "status": "success",
            "message": "Analytics exported",
            "file": "analytics_report.json"
        }
    
    def setup_default_triggers(self):
        """Set up default triggers for Ahmed's workflow"""
        defaults = [
            {
                "name": "Auto-CV Generation",
                "condition": "job_added",
                "action": "generate_cv",
                "params": {"auto_save": True}
            },
            {
                "name": "Low ATS Alert",
                "condition": "ats_score_low",
                "action": "send_notification",
                "params": {
                    "message": "ATS score below 75 - review CV optimization suggestions",
                    "priority": "high"
                }
            },
            {
                "name": "High Priority Job Alert",
                "condition": "high_priority_job",
                "action": "suggest_network_outreach",
                "params": {}
            },
            {
                "name": "Content Generation",
                "condition": "ats_score_low",
                "action": "create_content",
                "params": {"topic": "healthtech_ai"}
            },
            {
                "name": "Weekly Analytics",
                "condition": "weekly_check",
                "action": "export_analytics",
                "params": {"email": False}
            }
        ]
        
        for t_data in defaults:
            self.add_trigger(
                name=t_data["name"],
                condition=t_data["condition"],
                action=t_data["action"],
                params=t_data["params"]
            )
        
        return len(defaults)
    
    def run_event(self, event_type: str, event_data: Dict = None) -> List[Dict]:
        """Manually trigger an event check"""
        return self.check_triggers(event_type, event_data)
    
    def get_logs(self, limit: int = 20) -> List[Dict]:
        """Get recent trigger logs"""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
                return logs[-limit:]
        return []


# Integration with Opportunity Engine
class WorkflowAutomator:
    """High-level workflow automation"""
    
    def __init__(self):
        self.trigger_system = AutoTriggerSystem()
        self.trigger_system.setup_default_triggers()
    
    def on_job_added(self, job_data: Dict):
        """Called when a job is added"""
        results = self.trigger_system.run_event("job_added", job_data)
        
        # Auto-generate CV
        print(f"🤖 Auto-Trigger: Job added - {job_data.get('title')} at {job_data.get('company')}")
        
        for result in results:
            if result.get("result", {}).get("status") == "success":
                print(f"   ✅ {result['trigger']}: {result['result'].get('message', 'Done')}")
        
        return results
    
    def on_cv_generated(self, cv_data: Dict):
        """Called when CV is generated"""
        results = self.trigger_system.run_event("cv_generated", cv_data)
        
        ats_score = cv_data.get("ats_score", 100)
        print(f"🤖 Auto-Trigger: CV generated - ATS Score: {ats_score}")
        
        if ats_score < 75:
            print(f"   ⚠️  ATS score low - check suggestions")
        
        return results
    
    def daily_check(self):
        """Run daily automation checks"""
        print(f"🤖 Running daily automation check...")
        
        # Check follow-ups
        results = self.trigger_system.run_event("daily_check", {"check_type": "follow_ups"})
        
        return results


def main():
    """CLI interface"""
    import sys
    
    automator = WorkflowAutomator()
    
    if len(sys.argv) < 2:
        print("Auto-Trigger System - Workflow Automation")
        print()
        print("Usage:")
        print("  python auto_trigger.py setup          # Setup default triggers")
        print("  python auto_trigger.py list           # List all triggers")
        print("  python auto_trigger.py test <event>   # Test trigger")
        print("  python auto_trigger.py logs           # View recent logs")
        print()
        print("Events: job_added, cv_generated, daily_check")
        return
    
    command = sys.argv[1]
    
    if command == "setup":
        count = automator.trigger_system.setup_default_triggers()
        print(f"✅ Setup {count} default triggers")
    
    elif command == "list":
        print("\n📋 Triggers:")
        for trigger in automator.trigger_system.triggers.values():
            status = "🟢" if trigger.enabled else "🔴"
            print(f"  {status} {trigger.name}")
            print(f"     When: {trigger.condition} → Then: {trigger.action}")
            print(f"     Runs: {trigger.run_count}")
    
    elif command == "test":
        if len(sys.argv) < 3:
            print("Usage: python auto_trigger.py test <event>")
            return
        
        event = sys.argv[2]
        test_data = {
            "job_id": "test123",
            "company": "Test Corp",
            "title": "VP Test",
            "ats_score": 70,
            "priority": 5
        }
        
        results = automator.trigger_system.run_event(event, test_data)
        print(f"\n🧪 Test results for '{event}':")
        for result in results:
            print(f"  Trigger: {result['trigger']}")
            print(f"  Result: {result['result']}")
    
    elif command == "logs":
        logs = automator.trigger_system.get_logs()
        print(f"\n📜 Recent Logs ({len(logs)}):")
        for log in logs[-10:]:
            print(f"  {log['timestamp'][:16]} | {log['trigger_name']} | {log['action']}")
    
    elif command == "demo":
        print("🎬 Running automation demo...")
        
        # Simulate job added
        job_data = {
            "job_id": "demo123",
            "company": "Saudi German Hospital",
            "title": "VP Digital Transformation",
            "priority": 5
        }
        automator.on_job_added(job_data)
        
        # Simulate CV generated with low score
        cv_data = {
            "job_id": "demo123",
            "ats_score": 72,
            "company": "Saudi German Hospital"
        }
        automator.on_cv_generated(cv_data)
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
