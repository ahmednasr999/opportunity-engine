"""
Email Automation - Follow-up sequences and templates
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class EmailAutomation:
    """
    Automated email sequences for:
    - Application follow-ups
    - Interview thank-yous
    - Networking outreach
    - Recruiter check-ins
    """
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.templates_file = os.path.join(self.data_dir, 'email_templates.json')
        self.sequences_file = os.path.join(self.data_dir, 'email_sequences.json')
        
        self.templates = self._load_templates()
        self.sequences = self._load_json(self.sequences_file, [])
    
    def _load_json(self, filepath: str, default):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filepath: str, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_templates(self) -> Dict:
        """Load email templates"""
        default_templates = {
            'application_followup': {
                'name': 'Application Follow-Up',
                'subject': 'Following up on {job_title} application - {name}',
                'body': """Dear {hiring_manager},

I hope this message finds you well. I wanted to follow up on my application for the {job_title} position at {company} that I submitted on {application_date}.

I remain very excited about the opportunity to bring my 20+ years of digital transformation experience, particularly in {relevant_experience}, to your team. My recent work at Saudi German Hospital Group implementing HealthTech AI solutions aligns closely with {company}'s mission.

I would welcome the opportunity to discuss how my background in {key_skills} could contribute to your organization's goals. Please let me know if you need any additional information from me.

Thank you for your time and consideration.

Best regards,
{name}
{phone}
{email}
{linkedin}""",
                'timing': '7_days_after_application',
                'personalization': ['hiring_manager', 'job_title', 'company', 'relevant_experience']
            },
            
            'interview_thank_you': {
                'name': 'Interview Thank You',
                'subject': 'Thank you - {job_title} interview - {name}',
                'body': """Dear {interviewer_names},

Thank you for taking the time to meet with me today to discuss the {job_title} position at {company}. I enjoyed learning more about {specific_topic_discussed} and the team's vision for {company_direction}.

Our conversation reinforced my enthusiasm for this opportunity. I was particularly excited to hear about {specific_project_or_challenge}, as it aligns closely with my experience {relevant_achievement}.

I'm confident that my background in {key_qualification} would enable me to make an immediate impact on your team. I look forward to the possibility of contributing to {company}'s continued success.

Please don't hesitate to reach out if you need any additional information from me.

Best regards,
{name}
{phone}
{email}
{linkedin}""",
                'timing': 'within_24_hours',
                'personalization': ['interviewer_names', 'specific_topic_discussed', 'relevant_achievement']
            },
            
            'networking_outreach': {
                'name': 'Networking Outreach',
                'subject': '{connection_type} - HealthTech Leadership - {name}',
                'body': """Hi {contact_name},

I hope you're doing well! {connection_reference}

I'm currently exploring new HealthTech leadership opportunities and would value your insights given your experience at {contact_company}. I'm particularly interested in organizations that are {specific_interest}.

Would you be open to a brief 15-minute conversation? I'd love to hear your perspective on the market and any advice you might have for someone with my background in {brief_background}.

I completely understand if your schedule is tight, but any guidance would be greatly appreciated.

Thanks for considering,
{name}
{linkedin}""",
                'timing': 'immediate',
                'personalization': ['connection_reference', 'specific_interest', 'brief_background']
            },
            
            'recruiter_checkin': {
                'name': 'Recruiter Check-In',
                'subject': 'HealthTech VP opportunities - {name}',
                'body': """Hi {recruiter_name},

I hope you're having a great week! I wanted to check in regarding HealthTech leadership opportunities that might be a fit for my background.

Quick update on my search:
• Currently in discussions with {number} companies
• Targeting VP/Director level roles in digital transformation
• Open to {locations}
• Availability: {notice_period}

My recent highlights:
• Led HealthTech AI implementation across 12+ hospital facilities
• Managed $50M+ project portfolio at Saudi German Hospital Group
• Delivered 35% improvement in patient outcomes through digital innovation

If you have any roles that might align, I'd love to hear about them. I've also attached my updated CV for your reference.

Thanks for keeping me in mind!

Best,
{name}
{phone}
{email}""",
                'timing': 'weekly',
                'personalization': ['number', 'locations', 'notice_period']
            },
            
            'second_followup': {
                'name': 'Second Follow-Up',
                'subject': 'Re: {job_title} application - {name}',
                'body': """Dear {hiring_manager},

I wanted to follow up on my previous message regarding the {job_title} position. I understand you likely have many candidates to consider, and I appreciate the time it takes to review applications thoroughly.

I remain very interested in this opportunity and wanted to share a recent achievement that might be relevant: {recent_achievement}.

I believe my unique combination of {unique_value_proposition} makes me a strong fit for this role. I'd welcome the opportunity to discuss how I can contribute to {company}'s success.

If the position has been filled, I'd appreciate any feedback you might have on my application. I'm always looking to improve my approach.

Thank you again for your consideration.

Best regards,
{name}""",
                'timing': '14_days_after_first_followup',
                'personalization': ['recent_achievement', 'unique_value_proposition']
            },
            
            'post_offer_negotiation': {
                'name': 'Salary Negotiation',
                'subject': 'Excited about the offer - quick question',
                'body': """Dear {hiring_manager},

Thank you again for the offer to join {company} as {job_title}. I'm thrilled about the opportunity and confident I can make a significant impact on your team.

I've reviewed the offer details and wanted to discuss the base salary. Based on my research of the market and the value I bring with {key_qualifications}, I was expecting a base in the ${target_salary:,.0f} range.

