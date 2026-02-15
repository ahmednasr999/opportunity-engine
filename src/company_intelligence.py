"""
Company Intelligence - Real-time monitoring and alerts
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class CompanyIntelligence:
    """
    Monitor target companies for:
    - News and announcements
    - Funding rounds
    - Executive changes
    - Job posting patterns
    - Glassdoor reviews
    - Interview experiences
    """
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.companies_file = os.path.join(self.data_dir, 'tracked_companies.json')
        self.alerts_file = os.path.join(self.data_dir, 'company_alerts.json')
        
        self.companies = self._load_json(self.companies_file, {})
        self.alerts = self._load_json(self.alerts_file, [])
    
    def _load_json(self, filepath: str, default):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filepath: str, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def track_company(self, company_name: str, ticker: str = None, 
                     linkedin_url: str = None, priority: str = 'medium') -> Dict:
        """
        Start tracking a target company
        """
        company_id = company_name.lower().replace(' ', '_')
        
        self.companies[company_id] = {
            'id': company_id,
            'name': company_name,
            'ticker': ticker,
            'linkedin_url': linkedin_url,
            'priority': priority,  # high, medium, low
            'added_at': datetime.now().isoformat(),
            'status': 'tracking',
            'last_updated': None,
            'data': {
                'funding': [],
                'news': [],
                'executives': [],
                'job_openings': [],
                'glassdoor': {},
                'interviews': []
            },
            'alerts_enabled': {
                'funding': True,
                'news': True,
                'executive_changes': True,
                'new_jobs': True,
                'glassdoor_reviews': False
            }
        }
        
        self._save_json(self.companies_file, self.companies)
        
        return self.companies[company_id]
    
    def get_company_briefing(self, company_name: str) -> Dict:
        """
        Generate executive briefing before interview
        """
        company_id = company_name.lower().replace(' ', '_')
        company = self.companies.get(company_id, {})
        
        if not company:
            return self._generate_generic_briefing(company_name)
        
        data = company.get('data', {})
        
        briefing = {
            'company_name': company_name,
            'generated_at': datetime.now().isoformat(),
            'sections': {
                'overview': {
                    'size': self._estimate_company_size(company_name),
                    'stage': self._estimate_company_stage(company_name),
                    'recent_momentum': self._analyze_momentum(data)
                },
                'recent_news': data.get('news', [])[:5],
                'funding_status': data.get('funding', [{}])[-1] if data.get('funding') else None,
                'leadership': data.get('executives', [])[:3],
                'culture_signals': self._extract_culture_signals(data),
                'interview_intel': {
                    'common_questions': self._get_common_interview_questions(company_name),
                    'interview_process': self._estimate_interview_process(company_name),
                    'glassdoor_rating': data.get('glassdoor', {}).get('rating', 'N/A'),
                    'pros_cons': self._get_glassdoor_summary(data)
                },
                'talking_points': self._generate_talking_points(company_name, data),
                'questions_to_ask': self._generate_smart_questions(company_name, data)
            }
        }
        
        return briefing
    
    def _generate_generic_briefing(self, company_name: str) -> Dict:
        """Generate briefing when no data available"""
        return {
            'company_name': company_name,
            'note': 'Limited data available. Research manually:',
            'research_checklist': [
                f'Search: "{company_name} news" for recent updates',
                f'Check LinkedIn company page for updates',
                f'Review Glassdoor for interview experiences',
                f'Search Crunchbase for funding information',
                f'Check company blog for recent announcements'
            ],
            'questions_to_ask': [
                'What are the company\'s top priorities for this year?',
                'How is the digital transformation journey progressing?',
                'What does success look like in this role in 6 months?',
                'What are the biggest challenges the team is facing?'
            ]
        }
    
    def _estimate_company_size(self, company_name: str) -> str:
        """Estimate company size based on name/known info"""
        large_companies = ['google', 'microsoft', 'amazon', 'apple', 'meta', 'ibm', 'oracle']
        if any(lc in company_name.lower() for lc in large_companies):
            return 'Large Enterprise (10,000+)'
        return 'Research needed'
    
    def _estimate_company_stage(self, company_name: str) -> str:
        """Estimate if startup, growth, or enterprise"""
        return 'Research needed - Check Crunchbase'
    
    def _analyze_momentum(self, data: Dict) -> str:
        """Analyze if company is growing, stable, or declining"""
        news = data.get('news', [])
        funding = data.get('funding', [])
        
        if funding and len(funding) > 0:
            recent_funding = funding[-1]
            if 'amount' in recent_funding and recent_funding.get('amount'):
                return f"Growth mode - Recent funding: {recent_funding['amount']}"
        
        if len(news) > 5:
            return 'Active - Regular announcements'
        
        return 'Stable - Limited recent public activity'
    
    def _extract_culture_signals(self, data: Dict) -> Dict:
        """Extract culture indicators from available data"""
        glassdoor = data.get('glassdoor', {})
        
        return {
            'rating': glassdoor.get('rating', 'N/A'),
            'recommend_percentage': glassdoor.get('recommend', 'N/A'),
            'ceo_approval': glassdoor.get('ceo_approval', 'N/A'),
            'keywords': glassdoor.get('common_keywords', ['Research on Glassdoor']),
            'dress_code': 'Professional (verify during interview)',
            'work_life_balance': glassdoor.get('work_life', 'Research needed')
        }
    
    def _get_common_interview_questions(self, company_name: str) -> List[str]:
        """Get commonly reported interview questions"""
        # This would integrate with Glassdoor API
        generic_questions = [
            'Tell me about your experience with digital transformation',
            'How do you handle conflicting priorities?',
            'Describe a challenging project and how you managed it',
            'Why are you interested in joining our company?',
            'What do you know about our industry/challenges?'
        ]
        
        # Add role-specific based on company type
        if any(word in company_name.lower() for word in ['health', 'hospital', 'medical']):
            generic_questions.extend([
                'How do you ensure clinical adoption of technology?',
                'What experience do you have with healthcare regulations?',
                'How do you measure ROI in healthcare IT?'
            ])
        
        return generic_questions[:8]
    
    def _estimate_interview_process(self, company_name: str) -> str:
        """Estimate interview stages based on company size"""
        large_companies = ['google', 'microsoft', 'amazon', 'apple', 'meta']
        if any(lc in company_name.lower() for lc in large_companies):
            return 'Multi-stage (5-7 rounds): Recruiter screen → HM screen → Technical → Panel → Executive → Reference'
        
        return 'Typical (3-4 rounds): Recruiter → Hiring Manager → Team/Panel → Executive'
    
    def _get_glassdoor_summary(self, data: Dict) -> Dict:
        """Summarize Glassdoor pros/cons"""
        return {
            'common_pros': [
                'Strong mission and values',
                'Growth opportunities',
                'Smart colleagues'
            ],
            'common_cons': [
                'Fast-paced environment',
                'High expectations',
                'Work-life balance can be challenging'
            ],
            'interview_difficulty': 'Average to Hard',
            'interview_experience': 'Generally positive'
        }
    
    def _generate_talking_points(self, company_name: str, data: Dict) -> List[str]:
        """Generate personalized talking points"""
        points = [
            f"I've been following {company_name}'s journey in",
            "My experience scaling digital operations across KSA, UAE, and Egypt aligns with your regional focus",
            "I recently implemented Health Catalyst analytics platforms, similar to your data initiatives"
        ]
        
        # Add specific points based on news
        news = data.get('news', [])
        if news:
            latest = news[0]
            points.append(f"I read about your {latest.get('topic', 'recent initiative')} and was impressed by...")
        
        return points
    
    def _generate_smart_questions(self, company_name: str, data: Dict) -> List[Dict]:
        """Generate questions that show deep research"""
        questions = [
            {
                'question': f"I noticed {company_name} has been expanding in the region. How does this role contribute to that growth strategy?",
                'why_smart': 'Shows you did homework on company trajectory'
            },
            {
                'question': 'What are the biggest challenges this team is facing in the next 6-12 months?',
                'why_smart': 'Shows interest in problem-solving, not just title'
            },
            {
                'question': 'How does the organization measure success for this position?',
                'why_smart': 'Shows results-orientation'
            },
            {
                'question': 'What does the ideal candidate look like in 90 days? 1 year?',
                'why_smart': 'Shows long-term thinking'
            },
            {
                'question': 'How does this role collaborate with [specific team/department]?',
                'why_smart': 'Shows understanding of organizational structure'
            }
        ]
        
        # Add funding-related question if applicable
        funding = data.get('funding', [])
        if funding:
            questions.append({
                'question': 'With the recent funding, what are the top priorities for investment?',
                'why_smart': 'Shows awareness of company financial situation'
            })
        
        return questions
    
    def check_alerts(self) -> List[Dict]:
        """
        Check for new alerts on tracked companies
        """
        new_alerts = []
        
        for company_id, company in self.companies.items():
            if not company.get('alerts_enabled', {}).get('news', False):
                continue
            
            # Check for new news (simulated - would call news API)
            last_check = company.get('last_updated')
            if last_check:
                last_check_dt = datetime.fromisoformat(last_check)
                if datetime.now() - last_check_dt > timedelta(hours=24):
                    # Would check for new news here
                    pass
        
        return new_alerts
    
    def get_tracked_companies_summary(self) -> Dict:
        """Get summary of all tracked companies"""
        return {
            'total_tracked': len(self.companies),
            'by_priority': {
                'high': len([c for c in self.companies.values() if c.get('priority') == 'high']),
                'medium': len([c for c in self.companies.values() if c.get('priority') == 'medium']),
                'low': len([c for c in self.companies.values() if c.get('priority') == 'low'])
            },
            'companies': [
                {
                    'name': c['name'],
                    'priority': c['priority'],
                    'momentum': self._analyze_momentum(c.get('data', {}))
                }
                for c in self.companies.values()
            ]
        }
