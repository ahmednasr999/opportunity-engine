#!/usr/bin/env python3
"""
Calendar Integration - Sync job deadlines and interviews to calendar
Supports Google Calendar and Outlook
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class CalendarEvent:
    """Calendar event"""
    id: str
    title: str
    start_time: str
    end_time: str
    description: str
    event_type: str  # interview, deadline, follow_up, reminder
    job_id: str
    location: str
    attendees: List[str]
    reminder_minutes: int


class CalendarIntegration:
    """Calendar sync for job search"""
    
    def __init__(self, data_dir: str = "/root/.openclaw/workspace/tools/cv-optimizer/data"):
        self.data_dir = Path(data_dir)
        self.events_file = self.data_dir / "calendar_events.json"
        self.events: List[Dict] = []
        self.load()
    
    def load(self):
        """Load calendar events"""
        if self.events_file.exists():
            with open(self.events_file, 'r') as f:
                self.events = json.load(f)
    
    def save(self):
        """Save calendar events"""
        with open(self.events_file, 'w') as f:
            json.dump(self.events, f, indent=2)
    
    def add_event(self, 
                  title: str,
                  start_time: str,
                  end_time: str,
                  event_type: str,
                  job_id: str = "",
                  description: str = "",
                  location: str = "",
                  reminder_minutes: int = 60) -> Dict:
        """Add a calendar event"""
        
        event = {
            "id": f"evt_{int(datetime.now().timestamp())}",
            "title": title,
            "start_time": start_time,
            "end_time": end_time,
            "event_type": event_type,
            "job_id": job_id,
            "description": description,
            "location": location,
            "attendees": [],
            "reminder_minutes": reminder_minutes,
            "created_at": datetime.now().isoformat(),
            "synced": False
        }
        
        self.events.append(event)
        self.save()
        
        # Generate .ics file for easy import
        self._generate_ics(event)
        
        return event
    
    def _generate_ics(self, event: Dict):
        """Generate ICS file for calendar import"""
        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Opportunity Engine//Calendar//EN
BEGIN:VEVENT
UID:{event['id']}@opportunity-engine
DTSTART:{event['start_time'].replace('-', '').replace(':', '').replace('T', 'T')}
DTEND:{event['end_time'].replace('-', '').replace(':', '').replace('T', 'T')}
SUMMARY:{event['title']}
DESCRIPTION:{event['description']}
LOCATION:{event['location']}
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Reminder
TRIGGER:-PT{event['reminder_minutes']}M
END:VALARM
END:VEVENT
END:VCALENDAR"""
        
        ics_file = self.data_dir / f"{event['id']}.ics"
        with open(ics_file, 'w') as f:
            f.write(ics_content)
    
    def schedule_interview(self, company: str, role: str, date_str: str, time_str: str, 
                          duration_minutes: int = 60, location: str = "", job_id: str = "") -> Dict:
        """Schedule an interview"""
        
        # Parse date and time
        start_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        
        # Create prep reminder (1 day before)
        prep_time = start_dt - timedelta(days=1)
        self.add_event(
            title=f"📋 Prep for {company} Interview",
            start_time=prep_time.isoformat(),
            end_time=(prep_time + timedelta(minutes=30)).isoformat(),
            event_type="reminder",
            job_id=job_id,
            description=f"Prepare for {role} interview at {company}. Review job description, prepare questions, research company.",
            reminder_minutes=0
        )
        
        # Create interview event
        event = self.add_event(
            title=f"🤝 Interview: {company} - {role}",
            start_time=start_dt.isoformat(),
            end_time=end_dt.isoformat(),
            event_type="interview",
            job_id=job_id,
            description=f"Interview for {role} position at {company}.\n\nDon't forget:\n- Bring copies of CV\n- Prepare questions\n- Research company news",
            location=location,
            reminder_minutes=60
        )
        
        # Create follow-up reminder (2 hours after)
        follow_time = end_dt + timedelta(hours=2)
        self.add_event(
            title=f"📧 Send Thank You: {company}",
            start_time=follow_time.isoformat(),
            end_time=(follow_time + timedelta(minutes=15)).isoformat(),
            event_type="follow_up",
            job_id=job_id,
            description=f"Send thank you email to {company} interviewers.",
            reminder_minutes=0
        )
        
        return event
    
    def add_application_deadline(self, company: str, role: str, deadline_date: str, job_id: str = "") -> Dict:
        """Add application deadline reminder"""
        
        deadline_dt = datetime.strptime(deadline_date, "%Y-%m-%d")
        
        # Day before reminder
        reminder_dt = deadline_dt - timedelta(days=1)
        event = self.add_event(
            title=f"⏰ Apply: {company} - {role}",
            start_time=reminder_dt.isoformat(),
            end_time=(reminder_dt + timedelta(minutes=30)).isoformat(),
            event_type="deadline",
            job_id=job_id,
            description=f"Application deadline for {role} at {company}. Submit application today!",
            reminder_minutes=0
        )
        
        return event
    
    def add_follow_up_reminder(self, company: str, contact_name: str, days: int = 7, job_id: str = "") -> Dict:
        """Add follow-up reminder"""
        
        reminder_dt = datetime.now() + timedelta(days=days)
        
        event = self.add_event(
            title=f"🔔 Follow Up: {company} ({contact_name})",
            start_time=reminder_dt.isoformat(),
            end_time=(reminder_dt + timedelta(minutes=15)).isoformat(),
            event_type="follow_up",
            job_id=job_id,
            description=f"Follow up on {company} application. Check status, express continued interest.",
            reminder_minutes=0
        )
        
        return event
    
    def get_upcoming_events(self, days: int = 7) -> List[Dict]:
        """Get upcoming events"""
        now = datetime.now()
        cutoff = now + timedelta(days=days)
        
        upcoming = []
        for event in self.events:
            try:
                event_time = datetime.fromisoformat(event['start_time'])
                if now <= event_time <= cutoff:
                    upcoming.append(event)
            except:
                pass
        
        return sorted(upcoming, key=lambda e: e['start_time'])
    
    def get_events_for_job(self, job_id: str) -> List[Dict]:
        """Get all events for a specific job"""
        return [e for e in self.events if e.get('job_id') == job_id]
    
    def export_to_google_calendar(self) -> str:
        """Generate Google Calendar import file"""
        # Create combined ICS file
        ics_lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Opportunity Engine//EN"]
        
        for event in self.events:
            ics_lines.extend([
                "BEGIN:VEVENT",
                f"UID:{event['id']}@opportunity-engine",
                f"DTSTART:{event['start_time'].replace('-', '').replace(':', '').replace('T', 'T')}",
                f"DTEND:{event['end_time'].replace('-', '').replace(':', '').replace('T', 'T')}",
                f"SUMMARY:{event['title']}",
                f"DESCRIPTION:{event['description']}",
                f"LOCATION:{event['location']}",
                "END:VEVENT"
            ])
        
        ics_lines.append("END:VCALENDAR")
        
        ics_file = self.data_dir / "opportunity_engine_calendar.ics"
        with open(ics_file, 'w') as f:
            f.write("\n".join(ics_lines))
        
        return str(ics_file)
    
    def sync_with_job_tracker(self, job_tracker_data: List[Dict]):
        """Auto-sync job tracker data to calendar"""
        events_created = 0
        
        for job in job_tracker_data:
            job_id = job.get('id', '')
            company = job.get('company', '')
            title = job.get('title', '')
            status = job.get('status', '')
            
            # Check if already has events
            existing = self.get_events_for_job(job_id)
            
            if not existing:
                # Add follow-up reminder for applied jobs
                if status == 'Applied':
                    self.add_follow_up_reminder(company, "Recruiter", 7, job_id)
                    events_created += 1
        
        return events_created
    
    def print_weekly_schedule(self):
        """Print upcoming week's schedule"""
        events = self.get_upcoming_events(7)
        
        print("\n" + "=" * 60)
        print("📅 UPCOMING WEEK SCHEDULE")
        print("=" * 60)
        
        if not events:
            print("\nNo events scheduled for the next 7 days.")
            return
        
        current_date = None
        for event in events:
            event_time = datetime.fromisoformat(event['start_time'])
            event_date = event_time.strftime("%A, %B %d")
            
            if event_date != current_date:
                print(f"\n{event_date}")
                print("-" * 40)
                current_date = event_date
            
            time_str = event_time.strftime("%H:%M")
            emoji = {
                "interview": "🤝",
                "deadline": "⏰",
                "follow_up": "📧",
                "reminder": "📋"
            }.get(event['event_type'], "📅")
            
            print(f"  {emoji} {time_str} - {event['title']}")


