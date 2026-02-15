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
from network_mapper import NetworkMapper
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
from product_manager import product_manager

# Phase 4-9 imports
from phase4_cv_enhancements import (CVVersionHistory, ReadingTimeEstimator, CVHealthTimeline,
    MissingSkillsDetector, SectionReorderer, TemplatePreview, BulkExport,
    PDFAccessibilityChecker, LinkedInHeadlineOptimizer, ReferenceManager, PortfolioLinkGenerator)
from phase5_job_tracker import (ApplicationTimeline, CompanyResearchPanel, InterviewPrepGenerator,
    FollowUpScheduler, ApplicationTemplates, ReferralTracker, RejectionAnalysis,
    GanttTimelineView, SourceEffectiveness, ResponseTimeTracker, GhostJobDetector,
    OfferComparisonTool, CompetitorJobAlerts, ApplicationVelocity, JobDescriptionDiff)
from phase6_network import (LinkedInIntegration, IntroductionRequestGenerator, NetworkHealthScore,
    OutreachSequences, ContactImportCSV, RelationshipTimeline, MeetingNotes, FollowUpStreak,
    ContactGroups, GiftIdeasLog, ConversationHistory, BirthdayAnniversaryAlerts, VoiceMemoLogging,
    ColdEmailTemplates)
from phase7_content import (CarouselBuilder, PDFPostCreator, ContentGapFiller, BestTimeToPost,
    EngagementPrediction, ContentCalendar, HashtagRecommendations, ContentRecycling, HookGenerator,
    StoryTemplates, CommentReplyBank, CompetitorSwipeFile, ABTestHeadlines)
from phase8_analytics import (CohortAnalysis, BenchmarkComparisons, PredictivePipeline,
    SalaryTrends, TimeToOfferAnalytics, WeeklyReportEmail, GoalSettingDashboard, BurnoutDetector,
    ApplicationQualityScore, BestTimeToApply, SectorBreakdown, GeographicHeatmap,
    ResponseLeaderboard, RejectionPatternAnalysis, PeerBenchmarking)
from phase9_system import (ThemeManager, KeyboardShortcuts, BulkActions, AdvancedSearch,
    DataExport, ImportFromTools, MobileResponsive, OfflineMode)

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

# Phase 4-9 Instances
cv_version_history = CVVersionHistory()
reading_time_estimator = ReadingTimeEstimator()
cv_health_timeline = CVHealthTimeline()
missing_skills_detector = MissingSkillsDetector()
section_reorderer = SectionReorderer()
template_preview = TemplatePreview()
bulk_export = BulkExport()
pdf_accessibility = PDFAccessibilityChecker()
linkedin_headline = LinkedInHeadlineOptimizer()
reference_manager = ReferenceManager()
portfolio_links = PortfolioLinkGenerator()
app_timeline = ApplicationTimeline()
company_research = CompanyResearchPanel()
interview_prep = InterviewPrepGenerator()
followup_scheduler = FollowUpScheduler()
app_templates = ApplicationTemplates()
referral_tracker = ReferralTracker()
rejection_analysis = RejectionAnalysis()
gantt_view = GanttTimelineView()
source_effectiveness = SourceEffectiveness()
response_time_tracker = ResponseTimeTracker()
ghost_detector = GhostJobDetector()
offer_comparison = OfferComparisonTool()
competitor_alerts = CompetitorJobAlerts()
app_velocity = ApplicationVelocity()
jd_diff = JobDescriptionDiff()
linkedin_integration = LinkedInIntegration()
intro_request_gen = IntroductionRequestGenerator()
network_health = NetworkHealthScore()
outreach_sequences = OutreachSequences()
contact_import_csv = ContactImportCSV()
relationship_timeline = RelationshipTimeline()
meeting_notes = MeetingNotes()
followup_streak = FollowUpStreak()
contact_groups = ContactGroups()
gift_ideas = GiftIdeasLog()
conversation_history = ConversationHistory()
birthday_alerts = BirthdayAnniversaryAlerts()
voice_memos = VoiceMemoLogging()
cold_email_templates = ColdEmailTemplates()
carousel_builder = CarouselBuilder()
pdf_post_creator = PDFPostCreator()
content_gap_filler = ContentGapFiller()
best_time_post = BestTimeToPost()
engagement_prediction = EngagementPrediction()
content_calendar = ContentCalendar()
hashtag_recs = HashtagRecommendations()
content_recycling = ContentRecycling()
hook_generator = HookGenerator()
story_templates = StoryTemplates()
comment_replies = CommentReplyBank()
competitor_swipe = CompetitorSwipeFile()
ab_test_headlines = ABTestHeadlines()
cohort_analysis = CohortAnalysis()
benchmark_compare = BenchmarkComparisons()
predictive_pipeline = PredictivePipeline()
salary_trends = SalaryTrends()
time_to_offer = TimeToOfferAnalytics()
weekly_report = WeeklyReportEmail()
goal_dashboard = GoalSettingDashboard()
burnout_detector = BurnoutDetector()
app_quality_score = ApplicationQualityScore()
best_time_apply = BestTimeToApply()
sector_breakdown = SectorBreakdown()
geo_heatmap = GeographicHeatmap()
response_leaderboard = ResponseLeaderboard()
rejection_patterns = RejectionPatternAnalysis()
peer_benchmark = PeerBenchmarking()
theme_manager = ThemeManager()
keyboard_shortcuts = KeyboardShortcuts()
bulk_actions_mgr = BulkActions()
advanced_search = AdvancedSearch()
data_export = DataExport()
import_tools = ImportFromTools()
mobile_responsive = MobileResponsive()
offline_mode = OfflineMode()

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