My recent achievements include:
• {achievement_1}
• {achievement_2}
• {achievement_3}

I'm confident these experiences position me to deliver immediate ROI. Would there be flexibility to align the base closer to my expectations? I'm also open to discussing other components of the compensation package.

I'm very excited about the possibility of joining the team and look forward to your thoughts.

Best regards,
{name}""",
                'timing': 'within_48_hours_of_offer',
                'personalization': ['target_salary', 'key_qualifications', 'achievements']
            }
        }
        
        # Load saved templates or use defaults
        if os.path.exists(self.templates_file):
            with open(self.templates_file, 'r') as f:
                saved = json.load(f)
                return {**default_templates, **saved}
        
        return default_templates
    
    def generate_email(self, template_name: str, variables: Dict) -> Dict:
        """
        Generate personalized email from template
        """
        template = self.templates.get(template_name)
        if not template:
            return {'error': f'Template {template_name} not found'}
        
        # Fill in template
        subject = template['subject'].format(**variables)
        body = template['body'].format(**variables)
        
        return {
            'template': template_name,
            'subject': subject,
            'body': body,
            'timing': template['timing'],
            'personalization_needed': [p for p in template.get('personalization', []) 
                                      if p not in variables],
            'ready_to_send': len([p for p in template.get('personalization', []) 
                                 if p not in variables]) == 0
        }
    
    def create_followup_sequence(self, job_data: Dict) -> List[Dict]:
        """
        Create automated follow-up sequence for a job application
        """
        sequence = []
        application_date = datetime.now()
        
        # Step 1: Application submitted (immediate)
        sequence.append({
            'step': 1,
            'type': 'confirmation',
            'timing': 'immediate',
            'action': 'Application submitted',
            'status': 'completed',
            'date': application_date.isoformat()
        })
        
        # Step 2: First follow-up (Day 7)
        sequence.append({
            'step': 2,
            'type': 'email',
            'timing': '7_days',
            'template': 'application_followup',
            'status': 'scheduled',
            'scheduled_date': (application_date + timedelta(days=7)).isoformat(),
            'action': 'Send follow-up email'
        })
        
        # Step 3: LinkedIn connection (Day 10)
        sequence.append({
            'step': 3,
            'type': 'linkedin',
            'timing': '10_days',
            'status': 'scheduled',
            'scheduled_date': (application_date + timedelta(days=10)).isoformat(),
            'action': 'Connect with hiring manager on LinkedIn'
        })
        
        # Step 4: Second follow-up (Day 14)
        sequence.append({
            'step': 4,
            'type': 'email',
            'timing': '14_days',
            'template': 'second_followup',
            'status': 'scheduled',
            'scheduled_date': (application_date + timedelta(days=14)).isoformat(),
            'action': 'Send second follow-up'
        })
        
        # Step 5: Move on (Day 21)
        sequence.append({
            'step': 5,
            'type': 'decision',
            'timing': '21_days',
            'status': 'scheduled',
            'scheduled_date': (application_date + timedelta(days=21)).isoformat(),
            'action': 'If no response, focus energy on other opportunities'
        })
        
        # Save sequence
        sequence_record = {
            'id': f"seq_{len(self.sequences) + 1}",
            'job_id': job_data.get('id'),
            'company': job_data.get('company'),
            'title': job_data.get('title'),
            'created_at': application_date.isoformat(),
            'steps': sequence
        }
        
        self.sequences.append(sequence_record)
        self._save_json(self.sequences_file, self.sequences)
        
        return sequence
    
    def get_pending_emails(self) -> List[Dict]:
        """
        Get emails that need to be sent today
        """
        pending = []
        today = datetime.now().date()
        
        for sequence in self.sequences:
            for step in sequence.get('steps', []):
                if step.get('status') == 'scheduled':
                    scheduled_date = datetime.fromisoformat(step['scheduled_date']).date()
                    if scheduled_date <= today:
                        pending.append({
                            'sequence_id': sequence['id'],
                            'company': sequence['company'],
                            'title': sequence['title'],
                            'step': step['step'],
                            'type': step['type'],
                            'template': step.get('template'),
                            'action': step['action'],
                            'scheduled_date': step['scheduled_date']
                        })
        
        return pending
    
    def mark_email_sent(self, sequence_id: str, step_number: int):
        """Mark an email as sent"""
        for sequence in self.sequences:
            if sequence['id'] == sequence_id:
                for step in sequence['steps']:
                    if step['step'] == step_number:
                        step['status'] = 'sent'
                        step['sent_at'] = datetime.now().isoformat()
                        self._save_json(self.sequences_file, self.sequences)
                        return True
        return False
    
    def get_email_stats(self) -> Dict:
        """Get statistics on email activity"""
        total_sequences = len(self.sequences)
        
        emails_sent = 0
        emails_pending = 0
        responses_received = 0
        
        for sequence in self.sequences:
            for step in sequence.get('steps', []):
                if step.get('status') == 'sent':
                    emails_sent += 1
                elif step.get('status') == 'scheduled':
                    emails_pending += 1
                elif step.get('status') == 'responded':
                    responses_received += 1
        
        return {
            'total_sequences': total_sequences,
            'emails_sent': emails_sent,
            'emails_pending': emails_pending,
            'responses_received': responses_received,
            'response_rate': responses_received / emails_sent if emails_sent > 0 else 0,
            'templates_available': len(self.templates)
        }
