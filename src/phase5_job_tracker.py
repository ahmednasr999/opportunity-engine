#!/usr/bin/env python3
"""
Phase 5 - Job Tracker Enhancements
Features: Application Timeline, Company Research, Interview Prep, Follow-up Scheduler,
          Application Templates, Referral Tracker, Rejection Analysis,
          Gantt View, Source Effectiveness, Response Time, Ghost Job Detector, Offer Comparison
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path


class ApplicationTimeline:
    """Visual timeline of each job application"""

    STAGES = ["discovered", "applied", "screening", "interview_1", "interview_2", "technical", "offer", "accepted", "rejected"]

    def get_timeline(self, application: Dict) -> Dict:
        events = application.get("events", [])
        if not events:
            events = self._generate_sample(application)

        return {
            "application_id": application.get("id", ""),
            "company": application.get("company", ""),
            "role": application.get("role", ""),
            "events": events,
            "current_stage": events[-1]["stage"] if events else "discovered",
            "days_in_pipeline": self._calc_days(events),
            "stages": self.STAGES,
        }

    def _generate_sample(self, app: Dict) -> List[Dict]:
        base = datetime.now() - timedelta(days=random.randint(10, 60))
        events = []
        for i, stage in enumerate(["discovered", "applied", "screening"]):
            events.append({
                "stage": stage,
                "date": (base + timedelta(days=i * 3)).strftime("%Y-%m-%d"),
                "notes": f"Auto-tracked: {stage.replace('_', ' ').title()}"
            })
        return events

    def _calc_days(self, events: List[Dict]) -> int:
        if len(events) < 2:
            return 0
        try:
            first = datetime.strptime(events[0]["date"], "%Y-%m-%d")
            last = datetime.strptime(events[-1]["date"], "%Y-%m-%d")
            return (last - first).days
        except:
            return 0

    def add_event(self, application: Dict, stage: str, notes: str = "") -> Dict:
        events = application.get("events", [])
        events.append({
            "stage": stage,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "notes": notes
        })
        application["events"] = events
        return application


class CompanyResearchPanel:
    """Auto-gather company information"""

    MOCK_COMPANIES = {
        "default": {
            "founded": "2010",
            "employees": "500-1000",
            "industry": "Technology",
            "hq": "Dubai, UAE",
            "revenue": "$50M-100M",
            "glassdoor_rating": 3.8,
            "growth": "Growing",
            "recent_news": ["Series C funding announced", "Expanded to 3 new markets"],
            "culture_keywords": ["innovative", "fast-paced", "collaborative"],
            "tech_stack": ["Python", "AWS", "React"],
            "interview_process": "3-4 rounds typical",
            "benefits": ["Health insurance", "Remote work", "Learning budget"]
        }
    }

    def research(self, company_name: str) -> Dict:
        base = self.MOCK_COMPANIES["default"].copy()
        base["company_name"] = company_name
        base["research_date"] = datetime.now().isoformat()
        base["linkedin_url"] = f"https://linkedin.com/company/{company_name.lower().replace(' ', '-')}"
        base["website"] = f"https://www.{company_name.lower().replace(' ', '')}.com"
        
        # Customize based on company name keywords
        name_lower = company_name.lower()
        if "health" in name_lower or "hospital" in name_lower:
            base["industry"] = "Healthcare"
            base["culture_keywords"] = ["patient-centered", "innovative", "quality-driven"]
        elif "tech" in name_lower or "ai" in name_lower:
            base["industry"] = "Technology"
            base["tech_stack"] = ["Python", "TensorFlow", "AWS", "Kubernetes"]
        elif "bank" in name_lower or "finance" in name_lower:
            base["industry"] = "Financial Services"
            base["culture_keywords"] = ["analytical", "performance-driven", "regulated"]

        base["insights"] = [
            f"{company_name} appears to be a {base['growth'].lower()} company in {base['industry']}",
            f"Typical interview process: {base['interview_process']}",
            f"Glassdoor rating: {base['glassdoor_rating']}/5"
        ]
        return base


class InterviewPrepGenerator:
    """Generate custom interview preparation for each role"""

    def generate(self, role: str, company: str, job_description: str = "") -> Dict:
        questions = {
            "behavioral": [
                f"Tell me about a time you led a team through a major challenge at scale.",
                f"Describe a situation where you had to influence stakeholders without direct authority.",
                f"How have you handled a failed project or initiative?",
                f"Give an example of how you drove innovation in a previous role.",
                f"Tell me about a time you had to make a difficult decision with incomplete data.",
            ],
            "technical": [
                f"How would you approach building a {role.split()[0].lower()} strategy for {company}?",
                f"What KPIs would you track in this role?",
                f"Describe your experience with relevant technologies for this position.",
                f"How would you evaluate and improve current processes?",
                f"Walk me through a technical architecture you've designed.",
            ],
            "situational": [
                f"If hired as {role}, what would your first 90 days look like?",
                f"How would you handle a team member who consistently underperforms?",
                f"The CEO asks you to cut costs by 20%. How do you approach this?",
                f"A critical system goes down. Walk me through your response.",
                f"You disagree with your manager's strategy. What do you do?",
            ]
        }

        star_frameworks = [
            {
                "question": questions["behavioral"][0],
                "situation": "At [Company], we faced [challenge]...",
                "task": "I was responsible for...",
                "action": "I implemented a [approach] by...",
                "result": "This resulted in [metric] improvement..."
            }
        ]

        return {
            "role": role,
            "company": company,
            "questions": questions,
            "star_frameworks": star_frameworks,
            "research_points": [
                f"Review {company}'s recent news and press releases",
                f"Understand {company}'s market position and competitors",
                f"Prepare questions about team structure and growth plans",
                f"Know the interviewer's background (check LinkedIn)",
            ],
            "tips": [
                "Use STAR method for behavioral questions",
                "Prepare 3-5 questions to ask the interviewer",
                "Have salary expectations researched and ready",
                "Practice your elevator pitch (60 seconds)",
                "Prepare a 90-day plan outline"
            ],
            "salary_range": self._estimate_salary(role),
            "generated_at": datetime.now().isoformat()
        }

    def _estimate_salary(self, role: str) -> Dict:
        role_lower = role.lower()
        if "vp" in role_lower or "director" in role_lower:
            return {"min": 150000, "max": 250000, "currency": "USD"}
        elif "manager" in role_lower or "lead" in role_lower:
            return {"min": 100000, "max": 180000, "currency": "USD"}
        return {"min": 80000, "max": 140000, "currency": "USD"}


class FollowUpScheduler:
    """Auto-schedule follow-up reminders"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.schedule_file = self.data_dir / "followups.json"
        self.followups = self._load()

    def _load(self) -> List[Dict]:
        if self.schedule_file.exists():
            return json.loads(self.schedule_file.read_text())
        return []

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.schedule_file.write_text(json.dumps(self.followups, indent=2))

    def schedule(self, company: str, role: str, contact: str = "", days_delay: int = 7) -> Dict:
        followup = {
            "id": f"fu{len(self.followups)+1}",
            "company": company,
            "role": role,
            "contact": contact,
            "scheduled_date": (datetime.now() + timedelta(days=days_delay)).strftime("%Y-%m-%d"),
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "template": self._get_template(company, role),
        }
        self.followups.append(followup)
        self._save()
        return followup

    def get_pending(self) -> List[Dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        return [f for f in self.followups if f["status"] == "pending" and f["scheduled_date"] <= today]

    def get_upcoming(self) -> List[Dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        return [f for f in self.followups if f["status"] == "pending" and f["scheduled_date"] > today]

    def complete(self, followup_id: str) -> bool:
        for f in self.followups:
            if f["id"] == followup_id:
                f["status"] = "completed"
                f["completed_at"] = datetime.now().isoformat()
                self._save()
                return True
        return False

    def _get_template(self, company: str, role: str) -> str:
        return f"""Hi [Contact Name],

I hope this message finds you well. I wanted to follow up on my application for the {role} position at {company}.

I remain very enthusiastic about the opportunity and would welcome the chance to discuss how my experience in healthcare operations and AI can contribute to your team's goals.

Please let me know if there's any additional information I can provide.

Best regards,
Ahmed Nasr"""

    def get_all(self) -> List[Dict]:
        return self.followups


class ApplicationTemplates:
    """Save and manage application text templates"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.templates_file = self.data_dir / "app_templates.json"
        self.templates = self._load()

    def _load(self) -> List[Dict]:
        if self.templates_file.exists():
            return json.loads(self.templates_file.read_text())
        return [
            {
                "id": "t1", "name": "Healthcare Executive", "category": "cover_letter",
                "content": "Dear Hiring Manager,\n\nWith over 15 years in healthcare operations and a passion for leveraging AI to improve patient outcomes, I am excited to apply for [ROLE] at [COMPANY].\n\nMy experience leading cross-functional teams and implementing technology solutions has consistently delivered measurable improvements in operational efficiency and quality of care.\n\nI would welcome the opportunity to discuss how I can contribute to your organization's goals.\n\nBest regards,\nAhmed Nasr",
                "variables": ["ROLE", "COMPANY"],
                "usage_count": 5
            },
            {
                "id": "t2", "name": "Quick Follow-up", "category": "follow_up",
                "content": "Hi [NAME],\n\nI wanted to follow up on my application for [ROLE]. I remain very interested in the position and would love to discuss how my background aligns with your needs.\n\nBest,\nAhmed",
                "variables": ["NAME", "ROLE"],
                "usage_count": 3
            },
            {
                "id": "t3", "name": "Networking Intro", "category": "networking",
                "content": "Hi [NAME],\n\nI came across your profile and was impressed by your work at [COMPANY]. I'm currently exploring opportunities in [FIELD] and would love to connect and learn from your experience.\n\nWould you be open to a brief chat?\n\nBest regards,\nAhmed Nasr",
                "variables": ["NAME", "COMPANY", "FIELD"],
                "usage_count": 8
            }
        ]

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.templates_file.write_text(json.dumps(self.templates, indent=2))

    def get_all(self) -> List[Dict]:
        return self.templates

    def add(self, template_data: Dict) -> Dict:
        template = {
            "id": f"t{len(self.templates)+1}",
            "name": template_data.get("name", "Untitled"),
            "category": template_data.get("category", "general"),
            "content": template_data.get("content", ""),
            "variables": template_data.get("variables", []),
            "usage_count": 0,
            "created_at": datetime.now().isoformat()
        }
        self.templates.append(template)
        self._save()
        return template

    def use_template(self, template_id: str, variables: Dict) -> Dict:
        for t in self.templates:
            if t["id"] == template_id:
                content = t["content"]
                for var, val in variables.items():
                    content = content.replace(f"[{var}]", val)
                t["usage_count"] = t.get("usage_count", 0) + 1
                self._save()
                return {"content": content, "template": t["name"]}
        return {"error": "Template not found"}

    def delete(self, template_id: str) -> bool:
        self.templates = [t for t in self.templates if t["id"] != template_id]
        self._save()
        return True


class ReferralTracker:
    """Track who referred you where"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.referrals_file = self.data_dir / "referrals.json"
        self.referrals = self._load()

    def _load(self) -> List[Dict]:
        if self.referrals_file.exists():
            return json.loads(self.referrals_file.read_text())
        return [
            {"id": "r1", "referrer": "Sarah Al-Rashid", "company": "MENA HealthTech",
             "role": "VP Operations", "date": "2026-01-20", "status": "interview",
             "outcome": "Progressing", "notes": "Strong internal referral"},
            {"id": "r2", "referrer": "James Wilson", "company": "TechCorp Health",
             "role": "Director of AI", "date": "2026-02-01", "status": "applied",
             "outcome": "Pending", "notes": "Met at conference"}
        ]

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.referrals_file.write_text(json.dumps(self.referrals, indent=2))

    def add(self, referral_data: Dict) -> Dict:
        ref = {
            "id": f"r{len(self.referrals)+1}",
            "referrer": referral_data.get("referrer", ""),
            "company": referral_data.get("company", ""),
            "role": referral_data.get("role", ""),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "pending",
            "outcome": "Pending",
            "notes": referral_data.get("notes", ""),
        }
        self.referrals.append(ref)
        self._save()
        return ref

    def get_all(self) -> List[Dict]:
        return self.referrals

    def get_stats(self) -> Dict:
        total = len(self.referrals)
        by_status = {}
        for r in self.referrals:
            s = r.get("status", "unknown")
            by_status[s] = by_status.get(s, 0) + 1
        top_referrers = {}
        for r in self.referrals:
            name = r.get("referrer", "Unknown")
            top_referrers[name] = top_referrers.get(name, 0) + 1
        
        return {
            "total_referrals": total,
            "by_status": by_status,
            "top_referrers": sorted(top_referrers.items(), key=lambda x: x[1], reverse=True)[:5],
            "success_rate": round(by_status.get("interview", 0) / max(1, total) * 100, 1)
        }

    def update_status(self, ref_id: str, status: str, outcome: str = "") -> bool:
        for r in self.referrals:
            if r["id"] == ref_id:
                r["status"] = status
                if outcome:
                    r["outcome"] = outcome
                self._save()
                return True
        return False


class RejectionAnalysis:
    """Track and analyze patterns in rejections"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.rejections_file = self.data_dir / "rejections.json"
        self.rejections = self._load()

    def _load(self) -> List[Dict]:
        if self.rejections_file.exists():
            return json.loads(self.rejections_file.read_text())
        return [
            {"id": "rej1", "company": "BigCorp Health", "role": "VP Ops", "stage": "interview_2",
             "date": "2026-01-10", "reason": "Overqualified", "feedback": "Great candidate but salary expectations too high"},
            {"id": "rej2", "company": "StartupX", "role": "COO", "stage": "screening",
             "date": "2026-01-25", "reason": "Experience mismatch", "feedback": "Looking for startup experience"},
            {"id": "rej3", "company": "GovHealth", "role": "Director", "stage": "applied",
             "date": "2026-02-05", "reason": "No response", "feedback": "Ghost - no reply after 30 days"},
        ]

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.rejections_file.write_text(json.dumps(self.rejections, indent=2))

    def add(self, rejection_data: Dict) -> Dict:
        rej = {
            "id": f"rej{len(self.rejections)+1}",
            "company": rejection_data.get("company", ""),
            "role": rejection_data.get("role", ""),
            "stage": rejection_data.get("stage", "applied"),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "reason": rejection_data.get("reason", "Unknown"),
            "feedback": rejection_data.get("feedback", ""),
        }
        self.rejections.append(rej)
        self._save()
        return rej

    def analyze(self) -> Dict:
        if not self.rejections:
            return {"patterns": [], "total": 0}
        
        by_stage = {}
        by_reason = {}
        for r in self.rejections:
            stage = r.get("stage", "unknown")
            reason = r.get("reason", "unknown")
            by_stage[stage] = by_stage.get(stage, 0) + 1
            by_reason[reason] = by_reason.get(reason, 0) + 1
        
        # Find the most common rejection stage
        worst_stage = max(by_stage.items(), key=lambda x: x[1])[0] if by_stage else "unknown"
        top_reason = max(by_reason.items(), key=lambda x: x[1])[0] if by_reason else "unknown"
        
        patterns = []
        if by_stage.get("applied", 0) > len(self.rejections) * 0.4:
            patterns.append("Most rejections at application stage — consider improving CV targeting")
        if by_stage.get("screening", 0) > len(self.rejections) * 0.3:
            patterns.append("Many rejections at screening — practice phone interview skills")
        if by_reason.get("No response", 0) > len(self.rejections) * 0.3:
            patterns.append("High ghost rate — follow up more consistently")
        if by_reason.get("Overqualified", 0) > 0:
            patterns.append("Some 'overqualified' rejections — consider targeting more senior roles")

        return {
            "total_rejections": len(self.rejections),
            "by_stage": by_stage,
            "by_reason": by_reason,
            "worst_stage": worst_stage,
            "top_reason": top_reason,
            "patterns": patterns,
            "recommendations": [
                "Tailor each application to the specific role",
                "Follow up within 1 week of applying",
                "Request feedback after rejections",
                "Track and learn from every rejection"
            ],
            "chart_data": {
                "stages": list(by_stage.keys()),
                "counts": list(by_stage.values()),
                "reasons": list(by_reason.keys()),
                "reason_counts": list(by_reason.values())
            }
        }

    def get_all(self) -> List[Dict]:
        return self.rejections


class GanttTimelineView:
    """Gantt-style timeline view for all applications"""

    def generate(self, applications: List[Dict]) -> Dict:
        gantt_items = []
        for app in applications:
            start = app.get("applied_date", datetime.now().strftime("%Y-%m-%d"))
            status = app.get("status", "applied")
            
            duration_map = {"applied": 7, "screening": 14, "interview": 21, "offer": 28, "rejected": 10}
            duration = duration_map.get(status, 7)
            
            try:
                start_date = datetime.strptime(start, "%Y-%m-%d")
                end_date = start_date + timedelta(days=duration)
            except:
                start_date = datetime.now()
                end_date = start_date + timedelta(days=7)
            
            gantt_items.append({
                "id": app.get("id", ""),
                "company": app.get("company", "Unknown"),
                "role": app.get("role", "Unknown"),
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "status": status,
                "color": {"applied": "#4299e1", "screening": "#ed8936", "interview": "#48bb78",
                          "offer": "#38b2ac", "rejected": "#e53e3e", "accepted": "#805ad5"}.get(status, "#a0aec0"),
                "progress": {"applied": 20, "screening": 40, "interview": 60, "offer": 80,
                             "rejected": 100, "accepted": 100}.get(status, 10)
            })

        return {
            "items": gantt_items,
            "total_applications": len(gantt_items),
            "date_range": {
                "start": min(i["start"] for i in gantt_items) if gantt_items else None,
                "end": max(i["end"] for i in gantt_items) if gantt_items else None,
            }
        }


class SourceEffectiveness:
    """Track which job sources are most effective"""

    def analyze(self, applications: List[Dict]) -> Dict:
        sources = {}
        for app in applications:
            source = app.get("source", "Direct")
            if source not in sources:
                sources[source] = {"total": 0, "interviews": 0, "offers": 0, "rejections": 0}
            sources[source]["total"] += 1
            status = app.get("status", "")
            if status in ["interview", "interview_2", "technical"]:
                sources[source]["interviews"] += 1
            elif status == "offer":
                sources[source]["offers"] += 1
            elif status == "rejected":
                sources[source]["rejections"] += 1

        effectiveness = []
        for source, stats in sources.items():
            rate = round(stats["interviews"] / max(1, stats["total"]) * 100, 1)
            effectiveness.append({
                "source": source,
                "applications": stats["total"],
                "interviews": stats["interviews"],
                "offers": stats["offers"],
                "interview_rate": rate,
                "score": rate
            })
        
        effectiveness.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "sources": effectiveness,
            "best_source": effectiveness[0]["source"] if effectiveness else "N/A",
            "recommendation": f"Focus more on {effectiveness[0]['source']}" if effectiveness else "Apply to more sources"
        }


class ResponseTimeTracker:
    """Track how fast companies respond"""

    def analyze(self, applications: List[Dict]) -> Dict:
        response_times = []
        for app in applications:
            applied = app.get("applied_date")
            first_response = app.get("first_response_date")
            if applied and first_response:
                try:
                    d1 = datetime.strptime(applied, "%Y-%m-%d")
                    d2 = datetime.strptime(first_response, "%Y-%m-%d")
                    days = (d2 - d1).days
                    response_times.append({
                        "company": app.get("company", ""),
                        "days": days,
                        "status": app.get("status", "")
                    })
                except:
                    pass

        if not response_times:
            # Generate sample data
            response_times = [
                {"company": "Company A", "days": 3, "status": "interview"},
                {"company": "Company B", "days": 14, "status": "rejected"},
                {"company": "Company C", "days": 7, "status": "screening"},
            ]

        avg_days = round(sum(r["days"] for r in response_times) / max(1, len(response_times)), 1)
        fastest = min(response_times, key=lambda x: x["days"]) if response_times else None
        slowest = max(response_times, key=lambda x: x["days"]) if response_times else None

        return {
            "response_times": response_times,
            "average_days": avg_days,
            "fastest": fastest,
            "slowest": slowest,
            "industry_average": 10,
            "recommendation": "Average response time is good" if avg_days <= 10 else "Response times are slow — consider following up sooner"
        }


class GhostJobDetector:
    """Detect potentially ghost/fake job postings"""

    def detect(self, job_data: Dict) -> Dict:
        ghost_score = 0
        flags = []
        
        # Check for red flags
        if job_data.get("posted_days_ago", 0) > 60:
            ghost_score += 25
            flags.append("Job posted over 60 days ago")
        
        if not job_data.get("salary_range"):
            ghost_score += 10
            flags.append("No salary range listed")
        
        if job_data.get("reposted", False):
            ghost_score += 20
            flags.append("Job has been reposted multiple times")
        
        desc = job_data.get("description", "").lower()
        if "rockstar" in desc or "ninja" in desc or "guru" in desc:
            ghost_score += 15
            flags.append("Uses buzzwords (rockstar/ninja/guru)")
        
        if len(desc) < 100:
            ghost_score += 15
            flags.append("Very short job description")
        
        if job_data.get("company_reviews", 0) < 5:
            ghost_score += 10
            flags.append("Very few company reviews")

        verdict = "Likely Real" if ghost_score < 30 else "Suspicious" if ghost_score < 60 else "Likely Ghost Job"
        
        return {
            "ghost_score": min(100, ghost_score),
            "verdict": verdict,
            "flags": flags,
            "recommendation": "Proceed with caution" if ghost_score >= 30 else "Looks legitimate — apply with confidence",
            "tips": [
                "Check if the company is actively hiring on LinkedIn",
                "Look for the recruiter's profile",
                "Check Glassdoor for recent interview reviews",
                "Contact someone at the company to verify"
            ]
        }


class OfferComparisonTool:
    """Compare multiple job offers"""

    def compare(self, offers: List[Dict]) -> Dict:
        if not offers:
            offers = [
                {"company": "Company A", "salary": 180000, "bonus": 20000, "equity": 50000,
                 "remote": True, "pto_days": 25, "health_insurance": True, "learning_budget": 5000,
                 "commute_minutes": 0, "growth_potential": 8},
                {"company": "Company B", "salary": 200000, "bonus": 30000, "equity": 0,
                 "remote": False, "pto_days": 20, "health_insurance": True, "learning_budget": 2000,
                 "commute_minutes": 45, "growth_potential": 7},
            ]

        scored = []
        for offer in offers:
            total_comp = offer.get("salary", 0) + offer.get("bonus", 0) + offer.get("equity", 0) / 4
            score = 0
            score += min(40, total_comp / 5000)  # Compensation (max 40)
            score += 10 if offer.get("remote") else 0
            score += min(15, offer.get("pto_days", 0) / 2)
            score += 10 if offer.get("health_insurance") else 0
            score += min(10, offer.get("learning_budget", 0) / 500)
            score += min(15, offer.get("growth_potential", 0) * 1.5)
            
            scored.append({
                **offer,
                "total_compensation": round(total_comp),
                "score": round(score, 1)
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        
        return {
            "offers": scored,
            "best_overall": scored[0]["company"] if scored else None,
            "best_compensation": max(scored, key=lambda x: x["total_compensation"])["company"] if scored else None,
            "comparison_factors": ["salary", "bonus", "equity", "remote", "pto_days", "health_insurance", "growth_potential"]
        }


class CompetitorJobAlerts:
    """Track and alert on competitor job postings"""

    def get_alerts(self, tracked_companies: List[str] = None) -> Dict:
        companies = tracked_companies or ["Saudi German Hospital", "Cleveland Clinic Abu Dhabi", 
                                          "SEHA", "Mediclinic", "NMC Healthcare"]
        alerts = []
        for company in companies:
            alerts.append({
                "company": company,
                "new_roles": random.randint(0, 5),
                "relevant_roles": [
                    {"title": f"Director of Operations", "posted": "2 days ago", "location": "Dubai"},
                    {"title": f"VP Digital Health", "posted": "1 week ago", "location": "Riyadh"},
                ][:random.randint(0, 2)],
                "last_checked": datetime.now().isoformat()
            })
        
        return {
            "alerts": alerts,
            "total_new_roles": sum(a["new_roles"] for a in alerts),
            "tracked_companies": len(companies)
        }


class ApplicationVelocity:
    """Track application speed and momentum"""

    def calculate(self, applications: List[Dict]) -> Dict:
        # Group by week
        weekly = {}
        for app in applications:
            date_str = app.get("applied_date", "")
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    week = date.strftime("%Y-W%W")
                    weekly[week] = weekly.get(week, 0) + 1
                except:
                    pass

        if not weekly:
            weekly = {"2026-W04": 3, "2026-W05": 5, "2026-W06": 4, "2026-W07": 6}

        weeks = sorted(weekly.keys())
        counts = [weekly[w] for w in weeks]
        avg = round(sum(counts) / max(1, len(counts)), 1)
        
        trend = "accelerating" if len(counts) > 1 and counts[-1] > avg else "decelerating" if len(counts) > 1 and counts[-1] < avg else "steady"

        return {
            "weekly_data": {"weeks": weeks, "counts": counts},
            "average_per_week": avg,
            "current_week": counts[-1] if counts else 0,
            "trend": trend,
            "total_applications": sum(counts),
            "recommendation": "Great momentum!" if trend == "accelerating" else "Consider increasing application volume" if trend == "decelerating" else "Steady pace — keep it up"
        }


class JobDescriptionDiff:
    """Compare differences between job descriptions"""

    def diff(self, jd1: str, jd2: str) -> Dict:
        words1 = set(jd1.lower().split())
        words2 = set(jd2.lower().split())
        
        common = words1 & words2
        only_jd1 = words1 - words2
        only_jd2 = words2 - words1
        
        # Filter stopwords
        stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were"}
        only_jd1 = only_jd1 - stopwords
        only_jd2 = only_jd2 - stopwords
        
        similarity = round(len(common) / max(1, len(words1 | words2)) * 100, 1)
        
        return {
            "similarity_percent": similarity,
            "common_keywords": list(common - stopwords)[:20],
            "unique_to_jd1": list(only_jd1)[:15],
            "unique_to_jd2": list(only_jd2)[:15],
            "recommendation": "Very similar roles" if similarity > 70 else "Moderately similar" if similarity > 40 else "Very different roles — tailor CV separately"
        }
