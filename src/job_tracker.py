#!/usr/bin/env python3
"""
Job Tracker - Track job applications and opportunities
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid

@dataclass
class JobApplication:
    """A job application record"""
    id: str
    company: str
    title: str
    location: str
    salary_range: str
    source: str  # LinkedIn, Bayt, Referral, etc.
    date_applied: str
    status: str  # Applied, Phone Screen, Interview, Offer, Rejected, Ghosted
    cv_version: str  # Path to tailored CV used
    ats_score: int
    notes: str
    contacts: List[Dict]  # Recruiter, hiring manager info
    follow_up_dates: List[str]
    next_action: str
    priority: int  # 1-5, 5 being highest
    sector: str  # HealthTech, FinTech, etc.
    url: str
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'JobApplication':
        return cls(**data)


class JobTracker:
    """Track job applications pipeline"""
    
    def __init__(self, data_dir: str = "/root/.openclaw/workspace/tools/cv-optimizer/data"):
        self.data_dir = Path(data_dir)
        self.jobs_file = self.data_dir / "job_applications.json"
        self.jobs: List[JobApplication] = []
        self.load()
    
    def load(self):
        """Load jobs from disk"""
        if self.jobs_file.exists():
            with open(self.jobs_file, 'r') as f:
                data = json.load(f)
                self.jobs = [JobApplication.from_dict(j) for j in data]
    
    def save(self):
        """Save jobs to disk"""
        with open(self.jobs_file, 'w') as f:
            json.dump([j.to_dict() for j in self.jobs], f, indent=2)
    
    def add_job(self, 
                company: str,
                title: str,
                location: str = "",
                salary_range: str = "",
                source: str = "",
                cv_version: str = "",
                ats_score: int = 0,
                sector: str = "",
                url: str = "",
                priority: int = 3,
                notes: str = "") -> JobApplication:
        """Add a new job application"""
        
        job = JobApplication(
            id=str(uuid.uuid4())[:8],
            company=company,
            title=title,
            location=location,
            salary_range=salary_range,
            source=source,
            date_applied=datetime.now().isoformat(),
            status="Applied",
            cv_version=cv_version,
            ats_score=ats_score,
            notes=notes,
            contacts=[],
            follow_up_dates=[],
            next_action="Wait for response (7 days)",
            priority=priority,
            sector=sector,
            url=url
        )
        
        self.jobs.append(job)
        self.save()
        return job
    
    def update_status(self, job_id: str, new_status: str, notes: str = ""):
        """Update job status"""
        for job in self.jobs:
            if job.id == job_id:
                job.status = new_status
                if notes:
                    job.notes += f"\n[{datetime.now().strftime('%Y-%m-%d')}] {notes}"
                
                # Update next action based on status
                if new_status == "Applied":
                    job.next_action = "Follow up if no response in 7 days"
                    job.follow_up_dates.append((datetime.now() + timedelta(days=7)).isoformat())
                elif new_status == "Phone Screen":
                    job.next_action = "Prepare for technical interview"
                elif new_status == "Interview":
                    job.next_action = "Send thank you email, prepare for next round"
                elif new_status == "Offer":
                    job.next_action = "Evaluate offer, negotiate if needed"
                
                self.save()
                return job
        return None
    
    def add_contact(self, job_id: str, name: str, role: str, email: str = "", linkedin: str = ""):
        """Add a contact for a job"""
        for job in self.jobs:
            if job.id == job_id:
                job.contacts.append({
                    "name": name,
                    "role": role,
                    "email": email,
                    "linkedin": linkedin
                })
                self.save()
                return job
        return None
    
    def get_pipeline(self) -> Dict[str, List[JobApplication]]:
        """Get jobs grouped by status"""
        pipeline = {
            "Applied": [],
            "Phone Screen": [],
            "Interview": [],
            "Offer": [],
            "Rejected": [],
            "Ghosted": [],
            "Withdrawn": []
        }
        
        for job in self.jobs:
            if job.status in pipeline:
                pipeline[job.status].append(job)
            else:
                pipeline["Applied"].append(job)
        
        return pipeline
    
    def get_follow_ups(self, days: int = 7) -> List[JobApplication]:
        """Get jobs needing follow-up"""
        cutoff = datetime.now() + timedelta(days=days)
        follow_ups = []
        
        for job in self.jobs:
            if job.status in ["Applied", "Phone Screen"]:
                applied_date = datetime.fromisoformat(job.date_applied)
                days_since = (datetime.now() - applied_date).days
                
                if days_since >= 7 and job.status == "Applied":
                    follow_ups.append(job)
                elif days_since >= 14 and job.status == "Phone Screen":
                    follow_ups.append(job)
        
        return follow_ups
    
    def get_stats(self) -> Dict:
        """Get application statistics"""
        pipeline = self.get_pipeline()
        
        total = len(self.jobs)
        active = len([j for j in self.jobs if j.status not in ["Rejected", "Ghosted", "Withdrawn"]])
        offers = len(pipeline["Offer"])
        interviews = len(pipeline["Interview"])
        
        # By sector
        sectors = {}
        for job in self.jobs:
            sectors[job.sector] = sectors.get(job.sector, 0) + 1
        
        # By source
        sources = {}
        for job in self.jobs:
            sources[job.source] = sources.get(job.source, 0) + 1
        
        # Average ATS score
        avg_ats = sum(j.ats_score for j in self.jobs if j.ats_score > 0) / max(len([j for j in self.jobs if j.ats_score > 0]), 1)
        
        return {
            "total_applications": total,
            "active_applications": active,
            "offers": offers,
            "interviews": interviews,
            "conversion_rate": (interviews / max(total, 1)) * 100,
            "by_sector": sectors,
            "by_source": sources,
            "avg_ats_score": round(avg_ats, 1)
        }
    
    def search(self, query: str) -> List[JobApplication]:
        """Search jobs by company, title, or notes"""
        query = query.lower()
        results = []
        
        for job in self.jobs:
            if (query in job.company.lower() or 
                query in job.title.lower() or 
                query in job.notes.lower()):
                results.append(job)
        
        return results
    
    def get_high_priority(self) -> List[JobApplication]:
        """Get high priority jobs (4-5)"""
        return [j for j in self.jobs if j.priority >= 4 and j.status not in ["Rejected", "Ghosted", "Withdrawn"]]


def print_pipeline(tracker: JobTracker):
    """Print visual pipeline"""
    pipeline = tracker.get_pipeline()
    
    print("\n" + "=" * 80)
    print("JOB APPLICATION PIPELINE")
    print("=" * 80)
    
    for status, jobs in pipeline.items():
        if jobs:
            print(f"\n📌 {status.upper()} ({len(jobs)})")
            print("-" * 40)
            for job in sorted(jobs, key=lambda j: j.date_applied, reverse=True):
                priority_emoji = "🔴" if job.priority >= 4 else "🟡" if job.priority == 3 else "🟢"
                print(f"  {priority_emoji} [{job.id}] {job.title}")
                print(f"      {job.company} | {job.location}")
                print(f"      ATS: {job.ats_score}/100 | Applied: {job.date_applied[:10]}")
                if job.next_action:
                    print(f"      Next: {job.next_action}")
                print()


def print_stats(tracker: JobTracker):
    """Print statistics"""
    stats = tracker.get_stats()
    
    print("\n" + "=" * 80)
    print("APPLICATION STATISTICS")
    print("=" * 80)
    print(f"\n📊 Total Applications: {stats['total_applications']}")
    print(f"🎯 Active: {stats['active_applications']}")
    print(f"💼 Interviews: {stats['interviews']}")
    print(f"✅ Offers: {stats['offers']}")
    print(f"📈 Conversion Rate: {stats['conversion_rate']:.1f}%")
    print(f"⭐ Average ATS Score: {stats['avg_ats_score']}/100")
    
    if stats['by_sector']:
        print(f"\n🏭 By Sector:")
        for sector, count in sorted(stats['by_sector'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {sector}: {count}")
    
    if stats['by_source']:
        print(f"\n🔗 By Source:")
        for source, count in sorted(stats['by_source'].items(), key=lambda x: x[1], reverse=True):
            print(f"   {source}: {count}")


def print_follow_ups(tracker: JobTracker):
    """Print follow-up reminders"""
    follow_ups = tracker.get_follow_ups()
    
    if follow_ups:
        print("\n" + "=" * 80)
        print("⚠️  FOLLOW-UP REMINDERS")
        print("=" * 80)
        for job in follow_ups:
            applied_date = datetime.fromisoformat(job.date_applied)
            days_since = (datetime.now() - applied_date).days
            print(f"\n🔔 [{job.id}] {job.title} at {job.company}")
            print(f"   Applied: {days_since} days ago")
            print(f"   Status: {job.status}")
            print(f"   Suggested Action: Send follow-up email to recruiter")


def main():
    """CLI interface"""
    import sys
    
    tracker = JobTracker()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python job_tracker.py add 'Company' 'Title' [location] [source] [sector]")
        print("  python job_tracker.py status <id> <new_status> [notes]")
        print("  python job_tracker.py list")
        print("  python job_tracker.py stats")
        print("  python job_tracker.py followups")
        print("  python job_tracker.py search <query>")
        return
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 4:
            print("Usage: python job_tracker.py add 'Company' 'Title' [location] [source] [sector]")
            return
        
        company = sys.argv[2]
        title = sys.argv[3]
        location = sys.argv[4] if len(sys.argv) > 4 else ""
        source = sys.argv[5] if len(sys.argv) > 5 else ""
        sector = sys.argv[6] if len(sys.argv) > 6 else ""
        
        job = tracker.add_job(company, title, location, source=source, sector=sector)
        print(f"✅ Added job: [{job.id}] {title} at {company}")
    
    elif command == "status":
        if len(sys.argv) < 4:
            print("Usage: python job_tracker.py status <id> <new_status> [notes]")
            return
        
        job_id = sys.argv[2]
        new_status = sys.argv[3]
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        
        job = tracker.update_status(job_id, new_status, notes)
        if job:
            print(f"✅ Updated [{job.id}] to '{new_status}'")
        else:
            print(f"❌ Job not found: {job_id}")
    
    elif command == "list" or command == "pipeline":
        print_pipeline(tracker)
    
    elif command == "stats":
        print_stats(tracker)
    
    elif command == "followups":
        print_follow_ups(tracker)
        print_follow_ups(tracker)
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: python job_tracker.py search <query>")
            return
        
        query = sys.argv[2]
        results = tracker.search(query)
        print(f"\n🔍 Search results for '{query}':")
        for job in results:
            print(f"  [{job.id}] {job.title} at {job.company} ({job.status})")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
