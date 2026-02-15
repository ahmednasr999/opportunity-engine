"""
AI CV Rewriter - GPT-powered content generation for CVs
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime

class AICVRewriter:
    """
    AI-powered CV content generation
    - Rewrites experience bullets for impact
    - Generates multiple CV variants
    - Creates cover letters
    - Predicts interview questions
    """
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.variants_file = os.path.join(self.data_dir, 'cv_variants.json')
        self.variants = self._load_json(self.variants_file, [])
    
    def _load_json(self, filepath: str, default):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filepath: str, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def rewrite_experience_bullet(self, original: str, metric: str = None) -> str:
        """
        Rewrite experience bullet to be more impactful
        Uses templates optimized for executive resumes
        """
        # Power verb mapping
        power_verbs = {
            'led': ['Spearheaded', 'Orchestrated', 'Championed', 'Directed'],
            'managed': ['Steered', 'Oversaw', 'Governed', 'Commanded'],
            'implemented': ['Deployed', 'Executed', 'Pioneered', 'Established'],
            'improved': ['Optimized', 'Elevated', 'Transformed', 'Revolutionized'],
            'created': ['Architected', 'Designed', 'Devised', 'Engineered'],
            'increased': ['Accelerated', 'Amplified', 'Boosted', 'Maximized'],
            'reduced': ['Minimized', 'Streamlined', 'Condensed', 'Slashed'],
            'developed': ['Cultivated', 'Nurtured', 'Fostered', 'Advanced']
        }
        
        # Find and replace weak verbs
        lower_original = original.lower()
        result = original
        
        for weak, strong_list in power_verbs.items():
            if weak in lower_original:
                import random
                result = result.replace(weak, random.choice(strong_list), 1)
                break
        
        # Add metric if provided
        if metric and '%' not in result and '$' not in result:
            result = f"{result}, resulting in {metric}"
        
        return result
    
    def generate_cv_variant(self, profile: Dict, target_role: str, target_company: str, 
                           focus_area: str = 'general') -> Dict:
        """
        Generate a tailored CV variant for specific role/company
        """
        variant = {
            'id': f"variant_{len(self.variants) + 1}",
            'target_role': target_role,
            'target_company': target_company,
            'focus_area': focus_area,
            'created_at': datetime.now().isoformat(),
            'content': {}
        }
        
        # Generate tailored headline
        headlines = {
            'healthtech': f"HealthTech Digital Transformation Leader | {profile.get('certifications', '')}",
            'fintech': f"FinTech Strategy & Operations Executive | {profile.get('certifications', '')}",
            'pmo': f"Strategic PMO Leader & Change Agent | {profile.get('certifications', '')}",
            'general': f"Digital Transformation Expert & Regional Engagement Leader | {profile.get('certifications', '')}"
        }
        variant['content']['headline'] = headlines.get(focus_area, headlines['general'])
        
        # Generate tailored summary
        summaries = {
            'healthtech': f"Results-driven HealthTech executive with 20+ years transforming healthcare delivery through AI, data analytics, and digital innovation. Proven track record implementing enterprise-scale solutions across {target_company}'s focus areas.",
            'fintech': f"Strategic FinTech leader with deep expertise in digital payments, banking transformation, and regulatory compliance. Demonstrated success scaling operations and driving revenue growth in competitive markets.",
            'pmo': f"Strategic PMO leader specializing in large-scale transformation initiatives. Expert in establishing governance frameworks, optimizing project portfolios, and delivering measurable business outcomes across global organizations.",
            'general': profile.get('summary', '')
        }
        variant['content']['summary'] = summaries.get(focus_area, summaries['general'])
        
        # Tailor experience bullets
        tailored_experience = []
        for exp in profile.get('experience', []):
            tailored_exp = exp.copy()
            achievements = exp.get('achievements', [])
            
            # Select most relevant achievements based on focus
            if focus_area == 'healthtech':
                relevant = [a for a in achievements if any(word in a.lower() 
                    for word in ['health', 'hospital', 'patient', 'clinical', 'ai', 'analytics'])]
            elif focus_area == 'fintech':
                relevant = [a for a in achievements if any(word in a.lower() 
                    for word in ['revenue', 'growth', 'digital', 'payment', 'banking'])]
            elif focus_area == 'pmo':
                relevant = [a for a in achievements if any(word in a.lower() 
                    for word in ['project', 'portfolio', 'pmo', 'framework', 'team'])]
            else:
                relevant = achievements[:3]
            
            tailored_exp['highlighted_achievements'] = relevant[:3] if relevant else achievements[:3]
            tailored_experience.append(tailored_exp)
        
        variant['content']['experience'] = tailored_experience
        
        # Save variant
        self.variants.append(variant)
        self._save_json(self.variants_file, self.variants)
        
        return variant
    
    def generate_cover_letter(self, profile: Dict, job_title: str, company: str, 
                             job_description: str) -> str:
        """
        Generate tailored cover letter
        """
        # Extract key requirements from job description
        requirements = self._extract_requirements(job_description)
        
        # Build cover letter sections
        header = f"""{profile.get('name', '')}
{profile.get('contact', {}).get('email', '')} | {profile.get('contact', {}).get('uae', '').split('+')[-1].strip()} | {profile.get('contact', {}).get('egypt', '').split('+')[-1].strip()}
{datetime.now().strftime('%B %d, %Y')}

