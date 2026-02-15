#!/usr/bin/env python3
"""
CV Optimizer Tool
Generates tailored CVs based on job descriptions with ATS scoring.
"""

import json
import re
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class JobRequirements:
    """Parsed job description requirements"""
    title: str
    company: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_years: int
    experience_level: str
    responsibilities: List[str]
    qualifications: List[str]
    keywords: List[str]
    raw_text: str

@dataclass
class CVSection:
    """A section of the CV"""
    title: str
    content: str
    priority: int

@dataclass
class TailoredCV:
    """Generated CV output"""
    job_title: str
    company: str
    sections: List[CVSection]
    ats_score: int
    match_analysis: Dict
    suggestions: List[str]
    generated_at: str

class ProfileDatabase:
    """Ahmed's master profile data"""
    
    def __init__(self):
        self.data = {
            "name": "Ahmed Nasr",
            "title": "PMO & AI Automation Leader",
            "location": "Egypt (Work: UAE, KSA)",
            "visa": "UAE Permanent Work Visa",
            "summary": "PMO & AI Automation Leader at Saudi German Hospital Group with 20+ years scaling digital transformation across FinTech and HealthTech sectors. Former Intel and Microsoft.",
            
            "contact": {
                "linkedin": "https://linkedin.com/in/ahmednasr",
                "github": "https://github.com/ahmednasr999",
                "newsletter": "https://linkedin.com/newsletters/an-fintech-weekly-newsletter-7342491220318818304",
                "consulting": "https://anco-consulting.com"
            },
            
            "certifications": [
                "MBA", "PMP", "CSM", "CSPO", "Lean Six Sigma", 
                "CBAP", "MCAD", "MCP"
            ],
            
            "core_skills": {
                "leadership": [
                    "PMO Leadership", "Program Management", "Digital Transformation",
                    "AI Strategy", "Operational Excellence", "Change Management",
                    "Team Leadership", "Stakeholder Management", "Executive Reporting"
                ],
                "technical": [
                    "AI Automation", "Machine Learning", "Healthcare IT", "FinTech Systems",
                    "Business Intelligence", "Data Analytics", "Cloud Platforms",
                    "System Integration", "API Management", "Process Automation"
                ],
                "healthcare": [
                    "HealthTech", "Hospital Operations", "Clinical Systems",
                    "Healthcare AI", "EMR/EHR Systems", "Healthcare Compliance",
                    "Patient Experience", "Healthcare Digital Transformation"
                ],
                "fintech": [
                    "Digital Banking", "Payment Systems", "Stablecoins",
                    "Financial Technology", "Banking Operations", "Risk Management",
                    "Regulatory Compliance", "Financial Analytics"
                ],
                "methodologies": [
                    "Agile", "Scrum", "Lean", "Six Sigma", "ITIL",
                    "Waterfall", "Hybrid PM", "DevOps", "CI/CD"
                ]
            },
            
            "experience": [
                {
                    "title": "Acting PMO & Regional Engagement Lead",
                    "company": "TopMed - Saudi German Hospital Group (SGH)",
                    "location": "KSA",
                    "period": "2024 - Present",
                    "duration_years": 1,
                    "sector": "HealthTech",
                    "achievements": [
                        "Lead AI automation initiatives across hospital operations, reducing processing time by 40%",
                        "Manage PMO function for digital transformation programs across regional hospitals",
                        "Oversee implementation of AI-driven clinical decision support systems",
                        "Drive operational excellence initiatives resulting in 25% efficiency gains",
                        "Build and lead cross-functional teams of 50+ professionals",
                        "Manage multi-million dollar technology budgets and vendor relationships"
                    ],
                    "skills_used": ["AI Automation", "PMO", "Healthcare IT", "Digital Transformation", "Team Leadership"]
                },
                {
                    "title": "Digital Transformation Consultant",
                    "company": "AN & Co. Consulting",
                    "location": "MENA Region",
                    "period": "2020 - Present",
                    "duration_years": 5,
                    "sector": "Consulting",
                    "achievements": [
                        "Advise healthcare and FinTech organizations on digital transformation strategy",
                        "Deliver AI automation solutions for operational efficiency",
                        "Lead change management programs for technology adoption",
                        "Published weekly FinTech newsletter with 1000+ subscribers"
                    ],
                    "skills_used": ["Consulting", "Digital Strategy", "AI", "FinTech", "Change Management"]
                },
                {
                    "title": "Senior Program Manager",
                    "company": "Intel",
                    "location": "Global",
                    "period": "2015 - 2020",
                    "duration_years": 5,
                    "sector": "Technology",
                    "achievements": [
                        "Led large-scale technology programs across multiple regions",
                        "Managed complex stakeholder ecosystems in enterprise environments",
                        "Delivered digital transformation initiatives on time and budget",
                        "Drove operational excellence in technology operations"
                    ],
                    "skills_used": ["Program Management", "Enterprise IT", "Digital Transformation", "Leadership"]
                },
                {
                    "title": "Program Manager",
                    "company": "Microsoft",
                    "location": "Global",
                    "period": "2010 - 2015",
                    "duration_years": 5,
                    "sector": "Technology",
                    "achievements": [
                        "Managed enterprise software development programs",
                        "Led cross-functional teams in agile and waterfall environments",
                        "Delivered solutions for Fortune 500 clients",
                        "Built expertise in cloud platforms and enterprise systems"
                    ],
                    "skills_used": ["Program Management", "Agile", "Cloud", "Enterprise Software", "Client Management"]
                }
            ],
            
            "education": [
                {
                    "degree": "MBA",
                    "field": "Business Administration",
                    "institution": "[University]",
                    "year": "[Year]"
                }
            ],
            
            "total_experience_years": 20,
            "sectors": ["HealthTech", "FinTech", "Technology", "Consulting"],
            "target_roles": [
                "VP Digital Transformation", "Director PMO", "Head of AI",
                "Chief Technology Officer", "VP Healthcare Technology",
                "Digital Transformation Leader", "AI Strategy Director"
            ]
        }
    
    def get_all_skills(self) -> List[str]:
        """Get flat list of all skills"""
        skills = []
        for category in self.data["core_skills"].values():
            skills.extend(category)
        return skills
    
    def get_sector_skills(self, sector: str) -> List[str]:
        """Get skills for a specific sector"""
        return self.data["core_skills"].get(sector.lower(), [])
    
    def get_relevant_experience(self, keywords: List[str]) -> List[Dict]:
        """Get experience entries matching keywords"""
        relevant = []
        for exp in self.data["experience"]:
            score = 0
            exp_text = " ".join([
                exp["title"], exp["company"], exp["sector"],
                " ".join(exp["skills_used"]),
                " ".join(exp["achievements"])
            ]).lower()
            
            for kw in keywords:
                if kw.lower() in exp_text:
                    score += 1
            
            if score > 0:
                relevant.append({**exp, "relevance_score": score})
        
        return sorted(relevant, key=lambda x: x["relevance_score"], reverse=True)


