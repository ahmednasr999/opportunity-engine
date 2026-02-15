"""
Cover Letter Generator - Creates tailored cover letters for job applications
"""
from datetime import datetime
from typing import Dict, List

class CoverLetterGenerator:
    """Generate personalized cover letters based on job and profile"""
    
    def __init__(self):
        self.templates = {
            'executive': self._executive_template,
            'healthcare': self._healthcare_template,
            'tech': self._tech_template,
            'consulting': self._consulting_template
        }
    
    def generate(self, job_title: str, company: str, job_description: str, 
                 profile: Dict, style: str = 'executive') -> str:
        """Generate a tailored cover letter"""
        
        # Determine best template based on job
        if 'health' in job_description.lower() or 'clinical' in job_description.lower():
            template_func = self._healthcare_template
        elif 'consulting' in job_description.lower() or 'advisor' in job_description.lower():
            template_func = self._consulting_template
        elif 'product' in job_title.lower() or 'tech' in job_description.lower():
            template_func = self._tech_template
        else:
            template_func = self._executive_template
        
        return template_func(job_title, company, job_description, profile)
    
    def _executive_template(self, job_title: str, company: str, job_desc: str, profile: Dict) -> str:
        """Executive leadership focused cover letter"""
        
        # Extract key requirements
        has_budget = '$' in job_desc or 'budget' in job_desc.lower() or 'p&l' in job_desc.lower()
        has_ai = 'ai' in job_desc.lower() or 'machine learning' in job_desc.lower()
        has_healthcare = 'health' in job_desc.lower() or 'clinical' in job_desc.lower()
        
        # Build hook based on company
        if 'HCA' in company:
            hook = "As a healthcare operations leader who has implemented AI-driven clinical decision support across hospital networks, I was immediately drawn to HCA's scale and commitment to transforming patient care through technology."
        elif 'Tempus' in company:
            hook = "The intersection of AI and precision medicine represents the future of healthcare, and Tempus is clearly leading that transformation. My experience implementing Health Catalyst AI solutions across 10+ hospitals has prepared me to contribute immediately to your mission."
        elif 'Teladoc' in company:
            hook = "Virtual care isn't the future—it's the present. Having led digital transformation initiatives at Saudi German Hospital Group, I understand both the technical infrastructure and operational complexity required to deliver care at scale."
        else:
            hook = f"With 20+ years leading digital transformation across HealthTech and FinTech sectors, I am excited about the opportunity to bring my expertise in AI automation and operational excellence to {company}."
        
        # Build evidence paragraph
        evidence_parts = []
        
        if has_healthcare:
            evidence_parts.append("Currently serving as Acting PMO at Saudi German Hospital Group (TopMed), I lead AI automation initiatives that have reduced operational processing time by 40% and driven 25% efficiency gains across hospital operations.")
        
        if has_ai:
            evidence_parts.append("My implementation of AI-driven clinical decision support systems has directly improved patient outcomes while optimizing resource allocation.")
        
        if has_budget:
            evidence_parts.append("I bring extensive P&L management experience, having overseen multi-million dollar technology budgets and led cross-functional teams of 50+ professionals across four countries.")
        
        evidence = " ".join(evidence_parts) if evidence_parts else "Throughout my career at Intel, Microsoft, and now SGH, I have consistently delivered large-scale transformation initiatives that combine technical innovation with operational excellence."
        
        # Build differentiator
        differentiators = []
        if 'FinTech' in str(profile.get('sectors', [])):
            differentiators.append("unique perspective from the FinTech sector, where I published a weekly newsletter reaching 5,000+ industry professionals")
        if 'Microsoft' in str(profile.get('experience', [])):
            differentiators.append("enterprise-scale experience from Microsoft and Intel")
        
        differentiator = ""
        if differentiators:
            differentiator = f" What distinguishes my background is my {differentiators[0]}."
        
        letter = f"""Dear Hiring Manager,

{hook}

{evidence}{differentiator}

The {job_title} role at {company} aligns perfectly with my expertise in:

• AI/ML strategy and implementation in healthcare environments
• Large-scale operational transformation ($50M+ budget management)
• Building and leading high-performing, cross-functional teams
• Driving measurable outcomes: 40% efficiency gains, 25% cost reductions
• Stakeholder management across executive, clinical, and technical teams

I am particularly drawn to {company}'s commitment to {'advancing healthcare through AI' if has_healthcare else 'operational excellence and innovation'}. My MBA, PMP certification, and Lean Six Sigma training provide the formal framework, but my 20+ years of hands-on leadership across Intel, Microsoft, and Saudi German Hospital Group provide the practical expertise to deliver results from day one.

I would welcome the opportunity to discuss how my experience implementing enterprise-scale AI solutions can accelerate {company}'s strategic objectives. I am available for a conversation at your convenience and can be reached at ahmednasr999@gmail.com or +971 50 281 4490.

Thank you for considering my application. I look forward to the possibility of contributing to {company}'s continued success.

Sincerely,

Ahmed Nasr, MBA, PMP
PMO & AI Automation Leader
https://linkedin.com/in/ahmednasr
"""
        
        return letter
    
    def _healthcare_template(self, job_title: str, company: str, job_desc: str, profile: Dict) -> str:
        """Healthcare-specific cover letter"""
        
        return f"""Dear Hiring Manager,

Healthcare transformation requires leaders who understand both the clinical mission and the operational reality. Having led digital transformation at Saudi German Hospital Group while implementing AI-driven clinical decision support systems, I bring that dual perspective to the {job_title} role at {company}.

At SGH (TopMed), I have driven measurable improvements across our hospital network:
• 40% reduction in operational processing time through AI automation
• 25% efficiency gains through operational excellence initiatives  
• Successful implementation of Health Catalyst AI platform improving patient outcomes
• Management of multi-million dollar technology budgets across regional hospitals

My previous experience at Intel and Microsoft provided the enterprise-scale technical foundation, while my MBA and PMP credentials ensure I can translate clinical needs into executable strategies. I understand the unique challenges of healthcare operations: regulatory compliance (HIPAA), EMR/EHR optimization, clinical workflow integration, and the critical importance of stakeholder buy-in across medical and administrative teams.

What I offer {company} is not just healthcare experience, but proven ability to lead AI/ML initiatives that deliver both clinical and operational value. I have built and led teams of 50+ professionals across four countries, managed $50M+ portfolios, and consistently delivered transformation programs on time and budget.

The opportunity to bring this expertise to {company}'s mission of {'transforming patient care' if 'transform' in job_desc.lower() else 'advancing healthcare delivery'} genuinely excites me. I am eager to discuss how my background aligns with your strategic objectives.

Thank you for your consideration. I can be reached at ahmednasr999@gmail.com or +971 50 281 4490.

Sincerely,

Ahmed Nasr, MBA, PMP
"""
    
    def _tech_template(self, job_title: str, company: str, job_desc: str, profile: Dict) -> str:
        """Tech/product-focused cover letter"""
        
        return f"""Dear Hiring Manager,

Building great products requires understanding both the technology and the humans who use it. My 20+ years spanning Intel, Microsoft, and Saudi German Hospital Group have taught me that the best technical solutions fail without operational excellence—and vice versa.

As Acting PMO at Saudi German Hospital Group, I lead AI automation initiatives that reduced processing time by 40% while improving patient outcomes. This wasn't just a technology implementation—it required product thinking: understanding user workflows, managing stakeholder expectations, iterating based on feedback, and measuring outcomes.

My background offers {company}:
• Deep technical expertise: AI/ML, digital transformation, enterprise systems
• Product leadership: From concept to deployment to optimization
• Scale experience: Programs affecting 90M+ users (Intel/Microsoft) to hospital networks
• Business acumen: MBA, PMP, $50M+ budget management, P&L responsibility
• Cross-functional leadership: Teams of 50+, four countries, multiple stakeholders

The {job_title} role represents the intersection of my technical capabilities and my operational experience. I understand how to build products that not only work technically but drive real business outcomes.

I would welcome the opportunity to discuss how my experience can accelerate {company}'s product roadmap. I am available at ahmednasr999@gmail.com or +971 50 281 4490.

Best regards,

Ahmed Nasr, MBA, PMP
"""
    
    def _consulting_template(self, job_title: str, company: str, job_desc: str, profile: Dict) -> str:
        """Consulting-focused cover letter"""
        
        return f"""Dear Hiring Manager,

The best consultants combine deep subject matter expertise with the ability to translate complex challenges into actionable strategies. As both an internal transformation leader (Intel, Microsoft, SGH) and external advisor (AN & Co. Consulting), I bring that dual perspective to {company}.

My 20+ years have been spent solving hard problems:
• Led SAP S/4HANA migration for 3,000+ users across multiple countries
• Implemented Health Catalyst AI platform, improving patient outcomes by 23%
• Drove $2.3M annual cost reductions through process automation
• Built consulting practice serving healthcare and FinTech clients
• Published thought leadership reaching 5,000+ industry professionals weekly

What distinguishes my consulting approach is that I've been on both sides of the table. I know what it's like to receive recommendations—and to be accountable for implementing them. This ensures my advice is both strategically sound and practically executable.

For {company}'s clients, I offer:
• Healthcare AI and digital transformation expertise
• FinTech and payment systems experience  
• Enterprise-scale program management (PMP, Lean Six Sigma)
• Stakeholder management across C-suite, technical, and clinical teams
• Proven ability to deliver measurable ROI

I am excited about the possibility of contributing to {company}'s client success and would welcome a conversation about how my background aligns with your needs.

Thank you for your consideration.

Sincerely,

Ahmed Nasr, MBA, PMP
https://linkedin.com/in/ahmednasr
"""


# Quick test
def demo_cover_letters():
    """Generate sample cover letters"""
    generator = CoverLetterGenerator()
    
    profile = {
        'name': 'Ahmed Nasr',
        'title': 'PMO & AI Automation Leader',
        'sectors': ['HealthTech', 'FinTech'],
        'experience': ['Intel', 'Microsoft', 'SGH']
    }
    
    jobs = [
        ("VP Healthcare AI & Operations", "HCA Healthcare", "AI ML healthcare operations"),
        ("VP Product & Operations", "Tempus", "precision medicine AI product"),
        ("VP Digital Health Operations", "Teladoc Health", "telemedicine virtual care")
    ]
    
    for title, company, desc in jobs:
        print(f"\n{'='*70}")
        print(f"COVER LETTER: {title} at {company}")
        print(f"{'='*70}\n")
        
        letter = generator.generate(title, company, desc, profile)
        print(letter[:1500] + "...\n[Letter continues - full version generated]")


if __name__ == "__main__":
    demo_cover_letters()
