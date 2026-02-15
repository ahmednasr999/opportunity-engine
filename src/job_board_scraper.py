"""
Job Board Scraper - Auto-import jobs from LinkedIn, Indeed, Glassdoor
"""
import re
import json
import os
from typing import Dict, List, Optional
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class JobBoardScraper:
    """Scrape job listings from major job boards"""
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.cache_file = os.path.join(self.data_dir, 'scraped_jobs.json')
        self.cache = self._load_cache()
    
    def _load_cache(self) -> List[Dict]:
        """Load cached jobs"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_cache(self):
        """Save jobs to cache"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def extract_job_from_url(self, url: str) -> Dict:
        """
        Extract job details from URL
        Supports: LinkedIn, Indeed, Glassdoor, AngelList, company career pages
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        job_data = {
            'url': url,
            'source': self._identify_source(domain),
            'scraped_at': datetime.now().isoformat(),
            'title': '',
            'company': '',
            'location': '',
            'description': '',
            'salary': '',
            'employment_type': '',
            'remote': False,
            'status': 'needs_manual_entry'  # Flag for manual review
        }
        
        # Extract from URL patterns
        if 'linkedin.com' in domain:
            job_data.update(self._parse_linkedin_url(url))
        elif 'indeed.com' in domain:
            job_data.update(self._parse_indeed_url(url))
        elif 'glassdoor.com' in domain:
            job_data.update(self._parse_glassdoor_url(url))
        elif 'angel.co' in domain or 'wellfound.com' in domain:
            job_data.update(self._parse_angellist_url(url))
        
        # Add to cache
        self.cache.append(job_data)
        self._save_cache()
        
        return job_data
    
    def _identify_source(self, domain: str) -> str:
        """Identify job board from domain"""
        if 'linkedin.com' in domain:
            return 'LinkedIn'
        elif 'indeed.com' in domain:
            return 'Indeed'
        elif 'glassdoor.com' in domain:
            return 'Glassdoor'
        elif 'angel.co' in domain or 'wellfound.com' in domain:
            return 'AngelList'
        elif 'greenhouse.io' in domain:
            return 'Greenhouse'
        elif 'lever.co' in domain:
            return 'Lever'
        elif 'workday.com' in domain:
            return 'Workday'
        else:
            return 'Company Career Page'
    
    def _parse_linkedin_url(self, url: str) -> Dict:
        """Extract job ID and info from LinkedIn URL"""
        job_id = None
        title = None
        
        # Extract job ID
        match = re.search(r'/jobs/view/(\d+)', url)
        if match:
            job_id = match.group(1)
        else:
            match = re.search(r'[?&]jobId=(\d+)', url)
            if match:
                job_id = match.group(1)
        
        # Try to extract title from URL path
        match = re.search(r'/jobs/view/[^/]+-([^/\d]+)', url)
        if match:
            title_part = match.group(1)
            title = title_part.replace('-', ' ').replace('_', ' ').title()
        
        return {
            'job_id': job_id,
            'title': title or '',
            'company': '',  # Would need page scraping
            'notes': 'LinkedIn requires manual entry of description'
        }
    
    def _parse_indeed_url(self, url: str) -> Dict:
        """Extract job info from Indeed URL"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        job_id = params.get('jk', [''])[0]
        
        # Try to extract from path
        title = None
        company = None
        path_parts = parsed.path.split('/')
        if len(path_parts) > 2:
            # Format: /viewjob?jk=... or /q-*-l-*
            pass
        
        return {
            'job_id': job_id,
            'title': title or '',
            'company': company or '',
            'notes': 'Indeed requires manual entry of description'
        }
    
    def _parse_glassdoor_url(self, url: str) -> Dict:
        """Extract job info from Glassdoor URL"""
        job_id = None
        match = re.search(r'-KO\d+,(\d+)\.htm', url)
        if match:
            job_id = match.group(1)
        
        return {
            'job_id': job_id,
            'notes': 'Glassdoor requires manual entry'
        }
    
    def _parse_angellist_url(self, url: str) -> Dict:
        """Extract job info from AngelList URL"""
        return {
            'notes': 'AngelList/Wellfound job detected'
        }
    
    def get_company_research(self, company_name: str) -> Dict:
        """
        Get research on a company (would integrate with APIs)
        For now, returns template
        """
        return {
            'company': company_name,
            'glassdoor_rating': None,  # Would call Glassdoor API
            'recent_news': [],  # Would call News API
            'funding_info': None,  # Would call Crunchbase API
            'employee_count': None,
            'interview_process': None,
            'culture_keywords': [],
            'competitors': []
        }
    
    def get_interview_questions(self, company: str, role: str) -> List[str]:
        """
        Get common interview questions for company/role
        Would integrate with Glassdoor API or similar
        """
        # Generic questions by role type
        questions = {
            'pmo': [
                'How do you establish a PMO from scratch?',
                'Describe your experience with SAP S/4HANA implementation',
                'How do you measure PMO success?',
                'Tell me about a time you managed 300+ concurrent projects'
            ],
            'digital_transformation': [
                'How do you drive digital transformation in healthcare?',
                'Describe your experience with Health Catalyst or similar platforms',
                'How do you measure ROI on digital initiatives?',
                'Tell me about leading AI implementation in healthcare'
            ],
            'healthcare': [
                'How do you ensure JCI compliance?',
                'Describe your experience with EMR/HIS systems',
                'How do you manage stakeholder expectations in hospitals?',
                'Tell me about improving patient outcomes through technology'
            ],
            'leadership': [
                'How do you lead cross-functional teams across multiple countries?',
                'Describe your approach to change management',
                'How do you align technology with business strategy?',
                'Tell me about a failed project and what you learned'
            ]
        }
        
        # Return relevant questions
        role_lower = role.lower()
        result = []
        
        if 'pmo' in role_lower or 'project' in role_lower:
            result.extend(questions['pmo'])
        if 'transformation' in role_lower or 'digital' in role_lower:
            result.extend(questions['digital_transformation'])
        if any(word in role_lower for word in ['health', 'hospital', 'medical']):
            result.extend(questions['healthcare'])
        
        result.extend(questions['leadership'])
        
        return result[:6]  # Return top 6
    
    def estimate_success_probability(self, job: Dict, profile: Dict) -> Dict:
        """
        Estimate probability of getting offer based on match
        """
        score = 50  # Base score
        factors = []
        
        # Check title alignment
        job_title = job.get('title', '').lower()
        if any(word in job_title for word in ['pmo', 'project', 'program']):
            score += 15
            factors.append('✓ PMO experience match')
        
        if any(word in job_title for word in ['digital', 'transformation']):
            score += 15
            factors.append('✓ Digital transformation match')
        
        if any(word in job_title for word in ['health', 'hospital', 'medical']):
            score += 20
            factors.append('✓ HealthTech sector match')
        
        # Check certifications mentioned
        desc = job.get('description', '').lower()
        if 'pmp' in desc:
            score += 5
            factors.append('✓ PMP certification')
        
        if 'mba' in desc:
            score += 5
            factors.append('✓ MBA qualification')
        
        # Cap at 95%
        score = min(score, 95)
        
        return {
            'probability': score,
            'confidence': 'Medium' if score < 70 else 'High',
            'factors': factors,
            'recommendation': 'Strong apply' if score >= 70 else 'Tailor CV more' if score >= 50 else 'Consider other roles'
        }
    
    def auto_fill_job_form(self, url: str) -> Dict:
        """
        Main method: Take a job URL, extract all possible info
        Returns dict ready for Job Tracker
        """
        job_data = self.extract_job_from_url(url)
        
        # Add company research
        if job_data.get('company'):
            job_data['company_research'] = self.get_company_research(job_data['company'])
        
        # Add interview questions
        job_data['interview_prep'] = self.get_interview_questions(
            job_data.get('company', ''),
            job_data.get('title', '')
        )
        
        return job_data
