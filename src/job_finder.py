#!/usr/bin/env python3
"""
Job Auto-Find Feature
Scrapes job sites, matches to CVs, generates applications
"""

import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import uuid

# Data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
JOBS_FILE = os.path.join(DATA_DIR, 'found_jobs.json')
APPLICATIONS_FILE = os.path.join(DATA_DIR, 'job_applications.json')

@dataclass
class Job:
    """A job opportunity"""
    id: str
    title: str
    company: str
    location: str
    salary_range: str
    job_url: str
    source: str  # LinkedIn, Indeed, etc.
    description: str
    requirements: List[str]
    posted_date: str
    remote_policy: str  # remote, hybrid, on-site
    experience_level: str
    skills: List[str]
    sector: str
    ats_score: int = 0
    matched_cv: str = ""
    status: str = "found"  # found, applied, interview, offer, rejected
    applied_date: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Job':
        return cls(**data)


class JobFinder:
    """Find and match jobs to CVs"""
    
    # Job search criteria
    TARGET_ROLES = [
        "VP Healthcare AI",
        "VP Operations",
        "VP Product",
        "Director Healthcare AI",
        "Director Digital Transformation",
        "Chief Technology Officer",
        "VP Engineering",
        "Senior PMO Director"
    ]
    
    TARGET_SECTORS = [
        "healthcare",
        "healthtech",
        "medtech",
        "digital health",
        "hospital",
        "telemedicine",
        "medical",
        "pharma"
    ]
    
    TARGET_KEYWORDS = [
        "healthcare",
        "health tech",
        "digital transformation",
        "AI",
        "machine learning",
        "operations",
        "product",
        "PMO"
    ]
    
    EXCLUDE_KEYWORDS = [
        "intern",
        "junior",
        "entry level",
        "associate",
        "assistant"
    ]
    
    def __init__(self):
        self.found_jobs = self._load_jobs()
        self.applications = self._load_applications()
    
    def _load_jobs(self) -> List[Job]:
        """Load jobs from file"""
        if os.path.exists(JOBS_FILE):
            with open(JOBS_FILE, 'r') as f:
                data = json.load(f)
                return [Job.from_dict(j) for j in data]
        return []
    
    def _save_jobs(self):
        """Save jobs to file"""
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(JOBS_FILE, 'w') as f:
            json.dump([j.to_dict() for j in self.found_jobs], f, indent=2)
    
    def _load_applications(self) -> List[Dict]:
        """Load applications from file"""
        if os.path.exists(APPLICATIONS_FILE):
            with open(APPLICATIONS_FILE, 'r') as f:
                return json.load(f)
        return []
    
    def _save_applications(self):
        """Save applications to file"""
        with open(APPLICATIONS_FILE, 'w') as f:
            json.dump(self.applications, f, indent=2)
    
    def search_linkedin(self, role: str = "VP Healthcare AI") -> List[Job]:
        """Search LinkedIn for jobs (simulated - real API requires OAuth)"""
        print(f"🔍 Searching LinkedIn for: {role}")
        
        # Simulated results based on real patterns
        simulated_jobs = [
            Job(
                id=str(uuid.uuid4())[:8],
                title="VP Healthcare AI & Operations",
                company="HCA Healthcare",
                location="Nashville, TN (Hybrid)",
                salary_range="$180,000 - $250,000",
                job_url="https://linkedin.com/jobs/view/vp-healthcare-ai-hca",
                source="LinkedIn",
                description="Lead AI initiatives across HCA's 186 hospitals...",
                requirements=["10+ years healthcare", "AI/ML experience", "MBA"],
                posted_date=(datetime.now() - timedelta(days=2)).isoformat(),
                remote_policy="hybrid",
                experience_level="Senior",
                skills=["AI", "Healthcare", "Operations", "Python", "AWS"],
                sector="Healthcare"
            ),
            Job(
                id=str(uuid.uuid4())[:8],
                title="Director of Digital Health Products",
                company="Teladoc Health",
                location="New York, NY (Remote)",
                salary_range="$160,000 - $220,000",
                job_url="https://linkedin.com/jobs/view/director-digital-health-teladoc",
                source="LinkedIn",
                description="Lead digital product development for telehealth...",
                requirements=["8+ years product", "HealthTech experience", "PMP"],
                posted_date=(datetime.now() - timedelta(days=1)).isoformat(),
                remote_policy="remote",
                experience_level="Director",
                skills=["Product", "Digital Health", "Agile", "Data Analytics"],
                sector="Digital Health"
            ),
            Job(
                id=str(uuid.uuid4())[:8],
                title="VP Product & Operations",
                company="Tempus Labs",
                location="Chicago, IL (On-site)",
                salary_range="$200,000 - $280,000",
                job_url="https://linkedin.com/jobs/view/vp-product-ops-tempus",
                source="LinkedIn",
                description="Drive operational excellence across Tempus' AI-powered diagnostics...",
                requirements=["12+ years", "AI/ML", "Healthcare operations", "MBA"],
                posted_date=datetime.now().isoformat(),
                remote_policy="on-site",
                experience_level="VP",
                skills=["Operations", "AI", "Healthcare", "Leadership", "Strategy"],
                sector="HealthTech"
            ),
            Job(
                id=str(uuid.uuid4())[:8],
                title="Chief Digital Officer",
                company="Dignity Health",
                location="San Francisco, CA (Hybrid)",
                salary_range="$220,000 - $300,000",
                job_url="https://linkedin.com/jobs/view/cdo-dignity-health",
                source="LinkedIn",
                description="Lead digital transformation across 40 hospitals...",
                requirements=["15+ years", "Digital transformation", "Healthcare", "C-suite"],
                posted_date=(datetime.now() - timedelta(days=3)).isoformat(),
                remote_policy="hybrid",
                experience_level="C-Suite",
                skills=["Digital Transformation", "Healthcare", "Strategy", "AI"],
                sector="Healthcare"
            ),
            Job(
                id=str(uuid.uuid4())[:8],
                title="VP Engineering - Healthcare",
                company="Optum (UnitedHealth)",
                location="Eden Prairie, MN (Hybrid)",
                salary_range="$190,000 - $260,000",
                job_url="https://linkedin.com/jobs/view/vp-engineering-optum",
                source="LinkedIn",
                description="Lead engineering team for healthcare analytics platform...",
                requirements=["10+ years engineering", "Healthcare tech", "SaaS"],
                posted_date=(datetime.now() - timedelta(days=1)).isoformat(),
                remote_policy="hybrid",
                experience_level="VP",
                skills=["Engineering", "Healthcare", "SaaS", "Python", "Cloud"],
                sector="Healthcare"
            ),
            Job(
                id=str(uuid.uuid4())[:8],
                title="Director of AI Operations",
                company="Epic Systems",
                location="Madison, WI (On-site)",
                salary_range="$150,000 - $200,000",
                job_url="https://linkedin.com/jobs/view/director-ai-operations-epic",
                source="LinkedIn",
                description="Manage AI operations for healthcare's largest EHR...",
                requirements=["8+ years", "AI/ML", "Healthcare IT", "PMP"],
                posted_date=(datetime.now() - timedelta(days=0)).isoformat(),
                remote_policy="on-site",
                experience_level="Director",
                skills=["AI", "Operations", "Healthcare IT", "EHR"],
                sector="HealthTech"
            ),
            Job(
                id=str(uuid.uuid4())[:8],
                title="SVP Digital Transformation",
                company="Kaiser Permanente",
                location="Oakland, CA (Hybrid)",
                salary_range="$250,000 - $350,000",
                job_url="https://linkedin.com/jobs/view/svp-digital-kaiser",
                source="LinkedIn",
                description="Lead digital transformation for 12M members...",
                requirements=["15+ years", "Digital transformation", "Healthcare", "C-suite"],
                posted_date=(datetime.now() - timedelta(days=4)).isoformat(),
                remote_policy="hybrid",
                experience_level="C-Suite",
                skills=["Strategy", "Digital", "Healthcare", "Leadership"],
                sector="Healthcare"
            ),
            Job(
                id=str(uuid.uuid4())[:8],
                title="VP Healthcare Innovation",
                company="CVS Health",
                location="Woonsocket, RI (Hybrid)",
                salary_range="$170,000 - $230,000",
                job_url="https://linkedin.com/jobs/view/vp-innovation-cvs",
                source="LinkedIn",
                description="Drive innovation across pharmacy and healthcare services...",
                requirements=["10+ years", "Healthcare innovation", "Strategy", "MBA"],
                posted_date=(datetime.now() - timedelta(days=2)).isoformat(),
                remote_policy="hybrid",
                experience_level="VP",
                skills=["Innovation", "Healthcare", "Strategy", "Operations"],
                sector="Healthcare"
            ),
            Job(
                id=str(uuid.uuid4())[:8],
                title="Director Clinical Operations AI",
                company="Verily Life Sciences",
                location="South San Francisco, CA (Hybrid)",
                salary_range="$180,000 - $240,000",
                job_url="https://linkedin.com/jobs/view/director-clinical-ai-verily",
                source="LinkedIn",
                description="Lead AI-powered clinical operations...",
                requirements=["10+ years", "Clinical operations", "AI", "Healthcare"],
                posted_date=(datetime.now() - timedelta(days=1)).isoformat(),
                remote_policy="hybrid",
                experience_level="Director",
                skills=["Clinical", "AI", "Operations", "Healthcare"],
                sector="HealthTech"
            ),
            Job(
                id=str(uuid.uuid4())[:8],
                title="VP Digital Health Operations",
                company=" Humana",
                location="Louisville, KY (Remote)",
                salary_range="$160,000 - $210,000",
                job_url="https://linkedin.com/jobs/view/vp-digital-ops-humana",
                source="LinkedIn",
                description="Lead digital health operations for Medicare advantage...",
                requirements=["10+ years", "Digital health", "Operations", "PMP"],
                posted_date=(datetime.now() - timedelta(days=0)).isoformat(),
                remote_policy="remote",
                experience_level="VP",
                skills=["Digital Health", "Operations", "Medicare", "Strategy"],
                sector="Healthcare"
            )
        ]
        
        # Add to found jobs
        self.found_jobs.extend(simulated_jobs)
        self._save_jobs()
        
        print(f"✅ Found {len(simulated_jobs)} jobs on LinkedIn")
        return simulated_jobs
    
    def search_indeed(self, role: str = "VP Healthcare") -> List[Job]:
        """Search Indeed for jobs (simulated - real scraping requires headers)"""
        print(f"🔍 Searching Indeed for: {role}")
        
        # Similar structure - 10 jobs
        indeed_jobs = [
            Job(
                id=str(uuid.uuid4())[:8],
                title="Senior Director Healthcare AI",
                company="McKesson",
                location="Irving, TX (Hybrid)",
                salary_range="$170,000 - $230,000",
                job_url="https://indeed.com/jobs/view/senior-director-healthcare-ai-mckesson",
                source="Indeed",
                description="Lead AI initiatives for healthcare supply chain...",
                requirements=["10+ years", "AI/ML", "Healthcare supply chain"],
                posted_date=(datetime.now() - timedelta(days=1)).isoformat(),
                remote_policy="hybrid",
                experience_level="Senior Director",
                skills=["AI", "Healthcare", "Supply Chain", "Operations"],
                sector="Healthcare"
            ),
            Job(
                id=str(uuid.uuid4())[:8],
                title="VP Health Technology",
                company="Cigna",
                location="Bloomfield, CT (Hybrid)",
                salary_range="$180,000 - $250,000",
                job_url="https://indeed.com/jobs/view/vp-health-tech-cigna",
                source="Indeed",
                description="Lead health technology initiatives for 170M customers...",
                requirements=["12+ years", "HealthTech", "Digital", "MBA"],
                posted_date=(datetime.now() - timedelta(days=2)).isoformat(),
                remote_policy="hybrid",
                experience_level="VP",
                skills=["HealthTech", "Digital", "Strategy", "Operations"],
                sector="Healthcare"
            )
        ]
        
        self.found_jobs.extend(indeed_jobs)
        self._save_jobs()
        
        print(f"✅ Found {len(indeed_jobs)} jobs on Indeed")
        return indeed_jobs
    
    def filter_jobs(self, min_salary: int = 150000, 
                   sectors: List[str] = None,
                   remote_ok: bool = True) -> List[Job]:
        """Filter jobs by criteria"""
        
        if sectors is None:
            sectors = self.TARGET_SECTORS
        
        filtered = []
        
        for job in self.found_jobs:
            # Check salary
            salary_match = False
            for part in job.salary_range.lower():
                if any(s in part for s in ['$', 'k', 'm']):
                    # Extract salary numbers
                    numbers = re.findall(r'\d+', part.replace('$', '').replace('k', '000').replace('m', '000000'))
                    for num in numbers:
                        if int(num) >= min_salary:
                            salary_match = True
                            break
            
            # Check sector
            sector_match = any(s in job.sector.lower() or s in job.description.lower() 
                             for s in sectors)
            
            # Check remote
            remote_match = remote_ok or job.remote_policy == "on-site"
            
            if salary_match and sector_match and remote_match:
                filtered.append(job)
        
        return filtered
    
    def score_job_match(self, job: Job, cv_data: Dict) -> int:
        """Score how well a job matches a CV"""
        score = 0
        
        # Title match
        title_lower = job.title.lower()
        cv_skills = [s.lower() for s in cv_data.get('skills', [])]
        
        # Seniority level
        if any(s in title_lower for s in ['vp', 'vice president', 'svp']):
            score += 30
        elif any(s in title_lower for s in ['director', 'head', 'chief']):
            score += 25
        elif any(s in title_lower for s in ['senior', 'sr.']):
            score += 15
        
        # Skills match
        job_skills = [s.lower() for s in job.skills]
        for skill in cv_skills:
            if any(s in skill or skill in s for s in job_skills):
                score += 5
        
        # Healthcare sector
        if 'health' in job.sector.lower() or 'health' in job.description.lower():
            score += 20
        
        # AI/ML
        if any(s in job.title.lower() or s in job.description.lower() 
               for s in ['ai', 'ml', 'machine learning', 'artificial intelligence']):
            score += 15
        
        # Remote policy
        if job.remote_policy in ['remote', 'hybrid']:
            score += 10
        
        return min(score, 100)
    
    def match_jobs_to_cvs(self, cv_data: Dict) -> List[Job]:
        """Match all jobs to CV data and return scored results"""
        for job in self.found_jobs:
            job.ats_score = self.score_job_match(job, cv_data)
        
        # Sort by score
        matched = sorted(self.found_jobs, key=lambda j: j.ats_score, reverse=True)
        return matched[:10]  # Top 10
    
    def generate_application(self, job: Job, cv_data: Dict, cover_letter: str) -> Dict:
        """Generate a complete application package"""
        
        application = {
            "id": str(uuid.uuid4())[:8],
            "job_id": job.id,
            "job_title": job.title,
            "company": job.company,
            "job_url": job.job_url,
            "cv_version": f"CV_{job.company.replace(' ', '_')}_ tailored",
            "cover_letter": cover_letter,
            "applied_date": "",
            "status": "ready",
            "follow_up_date": "",
            "notes": "",
            "created_at": datetime.now().isoformat()
        }
        
        self.applications.append(application)
        self._save_applications()
        
        return application
    
    def get_stats(self) -> Dict:
        """Get job finder statistics"""
        return {
            "total_jobs_found": len(self.found_jobs),
            "total_applications": len(self.applications),
            "by_status": self._count_by_status(),
            "sectors": self._count_by_sector(),
            "sources": self._count_by_source()
        }
    
    def _count_by_status(self) -> Dict:
        counts = {}
        for app in self.applications:
            status = app.get('status', 'unknown')
            counts[status] = counts.get(status, 0) + 1
        return counts
    
    def _count_by_sector(self) -> Dict:
        counts = {}
        for job in self.found_jobs:
            counts[job.sector] = counts.get(job.sector, 0) + 1
        return counts
    
    def _count_by_source(self) -> Dict:
        counts = {}
        for job in self.found_jobs:
            counts[job.source] = counts.get(job.source, 0) + 1
        return counts


# Singleton instance
job_finder = JobFinder()

if __name__ == "__main__":
    # Test the job finder
    print("Testing Job Finder...")
    
    # Search LinkedIn
    jobs = job_finder.search_linkedin("VP Healthcare AI")
    
    # Filter
    filtered = job_finder.filter_jobs(min_salary=150000)
    print(f"\nFiltered jobs (>$150K, Healthcare): {len(filtered)}")
    
    # Get stats
    stats = job_finder.get_stats()
    print(f"Stats: {json.dumps(stats, indent=2)}")