# ===== PRODUCT MANAGEMENT ROUTES =====
@app.route("/product-management")
def product_management_view():
    """Product Management - Feature catalog and roadmap"""
    features = product_manager.get_all_features()
    roadmap = product_manager.get_roadmap()
    stats = product_manager.get_stats()
    return render_template("product_management.html", 
                          features=features, 
                          roadmap=roadmap,
                          stats=stats)

@app.route("/api/product/generate/<tool_id>", methods=["POST"])
def generate_features(tool_id):
    """Generate more missing features for a tool"""
    new_features = product_manager.generate_more_features(tool_id)
    return jsonify({'count': len(new_features), 'features': new_features})

@app.route("/api/product/roadmap", methods=["POST"])
def add_to_roadmap():
    """Add selected features to build roadmap"""
    data = request.json if request.json else request.form
    feature_ids = data.get('features', [])
    added = product_manager.add_to_roadmap(feature_ids)
    return jsonify({'added': added, 'count': len(added)})

@app.route("/api/product/built/<feature_id>", methods=["POST"])
def mark_feature_built(feature_id):
    """Mark a feature as built"""
    product_manager.mark_built(feature_id)
    return jsonify({'status': 'success', 'message': 'Feature marked as built'})

@app.route("/documents")
def documents_view():
    """View all documents (including auto-indexed CVs)"""
    docs = coordinator.documents
    cvs = coordinator.cvs
    return render_template("documents.html", documents=docs, cvs=cvs)

# ===== NEW FEATURES API ROUTES =====

# Interview Checklist Routes
@app.route("/api/job/<job_id>/checklist", methods=["POST"])
def create_interview_checklist(job_id):
    """Create an interview checklist for a job"""
    checklist = job_tracker.add_interview_checklist(job_id)
    if checklist:
        return jsonify({'status': 'success', 'checklist': asdict(checklist)})
    return jsonify({'status': 'error', 'message': 'Job not found'}), 404

@app.route("/api/job/<job_id>/checklist/<checklist_id>", methods=["GET"])
def get_interview_checklist(job_id, checklist_id):
    """Get an interview checklist"""
    checklist = job_tracker.get_checklist(checklist_id)
    if checklist:
        return jsonify({'status': 'success', 'checklist': asdict(checklist)})
    return jsonify({'status': 'error', 'message': 'Checklist not found'}), 404

@app.route("/api/checklist/<checklist_id>/item", methods=["POST"])
def update_checklist_item(checklist_id):
    """Update a checklist item"""
    data = request.json
    job_tracker.update_checklist_item(
        checklist_id, 
        data.get('item_type'), 
        data.get('item_index'), 
        data.get('completed')
    )
    return jsonify({'status': 'success'})

# Salary Negotiation Routes
@app.route("/api/job/<job_id>/negotiation", methods=["POST"])
def create_salary_negotiation(job_id):
    """Create salary negotiation tracking for a job"""
    data = request.json
    negotiation = job_tracker.add_salary_negotiation(
        job_id,
        initial_offer=data.get('initial_offer', 0),
        base_salary=data.get('base_salary', 0),
        bonus=data.get('bonus', 0),
        equity=data.get('equity', ''),
        benefits=data.get('benefits', '')
    )
    if negotiation:
        return jsonify({'status': 'success', 'negotiation': asdict(negotiation)})
    return jsonify({'status': 'error', 'message': 'Job not found'}), 404

@app.route("/api/negotiation/<negotiation_id>", methods=["GET"])
def get_salary_negotiation(negotiation_id):
    """Get salary negotiation"""
    negotiation = job_tracker.get_negotiation(negotiation_id)
    if negotiation:
        return jsonify({'status': 'success', 'negotiation': asdict(negotiation)})
    return jsonify({'status': 'error', 'message': 'Negotiation not found'}), 404

@app.route("/api/negotiation/<negotiation_id>/counter", methods=["POST"])
def add_counter_offer(negotiation_id):
    """Add a counter offer"""
    data = request.json
    job_tracker.add_counter_offer(
        negotiation_id,
        data.get('amount', 0),
        data.get('notes', '')
    )
    return jsonify({'status': 'success'})

@app.route("/api/negotiation/<negotiation_id>/finalize", methods=["POST"])
def finalize_negotiation(negotiation_id):
    """Finalize the negotiation"""
    data = request.json
    job_tracker.finalize_offer(
        negotiation_id,
        data.get('final_amount', 0),
        data.get('accepted', True)
    )
    return jsonify({'status': 'success'})

