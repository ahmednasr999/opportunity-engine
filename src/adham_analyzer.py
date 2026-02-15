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

# spaCy is optional - will use basic NLP if not available
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        nlp = None
except ImportError:
    nlp = None

print("ADHAM ATS Engine initialized (basic mode - install spacy for advanced NLP)")


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
    """
    ADHAM - Advanced ATS Optimization Engine
    
    Scoring Framework (0-100):
    - Hard Requirements Match: 30 points
    - Keyword Density: 25 points
    - Experience Relevance: 20 points
    - Quantified Achievements: 15 points
    - Soft Skills & Culture Fit: 10 points
    """
    
    def __init__(self):
        self.common_stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
            'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
            'can', 'will', 'just', 'should', 'now', 'job', 'work', 'role', 'position'
        }
    
    def analyze(self, job_posting: str, cv_text: str, profile: Dict) -> ATSAnalysis:
        """
        Complete ATS analysis of CV against job posting
        
        Returns structured analysis following ADHAM framework
        """
        
        # Normalize text
        job_lower = job_posting.lower()
        cv_lower = cv_text.lower()
        
        # Extract keywords from job posting
        keywords = self._extract_keywords(job_posting)
        hard_requirements = self._extract_hard_requirements(job_posting)
        action_verbs = self._extract_action_verbs(job_posting)
        seniority_indicators = self._extract_seniority(job_posting)
        quantitative_thresholds = self._extract_quantitative(job_posting)
        
        # Score each component
        hard_score, hard_details = self._score_hard_requirements(
            hard_requirements, cv_lower, profile
        )
        keyword_score, keyword_details = self._score_keyword_density(
            keywords, cv_lower
        )
        experience_score, experience_details = self._score_experience_relevance(
            job_posting, cv_lower, seniority_indicators
        )
        quantified_score, quantified_details = self._score_quantified_achievements(
            cv_text
        )
        soft_score, soft_details = self._score_soft_skills(
            job_posting, cv_lower, keywords
        )
        
        # Calculate total score
        total_score = hard_score + keyword_score + experience_score + quantified_score + soft_score
        
        # Identify gaps
        critical_gaps = self._identify_critical_gaps(hard_requirements, cv_lower, profile)
        high_priority = self._identify_high_priority_gaps(keywords, cv_lower, job_lower)
        medium_priority = self._identify_medium_priority_gaps(keywords, cv_lower, job_lower)
        low_priority = self._identify_low_priority_gaps(keywords, cv_lower)
        
        # Generate optimization strategy
        strategy = self._generate_optimization_strategy(
            job_posting, keywords, hard_requirements, critical_gaps,
            high_priority, medium_priority, profile
        )
        
        # Generate optimized CV
        optimized_cv = self._generate_optimized_cv(profile, strategy, job_posting)
        
        # Calculate projected new score
        projected = self._calculate_projected_score(
            total_score, critical_gaps, high_priority, medium_priority
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            critical_gaps, high_priority, medium_priority, projected, total_score
        )
        
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
            low_priority_gaps=low_priority,
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
        
        # Group related terms
        keywords = []
        for word, count in counts.most_common(50):
            # Identify technical terms, methodologies, tools
            if any(x in word for x in ['ai', 'ml', 'aws', 'azure', 'cloud', 'agile', 'scrum', 
                                         'pmp', 'itil', 'python', 'java', 'sql', 'api', 'data',
                                         'digital', 'transform', 'automation', 'analytics', 'health',
                                         'program', 'project', 'manager', 'lead', 'director']):
                keywords.append({
                    "term": word,
                    "count": count,
                    "weight": "high" if count >= 3 else "medium" if count >= 2 else "low"
                })
        
        return keywords[:30]
    
    def _extract_hard_requirements(self, text: str) -> List[Dict]:
        """Extract must-have requirements"""
        requirements = []
        
        # Degree requirements
        degree_patterns = [
            (r"(bachelor['s]?\s+(?:of|in)\s+\w+)", "Bachelor's degree required"),
            (r"(master['s]?\s+(?:of|in)\s+\w+)", "Master's degree required"),
            (r"(mba)", "MBA required/preferred"),
            (r"(phd|doctorate)", "PhD preferred")
        ]
        
        for pattern, desc in degree_patterns:
            if re.search(pattern, text.lower()):
                requirements.append({
                    "type": "education",
                    "requirement": desc,
                    "matched": False
                })
        
        # Certification requirements
        cert_patterns = [
            (r"pmp", "PMP certification"),
            (r"itil", "ITIL certification"),
            (r"csm|certified scrum master", "Scrum certification"),
            (r"six sigma", "Six Sigma certification"),
            (r"mba", "MBA")
        ]
        
        for pattern, desc in cert_patterns:
            if re.search(pattern, text.lower()):
                requirements.append({
                    "type": "certification",
                    "requirement": desc,
                    "matched": False
                })
        
        # Experience requirements
        exp_patterns = [
            (r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)", "Years of experience")
        ]
        
        for pattern, desc in exp_patterns:
            match = re.search(pattern, text.lower())
            if match:
                requirements.append({
                    "type": "experience",
                    "requirement": f"{match.group(1)}+ years experience",
                    "years": int(match.group(1)),
                    "matched": False
                })
        
        return requirements
    
    def _extract_action_verbs(self, text: str) -> List[str]:
        """Extract action verbs used in job posting"""
        action_verbs = [
            'lead', 'manage', 'direct', 'oversee', 'coordinate', 'implement',
            'develop', 'create', 'build', 'design', 'architect', 'strategize',
            'drive', 'ensure', 'optimize', 'improve', 'transform', 'deliver',
            'collaborate', 'communicate', 'stakeholder', 'vendor', 'negotiate'
        ]
        
        found = []
        text_lower = text.lower()
        for verb in action_verbs:
            if verb in text_lower:
                found.append(verb)
        
        return found
    
    def _extract_seniority(self, text: str) -> Dict:
        """Extract seniority requirements"""
        seniority = {
            "level": "mid",
            "indicators": [],
            "scope": {}
        }
        
        text_lower = text.lower()
        
        # Executive indicators
        if any(x in text_lower for x in ['chief', 'vp', 'vice president', 'senior vice president', 'svp']):
            seniority["level"] = "executive"
            seniority["indicators"].append("C-suite/VP level")
        
        # Director indicators
        if any(x in text_lower for x in ['director', 'head of', 'chief of']):
            seniority["level"] = "director"
            seniority["indicators"].append("Director level")
        
        # Senior indicators
        if any(x in text_lower for x in ['senior', 'sr.', 'sr ']):
            seniority["level"] = "senior"
            seniority["indicators"].append("Senior level")
        
        # Management scope
        if re.search(r"(\d+)\+?\s*(?:team|people|resources)", text_lower):
            match = re.search(r"(\d+)\+?\s*(?:team|people|resources)", text_lower)
            seniority["scope"]["team_size"] = int(match.group(1))
        
        if re.search(r"\$([\d,]+)\s*(?:million|billion|m)", text_lower):
            match = re.search(r"\$([\d,]+)\s*(?:million|billion|m)", text_lower)
            budget = int(match.group(1).replace(',', ''))
            if 'million' in text_lower:
                budget *= 1000000
            elif 'billion' in text_lower:
                budget *= 1000000000
            seniority["scope"]["budget"] = budget
        
        return seniority
    
    def _extract_quantitative(self, text: str) -> List[Dict]:
        """Extract quantitative thresholds"""
        thresholds = []
        
        # Years
        years_match = re.findall(r"(\d+)\+?\s*(?:years?|yrs?)", text.lower())
        for years in years_match:
            thresholds.append({
                "type": "years",
                "value": int(years),
                "context": "experience"
            })
        
        # Budget
        budget_match = re.findall(r"\$([\d,]+)\s*(?:million|billion|m)", text)
        for budget in budget_match:
            val = int(budget.replace(',', ''))
            if 'million' in budget_match or 'm' in text.lower():
                val *= 1000000
            thresholds.append({
                "type": "budget",
                "value": val,
                "context": "budget"
            })
        
        return thresholds
    
    def _score_hard_requirements(self, requirements: List[Dict], cv_lower: str, 
                                 profile: Dict) -> Tuple[int, Dict]:
        """Score hard requirements match (0-30)"""
        score = 0
        max_score = 30
        details = {"matched": [], "missing": []}
        
        # Check education
        for req in requirements:
            if req["type"] == "education":
                if "bachelor" in req["requirement"].lower():
                    if "bachelor" in cv_lower or "b.com" in cv_lower or "commerce" in cv_lower:
                        score += 10
                        details["matched"].append(req["requirement"])
                    else:
                        details["missing"].append(req["requirement"])
                elif "mba" in req["requirement"].lower():
                    if "mba" in cv_lower or "master" in cv_lower:
                        score += 10
                        details["matched"].append(req["requirement"])
                    else:
                        details["missing"].append(f"{req['requirement']} (in progress acceptable)")
        
        # Check certifications
        certs = profile.get('certifications', [])
        certs_lower = [c.lower() for c in certs]
        
        for req in requirements:
            if req["type"] == "certification":
                cert_name = req["requirement"].lower()
                if any(cert_name[:4] in c[:4] for c in certs_lower if len(c) >= 4):
                    score += 5
                    details["matched"].append(req["requirement"])
                else:
                    details["missing"].append(req["requirement"])
        
        # Check experience years
        for req in requirements:
            if req["type"] == "experience":
                total_years = profile.get('total_experience_years', 0)
                if total_years >= req["years"]:
                    score += 15
                    details["matched"].append(f"{total_years} years (required: {req['years']}+)")
                else:
                    details["missing"].append(f"{req['years']}+ years required")
        
        # Cap at max
        score = min(score, max_score)
        
        return score, details
    
    def _score_keyword_density(self, keywords: List[Dict], cv_lower: str) -> Tuple[int, Dict]:
        """Score keyword density match (0-25)"""
        max_score = 25
        found = []
        missing = []
        
        for kw in keywords:
            if kw["term"] in cv_lower:
                found.append(kw["term"])
            else:
                missing.append(kw["term"])
        
        # Score based on percentage of high/medium weight keywords found
        high_kw = [k for k in keywords if k["weight"] == "high"]
        medium_kw = [k for k in keywords if k["weight"] == "medium"]
        
        high_found = sum(1 for k in high_kw if k["term"] in cv_lower)
        medium_found = sum(1 for k in medium_kw if k["term"] in cv_lower)
        
        high_score = (high_found / len(high_kw) * 20) if high_kw else 0
        medium_score = (medium_found / len(medium_kw) * 5) if medium_kw else 0
        
        total = min(high_score + medium_score, max_score)
        
        return int(total), {
            "found": found[:10],
            "missing": missing[:10],
            "match_rate": f"{len(found)}/{len(keywords)} keywords"
        }
    
    def _score_experience_relevance(self, job_posting: str, cv_lower: str,
                                    seniority: Dict) -> Tuple[int, Dict]:
        """Score experience relevance (0-20)"""
        max_score = 20
        score = 0
        details = {}
        
        # Check industry relevance
        industries = ['healthcare', 'healthtech', 'technology', 'fintech', 'consulting']
        cv_industries = [i for i in industries if i in cv_lower]
        job_industries = [i for i in industries if i in job_posting.lower()]
        
        relevant = set(cv_industries) & set(job_industries)
        if relevant:
            score += 10
            details["industry_match"] = f"Relevant: {list(relevant)}"
        
        # Check seniority alignment
        profile_titles = cv_lower
        seniority_score = 0
        
        if seniority["level"] == "executive":
            if any(x in profile_titles for x in ['chief', 'vp', 'vice president', 'director', 'head']):
                seniority_score = 10
                details["seniority"] = "Executive level alignment ✓"
            else:
                seniority_score = 5
                details["seniority"] = "Seniority gap - consider repositioning"
        elif seniority["level"] == "director":
            if any(x in profile_titles for x in ['director', 'head', 'chief']):
                seniority_score = 10
                details["seniority"] = "Director level alignment ✓"
            else:
                seniority_score = 7
                details["seniority"] = "Near-director level"
        else:
            seniority_score = 8
            details["seniority"] = "Experience level acceptable"
        
        score = min(score + seniority_score, max_score)
        
        return score, details
    
    def _score_quantified_achievements(self, cv_text: str) -> Tuple[int, Dict]:
        """Score quantified achievements (0-15)"""
        max_score = 15
        score = 0
        details = {"found": [], "missing": []}
        
        # Find quantified metrics - simplified patterns
        patterns = [
            r'\$[\d,]+(?:\s*(?:million|billion|m))?',
            r'\d+(?:\.\d+)?\s*%',
            r'\d+\s*(?:team|people|resources|staff)',
            r'\d+\s*(?:months?|years?)',
        ]
        
        metrics = []
        for pattern in patterns:
            metrics.extend(re.findall(pattern, cv_text.lower()))
        
        if metrics:
            score = min(len(metrics) * 3, max_score)
            details["found"] = metrics[:5]
        else:
            details["missing"].append("Add quantified achievements ($X, X%, X team, X months)")
        
        return score, details
    
    def _score_soft_skills(self, job_posting: str, cv_lower: str,
                          keywords: List[Dict]) -> Tuple[int, Dict]:
        """Score soft skills and culture fit (0-10)"""
        max_score = 10
        score = 0
        details = {}
        
        # Extract soft skills from job posting
        soft_skills = [
            'leadership', 'communication', 'collaboration', 'stakeholder', 'problem solving',
            'analytical', 'strategic', 'innovative', 'team player', 'results-driven',
            'cross-functional', 'agile', 'adaptable', 'influential', 'negotiation'
        ]
        
        job_soft = [s for s in soft_skills if s in job_posting.lower()]
        cv_soft = [s for s in soft_skills if s in cv_lower]
        
        matched = set(job_soft) & set(cv_soft)
        
        score = min(len(matched) * 2, max_score)
        
        details["matched"] = list(matched)
        details["missing"] = [s for s in job_soft if s not in cv_soft]
        
        return score, details
    
    def _identify_critical_gaps(self, requirements: List[Dict], cv_lower: str,
                                profile: Dict) -> List[str]:
        """Identify critical gaps that may cause auto-rejection"""
        gaps = []
        
        for req in requirements:
            if req["type"] == "education":
                if "bachelor" in req["requirement"].lower():
                    if not any(x in cv_lower for x in ["bachelor", "b.com", "commerce", "business"]):
                        gaps.append(f"Missing: Bachelor's degree (or equivalent)")
            
            if req["type"] == "certification":
                certs = [c.lower() for c in profile.get('certifications', [])]
                cert_name = req["requirement"].lower()
                if not any(cert_name[:4] in c[:4] for c in certs if len(c) >= 4):
                    gaps.append(f"Missing: {req['requirement']}")
        
        return gaps
    
    def _identify_high_priority_gaps(self, keywords: List[Dict], cv_lower: str,
                                    job_lower: str) -> List[Dict]:
        """Identify keywords appearing 5+ times in job but missing in CV"""
        high_priority = []
        
        for kw in keywords:
            if kw["count"] >= 5 and kw["term"] not in cv_lower:
                high_priority.append({
                    "keyword": kw["term"],
                    "frequency": kw["count"],
                    "impact": "10-15 points",
                    "strategy": f"Add '{kw['term']}' to 2-3 bullet points"
                })
        
        return high_priority[:5]
    
    def _identify_medium_priority_gaps(self, keywords: List[Dict], cv_lower: str,
                                      job_lower: str) -> List[Dict]:
        """Identify keywords appearing 2-4 times in job"""
        medium_priority = []
        
        for kw in keywords:
            if 2 <= kw["count"] <= 4 and kw["term"] not in cv_lower:
                medium_priority.append({
                    "keyword": kw["term"],
                    "frequency": kw["count"],
                    "impact": "5-10 points",
                    "strategy": f"Add to 1-2 relevant bullet points"
                })
        
        return medium_priority[:5]
    
    def _identify_low_priority_gaps(self, keywords: List[Dict], cv_lower: str) -> List[Dict]:
        """Identify nice-to-have keywords"""
        low_priority = []
        
        for kw in keywords:
            if kw["count"] == 1 and kw["term"] not in cv_lower:
                low_priority.append({
                    "keyword": kw["term"],
                    "frequency": 1,
                    "impact": "1-5 points",
                    "strategy": f"Add to skills section if relevant"
                })
        
        return low_priority[:5]
    
    def _generate_optimization_strategy(self, job_posting: str, keywords: List[Dict],
                                       hard_requirements: List[Dict],
                                       critical_gaps: List[str],
                                       high_priority: List[Dict],
                                       medium_priority: List[Dict],
                                       profile: Dict) -> Dict:
        """Generate section-by-section optimization strategy"""
        
        strategy = {
            "professional_summary": {
                "current_issues": [],
                "add_keywords": [],
                "reframe_as": []
            },
            "core_competencies": {
                "missing_terms": [],
                "add_these": [],
                "format": "Tag cloud or bullet list"
            },
            "professional_experience": {
                "role_updates": [],
                "bullet_improvements": []
            },
            "education_certifications": {
                "gaps": [],
                "workarounds": [],
                "recommendations": []
            }
        }
        
        # Professional summary strategy
        summary_keywords = [k["term"] for k in keywords[:5] if k["term"] not in profile.get('summary', '').lower()]
        strategy["professional_summary"]["add_keywords"] = summary_keywords[:3]
        strategy["professional_summary"]["reframe_as"] = [
            "Open with role-specific achievement",
            "Include industry keywords naturally",
            "Quantify impact in opening sentence"
        ]
        
        # Core competencies
        missing = [k["term"] for k in keywords[:10] if k["term"] not in profile.get('summary', '').lower()]
        strategy["core_competencies"]["missing_terms"] = missing[:5]
        strategy["core_competencies"]["add_these"] = [
            kw["term"] for kw in keywords[:5] 
            if kw["term"] not in str(profile.get('core_skills', {}))
        ]
        
        # Experience bullets
        for exp in profile.get('experience', [])[:2]:
            strategy["professional_experience"]["role_updates"].append({
                "role": exp.get('title', ''),
                "add_keywords": [k["term"] for k in keywords[:3]]
            })
        
        # Education/certifications workarounds
        for gap in critical_gaps:
            if "degree" in gap.lower():
                strategy["education_certifications"]["workarounds"].append(
                    "Highlight relevant coursework if new graduate"
                )
            if "certification" in gap.lower():
                strategy["education_certifications"]["recommendations"].append(
                    f"Consider obtaining {gap.replace('Missing: ', '')} if time permits"
                )
        
        return strategy
    
    def _generate_optimized_cv(self, profile: Dict, strategy: Dict,
                              job_posting: str) -> str:
        """Generate optimized CV text"""
        
        optimized = f"""
================================================================================
OPTIMIZED CV - {profile.get('title', 'Professional')}
================================================================================

PROFESSIONAL SUMMARY
--------------------------------------------------------------------------------
{self._optimize_summary(profile.get('summary', ''), strategy, job_posting)}

CORE COMPETENCIES
--------------------------------------------------------------------------------
{self._optimize_skills(profile, strategy)}

PROFESSIONAL EXPERIENCE
--------------------------------------------------------------------------------
"""
        for exp in profile.get('experience', []):
            optimized += f"""
{exp.get('title', '')}
{exp.get('company', '')} | {exp.get('period', '')} | {exp.get('location', '')}

{self._optimize_bullets(exp.get('achievements', []), strategy, job_posting)}
"""
        
        optimized += f"""
EDUCATION
--------------------------------------------------------------------------------
"""
        for edu in profile.get('education', []):
            optimized += f"{edu.get('degree', '')} | {edu.get('institution', edu.get('school', ''))} | {edu.get('year', '')}\n"
        
        optimized += f"""
CERTIFICATIONS
--------------------------------------------------------------------------------
"""
        for cert in profile.get('certifications', []):
            optimized += f"• {cert}\n"
        
        return optimized
    
    def _optimize_summary(self, current_summary: str, strategy: Dict,
                         job_posting: str) -> str:
        """Optimize professional summary with keywords"""
        keywords_to_add = strategy.get("professional_summary", {}).get("add_keywords", [])[:3]
        
        optimized = current_summary
        if keywords_to_add:
            # Add keywords naturally at end
            keyword_phrase = ", ".join(keywords_to_add)
            optimized = f"{optimized.strip()} Expert in {keyword_phrase}."
        
        return optimized
    
    def _optimize_skills(self, profile: Dict, strategy: Dict) -> str:
        """Optimize skills section"""
        skills_text = []
        
        # Add all core skills
        for category, skills in profile.get('core_skills', {}).items():
            for skill in skills[:5]:
                skills_text.append(f"• {skill}")
        
        # Add missing keywords
        missing = strategy.get("core_competencies", {}).get("add_these", [])[:5]
        for m in missing:
            skills_text.append(f"• {m}")
        
        return "\n".join(skills_text)
    
    def _optimize_bullets(self, achievements: List[str], strategy: Dict,
                         job_posting: str) -> str:
        """Optimize achievement bullets with keywords"""
        optimized = []
        
        for i, ach in enumerate(achievements[:5]):
            optimized.append(f"• {ach}")
        
        # Add keyword-rich achievements based on job keywords
        job_keywords = [k["term"] for k in self._extract_keywords(job_posting)[:3]]
        for kw in job_keywords[:2]:
            optimized.append(f"• Strategic {kw} initiatives driving operational excellence")
        
        return "\n".join(optimized)
    
    def _calculate_projected_score(self, current_score: int, critical_gaps: List[str],
                                   high_priority: List[Dict],
                                   medium_priority: List[Dict]) -> int:
        """Calculate projected new score after optimization"""
        
        # If critical gaps exist, can't reach 90+
        if critical_gaps:
            base_projection = 75
        else:
            base_projection = 85
        
        # Add points for high priority gaps that can be fixed
        base_projection += len(high_priority) * 5
        base_projection += len(medium_priority) * 3
        
        return min(base_projection, 95)
    
    def _generate_recommendations(self, critical_gaps: List[str],
                                  high_priority: List[Dict],
                                  medium_priority: List[Dict],
                                  projected: int,
                                  current: int) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        improvement = projected - current
        
        if critical_gaps:
            recommendations.append(
                f"CRITICAL: Address missing requirements ({len(critical_gaps)} gaps) - "
                "these may trigger auto-rejection"
            )
        
        if high_priority:
            rec = f"Add {len(high_priority)} high-frequency keywords to experience section"
            recommendations.append(rec)
        
        if medium_priority:
            rec = f"Add {len(medium_priority)} medium-frequency keywords to boost score"
            recommendations.append(rec)
        
        if projected >= 90:
            recommendations.append(
                f"✓ Optimization achieves {projected}+ score with current credentials"
            )
        else:
            recommendations.append(
                f"To reach 90+: Consider obtaining missing certifications or credentials"
            )
        
        return recommendations
    
    def format_analysis(self, analysis: ATSAnalysis, job_title: str, company: str) -> str:
        """Format analysis in ADHAM's structured output"""
        
        output = f"""
================================================================================
                    ADHAM ATS OPTIMIZATION ANALYSIS
================================================================================

JOB: {job_title} at {company}
DATE: Analysis completed

================================================================================
                    📊 CURRENT ATS SCORE: {analysis.score}/100
================================================================================

SCORE BREAKDOWN:
--------------------------------------------------------------------------------
• Hard Requirements Match:     {analysis.score_breakdown["Hard Requirements"]["score"]}/30
• Keyword Density:            {analysis.score_breakdown["Keyword Density"]["score"]}/25
• Experience Relevance:       {analysis.score_breakdown["Experience Relevance"]["score"]}/20
• Quantified Impact:          {analysis.score_breakdown["Quantified Impact"]["score"]}/15
• Soft Skills & Culture:      {analysis.score_breakdown["Soft Skills & Culture"]["score"]}/10

Match Rate: {analysis.score_breakdown["Keyword Density"].get("match_rate", "N/A")}
"""
        
        # Critical gaps
        if analysis.critical_gaps:
            output += f"""
================================================================================
                    🚨 CRITICAL GAPS (Auto-Rejection Risk)
================================================================================

The following requirements are MISSING from your CV:

"""
            for gap in analysis.critical_gaps:
                output += f"• {gap}\n"
            
            output += """
Impact: These may trigger automatic ATS rejection.
"""
        
        # High priority gaps
        if analysis.high_priority_gaps:
            output += f"""
================================================================================
                    ⚠️ HIGH PRIORITY GAPS (10-15 point impact)
================================================================================

Keywords appearing 5+ times in job posting but MISSING from CV:

"""
            for gap in analysis.high_priority_gaps:
                output += f"• '{gap['keyword']}' ({gap['frequency']}x in job posting)\n"
                output += f"  Strategy: {gap['strategy']}\n\n"
        
        # Medium priority gaps
        if analysis.medium_priority_gaps:
            output += f"""
================================================================================
                    📋 MEDIUM PRIORITY GAPS (5-10 point impact)
================================================================================

Keywords appearing 2-4 times in job posting:

"""
            for gap in analysis.medium_priority_gaps:
                output += f"• '{gap['keyword']}' ({gap['frequency']}x in job posting)\n"
                output += f"  Strategy: {gap['strategy']}\n\n"
        
        # Projected score
        output += f"""
================================================================================
                    📈 PROJECTED NEW SCORE: {analysis.projected_new_score}/100
================================================================================

Improvement: +{analysis.projected_new_score - analysis.score} points

TO REACH 90+ SCORE:
"""
        for i, rec in enumerate(analysis.recommendations, 1):
            output += f"{i}. {rec}\n"
        
        output += f"""
================================================================================
                         OPTIMIZED CV
================================================================================

{analysis.optimized_cv}

================================================================================
                    END OF ADHAM ANALYSIS
================================================================================
"""
        
        return output


