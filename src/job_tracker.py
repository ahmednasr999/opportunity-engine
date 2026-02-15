#!/usr/bin/env python3
"""
Job Tracker - Track job applications and opportunities
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid

@dataclass
class InterviewChecklist:
    """Interview preparation checklist for a job"""
    id: str
    job_id: str
    pre_interview: List[Dict]  # Tasks before interview
    post_interview: List[Dict]  # Tasks after interview
    questions_to_ask: List[str]
    questions_to_answer: List[str]
    created_at: str
    updated_at: str

@dataclass
class SalaryNegotiation:
    """Salary negotiation tracking"""
    id: str
    job_id: str
    initial_offer: float
    base_salary: float
    bonus: float
    equity: str  # Stock options, RSUs
    benefits: str
    counter_offers: List[Dict]  # [{amount, date, notes}]
    final_offer: float
    status: str  # pending, negotiating, accepted, declined
    notes: str
    created_at: str
    updated_at: str

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
    interview_checklist_id: str = ""
    salary_negotiation_id: str = ""
    
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
    
    # ===== INTERVIEW CHECKLIST FEATURE =====
    def add_interview_checklist(self, job_id: str) -> Optional[InterviewChecklist]:
        """Add an interview checklist to a job"""
        checklist = InterviewChecklist(
            id=str(uuid.uuid4())[:8],
            job_id=job_id,
            pre_interview=[
                {"task": "Research company culture and recent news", "completed": False},
                {"task": "Review job description and requirements", "completed": False},
                {"task": "Prepare STAR stories for common questions", "completed": False},
                {"task": "Prepare questions to ask interviewer", "completed": False},
                {"task": "Test video call/phone connection", "completed": False},
                {"task": "Plan outfit - dress one level above company culture", "completed": False},
            ],
            post_interview=[
                {"task": "Send thank you email within 24 hours", "completed": False},
                {"task": "Note any questions you couldn't answer", "completed": False},
                {"task": "Follow up on any promised materials", "completed": False},
                {"task": "Update interview notes with key takeaways", "completed": False},
            ],
            questions_to_ask=[
                "What does success look like in this role after 90 days?",
                "How does the team handle cross-functional collaboration?",
                "What's the biggest challenge the team is facing?",
                "How do you support professional development?",
                "What's the team culture like?",
            ],
            questions_to_answer=[
                "Tell me about yourself",
                "Why do you want to work here?",
                "What's your greatest strength/weakness?",
                "Describe a challenging project",
                "Where do you see yourself in 5 years?",
            ],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # Add checklist ID to job
        for job in self.jobs:
            if job.id == job_id:
                job.interview_checklist_id = checklist.id
                self.save()
                break
        
        # Save checklist to file
        self._save_checklist(checklist)
        return checklist
    
    def get_checklist(self, checklist_id: str) -> Optional[InterviewChecklist]:
        """Get a checklist by ID"""
        checklist_file = self.data_dir / "interview_checklists.json"
        if checklist_file.exists():
            with open(checklist_file, 'r') as f:
                data = json.load(f)
                for c in data:
                    if c['id'] == checklist_id:
                        return InterviewChecklist(**c)
        return None
    
    def update_checklist_item(self, checklist_id: str, item_type: str, item_index: int, completed: bool):
        """Update a checklist item completion status"""
        checklist = self.get_checklist(checklist_id)
        if checklist:
            if item_type == "pre":
                checklist.pre_interview[item_index]["completed"] = completed
            elif item_type == "post":
                checklist.post_interview[item_index]["completed"] = completed
            
            checklist.updated_at = datetime.now().isoformat()
            self._save_checklist(checklist, update=True)
    
    def _save_checklist(self, checklist: InterviewChecklist, update: bool = False):
        """Save checklist to file"""
        checklist_file = self.data_dir / "interview_checklists.json"
        checklists = []
        
        if checklist_file.exists() and not update:
            with open(checklist_file, 'r') as f:
                checklists = json.load(f)
        
        if update:
            # Update existing
            if checklist_file.exists():
                with open(checklist_file, 'r') as f:
                    checklists = json.load(f)
                for i, c in enumerate(checklists):
                    if c['id'] == checklist.id:
                        checklists[i] = asdict(checklist)
                        break
        else:
            checklists.append(asdict(checklist))
        
        with open(checklist_file, 'w') as f:
            json.dump(checklists, f, indent=2)
    
    # ===== SALARY NEGOTIATION FEATURE =====
    def add_salary_negotiation(self, job_id: str, initial_offer: float = 0, 
                               base_salary: float = 0, bonus: float = 0,
                               equity: str = "", benefits: str = "") -> Optional[SalaryNegotiation]:
        """Add salary negotiation tracking to a job"""
        negotiation = SalaryNegotiation(
            id=str(uuid.uuid4())[:8],
            job_id=job_id,
            initial_offer=initial_offer,
            base_salary=base_salary,
            bonus=bonus,
            equity=equity,
            benefits=benefits,
            counter_offers=[],
            final_offer=0,
            status="pending",
            notes="",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        # Add negotiation ID to job
        for job in self.jobs:
            if job.id == job_id:
                job.salary_negotiation_id = negotiation.id
                self.save()
                break
        
        # Save negotiation to file
        self._save_negotiation(negotiation)
        return negotiation
    
    def get_negotiation(self, negotiation_id: str) -> Optional[SalaryNegotiation]:
        """Get a salary negotiation by ID"""
        neg_file = self.data_dir / "salary_negotiations.json"
        if neg_file.exists():
            with open(neg_file, 'r') as f:
                data = json.load(f)
                for n in data:
                    if n['id'] == negotiation_id:
                        return SalaryNegotiation(**n)
        return None
    
    def add_counter_offer(self, negotiation_id: str, amount: float, notes: str = ""):
        """Add a counter offer"""
        negotiation = self.get_negotiation(negotiation_id)
        if negotiation:
            negotiation.counter_offers.append({
                "amount": amount,
                "date": datetime.now().isoformat(),
                "notes": notes
            })
            negotiation.status = "negotiating"
            negotiation.updated_at = datetime.now().isoformat()
            self._save_negotiation(negotiation, update=True)
    
    def finalize_offer(self, negotiation_id: str, final_amount: float, accepted: bool = True):
        """Finalize the offer"""
        negotiation = self.get_negotiation(negotiation_id)
        if negotiation:
            negotiation.final_offer = final_amount
            negotiation.status = "accepted" if accepted else "declined"
            negotiation.updated_at = datetime.now().isoformat()
            self._save_negotiation(negotiation, update=True)
    
    def _save_negotiation(self, negotiation: SalaryNegotiation, update: bool = False):
        """Save negotiation to file"""
        neg_file = self.data_dir / "salary_negotiations.json"
        negotiations = []
        
        if neg_file.exists() and not update:
            with open(neg_file, 'r') as f:
                negotiations = json.load(f)
        
        if update:
            if neg_file.exists():
                with open(neg_file, 'r') as f:
                    negotiations = json.load(f)
                for i, n in enumerate(negotiations):
                    if n['id'] == negotiation.id:
                        negotiations[i] = asdict(negotiation)
                        break
        else:
            negotiations.append(asdict(negotiation))
        
        with open(neg_file, 'w') as f:
            json.dump(negotiations, f, indent=2)
    
    # ===== OFFER COMPARISON TOOL - PHASE 2 =====
    def compare_offers(self, negotiation_ids: List[str]) -> Dict:
        """Compare multiple job offers side-by-side"""
        offers = []
        for neg_id in negotiation_ids:
            negotiation = self.get_negotiation(neg_id)
            if negotiation:
                # Get job info
                job = next((j for j in self.jobs if j.salary_negotiation_id == neg_id), None)
                offers.append({
                    "negotiation": negotiation,
                    "job": job
                })
        
        if not offers:
            return {"error": "No valid offers found"}
        
        comparison = {
            "offers": [],
            "best_offer": None,
            "highest_salary": 0,
            "best_benefits": None
        }
        
        for offer in offers:
            neg = offer["negotiation"]
            job = offer["job"]
            
            total_value = neg.base_salary + neg.bonus
            # Add equity value estimate (simplified)
            if neg.equity:
                total_value += 20000  # Assume $20k for equity
            
            offer_data = {
                "company": job.company if job else "Unknown",
                "title": job.title if job else "Unknown",
                "base_salary": neg.base_salary,
                "bonus": neg.bonus,
                "equity": neg.equity,
                "benefits": neg.benefits,
                "total_value": total_value,
                "status": neg.status
            }
            comparison["offers"].append(offer_data)
            
            if total_value > comparison["highest_salary"]:
                comparison["highest_salary"] = total_value
                comparison["best_offer"] = offer_data
        
        return comparison
    
    # ===== SOURCE EFFECTIVENESS - PHASE 2 =====
    def get_source_effectiveness(self) -> Dict:
        """Calculate effectiveness by job source"""
        source_stats = {}
        
        for job in self.jobs:
            source = job.source or "Unknown"
            
            if source not in source_stats:
                source_stats[source] = {
                    "total": 0,
                    "phone_screens": 0,
                    "interviews": 0,
                    "offers": 0,
                    "rejected": 0,
                    "ghosted": 0
                }
            
            source_stats[source]["total"] += 1
            
            if job.status == "Phone Screen":
                source_stats[source]["phone_screens"] += 1
            elif job.status == "Interview":
                source_stats[source]["interviews"] += 1
            elif job.status == "Offer":
                source_stats[source]["offers"] += 1
            elif job.status == "Rejected":
                source_stats[source]["rejected"] += 1
            elif job.status == "Ghosted":
                source_stats[source]["ghosted"] += 1
        
        # Calculate rates
        for source, stats in source_stats.items():
            total = stats["total"]
            if total > 0:
                stats["screen_rate"] = round(stats["phone_screens"] / total * 100, 1)
                stats["interview_rate"] = round(stats["interviews"] / total * 100, 1)
                stats["offer_rate"] = round(stats["offers"] / total * 100, 1)
                stats["response_rate"] = round((stats["phone_screens"] + stats["interviews"]) / total * 100, 1)
        
        return source_stats


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
