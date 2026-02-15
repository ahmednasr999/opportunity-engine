#!/usr/bin/env python3
"""
Network Mapper - Executive Relationship Management
Tracks recruiters, referrals, and decision-makers for executive job search
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import uuid

@dataclass
class Contact:
    """A professional contact"""
    id: str
    name: str
    title: str
    company: str
    sector: str  # HealthTech, FinTech, ExecutiveSearch, etc.
    contact_type: str  # recruiter, hiring_manager, referral, peer, influencer
    email: str
    phone: str
    linkedin: str
    source: str  # How you met them
    relationship_score: int  # 1-10, strength of relationship
    last_contact_date: str
    next_follow_up: str
    notes: str
    tags: List[str]
    interactions: List[Dict]
    opportunities: List[str]  # Linked job IDs
    created_at: str
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Contact':
        return cls(**data)


@dataclass
class Interaction:
    """A touchpoint with a contact"""
    id: str
    contact_id: str
    interaction_type: str  # email, call, meeting, linkedin, intro
    date: str
    summary: str
    outcome: str
    next_steps: str
    follow_up_date: str
    sentiment: str  # positive, neutral, negative


class NetworkMapper:
    """Map and nurture professional relationships"""
    
    def __init__(self, data_dir: str = "/root/.openclaw/workspace/tools/cv-optimizer/data"):
        self.data_dir = Path(data_dir)
        self.contacts_file = self.data_dir / "network.json"
        self.interactions_file = self.data_dir / "interactions.json"
        self.contacts: Dict[str, Contact] = {}
        self.interactions: Dict[str, List[Interaction]] = {}
        self.load()
    
    def load(self):
        """Load network data"""
        if self.contacts_file.exists():
            with open(self.contacts_file, 'r') as f:
                data = json.load(f)
                for contact_data in data.get('contacts', []):
                    contact = Contact.from_dict(contact_data)
                    self.contacts[contact.id] = contact
        
        if self.interactions_file.exists():
            with open(self.interactions_file, 'r') as f:
                self.interactions = json.load(f)
    
    def save(self):
        """Save network data"""
        with open(self.contacts_file, 'w') as f:
            json.dump({
                'contacts': [c.to_dict() for c in self.contacts.values()],
                'updated_at': datetime.now().isoformat()
            }, f, indent=2)
        
        with open(self.interactions_file, 'w') as f:
            json.dump(self.interactions, f, indent=2)
    
    def add_contact(self, 
                   name: str,
                   title: str,
                   company: str,
                   contact_type: str = "peer",
                   sector: str = "",
                   email: str = "",
                   phone: str = "",
                   linkedin: str = "",
                   source: str = "",
                   relationship_score: int = 5,
                   notes: str = "") -> Contact:
        """Add a new contact"""
        
        contact = Contact(
            id=str(uuid.uuid4())[:8],
            name=name,
            title=title,
            company=company,
            sector=sector or self._infer_sector(company),
            contact_type=contact_type,
            email=email,
            phone=phone,
            linkedin=linkedin,
            source=source,
            relationship_score=relationship_score,
            last_contact_date=datetime.now().isoformat(),
            next_follow_up=(datetime.now() + timedelta(days=30)).isoformat(),
            notes=notes,
            tags=[contact_type, sector],
            interactions=[],
            opportunities=[],
            created_at=datetime.now().isoformat()
        )
        
        self.contacts[contact.id] = contact
        self.interactions[contact.id] = []
        self.save()
        return contact
    
    def _infer_sector(self, company: str) -> str:
        """Infer sector from company name"""
        company_lower = company.lower()
        health_keywords = ['hospital', 'health', 'medical', 'clinic', 'care', 'pharma']
        fintech_keywords = ['bank', 'finance', 'payment', 'fintech', 'insurance']
        tech_keywords = ['tech', 'software', 'digital', 'ai', 'data']
        
        if any(k in company_lower for k in health_keywords):
            return "HealthTech"
        elif any(k in company_keywords for k in fintech_keywords):
            return "FinTech"
        elif any(k in company_lower for k in tech_keywords):
            return "Technology"
        return "Other"
    
    def add_interaction(self, 
                       contact_id: str,
                       interaction_type: str,
                       summary: str,
                       outcome: str = "",
                       next_steps: str = "",
                       follow_up_days: int = 14,
                       sentiment: str = "positive") -> Optional[Interaction]:
        """Log an interaction with a contact"""
        
        if contact_id not in self.contacts:
            return None
        
        contact = self.contacts[contact_id]
        
        interaction = Interaction(
            id=str(uuid.uuid4())[:8],
            contact_id=contact_id,
            interaction_type=interaction_type,
            date=datetime.now().isoformat(),
            summary=summary,
            outcome=outcome,
            next_steps=next_steps,
            follow_up_date=(datetime.now() + timedelta(days=follow_up_days)).isoformat(),
            sentiment=sentiment
        )
        
        # Update contact
        contact.interactions.append(asdict(interaction))
        contact.last_contact_date = interaction.date
        contact.next_follow_up = interaction.follow_up_date
        
        # Update relationship score based on sentiment
        if sentiment == "positive":
            contact.relationship_score = min(10, contact.relationship_score + 1)
        elif sentiment == "negative":
            contact.relationship_score = max(1, contact.relationship_score - 1)
        
        self.save()
        return interaction
    
    def link_opportunity(self, contact_id: str, job_id: str):
        """Link a contact to a job opportunity"""
        if contact_id in self.contacts:
            if job_id not in self.contacts[contact_id].opportunities:
                self.contacts[contact_id].opportunities.append(job_id)
                self.save()
    
    def get_follow_ups(self, days: int = 7) -> List[Contact]:
        """Get contacts needing follow-up"""
        cutoff = datetime.now() + timedelta(days=days)
        follow_ups = []
        
        for contact in self.contacts.values():
            next_follow = datetime.fromisoformat(contact.next_follow_up)
            if next_follow <= cutoff:
                follow_ups.append(contact)
        
        return sorted(follow_ups, key=lambda c: c.next_follow_up)
    
    def get_by_type(self, contact_type: str) -> List[Contact]:
        """Get contacts by type"""
        return [c for c in self.contacts.values() if c.contact_type == contact_type]
    
    def get_by_sector(self, sector: str) -> List[Contact]:
        """Get contacts by sector"""
        return [c for c in self.contacts.values() if c.sector.lower() == sector.lower()]
    
    def get_warm_intros(self, target_company: str) -> List[Contact]:
        """Find contacts who can intro to a target company"""
        warm_intros = []
        
        for contact in self.contacts.values():
            # Direct connection
            if target_company.lower() in contact.company.lower():
                if contact.relationship_score >= 6:
                    warm_intros.append(contact)
            # Referral source
            elif contact.contact_type == "referral" and contact.relationship_score >= 7:
                warm_intros.append(contact)
        
        return sorted(warm_intros, key=lambda c: c.relationship_score, reverse=True)
    
    def get_recruiter_pipeline(self) -> Dict:
        """Get recruiters and their active opportunities"""
        recruiters = self.get_by_type("recruiter")
        pipeline = {}
        
        for recruiter in recruiters:
            pipeline[recruiter.id] = {
                "recruiter": recruiter,
                "active_opportunities": len(recruiter.opportunities),
                "last_contact": recruiter.last_contact_date,
                "relationship_score": recruiter.relationship_score
            }
        
        return pipeline
    
    def search(self, query: str) -> List[Contact]:
        """Search contacts"""
        query = query.lower()
        results = []
        
        for contact in self.contacts.values():
            if (query in contact.name.lower() or 
                query in contact.company.lower() or 
                query in contact.title.lower() or
                query in contact.notes.lower() or
                any(query in tag.lower() for tag in contact.tags)):
                results.append(contact)
        
        return results
    
    def get_stats(self) -> Dict:
        """Get network statistics"""
        total = len(self.contacts)
        by_type = {}
        by_sector = {}
        relationship_dist = {"weak": 0, "medium": 0, "strong": 0}
        
        for contact in self.contacts.values():
            by_type[contact.contact_type] = by_type.get(contact.contact_type, 0) + 1
            by_sector[contact.sector] = by_sector.get(contact.sector, 0) + 1
            
            if contact.relationship_score <= 4:
                relationship_dist["weak"] += 1
            elif contact.relationship_score <= 7:
                relationship_dist["medium"] += 1
            else:
                relationship_dist["strong"] += 1
        
        follow_ups_needed = len(self.get_follow_ups(7))
        
        return {
            "total_contacts": total,
            "by_type": by_type,
            "by_sector": by_sector,
            "relationship_distribution": relationship_dist,
            "follow_ups_needed": follow_ups_needed,
            "strong_relationships": relationship_dist["strong"]
        }
    
    def suggest_outreach(self, target_role: str = "VP", target_sector: str = "HealthTech") -> List[Dict]:
        """Suggest contacts to reach out to based on goals"""
        suggestions = []
        
        for contact in self.contacts.values():
            score = 0
            reason = []
            
            # High relationship score but not contacted recently
            if contact.relationship_score >= 7:
                days_since = (datetime.now() - datetime.fromisoformat(contact.last_contact_date)).days
                if days_since > 30:
                    score += 10
                    reason.append("Strong relationship, stale")
            
            # Sector match
            if target_sector.lower() in contact.sector.lower():
                score += 15
                reason.append(f"In {target_sector}")
            
            # Decision maker
            if contact.contact_type in ["hiring_manager", "recruiter"]:
                score += 20
                reason.append("Decision maker")
            
            # Has opportunities
            if len(contact.opportunities) > 0:
                score += 5
                reason.append("Active opportunities")
            
            if score >= 20:
                suggestions.append({
                    "contact": contact,
                    "score": score,
                    "reason": ", ".join(reason)
                })
        
        return sorted(suggestions, key=lambda x: x["score"], reverse=True)


def print_network_stats(mapper: NetworkMapper):
    """Print network statistics"""
    stats = mapper.get_stats()
    
    print("\n" + "=" * 60)
    print("NETWORK STATISTICS")
    print("=" * 60)
    print(f"\n👥 Total Contacts: {stats['total_contacts']}")
    print(f"🔔 Follow-ups Needed: {stats['follow_ups_needed']}")
    print(f"💪 Strong Relationships: {stats['strong_relationships']}")
    
    print("\n📊 By Type:")
    for contact_type, count in sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True):
        emoji = {"recruiter": "🎯", "hiring_manager": "💼", "referral": "🔗", "peer": "👤", "influencer": "⭐"}.get(contact_type, "👤")
        print(f"  {emoji} {contact_type.title()}: {count}")
    
    print("\n🏭 By Sector:")
    for sector, count in sorted(stats['by_sector'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {sector}: {count}")


def print_follow_ups(mapper: NetworkMapper):
    """Print follow-up reminders"""
    follow_ups = mapper.get_follow_ups()
    
    if follow_ups:
        print("\n" + "=" * 60)
        print("🔔 FOLLOW-UPS NEEDED")
        print("=" * 60)
        
        for contact in follow_ups[:10]:
            days_overdue = (datetime.now() - datetime.fromisoformat(contact.next_follow_up)).days
            emoji = "🔴" if days_overdue > 0 else "🟡"
            status = f"{days_overdue} days overdue" if days_overdue > 0 else f"Due in {abs(days_overdue)} days"
            
            print(f"\n{emoji} {contact.name}")
            print(f"   {contact.title} at {contact.company}")
            print(f"   Type: {contact.contact_type} | Score: {contact.relationship_score}/10")
            print(f"   Status: {status}")
            if contact.notes:
                print(f"   Notes: {contact.notes[:80]}...")


def print_suggestions(mapper: NetworkMapper):
    """Print outreach suggestions"""
    suggestions = mapper.suggest_outreach()
    
    if suggestions:
        print("\n" + "=" * 60)
        print("💡 SUGGESTED OUTREACH")
        print("=" * 60)
        
        for sug in suggestions[:5]:
            contact = sug["contact"]
            print(f"\n🎯 {contact.name} (Score: {sug['score']})")
            print(f"   {contact.title} at {contact.company}")
            print(f"   Why: {sug['reason']}")
            print(f"   Last contact: {contact.last_contact_date[:10]}")


def main():
    """CLI interface"""
    import sys
    
    mapper = NetworkMapper()
    
    if len(sys.argv) < 2:
        print_network_stats(mapper)
        print_follow_ups(mapper)
        print_suggestions(mapper)
        return
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 5:
            print("Usage: python network_mapper.py add 'Name' 'Title' 'Company' [type] [sector]")
            return
        
        name = sys.argv[2]
        title = sys.argv[3]
        company = sys.argv[4]
        contact_type = sys.argv[5] if len(sys.argv) > 5 else "peer"
        sector = sys.argv[6] if len(sys.argv) > 6 else ""
        
        contact = mapper.add_contact(name, title, company, contact_type, sector)
        print(f"✅ Added contact: [{contact.id}] {name} at {company}")
    
    elif command == "interact":
        if len(sys.argv) < 5:
            print("Usage: python network_mapper.py interact <contact_id> <type> 'Summary'")
            return
        
        contact_id = sys.argv[2]
        interaction_type = sys.argv[3]
        summary = sys.argv[4]
        
        interaction = mapper.add_interaction(contact_id, interaction_type, summary)
        if interaction:
            print(f"✅ Logged {interaction_type} with [{contact_id}]")
        else:
            print(f"❌ Contact not found: {contact_id}")
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: python network_mapper.py search <query>")
            return
        
        query = sys.argv[2]
        results = mapper.search(query)
        
        print(f"\n🔍 Search results for '{query}':")
        for contact in results:
            print(f"  [{contact.id}] {contact.name} - {contact.title} at {contact.company}")
    
    elif command == "warm":
        if len(sys.argv) < 3:
            print("Usage: python network_mapper.py warm 'Company Name'")
            return
        
        company = sys.argv[2]
        intros = mapper.get_warm_intros(company)
        
        print(f"\n🌡️ Warm intros to {company}:")
        for contact in intros:
            print(f"  [{contact.id}] {contact.name} - {contact.title}")
            print(f"      Relationship: {contact.relationship_score}/10")
    
    elif command == "stats":
        print_network_stats(mapper)
    
    elif command == "followups":
        print_follow_ups(mapper)
    
    elif command == "suggest":
        print_suggestions(mapper)
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