# Hook Generator Routes
@app.route("/api/content/hooks", methods=["GET"])
def generate_hooks():
    """Generate hooks for LinkedIn posts"""
    count = request.args.get('count', 5, type=int)
    hook_type = request.args.get('type', None)
    industry = request.args.get('industry', 'HealthTech')
    role = request.args.get('role', 'leader')
    
    hooks = content_factory.generate_hooks(count, hook_type, industry, role)
    return jsonify({'status': 'success', 'hooks': hooks})

# Meeting Notes Routes
@app.route("/api/contact/<contact_id>/note", methods=["POST"])
def add_meeting_note(contact_id):
    """Add meeting notes for a contact"""
    data = request.json
    note = network_mapper.add_meeting_note(
        contact_id,
        title=data.get('title', ''),
        content=data.get('content', ''),
        key_points=data.get('key_points', []),
        action_items=data.get('action_items', []),
        sentiment=data.get('sentiment', 'positive')
    )
    if note:
        return jsonify({'status': 'success', 'note': asdict(note)})
    return jsonify({'status': 'error', 'message': 'Contact not found'}), 404

@app.route("/api/contact/<contact_id>/notes", methods=["GET"])
def get_meeting_notes(contact_id):
    """Get all meeting notes for a contact"""
    notes = network_mapper.get_meeting_notes(contact_id)
    return jsonify({'status': 'success', 'notes': [asdict(n) for n in notes]})

# Contact Groups Routes
@app.route("/api/groups", methods=["GET"])
def get_contact_groups():
    """Get all contact groups"""
    groups = network_mapper.get_contact_groups()
    return jsonify({'status': 'success', 'groups': [asdict(g) for g in groups]})

@app.route("/api/groups", methods=["POST"])
def create_contact_group():
    """Create a new contact group"""
    data = request.json
    group = network_mapper.add_contact_group(
        name=data.get('name', ''),
        description=data.get('description', ''),
        color=data.get('color', '#3B82F6')
    )
    return jsonify({'status': 'success', 'group': asdict(group)})

@app.route("/api/groups/<group_id>/contact/<contact_id>", methods=["POST"])
def add_contact_to_group(group_id, contact_id):
    """Add a contact to a group"""
    network_mapper.add_contact_to_group(contact_id, group_id)
    return jsonify({'status': 'success'})

@app.route("/api/groups/<group_id>/contacts", methods=["GET"])
def get_group_contacts(group_id):
    """Get all contacts in a group"""
    contacts = network_mapper.get_contacts_by_group(group_id)
    return jsonify({'status': 'success', 'contacts': [asdict(c) for c in contacts]})

# Cold Email Templates Routes
@app.route("/api/templates/cold-email", methods=["GET"])
def get_cold_email_templates():
    """Get cold email templates"""
    category = request.args.get('category', None)
    templates = network_mapper.get_cold_email_templates(category)
    return jsonify({'status': 'success', 'templates': templates})

@app.route("/api/templates/cold-email/generate", methods=["POST"])
def generate_cold_email():
    """Generate a cold email from template"""
    data = request.json
    email = network_mapper.generate_cold_email(
        template_name=data.get('template_name', ''),
        variables=data.get('variables', {})
    )
    return jsonify({'status': 'success', 'email': email})

# Weekly Report Email Route
@app.route("/api/analytics/weekly-report", methods=["GET"])
def get_weekly_report():
    """Get weekly report email"""
    report = analytics.generate_weekly_report_email()
    return jsonify({'status': 'success', 'report': report})

# ===== ADDITIONAL FEATURES ROUTES =====
from src.additional_features import CVFeatures, ContentFeatures, NetworkFeatures, JobScraperFeatures

cv_features = CVFeatures()
content_features = ContentFeatures()
network_features = NetworkFeatures()
job_scraper = JobScraperFeatures()

# CV Features
@app.route("/api/cv/templates", methods=["GET"])
def get_cv_templates():
    """Get CV templates"""
    templates = cv_features.get_templates()
    return jsonify({'status': 'success', 'templates': templates})

@app.route("/api/cv/compare", methods=["POST"])
def compare_cvs():
    """Compare two CVs"""
    data = request.json
    result = cv_features.compare_cvs(
        data.get('cv1', {}),
        data.get('cv2', {}),
        data.get('job_requirements', {})
    )
    return jsonify({'status': 'success', 'comparison': result})

@app.route("/api/cv/keyword-heatmap", methods=["POST"])
def keyword_heatmap():
    """Get keyword heatmap"""
    data = request.json
    result = cv_features.keyword_heatmap(
        data.get('cv_text', ''),
        data.get('job_text', '')
    )
    return jsonify({'status': 'success', 'heatmap': result})

@app.route("/api/cv/bullet-strength", methods=["POST"])
def bullet_strength():
    """Analyze bullet strength"""
    data = request.json
    result = cv_features.analyze_bullet_strength(data.get('bullets', []))
    return jsonify({'status': 'success', 'analysis': result})

@app.route("/api/cv/export-docx", methods=["POST"])
def export_cv_docx():
    """Export CV to DOCX (mock)"""
    return jsonify({
        'status': 'success',
        'message': 'DOCX export mock - would generate Word document',
        'format': 'docx'
    })

