#!/usr/bin/env python3
"""
Additional Features Module
Phase 2 & 3 Features Implementation
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path


class CVFeatures:
    """CV Optimizer Additional Features"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> List[Dict]:
        """Load CV templates"""
        return [
            {
                "id": "healthtech",
                "name": "HealthTech Professional",
                "description": "Modern template for HealthTech AI leaders",
                "color_scheme": "blue_teal",
                "sections_order": ["summary", "experience", "skills", "education", "certifications"]
            },
            {
                "id": "fintech",
                "name": "FinTech Executive",
                "description": "Professional template for FinTech executives",
                "color_scheme": "green_gold",
                "sections_order": ["summary", "experience", "achievements", "skills", "education"]
            },
            {
                "id": "academic",
                "name": "Academic Researcher",
                "description": "Template for academic and research roles",
                "color_scheme": "gray_maroon",
                "sections_order": ["summary", "education", "research", "publications", "experience"]
            }
        ]
    
    def get_templates(self) -> List[Dict]:
        """Get all CV templates"""
        return self.templates
    
    def compare_cvs(self, cv1_data: Dict, cv2_data: Dict, job_requirements: Dict) -> Dict:
        """Compare two CV versions for the same job"""
        required_skills = set(job_requirements.get('required_skills', []))
        
        def analyze_cv(cv_data):
            ats_score = cv_data.get('ats_score', 0)
            skills = set(cv_data.get('skills', []))
            experience_years = cv_data.get('experience_years', 0)
            
            matched = skills.intersection(required_skills)
            missing = required_skills - skills
            
            return {
                "ats_score": ats_score,
                "skills_matched": len(matched),
                "skills_missing": len(missing),
                "matched_skills": list(matched),
                "missing_skills": list(missing),
                "experience_years": experience_years
            }
        
        analysis1 = analyze_cv(cv1_data)
        analysis2 = analyze_cv(cv2_data)
        
        winner = "cv1" if analysis1['ats_score'] > analysis2['ats_score'] else "cv2"
        if analysis1['ats_score'] == analysis2['ats_score']:
            winner = "tie"
        
        return {
            "cv1_analysis": analysis1,
            "cv2_analysis": analysis2,
            "winner": winner,
            "recommendation": f"CV1 has {analysis1['ats_score']}% ATS vs CV2's {analysis2['ats_score']}%"
        }
    
    def keyword_heatmap(self, cv_text: str, job_text: str) -> Dict:
        """Generate keyword heatmap showing matched/missing keywords"""
        # Extract keywords from job description
        job_keywords = set(re.findall(r'\b\w+\b', job_text.lower()))
        
        # Common stopwords to filter
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                     'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                     'would', 'could', 'should', 'may', 'might', 'must', 'can'}
        
        job_keywords = job_keywords - stopwords
        
        cv_text_lower = cv_text.lower()
        matched = []
        missing = []
        
        for keyword in job_keywords:
            if len(keyword) > 3:  # Only consider longer keywords
                if keyword in cv_text_lower:
                    matched.append(keyword)
                else:
                    missing.append(keyword)
        
        # Calculate match percentage
        total = len(matched) + len(missing)
        match_percentage = (len(matched) / total * 100) if total > 0 else 0
        
        return {
            "matched_keywords": matched[:20],  # Top 20
            "missing_keywords": missing[:20],
            "match_percentage": round(match_percentage, 1),
            "total_matched": len(matched),
            "total_missing": len(missing)
        }
    
    def analyze_bullet_strength(self, bullets: List[str]) -> Dict:
        """Analyze strength of bullet points"""
        strong_verbs = ['led', 'created', 'developed', 'implemented', 'managed', 'achieved',
                       'reduced', 'increased', 'optimized', 'transformed', 'delivered',
                       'exceeded', 'won', 'built', 'designed', 'launched', 'spearheaded']
        
        weak_words = ['helped', 'assisted', 'worked', 'participated', 'involved', 'tried']
        
        results = []
        strong_count = 0
        medium_count = 0
        weak_count = 0
        
        for bullet in bullets:
            bullet_lower = bullet.lower()
            
            if any(verb in bullet_lower for verb in strong_verbs):
                strength = "strong"
                strong_count += 1
            elif any(word in bullet_lower for word in weak_words):
                strength = "weak"
                weak_count += 1
            else:
                strength = "medium"
                medium_count += 1
            
            results.append({
                "bullet": bullet,
                "strength": strength,
                "suggestion": self._get_bullet_suggestion(bullet, strength)
            })
        
        return {
            "bullets": results,
            "strong": strong_count,
            "medium": medium_count,
            "weak": weak_count,
            "overall_score": round((strong_count * 3 + medium_count * 2 + weak_count * 1) / 
                                   (len(bullets) * 3) * 100, 1) if bullets else 0
        }
    
    def _get_bullet_suggestion(self, bullet: str, current_strength: str) -> str:
        """Get suggestion for improving bullet strength"""
        if current_strength == "weak":
            return "Start with a strong action verb and quantify results"
        elif current_strength == "medium":
            return "Add metrics and numbers to quantify impact"
        return "Great! Keep it up"


