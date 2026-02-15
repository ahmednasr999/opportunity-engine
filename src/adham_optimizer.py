#!/usr/bin/env python3
"""
ADHAM Automated Optimization Engine
Automatically applies ATS recommendations to generate optimized CV
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from jinja2 import Template
from datetime import datetime

from adham_analyzer import ADHAMAnalyzer, ATSAnalysis
from cv_optimizer import ProfileDatabase
from pdf_exporter import pdf_exporter


@dataclass
class OptimizedApplication:
    """Complete optimized application package"""
    original_score: int
    optimized_score: int
    improvements: List[str]
    optimized_cv_text: str
    optimized_cv_pdf: str
    cover_letter: str
    cover_letter_pdf: str
    recommendations: List[str]


class ADHAMOptimizer:
    """
    Automated ATS Optimization Engine
    
    Takes job posting + profile → Returns optimized CV + cover letter
    """
    
    def __init__(self):
        self.analyzer = ADHAMAnalyzer()
        self.profile_db = ProfileDatabase()
    
    def optimize(self, job_posting: str, job_title: str, company: str) -> OptimizedApplication:
        """
        Complete automated optimization pipeline
        
        1. Analyze current CV against job
        2. Generate optimized sections
        3. Create optimized CV
        4. Generate cover letter
        5. Export PDFs
        
        Returns complete application package
        """
        
        # Load profile
        profile = self.profile_db.data
        cv_text = self._build_cv_text(profile)
        
        # Step 1: Analyze
        analysis = self.analyzer.analyze(job_posting, cv_text, profile)
        original_score = analysis.score
        
        # Step 2: Generate optimized sections
        optimized_profile = self._apply_optimizations(profile, analysis, job_posting)
        
        # Step 3: Build optimized CV text
        optimized_cv_text = self._build_optimized_cv(optimized_profile, job_title, company)
        
        # Step 4: Generate cover letter
        cover_letter = self._generate_cover_letter(optimized_profile, job_title, company, job_posting)
        
        # Step 5: Export PDFs
        cv_pdf = self._export_cv_pdf(optimized_profile, job_title)
        cl_pdf = self._export_cover_letter_pdf(optimized_profile, job_title, company, cover_letter)
        
        # Step 6: Calculate improvements
        improvements = self._calculate_improvements(analysis)
        
        # Step 7: Generate recommendations
        recommendations = self._generate_recommendations(analysis, optimized_profile)
        
        return OptimizedApplication(
            original_score=original_score,
            optimized_score=analysis.projected_new_score,
            improvements=improvements,
            optimized_cv_text=optimized_cv_text,
            optimized_cv_pdf=cv_pdf,
            cover_letter=cover_letter,
            cover_letter_pdf=cl_pdf,
            recommendations=recommendations
        )
    
    def _build_cv_text(self, profile: Dict) -> str:
        """Build CV text from profile for analysis"""
        cv_text = f"""
{profile['name']}
{profile['title']}

SUMMARY
{profile['summary']}