# Content Features
@app.route("/api/content/viral-predict", methods=["POST"])
def predict_viral():
    """Predict viral score for content"""
    data = request.json
    result = content_features.predict_viral_score(
        data.get('content', ''),
        data.get('topic', '')
    )
    return jsonify({'status': 'success', 'prediction': result})

@app.route("/api/content/quote-image", methods=["POST"])
def generate_quote_image():
    """Generate quote image specs"""
    data = request.json
    result = content_features.generate_quote_image(
        data.get('quote', ''),
        data.get('author', ''),
        data.get('template', 'modern')
    )
    return jsonify({'status': 'success', 'image_specs': result})

# Network Features
@app.route("/api/network/heatmap", methods=["POST"])
def contact_heatmap():
    """Generate contact heatmap"""
    data = request.json
    contacts = data.get('contacts', [])
    result = network_features.generate_contact_heatmap(contacts)
    return jsonify({'status': 'success', 'heatmap': result})

# Job Scraper Features
@app.route("/api/jobs/search", methods=["GET"])
def search_jobs():
    """Search jobs (mock)"""
    keywords = request.args.get('keywords', '')
    location = request.args.get('location', '')
    results = job_scraper.search_jobs(keywords, location)
    return jsonify({'status': 'success', 'jobs': results})

@app.route("/api/linkedin/import", methods=["POST"])
def linkedin_import():
    """Simulate LinkedIn import"""
    data = request.json
    profile_url = data.get('profile_url', '')
    result = job_scraper.import_from_linkedin(profile_url)
    return jsonify(result)

# ============================================================
# PHASE 4: CV Core Enhancement Routes
# ============================================================

@app.route("/api/cv/versions", methods=["GET"])
def get_cv_versions():
    return jsonify({"status": "success", "versions": cv_version_history.get_versions()})

@app.route("/api/cv/versions/save", methods=["POST"])
def save_cv_version():
    data = request.json or {}
    result = cv_version_history.save_version(data.get("cv_data", {}), data.get("label", ""), data.get("job_title", ""))
    return jsonify({"status": "success", "version": result})

@app.route("/api/cv/versions/<version_id>", methods=["GET"])
def get_cv_version(version_id):
    ver = cv_version_history.get_version(version_id)
    return jsonify({"status": "success", "version": ver}) if ver else jsonify({"status": "error", "message": "Not found"}), 404

@app.route("/api/cv/versions/<version_id>/revert", methods=["POST"])
def revert_cv_version(version_id):
    result = cv_version_history.revert_to(version_id)
    return jsonify({"status": "success", "version": result}) if result else jsonify({"status": "error"}), 404

@app.route("/api/cv/reading-time", methods=["POST"])
def cv_reading_time():
    data = request.json or {}
    result = reading_time_estimator.estimate(data.get("cv_text", ""))
    return jsonify({"status": "success", "reading_time": result})

@app.route("/api/cv/health-timeline", methods=["GET"])
def cv_health_timeline_route():
    return jsonify({"status": "success", "timeline": cv_health_timeline.get_timeline()})

@app.route("/api/cv/health-timeline/add", methods=["POST"])
def add_health_entry():
    data = request.json or {}
    result = cv_health_timeline.add_entry(data.get("ats_score", 0), data.get("job_title", ""), data.get("changes", ""))
    return jsonify({"status": "success", "entry": result})

@app.route("/api/cv/missing-skills", methods=["POST"])
def detect_missing_skills():
    data = request.json or {}
    result = missing_skills_detector.detect(data.get("cv_text", ""), data.get("job_description", ""))
    return jsonify({"status": "success", "analysis": result})

@app.route("/api/cv/sections", methods=["GET"])
def get_cv_sections():
    return jsonify({"status": "success", "sections": section_reorderer.get_sections()})

@app.route("/api/cv/sections/reorder", methods=["POST"])
def reorder_cv_sections():
    data = request.json or {}
    result = section_reorderer.reorder(data.get("order", []))
    return jsonify({"status": "success", "sections": result})

@app.route("/api/cv/template-preview", methods=["GET"])
def get_template_previews():
    return jsonify({"status": "success", "templates": template_preview.get_all_templates()})

@app.route("/api/cv/template-preview/<template_id>", methods=["POST"])
def preview_template(template_id):
    data = request.json or {}
    result = template_preview.preview(template_id, data.get("cv_data", {}))
    return jsonify({"status": "success", "preview": result})

@app.route("/api/cv/bulk-export", methods=["GET"])
def bulk_export_cvs():
    versions = cv_version_history.get_versions()
    result = bulk_export.export_summary(versions)
    return jsonify({"status": "success", "export": result})

@app.route("/api/cv/accessibility", methods=["POST"])
def check_accessibility():
    data = request.json or {}
    result = pdf_accessibility.check(data.get("cv_data", {}))
    return jsonify({"status": "success", "accessibility": result})

@app.route("/api/cv/linkedin-headline", methods=["POST"])
def optimize_headline():
    data = request.json or {}
    result = linkedin_headline.optimize(data.get("headline", ""), data.get("target_role", ""), data.get("skills", []))
    return jsonify({"status": "success", "optimization": result})