def main():
    """CLI interface"""
    import sys
    
    calendar = CalendarIntegration()
    
    if len(sys.argv) < 2:
        calendar.print_weekly_schedule()
        return
    
    command = sys.argv[1]
    
    if command == "interview":
        if len(sys.argv) < 6:
            print("Usage: python calendar_integration.py interview 'Company' 'Role' 'YYYY-MM-DD' 'HH:MM' [location]")
            return
        
        company = sys.argv[2]
        role = sys.argv[3]
        date = sys.argv[4]
        time = sys.argv[5]
        location = sys.argv[6] if len(sys.argv) > 6 else ""
        
        event = calendar.schedule_interview(company, role, date, time, location=location)
        print(f"✅ Interview scheduled: {event['title']}")
        print(f"   When: {date} at {time}")
        print(f"   Reminders: Prep (1 day before) + Thank you (2 hours after)")
    
    elif command == "deadline":
        if len(sys.argv) < 5:
            print("Usage: python calendar_integration.py deadline 'Company' 'Role' 'YYYY-MM-DD'")
            return
        
        company = sys.argv[2]
        role = sys.argv[3]
        date = sys.argv[4]
        
        event = calendar.add_application_deadline(company, role, date)
        print(f"✅ Deadline reminder set: {event['title']}")
    
    elif command == "followup":
        if len(sys.argv) < 5:
            print("Usage: python calendar_integration.py followup 'Company' 'Contact' [days]")
            return
        
        company = sys.argv[2]
        contact = sys.argv[3]
        days = int(sys.argv[4]) if len(sys.argv) > 4 else 7
        
        event = calendar.add_follow_up_reminder(company, contact, days)
        print(f"✅ Follow-up reminder: {event['title']}")
    
    elif command == "export":
        ics_file = calendar.export_to_google_calendar()
        print(f"✅ Calendar exported: {ics_file}")
        print("   Import this file to Google Calendar or Outlook")
    
    elif command == "list":
        calendar.print_weekly_schedule()
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