class JDParser:
    """Parse job descriptions to extract requirements"""
    
    # Keywords indicating requirements
    REQUIRED_INDICATORS = [
        "required", "must have", "essential", "necessary", "mandatory",
        "need to have", "required skills", "requirements", "qualifications"
    ]
    
    PREFERRED_INDICATORS = [
        "preferred", "nice to have", "desired", "beneficial", "plus",
        "advantageous", "ideal candidate", "bonus"
    ]
    
    EXPERIENCE_PATTERNS = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'(\d+)\+?\s*yrs?\s*(?:of\s*)?exp',
        r'experience\s*:\s*(\d+)\+?\s*years?',
        r'(\d+)\+?\s*years?\s*in\s*[\w\s]+'
    ]
    
    SKILL_KEYWORDS = [
        "python", "java", "javascript", "sql", "aws", "azure", "gcp",
        "machine learning", "ai", "artificial intelligence", "data science",
        "project management", "agile", "scrum", "leadership", "strategy",
        "healthcare", "fintech", "banking", "digital transformation",
        "pmo", "program management", "product management", "operations",
        "stakeholder management", "vendor management", "budget management",
        "change management", "process improvement", "six sigma", "lean",
        "cloud", "devops", "ci/cd", "api", "microservices",
        "analytics", "bi", "tableau", "power bi", "excel"
    ]
    
    def __init__(self):
        self.skill_patterns = [re.compile(r'\b' + re.escape(skill) + r'\b', re.I) 
                               for skill in self.SKILL_KEYWORDS]
    
    def parse(self, job_text: str, title: str = "", company: str = "") -> JobRequirements:
        """Parse a job description"""
        text_lower = job_text.lower()
        
        # Extract skills
        required_skills = self._extract_skills(job_text, self.REQUIRED_INDICATORS)
        preferred_skills = self._extract_skills(job_text, self.PREFERRED_INDICATORS)
        
        # Extract experience years
        experience_years = self._extract_experience_years(job_text)
        experience_level = self._determine_level(experience_years)
        
        # Extract responsibilities
        responsibilities = self._extract_responsibilities(job_text)
        
        # Extract qualifications
        qualifications = self._extract_qualifications(job_text)
        
        # Get all keywords
        keywords = self._extract_all_keywords(job_text)
        
        return JobRequirements(
            title=title,
            company=company,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            experience_years=experience_years,
            experience_level=experience_level,
            responsibilities=responsibilities,
            qualifications=qualifications,
            keywords=keywords,
            raw_text=job_text
        )
    
    def _extract_skills(self, text: str, indicators: List[str]) -> List[str]:
        """Extract skills from text sections marked by indicators"""
        skills = []
        text_lower = text.lower()
        
        # Find skill mentions throughout
        for skill in self.SKILL_KEYWORDS:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                skills.append(skill)
        
        return list(set(skills))
    
    def _extract_experience_years(self, text: str) -> int:
        """Extract required years of experience"""
        for pattern in self.EXPERIENCE_PATTERNS:
            matches = re.findall(pattern, text.lower())
            if matches:
                years = [int(m) if isinstance(m, str) and m.isdigit() else int(m[0]) 
                        for m in matches if (isinstance(m, str) and m.isdigit()) or isinstance(m, tuple)]
                if years:
                    return max(years)
        return 0
    
    def _determine_level(self, years: int) -> str:
        """Determine experience level from years"""
        if years >= 15:
            return "Executive"
        elif years >= 10:
            return "Senior"
        elif years >= 5:
            return "Mid-Level"
        else:
            return "Junior"
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract key responsibilities"""
        responsibilities = []
        
        # Look for bullet points after responsibility keywords
        resp_section = re.search(
            r'(?:responsibilities|what you.ll do|key duties|role overview)[\s\S]*?(?:qualifications|requirements|what you need|$)',
            text.lower()
        )
        
        if resp_section:
            section_text = resp_section.group(0)
            # Extract bullet points
            bullets = re.findall(r'[•\-\*]\s*([^\n]+)', section_text)
            responsibilities = [b.strip() for b in bullets if len(b.strip()) > 10][:10]
        
        return responsibilities
    
    def _extract_qualifications(self, text: str) -> List[str]:
        """Extract qualifications"""
        qualifications = []
        
        qual_section = re.search(
            r'(?:qualifications|requirements|what you need|education)[\s\S]*?(?:preferred|benefits|about us|$)',
            text.lower()
        )
        
        if qual_section:
            section_text = qual_section.group(0)
            bullets = re.findall(r'[•\-\*]\s*([^\n]+)', section_text)
            qualifications = [b.strip() for b in bullets if len(b.strip()) > 10][:10]
        
        return qualifications
    
    def _extract_all_keywords(self, text: str) -> List[str]:
        """Extract all relevant keywords"""
        keywords = []
        text_lower = text.lower()
        
        # Common job keywords
        keyword_list = [
            "leadership", "management", "strategy", "operations", "digital",
            "transformation", "innovation", "optimization", "efficiency",
            "stakeholder", "vendor", "budget", "p&l", "roi", "kpi",
            "agile", "scrum", "waterfall", "sdlc", "devops",
            "cloud", "aws", "azure", "gcp", "saas", "paas",
            "ai", "ml", "data", "analytics", "bi", "automation",
            "healthcare", "health", "medical", "clinical", "hospital",
            "fintech", "banking", "payments", "financial", "insurance",
            "enterprise", "scale", "growth", "expansion", "regional",
            "gcc", "mena", "uae", "saudi", "ksa", "dubai"
        ]
        
        for kw in keyword_list:
            if kw in text_lower:
                keywords.append(kw)
        
        return list(set(keywords))


class ATSScorer:
    """Score CV against job description for ATS compatibility"""
    
    def __init__(self):
        self.weights = {
            "keyword_match": 30,
            "experience_match": 25,
            "skills_match": 25,
            "format_score": 10,
            "qualifications": 10
        }
    
    def score(self, profile: Dict, job: JobRequirements) -> Tuple[int, Dict]:
        """
        Score CV against job requirements
        Returns: (total_score, breakdown)
        """
        breakdown = {}
        
        # Keyword match score
        profile_text = self._profile_to_text(profile).lower()
        keyword_matches = sum(1 for kw in job.keywords if kw.lower() in profile_text)
        keyword_score = min(30, int((keyword_matches / max(len(job.keywords), 1)) * 30))
        breakdown["keyword_match"] = keyword_score
        
        # Experience match
        exp_score = self._score_experience(profile, job)
        breakdown["experience_match"] = exp_score
        
        # Skills match
        skills_score = self._score_skills(profile, job)
        breakdown["skills_match"] = skills_score
        
        # Format score (assumes good format)
        breakdown["format_score"] = 8
        
        # Qualifications match
        qual_score = self._score_qualifications(profile, job)
        breakdown["qualifications"] = qual_score
        
        total = sum(breakdown.values())
        return total, breakdown
    
    def _profile_to_text(self, profile: Dict) -> str:
        """Convert profile to searchable text"""
        parts = [
            profile.get("name", ""),
            profile.get("title", ""),
            profile.get("summary", ""),
            " ".join(profile.get("certifications", []))
        ]
        
        for exp in profile.get("experience", []):
            parts.extend([
                exp.get("title", ""),
                exp.get("company", ""),
                exp.get("sector", ""),
                " ".join(exp.get("achievements", [])),
                " ".join(exp.get("skills_used", []))
            ])
        
        return " ".join(parts)
    
    def _score_experience(self, profile: Dict, job: JobRequirements) -> int:
        """Score experience match"""
        total_exp = profile.get("total_experience_years", 0)
        
        if total_exp >= job.experience_years:
            base_score = 25
        elif total_exp >= job.experience_years * 0.8:
            base_score = 20
        elif total_exp >= job.experience_years * 0.6:
            base_score = 15
        else:
            base_score = 10
        
        # Bonus for sector match
        job_sector = self._detect_sector(job.keywords)
        if job_sector in profile.get("sectors", []):
            base_score += 5
        
        return min(25, base_score)
    
    def _score_skills(self, profile: Dict, job: JobRequirements) -> int:
        """Score skills match"""
        all_skills = []
        for category, skills in profile.get("core_skills", {}).items():
            all_skills.extend([s.lower() for s in skills])
        
        required_matches = sum(1 for skill in job.required_skills 
                              if any(skill.lower() in s for s in all_skills))
        
        if len(job.required_skills) > 0:
            match_ratio = required_matches / len(job.required_skills)
        else:
            match_ratio = 0.5
        
        return min(25, int(match_ratio * 25))
    
    def _score_qualifications(self, profile: Dict, job: JobRequirements) -> int:
        """Score qualifications match"""
        certs = [c.lower() for c in profile.get("certifications", [])]
        
        # Check for degree requirements
        has_mba = "mba" in " ".join(certs) or "mba" in job.raw_text.lower()
        
        # Check for PMP/PM certifications
        has_pm_cert = any(cert in ["pmp", "csm", "cspo"] for cert in certs)
        
        score = 0
        if has_mba:
            score += 5
        if has_pm_cert:
            score += 5
        
        return min(10, score)
    
    def _detect_sector(self, keywords: List[str]) -> str:
        """Detect job sector from keywords"""
        health_keywords = ["healthcare", "health", "medical", "clinical", "hospital", "patient"]
        fintech_keywords = ["fintech", "banking", "payments", "financial", "stablecoin"]
        
        health_count = sum(1 for k in keywords if k.lower() in health_keywords)
        fintech_count = sum(1 for k in keywords if k.lower() in fintech_keywords)
        
        if health_count > fintech_count:
            return "HealthTech"
        elif fintech_count > health_count:
            return "FinTech"
        return "Technology"


class CVGenerator:
    """Generate tailored CV based on job requirements"""
    
    def __init__(self, profile_db: ProfileDatabase):
        self.profile = profile_db
        self.parser = JDParser()
        self.scorer = ATSScorer()
    
    def generate(self, job_text: str, job_title: str = "", company: str = "") -> TailoredCV:
        """Generate a tailored CV for a job"""
        # Parse job requirements
        job = self.parser.parse(job_text, job_title, company)
        
        # Score current profile
        ats_score, breakdown = self.scorer.score(self.profile.data, job)
        
        # Generate tailored sections
        sections = self._generate_sections(job)
        
        # Generate suggestions for improvement
        suggestions = self._generate_suggestions(job, ats_score, breakdown)
        
        return TailoredCV(
            job_title=job.title,
            company=job.company,
            sections=sections,
            ats_score=ats_score,
            match_analysis=breakdown,
            suggestions=suggestions,
            generated_at=datetime.now().isoformat()
        )
    
    def _generate_sections(self, job: JobRequirements) -> List[CVSection]:
        """Generate CV sections tailored to job"""
        sections = []
        
        # Header section
        header = f"""{self.profile.data['name']}
{self.profile.data['title']}
{self.profile.data['location']}
LinkedIn: {self.profile.data['contact']['linkedin']}
"""
        sections.append(CVSection("Header", header, 1))
        
        # Summary - tailored to job
        summary = self._generate_summary(job)
        sections.append(CVSection("Professional Summary", summary, 2))
        
        # Core Competencies - prioritize job-relevant skills
        competencies = self._generate_competencies(job)
        sections.append(CVSection("Core Competencies", competencies, 3))
        
        # Experience - prioritize relevant roles
        experience = self._generate_experience(job)
        sections.append(CVSection("Professional Experience", experience, 4))
        
        # Certifications
        certs = " • ".join(self.profile.data['certifications'])
        sections.append(CVSection("Certifications", certs, 5))
        
        # Education
        education = self._generate_education()
        sections.append(CVSection("Education", education, 6))
        
        return sections
    
    def _generate_summary(self, job: JobRequirements) -> str:
        """Generate tailored professional summary"""
        base_summary = self.profile.data['summary']
        
        # Add job-specific emphasis
        sector = self.scorer._detect_sector(job.keywords)
        
        if sector == "HealthTech":
            emphasis = (" with deep expertise in healthcare AI and hospital operations. "
                       "Currently leading digital transformation at Saudi German Hospital Group.")
        elif sector == "FinTech":
            emphasis = (" with extensive FinTech background in digital banking and payment systems. "
                       "Publisher of weekly FinTech newsletter with established industry following.")
        else:
            emphasis = (" with proven track record across HealthTech and FinTech sectors. "
                       "Combines technical expertise with strategic leadership.")
        
        return base_summary + emphasis
    
    def _generate_competencies(self, job: JobRequirements) -> str:
        """Generate competencies prioritized for job"""
        all_skills = self.profile.get_all_skills()
        
        # Prioritize skills mentioned in job
        prioritized = []
        other_skills = []
        
        job_skills = set(s.lower() for s in job.required_skills + job.preferred_skills)
        
        for skill in all_skills:
            if any(job_skill in skill.lower() for job_skill in job_skills):
                prioritized.append(skill)
            else:
                other_skills.append(skill)
        
        # Take top prioritized + fill with other skills
        selected = prioritized[:8] + other_skills[:7]
        
        return " • ".join(selected[:15])
    
    def _generate_experience(self, job: JobRequirements) -> str:
        """Generate experience section prioritized for job"""
        relevant = self.profile.get_relevant_experience(job.keywords)
        
        exp_texts = []
        for exp in relevant[:4]:  # Top 4 most relevant
            achievements = "\n  • ".join([""] + exp['achievements'])
            text = f"""
{exp['title']} | {exp['company']} | {exp['period']}
{exp['location']} | {exp['sector']}{achievements}
"""
            exp_texts.append(text)
        
        return "\n---\n".join(exp_texts)
    
    def _generate_education(self) -> str:
        """Generate education section"""
        education = self.profile.data.get('education', [])
        if education:
            edu = education[0]
            return f"{edu['degree']} - {edu['field']}\n{edu['institution']}"
        return "MBA - Business Administration"
    
    def _generate_suggestions(self, job: JobRequirements, ats_score: int, breakdown: Dict) -> List[str]:
        """Generate suggestions to improve CV for this job"""
        suggestions = []
        
        if ats_score < 90:
            suggestions.append(f"⚠️ ATS Score: {ats_score}/100 - Target: 90+")
        
        if breakdown['keyword_match'] < 25:
            missing_keywords = [kw for kw in job.keywords[:10] 
                               if kw.lower() not in self.scorer._profile_to_text(self.profile.data).lower()]
            if missing_keywords:
                suggestions.append(f"🔍 Add these keywords to your CV: {', '.join(missing_keywords[:5])}")
        
        if breakdown['skills_match'] < 20:
            missing_skills = [s for s in job.required_skills[:5] 
                             if s.lower() not in " ".join(self.profile.get_all_skills()).lower()]
            if missing_skills:
                suggestions.append(f"💡 Highlight these skills (if you have them): {', '.join(missing_skills)}")
        
        if job.experience_years > self.profile.data['total_experience_years']:
            suggestions.append(f"📊 Job requires {job.experience_years}+ years, you have {self.profile.data['total_experience_years']}. Emphasize total career impact over years.")
        
        # Sector-specific suggestions
        sector = self.scorer._detect_sector(job.keywords)
        if sector == "HealthTech":
            suggestions.append("🏥 HealthTech Role: Lead with SGH experience, emphasize AI automation in healthcare")
        elif sector == "FinTech":
            suggestions.append("💰 FinTech Role: Emphasize newsletter authority, Intel/Microsoft enterprise experience")
        
        return suggestions
    
    def export_to_text(self, tailored_cv: TailoredCV) -> str:
        """Export CV to text format"""
        lines = [
            f"TAILORED CV FOR: {tailored_cv.job_title} at {tailored_cv.company}",
            f"Generated: {tailored_cv.generated_at}",
            f"ATS Score: {tailored_cv.ats_score}/100",
            "=" * 60,
            ""
        ]
        
        for section in sorted(tailored_cv.sections, key=lambda s: s.priority):
            lines.append(section.title.upper())
            lines.append("-" * len(section.title))
            lines.append(section.content)
            lines.append("")
        
        if tailored_cv.suggestions:
            lines.append("OPTIMIZATION SUGGESTIONS")
            lines.append("-" * 25)
            for suggestion in tailored_cv.suggestions:
                lines.append(suggestion)
        
        return "\n".join(lines)


# CLI Interface
def main():
    """Main CLI entry point"""
    import sys
    
    print("=" * 60)
    print("CV OPTIMIZER - Ahmed Nasr Profile")
    print("=" * 60)
    print()
    
    # Initialize
    profile_db = ProfileDatabase()
    generator = CVGenerator(profile_db)
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        # Read from file
        job_file = sys.argv[1]
        with open(job_file, 'r') as f:
            job_text = f.read()
        
        job_title = sys.argv[2] if len(sys.argv) > 2 else "Unknown Position"
        company = sys.argv[3] if len(sys.argv) > 3 else "Unknown Company"
    else:
        # Interactive mode
        print("Paste job description (press Ctrl+D when done):")
        job_text = sys.stdin.read()
        
        job_title = input("\nJob Title: ").strip()
        company = input("Company: ").strip()
    
    # Generate tailored CV
    print("\n" + "=" * 60)
    print("GENERATING TAILORED CV...")
    print("=" * 60 + "\n")
    
    tailored_cv = generator.generate(job_text, job_title, company)
    
    # Display results
    print(f"📄 Job: {tailored_cv.job_title} at {tailored_cv.company}")
    print(f"🎯 ATS Score: {tailored_cv.ats_score}/100")
    print()
    
    print("Match Analysis:")
    for category, score in tailored_cv.match_analysis.items():
        bar = "█" * (score // 2) + "░" * (50 - score // 2)
        print(f"  {category:20} [{bar}] {score}")
    print()
    
    if tailored_cv.suggestions:
        print("💡 Suggestions:")
        for suggestion in tailored_cv.suggestions:
            print(f"  {suggestion}")
        print()
    
    # Export
    output = generator.export_to_text(tailored_cv)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cv_{company.replace(' ', '_')}_{timestamp}.txt"
    filepath = Path("/root/.openclaw/workspace/tools/cv-optimizer/output") / filename
    
    with open(filepath, 'w') as f:
        f.write(output)
    
    print(f"✅ CV saved to: {filepath}")
    print()
    print("=" * 60)
    print("PREVIEW:")
    print("=" * 60)
    print(output[:2000] + "..." if len(output) > 2000 else output)


if __name__ == "__main__":
    main()
