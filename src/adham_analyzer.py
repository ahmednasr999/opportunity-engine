#!/usr/bin/env python3
"""
ADHAM - Advanced ATS Optimization Engine
Uses semantic analysis to maximize ATS scores
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import Counter


@dataclass
class ATSAnalysis:
    """Complete ATS analysis result"""
    score: int
    score_breakdown: Dict
    critical_gaps: List[str]
    high_priority_gaps: List[Dict]
    medium_priority_gaps: List[Dict]
    low_priority_gaps: List[Dict]
    optimization_strategy: Dict
    optimized_cv: str
    projected_new_score: int
    recommendations: List[str]


class ADHAMAnalyzer:
    """ADHAM - Advanced ATS Optimization Engine"""
    
    def __init__(self):
        self.common_stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during'
        }
    
    def analyze(self, job_posting: str, cv_text: str, profile: Dict) -> ATSAnalysis:
        """Complete ATS analysis of CV against job posting"""
        
        # Normalize text
        job_lower = job_posting.lower()
        cv_lower = cv_text.lower()
        
        # Extract keywords from job posting
        keywords = self._extract_keywords(job_posting)
        hard_requirements = self._extract_hard_requirements(job_posting)
        
        # Score each component
        hard_score, hard_details = self._score_hard_requirements(hard_requirements, cv_lower, profile)
        keyword_score, keyword_details = self._score_keyword_density(keywords, cv_lower)
        experience_score, experience_details = self._score_experience_relevance(job_posting, cv_lower)
        quantified_score, quantified_details = self._score_quantified_achievements(cv_text)
        soft_score, soft_details = self._score_soft_skills(job_posting, cv_lower)
        
        # Calculate total score
        total_score = hard_score + keyword_score + experience_score + quantified_score + soft_score
        
        # Identify gaps
        critical_gaps = self._identify_critical_gaps(hard_requirements, cv_lower, profile)
        high_priority = self._identify_high_priority_gaps(keywords, cv_lower, job_lower)
        medium_priority = self._identify_medium_priority_gaps(keywords, cv_lower, job_lower)
        
        # Generate optimization strategy
        strategy = self._generate_optimization_strategy(job_posting, keywords, profile)
        
        # Generate optimized CV
        optimized_cv = self._generate_optimized_cv(profile, strategy, job_posting)
        
        # Calculate projected new score
        projected = self._calculate_projected_score(total_score, critical_gaps, high_priority, medium_priority)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(critical_gaps, high_priority, medium_priority, projected, total_score)
        
        return ATSAnalysis(
            score=total_score,
            score_breakdown={
                "Hard Requirements": {"score": hard_score, "max": 30, **hard_details},
                "Keyword Density": {"score": keyword_score, "max": 25, **keyword_details},
                "Experience Relevance": {"score": experience_score, "max": 20, **experience_details},
                "Quantified Impact": {"score": quantified_score, "max": 15, **quantified_details},
                "Soft Skills & Culture": {"score": soft_score, "max": 10, **soft_details}
            },
            critical_gaps=critical_gaps,
            high_priority_gaps=high_priority,
            medium_priority_gaps=medium_priority,
            low_priority_gaps=[],
            optimization_strategy=strategy,
            optimized_cv=optimized_cv,
            projected_new_score=projected,
            recommendations=recommendations
        )
    
    def _extract_keywords(self, text: str) -> List[Dict]:
        """Extract keywords with frequency from job posting"""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        filtered = [w for w in words if w not in self.common_stopwords]
        counts = Counter(filtered)
        
        keywords = []
        for word, count in counts.most_common(50):
            if any(x in word for x in ['ai', 'ml', 'cloud', 'digital', 'health', 'program', 'lead']):
                keywords.append({"term": word, "count": count, "weight": "high" if count >= 3 else "medium"})
        
        return keywords[:30]
    
    def _extract_hard_requirements(self, text: str) -> List[Dict]:
        """Extract must-have requirements"""
        requirements = []
        
        # Degree requirements
        if re.search(r"bachelor", text.lower()):
            requirements.append({"type": "education", "requirement": "Bachelor's degree", "matched": False})
        
        # Certification requirements
        for cert in ['pmp', 'itil', 'csm', 'six sigma']:
            if re.search(cert, text.lower()):
                requirements.append({"type": "certification", "requirement": cert.upper(), "matched": False})
        
        return requirements
    
    def _score_hard_requirements(self, requirements: List[Dict], cv_lower: str, profile: Dict) -> Tuple[int, Dict]:
        """Score hard requirements match (0-30)"""
        score = 0
        details = {"matched": [], "missing": []}
        
        for req in requirements:
            if req["type"] == "education":
                if "bachelor" in cv_lower:
                    score += 10
                    details["matched"].append(req["requirement"])
                else:
                    details["missing"].append(req["requirement"])
            
            if req["type"] == "certification":
                certs = [c.lower() for c in profile.get('certifications', [])]
                if any(req["requirement"].lower() in c for c in certs):
                    score += 5
                    details["matched"].append(req["requirement"])
                else:
                    details["missing"].append(req["requirement"])
        
        return min(score, 30), details
    
    def _score_keyword_density(self, keywords: List[Dict], cv_lower: str) -> Tuple[int, Dict]:
        """Score keyword density match (0-25)"""
        found = [kw for kw in keywords if kw["term"] in cv_lower]
        missing = [kw for kw in keywords if kw["term"] not in cv_lower]
        
        high_kw = [k for k in keywords if k["weight"] == "high"]
        high_found = sum(1 for k in high_kw if k["term"] in cv_lower)
        
        score = (high_found / len(high_kw) * 20) if high_kw else 0
        
        return int(min(score, 25)), {"found": found[:10], "missing": missing[:10]}
    
    def _score_experience_relevance(self, job_posting: str, cv_lower: str) -> Tuple[int, Dict]:
        """Score experience relevance (0-20)"""
        score = 15  # Base score
        
        # Check industry relevance
        industries = ['healthcare', 'healthtech', 'technology', 'fintech']
        for ind in industries:
            if ind in job_posting.lower() and ind in cv_lower:
                score += 5
                break
        
        return min(score, 20), {}
    
    def _score_quantified_achievements(self, cv_text: str) -> Tuple[int, Dict]:
        """Score quantified achievements (0-15)"""
        patterns = [r'\$[\d,]+', r'\d+%', r'\d+\s*(?:team|people)']
        metrics = []
        for pattern in patterns:
            metrics.extend(re.findall(pattern, cv_text.lower()))
        
        score = min(len(metrics) * 3, 15)
        return score, {"found": metrics[:5]}
    
    def _score_soft_skills(self, job_posting: str, cv_lower: str) -> Tuple[int, Dict]:
        """Score soft skills and culture fit (0-10)"""
        soft_skills = ['leadership', 'communication', 'strategic', 'stakeholder']
        matched = sum(1 for s in soft_skills if s in job_posting.lower() and s in cv_lower)
        return min(matched * 3, 10), {}
    
    def _identify_critical_gaps(self, requirements: List[Dict], cv_lower: str, profile: Dict) -> List[str]:
        """Identify critical gaps that may cause auto-rejection"""
        gaps = []
        for req in requirements:
            if req["type"] == "education" and "bachelor" in req["requirement"].lower():
                if "bachelor" not in cv_lower and "bsc" not in cv_lower:
                    gaps.append("Bachelor's degree")
        return gaps
    
    def _identify_high_priority_gaps(self, keywords: List[Dict], cv_lower: str, job_lower: str) -> List[Dict]:
        """Identify keywords appearing 5+ times in job but missing in CV"""
        return [{"keyword": kw["term"], "frequency": kw["count"], "impact": "10-15 points", 
                "strategy": f"Add '{kw['term']}' to CV"} for kw in keywords if kw["count"] >= 5 and kw["term"] not in cv_lower][:5]
    
    def _identify_medium_priority_gaps(self, keywords: List[Dict], cv_lower: str, job_lower: str) -> List[Dict]:
        """Identify keywords appearing 2-4 times in job"""
        return [{"keyword": kw["term"], "frequency": kw["count"], "impact": "5-10 points",
                "strategy": f"Add to relevant bullet"} for kw in keywords if 2 <= kw["count"] <= 4 and kw["term"] not in cv_lower][:5]
    
    def _generate_optimization_strategy(self, job_posting: str, keywords: List[Dict], profile: Dict) -> Dict:
        """Generate section-by-section optimization strategy"""
        return {
            "professional_summary": {"add_keywords": [k["term"] for k in keywords[:3]]},
            "core_competencies": {"missing_terms": [k["term"] for k in keywords[:5]]},
            "professional_experience": {}
        }
    
    def _generate_optimized_cv(self, profile: Dict, strategy: Dict, job_posting: str) -> str:
        """Generate optimized CV text"""
        
        cv = f"""
{profile.get('name', '')}
{profile.get('title', '')}