@app.route("/api/cv/references", methods=["GET"])
def get_references():
    return jsonify({"status": "success", "references": reference_manager.get_all()})

@app.route("/api/cv/references", methods=["POST"])
def add_reference():
    result = reference_manager.add(request.json or {})
    return jsonify({"status": "success", "reference": result})

@app.route("/api/cv/portfolio", methods=["GET"])
def get_portfolio_links():
    return jsonify({"status": "success", "portfolio": portfolio_links.generate()})

# ============================================================
# PHASE 5: Job Tracker Enhancement Routes
# ============================================================

@app.route("/api/jobs/timeline/<app_id>", methods=["GET"])
def get_app_timeline(app_id):
    result = app_timeline.get_timeline({"id": app_id, "company": "Company", "role": "Role"})
    return jsonify({"status": "success", "timeline": result})

@app.route("/api/jobs/company-research/<company>", methods=["GET"])
def research_company(company):
    result = company_research.research(company)
    return jsonify({"status": "success", "research": result})

@app.route("/api/jobs/interview-prep", methods=["POST"])
def generate_interview_prep():
    data = request.json or {}
    result = interview_prep.generate(data.get("role", ""), data.get("company", ""), data.get("job_description", ""))
    return jsonify({"status": "success", "prep": result})

@app.route("/api/jobs/followups", methods=["GET"])
def get_followups():
    return jsonify({"status": "success", "pending": followup_scheduler.get_pending(), "upcoming": followup_scheduler.get_upcoming(), "all": followup_scheduler.get_all()})

@app.route("/api/jobs/followups/schedule", methods=["POST"])
def schedule_followup():
    data = request.json or {}
    result = followup_scheduler.schedule(data.get("company", ""), data.get("role", ""), data.get("contact", ""), data.get("days", 7))
    return jsonify({"status": "success", "followup": result})

@app.route("/api/jobs/followups/<fid>/complete", methods=["POST"])
def complete_followup(fid):
    followup_scheduler.complete(fid)
    return jsonify({"status": "success"})

@app.route("/api/jobs/app-templates", methods=["GET"])
def get_app_templates():
    return jsonify({"status": "success", "templates": app_templates.get_all()})

@app.route("/api/jobs/app-templates", methods=["POST"])
def add_app_template():
    result = app_templates.add(request.json or {})
    return jsonify({"status": "success", "template": result})

@app.route("/api/jobs/app-templates/<tid>/use", methods=["POST"])
def use_app_template(tid):
    data = request.json or {}
    result = app_templates.use_template(tid, data.get("variables", {}))
    return jsonify({"status": "success", "result": result})

@app.route("/api/jobs/referrals", methods=["GET"])
def get_referrals():
    return jsonify({"status": "success", "referrals": referral_tracker.get_all(), "stats": referral_tracker.get_stats()})

@app.route("/api/jobs/referrals", methods=["POST"])
def add_referral():
    result = referral_tracker.add(request.json or {})
    return jsonify({"status": "success", "referral": result})

@app.route("/api/jobs/rejections", methods=["GET"])
def get_rejections():
    return jsonify({"status": "success", "rejections": rejection_analysis.get_all(), "analysis": rejection_analysis.analyze()})

@app.route("/api/jobs/rejections", methods=["POST"])
def add_rejection():
    result = rejection_analysis.add(request.json or {})
    return jsonify({"status": "success", "rejection": result})

@app.route("/api/jobs/gantt", methods=["GET"])
def get_gantt_view():
    apps = job_tracker.get_pipeline() if hasattr(job_tracker, 'get_pipeline') else []
    result = gantt_view.generate(apps if isinstance(apps, list) else [])
    return jsonify({"status": "success", "gantt": result})

@app.route("/api/jobs/source-effectiveness", methods=["GET"])
def get_source_effectiveness():
    apps = job_tracker.get_pipeline() if hasattr(job_tracker, 'get_pipeline') else []
    result = source_effectiveness.analyze(apps if isinstance(apps, list) else [])
    return jsonify({"status": "success", "effectiveness": result})

@app.route("/api/jobs/response-times", methods=["GET"])
def get_response_times():
    result = response_time_tracker.analyze([])
    return jsonify({"status": "success", "response_times": result})

@app.route("/api/jobs/ghost-detect", methods=["POST"])
def detect_ghost_job():
    result = ghost_detector.detect(request.json or {})
    return jsonify({"status": "success", "detection": result})

@app.route("/api/jobs/offer-compare", methods=["POST"])
def compare_offers():
    data = request.json or {}
    result = offer_comparison.compare(data.get("offers", []))
    return jsonify({"status": "success", "comparison": result})

@app.route("/api/jobs/competitor-alerts", methods=["GET"])
def get_competitor_alerts():
    result = competitor_alerts.get_alerts()
    return jsonify({"status": "success", "alerts": result})

@app.route("/api/jobs/velocity", methods=["GET"])
def get_app_velocity():
    result = app_velocity.calculate([])
    return jsonify({"status": "success", "velocity": result})

