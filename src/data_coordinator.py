"""
Data Coordinator - Central hub connecting all tools
Ensures CVs, jobs, contacts, and documents are linked
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class DataCoordinator:
    """
    Central coordinator that links all tools:
    - Auto-index generated CVs in 2nd Brain
    - Link CVs to job applications
    - Cross-reference contacts with jobs
    - Unified timeline of all activities
    - Global search across all data
    """
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        
        # Ensure all data files exist
        self._ensure_data_files()
        
        # Load all data
        self.jobs = self._load_json('jobs.json', [])
        self.contacts = self._load_json('contacts.json', [])
        self.documents = self._load_json('documents.json', [])
        self.cvs = self._load_json('generated_cvs.json', [])
        self.calendar = self._load_json('calendar_events.json', [])
        self.activities = self._load_json('activities.json', [])
        self.links = self._load_json('links.json', {'cv_job': [], 'contact_job': [], 'document_job': []})
    
    def _ensure_data_files(self):
        """Create data files if they don't exist"""
        files = ['jobs.json', 'contacts.json', 'documents.json', 'generated_cvs.json', 
                'calendar_events.json', 'activities.json', 'links.json']
        for f in files:
            path = os.path.join(self.data_dir, f)
            if not os.path.exists(path):
                with open(path, 'w') as file:
                    json.dump([] if f != 'links.json' else {'cv_job': [], 'contact_job': [], 'document_job': []}, file)
    
    def _load_json(self, filename: str, default: Any) -> Any:
        """Load JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filename: str, data: Any):
        """Save to JSON file"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register_cv(self, cv_data: Dict, auto_index: bool = True) -> str:
        """
        Register a generated CV and optionally index in 2nd Brain
        """
        cv_record = {
            'id': f"cv_{len(self.cvs) + 1}",
            'filename': cv_data.get('filename', ''),
            'pdf_filename': cv_data.get('pdf_filename', ''),
            'company': cv_data.get('company', ''),
            'title': cv_data.get('title', ''),
            'ats_score': cv_data.get('ats_score', 0),
            'content_preview': cv_data.get('cv_text', '')[:500] + '...' if len(cv_data.get('cv_text', '')) > 500 else cv_data.get('cv_text', ''),
            'created_at': datetime.now().isoformat(),
            'linked_to_job': None,
            'indexed': auto_index
        }
        
        self.cvs.append(cv_record)
        self._save_json('generated_cvs.json', self.cvs)
        
        # Auto-index in 2nd Brain (documents)
        if auto_index:
            self._index_in_second_brain(cv_record)
        
        # Log activity
        self._log_activity('cv_generated', f"Generated CV for {cv_record['title']} at {cv_record['company']}", cv_record['id'])
        
        return cv_record['id']
    
    def _index_in_second_brain(self, cv_record: Dict):
        """Add CV to 2nd Brain documents"""
        content = cv_record.get('content_preview') or cv_record.get('cv_text', '')[:500] + '...'
        doc = {
            'id': f"doc_cv_{cv_record['id']}",
            'title': f"CV - {cv_record['title']} at {cv_record['company']}",
            'doc_type': 'cv',
            'content': content,
            'metadata': {
                'company': cv_record['company'],
                'role': cv_record['title'],
                'ats_score': cv_record.get('ats_score', 0),
                'source_cv_id': cv_record['id']
            },
            'tags': ['cv', 'generated', cv_record['company'].lower().replace(' ', '_')],
            'date_added': datetime.now().isoformat()
        }
        
        # Add to documents if not already there
        existing = [d for d in self.documents if d.get('metadata', {}).get('source_cv_id') == cv_record['id']]
        if not existing:
            self.documents.append(doc)
            self._save_json('documents.json', self.documents)
    
    def link_cv_to_job(self, cv_id: str, job_id: str):
        """Link a CV to a job application"""
        # Update CV record
        for cv in self.cvs:
            if cv['id'] == cv_id:
                cv['linked_to_job'] = job_id
                break
        self._save_json('generated_cvs.json', self.cvs)
        
        # Update job record
        for job in self.jobs:
            if job.get('id') == job_id:
                job['linked_cv_id'] = cv_id
                break
        self._save_json('jobs.json', self.jobs)
        
        # Add to links
        self.links['cv_job'].append({
            'cv_id': cv_id,
            'job_id': job_id,
            'linked_at': datetime.now().isoformat()
        })
        self._save_json('links.json', self.links)
        
        # Log activity
        self._log_activity('cv_linked', f"Linked CV {cv_id} to job {job_id}", job_id)
    
    def register_job(self, job_data: Dict, auto_search_contacts: bool = True) -> str:
        """
        Register a job and optionally find relevant contacts
        """
        job_id = job_data.get('id') or f"job_{len(self.jobs) + 1}"
        job_data['id'] = job_id
        job_data['registered_at'] = datetime.now().isoformat()
        
        # Check if already exists
        existing = [j for j in self.jobs if j.get('id') == job_id]
        if not existing:
            self.jobs.append(job_data)
            self._save_json('jobs.json', self.jobs)
        
        # Auto-find contacts at company
        if auto_search_contacts and job_data.get('company'):
            contacts = self.find_contacts_at_company(job_data['company'])
            if contacts:
                job_data['suggested_contacts'] = [c['id'] for c in contacts]
        
        # Log activity
        self._log_activity('job_added', f"Added job: {job_data.get('title', 'Unknown')} at {job_data.get('company', 'Unknown')}", job_id)
        
        return job_id
    
    def find_contacts_at_company(self, company_name: str) -> List[Dict]:
        """Find all contacts at a specific company"""
        company_lower = company_name.lower()
        matches = []
        
        for contact in self.contacts:
            contact_company = contact.get('company', '').lower()
            # Exact match or partial
            if company_lower in contact_company or contact_company in company_lower:
                matches.append(contact)
        
        return matches
    
    def get_job_context(self, job_id: str) -> Dict:
        """
        Get full context for a job: CVs, contacts, activities, timeline
        """
        job = None
        for j in self.jobs:
            if j.get('id') == job_id:
                job = j
                break
        
        if not job:
            return {'error': 'Job not found'}
        
        # Find linked CV
        linked_cv = None
        for cv in self.cvs:
            if cv.get('linked_to_job') == job_id:
                linked_cv = cv
                break
        
        # Find contacts at company
        contacts = self.find_contacts_at_company(job.get('company', ''))
        
        # Find related activities
        related_activities = [a for a in self.activities if a.get('related_id') == job_id]
        
        # Build timeline
        timeline = self._build_timeline(job_id, related_activities)
        
        return {
            'job': job,
            'linked_cv': linked_cv,
            'all_cvs_for_company': [cv for cv in self.cvs if cv.get('company', '').lower() == job.get('company', '').lower()],
            'contacts_at_company': contacts,
            'suggested_outreach': self._suggest_outreach(contacts),
            'activities': related_activities,
            'timeline': timeline,
            'next_actions': self._suggest_next_actions(job, linked_cv, contacts)
        }
    
    def _build_timeline(self, job_id: str, activities: List[Dict]) -> List[Dict]:
        """Build chronological timeline of job-related activities"""
        timeline = []
        
        # Add job creation
        job = next((j for j in self.jobs if j.get('id') == job_id), None)
        if job:
            timeline.append({
                'date': job.get('date_applied') or job.get('registered_at'),
                'type': 'job_added',
                'description': f"Applied to {job.get('title')} at {job.get('company')}"
            })
        
        # Add CV generation
        cv = next((c for c in self.cvs if c.get('linked_to_job') == job_id), None)
        if cv:
            timeline.append({
                'date': cv.get('created_at'),
                'type': 'cv_generated',
                'description': f"Generated tailored CV (ATS: {cv.get('ats_score')})"
            })
        
        # Add activities
        for activity in activities:
            timeline.append({
                'date': activity.get('timestamp'),
                'type': activity.get('type'),
                'description': activity.get('description')
            })
        
        # Sort by date
        timeline.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return timeline
    
    def _suggest_next_actions(self, job: Dict, linked_cv: Dict, contacts: List[Dict]) -> List[Dict]:
        """Suggest next actions based on job state"""
        actions = []
        
        if not linked_cv:
            actions.append({
                'priority': 'high',
                'action': 'Generate tailored CV',
                'reason': 'No CV linked to this job yet'
            })
        
        if contacts:
            actions.append({
                'priority': 'high',
                'action': f'Reach out to {contacts[0].get("name", "contact")} at {job.get("company")}',
                'reason': 'Warm connection available'
            })
        
        status = job.get('status', 'applied')
        if status == 'applied':
            actions.append({
                'priority': 'medium',
                'action': 'Schedule follow-up in 7 days',
                'reason': 'Application just submitted'
            })
        
        return actions
    
    def _suggest_outreach(self, contacts: List[Dict]) -> List[Dict]:
        """Suggest outreach messages for contacts"""
        suggestions = []
        for contact in contacts:
            suggestions.append({
                'contact': contact,
                'suggested_message': f"Hi {contact.get('name')}, I noticed you're at {contact.get('company')}. I'm applying for a role there and would love any insights you might share."
            })
        return suggestions
    
    def unified_search(self, query: str) -> Dict:
        """
        Search across all data: jobs, contacts, documents, CVs
        """
        query_lower = query.lower()
        results = {
            'jobs': [],
            'contacts': [],
            'documents': [],
            'cvs': [],
            'activities': []
        }
        
        # Search jobs
        for job in self.jobs:
            if (query_lower in job.get('company', '').lower() or
                query_lower in job.get('title', '').lower() or
                query_lower in job.get('status', '').lower()):
                results['jobs'].append(job)
        
        # Search contacts
        for contact in self.contacts:
            if (query_lower in contact.get('name', '').lower() or
                query_lower in contact.get('company', '').lower() or
                query_lower in contact.get('title', '').lower()):
                results['contacts'].append(contact)
        
        # Search documents
        for doc in self.documents:
            if (query_lower in doc.get('title', '').lower() or
                query_lower in doc.get('content', '').lower()):
                results['documents'].append(doc)
        
        # Search CVs
        for cv in self.cvs:
            if (query_lower in cv.get('company', '').lower() or
                query_lower in cv.get('title', '').lower()):
                results['cvs'].append(cv)
        
        # Search activities
        for activity in self.activities:
            if query_lower in activity.get('description', '').lower():
                results['activities'].append(activity)
        
        return results
    
    def _log_activity(self, activity_type: str, description: str, related_id: str = None):
        """Log an activity"""
        activity = {
            'id': f"act_{len(self.activities) + 1}",
            'type': activity_type,
            'description': description,
            'timestamp': datetime.now().isoformat(),
            'related_id': related_id
        }
        
        self.activities.append(activity)
        self._save_json('activities.json', self.activities)
    
    def get_dashboard_summary(self) -> Dict:
        """Get unified dashboard summary"""
        # Recent activity (last 7 days)
        week_ago = (datetime.now() - __import__('datetime').timedelta(days=7)).isoformat()
        recent_activities = [a for a in self.activities if a.get('timestamp', '') > week_ago]
        
        # Unlinked CVs
        unlinked_cvs = [cv for cv in self.cvs if not cv.get('linked_to_job')]
        
        # Jobs without CVs
        jobs_without_cv = [j for j in self.jobs if not any(cv.get('linked_to_job') == j.get('id') for cv in self.cvs)]
        
        # Contacts at applied companies
        applied_companies = set(j.get('company', '').lower() for j in self.jobs)
        contacts_at_targets = [c for c in self.contacts if any(comp in c.get('company', '').lower() for comp in applied_companies)]
        
        return {
            'totals': {
                'jobs': len(self.jobs),
                'contacts': len(self.contacts),
                'cvs': len(self.cvs),
                'documents': len(self.documents)
            },
            'recent_activity': recent_activities[:5],
            'needs_attention': {
                'unlinked_cvs': len(unlinked_cvs),
                'jobs_without_cv': len(jobs_without_cv),
                'potential_connections': len(contacts_at_targets)
            },
            'suggestions': [
                'Link unlinked CVs to jobs' if unlinked_cvs else None,
                'Generate CVs for jobs without them' if jobs_without_cv else None,
                f'Reach out to {len(contacts_at_targets)} contacts at target companies' if contacts_at_targets else None
            ]
        }

# Global coordinator instance
coordinator = DataCoordinator()