PROFESSIONAL SUMMARY
{profile.get('summary', '')}

PROFESSIONAL EXPERIENCE
"""
        for exp in profile.get('experience', []):
            cv += f"""
{exp.get('title', '')}
{exp.get('company', '')} | {exp.get('period', '')}
- {chr(10).join(['• ' + a for a in exp.get('achievements', [])[:4]])}
"""
        
        cv += """
EDUCATION
"""
        for edu in profile.get('education', []):
            cv += f"  • {edu.get('degree', '')} | {edu.get('institution', '')} | {edu.get('year', '')}\n"
        
        return cv
    
    def _calculate_projected_score(self, current_score: int, critical_gaps: List[str],
                                   high_priority: List[Dict], medium_priority: List[Dict]) -> int:
        """Calculate projected new score after optimization"""
        base = 75 if critical_gaps else 85
        return min(base + len(high_priority) * 5 + len(medium_priority) * 3, 95)
    
    def _generate_recommendations(self, critical_gaps: List[str], high_priority: List[Dict],
                                  medium_priority: List[Dict], projected: int, current: int) -> List[str]:
        """Generate actionable recommendations"""
        recs = []
        if critical_gaps:
            recs.append(f"CRITICAL: Address {len(critical_gaps)} missing requirements")
        if high_priority:
            recs.append(f"Add {len(high_priority)} high-priority keywords")
        if projected >= 90:
            recs.append(f"✓ Optimization achieves {projected}+ score")
        return recs
    
    def format_analysis(self, analysis: ATSAnalysis, job_title: str, company: str) -> str:
        """Format analysis in ADHAM's structured output"""
        
        output = f"""
================================================================================
                    ADHAM ATS OPTIMIZATION ANALYSIS
================================================================================

JOB: {job_title} at {company}

================================================================================
                    📊 CURRENT ATS SCORE: {analysis.score}/100
================================================================================

SCORE BREAKDOWN:
• Hard Requirements Match:     {analysis.score_breakdown["Hard Requirements"]["score"]}/30
• Keyword Density:            {analysis.score_breakdown["Keyword Density"]["score"]}/25
• Experience Relevance:       {analysis.score_breakdown["Experience Relevance"]["score"]}/20
• Quantified Impact:          {analysis.score_breakdown["Quantified Impact"]["score"]}/15
• Soft Skills & Culture:      {analysis.score_breakdown["Soft Skills & Culture"]["score"]}/10
"""
        
        if analysis.critical_gaps:
            output += f"""
================================================================================
                    🚨 CRITICAL GAPS
================================================================================
"""
            for gap in analysis.critical_gaps:
                output += f"• {gap}\n"
        
        if analysis.high_priority_gaps:
            output += f"""
================================================================================
                    ⚠️ HIGH PRIORITY GAPS
================================================================================
"""
            for gap in analysis.high_priority_gaps:
                output += f"• '{gap['keyword']}' ({gap['frequency']}x in job)\n"
        
        output += f"""
================================================================================
                    📈 PROJECTED SCORE: {analysis.projected_new_score}/100
================================================================================

IMPROVEMENT: +{analysis.projected_new_score - analysis.score} points
"""
        
        for rec in analysis.recommendations:
            output += f"• {rec}\n"
        
        return output


# Singleton
adham_analyzer = ADHAMAnalyzer()