@app.route("/api/jobs/jd-diff", methods=["POST"])
def diff_jds():
    data = request.json or {}
    result = jd_diff.diff(data.get("jd1", ""), data.get("jd2", ""))
    return jsonify({"status": "success", "diff": result})

# ============================================================
# PHASE 6: Network Enhancement Routes
# ============================================================

@app.route("/api/network/linkedin-connect", methods=["POST"])
def linkedin_connect():
    data = request.json or {}
    result = linkedin_integration.connect(data.get("profile_url", ""))
    return jsonify({"status": "success", "connection": result})

@app.route("/api/network/linkedin-stats", methods=["GET"])
def linkedin_stats():
    return jsonify({"status": "success", "stats": linkedin_integration.get_profile_stats()})

@app.route("/api/network/linkedin-connections", methods=["GET"])
def linkedin_connections():
    return jsonify({"status": "success", "data": linkedin_integration.import_connections()})

@app.route("/api/network/intro-request", methods=["POST"])
def generate_intro_request():
    data = request.json or {}
    result = intro_request_gen.generate(data.get("target_name", ""), data.get("target_company", ""),
        data.get("mutual_contact", ""), data.get("field", "healthcare AI"))
    return jsonify({"status": "success", "intro_request": result})

@app.route("/api/network/health-score", methods=["GET"])
def get_network_health():
    return jsonify({"status": "success", "health": network_health.calculate()})

@app.route("/api/network/outreach-sequences", methods=["GET"])
def get_outreach_sequences():
    return jsonify({"status": "success", "sequences": outreach_sequences.get_all()})

@app.route("/api/network/outreach-sequences", methods=["POST"])
def create_outreach_sequence():
    data = request.json or {}
    result = outreach_sequences.create_sequence(data.get("name", ""), data.get("target", ""))
    return jsonify({"status": "success", "sequence": result})

@app.route("/api/network/import-csv", methods=["POST"])
def import_contacts_csv():
    data = request.json or {}
    result = contact_import_csv.parse_csv(data.get("csv_content", ""))
    return jsonify({"status": "success", "import": result})

@app.route("/api/network/import-csv/template", methods=["GET"])
def get_csv_template():
    return jsonify({"status": "success", "template": contact_import_csv.get_template()})

@app.route("/api/network/relationship-timeline/<contact>", methods=["GET"])
def get_relationship_timeline(contact):
    result = relationship_timeline.get_timeline(contact)
    return jsonify({"status": "success", "timeline": result})

@app.route("/api/network/meeting-notes/all", methods=["GET"])
def get_all_meeting_notes():
    return jsonify({"status": "success", "notes": meeting_notes.get_all()})

@app.route("/api/network/meeting-notes/add", methods=["POST"])
def create_meeting_note():
    result = meeting_notes.add(request.json or {})
    return jsonify({"status": "success", "note": result})

@app.route("/api/network/followup-streaks", methods=["GET"])
def get_followup_streaks():
    return jsonify({"status": "success", "streaks": followup_streak.calculate()})

@app.route("/api/network/groups/all", methods=["GET"])
def get_network_groups():
    return jsonify({"status": "success", "groups": contact_groups.get_all()})

@app.route("/api/network/groups/add", methods=["POST"])
def add_network_group():
    data = request.json or {}
    result = contact_groups.create(data.get("name", ""), data.get("color", "#4299e1"))
    return jsonify({"status": "success", "group": result})

@app.route("/api/network/gifts", methods=["GET"])
def get_gift_ideas():
    return jsonify({"status": "success", "gifts": gift_ideas.get_all(), "upcoming": gift_ideas.get_upcoming()})

@app.route("/api/network/gifts", methods=["POST"])
def add_gift_idea():
    result = gift_ideas.add(request.json or {})
    return jsonify({"status": "success", "gift": result})

@app.route("/api/network/conversations", methods=["GET"])
def get_conversations():
    return jsonify({"status": "success", "conversations": conversation_history.get_all()})

@app.route("/api/network/conversations", methods=["POST"])
def add_conversation():
    data = request.json or {}
    result = conversation_history.add(data.get("contact", ""), data.get("channel", ""), data.get("summary", ""))
    return jsonify({"status": "success", "conversation": result})

@app.route("/api/network/birthdays", methods=["GET"])
def get_birthday_alerts():
    return jsonify({"status": "success", "upcoming": birthday_alerts.get_upcoming(), "all": birthday_alerts.get_all()})

@app.route("/api/network/birthdays", methods=["POST"])
def add_birthday_alert():
    data = request.json or {}
    result = birthday_alerts.add(data.get("contact", ""), data.get("type", "birthday"), data.get("date", ""), data.get("notes", ""))
    return jsonify({"status": "success", "alert": result})

@app.route("/api/network/voice-memos", methods=["GET"])
def get_voice_memos():
    return jsonify({"status": "success", "memos": voice_memos.get_all()})

@app.route("/api/network/voice-memos", methods=["POST"])
def add_voice_memo():
    data = request.json or {}
    result = voice_memos.add(data.get("contact", ""), data.get("transcript", ""), data.get("duration", 60))
    return jsonify({"status": "success", "memo": result})