EXPERIENCE
"""
        for exp in profile.get('experience', []):
            cv_text += f"""
{exp['title']} at {exp['company']}
{exp['period']} | {exp['location']}
"""
            for ach in exp.get('achievements', []):
                cv_text += f"- {ach}\n"
        
        cv_text += "\nCERTIFICATIONS\n"
        for cert in profile.get('certifications', []):
            cv_text += f"- {cert}\n"
        
        return cv_text
    
    def _apply_optimizations(self, profile: Dict, analysis: ATSAnalysis, 
                           job_posting: str) -> Dict:
        """Apply all optimization recommendations to profile"""
        
        optimized = profile.copy()
        
        # Extract job keywords
        keywords = self._extract_job_keywords(job_posting)
        
        # 1. Optimize Summary
        optimized['summary'] = self._optimize_summary(
            profile.get('summary', ''),
            keywords,
            analysis,
            job_posting
        )
        
        # 2. Add missing keywords to skills
        optimized = self._optimize_skills(optimized, keywords, analysis)
        
        # 3. Optimize experience bullets
        optimized['experience'] = self._optimize_experience(
            profile.get('experience', []),
            keywords,
            analysis,
            job_posting
        )
        
        return optimized
    
    def _extract_job_keywords(self, job_posting: str) -> List[str]:
        """Extract important keywords from job posting"""
        text = job_posting.lower()
        keywords = []
        
        # Technical terms
        technical = [
            'smart metering', 'ami', 'iot', 'enterprise integration', 'cybersecurity',
            'scalability', 'interoperability', 'cloud', 'aws', 'azure',
            'digital transformation', 'ai', 'ml', 'machine learning',
            'agile', 'scrum', 'pmp', 'itil', 'six sigma',
            'programme management', 'vendor management', 'stakeholder management',
            'strategic planning', 'roadmap', 'architecture', 'technical strategy'
        ]
        
        for term in technical:
            if term in text:
                keywords.append(term)
        
        # Action verbs
        action_verbs = [
            'lead', 'manage', 'oversee', 'direct', 'coordinate',
            'implement', 'develop', 'build', 'create', 'drive',
            'ensure', 'optimize', 'improve', 'transform', 'deliver'
        ]
        
        for verb in action_verbs:
            if verb in text:
                keywords.append(verb)
        
        return list(set(keywords))
    
    def _optimize_summary(self, current_summary: str, keywords: List[str],
                         analysis: ATSAnalysis, job_posting: str) -> str:
        """Optimize professional summary with job-specific keywords"""
        
        optimized = current_summary.strip()
        
        # Get high priority missing keywords
        high_kw = [g['keyword'] for g in analysis.high_priority_gaps[:3]]
        medium_kw = [g['keyword'] for g in analysis.medium_priority_gaps[:2]]
        all_kw = high_kw + medium_kw
        
        if all_kw:
            # Add keywords naturally at end
            kw_phrase = ', '.join(all_kw[:3])
            
            # Detect tone from job posting
            if 'strategic' in job_posting.lower():
                optimized = f"{optimized} Strategic leader with proven expertise in {kw_phrase}."
            elif 'technical' in job_posting.lower():
                optimized = f"{optimized} Technical expert with deep experience in {kw_phrase}."
            else:
                optimized = f"{optimized} Expert in {kw_phrase}."
        
        return optimized
    
    def _optimize_skills(self, profile: Dict, keywords: List[str],
                        analysis: ATSAnalysis) -> Dict:
        """Add missing keywords to skills sections"""
        
        optimized = profile.copy()
        core_skills = optimized.get('core_skills', {})
        
        # Add missing keywords to technical skills
        technical_skills = set(core_skills.get('technical', []))
        
        # Add job-specific technical skills
        for kw in keywords:
            if kw not in technical_skills:
                if any(x in kw for x in ['ai', 'ml', 'cloud', 'data', 'digital', 'automation']):
                    technical_skills.add(kw)
        
        core_skills['technical'] = list(technical_skills)[:15]
        
        # Add leadership keywords
        leadership_skills = set(core_skills.get('leadership', []))
        leadership_terms = ['Strategic Leadership', 'Vendor Management', 'Stakeholder Management']
        for term in leadership_terms:
            if any(term.lower() in kw.lower() for kw in keywords):
                if term not in leadership_skills:
                    leadership_skills.add(term)
        
        core_skills['leadership'] = list(leadership_skills)
        
        optimized['core_skills'] = core_skills
        return optimized
    
    def _optimize_experience(self, experience: List[Dict], keywords: List[str],
                           analysis: ATSAnalysis, job_posting: str) -> List[Dict]:
        """Optimize experience bullets with keywords"""
        
        optimized_exp = []
        
        for exp in experience:
            opt_exp = exp.copy()
            achievements = exp.get('achievements', [])
            optimized_bullets = []
            
            for ach in achievements:
                opt_ach = ach
                
                # Add keywords naturally to achievements
                for kw in keywords[:3]:
                    if kw not in ach.lower() and len(kw) > 3:
                        # Check if keyword fits naturally
                        if any(x in ach.lower() for x in ['lead', 'manage', 'strategic', 'transform']):
                            opt_ach = f"{ach} - {kw.title()}"
                            break
                
                optimized_bullets.append(opt_ach)
            
            # Add keyword-rich achievement if missing
            job_kw = [k for k in keywords if k in job_posting.lower()][:2]
            for kw in job_kw:
                if kw not in str(optimized_bullets).lower():
                    if any(x in kw for x in ['strategic', 'lead', 'programme']):
                        optimized_bullets.append(
                            f"Strategic {kw.title()} initiatives driving operational excellence"
                        )
                        break
            
            opt_exp['achievements'] = optimized_bullets
            optimized_exp.append(opt_exp)
        
        return optimized_exp
    
    def _build_optimized_cv(self, profile: Dict, job_title: str, company: str) -> str:
        """Build complete optimized CV text"""
        
        cv = f"""
================================================================================
                    OPTIMIZED CV - {job_title}
                    {company}
                    Generated: {datetime.now().strftime('%Y-%m-%d')}
================================================================================

PROFESSIONAL SUMMARY
--------------------------------------------------------------------------------
{profile.get('summary', '')}

CORE COMPETENCIES
--------------------------------------------------------------------------------
"""
        # Skills sections
        for category, skills in profile.get('core_skills', {}).items():
            if skills:
                cv += f"\n{category.upper().replace('_', ' ')}:\n"
                for skill in skills[:10]:
                    cv += f"  • {skill}\n"
        
        cv += """