Hiring Manager
{company}

"""
        
        opening = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company}. With over 20 years of experience driving digital transformation across healthcare and FinTech sectors, I am excited about the opportunity to contribute to {company}'s innovative mission.

"""
        
        # Match requirements to experience
        body_paragraphs = []
        for req in requirements[:3]:
            match = self._find_matching_experience(req, profile)
            if match:
                body_paragraphs.append(f"{match}\n")
        
        body = "\n".join(body_paragraphs)
        
        closing = f"""
I am particularly drawn to {company} because of {'your commitment to innovation in healthcare technology' if 'health' in company.lower() or 'health' in job_title.lower() else 'your market leadership and growth trajectory'}. I am confident that my track record of {self._get_key_achievement(profile)} would enable me to make an immediate impact on your team.

I would welcome the opportunity to discuss how my background in digital transformation, team leadership, and strategic planning aligns with {company}'s goals. Thank you for considering my application.

Sincerely,

{profile.get('name', '')}
"""
        
        return header + opening + body + closing
    
    def _extract_requirements(self, job_description: str) -> List[str]:
        """Extract key requirements from job description"""
        # Simple extraction - look for bullet points or numbered lists
        lines = job_description.split('\n')
        requirements = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('•') or line.startswith('-') or line[0].isdigit():
                if len(line) > 20:  # Meaningful requirement
                    requirements.append(line.lstrip('•-0123456789. '))
        
        return requirements[:5]  # Top 5 requirements
    
    def _find_matching_experience(self, requirement: str, profile: Dict) -> str:
        """Find experience that matches a requirement"""
        req_lower = requirement.lower()
        
        # Keyword matching
        if any(word in req_lower for word in ['leadership', 'team', 'manage']):
            return f"Your requirement for {requirement.split()[0]} leadership aligns perfectly with my experience leading cross-functional teams of 50+ professionals across multiple countries, most recently at Saudi German Hospital Group where I established PMO frameworks managing $50M+ in projects."
        
        if any(word in req_lower for word in ['healthcare', 'health', 'clinical']):
            return f"Regarding {requirement[:30]}..., I have successfully implemented HealthTech solutions across 12+ hospital facilities, including AI-driven Clinical Decision Support systems and Health Catalyst analytics platforms that improved patient outcomes by 35%."
        
        if any(word in req_lower for word in ['digital', 'transformation', 'technology']):
            return f"My background in {requirement[:30]}... includes leading enterprise-wide digital transformations at both PaySky and El Araby Group, where I delivered SAP S/4HANA implementations and modernized operational systems serving millions of users."
        
        if any(word in req_lower for word in ['strategy', 'strategic']):
            return f"In terms of {requirement[:30]}..., I have advised C-suite executives on multi-year strategic plans, market expansion strategies, and digital innovation roadmaps that delivered measurable ROI across FinTech and healthcare sectors."
        
        return f"Your requirement for {requirement[:40]}... resonates with my experience driving operational excellence and delivering complex initiatives on time and under budget across diverse industries."
    
    def _get_key_achievement(self, profile: Dict) -> str:
        """Get a key achievement for closing paragraph"""
        for exp in profile.get('experience', []):
            achievements = exp.get('achievements', [])
            for a in achievements:
                if any(metric in a for metric in ['%', '$', 'M', 'K', 'fold']):
                    return a[:100] + "..."
        return "delivering large-scale transformation initiatives"
    
    def predict_interview_questions(self, job_title: str, company: str, 
                                   job_description: str) -> List[Dict]:
        """
        Predict likely interview questions and provide answer frameworks
        """
        questions = []
        
        # Role-based questions
        role_questions = {
            'pmo': [
                {
                    'question': 'How do you establish a PMO from scratch?',
                    'framework': 'Use STAR method: Situation (blank slate), Task (build PMO), Action (governance, tools, training), Result (300 projects managed)',
                    'key_points': ['Governance framework', 'Tool selection', 'Change management', 'Metrics definition']
                },
                {
                    'question': 'How do you handle conflicting priorities across multiple projects?',
                    'framework': 'Discuss portfolio prioritization, stakeholder alignment, and resource optimization',
                    'key_points': ['OKR alignment', 'Resource allocation', 'Stakeholder communication', 'Risk assessment']
                }
            ],
            'healthtech': [
                {
                    'question': 'How do you ensure clinical adoption of new technology?',
                    'framework': 'Emphasize change management, training, and demonstrating value to clinicians',
                    'key_points': ['Physician champions', 'Workflow integration', 'Training programs', 'Success metrics']
                },
                {
                    'question': 'Describe your experience with healthcare data analytics.',
                    'framework': 'Highlight Health Catalyst, EDW implementation, and clinical outcomes improvement',
                    'key_points': ['Health Catalyst EDW', 'Predictive analytics', 'Clinical decision support', 'ROI measurement']
                }
            ],
            'leadership': [
                {
                    'question': 'Tell me about a time you led a major transformation.',
                    'framework': 'Use the example from TopMed/SGH: scale, complexity, multi-country, measurable results',
                    'key_points': ['Digital transformation', 'Cross-functional teams', 'Change management', 'Measurable outcomes']
                },
                {
                    'question': 'How do you align technology initiatives with business strategy?',
                    'framework': 'Discuss strategic planning, OKRs, stakeholder engagement, and ROI focus',
                    'key_points': ['Strategic alignment', 'Business case development', 'Executive communication', 'Value delivery']
                }
            ]
        }
        
        # Add role-specific questions
        job_lower = job_title.lower()
        if 'pmo' in job_lower or 'project' in job_lower:
            questions.extend(role_questions['pmo'])
        if any(word in job_lower for word in ['health', 'hospital', 'medical']):
            questions.extend(role_questions['healthtech'])
        questions.extend(role_questions['leadership'])
        
        # Company-specific questions
        questions.append({
            'question': f'Why {company}?',
            'framework': f'Research company mission, recent news, and connect to your HealthTech/FinTech experience',
            'key_points': ['Company mission alignment', 'Recent achievements', 'Growth opportunities', 'Cultural fit']
        })
        
        # Behavioral questions
        questions.extend([
            {
                'question': 'Tell me about a failure and what you learned.',
                'framework': 'Be honest, focus on learning and growth, show resilience',
                'key_points': ['Specific situation', 'Your responsibility', 'Lesson learned', 'How you applied it']
            },
            {
                'question': 'How do you handle stress and tight deadlines?',
                'framework': 'Discuss prioritization, delegation, and maintaining quality under pressure',
                'key_points': ['Prioritization methods', 'Team support', 'Communication', 'Self-care']
            }
        ])
        
        return questions[:8]  # Top 8 questions
    
    def generate_salary_negotiation_script(self, offer_amount: float, target_amount: float, 
                                          job_title: str) -> Dict:
        """
        Generate salary negotiation talking points
        """
        difference = target_amount - offer_amount
        percent_diff = (difference / offer_amount) * 100
        
        script = {
            'offer_amount': offer_amount,
            'target_amount': target_amount,
            'difference': difference,
            'strategy': 'collaborative' if percent_diff < 15 else 'value-based',
            'opening': f"Thank you for the offer. I'm excited about the opportunity. Based on my research and the value I bring, I was expecting a base salary in the ${target_amount:,.0f} range.",
            'justification_points': [
                "20+ years of digital transformation experience across HealthTech and FinTech",
                "Proven track record managing $50M+ project portfolios",
                "Recent HealthTech AI implementations with measurable ROI",
                "Multi-country leadership experience (KSA, UAE, Egypt)",
                f"Market rate for {job_title} roles is ${target_amount:,.0f}-{(target_amount * 1.15):,.0f}"
            ],
            'fallback_options': [
                f"If base is fixed, could we discuss a ${difference:,.0f} signing bonus?",
                "Could we include performance-based bonuses tied to project delivery?",
                "Would additional PTO or flexible work arrangements be possible?",
                "Can we schedule a compensation review in 6 months based on performance?"
            ],
            'closing': "I'm confident I can deliver significant value in this role, and I want to ensure the compensation reflects that impact. I'm open to discussing how we can structure this to work for both of us."
        }
        
        return script
