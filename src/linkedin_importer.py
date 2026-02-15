"""
LinkedIn Job Scraper - Auto-import job details from LinkedIn URLs
"""
import re
import json
from typing import Dict, Optional
from urllib.parse import urlparse

class LinkedInJobImporter:
    """Import job details from LinkedIn job posting URLs"""
    
    def __init__(self):
        self.job_patterns = [
            r'linkedin\.com/jobs/view/[^/]+',
            r'linkedin\.com/jobs/collection/[^/]+',
        ]
    
    def is_linkedin_url(self, url: str) -> bool:
        """Check if URL is a valid LinkedIn job URL"""
        return 'linkedin.com' in url and ('/jobs/' in url or 'jobId=' in url)
    
    def extract_job_id(self, url: str) -> Optional[str]:
        """Extract job ID from LinkedIn URL"""
        # Pattern 1: /jobs/view/1234567890
        match = re.search(r'/jobs/view/(\d+)', url)
        if match:
            return match.group(1)
        
        # Pattern 2: ?jobId=1234567890
        match = re.search(r'[?&]jobId=(\d+)', url)
        if match:
            return match.group(1)
        
        # Pattern 3: /jobs/collection/.../1234567890
        match = re.search(r'/jobs/collection/[^/]+/(\d+)', url)
        if match:
            return match.group(1)
        
        return None
    
    def scrape_job(self, url: str) -> Dict[str, str]:
        """
        Scrape job details from LinkedIn
        Note: LinkedIn blocks automated scraping. This is a framework that:
        1. Can use browser automation (Playwright/Selenium)
        2. Can accept manually pasted job details
        3. Provides structured extraction when content is available
        """
        job_id = self.extract_job_id(url)
        
        result = {
            'url': url,
            'job_id': job_id,
            'title': '',
            'company': '',
            'location': '',
            'description': '',
            'employment_type': '',
            'seniority_level': '',
            'industries': [],
            'job_functions': [],
            'scraped': False,
            'method': 'manual_required'
        }
        
        # Try to extract from URL patterns
        parsed = urlparse(url)
        path_parts = parsed.path.split('/')
        
        # Some URLs have job title in path
        for part in path_parts:
            if part and part not in ['jobs', 'view', 'collection']:
                # Clean up URL-encoded title
                clean = part.replace('-', ' ').replace('_', ' ')
                if len(clean) > 5 and not clean.isdigit():
                    result['title'] = clean.title()
                    break
        
        return result
    
    def format_for_cv_optimizer(self, job_data: Dict[str, str]) -> str:
        """Format scraped job data for CV Optimizer input"""
        formatted = f"""Job Title: {job_data.get('title', '')}
Company: {job_data.get('company', '')}
Location: {job_data.get('location', '')}
Employment Type: {job_data.get('employment_type', '')}
Seniority Level: {job_data.get('seniority_level', '')}

Job Description:
{job_data.get('description', '')}

Requirements:
{job_data.get('requirements', 'Please paste requirements here...')}

About the Company:
{job_data.get('company_description', '')}
"""
        return formatted
    
    def get_manual_import_template(self, url: str) -> Dict:
        """
        Return template for manual job import when scraping isn't possible
        """
        return {
            'url': url,
            'instruction': 'LinkedIn blocks automated scraping. Please paste the job details below.',
            'fields': {
                'title': {'label': 'Job Title', 'required': True},
                'company': {'label': 'Company Name', 'required': True},
                'location': {'label': 'Location', 'required': False},
                'description': {'label': 'Job Description', 'required': True, 'type': 'textarea'},
                'requirements': {'label': 'Requirements', 'required': True, 'type': 'textarea'},
            },
            'tips': [
                'Copy the full job description for best results',
                'Include requirements and qualifications',
                'Add company information if available'
            ]
        }

# Simple in-memory cache for job details
_job_cache = {}

def cache_job(job_id: str, job_data: Dict):
    """Cache job details to avoid re-scraping"""
    _job_cache[job_id] = job_data

def get_cached_job(job_id: str) -> Optional[Dict]:
    """Get cached job details"""
    return _job_cache.get(job_id)
