#!/usr/bin/env python3
"""
Phase 6 - Network Enhancements
Features: LinkedIn Integration (mock), Introduction Requests, Network Health Score,
          Outreach Sequences, Contact Import CSV, Relationship Timeline,
          Meeting Notes, Follow-up Streak, Contact Groups, Gift Ideas,
          Conversation History, Birthday Alerts
"""

import json
import csv
import io
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path


class LinkedInIntegration:
    """Mock LinkedIn API integration"""

    def connect(self, profile_url: str = "") -> Dict:
        return {
            "status": "connected",
            "platform": "LinkedIn",
            "profile_url": profile_url or "https://linkedin.com/in/ahmed-nasr",
            "mock": True,
            "features": ["profile_sync", "connection_import", "job_alerts", "message_tracking"],
            "synced_data": {
                "connections": 1247,
                "pending_invitations": 12,
                "profile_views_30d": 89,
                "search_appearances_7d": 34,
                "post_impressions_30d": 4520,
                "ssi_score": 72
            },
            "last_sync": datetime.now().isoformat()
        }

    def get_profile_stats(self) -> Dict:
        return {
            "profile_strength": "All-Star",
            "connections": 1247,
            "followers": 1589,
            "endorsements": 45,
            "recommendations": 8,
            "profile_views": {"weekly": [23, 18, 34, 28, 42, 31, 38]},
            "ssi_score": {
                "total": 72,
                "establish_brand": 78,
                "find_right_people": 65,
                "engage_insights": 71,
                "build_relationships": 74
            }
        }

    def import_connections(self) -> Dict:
        connections = [
            {"name": "Sarah Al-Rashid", "title": "CEO, MENA HealthTech", "connected_date": "2023-05-15", "industry": "Healthcare"},
            {"name": "James Wilson", "title": "VP Engineering, TechCorp", "connected_date": "2024-01-20", "industry": "Technology"},
            {"name": "Fatima Hassan", "title": "Director, Hospital Group", "connected_date": "2024-06-10", "industry": "Healthcare"},
            {"name": "Michael Chen", "title": "CTO, AI Health", "connected_date": "2025-03-05", "industry": "AI/ML"},
            {"name": "Aisha Mohammed", "title": "HR Director, Gulf Medical", "connected_date": "2025-08-12", "industry": "Healthcare"},
        ]
        return {
            "imported": len(connections),
            "connections": connections,
            "duplicates_skipped": 0,
            "new_contacts": len(connections)
        }


class IntroductionRequestGenerator:
    """Auto-generate introduction request messages"""

    TEMPLATES = {
        "warm": "Hi {mutual_contact},\n\nI hope you're doing well! I noticed you're connected with {target_name} at {target_company}. I'm currently exploring opportunities in {field} and believe {target_name}'s insights would be incredibly valuable.\n\nWould you be open to making a brief introduction? I'd be happy to send you a short blurb about myself that you could forward.\n\nThank you so much!\nAhmed",
        "cold": "Hi {target_name},\n\nI came across your profile and was impressed by your work at {target_company}. As someone passionate about {field}, I'd love to learn from your experience.\n\nWould you be open to a 15-minute virtual coffee?\n\nBest regards,\nAhmed Nasr",
        "referral": "Hi {target_name},\n\n{mutual_contact} suggested I reach out to you regarding the {role} position at {target_company}. With my background in healthcare operations and AI, I believe I could bring significant value to your team.\n\nI'd welcome the chance to discuss this further at your convenience.\n\nBest regards,\nAhmed Nasr"
    }

    def generate(self, target_name: str, target_company: str, mutual_contact: str = "",
                 field: str = "healthcare AI", role: str = "", template_type: str = "warm") -> Dict:
        template = self.TEMPLATES.get(template_type, self.TEMPLATES["warm"])
        message = template.format(
            mutual_contact=mutual_contact or "there",
            target_name=target_name,
            target_company=target_company,
            field=field,
            role=role or "the open position"
        )
        
        return {
            "message": message,
            "type": template_type,
            "target": {"name": target_name, "company": target_company},
            "mutual_contact": mutual_contact,
            "tips": [
                "Personalize the first line with something specific",
                "Keep it under 150 words",
                "Include a clear ask (coffee chat, intro, etc.)",
                "Follow up in 5-7 days if no response"
            ],
            "generated_at": datetime.now().isoformat()
        }

    def batch_generate(self, targets: List[Dict]) -> List[Dict]:
        return [
            self.generate(
                t.get("name", ""), t.get("company", ""),
                t.get("mutual_contact", ""), t.get("field", "healthcare AI")
            )
            for t in targets
        ]