@app.route("/api/network/cold-email-templates/all", methods=["GET"])
def get_network_email_templates():
    return jsonify({"status": "success", "templates": cold_email_templates.get_templates()})

# ============================================================
# PHASE 7: Content Enhancement Routes
# ============================================================

@app.route("/api/content/carousel", methods=["POST"])
def create_carousel():
    data = request.json or {}
    result = carousel_builder.create(data.get("title", ""), data.get("slides"), data.get("theme", "professional"))
    return jsonify({"status": "success", "carousel": result})

@app.route("/api/content/carousel/templates", methods=["GET"])
def get_carousel_templates():
    return jsonify({"status": "success", "templates": carousel_builder.get_templates()})

@app.route("/api/content/pdf-post", methods=["POST"])
def create_pdf_post():
    data = request.json or {}
    result = pdf_post_creator.create(data.get("content", ""), data.get("title", ""), data.get("author", "Ahmed Nasr"))
    return jsonify({"status": "success", "pdf": result})

@app.route("/api/content/gap-analysis", methods=["GET"])
def content_gap_analysis():
    return jsonify({"status": "success", "analysis": content_gap_filler.analyze()})

@app.route("/api/content/best-time", methods=["GET"])
def get_best_time_to_post():
    audience = request.args.get("audience", "professional")
    return jsonify({"status": "success", "recommendation": best_time_post.recommend(audience=audience)})

@app.route("/api/content/engagement-predict", methods=["POST"])
def predict_engagement():
    data = request.json or {}
    result = engagement_prediction.predict(data.get("content", ""), data.get("type", "text"), data.get("hashtags", 3))
    return jsonify({"status": "success", "prediction": result})

@app.route("/api/content/calendar", methods=["GET"])
def get_content_calendar():
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    return jsonify({"status": "success", "calendar": content_calendar.get_calendar(month, year)})

@app.route("/api/content/calendar", methods=["POST"])
def add_calendar_entry():
    result = content_calendar.add_entry(request.json or {})
    return jsonify({"status": "success", "entry": result})

@app.route("/api/content/hashtags", methods=["POST"])
def get_hashtag_recommendations():
    data = request.json or {}
    result = hashtag_recs.recommend(data.get("content", ""), data.get("max", 5))
    return jsonify({"status": "success", "hashtags": result})

@app.route("/api/content/recycle", methods=["GET"])
def get_content_recycling():
    return jsonify({"status": "success", "suggestions": content_recycling.suggest()})

@app.route("/api/content/hooks/generate", methods=["POST"])
def create_hooks():
    data = request.json or {}
    result = hook_generator.generate(data.get("topic", ""), data.get("count", 5))
    return jsonify({"status": "success", "hooks": result})

@app.route("/api/content/story-templates", methods=["GET"])
def get_story_templates():
    return jsonify({"status": "success", "templates": story_templates.get_templates()})

@app.route("/api/content/reply-bank", methods=["GET"])
def get_reply_bank():
    return jsonify({"status": "success", "replies": comment_replies.get_replies()})

@app.route("/api/content/swipe-file", methods=["GET"])
def get_swipe_file():
    return jsonify({"status": "success", "entries": competitor_swipe.get_all()})

@app.route("/api/content/swipe-file", methods=["POST"])
def add_swipe_entry():
    result = competitor_swipe.add(request.json or {})
    return jsonify({"status": "success", "entry": result})

@app.route("/api/content/ab-tests", methods=["GET"])
def get_ab_tests():
    return jsonify({"status": "success", "tests": ab_test_headlines.get_all()})

@app.route("/api/content/ab-tests", methods=["POST"])
def create_ab_test():
    data = request.json or {}
    result = ab_test_headlines.create_test(data.get("headline_a", ""), data.get("headline_b", ""), data.get("topic", ""))
    return jsonify({"status": "success", "test": result})

# ============================================================
# PHASE 8: Analytics Enhancement Routes
# ============================================================

@app.route("/api/analytics/cohort", methods=["GET"])
def get_cohort_analysis():
    return jsonify({"status": "success", "cohort": cohort_analysis.analyze()})

@app.route("/api/analytics/benchmarks", methods=["GET"])
def get_benchmarks():
    return jsonify({"status": "success", "benchmarks": benchmark_compare.compare()})

@app.route("/api/analytics/pipeline-forecast", methods=["GET"])
def get_pipeline_forecast():
    return jsonify({"status": "success", "forecast": predictive_pipeline.forecast()})

@app.route("/api/analytics/salary-trends", methods=["GET"])
def get_salary_trends():
    return jsonify({"status": "success", "trends": salary_trends.analyze()})

@app.route("/api/analytics/time-to-offer", methods=["GET"])
def get_time_to_offer():
    return jsonify({"status": "success", "analytics": time_to_offer.analyze()})

@app.route("/api/analytics/weekly-report/current", methods=["GET"])
def get_current_weekly_report():
    return jsonify({"status": "success", "report": weekly_report.generate()})

@app.route("/api/analytics/goals", methods=["GET"])
def get_goals():
    return jsonify({"status": "success", "goals": goal_dashboard.get_all()})

