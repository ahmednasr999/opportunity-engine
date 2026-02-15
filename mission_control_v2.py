#!/usr/bin/env python3
"""
Mission Control v2 - Unified Web Dashboard
All 11 tools integrated: CV Optimizer, Job Tracker, Content Factory, 2nd Brain,
Network Mapper, Auto-Trigger, Voice Transcription, Analytics, Calendar, Notifications
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cv_optimizer import CVGenerator, ProfileDatabase
from job_tracker import JobTracker
from content_factory import ContentFactory
from second_brain import SecondBrain
from network_mapper import NetworkMapper
from auto_trigger import WorkflowAutomator
from voice_transcription import VoiceTranscriber, VoiceContentPipeline
from analytics_dashboard import AnalyticsDashboard
from calendar_integration import CalendarIntegration
from notification_hub import NotificationHub

app = Flask(__name__)
app.secret_key = "opportunity-engine-secret-key"

# Initialize all tools
print("🚀 Initializing Opportunity Engine v2...")
profile_db = ProfileDatabase()
cv_generator = CVGenerator(profile_db)
job_tracker = JobTracker()
content_factory = ContentFactory()
brain = SecondBrain()
network_mapper = NetworkMapper()
auto_trigger = WorkflowAutomator()
voice_transcriber = VoiceTranscriber()
voice_pipeline = VoiceContentPipeline()
analytics = AnalyticsDashboard()
calendar = CalendarIntegration()
notifications = NotificationHub()
print("✅ All 11 systems ready\n")

# ============== ROUTES ==============

@app.route("/")
def dashboard():
    """Main dashboard"""
    stats = job_tracker.get_stats()
    pipeline = job_tracker.get_pipeline()
    follow_ups = job_tracker.get_follow_ups()
    brain_stats = brain.get_stats()
    network_stats = network_mapper.get_stats()
    notif_stats = notifications.get_stats()
    
    # Get analytics summary
    try:
        jobs_file = Path("/root/.openclaw/workspace/tools/cv-optimizer/data/job_applications.json")
        jobs = []
        if jobs_file.exists():
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
        revenue = analytics.calculate_revenue_metrics(jobs)
        progress = revenue.progress_to_target
    except:
        progress = 0
    
    return render_template("dashboard_v2.html", 
                          stats=stats,
                          pipeline=pipeline,
                          follow_ups=follow_ups,
                          brain_stats=brain_stats,
                          network_stats=network_stats,
                          notif_stats=notif_stats,
                          progress=progress)

# CV Optimizer Routes
@app.route("/cv-optimizer", methods=["GET", "POST"])
def cv_optimizer():
    """CV Optimizer page"""
    result = None
    
    if request.method == "POST":
        job_text = request.form.get("job_text", "")
        company = request.form.get("company", "")
        title = request.form.get("title", "")
        
        if job_text and company and title:
            tailored_cv = cv_generator.generate(job_text, title, company)
            
            output = cv_generator.export_to_text(tailored_cv)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cv_{company.replace(' ', '_')}_{timestamp}.txt"
            filepath = Path("/root/.openclaw/workspace/tools/cv-optimizer/output") / filename
            
            with open(filepath, 'w') as f:
                f.write(output)
            
            # Add to job tracker
            job = job_tracker.add_job(company, title, cv_version=str(filepath), 
                                     ats_score=tailored_cv.ats_score)
            
            # Index in brain
            brain.ingest_job_posting(job_text, company, title)
            
            # Notify
            notifications.notify_job_added(company, title, tailored_cv.ats_score)
            
            # Auto-trigger for low ATS
            if tailored_cv.ats_score < 75:
                notifications.notify_ats_low(company, tailored_cv.ats_score, 
                                            tailored_cv.suggestions)
            
            result = {
                "ats_score": tailored_cv.ats_score,
                "match_analysis": tailored_cv.match_analysis,
                "suggestions": tailored_cv.suggestions,
                "cv_text": output,
                "filename": str(filename),
                "company": company,
                "title": title,
                "job_id": job.id
            }
            
            flash(f"✅ CV generated and job tracked! ATS Score: {tailored_cv.ats_score}/100", "success")
    
    return render_template("cv_optimizer.html", result=result)

# Job Tracker Routes
@app.route("/job-tracker")
def job_tracker_view():
    """Job Tracker page"""
    pipeline = job_tracker.get_pipeline()
    stats = job_tracker.get_stats()
    follow_ups = job_tracker.get_follow_ups()
    return render_template("job_tracker.html", pipeline=pipeline, stats=stats, follow_ups=follow_ups)

@app.route("/job-tracker/add", methods=["POST"])
def add_job():
    """Add a new job"""
    company = request.form.get("company", "")
    title = request.form.get("title", "")
    location = request.form.get("location", "")
    source = request.form.get("source", "")
    sector = request.form.get("sector", "HealthTech")
    priority = int(request.form.get("priority", 3))
    
    if company and title:
        job = job_tracker.add_job(company, title, location, source, sector, priority=priority)
        
        # Auto-trigger
        auto_trigger.on_job_added({
            "job_id": job.id,
            "company": company,
            "title": title,
            "priority": priority
        })
        
        flash(f"✅ Job added: {title} at {company}", "success")
    
    return redirect(url_for("job_tracker_view"))

@app.route("/job-tracker/update/<job_id>", methods=["POST"])
def update_job(job_id):
    """Update job status"""
    status = request.form.get("status", "")
    notes = request.form.get("notes", "")
    
    if status:
        job = job_tracker.update_status(job_id, status, notes)
        
        # Notify for important status changes
        if status == "Offer":
            notifications.notify_offer_received(job.company)
        elif status == "Interview":
            # Auto-add to calendar
            calendar.add_follow_up_reminder(job.company, "Interview prep", 1, job_id)
        
        flash(f"✅ Status updated to {status}", "success")
    
    return redirect(url_for("job_tracker_view"))

# Content Factory Routes
@app.route("/content-factory", methods=["GET", "POST"])
def content_factory_view():
    """Content Factory page"""
    result = None
    
    if request.method == "POST":
        content_type = request.form.get("content_type", "linkedin")
        topic = request.form.get("topic", "healthtech_ai")
        
        if content_type == "linkedin":
            result = content_factory.generate_linkedin_post(topic)
            notifications.notify_content_generated("LinkedIn", result.get('character_count', 0))
        elif content_type == "newsletter":
            result = content_factory.generate_newsletter("weekly_roundup")
            notifications.notify_content_generated("Newsletter", result.get('word_count', 0))
        elif content_type == "calendar":
            calendar_data = content_factory.generate_content_calendar(30)
            result = {"type": "calendar", "calendar": calendar_data[:10], "total": len(calendar_data)}
        
        if result and content_type != "calendar":
            filepath = content_factory.save_content(result)
            result['saved_to'] = str(filepath)
    
    return render_template("content_factory.html", result=result)

# 2nd Brain Routes
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
    return render_template("second_brain.html", results=results, query=query, stats=stats)

# Network Mapper Routes
@app.route("/network")
def network_view():
    """Network Mapper page"""
    stats = network_mapper.get_stats()
    follow_ups = network_mapper.get_follow_ups()
    suggestions = network_mapper.suggest_outreach()
    
    return render_template("network_mapper.html", 
                          stats=stats,
                          follow_ups=follow_ups,
                          suggestions=suggestions)

@app.route("/network/add", methods=["POST"])
def add_contact():
    """Add a new contact"""
    name = request.form.get("name", "")
    title = request.form.get("title", "")
    company = request.form.get("company", "")
    contact_type = request.form.get("contact_type", "peer")
    sector = request.form.get("sector", "")
    
    if name and title and company:
        network_mapper.add_contact(name, title, company, contact_type, sector)
        flash(f"✅ Contact added: {name}", "success")
    
    return redirect(url_for("network_view"))

# Analytics Routes
@app.route("/analytics")
def analytics_view():
    """Analytics Dashboard"""
    # Load jobs
    jobs_file = Path("/root/.openclaw/workspace/tools/cv-optimizer/data/job_applications.json")
    jobs = []
    if jobs_file.exists():
        with open(jobs_file, 'r') as f:
            jobs = json.load(f)
    
    revenue = analytics.calculate_revenue_metrics(jobs)
    funnel = analytics.calculate_conversion_funnel(jobs)
    activity = analytics.calculate_activity_metrics(jobs)
    summary = analytics.generate_executive_summary()
    
    return render_template("analytics.html",
                          revenue=revenue,
                          funnel=funnel,
                          activity=activity,
                          summary=summary)

# Calendar Routes
@app.route("/calendar")
def calendar_view():
    """Calendar view"""
    upcoming = calendar.get_upcoming_events(14)
    return render_template("calendar.html", events=upcoming)

@app.route("/calendar/add-interview", methods=[["POST"]])
def add_interview():
    """Add interview to calendar"""
    company = request.form.get("company", "")
    role = request.form.get("role", "")
    date = request.form.get("date", "")
    time = request.form.get("time", "")
    location = request.form.get("location", "")
    
    if company and role and date and time:
        event = calendar.schedule_interview(company, role, date, time, location=location)
        notifications.notify_interview_scheduled(company, date, time)
        flash(f"✅ Interview scheduled with {company}", "success")
    
    return redirect(url_for("calendar_view"))

# Notifications Routes
@app.route("/notifications")
def notifications_view():
    """Notifications page"""
    unread = notifications.get_unread()
    stats = notifications.get_stats()
    action_required = notifications.get_action_required()
    
    return render_template("notifications.html",
                          notifications=unread,
                          stats=stats,
                          action_required=action_required)

@app.route("/notifications/mark-read/<notif_id>")
def mark_notif_read(notif_id):
    """Mark notification as read"""
    notifications.mark_read(notif_id)
    return redirect(url_for("notifications_view"))

# Voice Routes
@app.route("/voice", methods=["GET", "POST"])
def voice_view():
    """Voice transcription page"""
    result = None
    
    if request.method == "POST":
        # This would handle file upload in production
        content_type = request.form.get("content_type", "linkedin")
        flash("🎙️ Voice transcription ready. Upload audio file to process.", "info")
    
    return render_template("voice.html", result=result)

# API Endpoints
@app.route("/api/stats")
def api_stats():
    """API endpoint for stats"""
    return jsonify({
        "jobs": job_tracker.get_stats(),
        "brain": brain.get_stats(),
        "network": network_mapper.get_stats(),
        "notifications": notifications.get_stats()
    })

@app.route("/api/notifications/unread-count")
def api_unread_count():
    """Get unread notification count"""
    stats = notifications.get_stats()
    return jsonify({"unread": stats['unread'], "action_required": stats['action_required']})

if __name__ == "__main__":
    print("🚀 Starting Mission Control v2...")
    print("📍 Access at: http://localhost:5000")
    print("🔗 Tailscale: https://srv1352768.tail945bbc.ts.net:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
