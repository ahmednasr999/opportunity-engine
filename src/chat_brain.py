"""
ChatBrain - Conversational AI interface for 2nd Brain
Ask questions in natural language, get intelligent answers
"""
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class ChatBrain:
    """
    Conversational interface to all your data:
    - Jobs applied to
    - Network contacts
    - Documents and CVs
    - Calendar events
    - Analytics and insights
    
    Ask: "What jobs did I apply to last week?"
    Ask: "Who can introduce me to Google?"
    Ask: "When is my next interview?"
    """
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.context = {}  # Conversation context
        
        # Load all data sources
        self.jobs = self._load_json(os.path.join(self.data_dir, 'jobs.json'), [])
        self.contacts = self._load_json(os.path.join(self.data_dir, 'contacts.json'), [])
        self.documents = self._load_json(os.path.join(self.data_dir, 'documents.json'), [])
        self.calendar = self._load_json(os.path.join(self.data_dir, 'calendar_events.json'), [])
        self.expenses = self._load_json(os.path.join(self.data_dir, 'expenses.json'), [])
        self.bookmarks = self._load_json(os.path.join(self.data_dir, 'bookmarks.json'), [])
    
    def _load_json(self, filepath: str, default):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def process_query(self, query: str) -> Dict:
        """
        Process natural language query and return answer
        """
        query_lower = query.lower()
        
        # Intent detection
        intent, entities = self._detect_intent(query_lower)
        
        # Route to appropriate handler
        handlers = {
            'job_search': self._handle_job_query,
            'contact_search': self._handle_contact_query,
            'calendar_query': self._handle_calendar_query,
            'document_search': self._handle_document_query,
            'analytics_query': self._handle_analytics_query,
            'introduction_request': self._handle_introduction_request,
            'action_request': self._handle_action_request,
            'general_question': self._handle_general_question
        }
        
        handler = handlers.get(intent, self._handle_general_question)
        response = handler(entities, query)
        
        return {
            'query': query,
            'intent': intent,
            'response': response['text'],
            'data': response.get('data'),
            'suggested_actions': response.get('actions', [])
        }
    
    def _detect_intent(self, query: str) -> Tuple[str, Dict]:
        """Detect user intent and extract entities"""
        entities = {}
        
        # Job-related queries
        job_patterns = [
            r'(?:what|which|how many) jobs (?:did i|have i) (?:apply|applied)',
            r'(?:show|list) (?:my )?jobs',
            r'where (?:did i|have i) applied',
            r'job (?:status|update)',
            r'(?:any|new) (?:interview|offer)',
            r'(?:applied|application) (?:last|this) (?:week|month)'
        ]
        
        for pattern in job_patterns:
            if re.search(pattern, query):
                # Extract time frame
                if 'last week' in query:
                    entities['timeframe'] = 'last_week'
                elif 'this week' in query:
                    entities['timeframe'] = 'this_week'
                elif 'last month' in query:
                    entities['timeframe'] = 'last_month'
                
                # Extract status
                if 'interview' in query:
                    entities['status'] = 'interview'
                elif 'offer' in query:
                    entities['status'] = 'offer'
                
                return 'job_search', entities
        
        # Contact/introduction queries
        contact_patterns = [
            r'(?:who|whom) (?:can|could) (?:introduce|connect)',
            r'(?:do you|anyone) know (?:someone|anyone) at',
            r'(?:contact|reach out to) (?:someone|anyone) at',
            r'(?:find|search for) (?:contact|person) at',
            r'(?:network|connection) at'
        ]
        
        for pattern in contact_patterns:
            if re.search(pattern, query):
                # Extract company
                companies = self._extract_company(query)
                if companies:
                    entities['target_company'] = companies[0]
                return 'introduction_request', entities
        
        # Calendar queries
        calendar_patterns = [
            r'(?:when|what time) (?:is|are) (?:my|the) (?:interview|meeting)',
            r'(?:what|anything) (?:scheduled|coming up|on my calendar)',
            r'(?:next|upcoming) (?:interview|event|meeting)',
            r'(?:do i have|am i) (?:busy|free|available)'
        ]
        
        for pattern in calendar_patterns:
            if re.search(pattern, query):
                if 'tomorrow' in query:
                    entities['date'] = 'tomorrow'
                elif 'today' in query:
                    entities['date'] = 'today'
                elif 'this week' in query:
                    entities['date'] = 'this_week'
                return 'calendar_query', entities
        
        # Document/CV queries
        document_patterns = [
            r'(?:find|search|where is) (?:my|the) (?:cv|resume|document)',
            r'(?:show|list) (?:my )?(?:documents|cvs|files)',
            r'(?:what|which) (?:version|cv) (?:did i|have i) (?:send|sent|use)'
        ]
        
        for pattern in document_patterns:
            if re.search(pattern, query):
                if 'google' in query or 'amazon' in query:
                    entities['company'] = self._extract_company(query)[0] if self._extract_company(query) else None
                return 'document_search', entities
        
        # Analytics/insights queries
        analytics_patterns = [
            r'(?:how am i|what is my) (?:doing|progress|status)',
            r'(?:analytics|statistics|metrics|numbers)',
            r'(?:success|interview|offer) (?:rate|chance|probability)',
            r'(?:should i|recommendation) (?:apply|focus|prioritize)'
        ]
        
        for pattern in analytics_patterns:
            if re.search(pattern, query):
                return 'analytics_query', entities
        
        # Action requests
        action_patterns = [
            r'(?:remind me|set reminder|schedule)',
            r'(?:add|create) (?:job|contact|event)',
            r'(?:send|write) (?:email|follow.?up)',
            r'(?:generate|create) (?:cv|cover letter)'
        ]
        
        for pattern in action_patterns:
            if re.search(pattern, query):
                return 'action_request', entities
        
        # Default
        return 'general_question', entities
    
    def _extract_company(self, text: str) -> List[str]:
        """Extract company names from text"""
        # Simple extraction - look for capitalized words
        # In production, this would use NER
        words = text.split()
        companies = []
        
        for i, word in enumerate(words):
            if word[0].isupper() and len(word) > 2:
                if i > 0 and words[i-1].lower() in ['at', 'to', 'for', 'from']:
                    companies.append(word)
        
        return companies
    
    def _handle_job_query(self, entities: Dict, original_query: str) -> Dict:
        """Handle job-related queries"""
        timeframe = entities.get('timeframe', 'all')
        status_filter = entities.get('status')
        
        # Filter jobs
        filtered = self.jobs
        
        if timeframe == 'last_week':
            from datetime import datetime, timedelta
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()
            filtered = [j for j in filtered if j.get('date_applied', '') > week_ago]
        elif timeframe == 'this_week':
            from datetime import datetime, timedelta
            week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).isoformat()
            filtered = [j for j in filtered if j.get('date_applied', '') >= week_start]
        
        if status_filter:
            filtered = [j for j in filtered if j.get('status') == status_filter]
        
        # Build response
        count = len(filtered)
        
        if count == 0:
            return {
                'text': f"I don't see any jobs matching your query. Would you like to add a new job application?",
                'actions': ['Add job', 'Search all jobs']
            }
        
        job_list = "\n".join([f"• {j.get('company', 'Unknown')} - {j.get('title', 'Unknown')} ({j.get('status', 'unknown')})" 
                             for j in filtered[:5]])
        
        return {
            'text': f"I found {count} job(s) matching your query:\n\n{job_list}",
            'data': filtered,
            'actions': ['View all', 'Add follow-up', 'Generate CV']
        }
    
    def _handle_contact_query(self, entities: Dict, original_query: str) -> Dict:
        """Handle contact-related queries"""
        # Search contacts
        contacts = self.contacts[:5]  # Top 5 for demo
        
        contact_list = "\n".join([f"• {c.get('name', 'Unknown')} - {c.get('title', '')} at {c.get('company', '')}" 
                                 for c in contacts])
        
        return {
            'text': f"Here are some of your contacts:\n\n{contact_list}",
            'data': contacts,
            'actions': ['Add contact', 'Search network', 'Find warm intros']
        }
    
    def _handle_introduction_request(self, entities: Dict, original_query: str) -> Dict:
        """Handle requests for introductions"""
        target_company = entities.get('target_company', '').lower()
        
        if not target_company:
            return {
                'text': "Which company would you like an introduction to?",
                'actions': ['Search companies', 'Browse network']
            }
        
        # Search for connections at target company
        connections = [c for c in self.contacts if target_company in c.get('company', '').lower()]
        
        if connections:
            connection = connections[0]
            return {
                'text': f"Great! I found someone who can help:\n\n{connection.get('name')} works at {connection.get('company')} as {connection.get('title')}.\n\nWould you like me to draft an introduction message?",
                'data': connection,
                'actions': ['Draft message', 'View profile', 'Find another contact']
            }
        else:
            # Look for second-degree connections
            return {
                'text': f"I don't see any direct connections at {target_company.title()}. Let me search for people who might know someone there...",
                'actions': ['Search extended network', 'Add target company', 'Browse recruiters']
            }
    
    def _handle_calendar_query(self, entities: Dict, original_query: str) -> Dict:
        """Handle calendar-related queries"""
        upcoming = [e for e in self.calendar if e.get('status') != 'completed'][:5]
        
        if not upcoming:
            return {
                'text': "You don't have any upcoming events on your calendar.",
                'actions': ['Add interview', 'View calendar', 'Schedule follow-up']
            }
        
        event_list = "\n".join([f"• {e.get('title', 'Unknown')} - {e.get('start_time', 'TBD')[:10]}" 
                               for e in upcoming[:3]])
        
        return {
            'text': f"Here are your upcoming events:\n\n{event_list}",
            'data': upcoming,
            'actions': ['View calendar', 'Add event', 'Set reminder']
        }
    
    def _handle_document_query(self, entities: Dict, original_query: str) -> Dict:
        """Handle document-related queries"""
        docs = self.documents[:5]
        
        if not docs:
            return {
                'text': "I don't see any documents in your system yet.",
                'actions': ['Upload CV', 'Add document', 'Generate new CV']
            }
        
        doc_list = "\n".join([f"• {d.get('title', 'Unknown')} ({d.get('doc_type', 'document')})" 
                             for d in docs])
        
        return {
            'text': f"Here are your documents:\n\n{doc_list}",
            'data': docs,
            'actions': ['View all', 'Search documents', 'Upload new']
        }
    
    def _handle_analytics_query(self, entities: Dict, original_query: str) -> Dict:
        """Handle analytics and insights queries"""
        total_jobs = len(self.jobs)
        interviews = len([j for j in self.jobs if j.get('status') in ['interview', 'offer']])
        offers = len([j for j in self.jobs if j.get('status') == 'offer'])
        
        response = f"""Here's your current status:

📊 **Applications:** {total_jobs} jobs applied
🎯 **Interviews:** {interviews} ({interviews/total_jobs*100:.1f}% rate) if total_jobs > 0 else 0
💼 **Offers:** {offers}

**Recommendations:**
"""
        
        if total_jobs < 10:
            response += "• Apply to more jobs (target: 5 per week)\n"
        if interviews == 0 and total_jobs > 5:
            response += "• Review your CV quality - aim for ATS scores 85+\n"
        
        response += "• Keep networking and following up\n"
        
        return {
            'text': response,
            'actions': ['View detailed analytics', 'Generate report', 'Set goals']
        }
    
    def _handle_action_request(self, entities: Dict, original_query: str) -> Dict:
        """Handle action requests"""
        return {
            'text': "I can help you with that. What would you like to do?",
            'actions': ['Add job application', 'Schedule interview', 'Send follow-up email', 'Generate CV']
        }
    
    def _handle_general_question(self, entities: Dict, original_query: str) -> Dict:
        """Handle general questions"""
        responses = [
            "I'm here to help you with your job search! You can ask me things like:\n\n• What jobs did I apply to last week?\n• Who can introduce me to Google?\n• When is my next interview?\n• How am I doing with my applications?\n• Generate a CV for a HealthTech role",
            "I can help you track jobs, manage your network, prepare for interviews, and analyze your progress. What would you like to know?",
            "I'm your job search assistant! Try asking me about your applications, network connections, upcoming interviews, or documents."
        ]
        
        import random
        return {
            'text': random.choice(responses),
            'actions': ['View dashboard', 'Add job', 'Browse network', 'View analytics']
        }
    
    def get_suggested_queries(self) -> List[str]:
        """Get suggested queries for the user"""
        return [
            "What jobs did I apply to this week?",
            "Who can introduce me to [company]?",
            "When is my next interview?",
            "How many applications do I have?",
            "Generate a CV for a VP Digital Transformation role",
            "What should I focus on this week?",
            "Show me my network in HealthTech",
            "What's my interview success rate?"
        ]