@app.route("/api/analytics/goals", methods=["POST"])
def add_goal():
    result = goal_dashboard.add(request.json or {})
    return jsonify({"status": "success", "goal": result})

@app.route("/api/analytics/goals/<gid>/update", methods=["POST"])
def update_goal(gid):
    data = request.json or {}
    goal_dashboard.update_progress(gid, data.get("value", 0))
    return jsonify({"status": "success"})

@app.route("/api/analytics/burnout", methods=["GET"])
def check_burnout():
    return jsonify({"status": "success", "assessment": burnout_detector.assess()})

@app.route("/api/analytics/app-quality", methods=["POST"])
def score_app_quality():
    result = app_quality_score.score(request.json or {})
    return jsonify({"status": "success", "quality": result})

@app.route("/api/analytics/best-time-apply", methods=["GET"])
def get_best_time_to_apply():
    return jsonify({"status": "success", "recommendation": best_time_apply.recommend()})

@app.route("/api/analytics/sector-breakdown", methods=["GET"])
def get_sector_breakdown():
    return jsonify({"status": "success", "breakdown": sector_breakdown.analyze()})

@app.route("/api/analytics/geo-heatmap", methods=["GET"])
def get_geo_heatmap():
    return jsonify({"status": "success", "heatmap": geo_heatmap.generate()})

@app.route("/api/analytics/response-leaderboard", methods=["GET"])
def get_response_leaderboard():
    return jsonify({"status": "success", "leaderboard": response_leaderboard.generate()})

@app.route("/api/analytics/rejection-patterns", methods=["GET"])
def get_rejection_patterns():
    return jsonify({"status": "success", "patterns": rejection_patterns.analyze()})

@app.route("/api/analytics/peer-benchmark", methods=["GET"])
def get_peer_benchmark():
    return jsonify({"status": "success", "benchmark": peer_benchmark.benchmark()})

# ============================================================
# PHASE 9: System Feature Routes
# ============================================================

@app.route("/api/theme", methods=["GET"])
def get_theme():
    return jsonify({"status": "success", "theme": theme_manager.get_theme()})

@app.route("/api/theme/toggle", methods=["POST"])
def toggle_theme():
    result = theme_manager.toggle()
    return jsonify({"status": "success", **result})

@app.route("/api/theme/set", methods=["POST"])
def set_theme():
    data = request.json or {}
    result = theme_manager.set_theme(data.get("theme", "dark"))
    return jsonify({"status": "success", **result})

@app.route("/api/shortcuts", methods=["GET"])
def get_shortcuts():
    return jsonify({"status": "success", "shortcuts": keyboard_shortcuts.get_all()})

@app.route("/api/bulk-actions", methods=["POST"])
def process_bulk_actions():
    data = request.json or {}
    result = bulk_actions_mgr.process(data.get("action", ""), data.get("ids", []), data.get("type", ""))
    return jsonify({"status": "success", "result": result})

@app.route("/api/bulk-actions/options/<item_type>", methods=["GET"])
def get_bulk_action_options(item_type):
    return jsonify({"status": "success", "actions": bulk_actions_mgr.get_available_actions(item_type)})

@app.route("/api/search", methods=["GET"])
def global_search():
    query = request.args.get("q", "")
    item_type = request.args.get("type", "all")
    result = advanced_search.search(query, item_type=item_type)
    return jsonify({"status": "success", "search": result})

@app.route("/api/search/filters", methods=["GET"])
def get_search_filters():
    return jsonify({"status": "success", "filters": advanced_search.get_filter_options()})

@app.route("/api/export/json", methods=["GET"])
def export_json():
    return jsonify({"status": "success", "export": data_export.export_json()})

@app.route("/api/export/csv/<data_type>", methods=["GET"])
def export_csv(data_type):
    result = data_export.export_csv(data_type)
    return jsonify({"status": "success", "export": result})

@app.route("/api/import/linkedin", methods=["POST"])
def import_linkedin_data():
    result = import_tools.import_linkedin_export(request.json)
    return jsonify({"status": "success", "import": result})

@app.route("/api/import/indeed", methods=["POST"])
def import_indeed_data():
    result = import_tools.import_indeed_export(request.json)
    return jsonify({"status": "success", "import": result})

@app.route("/api/import/formats", methods=["GET"])
def get_import_formats():
    return jsonify({"status": "success", "formats": import_tools.get_supported_formats()})

@app.route("/api/mobile/config", methods=["GET"])
def get_mobile_config():
    return jsonify({"status": "success", "config": mobile_responsive.get_config()})

@app.route("/api/offline/config", methods=["GET"])
def get_offline_config():
    return jsonify({"status": "success", "config": offline_mode.get_config()})

@app.route("/manifest.json")
def pwa_manifest():
    return jsonify(offline_mode.get_manifest())

@app.route("/sw.js")
def service_worker():
    from flask import Response
    return Response(offline_mode.get_service_worker(), mimetype="application/javascript")


if __name__ == "__main__":
    print("🚀 Starting Mission Control...")
    print("📍 Access at: http://localhost:5000")
    print("🔗 Or via Tailscale: https://srv1352768.tail945bbc.ts.net:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