class NetworkHealthScore:
    """Calculate overall network strength metric"""

    def calculate(self, contacts: List[Dict] = None) -> Dict:
        if not contacts:
            contacts = self._sample_contacts()
        
        total = len(contacts)
        if total == 0:
            return {"score": 0, "grade": "F", "breakdown": {}}
        
        # Diversity score (different industries)
        industries = set(c.get("industry", "Unknown") for c in contacts)
        diversity_score = min(25, len(industries) * 5)
        
        # Engagement score (recent contacts)
        now = datetime.now()
        active_30d = 0
        for c in contacts:
            try:
                last = datetime.fromisoformat(c.get("last_contact", "2020-01-01"))
                if (now - last).days <= 30:
                    active_30d += 1
            except:
                pass
        engagement_score = min(25, round(active_30d / max(1, total) * 100))
        
        # Size score
        size_score = min(25, total // 4)
        
        # Seniority score
        senior = sum(1 for c in contacts if any(t in c.get("title", "").lower() for t in ["vp", "director", "ceo", "cto", "coo", "head"]))
        seniority_score = min(25, senior * 5)
        
        total_score = diversity_score + engagement_score + size_score + seniority_score
        grade = "A+" if total_score >= 90 else "A" if total_score >= 80 else "B" if total_score >= 65 else "C" if total_score >= 50 else "D" if total_score >= 35 else "F"
        
        return {
            "score": total_score,
            "grade": grade,
            "breakdown": {
                "diversity": {"score": diversity_score, "max": 25, "detail": f"{len(industries)} industries"},
                "engagement": {"score": engagement_score, "max": 25, "detail": f"{active_30d} active in 30 days"},
                "size": {"score": size_score, "max": 25, "detail": f"{total} total contacts"},
                "seniority": {"score": seniority_score, "max": 25, "detail": f"{senior} senior contacts"}
            },
            "recommendations": [
                "Diversify your network across more industries" if diversity_score < 15 else "Good industry diversity",
                "Reach out to more contacts this month" if engagement_score < 15 else "Strong engagement",
                "Grow your network — aim for 200+ contacts" if size_score < 15 else "Healthy network size",
                "Connect with more senior leaders" if seniority_score < 15 else "Good seniority mix"
            ]
        }

    def _sample_contacts(self) -> List[Dict]:
        return [
            {"name": f"Contact {i}", "industry": random.choice(["Healthcare", "Tech", "Finance", "Consulting"]),
             "title": random.choice(["VP Operations", "Director", "Manager", "CEO", "Engineer"]),
             "last_contact": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat()}
            for i in range(50)
        ]


class OutreachSequences:
    """Multi-touch email/message outreach sequences"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.sequences_file = self.data_dir / "outreach_sequences.json"
        self.sequences = self._load()

    def _load(self) -> List[Dict]:
        if self.sequences_file.exists():
            return json.loads(self.sequences_file.read_text())
        return []

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.sequences_file.write_text(json.dumps(self.sequences, indent=2))

    def create_sequence(self, name: str, target: str, touchpoints: int = 4) -> Dict:
        templates = [
            {"day": 0, "type": "initial", "subject": f"Connecting re: opportunities at {target}",
             "body": f"Hi [Name],\n\nI'm reaching out because I'm interested in opportunities at {target}. My background in healthcare operations and AI might be a great fit.\n\nWould you be open to a brief conversation?\n\nBest,\nAhmed"},
            {"day": 3, "type": "follow_up_1", "subject": "Quick follow-up",
             "body": "Hi [Name],\n\nJust wanted to follow up on my previous message. I'd love to hear your perspective on the team and culture.\n\nNo pressure at all — just wanted to make sure my note didn't get lost.\n\nBest,\nAhmed"},
            {"day": 7, "type": "value_add", "subject": "Thought you might find this interesting",
             "body": "Hi [Name],\n\nI came across this article about [topic] and thought of our conversation. [Link]\n\nHope it's useful!\n\nBest,\nAhmed"},
            {"day": 14, "type": "final", "subject": "Last note from me",
             "body": "Hi [Name],\n\nI know you're busy, so this will be my last message. If you're ever open to connecting, I'd welcome the conversation.\n\nWishing you all the best,\nAhmed"}
        ]

        seq = {
            "id": f"seq{len(self.sequences)+1}",
            "name": name,
            "target": target,
            "touchpoints": templates[:touchpoints],
            "status": "active",
            "current_step": 0,
            "created_at": datetime.now().isoformat(),
            "contacts": []
        }
        self.sequences.append(seq)
        self._save()
        return seq

    def get_all(self) -> List[Dict]:
        return self.sequences

    def add_contact_to_sequence(self, seq_id: str, contact: Dict) -> bool:
        for seq in self.sequences:
            if seq["id"] == seq_id:
                seq["contacts"].append({
                    **contact,
                    "current_step": 0,
                    "added_at": datetime.now().isoformat()
                })
                self._save()
                return True
        return False

    def advance_step(self, seq_id: str, contact_email: str) -> Dict:
        for seq in self.sequences:
            if seq["id"] == seq_id:
                for c in seq["contacts"]:
                    if c.get("email") == contact_email:
                        c["current_step"] = c.get("current_step", 0) + 1
                        self._save()
                        step = c["current_step"]
                        if step < len(seq["touchpoints"]):
                            return {"next_message": seq["touchpoints"][step], "step": step}
                        return {"completed": True}
        return {"error": "Not found"}


class ContactImportCSV:
    """Import contacts from CSV/spreadsheet"""

    EXPECTED_HEADERS = ["name", "email", "company", "title", "phone", "industry", "notes"]

    def parse_csv(self, csv_content: str) -> Dict:
        reader = csv.DictReader(io.StringIO(csv_content))
        contacts = []
        errors = []
        
        for i, row in enumerate(reader):
            if not row.get("name") and not row.get("Name"):
                errors.append(f"Row {i+1}: Missing name")
                continue
            
            contact = {
                "name": row.get("name", row.get("Name", "")),
                "email": row.get("email", row.get("Email", "")),
                "company": row.get("company", row.get("Company", "")),
                "title": row.get("title", row.get("Title", "")),
                "phone": row.get("phone", row.get("Phone", "")),
                "industry": row.get("industry", row.get("Industry", "")),
                "notes": row.get("notes", row.get("Notes", "")),
                "source": "csv_import",
                "imported_at": datetime.now().isoformat()
            }
            contacts.append(contact)

        return {
            "imported": len(contacts),
            "errors": len(errors),
            "error_details": errors[:10],
            "contacts": contacts,
            "sample": contacts[:5]
        }

    def get_template(self) -> str:
        return "name,email,company,title,phone,industry,notes\nJohn Doe,john@example.com,Acme Corp,VP Engineering,+1-555-0100,Technology,Met at conference"

    def validate_csv(self, csv_content: str) -> Dict:
        try:
            reader = csv.reader(io.StringIO(csv_content))
            headers = next(reader)
            rows = list(reader)
            return {
                "valid": True,
                "headers": headers,
                "row_count": len(rows),
                "missing_recommended": [h for h in self.EXPECTED_HEADERS if h not in [x.lower() for x in headers]]
            }
        except Exception as e:
            return {"valid": False, "error": str(e)}


class RelationshipTimeline:
    """Visual timeline of relationship history with contacts"""

    def get_timeline(self, contact_name: str) -> Dict:
        # Generate sample timeline for any contact
        events = [
            {"date": "2024-03-15", "type": "connected", "description": f"Connected with {contact_name} on LinkedIn"},
            {"date": "2024-06-20", "type": "meeting", "description": "Coffee meeting — discussed healthcare AI trends"},
            {"date": "2024-09-10", "type": "email", "description": "Shared article on hospital operations"},
            {"date": "2025-01-05", "type": "referral", "description": "Referred to VP role at their company"},
            {"date": "2025-04-18", "type": "meeting", "description": "Lunch meeting — career advice"},
            {"date": "2025-09-22", "type": "introduction", "description": f"{contact_name} introduced me to their CTO"},
            {"date": "2026-01-15", "type": "follow_up", "description": "Caught up on recent projects"},
        ]
        
        return {
            "contact": contact_name,
            "events": events,
            "total_interactions": len(events),
            "relationship_strength": "strong",
            "first_contact": events[0]["date"],
            "last_contact": events[-1]["date"],
            "relationship_duration_days": 672,
            "interaction_types": {"meeting": 2, "email": 1, "referral": 1, "introduction": 1, "connected": 1, "follow_up": 1}
        }


class MeetingNotes:
    """Track meeting notes with contacts"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.notes_file = self.data_dir / "meeting_notes.json"
        self.notes = self._load()

    def _load(self) -> List[Dict]:
        if self.notes_file.exists():
            return json.loads(self.notes_file.read_text())
        return [
            {"id": "mn1", "contact": "Sarah Al-Rashid", "date": "2026-02-01", "type": "video_call",
             "duration_min": 30, "topics": ["Career transition", "AI in healthcare"],
             "action_items": ["Send CV", "Follow up in 2 weeks"], "notes": "Very supportive, willing to refer"},
        ]

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.notes_file.write_text(json.dumps(self.notes, indent=2))

    def add(self, note_data: Dict) -> Dict:
        note = {
            "id": f"mn{len(self.notes)+1}",
            "contact": note_data.get("contact", ""),
            "date": note_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            "type": note_data.get("type", "meeting"),
            "duration_min": note_data.get("duration_min", 30),
            "topics": note_data.get("topics", []),
            "action_items": note_data.get("action_items", []),
            "notes": note_data.get("notes", ""),
        }
        self.notes.append(note)
        self._save()
        return note

    def get_all(self) -> List[Dict]:
        return self.notes

    def get_by_contact(self, contact_name: str) -> List[Dict]:
        return [n for n in self.notes if contact_name.lower() in n.get("contact", "").lower()]


class FollowUpStreak:
    """Track follow-up consistency streaks"""

    def calculate(self, contacts: List[Dict] = None) -> Dict:
        if not contacts:
            contacts = [
                {"name": "Contact A", "follow_ups": ["2026-01-01", "2026-01-08", "2026-01-15", "2026-01-22", "2026-01-29", "2026-02-05", "2026-02-12"]},
                {"name": "Contact B", "follow_ups": ["2026-01-10", "2026-02-10"]},
            ]
        
        streaks = []
        for c in contacts:
            dates = sorted(c.get("follow_ups", []))
            streak = 0
            max_streak = 0
            for i in range(1, len(dates)):
                try:
                    d1 = datetime.strptime(dates[i-1], "%Y-%m-%d")
                    d2 = datetime.strptime(dates[i], "%Y-%m-%d")
                    if (d2 - d1).days <= 10:
                        streak += 1
                    else:
                        max_streak = max(max_streak, streak)
                        streak = 0
                except:
                    pass
            max_streak = max(max_streak, streak)
            streaks.append({"name": c["name"], "current_streak": streak, "best_streak": max_streak})
        
        return {
            "streaks": streaks,
            "overall_consistency": round(sum(s["current_streak"] for s in streaks) / max(1, len(streaks)), 1),
            "best_performer": max(streaks, key=lambda s: s["best_streak"])["name"] if streaks else None,
            "tips": [
                "Set weekly reminders for key contacts",
                "Even a quick LinkedIn like counts as a touchpoint",
                "Aim for at least monthly contact with top 20 people"
            ]
        }


class ContactGroups:
    """Organize contacts into groups/tags"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.groups_file = self.data_dir / "contact_groups.json"
        self.groups = self._load()

    def _load(self) -> List[Dict]:
        if self.groups_file.exists():
            return json.loads(self.groups_file.read_text())
        return [
            {"id": "g1", "name": "Healthcare Leaders", "color": "#38b2ac", "contacts": ["Sarah Al-Rashid", "Dr. Hassan"], "count": 2},
            {"id": "g2", "name": "Tech Founders", "color": "#805ad5", "contacts": ["Michael Chen", "Lisa Park"], "count": 2},
            {"id": "g3", "name": "Recruiters", "color": "#ed8936", "contacts": ["James Wilson", "Anna Lee"], "count": 2},
            {"id": "g4", "name": "Mentors", "color": "#4299e1", "contacts": ["Prof. Ahmed", "Mark Johnson"], "count": 2},
        ]

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.groups_file.write_text(json.dumps(self.groups, indent=2))

    def get_all(self) -> List[Dict]:
        return self.groups

    def create(self, name: str, color: str = "#4299e1") -> Dict:
        group = {"id": f"g{len(self.groups)+1}", "name": name, "color": color, "contacts": [], "count": 0}
        self.groups.append(group)
        self._save()
        return group

    def add_contact(self, group_id: str, contact_name: str) -> bool:
        for g in self.groups:
            if g["id"] == group_id:
                if contact_name not in g["contacts"]:
                    g["contacts"].append(contact_name)
                    g["count"] = len(g["contacts"])
                    self._save()
                return True
        return False

    def remove_contact(self, group_id: str, contact_name: str) -> bool:
        for g in self.groups:
            if g["id"] == group_id:
                g["contacts"] = [c for c in g["contacts"] if c != contact_name]
                g["count"] = len(g["contacts"])
                self._save()
                return True
        return False


class GiftIdeasLog:
    """Track gift ideas and occasions for contacts"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.gifts_file = self.data_dir / "gift_ideas.json"
        self.gifts = self._load()

    def _load(self) -> List[Dict]:
        if self.gifts_file.exists():
            return json.loads(self.gifts_file.read_text())
        return [
            {"id": "gift1", "contact": "Sarah Al-Rashid", "occasion": "Thank you (referral)",
             "idea": "Luxury notebook set", "budget": "$50-100", "status": "planned", "date": "2026-02-20"},
        ]

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.gifts_file.write_text(json.dumps(self.gifts, indent=2))

    def add(self, gift_data: Dict) -> Dict:
        gift = {
            "id": f"gift{len(self.gifts)+1}",
            "contact": gift_data.get("contact", ""),
            "occasion": gift_data.get("occasion", ""),
            "idea": gift_data.get("idea", ""),
            "budget": gift_data.get("budget", "$25-50"),
            "status": "planned",
            "date": gift_data.get("date", ""),
        }
        self.gifts.append(gift)
        self._save()
        return gift

    def get_all(self) -> List[Dict]:
        return self.gifts

    def get_upcoming(self) -> List[Dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        return [g for g in self.gifts if g.get("status") == "planned" and g.get("date", "9999") >= today]


class ConversationHistory:
    """Track conversation history with contacts"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.history_file = self.data_dir / "conversations.json"
        self.conversations = self._load()

    def _load(self) -> List[Dict]:
        if self.history_file.exists():
            return json.loads(self.history_file.read_text())
        return []

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.history_file.write_text(json.dumps(self.conversations, indent=2))

    def add(self, contact: str, channel: str, summary: str, topics: List[str] = None) -> Dict:
        conv = {
            "id": f"conv{len(self.conversations)+1}",
            "contact": contact,
            "channel": channel,
            "date": datetime.now().isoformat(),
            "summary": summary,
            "topics": topics or [],
            "sentiment": "positive"
        }
        self.conversations.append(conv)
        self._save()
        return conv

    def get_by_contact(self, contact: str) -> List[Dict]:
        return [c for c in self.conversations if contact.lower() in c.get("contact", "").lower()]

    def get_all(self) -> List[Dict]:
        return self.conversations


class BirthdayAnniversaryAlerts:
    """Track and alert on birthdays and work anniversaries"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.alerts_file = self.data_dir / "birthday_alerts.json"
        self.alerts = self._load()

    def _load(self) -> List[Dict]:
        if self.alerts_file.exists():
            return json.loads(self.alerts_file.read_text())
        return [
            {"contact": "Sarah Al-Rashid", "type": "birthday", "date": "03-15", "notes": "Likes coffee"},
            {"contact": "James Wilson", "type": "work_anniversary", "date": "06-01", "notes": "5 years at TechCorp"},
            {"contact": "Michael Chen", "type": "birthday", "date": "02-28", "notes": ""},
        ]

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.alerts_file.write_text(json.dumps(self.alerts, indent=2))

    def add(self, contact: str, alert_type: str, date: str, notes: str = "") -> Dict:
        alert = {"contact": contact, "type": alert_type, "date": date, "notes": notes}
        self.alerts.append(alert)
        self._save()
        return alert

    def get_upcoming(self, days: int = 30) -> List[Dict]:
        today = datetime.now()
        upcoming = []
        for alert in self.alerts:
            try:
                month, day = map(int, alert["date"].split("-"))
                alert_date = today.replace(month=month, day=day)
                if alert_date < today:
                    alert_date = alert_date.replace(year=today.year + 1)
                if (alert_date - today).days <= days:
                    upcoming.append({**alert, "days_until": (alert_date - today).days, "full_date": alert_date.strftime("%Y-%m-%d")})
            except:
                pass
        return sorted(upcoming, key=lambda x: x.get("days_until", 999))

    def get_all(self) -> List[Dict]:
        return self.alerts


class VoiceMemoLogging:
    """Log voice memos for contacts (mock transcription)"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.memos_file = self.data_dir / "voice_memos.json"
        self.memos = self._load()

    def _load(self) -> List[Dict]:
        if self.memos_file.exists():
            return json.loads(self.memos_file.read_text())
        return []

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.memos_file.write_text(json.dumps(self.memos, indent=2))

    def add(self, contact: str, transcript: str, duration_sec: int = 60) -> Dict:
        memo = {
            "id": f"vm{len(self.memos)+1}",
            "contact": contact,
            "transcript": transcript,
            "duration_seconds": duration_sec,
            "recorded_at": datetime.now().isoformat(),
            "tags": self._extract_tags(transcript)
        }
        self.memos.append(memo)
        self._save()
        return memo

    def _extract_tags(self, text: str) -> List[str]:
        keywords = ["follow up", "meeting", "call", "opportunity", "referral", "introduction"]
        return [k for k in keywords if k in text.lower()]

    def get_by_contact(self, contact: str) -> List[Dict]:
        return [m for m in self.memos if contact.lower() in m.get("contact", "").lower()]

    def get_all(self) -> List[Dict]:
        return self.memos


class ColdEmailTemplates:
    """Pre-built cold email templates"""

    def get_templates(self) -> List[Dict]:
        return [
            {"id": "ce1", "name": "Value-First Cold Outreach", "category": "cold_email",
             "subject": "Quick thought on {company}'s {initiative}",
             "body": "Hi {name},\n\nI noticed {company} is working on {initiative}. Having led similar initiatives in healthcare, I wanted to share a quick insight that might be useful:\n\n{value_point}\n\nWould you be open to a brief chat to explore this further?\n\nBest,\nAhmed Nasr"},
            {"id": "ce2", "name": "Mutual Connection", "category": "warm_intro",
             "subject": "{mutual} suggested I reach out",
             "body": "Hi {name},\n\n{mutual} mentioned you might be a great person to connect with regarding {topic}. I'd love to hear your perspective over a 15-minute call.\n\nBest,\nAhmed"},
            {"id": "ce3", "name": "Congratulations Hook", "category": "cold_email",
             "subject": "Congrats on {achievement}!",
             "body": "Hi {name},\n\nI saw the news about {achievement} — congratulations! That's a significant milestone.\n\nI work in a similar space and would love to connect. No pitch — just genuinely impressed and would love to learn from your experience.\n\nBest,\nAhmed Nasr"},
            {"id": "ce4", "name": "Event Follow-up", "category": "warm_follow_up",
             "subject": "Great meeting you at {event}",
             "body": "Hi {name},\n\nIt was great chatting at {event}. I enjoyed our conversation about {topic}.\n\nWould love to continue the discussion over coffee/virtual meeting. Are you available next week?\n\nBest,\nAhmed"},
        ]

    def fill_template(self, template_id: str, variables: Dict) -> Dict:
        templates = {t["id"]: t for t in self.get_templates()}
        tmpl = templates.get(template_id)
        if not tmpl:
            return {"error": "Template not found"}
        
        subject = tmpl["subject"]
        body = tmpl["body"]
        for key, val in variables.items():
            subject = subject.replace(f"{{{key}}}", val)
            body = body.replace(f"{{{key}}}", val)
        
        return {"subject": subject, "body": body, "template_name": tmpl["name"]}
