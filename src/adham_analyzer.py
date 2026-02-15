#!/usr/bin/env python3
"""
ADHAM - Enhanced ATS Optimization Engine v2.0
Advanced scoring with analogous experience, keyword criticality, and job-specific requirements
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import Counter


@dataclass
class ATSAnalysis:
    """Complete ATS analysis result - Enhanced Framework"""
    score: int
    score_breakdown: Dict
    critical_gaps: List[str]
    high_priority_gaps: List[Dict]
    medium_priority_gaps: List[Dict]
    low_priority_gaps: List[Dict]
    analogous_experience: List[Dict]
    optimization_strategy: Dict
    optimized_cv: str
    projected_new_score: int
    recommendations: List[str]


# Analogous Experience Mappings
ANALOGOUS_MAPPINGS = {
    # Smart Metering / AMI mappings
    "smart metering": [
        ("IoT device networks", 0.70),
        ("HealthTech monitoring systems", 0.70),
        ("Real-time sensor networks", 0.80),
        ("Industrial automation", 0.60),
    ],
    "ami": [
        ("IoT device networks", 0.70),
        ("Healthcare monitoring systems", 0.70),
        ("Real-time sensor networks", 0.80),
        ("Industrial IoT", 0.65),
    ],
    "metering": [
        ("Monitoring systems", 0.70),
        ("Sensor networks", 0.75),
        ("Data collection systems", 0.70),
        ("Utility systems", 0.80),
    ],
    # HES mappings
    "head-end system": [
        ("Command centers", 0.70),
        ("Central monitoring platforms", 0.80),
        ("SCADA systems", 0.90),
        ("Network operations centers", 0.70),
    ],
    "hes": [
        ("Command centers", 0.70),
        ("Central monitoring platforms", 0.80),
        ("SCADA systems", 0.90),
        ("Network operations centers", 0.70),
    ],
    # MDMS mappings
    "meter data management": [
        ("Enterprise data warehouses", 0.70),
        ("Real-time analytics platforms", 0.70),
        ("Big data processing systems", 0.60),
        ("Healthcare EDW systems", 0.75),
    ],
    "mdms": [
        ("Enterprise data warehouses", 0.70),
        ("Real-time analytics platforms", 0.70),
        ("Big data processing systems", 0.60),
        ("Healthcare EDW systems", 0.75),
    ],
    # Enterprise Integration
    "enterprise integration": [
        ("API management", 0.80),
        ("Middleware platforms", 0.80),
        ("System integration projects", 0.90),
        ("ESB implementations", 0.85),
    ],
    "api": [
        ("Integration platforms", 0.75),
        ("System integration", 0.80),
        ("Platform architecture", 0.70),
    ],
    # Healthcare specific
    "healthcare": [
        ("HealthTech", 1.0),
        ("Hospital systems", 0.90),
        ("Clinical systems", 0.85),
        ("Patient data systems", 0.85),
    ],
    "hospital": [
        ("Healthcare operations", 0.90),
        ("Clinical management", 0.85),
        ("Patient care systems", 0.80),
        ("Medical systems", 0.85),
    ],
    # Digital Transformation
    "digital transformation": [
        ("Digital modernization", 1.0),
        ("Technology transformation", 0.95),
        ("Business transformation", 0.85),
        ("Operational transformation", 0.85),
    ],
    # PMO
    "pmo": [
        ("Project management office", 1.0),
        ("Program management", 0.95),
        ("Project governance", 0.90),
        ("Portfolio management", 0.90),
    ],
    # ERP
    "erp": [
        ("Enterprise systems", 0.95),
        ("SAP implementation", 0.90),
        ("System integration", 0.85),
        ("Business systems", 0.85),
    ],
}


class ADHAMAnalyzer:
    """
    ADHAM - Advanced ATS Optimization Engine v2.0
    
    Enhanced Scoring Framework (100 points):
    1. Hard Requirements: 30 points (education, experience, certifications)
    2. Keyword Density: 25 points (weighted by criticality)
    3. Experience Relevance: 20 points (includes analogous credit)
    4. Quantified Impact: 15 points (metrics counting)
    5. Soft Skills & Culture: 10 points
    """
    
    def __init__(self):
        self.common_stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during'
        }
    
    def analyze(self, job_posting: str, cv_text: str, profile: Dict) -> ATSAnalysis:
        """
        Complete ATS analysis using enhanced framework
        """
        job_lower = job_posting.lower()
        cv_lower = cv_text.lower()
        
        # Step 1: Extract job requirements
        hard_requirements = self._extract_hard_requirements(job_posting)
        keywords = self._extract_weighted_keywords(job_posting)
        soft_skills = self._extract_soft_skills(job_posting)
        seniority = self._extract_seniority(job_posting)
        
        # Step 2: Score each component
        hard_score, hard_details = self._score_hard_requirements(
            hard_requirements, cv_lower, profile
        )
        keyword_score, keyword_details = self._score_keyword_density(
            keywords, cv_lower
        )
        exp_score, exp_details, analogous = self._score_experience_relevance(
            job_posting, cv_lower, seniority
        )
        quantified_score, quantified_details = self._score_quantified_achievements(cv_text)
        soft_score, soft_details = self._score_soft_skills(soft_skills, cv_lower)
        
        # Calculate total
        total_score = hard_score + keyword_score + exp_score + quantified_score + soft_score
        
        # Identify gaps
        critical = self._identify_critical_gaps(hard_requirements, cv_lower, profile)
        high_priority = self._identify_high_priority_gaps(keywords, cv_lower)
        medium_priority = self._identify_medium_priority_gaps(keywords, cv_lower)
        low_priority = self._identify_low_priority_gaps(keywords, cv_lower)
        
        # Generate optimization
        strategy = self._generate_optimization_strategy(
            keywords, critical, high_priority, medium_priority, analogous, profile
        )
        optimized_cv = self._generate_optimized_cv(profile, strategy, job_posting)
        projected = self._calculate_projected_score(total_score, critical, high_priority, medium_priority)
        recommendations = self._generate_recommendations(critical, high_priority, medium_priority, projected)
        
        return ATSAnalysis(
            score=total_score,
            score_breakdown={
                "Hard Requirements": {"score": hard_score, "max": 30, **hard_details},
                "Keyword Density": {"score": keyword_score, "max": 25, **keyword_details},
                "Experience Relevance": {"score": exp_score, "max": 20, **exp_details},
                "Quantified Impact": {"score": quantified_score, "max": 15, **quantified_details},
                "Soft Skills & Culture": {"score": soft_score, "max": 10, **soft_details}
            },
            critical_gaps=critical,
            high_priority_gaps=high_priority,
            medium_priority_gaps=medium_priority,
            low_priority_gaps=low_priority,
            analogous_experience=analogous,
            optimization_strategy=strategy,
            optimized_cv=optimized_cv,
            projected_new_score=projected,
            recommendations=recommendations
        )
    
    # ==================== HARD REQUIREMENTS (30 points) ====================
    
    def _extract_hard_requirements(self, text: str) -> Dict:
        """Extract must-have requirements from job posting"""
        requirements = {
            "education": {"required": None, "type": None},
            "experience": {"years": None, "field": None},
            "certifications": [],
            "skills": []
        }
        
        # Education extraction
        if re.search(r"bachelor['s]?\s*(?:degree|dgree)?", text.lower()):
            requirements["education"]["type"] = "bachelor"
        if re.search(r"master['s]?\s*(?:degree|mba)?", text.lower()):
            requirements["education"]["type"] = "master"
        if re.search(r"mba", text.lower()):
            requirements["education"]["type"] = "mba"
        if re.search(r"phd|doctorate", text.lower()):
            requirements["education"]["type"] = "phd"
        
        # Years of experience
        years_match = re.search(r"(\d+)\+?\s*(?:years?|yrs?)", text.lower())
        if years_match:
            requirements["experience"]["years"] = int(years_match.group(1))
        
        # Experience field
        fields = ["healthcare", "healthtech", "fintech", "technology", "erp", "sap", 
                  "smart metering", "ami", "utilities", "energy"]
        for field in fields:
            if field in text.lower():
                requirements["experience"]["field"] = field
                break
        
        # Certifications
        certs = ["pmp", "itil", "csm", "six sigma", "cissp", "cissp", "mba", "cbap"]
        for cert in certs:
            if cert in text.lower():
                requirements["certifications"].append(cert)
        
        return requirements
    
    def _score_hard_requirements(self, requirements: Dict, cv_lower: str, 
                                  profile: Dict) -> Tuple[int, Dict]:
        """Score hard requirements (max 30 points)"""
        score = 0
        details = {"education": {}, "experience": {}, "certifications": {}}
        
        # Education (max 10 points)
        edu_type = requirements.get("education", {}).get("type")
        if edu_type:
            cv_education = " ".join([
                e.get("degree", "").lower() 
                for e in profile.get("education", [])
            ])
            
            if edu_type == "bachelor":
                if "bachelor" in cv_education or "bsc" in cv_education:
                    score += 10
                    details["education"] = {"score": 10, "status": "Exact match"}
                elif "mba" in cv_education or "master" in cv_education:
                    score += 8
                    details["education"] = {"score": 8, "status": "Higher degree"}
                else:
                    score += 5
                    details["education"] = {"score": 5, "status": "Compensating credentials"}
            
            elif edu_type in ["master", "mba"]:
                if "mba" in cv_education or "master" in cv_education:
                    score += 10
                    details["education"] = {"score": 10, "status": "Exact match"}
                elif "bachelor" in cv_education:
                    score += 6
                    details["education"] = {"score": 6, "status": "Lower degree + certs"}
                else:
                    score += 3
                    details["education"] = {"score": 3, "status": "No degree match"}
        else:
            score += 5
            details["education"] = {"score": 5, "status": "Not specified"}
        
        # Experience (max 10 points)
        req_years = requirements.get("experience", {}).get("years")
        req_field = requirements.get("experience", {}).get("field")
        total_exp = profile.get("total_experience_years", 0)
        
        if req_years:
            if total_exp >= req_years:
                score += 10
                details["experience"] = {
                    "score": 10, 
                    "status": f"{total_exp}yrs >= {req_years}yrs required"
                }
            elif total_exp >= req_years * 0.7:
                score += 7
                details["experience"] = {
                    "score": 7, 
                    "status": f"{total_exp}yrs (analogous credit)"
                }
            else:
                score += 3
                details["experience"] = {
                    "score": 3, 
                    "status": f"Insufficient: {total_exp}yrs"
                }
        else:
            score += 5
            details["experience"] = {"score": 5, "status": "Not specified"}
        
        # Certifications (max 10 points)
        req_certs = requirements.get("certifications", [])
        cv_certs = [c.lower() for c in profile.get("certifications", [])]
        
        if req_certs:
            matches = sum(1 for c in req_certs if any(c[:4] in cert[:4] for cert in cv_certs))
            match_rate = matches / len(req_certs)
            
            if match_rate >= 1.0:
                score += 10
                details["certifications"] = {"score": 10, "status": "All required"}
            elif match_rate >= 0.75:
                score += 7
                details["certifications"] = {"score": 7, "status": "75%+ matched"}
            elif match_rate >= 0.5:
                score += 5
                details["certifications"] = {"score": 5, "status": "50%+ matched"}
            else:
                score += 2
                details["certifications"] = {"score": 2, "status": "<50% matched"}
        else:
            score += 5
            details["certifications"] = {"score": 5, "status": "Not specified"}
        
        return min(score, 30), details
    
    # ==================== KEYWORD DENSITY (25 points) ====================
    
    def _extract_weighted_keywords(self, text: str) -> List[Dict]:
        """Extract keywords with context weights"""
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        filtered = [w for w in words if w not in self.common_stopwords]
        counts = Counter(filtered)
        
        text_lower = text.lower()
        keywords = []
        
        for word, count in counts.most_common(50):
            # Weight 3: CRITICAL (in title, "required", technical specs)
            weight = 1
            
            if (word in text_lower and 
                any(x in text_lower[:text_lower.find(word)+100] 
                    for x in ["required", "must have", "essential"])):
                weight = 3
            
            # Title proximity bonus
            lines = text_lower.split('\n')
            for line in lines[:5]:
                if word in line and len(line) < 100:  # Likely title
                    weight = 3
                    break
            
            # High frequency bonus
            if count >= 5:
                weight = max(weight, 2)
            elif count >= 3:
                weight = max(weight, 1)
            
            keywords.append({
                "term": word,
                "count": count,
                "weight": weight,  # 3=Critical, 2=High, 1=Medium
                "category": self._categorize_keyword(word)
            })
        
        # Sort by weight then count
        keywords.sort(key=lambda x: (x["weight"], x["count"]), reverse=True)
        
        return keywords[:30]
    
    def _categorize_keyword(self, word: str) -> str:
        """Categorize keyword type"""
        categories = {
            "technical": ["sap", "erp", "api", "cloud", "ai", "ml", "data", "analytics"],
            "leadership": ["leadership", "management", "strategy", "stakeholder", "team"],
            "domain": ["healthcare", "fintech", "metering", "utilities", "energy"],
            "process": ["pmo", "agile", "scrum", "transformation", "implementation"]
        }
        
        for cat, terms in categories.items():
            if any(t in word for t in terms):
                return cat
        return "general"
    
    def _score_keyword_density(self, keywords: List[Dict], cv_lower: str) -> Tuple[int, Dict]:
        """Score keyword matching with weights (max 25 points)"""
        critical_found = 0
        high_found = 0
        medium_found = 0
        critical_total = len([k for k in keywords if k["weight"] == 3])
        high_total = len([k for k in keywords if k["weight"] == 2])
        medium_total = len([k for k in keywords if k["weight"] == 1])
        
        for kw in keywords:
            if kw["term"] in cv_lower:
                cv_count = cv_lower.count(kw["term"])
                capped_count = min(cv_count, 3)
                
                if kw["weight"] == 3:
                    critical_found += capped_count
                elif kw["weight"] == 2:
                    high_found += capped_count
                else:
                    medium_found += capped_count
        
        # Calculate score
        max_critical = critical_total * 3 if critical_total else 1
        max_high = high_total * 2 if high_total else 1
        max_medium = medium_total * 1 if medium_total else 1
        
        critical_score = min((critical_found / max_critical) * 15, 15)
        high_score = min((high_found / max_high) * 7, 7)
        medium_score = min((medium_found / max_medium) * 3, 3)
        
        total = min(critical_score + high_score + medium_score, 25)
        
        return int(total), {
            "critical": {"found": critical_found, "total": critical_total},
            "high": {"found": high_found, "total": high_total},
            "medium": {"found": medium_found, "total": medium_total}
        }
    
    # ==================== EXPERIENCE RELEVANCE (20 points) ====================
    
    def _extract_seniority(self, text: str) -> Dict:
        """Extract seniority requirements"""
        seniority = {"level": "mid", "title": None, "scope": {}}
        
        text_lower = text.lower()
        
        if any(x in text_lower for x in ["chief", "cto", "cio", "cfo", "ceo"]):
            seniority["level"] = "executive"
            seniority["title"] = "C-suite"
        elif any(x in text_lower for x in ["vp", "vice president", "senior vice president"]):
            seniority["level"] = "vp"
            seniority["title"] = "VP"
        elif any(x in text_lower for x in ["director", "head of"]):
            seniority["level"] = "director"
            seniority["title"] = "Director"
        elif any(x in text_lower for x in ["senior", "sr."]):
            seniority["level"] = "senior"
            seniority["title"] = "Senior"
        
        return seniority
    
    def _score_experience_relevance(self, job_posting: str, cv_lower: str,
                                    seniority: Dict) -> Tuple[int, Dict, List]:
        """Score experience with analogous mapping (max 20 points)"""
        score = 0
        analogous = []
        
        # Industry match
        job_industries = self._extract_industries(job_posting)
        cv_industries = self._extract_industries(cv_lower)
        
        industry_score = 0
        for job_ind in job_industries:
            if job_ind in cv_industries:
                industry_score = 10
                break
            else:
                # Check analogous mapping
                for cv_ind in cv_industries:
                    analog_score = self._get_analogy_score(job_ind, cv_ind)
                    if analog_score >= 0.70:
                        industry_score = max(industry_score, int(analog_score * 10))
                        analogous.append({
                            "cv_experience": cv_ind,
                            "job_requirement": job_ind,
                            "credit": f"{int(analog_score * 100)}%"
                        })
                        break
        
        # Seniority alignment
        seniority_score = self._score_seniority(seniority, cv_lower)
        
        total = min(industry_score + seniority_score, 20)
        
        return total, {
            "industry_score": industry_score,
            "seniority_score": seniority_score,
            "industries_found": cv_industries
        }, analogous
    
    def _extract_industries(self, text: str) -> List[str]:
        """Extract industry keywords"""
        industries = []
        keywords = [
            "healthcare", "healthtech", "fintech", "technology", "utilities", 
            "energy", "metering", "erp", "sap", "hospital", "medical",
            "digital transformation", "iot", "smart grid", "ami"
        ]
        
        for kw in keywords:
            if kw in text.lower():
                industries.append(kw)
        
        return industries
    
    def _get_analogy_score(self, target: str, source: str) -> float:
        """Get analogous experience credit score"""
        target_lower = target.lower()
        source_lower = source.lower()
        
        # Direct mapping
        if target_lower == source_lower:
            return 1.0
        
        # Check predefined mappings
        for key, mappings in ANALOGOUS_MAPPINGS.items():
            if key in target_lower or key in source_lower:
                for mapped_term, credit in mappings:
                    if mapped_term in source_lower or mapped_term in target_lower:
                        return credit
        
        return 0.0
    
    def _score_seniority(self, seniority: Dict, cv_lower: str) -> int:
        """Score seniority alignment"""
        cv_titles = cv_lower
        
        if seniority["level"] == "executive":
            if any(x in cv_titles for x in ["chief", "cto", "cio", "vp", "director", "head"]):
                return 10
            elif any(x in cv_titles for x in ["senior manager", "lead", "principal"]):
                return 7
            else:
                return 5
        
        elif seniority["level"] == "director":
            if "director" in cv_titles or "head" in cv_titles:
                return 10
            elif "vp" in cv_titles or "chief" in cv_titles:
                return 10
            elif "senior manager" in cv_titles or "lead" in cv_titles:
                return 8
            else:
                return 6
        
        else:  # mid/senior
            return 8
        
        return 5
    
    # ==================== QUANTIFIED IMPACT (15 points) ====================
    
    def _score_quantified_achievements(self, cv_text: str) -> Tuple[int, Dict]:
        """Score quantified achievements (max 15 points)"""
        patterns = [
            r'\$[\d,]+(?:\s*(?:million|billion|m))?',
            r'\d+(?:\.\d+)?\s*%',
            r'\d+\s*(?:million|billion|m)',
            r'\d+\s*(?:team|people|resources|staff)',
            r'\d+x\s*(?:growth|increase|improvement)',
            r'\d+\s*(?:months?|years?)\s*(?:reduction|savings|improvement)',
        ]
        
        metrics = []
        for pattern in patterns:
            matches = re.findall(pattern, cv_text.lower())
            metrics.extend(matches)
        
        score = min(len(metrics) * 3, 15)
        
        return score, {"metrics_found": len(metrics), "examples": metrics[:5]}
    
    # ==================== SOFT SKILLS (10 points) ====================
    
    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills from job posting"""
        skills = []
        keywords = [
            "leadership", "communication", "collaboration", "strategic", 
            "stakeholder", "problem-solving", "analytical", "innovative",
            "team player", "results-driven", "cross-functional", "agile",
            "adaptable", "influential", "negotiation", "change management"
        ]
        
        text_lower = text.lower()
        for skill in keywords:
            if skill in text_lower:
                skills.append(skill)
        
        return skills
    
    def _score_soft_skills(self, required_skills: List[str], cv_lower: str) -> Tuple[int, Dict]:
        """Score soft skills match (max 10 points)"""
        matched = [s for s in required_skills if s in cv_lower]
        score = min(len(matched) * 2, 10)
        
        return score, {"matched": matched, "missing": [s for s in required_skills if s not in cv_lower]}
    
    # ==================== GAP IDENTIFICATION ====================
    
    def _identify_critical_gaps(self, requirements: Dict, cv_lower: str, 
                                profile: Dict) -> List[str]:
        """Identify gaps that may cause auto-rejection"""
        gaps = []
        
        # Check education
        edu_type = requirements.get("education", {}).get("type")
        if edu_type:
            cv_edu = " ".join([e.get("degree", "").lower() for e in profile.get("education", [])])
            if "bachelor" in edu_type and not any(x in cv_edu for x in ["bachelor", "bsc", "b.com"]):
                gaps.append(f"Missing: Bachelor's degree (Required)")
            if "mba" in edu_type and "mba" not in cv_edu and "master" not in cv_edu:
                gaps.append(f"Missing: MBA (Preferred/Required)")
        
        # Check experience
        req_years = requirements.get("experience", {}).get("years")
        total_exp = profile.get("total_experience_years", 0)
        if req_years and total_exp < req_years * 0.7:
            gaps.append(f"Experience gap: {req_years}+ years required, have {total_exp}")
        
        # Check certifications
        req_certs = requirements.get("certifications", [])
        cv_certs = [c.lower() for c in profile.get("certifications", [])]
        for cert in req_certs:
            if not any(cert[:4] in c[:4] for c in cv_certs):
                gaps.append(f"Missing certification: {cert.upper()}")
        
        return gaps
    
    def _identify_high_priority_gaps(self, keywords: List[Dict], cv_lower: str) -> List[Dict]:
        """Identify critical keywords (weight 3) missing from CV"""
        gaps = []
        for kw in keywords:
            if kw["weight"] == 3 and kw["term"] not in cv_lower:
                gaps.append({
                    "keyword": kw["term"],
                    "frequency": kw["count"],
                    "impact": "10-15 points",
                    "strategy": f"MUST add '{kw['term']}' to Summary + 2 bullets"
                })
        return gaps[:5]
    
    def _identify_medium_priority_gaps(self, keywords: List[Dict], cv_lower: str) -> List[Dict]:
        """Identify high-frequency keywords (weight 2) missing"""
        gaps = []
        for kw in keywords:
            if kw["weight"] == 2 and kw["term"] not in cv_lower:
                gaps.append({
                    "keyword": kw["term"],
                    "frequency": kw["count"],
                    "impact": "5-10 points",
                    "strategy": f"Add to 1-2 relevant bullet points"
                })
        return gaps[:5]
    
    def _identify_low_priority_gaps(self, keywords: List[Dict], cv_lower: str) -> List[Dict]:
        """Identify medium-frequency keywords"""
        gaps = []
        for kw in keywords:
            if kw["weight"] == 1 and kw["term"] not in cv_lower:
                gaps.append({
                    "keyword": kw["term"],
                    "frequency": kw["count"],
                    "impact": "1-5 points",
                    "strategy": f"Add to skills section if relevant"
                })
        return gaps[:5]
    
    # ==================== OPTIMIZATION ====================
    
    def _generate_optimization_strategy(self, keywords: List[Dict], 
                                       critical: List[str],
                                       high: List[Dict], 
                                       medium: List[Dict],
                                       analogous: List[Dict],
                                       profile: Dict) -> Dict:
        """Generate section-by-section optimization strategy"""
        
        strategy = {
            "professional_summary": {
                "current_issues": [c for c in critical if "degree" in c.lower()],
                "keywords_to_add": [kw["term"] for kw in keywords[:5]],
                "positioning": "Lead with job title + critical keywords"
            },
            "experience_bullets": {
                "high_priority": [h["keyword"] for h in high[:3]],
                "analogous_to_highlight": analogous[:3],
                "format": "Action verb + metric + keyword"
            },
            "skills_section": {
                "missing_critical": [h["keyword"] for h in high],
                "suggested_additions": [m["keyword"] for m in medium[:5]]
            }
        }
        
        return strategy
    
    def _generate_optimized_cv(self, profile: Dict, strategy: Dict,
                              job_posting: str) -> str:
        """Generate optimized CV text"""
        
        optimized = f"""
{'='*80}
OPTIMIZED CV FOR ATS - {profile.get('name', 'Candidate')}
{'='*80}

PROFESSIONAL SUMMARY
--------------------------------------------------------------------------------
"""
        
        # Optimized summary with keywords
        summary_kw = strategy.get("professional_summary", {}).get("keywords_to_add", [])[:5]
        current_summary = profile.get("summary", "")
        
        if summary_kw:
            kw_phrase = ", ".join(summary_kw[:3])
            optimized += f"{current_summary}\n\nExpertise in: {kw_phrase}\n"
        
        optimized += """
CORE COMPETENCIES
--------------------------------------------------------------------------------
"""
        # Add missing keywords to skills
        skills = strategy.get("skills_section", {}).get("suggested_additions", [])
        for skill in skills[:10]:
            optimized += f"• {skill.title()}\n"
        
        optimized += """
PROFESSIONAL EXPERIENCE
--------------------------------------------------------------------------------
"""
        for exp in profile.get("experience", []):
            optimized += f"""
{exp.get('title', '')} | {exp.get('company', '')}
{exp.get('period', '')} | {exp.get('location', '')}

"""
            # Add keywords to achievements
            for ach in exp.get('achievements', []):
                optimized += f"• {ach}\n"
        
        return optimized
    
    def _calculate_projected_score(self, current: int, critical: List[str],
                                   high: List[Dict], medium: List[Dict]) -> int:
        """Calculate projected score after optimization"""
        
        # Base projection
        if critical:
            base = 70
        else:
            base = 80
        
        # Add points for fixable gaps
        base += len(high) * 8  # ~8 pts each
        base += len(medium) * 4  # ~4 pts each
        
        return min(base, 95)
    
    def _generate_recommendations(self, critical: List[str], high: List[Dict],
                                  medium: List[Dict], projected: int) -> List[str]:
        """Generate actionable recommendations"""
        
        recs = []
        
        if critical:
            recs.append(f"CRITICAL: Address {len(critical)} auto-rejection gaps")
        
        if high:
            recs.append(f"HIGH: Add {len(high)} critical keywords to Summary + bullets")
        
        if medium:
            recs.append(f"MEDIUM: Add {len(medium)} high-frequency keywords")
        
        recs.append(f"Projected score after optimization: {projected}/100")
        
        return recs
    
    def format_analysis(self, analysis: ATSAnalysis, job_title: str, company: str) -> str:
        """Format analysis in readable output"""
        
        output = f"""
{'='*80}
                    ADHAM ATS OPTIMIZATION ANALYSIS v2.0
{'='*80}

JOB: {job_title} at {company}

{'='*80}
                    📊 CURRENT ATS SCORE: {analysis.score}/100
{'='*80}

Score Breakdown:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Hard Requirements:          {analysis.score_breakdown['Hard Requirements']['score']}/30
Keyword Density:           {analysis.score_breakdown['Keyword Density']['score']}/25
Experience Relevance:      {analysis.score_breakdown['Experience Relevance']['score']}/20
Quantified Impact:         {analysis.score_breakdown['Quantified Impact']['score']}/15
Soft Skills & Culture:      {analysis.score_breakdown['Soft Skills & Culture']['score']}/10
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        if analysis.critical_gaps:
            output += f"""🚨 CRITICAL GAPS (Auto-Rejection Risk)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for gap in analysis.critical_gaps:
                output += f"• {gap}\n"
            output += "\n"
        
        if analysis.high_priority_gaps:
            output += f"""⚠️ HIGH PRIORITY GAPS (10-15 point impact)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Critical Keywords (Weight 3):
| Keyword     | Job Mentions | CV Mentions | Points Lost |
|-------------|--------------|-------------|-------------|
"""
            for gap in analysis.high_priority_gaps:
                output += f"| {gap['keyword']:<11} | {gap['frequency']:<12} | 0           | -9          |\n"
            output += "\n"
        
        if analysis.analogous_experience:
            output += f"""🎯 ANALOGOUS EXPERIENCE OPPORTUNITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for analog in analysis.analogous_experience:
                output += f"• CV: {analog['cv_experience']} ←→ Job: {analog['job_requirement']} ({analog['credit']})\n"
            output += "\n"
        
        output += f"""📈 PROJECTED SCORE: {analysis.projected_new_score}/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Improvement: +{analysis.projected_new_score - analysis.score} points

"""
        
        for rec in analysis.recommendations:
            output += f"• {rec}\n"
        
        return output


# Singleton instance
adham_analyzer = ADHAMAnalyzer()
