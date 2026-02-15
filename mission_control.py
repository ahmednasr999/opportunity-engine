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
            
            result = {
                "ats_score": tailored_cv.ats_score,
                "match_analysis": tailored_cv.match_analysis,
                "suggestions": tailored_cv.suggestions,
                "cv_text": output,
                "filename": str(filename),
                "company": company,
                "title": title
            }
    
    return render_template("cv_optimizer.html", result=result)

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
    """Add a new job"""
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

if __name__ == "__main__":
    print("🚀 Starting Mission Control...")
    print("📍 Access at: http://localhost:5000")
    print("🔗 Or via Tailscale: https://srv1352768.tail945bbc.ts.net:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
