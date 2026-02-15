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

# Import semantic scoring (uses MiniMax, no extra cost)
try:
    from semantic_ats import SemanticATSScorer
    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False

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
    """Ahmed's master profile data - UPDATED with complete information"""
    
    def __init__(self):
        self.data = {
            "name": "Ahmed Nasr",
            "title": "HealthTech Digital Transformation Expert & Regional Engagement Leader",
            "location": "Dubai, UAE",
            "visa": "UAE Permanent Work Visa (ID: 143529044)",
            "summary": "A distinguished Digital Transformation Expert and Regional Engagement Leader with over 20 years of experience, driving innovation and operational excellence across FinTech, healthcare, and e-commerce sectors. Adept at leading large-scale digital projects, managing high-performance cross-functional teams, and delivering transformative business solutions.",
            
            "contact": {
                "phone_uae": "+971 50 281 4490",
                "phone_egypt": "+20 128 573 3991",
                "email": "ahmednasr999@gmail.com",
                "linkedin": "linkedin.com/in/ahmednasr",
                "address": "Al Barsha Rd, Dubai, UAE"
            },
            
            "core_skills": {
                "leadership": [
                    "Regional Engagement & Market Expansion",
                    "Strategic Business Planning",
                    "P&L Leadership",
                    "Stakeholder & Change Management",
                    "People Leadership & Team Building",
                    "Go-To-Market Strategy",
                    "Business Development"
                ],
                "technical": [
                    "Digital Transformation",
                    "HealthTech & Healthcare IT",
                    "ERP/HIS Systems (SAP S/4HANA)",
                    "Enterprise Data & Analytics (Health Catalyst EDW)",
                    "AI-Powered Clinical Decision Support",
                    "Patient Engagement Platforms",
                    "Telemedicine & Mobile Health",
                    "Process Automation"
                ],
                "project_management": [
                    "PMO Establishment",
                    "Program & Project Management",
                    "Agile & Scrum",
                    "OKR & KPI Management",
                    "Lean Six Sigma",
                    "Project Automation"
                ],
                "consulting": [
                    "Strategic Advisory",
                    "Business Analysis (CBAP)",
                    "Solution Architecture",
                    "Digital Operations",
                    "Healthcare Compliance (JCI, HIMSS, MOH)"
                ]
            },
            
            "experience": [
                {
                    "title": "Acting PMO & Regional Engagement Lead",
                    "company": "TopMed (Saudi German Hospital Group - SGH)",
                    "location": "KSA, UAE, Egypt",
                    "period": "June 2024 - Present",
                    "duration_years": 1,
                    "sector": "HealthTech",
                    "achievements": [
                        "Leading HealthTech Digital Transformation across SGH Group in KSA, UAE & Egypt",
                        "Strategic Partnerships with Health Catalyst and KLAS Research (US healthcare providers)",
                        "PMO Framework: Established structured PMO for large-scale HealthTech projects",
                        "Enterprise Data Strategy: Implemented Health Catalyst EDW for real-time analytics",
                        "AI Clinical Decision Support: Deployed AI-driven CDS for diagnostics and patient safety",
                        "Patient Digital Engagement: Launched telemedicine, mobile apps, and engagement portals",
                        "Operational Efficiency: Data-driven insights streamlined workflows, reduced costs",
                        "Healthcare Compliance: Aligned with JCI, HIMSS, and MOH regulations"
                    ],
                    "skills_used": ["PMO", "Digital Transformation", "Healthcare IT", "AI/ML", "Data Analytics"]
                },
                {
                    "title": "Country Manager",
                    "company": "PaySky & Yalla SuperApp (Acquired by ENPO)",
                    "location": "Egypt",
                    "period": "Apr 2021 - Jan 2022",
                    "duration_years": 1,
                    "sector": "FinTech",
                    "achievements": [
                        "P&L Leadership: Managed operating budgets, achieved financial OKRs, drove revenue growth",
                        "Business Strategy: Directed market mapping, product strategy, data analytics, client insights",
                        "People Leadership: Managed cross-functional teams, headcount, budgets, and resources",
                        "Sales & Revenue: Enhanced client relationships, closed high-value deals, up-selling strategies",
                        "GTM: Built world-class Go-To-Market team for B2B and B2C success"
                    ],
                    "skills_used": ["P&L Management", "Strategy", "GTM", "Team Leadership", "FinTech"]
                },
                {
                    "title": "Head of Strategy & VP Advisor",
                    "company": "El Aroby Group",
                    "location": "Egypt",
                    "period": "Jan 2020 - Dec 2021",
                    "duration_years": 2,
                    "sector": "HealthTech / Enterprise",
                    "achievements": [
                        "SAP S/4HANA Implementation: Led successful ERP implementation, streamlined business processes",
                        "Health ERP System: Led Aroby Hospital implementation (Mayo Clinic system equivalent)",
                        "Strategic Planning: Developed multi-year strategic business plans, organizational alignment",
                        "Mentorship: Advised executive teams on operations, marketing, and financial planning"
                    ],
                    "skills_used": ["SAP S/4HANA", "ERP", "Strategic Planning", "Executive Advisory"]
                },
                {
                    "title": "CEO & Business Partner",
                    "company": "Soleek Lab",
                    "location": "Egypt",
                    "period": "May 2018 - Jul 2019",
                    "duration_years": 1.5,
                    "sector": "HealthTech / E-commerce",
                    "achievements": [
                        "Business Development: Spearedheaded strategic planning and customer engagement strategies",
                        "Operational Management: Enhanced project delivery and customer satisfaction",
                        "Company Growth: Drove growth through innovation and project excellence"
                    ],
                    "skills_used": ["Business Strategy", "Operations", "Customer Engagement"]
                },
                {
                    "title": "PMO Section Head",
                    "company": "EMP (Acquired by Network International)",
                    "location": "Egypt",
                    "period": "Sep 2014 - Jun 2017",
                    "duration_years": 3,
                    "sector": "FinTech / Payments",
                    "achievements": [
                        "PMO from Scratch: Built PMO for African bank projects, integrated with central banks",
                        "Strategic Dashboard: Developed proactive decision-making dashboard, increased net profit 3x",
                        "Project Automation: Implemented Microsoft Project Server on cloud, managed 300 concurrent projects"
                    ],
                    "skills_used": ["PMO", "Project Management", "Dashboard Development", "Cloud Systems"]
                },
                {
                    "title": "Product Development Manager",
                    "company": "Talabat (Delivery Hero SE)",
                    "location": "Egypt",
                    "period": "Jun 2017 - May 2018",
                    "duration_years": 1,
                    "sector": "E-commerce / FoodTech",
                    "achievements": [
                        "Regional Liaison: Focal point between Berlin HQ and MENA region companies",
                        "Office Setup: Established Egypt office, managed software engineers, account/product managers",
                        "Scale Achievement: Moved daily orders from 30K to 7M through operational excellence",
                        "Tracking & Excellence: Implemented tracking features, enhanced customer experience"
                    ],
                    "skills_used": ["Product Management", "Regional Operations", "Team Building"]
                },
                {
                    "title": "Project Manager",
                    "company": "Intel, Microsoft, Revamp Consulting",
                    "location": "Global / Egypt",
                    "period": "2007 - 2014",
                    "duration_years": 7,
                    "sector": "Technology / Consulting",
                    "achievements": [
                        "Successfully managed and delivered multiple software engineering projects",
                        "Regional engagement and technical leadership",
                        "Various consulting engagements in technology and operations"
                    ],
                    "skills_used": ["Project Management", "Software Engineering", "Consulting"]
                }
            ],
            
            "education": [
                {
                    "degree": "MBA (In Progress)",
                    "field": "Business Administration",
                    "institution": "Sadat Academy for Management Sciences",
                    "year": "Expected 2026"
                },
                {
                    "degree": "BSc. Computer Sciences & Business Administration",
                    "field": "Computer Sciences & Business Administration",
                    "institution": "Sadat Academy for Management Sciences",
                    "year": "June 2006"
                }
            ],
            
            "certifications": [
                "Project Management Professional (PMP)",
                "Certified Scrum Master (CSM)",
                "Certified Business Analysis Professional (CBAP)",
                "Microsoft Certified Application Developer (MCAD)",
                "Microsoft Certified Professional (MCP)",
                "Lean Six Sigma Certified Professional",
                "Six Sigma (Multiple Certificates)"
            ],
            
        "total_experience_years": 20,
            
            "sectors": ["HealthTech", "FinTech", "E-commerce", "Enterprise Technology", "Consulting"],
            
            "languages": ["Arabic (Native)", "English (Professional)"],
            
            "key_metrics": [
                "$25M+ transformation initiatives",
                "40% efficiency gains",
                "25% cost reductions",
                "300 concurrent projects managed",
                "7M daily orders scale (Talabat)",
                "3x net profit increase (EMP)"
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
    
    # Expanded skill vocabulary - 500+ terms
    SKILL_KEYWORDS = [
        # Technical Skills
        "python", "java", "javascript", "typescript", "sql", "nosql", "mongodb", "postgresql",
        "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud",
        "docker", "kubernetes", "k8s", "terraform", "ansible", "jenkins", "git", "github",
        "machine learning", "ml", "deep learning", "ai", "artificial intelligence", 
        "data science", "data engineering", "data analytics", "big data", "hadoop", "spark",
        "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib",
        "react", "angular", "vue", "node.js", "express", "django", "flask", "spring",
        "microservices", "api", "rest api", "graphql", "soap", "web services",
        "ci/cd", "devops", "devsecops", "sre", "site reliability",
        
        # Healthcare Skills
        "healthcare", "health", "medical", "clinical", "hospital", "patient care",
        "ehr", "electronic health records", "emr", "electronic medical records",
        "hl7", "fhir", "health informatics", "clinical data", "medical imaging",
        "healthcare ai", "clinical ai", "precision medicine", "telemedicine",
        "hipaa", "healthcare compliance", "medical devices", "pharma", "biotech",
        "laboratory information systems", "lis", "pacs", "radiology information systems",
        
        # Finance/FinTech Skills
        "fintech", "banking", "payments", "financial technology", "digital banking",
        "blockchain", "cryptocurrency", "crypto", "bitcoin", "ethereum", "smart contracts",
        "payment processing", "payment gateways", "digital wallets", "mobile payments",
        "risk management", "credit risk", "market risk", "operational risk",
        "compliance", "regulatory compliance", "regtech", "aml", "kyc",
        "trading systems", "algorithmic trading", "quantitative finance", "quant",
        "financial modeling", "valuation", "financial analysis", "investment banking",
        "wealth management", "asset management", "portfolio management",
        "insurance", "insurtech", "underwriting", "claims processing",
        "stablecoin", "defi", "decentralized finance", "web3",
        
        # Management Skills
        "project management", "program management", "portfolio management", "ppm",
        "agile", "scrum", "kanban", "lean", "six sigma", "pmp", "safe",
        "product management", "product owner", "scrum master", "delivery manager",
        "pmo", "project management office", "project coordinator",
        "waterfall", "sdlc", "software development life cycle",
        "jira", "confluence", "asana", "monday.com", "trello", "ms project",
        "resource management", "capacity planning", "demand management",
        "release management", "change management", "itil", "it service management",
        
        # Leadership Skills
        "leadership", "executive leadership", "senior leadership", "c-level",
        "team leadership", "people management", "talent management", "performance management",
        "coaching", "mentoring", "succession planning", "workforce planning",
        "stakeholder management", "stakeholder engagement", "executive presence",
        "strategic planning", "business strategy", "corporate strategy", "growth strategy",
        "change leadership", "transformational leadership", "thought leadership",
        "cross-functional leadership", "matrix management", "virtual teams",
        
        # Operations Skills
        "operations", "business operations", "technical operations", "it operations",
        "process improvement", "process optimization", "business process reengineering",
        "operational excellence", "opex", "continuous improvement", "kaizen",
        "supply chain", "logistics", "procurement", "vendor management", "sourcing",
        "quality assurance", "qa", "quality control", "qc", "testing", "automation testing",
        "service delivery", "sla management", "incident management", "problem management",
        "capacity management", "availability management", "disaster recovery", "business continuity",
        
        # Data & Analytics
        "data governance", "data quality", "data management", "master data management", "mdm",
        "data warehousing", "data lake", "data lakehouse", "etl", "elt", "data integration",
        "business intelligence", "bi", "tableau", "power bi", "qlik", "looker", "microstrategy",
        "data visualization", "dashboards", "kpi", "metrics", "okr", "balanced scorecard",
        "predictive analytics", "prescriptive analytics", "descriptive analytics",
        "statistical analysis", "a/b testing", "experimentation", "data mining",
        
        # Business Skills
        "business analysis", "business architecture", "enterprise architecture", "togaf",
        "requirements gathering", "user stories", "use cases", "process mapping",
        "business case development", "roi analysis", "cost-benefit analysis",
        "vendor evaluation", "rfp", "request for proposal", "contract negotiation",
        "budget management", "financial management", "p&l", "profit and loss", "fp&a",
        "mergers and acquisitions", "m&a", "due diligence", "integration",
        
        # Soft Skills
        "communication", "written communication", "verbal communication", "presentation skills",
        "negotiation", "conflict resolution", "problem solving", "critical thinking",
        "decision making", "analytical thinking", "systems thinking", "design thinking",
        "collaboration", "teamwork", "influencing", "persuasion", "storytelling",
        "adaptability", "flexibility", "resilience", "emotional intelligence", "eq",
        "cultural awareness", "diversity and inclusion", "dei",
        
        # Emerging Tech
        "generative ai", "genai", "llm", "large language models", "chatgpt", "claude",
        "prompt engineering", "rag", "retrieval augmented generation", "vector databases",
        "iot", "internet of things", "edge computing", "5g", "robotics", "rpa",
        "low code", "no code", "power platform", "salesforce", "sap", "oracle",
        "crm", "customer relationship management", "erp", "enterprise resource planning",
        "crm", "salesforce", "hubspot", "microsoft dynamics", "zendesk",
        
        # Security
        "cybersecurity", "information security", "infosec", "security operations", "soc",
        "penetration testing", "ethical hacking", "vulnerability assessment",
        "identity and access management", "iam", "sso", "single sign-on", "mfa",
        "security compliance", "iso 27001", "soc 2", "gdpr", "ccpa", "privacy",
        "threat intelligence", "incident response", "forensics", "siem", "soar"
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


# Skill synonym mapping for semantic matching
SKILL_SYNONYMS = {
    # Project Management
    "project manager": ["pm", "program manager", "delivery manager", "project coordinator"],
    "program manager": ["pgm", "program director", "portfolio manager"],
    "scrum master": ["agile coach", "scrum coach", "iteration manager"],
    "product manager": ["pm", "product owner", "po"],
    "agile": ["scrum", "kanban", "lean", "iterative", "sprint"],
    
    # Leadership
    "director": ["vp", "vice president", "head of", "lead"],
    "vp": ["vice president", "svp", "vice president"],
    "cto": ["chief technology officer", "vp engineering", "head of engineering"],
    "ceo": ["chief executive officer", "founder", "co-founder"],
    
    # Technical
    "software engineer": ["developer", "software developer", "programmer", "coder"],
    "full stack": ["fullstack", "full-stack", "frontend and backend", "end-to-end"],
    "frontend": ["front-end", "ui developer", "client-side"],
    "backend": ["back-end", "server-side", "api developer"],
    "devops": ["sre", "platform engineer", "infrastructure engineer"],
    "cloud": ["aws", "azure", "gcp", "cloud computing", "cloud infrastructure"],
    
    # Data
    "data scientist": ["data science", "machine learning engineer", "ml engineer"],
    "data engineer": ["data engineering", "etl developer", "big data engineer"],
    "business analyst": ["ba", "business systems analyst", "requirements analyst"],
    "data analyst": ["data analytics", "bi analyst", "reporting analyst"],
    
    # AI/ML
    "machine learning": ["ml", "deep learning", "ai", "artificial intelligence"],
    "ai": ["artificial intelligence", "machine learning", "cognitive computing"],
    "generative ai": ["genai", "gen ai", "llm", "foundation models"],
    
    # Healthcare
    "healthcare": ["health care", "medical", "clinical", "hospital"],
    "ehr": ["electronic health records", "emr", "electronic medical records"],
    "clinical": ["medical", "patient care", "healthcare delivery"],
    
    # Finance
    "fintech": ["financial technology", "digital finance", "finance technology"],
    "banking": ["financial services", "retail banking", "commercial banking"],
    "investment": ["asset management", "portfolio management", "wealth management"]
}


class ATSScorer:
    """Score CV against job description for ATS compatibility"""
    
    def __init__(self):
        self.weights = {
            "keyword_match": 25,
            "experience_match": 25,
            "skills_match": 25,
            "format_score": 10,
            "qualifications": 10,
            "recency": 5
        }
    
    def score(self, profile: Dict, job: JobRequirements) -> Tuple[int, Dict, List[str]]:
        """
        Score CV against job requirements
        Returns: (total_score, breakdown, feedback)
        """
        breakdown = {}
        feedback = []
        
        # Keyword match score with synonym expansion
        profile_text = self._profile_to_text(profile).lower()
        keyword_score, keyword_feedback = self._score_keywords_advanced(profile_text, job.keywords)
        breakdown["keyword_match"] = keyword_score
        feedback.extend(keyword_feedback)
        
        # Experience match
        exp_score, exp_feedback = self._score_experience_advanced(profile, job)
        breakdown["experience_match"] = exp_score
        if exp_feedback:
            feedback.append(exp_feedback)
        
        # Skills match with synonyms
        skills_score, skills_feedback = self._score_skills_advanced(profile, job)
        breakdown["skills_match"] = skills_score
        feedback.extend(skills_feedback)
        
        # Format score with validation
        format_score, format_feedback = self._score_format_advanced(profile)
        breakdown["format_score"] = format_score
        if format_feedback:
            feedback.append(format_feedback)
        
        # Qualifications match
        qual_score, qual_feedback = self._score_qualifications_advanced(profile, job)
        breakdown["qualifications"] = qual_score
        if qual_feedback:
            feedback.append(qual_feedback)
        
        # Recency scoring
        recency_score, recency_feedback = self._score_recency(profile)
        breakdown["recency"] = recency_score
        if recency_feedback:
            feedback.append(recency_feedback)
        
        total = sum(breakdown.values())
        
        # Generate priority feedback
        if total < 60:
            feedback.insert(0, "⚠️ CRITICAL: CV needs significant improvements before applying")
        elif total < 75:
            feedback.insert(0, "⚡ PRIORITY: Address gaps below to improve interview chances")
        else:
            feedback.insert(0, "✅ Strong match! Minor tweaks can push this to 85+")
        
        return total, breakdown, feedback
    
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
    
    def _score_keywords_advanced(self, profile_text: str, job_keywords: List[str]) -> Tuple[int, List[str]]:
        """Advanced keyword matching with synonyms"""
        feedback = []
        matches = 0
        expanded_keywords = set()
        
        # Expand keywords with synonyms
        for kw in job_keywords:
            expanded_keywords.add(kw.lower())
            # Add synonyms if keyword is in our mapping
            for main_term, synonyms in SKILL_SYNONYMS.items():
                if kw.lower() == main_term.lower() or kw.lower() in [s.lower() for s in synonyms]:
                    expanded_keywords.add(main_term.lower())
                    expanded_keywords.update([s.lower() for s in synonyms])
        
        # Count matches
        matched_terms = []
        missing_terms = []
        
        for kw in expanded_keywords:
            if kw in profile_text:
                matches += 1
                if kw not in matched_terms:
                    matched_terms.append(kw)
            else:
                if kw not in missing_terms and len(missing_terms) < 5:
                    missing_terms.append(kw)
        
        # Calculate score
        if len(expanded_keywords) > 0:
            score = min(25, int((matches / len(expanded_keywords)) * 25))
        else:
            score = 12
        
        # Generate feedback
        if score < 15:
            feedback.append(f"⚠️ Keyword Gap: Missing {len(missing_terms)} key terms: {', '.join(missing_terms[:3])}")
            feedback.append("💡 Add these keywords naturally in your summary or experience bullets")
        elif score < 20:
            feedback.append(f"⚡ Keyword Boost: Consider adding: {', '.join(missing_terms[:2])}")
        
        return score, feedback
    
    def _score_experience_advanced(self, profile: Dict, job: JobRequirements) -> Tuple[int, str]:
        """Advanced experience scoring with context"""
        total_exp = profile.get("total_experience_years", 20)  # Default to 20 for Ahmed
        feedback = ""
        
        # Base scoring
        if total_exp >= job.experience_years:
            base_score = 22
        elif total_exp >= job.experience_years * 0.8:
            base_score = 18
        elif total_exp >= job.experience_years * 0.6:
            base_score = 14
            feedback = f"⚠️ Experience Gap: You have {total_exp} years, role asks for {job.experience_years}"
        else:
            base_score = 10
            feedback = f"❌ Experience Mismatch: {total_exp} vs {job.experience_years} years required"
        
        # Sector match bonus
        job_sector = self._detect_sector(job.keywords)
        if job_sector in profile.get("sectors", ["healthcare", "fintech", "technology"]):
            base_score += 3
        
        # Leadership level check
        job_title = job.title.lower()
        has_leadership = any(term in job_title for term in ["vp", "director", "head", "lead", "chief", "senior"])
        if has_leadership:
            # Check if profile shows leadership experience
            leadership_exp = sum(1 for exp in profile.get("experience", [])
                               if any(term in exp.get("title", "").lower() 
                                     for term in ["vp", "director", "head", "lead", "chief", "manager"]))
            if leadership_exp > 0:
                base_score += 3
            else:
                feedback = "⚠️ Leadership Evidence: Add more leadership-focused achievements"
        
        return min(25, base_score), feedback
    
    def _score_skills_advanced(self, profile: Dict, job: JobRequirements) -> Tuple[int, List[str]]:
        """Advanced skills matching with synonym detection"""
        feedback = []
        
        # Build profile skills set with synonyms
        profile_skills = set()
        for category, skills in profile.get("core_skills", {}).items():
            for skill in skills:
                skill_lower = skill.lower()
                profile_skills.add(skill_lower)
                # Add synonyms
                for main_term, synonyms in SKILL_SYNONYMS.items():
                    if skill_lower == main_term.lower() or skill_lower in [s.lower() for s in synonyms]:
                        profile_skills.add(main_term.lower())
                        profile_skills.update([s.lower() for s in synonyms])
        
        # Match against job skills with synonym expansion
        required_matches = 0
        matched_skills = []
        missing_skills = []
        
        for job_skill in job.required_skills:
            job_skill_lower = job_skill.lower()
            # Check direct match
            if any(job_skill_lower in ps for ps in profile_skills):
                required_matches += 1
                matched_skills.append(job_skill)
            else:
                # Check synonym match
                found_synonym = False
                for main_term, synonyms in SKILL_SYNONYMS.items():
                    if job_skill_lower == main_term.lower() or job_skill_lower in [s.lower() for s in synonyms]:
                        if any(main_term.lower() in ps or any(s.lower() in ps for s in synonyms) 
                               for ps in profile_skills):
                            required_matches += 1
                            matched_skills.append(f"{job_skill} (via synonym)")
                            found_synonym = True
                            break
                if not found_synonym and len(missing_skills) < 5:
                    missing_skills.append(job_skill)
        
        # Calculate score
        if len(job.required_skills) > 0:
            score = min(25, int((required_matches / len(job.required_skills)) * 25))
        else:
            score = 20  # Default if no required skills specified
        
        # Generate feedback
        if score < 15:
            feedback.append(f"⚠️ Skills Gap: Missing {len(missing_skills)} required skills")
            feedback.append(f"💡 Top skills to add: {', '.join(missing_skills[:3])}")
        elif score < 20:
            feedback.append(f"⚡ Skills Boost: Add {', '.join(missing_skills[:2])} if you have them")
        
        return score, feedback
    
    def _score_format_advanced(self, profile: Dict) -> Tuple[int, str]:
        """Score CV format for ATS compatibility"""
        issues = []
        score = 10
        
        # Check for common ATS issues
        summary = profile.get("summary", "")
        experience = profile.get("experience", [])
        
        # Check summary length
        if len(summary) < 100:
            issues.append("Summary too short (aim for 150-300 characters)")
            score -= 2
        elif len(summary) > 500:
            issues.append("Summary may be too long for some ATS")
            score -= 1
        
        # Check for bullet points in achievements
        for exp in experience:
            achievements = exp.get("achievements", [])
            if len(achievements) < 3:
                issues.append(f"Add more achievement bullets for {exp.get('title', 'role')}")
                score -= 1
            
            # Check for metrics in bullets
            has_metrics = any(any(char.isdigit() for char in ach) for ach in achievements)
            if not has_metrics:
                issues.append(f"Add metrics ($, %, numbers) to {exp.get('title', 'role')} bullets")
                score -= 1
        
        # Check for skills section
        core_skills = profile.get("core_skills", {})
        if not core_skills or sum(len(v) for v in core_skills.values()) < 10:
            issues.append("Expand skills section (aim for 15+ skills)")
            score -= 2
        
        feedback = ""
        if issues:
            feedback = "⚠️ Format Issues:\n  • " + "\n  • ".join(issues[:3])
        
        return max(0, score), feedback
    
    def _score_qualifications_advanced(self, profile: Dict, job: JobRequirements) -> Tuple[int, str]:
        """Advanced qualifications matching"""
        certs = [c.lower() for c in profile.get("certifications", [])]
        job_text = job.raw_text.lower()
        feedback = ""
        score = 0
        
        # Check for specific degree requirements
        degree_patterns = [
            (r"bachelor'?s? degree", ["bachelor", "bs", "ba", "b.s.", "b.a."]),
            (r"master'?s? degree", ["master", "ms", "ma", "mba", "m.s.", "m.a.", "m.b.a."]),
            (r"mba", ["mba", "m.b.a."]),
            (r"phd|doctorate|doctoral", ["phd", "ph.d.", "doctorate", "doctoral"])
        ]
        
        for pattern, matching_certs in degree_patterns:
            if re.search(pattern, job_text):
                if any(mc in " ".join(certs) for mc in matching_certs):
                    score += 3
                else:
                    feedback = f"⚠️ Degree Requirement: Consider highlighting relevant education"
        
        # Check for certifications
        cert_keywords = ["pmp", "csm", "cspo", "pmi", "safe", "itil", "six sigma", "lean"]
        job_certs = [ck for ck in cert_keywords if ck in job_text]
        
        if job_certs:
            matched_certs = [jc for jc in job_certs if any(jc in c for c in certs)]
            score += min(4, len(matched_certs) * 2)
            
            missing = [jc.upper() for jc in job_certs if not any(jc in c for c in certs)]
            if missing and not feedback:
                feedback = f"⚡ Certifications: Consider obtaining {', '.join(missing[:2])}"
        
        return min(10, score), feedback
    
    def _score_recency(self, profile: Dict) -> Tuple[int, str]:
        """Score recency of experience (recent = more relevant)"""
        experience = profile.get("experience", [])
        feedback = ""
        
        if not experience:
            return 0, "❌ No experience data"
        
        # Check if most recent role is current
        most_recent = experience[0]
        is_current = "present" in most_recent.get("date_range", "").lower() or \
                     "current" in most_recent.get("date_range", "").lower()
        
        if is_current:
            score = 5
        else:
            score = 3
            feedback = "⚡ Recency: Ensure your most recent role is marked as current"
        
        # Bonus for recent leadership
        recent_titles = [exp.get("title", "").lower() for exp in experience[:2]]
        has_recent_leadership = any(term in " ".join(recent_titles) 
                                   for term in ["director", "vp", "head", "lead", "chief", "senior"])
        
        if has_recent_leadership:
            score += 2
        
        return min(5, score), feedback
    
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
        
        # Score current profile with advanced scoring and feedback
        ats_score, breakdown, feedback = self.scorer.score(self.profile.data, job)
        
        # Generate tailored sections
        sections = self._generate_sections(job)
        
        # Generate suggestions for improvement
        suggestions = self._generate_suggestions_advanced(job, ats_score, breakdown, feedback)
        
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
        job_lower = job.title.lower() + " " + job.raw_text.lower()
        
        # Build targeted emphasis based on job requirements
        emphasis_parts = []
        
        # Healthcare emphasis
        if "health" in job_lower or "clinical" in job_lower:
            emphasis_parts.append("deep expertise in healthcare AI, machine learning, and hospital operations")
        
        # AI/ML emphasis
        if "ai" in job_lower or "machine learning" in job_lower or "artificial intelligence" in job_lower:
            emphasis_parts.append("proven track record implementing AI-driven clinical decision support and predictive analytics")
        
        # P&L/Budget emphasis
        if "p&l" in job_lower or "budget" in job_lower or "$" in job.raw_text:
            emphasis_parts.append("extensive P&L management experience with $50M+ technology budgets")
        
        # Telemedicine/virtual care
        if "telemedicine" in job_lower or "virtual care" in job_lower or "digital health" in job_lower:
            emphasis_parts.append("leader in digital health transformation and virtual care delivery")
        
        # Product/Operations
        if "product" in job_lower:
            emphasis_parts.append("product leadership from concept to commercialization")
        
        # Build final emphasis
        if emphasis_parts:
            emphasis = " with " + ", ".join(emphasis_parts[:2]) + ". "
        else:
            emphasis = " with proven track record across HealthTech and FinTech sectors. "
        
        # Add current context
        emphasis += "Currently leading digital transformation initiatives at Saudi German Hospital Group (TopMed)."
        
        # Clean up any double periods
        result = base_summary + emphasis
        result = result.replace("..", ".").replace(". .", ". ")
        
        return result
    
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
            inst = edu.get('institution', 'Leading Business School')
            return f"{edu['degree']} - {edu['field']}\n{inst}"
        return "MBA - Business Administration\nLeading Business School"
    
    def _generate_suggestions_advanced(self, job: JobRequirements, ats_score: int, breakdown: Dict, feedback: List[str]) -> List[str]:
        """Generate detailed suggestions using new feedback system"""
        suggestions = feedback.copy()  # Start with detailed scorer feedback
        
        # Add score context
        if ats_score >= 85:
            suggestions.append(f"🎯 Excellent Match! Score: {ats_score}/100")
        elif ats_score >= 70:
            suggestions.append(f"📈 Good Match. Score: {ats_score}/100 - Minor improvements recommended")
        else:
            suggestions.append(f"⚠️ Needs Work. Score: {ats_score}/100 - Significant gaps to address")
        
        # Add breakdown details
        suggestions.append(f"\n📊 Score Breakdown:")
        for category, score in breakdown.items():
            if category != 'recency' or score < 5:
                bar = "█" * (score // 2) + "░" * ((25 - score) // 2)
                suggestions.append(f"  {category.replace('_', ' ').title()}: {bar} {score}/25")
        
        # Sector-specific strategic suggestions
        sector = self.scorer._detect_sector(job.keywords)
        suggestions.append(f"\n🎯 Strategic Recommendations:")
        
        if sector == "HealthTech":
            suggestions.append("  • Lead with Saudi German Hospital Group (SGH) experience")
            suggestions.append("  • Emphasize AI automation and clinical systems impact")
            suggestions.append("  • Highlight Healthcare AI and Health Catalyst initiatives")
        elif sector == "FinTech":
            suggestions.append("  • Lead with Intel PaySky / Microsoft payment systems experience")
            suggestions.append("  • Reference weekly FinTech newsletter authority")
            suggestions.append("  • Emphasize stablecoin and digital banking expertise")
        elif sector == "Technology":
            suggestions.append("  • Balance HealthTech and FinTech experience")
            suggestions.append("  • Emphasize cross-sector digital transformation")
            suggestions.append("  • Highlight AI/ML implementation across domains")
        
        # Quick wins
        suggestions.append(f"\n⚡ Quick Wins (implement in 10 minutes):")
        if breakdown.get('keyword_match', 0) < 20:
            missing = [kw for kw in job.keywords[:5] if kw.lower() not in self.scorer._profile_to_text(self.profile.data).lower()]
            if missing:
                suggestions.append(f"  1. Add these keywords to your summary: {', '.join(missing[:3])}")
        if breakdown.get('format_score', 0) < 8:
            suggestions.append(f"  2. Add metrics (%, $, numbers) to your top 3 achievements")
        suggestions.append(f"  3. Tailor your headline to match the exact job title")
        
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
    print(f"🎯 Traditional ATS Score: {tailored_cv.ats_score}/100")
    
    # Add semantic scoring if available
    if SEMANTIC_AVAILABLE:
        print("\n🧠 Running Semantic Analysis (MiniMax)...")
        semantic_scorer = SemanticATSScorer()
        cv_text = "\n".join([section.content for section in tailored_cv.sections])
        semantic_result = semantic_scorer.score_semantic(cv_text, job_text)
        print(f"🎯 Semantic Score: {semantic_result.overall_score}/100 (confidence: {semantic_result.confidence:.0%})")
        print(f"   +{semantic_result.overall_score - tailored_cv.ats_score} points of understanding")
        print(f"\n💡 {semantic_result.reasoning[:100]}...")
    
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
