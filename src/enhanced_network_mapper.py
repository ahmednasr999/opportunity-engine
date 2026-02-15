"""
Enhanced Network Mapper - LinkedIn integration, warm intros, relationship tracking
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class EnhancedNetworkMapper:
    """
    Advanced network management with:
    - LinkedIn contact import
    - Warm intro pathfinding
    - Relationship health tracking
    - AI conversation starters
    """
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.contacts_file = os.path.join(self.data_dir, 'enhanced_contacts.json')
        self.interactions_file = os.path.join(self.data_dir, 'interactions.json')
        
        self.contacts = self._load_json(self.contacts_file, {})
        self.interactions = self._load_json(self.interactions_file, [])
    
    def _load_json(self, filepath: str, default: Any) -> Any:
        """Load JSON file or return default"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filepath: str, data: Any):
        """Save data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def import_linkedin_contacts(self, contacts_list: List[Dict]) -> int:
        """
        Import contacts from LinkedIn export
        contacts_list: List of dicts with name, title, company, email, etc.
        """
        imported = 0
        for contact in contacts_list:
            contact_id = f"linkedin_{contact.get('email', contact.get('name', '')).replace('@', '_')}"
            
            if contact_id not in self.contacts:
                self.contacts[contact_id] = {
                    'id': contact_id,
                    'source': 'linkedin',
                    'name': contact.get('name', ''),
                    'title': contact.get('title', ''),
                    'company': contact.get('company', ''),
                    'email': contact.get('email', ''),
                    'linkedin_url': contact.get('linkedin_url', ''),
                    'phone': contact.get('phone', ''),
                    'tags': contact.get('tags', []),
                    'imported_at': datetime.now().isoformat(),
                    'last_interaction': None,
                    'interaction_count': 0,
                    'relationship_score': 50,  # 0-100
                    'warmth_level': 'cold',  # cold, warm, hot
                    'notes': '',
                    'can_introduce_to': [],  # Companies they can intro to
                    'interests': [],
                    'last_post': None
                }
                imported += 1
        
        self._save_json(self.contacts_file, self.contacts)
        return imported
    
    def find_warm_intro_path(self, target_company: str, target_person: str = None) -> List[Dict]:
        """
        Find the shortest path to someone at target company
        Returns list of contacts who can make introductions
        """
        paths = []
        
        # Direct connections
        for contact_id, contact in self.contacts.items():
            if target_company.lower() in contact.get('company', '').lower():
                paths.append({
                    'type': 'direct',
                    'connection': contact,
                    'path_length': 1,
                    'strength': contact.get('relationship_score', 0),
                    'message': f"{contact['name']} works at {target_company}"
                })
        
        # Second-degree connections (who can they introduce us to?)
        for contact_id, contact in self.contacts.items():
            can_intro = contact.get('can_introduce_to', [])
            for company in can_intro:
                if target_company.lower() in company.lower():
                    paths.append({
                        'type': 'second_degree',
                        'connection': contact,
                        'target_company': company,
                        'path_length': 2,
                        'strength': contact.get('relationship_score', 0) * 0.8,  # Slightly lower
                        'message': f"{contact['name']} can introduce you to {company}"
                    })
        
        # Sort by strength
        paths.sort(key=lambda x: x['strength'], reverse=True)
        
        return paths[:5]  # Top 5 paths
    
    def get_conversation_starter(self, contact_id: str) -> str:
        """
        Generate AI conversation starter based on contact info
        """
        contact = self.contacts.get(contact_id, {})
        
        if not contact:
            return "Hi [Name], hope you're doing well!"
        
        starters = []
        
        # Based on company news
        company = contact.get('company', '')
        if company:
            starters.append(f"Hi {contact['name']}, saw the great work {company} is doing in digital transformation. Would love to catch up!")
        
        # Based on last interaction
        last_interaction = contact.get('last_interaction')
        if last_interaction:
            days_ago = (datetime.now() - datetime.fromisoformat(last_interaction)).days
            if days_ago > 90:
                starters.append(f"Hi {contact['name']}, it's been a while! Would love to reconnect and hear what you're working on at {company}.")
            else:
                starters.append(f"Hi {contact['name']}, following up on our conversation from {days_ago} days ago. Any updates on [topic]"))
        else:
            # First outreach
            title = contact.get('title', '')
            if 'recruiter' in title.lower():
                starters.append(f"Hi {contact['name']}, I'm exploring new HealthTech leadership opportunities and would value your insights. Any chance for a brief chat?")
            elif 'vp' in title.lower() or 'director' in title.lower() or 'head' in title.lower():
                starters.append(f"Hi {contact['name']}, impressed by your work at {company}. I'd love to learn about your digital transformation journey. Open to a brief conversation?")
            else:
                starters.append(f"Hi {contact['name']}, I came across your profile and was impressed by your background in {contact.get('industry', 'the industry')}. Would love to connect!")
        
        # Based on common interests
        interests = contact.get('interests', [])
        if interests:
            starters.append(f"Hi {contact['name']}, saw your post about {interests[0]}. Really resonated with your perspective on the industry!")
        
        # Return the most appropriate starter
        return starters[0] if starters else f"Hi {contact['name']}, hope you're doing well!"
    
    def track_interaction(self, contact_id: str, interaction_type: str, notes: str = '', metadata: Dict = None):
        """
        Track an interaction with a contact
        """
        if contact_id not in self.contacts:
            return False
        
        interaction = {
            'id': f"int_{len(self.interactions) + 1}",
            'contact_id': contact_id,
            'type': interaction_type,  # email, call, meeting, linkedin_message
            'date': datetime.now().isoformat(),
            'notes': notes,
            'metadata': metadata or {}
        }
        
        self.interactions.append(interaction)
        
        # Update contact
        self.contacts[contact_id]['last_interaction'] = interaction['date']
        self.contacts[contact_id]['interaction_count'] = self.contacts[contact_id].get('interaction_count', 0) + 1
        
        # Update relationship score
        current_score = self.contacts[contact_id].get('relationship_score', 50)
        if interaction_type in ['meeting', 'call']:
            new_score = min(current_score + 5, 100)
        elif interaction_type == 'email':
            new_score = min(current_score + 2, 100)
        else:
            new_score = min(current_score + 1, 100)
        
        self.contacts[contact_id]['relationship_score'] = new_score
        
        # Update warmth level
        if new_score >= 80:
            self.contacts[contact_id]['warmth_level'] = 'hot'
        elif new_score >= 50:
            self.contacts[contact_id]['warmth_level'] = 'warm'
        
        self._save_json(self.interactions_file, self.interactions)
        self._save_json(self.contacts_file, self.contacts)
        
        return True
    
    def get_relationship_health(self, contact_id: str) -> Dict:
        """
        Get relationship health metrics
        """
        contact = self.contacts.get(contact_id, {})
        if not contact:
            return {}
        
        last_interaction = contact.get('last_interaction')
        if last_interaction:
            days_since = (datetime.now() - datetime.fromisoformat(last_interaction)).days
        else:
            days_since = 999
        
        score = contact.get('relationship_score', 0)
        
        # Determine status
        if days_since > 180:
            status = 'at_risk'
            action = 'Reconnect urgently'
        elif days_since > 90:
            status = 'needs_attention'
            action = 'Schedule catch-up'
        elif days_since > 30:
            status = 'healthy'
            action = 'Maintain relationship'
        else:
            status = 'strong'
            action = 'Keep momentum'
        
        return {
            'contact': contact,
            'relationship_score': score,
            'days_since_last_contact': days_since,
            'interaction_count': contact.get('interaction_count', 0),
            'warmth_level': contact.get('warmth_level', 'cold'),
            'status': status,
            'recommended_action': action,
            'next_interaction_suggestion': self.get_conversation_starter(contact_id)
        }
    
    def get_outreach_recommendations(self) -> List[Dict]:
        """
        Get prioritized list of who to contact
        """
        recommendations = []
        
        for contact_id, contact in self.contacts.items():
            health = self.get_relationship_health(contact_id)
            
            # Skip if contacted recently
            if health['days_since_last_contact'] < 7:
                continue
            
            # Calculate priority score
            priority = 0
            reasons = []
            
            # High-value contacts need more attention
            if contact.get('warmth_level') == 'hot':
                priority += 50
                reasons.append('Strong relationship')
            
            if contact.get('can_introduce_to'):
                priority += 30
                reasons.append('Can make introductions')
            
            if 'recruiter' in contact.get('title', '').lower():
                priority += 40
                reasons.append('Recruiter - job opportunity')
            
            if health['days_since_last_contact'] > 90:
                priority += 20
                reasons.append('Overdue for contact')
            
            if priority > 0:
                recommendations.append({
                    'contact': contact,
                    'priority_score': priority,
                    'reasons': reasons,
                    'health': health,
                    'suggested_message': self.get_conversation_starter(contact_id)
                })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return recommendations[:10]  # Top 10
    
    def get_network_stats(self) -> Dict:
        """
        Get comprehensive network statistics
        """
        total = len(self.contacts)
        
        by_warmth = {'cold': 0, 'warm': 0, 'hot': 0}
        by_source = {}
        by_company = {}
        
        for contact in self.contacts.values():
            # By warmth
            warmth = contact.get('warmth_level', 'cold')
            by_warmth[warmth] = by_warmth.get(warmth, 0) + 1
            
            # By source
            source = contact.get('source', 'manual')
            by_source[source] = by_source.get(source, 0) + 1
            
            # By company
            company = contact.get('company', 'Unknown')
            by_company[company] = by_company.get(company, 0) + 1
        
        # Recent interactions
        recent_interactions = [
            i for i in self.interactions
            if (datetime.now() - datetime.fromisoformat(i['date'])).days <= 30
        ]
        
        return {
            'total_contacts': total,
            'by_warmth': by_warmth,
            'by_source': by_source,
            'top_companies': sorted(by_company.items(), key=lambda x: x[1], reverse=True)[:10],
            'recent_interactions': len(recent_interactions),
            'avg_relationship_score': sum(c.get('relationship_score', 0) for c in self.contacts.values()) / total if total else 0,
            'needs_follow_up': len([c for c in self.contacts.values() if self._needs_follow_up(c)])
        }
    
    def _needs_follow_up(self, contact: Dict) -> bool:
        """Check if contact needs follow up"""
        last = contact.get('last_interaction')
        if not last:
            return True
        days = (datetime.now() - datetime.fromisoformat(last)).days
        return days > 90