class ContentFeatures:
    """Content Factory Additional Features"""
    
    def predict_viral_score(self, content: str, topic: str) -> Dict:
        """Predict viral potential of content"""
        score = 50  # Base score
        
        # Engagement factors
        if "?" in content:
            score += 10  # Questions perform better
        
        if any(emoji in content for emoji in ["🔥", "💡", "⚡", "🎯"]):
            score += 5  # Emoji usage
        
        # Length factors
        if 1500 > len(content) > 300:
            score += 15  # Optimal length
        
        # Controversy factor
        contrarian_words = ["unpopular", "controversial", "actually", "really", "truth"]
        if any(word in content.lower() for word in contrarian_words):
            score += 10
        
        # List format
        if any(char in content for char in ["1️⃣", "2️⃣", "3️⃣", "•", "-"]):
            score += 10
        
        # Engagement prediction
        if score >= 80:
            prediction = "Highly Likely to Go Viral"
        elif score >= 60:
            prediction = "Good Viral Potential"
        elif score >= 40:
            prediction = "Average Engagement"
        else:
            prediction = "Low Viral Potential"
        
        return {
            "viral_score": min(score, 100),
            "prediction": prediction,
            "factors": {
                "question_bonus": 10 if "?" in content else 0,
                "emoji_bonus": 5 if any(emoji in content for emoji in ["🔥", "💡", "⚡", "🎯"]) else 0,
                "length_bonus": 15 if 1500 > len(content) > 300 else 0,
                "controversy_bonus": 10 if any(word in content.lower() for word in contrarian_words) else 0,
                "format_bonus": 10 if any(char in content for char in ["1️⃣", "2️⃣", "3️⃣", "•", "-"]) else 0
            }
        }
    
    def generate_quote_image(self, quote: str, author: str = "", template: str = "modern") -> Dict:
        """Generate quote image specs"""
        return {
            "quote": quote,
            "author": author,
            "template": template,
            "specs": {
                "width": 1200,
                "height": 1200,
                "background": "#1a1a2e" if template == "modern" else "#ffffff",
                "text_color": "#ffffff" if template == "modern" else "#1a1a2e",
                "font": "Montserrat",
                "branding": "Ahmed Nasr"
            },
            "generated_at": datetime.now().isoformat()
        }


class NetworkFeatures:
    """Network Mapper Additional Features"""
    
    def generate_contact_heatmap(self, contacts: List[Dict]) -> Dict:
        """Generate contact heatmap visualization data"""
        # Group contacts by recency of contact
        now = datetime.now()
        
        hot = []  # Contacted in last 7 days
        warm = []  # Contacted in last 30 days
        cold = []  # Not contacted in 30+ days
        
        for contact in contacts:
            last_contact = contact.get('last_contact_date', '')
            if last_contact:
                try:
                    last_date = datetime.fromisoformat(last_contact)
                    days_ago = (now - last_date).days
                    
                    if days_ago <= 7:
                        hot.append(contact)
                    elif days_ago <= 30:
                        warm.append(contact)
                    else:
                        cold.append(contact)
                except:
                    cold.append(contact)
            else:
                cold.append(contact)
        
        return {
            "hot": {"count": len(hot), "contacts": hot},
            "warm": {"count": len(warm), "contacts": warm},
            "cold": {"count": len(cold), "contacts": cold},
            "total": len(contacts),
            "recommendation": f"Reach out to {len(cold)} cold contacts this week"
        }


class JobScraperFeatures:
    """Job Auto-Scraper (Mock Implementation)"""
    
    def __init__(self):
        self.mock_jobs = self._load_mock_jobs()
    
    def _load_mock_jobs(self) -> List[Dict]:
        """Load mock job listings"""
        return [
            {
                "id": "job001",
                "title": "VP of Operations",
                "company": "Saudi German Hospital",
                "location": "Riyadh, Saudi Arabia",
                "salary": "$150,000 - $200,000",
                "source": "LinkedIn",
                "url": "https://linkedin.com/jobs/123",
                "posted_date": "2026-02-10",
                "description": "Looking for experienced VP to lead hospital operations..."
            },
            {
                "id": "job002",
                "title": "Director of AI",
                "company": "TechCorp Health",
                "location": "Dubai, UAE",
                "salary": "$180,000 - $250,000",
                "source": "Indeed",
                "url": "https://indeed.com/jobs/456",
                "posted_date": "2026-02-12",
                "description": "Seeking AI leader to transform healthcare delivery..."
            },
            {
                "id": "job003",
                "title": "PMO Lead",
                "company": "MENA HealthTech",
                "location": "Remote",
                "salary": "$120,000 - $160,000",
                "source": "Bayt",
                "url": "https://bayt.com/jobs/789",
                "posted_date": "2026-02-14",
                "description": "Lead project management office for healthcare initiatives..."
            }
        ]
    
    def search_jobs(self, keywords: str = "", location: str = "") -> List[Dict]:
        """Search for jobs (mock)"""
        results = self.mock_jobs
        
        if keywords:
            results = [j for j in results if keywords.lower() in j['title'].lower() 
                      or keywords.lower() in j['description'].lower()]
        
        if location:
            results = [j for j in results if location.lower() in j['location'].lower()]
        
        return results
    
    def import_from_linkedin(self, profile_url: str) -> Dict:
        """Simulate LinkedIn import"""
        return {
            "status": "success",
            "message": "LinkedIn import simulation - would scrape profile data",
            "profile_url": profile_url,
            "mock_data": {
                "name": "John Doe",
                "headline": "VP of Operations | Healthcare Leader",
                "connections": 500,
                "experience": [
                    {"title": "VP Operations", "company": "Hospital Group", "years": "5"}
                ]
            }
        }


import re  # Add this import
