#!/usr/bin/env python3
"""
Mission Control - Web Dashboard for Opportunity Engine
Integrates CV Optimizer, Job Tracker, Content Factory, and 2nd Brain
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cv_optimizer import CVGenerator, ProfileDatabase, JDParser
from job_tracker import JobTracker
from content_factory import ContentFactory
from second_brain import SecondBrain
from network_mapper import NetworkMapper
from analytics_dashboard import AnalyticsDashboard
from calendar_integration import CalendarIntegration
from notification_hub import NotificationHub
from expense_tracker import ExpenseTracker
from bookmark_manager import BookmarkManager
from search_aggregator import SearchAggregator
from cv_pdf_generator import CVPDFGenerator
from linkedin_importer import LinkedInJobImporter
from ahmed_profile import AHMED_PROFILE, SECTOR_SUMMARIES
from job_board_scraper import JobBoardScraper
from enhanced_network_mapper import EnhancedNetworkMapper
from enhanced_content_factory import EnhancedContentFactory
from enhanced_analytics import EnhancedAnalyticsDashboard
from ai_cv_rewriter import AICVRewriter
from company_intelligence import CompanyIntelligence
from email_automation import EmailAutomation
from chat_brain import ChatBrain
from data_coordinator import coordinator

app = Flask(__name__)

# Initialize all tools
profile_db = ProfileDatabase()
cv_generator = CVGenerator(profile_db)
job_tracker = JobTracker()
content_factory = ContentFactory()
brain = SecondBrain()
network_mapper = NetworkMapper()
analytics = AnalyticsDashboard()
calendar = CalendarIntegration()
notifications = NotificationHub()
expense_tracker = ExpenseTracker()
bookmark_manager = BookmarkManager()
search_aggregator = SearchAggregator()
pdf_generator = CVPDFGenerator()
linkedin_importer = LinkedInJobImporter()
job_scraper = JobBoardScraper()
enhanced_network = EnhancedNetworkMapper()
enhanced_content = EnhancedContentFactory()
enhanced_analytics = EnhancedAnalyticsDashboard()
ai_rewriter = AICVRewriter()
company_intel = CompanyIntelligence()
email_auto = EmailAutomation()
chat_brain = ChatBrain()

@app.route("/")
def dashboard():
    """Main dashboard"""
    stats = job_tracker.get_stats()
    pipeline = job_tracker.get_pipeline()
    follow_ups = job_tracker.get_follow_ups()
    brain_stats = brain.get_stats()
    
    return render_template("dashboard.html", 
                          stats=stats,
                          pipeline=pipeline,
                          follow_ups=follow_ups,
                          brain_stats=brain_stats)

@app.route("/cv-optimizer", methods=["GET", "POST"])
def cv_optimizer():
    """CV Optimizer page"""
    result = None
    linkedin_data = None
    
    # Check for LinkedIn import
    linkedin_url = request.args.get('linkedin_url', '')
    print(f"DEBUG: linkedin_url from args = {linkedin_url}")  # Debug output
    if linkedin_url and linkedin_importer.is_linkedin_url(linkedin_url):
        linkedin_data = linkedin_importer.scrape_job(linkedin_url)
        print(f"DEBUG: linkedin_data = {linkedin_data}")  # Debug output
    
    if request.method == "POST":
        job_text = request.form.get("job_text", "")
        company = request.form.get("company", "")
        title = request.form.get("title", "")
        
        if job_text and company and title:
            # Generate tailored CV
            tailored_cv = cv_generator.generate(job_text, title, company)
            
            # Export to text
            output = cv_generator.export_to_text(tailored_cv)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cv_{company.replace(' ', '_')}_{timestamp}.txt"
            filepath = Path("/root/.openclaw/workspace/tools/cv-optimizer/output") / filename
            
            with open(filepath, 'w') as f:
                f.write(output)
            
            # Generate PDF with Ahmed's real data
            # Determine sector based on job title keywords
            job_lower = title.lower()
            if any(word in job_lower for word in ['health', 'medical', 'hospital', 'clinical', 'patient']):
                summary = SECTOR_SUMMARIES['healthtech']
            elif any(word in job_lower for word in ['fintech', 'bank', 'payment', 'financial']):
                summary = SECTOR_SUMMARIES['fintech']
            else:
                summary = SECTOR_SUMMARIES['general']
            
            # Build experience section from real data
            jobs = []
            for exp in AHMED_PROFILE['experience'][:3]:  # Top 3 roles
                achievements_text = " ".join(exp['achievements'][:3])  # Top 3 achievements
                jobs.append({
                    'title': exp['title'],
                    'company': exp['company'],
                    'dates': exp['dates'],
                    'description': achievements_text
                })
            
            cv_data = {
                'target_title': title,
                'target_company': company,
                'ats_score': tailored_cv.ats_score,
                'profile': AHMED_PROFILE,
                'sections': [
                    {
                        'type': 'summary',
                        'title': 'Professional Summary',
                        'content': summary
                    },
                    {
                        'type': 'experience',
                        'title': 'Professional Experience',
                        'jobs': jobs
                    },
                    {
                        'type': 'skills',
                        'title': 'Core Competencies',
                        'skills': AHMED_PROFILE['core_competencies']
                    }
                ]
            }
            pdf_filename = pdf_generator.generate_pdf(cv_data)
            
            result = {
                "ats_score": tailored_cv.ats_score,
                "match_analysis": tailored_cv.match_analysis,
                "suggestions": tailored_cv.suggestions,
                "cv_text": output,
                "filename": str(filename),
                "pdf_filename": pdf_filename,
                "company": company,
                "title": title
            }
            
            # Register CV in unified system
            cv_id = coordinator.register_cv({
                'filename': filename,
                'pdf_filename': pdf_filename,
                'company': company,
                'title': title,
                'ats_score': tailored_cv.ats_score,
                'cv_text': output
            })
            result['cv_id'] = cv_id
            
            # Auto-find matching jobs to suggest linking
            matching_jobs = [j for j in coordinator.jobs if 
                           company.lower() in j.get('company', '').lower() or
                           j.get('company', '').lower() in company.lower()]
            if matching_jobs:
                result['suggested_job_link'] = matching_jobs[0]
    
    return render_template("cv_optimizer.html", result=result, linkedin_data=linkedin_data)

@app.route("/job-tracker")
def job_tracker_view():
    """Job Tracker page"""
    pipeline = job_tracker.get_pipeline()
    stats = job_tracker.get_stats()
    follow_ups = job_tracker.get_follow_ups()
    
    return render_template("job_tracker.html",
                          pipeline=pipeline,
                          stats=stats,
                          follow_ups=follow_ups)

@app.route("/job-tracker/add", methods=["POST"])
def add_job():
    """Add a new job - with auto-connections"""
    company = request.form.get("company", "")
    title = request.form.get("title", "")
    location = request.form.get("location", "")
    source = request.form.get("source", "")
    sector = request.form.get("sector", "HealthTech")
    url = request.form.get("url", "")
    priority = int(request.form.get("priority", 3))
    
    if company and title:
        job = job_tracker.add_job(
            company=company,
            title=title,
            location=location,
            source=source,
            sector=sector,
            priority=priority
        )
        job.url = url
        job_tracker.save()
        
        # Register with coordinator for unified tracking
        job_data = {
            'id': job.id,
            'company': company,
            'title': title,
            'location': location,
            'source': source,
            'sector': sector,
            'url': url,
            'date_applied': datetime.now().isoformat(),
            'status': 'applied'
        }
        coordinator.register_job(job_data)
        
        # Auto-find contacts at this company
        contacts = coordinator.find_contacts_at_company(company)
        if contacts:
            job.suggested_contacts = [c.get('id') for c in contacts]
    
    return redirect(url_for("job_tracker_view"))

@app.route("/job-tracker/update/<job_id>", methods=["POST"])
def update_job(job_id):
    """Update job status"""
    status = request.form.get("status", "")
    notes = request.form.get("notes", "")
    
    if status:
        job_tracker.update_status(job_id, status, notes)
    
    return redirect(url_for("job_tracker_view"))

@app.route("/content-factory", methods=["GET", "POST"])
def content_factory_view():
    """Content Factory page"""
    result = None
    
    if request.method == "POST":
        content_type = request.form.get("content_type", "linkedin")
        topic = request.form.get("topic", "healthtech_ai")
        
        if content_type == "linkedin":
            result = content_factory.generate_linkedin_post(topic)
        elif content_type == "newsletter":
            result = content_factory.generate_newsletter("weekly_roundup")
        elif content_type == "calendar":
            calendar = content_factory.generate_content_calendar(30)
            result = {
                "type": "calendar",
                "calendar": calendar[:10],  # First 10 items
                "total": len(calendar)
            }
    
    return render_template("content_factory.html", result=result)

@app.route("/second-brain", methods=["GET", "POST"])
def second_brain_view():
    """2nd Brain search page"""
    results = None
    query = ""
    
    if request.method == "POST":
        query = request.form.get("query", "")
        doc_type = request.form.get("doc_type", "")
        
        if query:
            results = brain.search(query, doc_type=doc_type if doc_type else None, top_k=10)
    
    stats = brain.get_stats()
    
    return render_template("second_brain.html", 
                          results=results,
                          query=query,
                          stats=stats)

@app.route("/network")
def network_view():
    """Network Mapper page"""
    stats = network_mapper.get_stats()
    follow_ups = network_mapper.get_follow_ups()
    suggestions = network_mapper.suggest_outreach()
    contacts = list(network_mapper.contacts.values())
    return render_template("network_mapper.html",
                          stats=stats,
                          follow_ups=follow_ups,
                          suggestions=suggestions,
                          contacts=contacts)

@app.route("/network/add", methods=["POST"])
def add_contact():
    """Add a new contact"""
    name = request.form.get("name", "")
    title = request.form.get("title", "")
    company = request.form.get("company", "")
    contact_type = request.form.get("contact_type", "peer")
    sector = request.form.get("sector", "")
    email = request.form.get("email", "")
    linkedin = request.form.get("linkedin", "")
    
    if name and title and company:
        network_mapper.add_contact(name, title, company, contact_type, sector, email, linkedin)
    
    return redirect(url_for("network_view"))

@app.route("/analytics")
def analytics_view():
    """Analytics Dashboard"""
    jobs_file = Path("/root/.openclaw/workspace/tools/cv-optimizer/data/job_applications.json")
    jobs = []
    if jobs_file.exists():
        with open(jobs_file, 'r') as f:
            jobs = json.load(f)
    
    revenue = analytics.calculate_revenue_metrics(jobs)
    funnel = analytics.calculate_conversion_funnel(jobs)
    activity = analytics.calculate_activity_metrics(jobs)
    
    return render_template("analytics.html",
                          revenue=revenue,
                          funnel=funnel,
                          activity=activity)

@app.route("/calendar")
def calendar_view():
    """Calendar view"""
    upcoming = calendar.get_upcoming_events(14)
    return render_template("calendar.html", events=upcoming)

@app.route("/notifications")
def notifications_view():
    """Notifications page"""
    unread = notifications.get_unread()
    stats = notifications.get_stats()
    return render_template("notifications.html",
                          notifications=unread,
                          stats=stats)

@app.route("/api/stats")
def api_stats():
    """API endpoint for stats"""
    return jsonify({
        "jobs": job_tracker.get_stats(),
        "brain": brain.get_stats(),
        "network": network_mapper.get_stats(),
        "notifications": notifications.get_stats()
    })

# ===== EXPENSE TRACKER ROUTES =====
@app.route("/expenses")
def expenses_view():
    """Expense Tracker page"""
    expenses = expense_tracker.get_expenses()
    summary = expense_tracker.get_summary()
    return render_template("expenses.html", expenses=expenses, summary=summary)

@app.route("/expenses/add", methods=["POST"])
def add_expense():
    """Add a new expense"""
    amount = request.form.get("amount", 0)
    category = request.form.get("category", "Other")
    description = request.form.get("description", "")
    date = request.form.get("date")
    is_job_related = request.form.get("is_job_related") == "true"
    
    if amount and description:
        expense_tracker.add_expense(float(amount), category, description, date, is_job_related)
    
    return redirect(url_for("expenses_view"))

# ===== BOOKMARK MANAGER ROUTES =====
@app.route("/bookmarks")
def bookmarks_view():
    """Bookmark Manager page"""
    bookmarks = bookmark_manager.get_bookmarks()
    stats = bookmark_manager.get_stats()
    return render_template("bookmarks.html", bookmarks=bookmarks, stats=stats)

@app.route("/bookmarks/add", methods=["POST"])
def add_bookmark():
    """Add a new bookmark"""
    title = request.form.get("title", "")
    url = request.form.get("url", "")
    category = request.form.get("category", "other")
    notes = request.form.get("notes", "")
    tags_str = request.form.get("tags", "")
    tags = [t.strip() for t in tags_str.split(",") if t.strip()]
    
    if title and url:
        bookmark_manager.add_bookmark(title, url, category, notes, tags)
    
    return redirect(url_for("bookmarks_view"))

# ===== SEARCH AGGREGATOR ROUTES =====
@app.route("/search", methods=["GET", "POST"])
def search_view():
    """Unified search page"""
    results = None
    query = ""
    
    if request.method == "POST":
        query = request.form.get("query", "")
        if query:
            results = search_aggregator.search_all(query)
    
    stats = search_aggregator.get_stats()
    return render_template("search.html", results=results, query=query, stats=stats)

# ===== LINKEDIN IMPORT ROUTE =====
@app.route("/cv-optimizer/import-linkedin", methods=["POST"])
def import_linkedin():
    """Import job from LinkedIn URL"""
    url = request.form.get("url", "")
    if linkedin_importer.is_linkedin_url(url):
        return redirect(url_for("cv_optimizer", linkedin_url=url))
    return redirect(url_for("cv_optimizer"))

# ===== PDF DOWNLOAD ROUTE =====
@app.route("/cv-optimizer/view-cv/<path:filename>")
def view_cv(filename):
    """View generated CV HTML in browser (user can print to PDF)"""
    output_dir = Path("/root/.openclaw/workspace/tools/cv-optimizer/output")
    file_path = output_dir / filename
    
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    else:
        return "File not found", 404

# ===== UNIFIED DATA ROUTES =====
@app.route("/job/<job_id>/context")
def job_context(job_id):
    """Get full context for a job: CVs, contacts, timeline"""
    context = coordinator.get_job_context(job_id)
    return jsonify(context)

@app.route("/api/unified-search", methods=["POST"])
def unified_search():
    """Search across all data: jobs, contacts, documents, CVs"""
    query = request.json.get('query', '') if request.json else request.form.get('query', '')
    results = coordinator.unified_search(query)
    return jsonify(results)

@app.route("/api/dashboard-summary")
def dashboard_summary():
    """Get unified dashboard summary"""
    summary = coordinator.get_dashboard_summary()
    return jsonify(summary)

@app.route("/api/link-cv-to-job", methods=["POST"])
def link_cv_to_job():
    """Link a CV to a job application"""
    cv_id = request.form.get('cv_id', '')
    job_id = request.form.get('job_id', '')
    
    if cv_id and job_id:
        coordinator.link_cv_to_job(cv_id, job_id)
        return jsonify({'status': 'success', 'message': 'CV linked to job'})
    
    return jsonify({'status': 'error', 'message': 'Missing cv_id or job_id'}), 400

@app.route("/api/connections")
def get_connections():
    """Get all auto-detected connections between tools"""
    connections = {
        'cv_to_jobs': [],
        'jobs_to_contacts': [],
        'unlinked_cvs': [],
        'jobs_without_cv': [],
        'recent_activities': coordinator.activities[-10:]
    }
    
    # Find CVs that could link to jobs
    for cv in coordinator.cvs:
        if not cv.get('linked_to_job'):
            matching_jobs = [j for j in coordinator.jobs 
                           if cv.get('company', '').lower() in j.get('company', '').lower()
                           or j.get('company', '').lower() in cv.get('company', '').lower()]
            if matching_jobs:
                connections['cv_to_jobs'].append({
                    'cv': cv,
                    'suggested_jobs': matching_jobs
                })
            else:
                connections['unlinked_cvs'].append(cv)
    
    # Find jobs without CVs
    for job in coordinator.jobs:
        if not any(cv.get('linked_to_job') == job.get('id') for cv in coordinator.cvs):
            connections['jobs_without_cv'].append(job)
    
    # Find jobs with contacts at company
    for job in coordinator.jobs:
        contacts = coordinator.find_contacts_at_company(job.get('company', ''))
        if contacts:
            connections['jobs_to_contacts'].append({
                'job': job,
                'contacts': contacts
            })
    
    return jsonify(connections)

@app.route("/documents")
def documents_view():
    """View all documents (including auto-indexed CVs)"""
    docs = coordinator.documents
    cvs = coordinator.cvs
    return render_template("documents.html", documents=docs, cvs=cvs)

if __name__ == "__main__":
    print("🚀 Starting Mission Control...")
    print("📍 Access at: http://localhost:5000")
    print("🔗 Or via Tailscale: https://srv1352768.tail945bbc.ts.net:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