# Singleton instance
adham_analyzer = ADHAMAnalyzer()


if __name__ == "__main__":
    # Test with sample data
    print("Testing ADHAM ATS Analyzer...")
    
    job_posting = """
    Chief Technology Officer - Smart Metering Programme
    
    Talan is seeking a CTO to lead our Smart Metering Programme in Abu Dhabi.
    
    Requirements:
    - 15+ years in technology leadership
    - Experience with AMI architectures and smart metering
    - Strong background in IoT and enterprise integration
    - Strategic leadership and vendor management
    - MBA or equivalent preferred
    - PMP certification a plus
    
    Responsibilities:
    - Lead technical strategy and architecture
    - Oversee technology roadmap
    - Ensure cybersecurity and scalability
    - Manage vendor relationships
    - Guide technical teams across delivery streams
    """
    
    cv_text = """
    Ahmed Nasr
    PMO & AI Automation Leader
    
    Experience:
    - Acting PMO & Regional Engagement Lead at TopMed - Saudi German Hospital Group
    - Digital Transformation Consultant at AN & Co. Consulting
    - Senior Program Manager at Intel
    - Program Manager at Microsoft
    
    Achievements:
    - Led $25M transformation initiative
    - 40% efficiency gains through AI
    - Built and led teams of 50+ professionals
    """
    
    from cv_optimizer import ProfileDatabase
    profile = ProfileDatabase().data
    
    analysis = adham_analyzer.analyze(job_posting, cv_text, profile)
    
    print(adham_analyzer.format_analysis(analysis, "CTO Smart Metering", "Talan"))