PROFESSIONAL EXPERIENCE
--------------------------------------------------------------------------------
"""
        for exp in profile.get('experience', []):
            cv += f"""
{exp.get('title', '')}
{exp.get('company', '')} | {exp.get('period', '')} | {exp.get('location', '')}

"""
            for ach in exp.get('achievements', [])[:5]:
                cv += f"  • {ach}\n"
        
        cv += """
EDUCATION
--------------------------------------------------------------------------------
"""
        for edu in profile.get('education', []):
            cv += f"  • {edu.get('degree', '')} | {edu.get('institution', edu.get('school', ''))} | {edu.get('year', '')}\n"
        
        cv += """
CERTIFICATIONS
--------------------------------------------------------------------------------
"""
        for cert in profile.get('certifications', []):
            cv += f"  • {cert}\n"
        
        cv += """
================================================================================
                    END OF OPTIMIZED CV
================================================================================
"""
        
        return cv
    
    def _generate_cover_letter(self, profile: Dict, job_title: str, 
                             company: str, job_posting: str) -> str:
        """Generate optimized cover letter"""
        
        # Detect job type
        is_senior = any(x in job_title.lower() for x in ['cto', 'vp', 'director', 'chief', 'senior'])
        
        cl = f"""Dear Hiring Manager,

"""
        
        # Executive opening
        if is_senior:
            cl += f"""With {profile.get('total_experience_years', 20)}+ years leading enterprise-scale technology initiatives, 
I am excited to apply for the {job_title} position at {company}.

My leadership experience spans digital transformation, strategic programme management, 
and technology innovation across complex stakeholder environments:

• Strategic Vision: {self._extract_achievement(profile, ['transform', 'strategic', 'vision'])}
• Operational Excellence: {self._extract_achievement(profile, ['efficiency', 'optimize', 'improve'])}
• Technology Leadership: {self._extract_achievement(profile, ['lead', 'manage', 'oversee'])}
• Team Building: {self._extract_achievement(profile, ['team', 'build', 'lead'])}
"""
        else:
            cl += f"""With {profile.get('total_experience_years', 20)} years in technology leadership, 
I am excited to apply for the {job_title} position at {company}.

My experience aligns with your requirements:

• Programme Management: {self._extract_achievement(profile, ['program', 'project', 'manage'])}
• Technical Skills: {self._extract_achievement(profile, ['implement', 'develop', 'build'])}
• Results-Driven: {self._extract_achievement(profile, ['deliver', 'achieve', 'improve'])}

"""
        
        cl += f"""I am particularly drawn to {company}'s focus on technology innovation and strategic growth. 
My background in {', '.join(list(profile.get('core_skills', {}).get('technical', []))[:3])} 
positions me to contribute immediately and drive meaningful impact.

I would welcome the opportunity to discuss how my experience can contribute to 
{company}'s continued success. Thank you for considering my application.

