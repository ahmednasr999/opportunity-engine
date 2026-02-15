#!/usr/bin/env python3
"""
Opportunity Engine - Master integration of CV Optimizer, Job Tracker, Content Factory, and 2nd Brain
"""

import sys
import argparse
from pathlib import Path
from typing import Dict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cv_optimizer import CVGenerator, ProfileDatabase, JDParser, ATSScorer
from job_tracker import JobTracker, print_pipeline, print_stats, print_follow_ups
from content_factory import ContentFactory
from second_brain import SecondBrain


class OpportunityEngine:
    """Master integration of all tools"""
    
    def __init__(self):
        print("🚀 Initializing Opportunity Engine...")
        self.profile = ProfileDatabase()
        self.cv_gen = CVGenerator(self.profile)
        self.job_tracker = JobTracker()
        self.content_factory = ContentFactory()
        self.brain = SecondBrain()
        print("✅ All systems ready\n")
    
    def optimize_cv_for_job(self, job_text: str, company: str, title: str) -> Dict:
        """Complete workflow: Parse job → Generate CV → Track application"""
        print(f"📄 Processing: {title} at {company}")
        print("-" * 60)
        
        # 1. Generate tailored CV
        print("📝 Generating tailored CV...")
        tailored_cv = self.cv_gen.generate(job_text, title, company)
        
        # 2. Save CV
        output = self.cv_gen.export_to_text(tailored_cv)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cv_{company.replace(' ', '_')}_{timestamp}.txt"
        filepath = Path("/root/.openclaw/workspace/tools/cv-optimizer/output") / filename
        
        with open(filepath, 'w') as f:
            f.write(output)
        
        print(f"✅ CV saved: {filepath}")
        print(f"🎯 ATS Score: {tailored_cv.ats_score}/100")
        
        # 3. Add to job tracker
        print("📊 Adding to job tracker...")
        job = self.job_tracker.add_job(
            company=company,
            title=title,
            cv_version=str(filepath),
            ats_score=tailored_cv.ats_score,
            sector=self._detect_sector(job_text),
            notes=f"Generated via Opportunity Engine. ATS: {tailored_cv.ats_score}"
        )
        print(f"✅ Tracked: [{job.id}] {title}")
        
        # 4. Ingest to 2nd Brain
        print("🧠 Adding to knowledge base...")
        job_doc_id = self.brain.ingest_job_posting(job_text, company, title)
        print(f"✅ Indexed: {job_doc_id}")
        
        # 5. Show suggestions
        if tailored_cv.suggestions:
            print("\n💡 Suggestions:")
            for suggestion in tailored_cv.suggestions[:3]:
                print(f"   {suggestion}")
        
        return {
            "job_id": job.id,
            "cv_path": str(filepath),
            "ats_score": tailored_cv.ats_score,
            "suggestions": tailored_cv.suggestions
        }
    
    def _detect_sector(self, job_text: str) -> str:
        """Detect job sector from text"""
        text_lower = job_text.lower()
        health_keywords = ["healthcare", "health", "medical", "clinical", "hospital", "patient"]
        fintech_keywords = ["fintech", "banking", "payments", "financial"]
        
        health_count = sum(1 for k in health_keywords if k in text_lower)
        fintech_count = sum(1 for k in fintech_keywords if k in text_lower)
        
        if health_count > fintech_count:
            return "HealthTech"
        elif fintech_count > health_count:
            return "FinTech"
        return "Technology"
    
    def dashboard(self):
        """Show full dashboard"""
        print("\n" + "=" * 80)
        print("OPPORTUNITY ENGINE DASHBOARD")
        print("=" * 80)
        
        # Job stats
        print_stats(self.job_tracker)
        
        # Pipeline
        print_pipeline(self.job_tracker)
        
        # Follow-ups
        print_follow_ups(self.job_tracker)
        
        # Brain stats
        brain_stats = self.brain.get_stats()
        print("\n" + "=" * 80)
        print("KNOWLEDGE BASE")
        print("=" * 80)
        print(f"Documents: {brain_stats['total_documents']}")
        print(f"Unique Terms: {brain_stats['unique_terms']}")
    
    def content_pipeline(self, topic: str = "healthtech_ai"):
        """Generate content for the week"""
        print("\n" + "=" * 80)
        print("CONTENT PIPELINE")
        print("=" * 80)
        
        # Generate LinkedIn post
        print("\n📝 Generating LinkedIn post...")
        post = self.content_factory.generate_linkedin_post(topic)
        print(f"   Characters: {post['character_count']}")
        print(f"   Template: {post['template']}")
        
        # Save
        filepath = self.content_factory.save_content(post)
        print(f"   Saved: {filepath}")
        
        # Generate newsletter
        print("\n📧 Generating newsletter...")
        newsletter = self.content_factory.generate_newsletter("weekly_roundup")
        print(f"   Words: {newsletter['word_count']}")
        print(f"   Subject: {newsletter.get('subject', 'N/A')}")
        
        # Save
        filepath = self.content_factory.save_content(newsletter, f"newsletter_{topic}.md")
        print(f"   Saved: {filepath}")
    
    def search_brain(self, query: str):
        """Search knowledge base"""
        results = self.brain.search(query, top_k=5)
        
        print(f"\n🔍 Search: '{query}'")
        print("=" * 60)
        
        for i, result in enumerate(results, 1):
            doc = result.document
            print(f"\n{i}. {doc.title}")
            print(f"   Type: {doc.doc_type} | Score: {result.score:.3f}")
            print(f"   {result.excerpt[:120]}...")


def main():
    parser = argparse.ArgumentParser(description="Opportunity Engine - Your job search command center")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Process job command
    process_parser = subparsers.add_parser("process", help="Process a job posting")
    process_parser.add_argument("file", help="Path to job description file")
    process_parser.add_argument("--company", required=True, help="Company name")
    process_parser.add_argument("--title", required=True, help="Job title")
    
    # Dashboard command
    subparsers.add_parser("dashboard", help="Show full dashboard")
    
    # Content command
    content_parser = subparsers.add_parser("content", help="Generate content")
    content_parser.add_argument("--topic", default="healthtech_ai", help="Content topic")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search knowledge base")
    search_parser.add_argument("query", help="Search query")
    
    # Job tracker commands
    job_parser = subparsers.add_parser("jobs", help="Job tracker commands")
    job_parser.add_argument("--list", action="store_true", help="List all jobs")
    job_parser.add_argument("--followups", action="store_true", help="Show follow-ups")
    job_parser.add_argument("--update", nargs=3, metavar=("ID", "STATUS", "NOTES"), help="Update job status")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    engine = OpportunityEngine()
    
    if args.command == "process":
        with open(args.file, 'r') as f:
            job_text = f.read()
        engine.optimize_cv_for_job(job_text, args.company, args.title)
    
    elif args.command == "dashboard":
        engine.dashboard()
    
    elif args.command == "content":
        engine.content_pipeline(args.topic)
    
    elif args.command == "search":
        engine.search_brain(args.query)
    
    elif args.command == "jobs":
        if args.list:
            print_pipeline(engine.job_tracker)
        elif args.followups:
            print_follow_ups(engine.job_tracker)
        elif args.update:
            job_id, status, notes = args.update
            engine.job_tracker.update_status(job_id, status, notes)
            print(f"✅ Updated [{job_id}] to '{status}'")
        else:
            print_stats(engine.job_tracker)


if __name__ == "__main__":
    main()