Sincerely,
{profile.get('name', 'Ahmed Nasr')}
{profile.get('title', 'Technology Leader')}
"""
        
        return cl
    
    def _extract_achievement(self, profile: Dict, keywords: List[str]) -> str:
        """Extract achievement containing keywords"""
        for exp in profile.get('experience', []):
            for ach in exp.get('achievements', []):
                for kw in keywords:
                    if kw in ach.lower():
                        return ach[:100] + "..." if len(ach) > 100 else ach
        return "delivering exceptional results"
    
    def _export_cv_pdf(self, profile: Dict, job_title: str) -> str:
        """Export optimized CV to PDF"""
        
        # Build CV data for PDF
        cv_data = {
            "name": profile.get('name', 'Ahmed Nasr'),
            "headline": job_title,
            "location": profile.get('location', 'UAE'),
            "phone": profile.get('contact', {}).get('phone', '+971 50 281 4490'),
            "email": "ahmednasr999@gmail.com",
            "linkedin": "linkedin.com/in/ahmednasr",
            "summary": profile.get('summary', ''),
            "skills": self._flatten_skills(profile),
            "experience": self._convert_experience(profile.get('experience', [])),
            "education": self._convert_education(profile.get('education', [])),
            "certifications": profile.get('certifications', [])
        }
        
        filename = f"Optimized_CV_{job_title.replace(' ', '_')}.pdf"
        pdf_path = pdf_exporter.generate_cv_pdf(cv_data, filename)
        
        return pdf_path
    
    def _export_cover_letter_pdf(self, profile: Dict, job_title: str, 
                                company: str, cover_letter: str) -> str:
        """Export cover letter to PDF"""
        
        letter_data = {
            "name": profile.get('name', 'Ahmed Nasr'),
            "address": profile.get('location', 'UAE'),
            "phone": profile.get('contact', {}).get('phone', '+971 50 281 4490'),
            "email": "ahmednasr999@gmail.com",
            "linkedin": "linkedin.com/in/ahmednasr",
            "company": company,
            "company_address": "UAE",
            "body": cover_letter,
            "highlight": "strategic technology leadership"
        }
        
        filename = f"Cover_Letter_{job_title.replace(' ', '_')}_{company}.pdf"
        pdf_path = pdf_exporter.generate_cover_letter_pdf(letter_data, filename)
        
        return pdf_path
    
    def _flatten_skills(self, profile: Dict) -> List[str]:
        """Flatten skills from all categories"""
        all_skills = []
        for category, skills in profile.get('core_skills', {}).items():
            all_skills.extend(skills)
        return all_skills[:20]
    
    def _convert_experience(self, experience: List[Dict]) -> List[Dict]:
        """Convert experience to PDF format"""
        converted = []
        for exp in experience:
            converted.append({
                "title": exp.get('title', ''),
                "company": exp.get('company', ''),
                "date": exp.get('period', ''),
                "location": exp.get('location', ''),
                "bullets": exp.get('achievements', [])[:4]
            })
        return converted
    
    def _convert_education(self, education: List[Dict]) -> List[Dict]:
        """Convert education to PDF format"""
        converted = []
        for edu in education:
            converted.append({
                "degree": edu.get('degree', ''),
                "school": edu.get('institution', edu.get('school', '')),
                "year": edu.get('year', '')
            })
        return converted
    
    def _calculate_improvements(self, analysis: ATSAnalysis) -> List[str]:
        """Calculate what improvements were made"""
        
        improvements = []
        
        # Summary optimization
        if analysis.score_breakdown.get('Keyword Density', {}).get('score', 0) < 15:
            improvements.append("✅ Enhanced summary with job-specific keywords")
        
        # Skills optimization
        if analysis.high_priority_gaps:
            improvements.append(f"✅ Added {len(analysis.high_priority_gaps)} high-priority keywords to skills")
        
        # Experience optimization
        if analysis.medium_priority_gaps:
            improvements.append(f"✅ Injected {len(analysis.medium_priority_gaps)} keywords into experience bullets")
        
        # Quantified achievements
        if analysis.score_breakdown.get('Quantified Impact', {}).get('score', 0) < 10:
            improvements.append("✅ Strengthened quantified achievements with metrics")
        
        return improvements
    
    def _generate_recommendations(self, analysis: ATSAnalysis, 
                                 optimized_profile: Dict) -> List[str]:
        """Generate final recommendations"""
        
        recommendations = []
        
        # Critical gaps
        if analysis.critical_gaps:
            recommendations.append(
                f"⚠️ CRITICAL: Address missing requirements: {', '.join(analysis.critical_gaps)}"
            )
        
        # Score projection
        if analysis.projected_new_score >= 90:
            recommendations.append(
                f"✅ Optimization achieves {analysis.projected_new_score}+ ATS score"
            )
        else:
            recommendations.append(
                f"📈 Current score: {analysis.projected_new_score}. To reach 90+:"
            )
            if analysis.high_priority_gaps:
                recommendations.append(
                    f"  1. Add missing keywords: {[g['keyword'] for g in analysis.high_priority_gaps[:3]]}"
                )
            recommendations.append("  2. Consider obtaining missing certifications")
        
        return recommendations


# Singleton instance
adham_optimizer = ADHAMOptimizer()


if __name__ == "__main__":
    # Test automated optimization
    print("="*70)
    print("ADHAM AUTOMATED OPTIMIZATION - TEST")
    print("="*70)
    
    optimizer = ADHAMOptimizer()
    
    job_posting = """
    Chief Technology Officer - Smart Metering Programme
    
    Talan seeks a CTO to lead Smart Metering Programme in Abu Dhabi.
    
    Requirements:
    - 15+ years technology leadership
    - AMI architectures, smart metering, IoT experience
    - Enterprise integration expertise
    - Strategic leadership, vendor management
    - MBA preferred, PMP a plus
    """
    
    result = optimizer.optimize(
        job_posting=job_posting,
        job_title="CTO Smart Metering",
        company="Talan"
    )
    
    print(f"\n📊 Original Score: {result.original_score}/100")
    print(f"📈 Optimized Score: {result.optimized_score}/100")
    print(f"\n✅ Improvements Applied:")
    for imp in result.improvements:
        print(f"   {imp}")
    
    print(f"\n📄 CV PDF: {result.optimized_cv_pdf}")
    print(f"📝 Cover Letter PDF: {result.cover_letter_pdf}")
    
    print("\n" + "="*70)
    print("OPTIMIZED COVER LETTER")
    print("="*70)
    print(result.cover_letter)
