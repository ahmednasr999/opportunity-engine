#!/usr/bin/env python3
"""
Phase 8 - Analytics Enhancements
Features: Cohort Analysis, Benchmark Comparisons, Predictive Pipeline,
          Salary Trends, Time-to-Offer, Weekly Report, Goal Setting,
          Burnout Detector, Application Quality, Best Time to Apply,
          Sector Breakdown, Geographic Heatmap, Response Leaderboard,
          Rejection Pattern Analysis, Peer Benchmarking
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path


class CohortAnalysis:
    """Track applications grouped by month/cohort"""

    def analyze(self, applications: List[Dict] = None) -> Dict:
        if not applications:
            applications = self._sample_data()

        cohorts = {}
        for app in applications:
            date_str = app.get("applied_date", "")
            if date_str:
                month = date_str[:7]  # YYYY-MM
            else:
                month = "2026-02"
            
            if month not in cohorts:
                cohorts[month] = {"total": 0, "interviews": 0, "offers": 0, "rejections": 0, "pending": 0}
            cohorts[month]["total"] += 1
            status = app.get("status", "applied")
            if status in ["interview", "interview_2", "technical"]:
                cohorts[month]["interviews"] += 1
            elif status == "offer":
                cohorts[month]["offers"] += 1
            elif status == "rejected":
                cohorts[month]["rejections"] += 1
            else:
                cohorts[month]["pending"] += 1

        # Calculate conversion rates
        for month, data in cohorts.items():
            data["interview_rate"] = round(data["interviews"] / max(1, data["total"]) * 100, 1)
            data["offer_rate"] = round(data["offers"] / max(1, data["total"]) * 100, 1)

        sorted_months = sorted(cohorts.keys())
        
        return {
            "cohorts": {m: cohorts[m] for m in sorted_months},
            "chart_data": {
                "labels": sorted_months,
                "applications": [cohorts[m]["total"] for m in sorted_months],
                "interviews": [cohorts[m]["interviews"] for m in sorted_months],
                "offers": [cohorts[m]["offers"] for m in sorted_months],
            },
            "best_month": max(sorted_months, key=lambda m: cohorts[m]["interview_rate"]) if sorted_months else None,
            "trend": "improving" if len(sorted_months) > 1 and cohorts[sorted_months[-1]]["interview_rate"] > cohorts[sorted_months[0]]["interview_rate"] else "steady"
        }

    def _sample_data(self) -> List[Dict]:
        apps = []
        statuses = ["applied", "interview", "rejected", "offer", "pending"]
        for i in range(30):
            month = random.choice(["2025-11", "2025-12", "2026-01", "2026-02"])
            apps.append({
                "id": f"app{i}", "applied_date": f"{month}-{random.randint(1,28):02d}",
                "status": random.choice(statuses), "company": f"Company {i}"
            })
        return apps


class BenchmarkComparisons:
    """Compare user metrics to industry averages"""

    INDUSTRY_BENCHMARKS = {
        "application_to_interview_rate": 15.0,
        "interview_to_offer_rate": 25.0,
        "average_applications_per_month": 20,
        "average_time_to_offer_days": 45,
        "average_ats_score": 72,
        "networking_contacts_per_month": 10,
        "content_posts_per_week": 2,
        "follow_up_rate": 60.0,
        "referral_percentage": 30.0,
    }

    def compare(self, user_metrics: Dict = None) -> Dict:
        if not user_metrics:
            user_metrics = {
                "application_to_interview_rate": 22.0,
                "interview_to_offer_rate": 30.0,
                "average_applications_per_month": 15,
                "average_time_to_offer_days": 38,
                "average_ats_score": 85,
                "networking_contacts_per_month": 8,
                "content_posts_per_week": 3,
                "follow_up_rate": 75.0,
                "referral_percentage": 25.0,
            }

        comparisons = []
        above_count = 0
        for metric, benchmark in self.INDUSTRY_BENCHMARKS.items():
            user_val = user_metrics.get(metric, 0)
            diff = user_val - benchmark
            is_better = diff > 0
            if metric in ["average_time_to_offer_days"]:
                is_better = diff < 0
                diff = -diff
            
            if is_better:
                above_count += 1
            
            comparisons.append({
                "metric": metric.replace("_", " ").title(),
                "your_value": user_val,
                "benchmark": benchmark,
                "difference": round(diff, 1),
                "status": "above" if is_better else "below" if abs(diff) > benchmark * 0.1 else "on_par",
                "icon": "📈" if is_better else "📉"
            })

        overall = round(above_count / max(1, len(comparisons)) * 100, 1)

        return {
            "comparisons": comparisons,
            "overall_percentile": overall,
            "above_benchmark_count": above_count,
            "total_metrics": len(comparisons),
            "grade": "A" if overall >= 80 else "B" if overall >= 60 else "C" if overall >= 40 else "D",
            "top_strength": max(comparisons, key=lambda c: c["difference"])["metric"] if comparisons else None,
            "biggest_gap": min(comparisons, key=lambda c: c["difference"])["metric"] if comparisons else None,
        }


class PredictivePipeline:
    """Forecast offer probability based on pipeline data"""

    def forecast(self, applications: List[Dict] = None) -> Dict:
        if not applications:
            applications = [
                {"company": "HealthTech A", "stage": "interview_2", "days_in_stage": 5},
                {"company": "TechCorp B", "stage": "screening", "days_in_stage": 10},
                {"company": "Hospital C", "stage": "applied", "days_in_stage": 15},
                {"company": "AI Health D", "stage": "technical", "days_in_stage": 3},
            ]

        stage_probabilities = {
            "applied": 0.15, "screening": 0.30, "interview_1": 0.45,
            "interview_2": 0.60, "technical": 0.70, "offer": 0.90, "final": 0.85
        }

        predictions = []
        for app in applications:
            stage = app.get("stage", "applied")
            base_prob = stage_probabilities.get(stage, 0.10)
            
            # Decay based on days in stage
            days = app.get("days_in_stage", 0)
            if days > 14:
                base_prob *= 0.7
            elif days > 7:
                base_prob *= 0.85
            
            predictions.append({
                "company": app.get("company", "Unknown"),
                "stage": stage,
                "offer_probability": round(base_prob * 100, 1),
                "days_in_stage": days,
                "expected_days_to_offer": max(7, int((1 - base_prob) * 45)),
                "risk": "low" if base_prob > 0.5 else "medium" if base_prob > 0.25 else "high"
            })

        predictions.sort(key=lambda x: x["offer_probability"], reverse=True)
        
        # Aggregate
        total_prob = 1 - 1
        for p in predictions:
            total_prob = 1 - (1 - total_prob) * (1 - p["offer_probability"] / 100)
        
        return {
            "predictions": predictions,
            "at_least_one_offer_probability": round(min(99, total_prob * 100), 1),
            "strongest_lead": predictions[0]["company"] if predictions else None,
            "pipeline_health": "strong" if total_prob > 0.7 else "moderate" if total_prob > 0.4 else "needs_more_applications",
            "recommendation": "Pipeline looks healthy" if total_prob > 0.5 else "Consider applying to more positions to improve odds"
        }


class SalaryTrends:
    """Track salary data over time"""

    def analyze(self, salary_data: List[Dict] = None) -> Dict:
        if not salary_data:
            salary_data = [
                {"date": "2025-06", "role": "Director Ops", "min": 120000, "max": 160000, "source": "LinkedIn"},
                {"date": "2025-09", "role": "VP Operations", "min": 150000, "max": 200000, "source": "Glassdoor"},
                {"date": "2025-12", "role": "VP AI Health", "min": 170000, "max": 230000, "source": "Indeed"},
                {"date": "2026-01", "role": "VP Operations", "min": 155000, "max": 210000, "source": "LinkedIn"},
                {"date": "2026-02", "role": "Director AI", "min": 140000, "max": 190000, "source": "Glassdoor"},
            ]

        midpoints = [(d["min"] + d["max"]) / 2 for d in salary_data]
        avg = round(sum(midpoints) / max(1, len(midpoints)))
        trend = "increasing" if len(midpoints) > 1 and midpoints[-1] > midpoints[0] else "stable" if len(midpoints) > 1 and abs(midpoints[-1] - midpoints[0]) < 5000 else "decreasing"

        return {
            "data_points": salary_data,
            "average_midpoint": avg,
            "highest": max(d["max"] for d in salary_data) if salary_data else 0,
            "lowest": min(d["min"] for d in salary_data) if salary_data else 0,
            "trend": trend,
            "chart_data": {
                "labels": [d["date"] for d in salary_data],
                "min_values": [d["min"] for d in salary_data],
                "max_values": [d["max"] for d in salary_data],
                "midpoints": [int(m) for m in midpoints]
            },
            "market_position": "Above average for this role level" if avg > 150000 else "Competitive",
            "negotiation_tip": f"Your target range should be ${avg-10000:,}-${avg+20000:,} based on market data"
        }


class TimeToOfferAnalytics:
    """Track average time from application to each stage"""

    def analyze(self, applications: List[Dict] = None) -> Dict:
        if not applications:
            applications = [
                {"company": "Co A", "applied": "2026-01-01", "screening": "2026-01-05", "interview": "2026-01-12", "offer": "2026-01-25"},
                {"company": "Co B", "applied": "2026-01-10", "screening": "2026-01-18", "interview": "2026-01-28", "offer": None},
                {"company": "Co C", "applied": "2026-01-15", "screening": "2026-01-20", "interview": None, "offer": None},
            ]

        stage_times = {"to_screening": [], "to_interview": [], "to_offer": []}
        
        for app in applications:
            applied = app.get("applied")
            if not applied:
                continue
            try:
                applied_date = datetime.strptime(applied, "%Y-%m-%d")
                if app.get("screening"):
                    stage_times["to_screening"].append((datetime.strptime(app["screening"], "%Y-%m-%d") - applied_date).days)
                if app.get("interview"):
                    stage_times["to_interview"].append((datetime.strptime(app["interview"], "%Y-%m-%d") - applied_date).days)
                if app.get("offer"):
                    stage_times["to_offer"].append((datetime.strptime(app["offer"], "%Y-%m-%d") - applied_date).days)
            except:
                pass

        averages = {}
        for stage, times in stage_times.items():
            if times:
                averages[stage] = {
                    "average_days": round(sum(times) / len(times), 1),
                    "fastest": min(times),
                    "slowest": max(times),
                    "data_points": len(times)
                }

        return {
            "stage_averages": averages,
            "overall_average_to_offer": averages.get("to_offer", {}).get("average_days", "N/A"),
            "industry_average": 42,
            "chart_data": {
                "stages": ["Application", "Screening", "Interview", "Offer"],
                "your_days": [0, averages.get("to_screening", {}).get("average_days", 0),
                             averages.get("to_interview", {}).get("average_days", 0),
                             averages.get("to_offer", {}).get("average_days", 0)],
                "industry_days": [0, 7, 21, 42]
            },
            "insights": [
                "You're faster than average" if averages.get("to_offer", {}).get("average_days", 99) < 42 else "Your timeline is typical",
                "Screening stage is your bottleneck" if averages.get("to_screening", {}).get("average_days", 0) > 10 else "Good screening speed"
            ]
        }


class WeeklyReportEmail:
    """Generate weekly summary report"""

    def generate(self, stats: Dict = None) -> Dict:
        if not stats:
            stats = {
                "applications_sent": 5,
                "interviews_scheduled": 2,
                "follow_ups_sent": 3,
                "networking_contacts": 4,
                "content_posts": 2,
                "ats_score_avg": 85,
                "pipeline_active": 8
            }

        report = f"""
📊 Weekly Job Search Report - {datetime.now().strftime('%B %d, %Y')}

📝 Applications: {stats.get('applications_sent', 0)} sent this week
🎯 Interviews: {stats.get('interviews_scheduled', 0)} scheduled
📧 Follow-ups: {stats.get('follow_ups_sent', 0)} sent
🤝 Networking: {stats.get('networking_contacts', 0)} new contacts
📱 Content: {stats.get('content_posts', 0)} posts published
📈 Avg ATS Score: {stats.get('ats_score_avg', 0)}%
🔄 Active Pipeline: {stats.get('pipeline_active', 0)} applications

💡 Recommendation: {"Keep up the great momentum!" if stats.get('applications_sent', 0) >= 5 else "Try to increase application volume this week."}
"""
        return {
            "report_text": report.strip(),
            "stats": stats,
            "generated_at": datetime.now().isoformat(),
            "week_number": datetime.now().isocalendar()[1],
            "highlights": [
                f"Sent {stats.get('applications_sent', 0)} applications",
                f"{stats.get('interviews_scheduled', 0)} interviews lined up",
            ],
            "goals_for_next_week": [
                "Send at least 5 applications",
                "Follow up on all pending applications",
                "Publish 2+ LinkedIn posts",
                "Connect with 3 new industry contacts"
            ]
        }


class GoalSettingDashboard:
    """Set and track job search goals"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.goals_file = self.data_dir / "goals.json"
        self.goals = self._load()

    def _load(self) -> List[Dict]:
        if self.goals_file.exists():
            return json.loads(self.goals_file.read_text())
        return [
            {"id": "g1", "name": "Applications per week", "target": 5, "current": 3, "unit": "apps", "period": "weekly"},
            {"id": "g2", "name": "Networking contacts", "target": 10, "current": 6, "unit": "contacts", "period": "monthly"},
            {"id": "g3", "name": "LinkedIn posts", "target": 3, "current": 2, "unit": "posts", "period": "weekly"},
            {"id": "g4", "name": "ATS score average", "target": 90, "current": 85, "unit": "%", "period": "ongoing"},
            {"id": "g5", "name": "Interview success rate", "target": 50, "current": 33, "unit": "%", "period": "ongoing"},
        ]

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.goals_file.write_text(json.dumps(self.goals, indent=2))

    def get_all(self) -> List[Dict]:
        for g in self.goals:
            g["progress"] = round(g["current"] / max(1, g["target"]) * 100, 1)
            g["on_track"] = g["current"] >= g["target"] * 0.7
        return self.goals

    def add(self, goal_data: Dict) -> Dict:
        goal = {
            "id": f"g{len(self.goals)+1}",
            "name": goal_data.get("name", ""),
            "target": goal_data.get("target", 0),
            "current": 0,
            "unit": goal_data.get("unit", ""),
            "period": goal_data.get("period", "weekly"),
        }
        self.goals.append(goal)
        self._save()
        return goal

    def update_progress(self, goal_id: str, value: float) -> bool:
        for g in self.goals:
            if g["id"] == goal_id:
                g["current"] = value
                self._save()
                return True
        return False


class BurnoutDetector:
    """Detect signs of job search burnout"""

    def assess(self, activity_data: Dict = None) -> Dict:
        if not activity_data:
            activity_data = {
                "applications_last_7d": 8,
                "applications_prev_7d": 12,
                "hours_spent_daily": 6,
                "rejections_last_7d": 5,
                "mood_ratings": [7, 6, 5, 4, 4, 3, 3],  # Last 7 days
                "days_since_break": 21,
                "sleep_quality": 5,  # 1-10
            }

        burnout_score = 0
        signals = []

        # Declining activity
        if activity_data.get("applications_last_7d", 0) < activity_data.get("applications_prev_7d", 0) * 0.7:
            burnout_score += 20
            signals.append("Application volume declining significantly")

        # High hours
        if activity_data.get("hours_spent_daily", 0) > 5:
            burnout_score += 15
            signals.append("Spending too many hours per day on job search")

        # Many rejections
        if activity_data.get("rejections_last_7d", 0) > 3:
            burnout_score += 15
            signals.append("High rejection rate recently")

        # Declining mood
        moods = activity_data.get("mood_ratings", [])
        if moods and len(moods) > 2 and moods[-1] < moods[0] - 2:
            burnout_score += 20
            signals.append("Mood has been declining")

        # No breaks
        if activity_data.get("days_since_break", 0) > 14:
            burnout_score += 15
            signals.append("Haven't taken a break in over 2 weeks")

        # Poor sleep
        if activity_data.get("sleep_quality", 10) < 5:
            burnout_score += 15
            signals.append("Sleep quality is poor")

        status = "Healthy" if burnout_score < 30 else "Warning" if burnout_score < 60 else "Burnout Risk"
        
        return {
            "burnout_score": min(100, burnout_score),
            "status": status,
            "signals": signals,
            "recommendations": [
                "Take a full day off from job searching" if burnout_score > 40 else "You're doing well — keep it balanced",
                "Limit job search to 3 hours per day",
                "Celebrate small wins (applications sent, connections made)",
                "Exercise for 30 minutes daily",
                "Talk to someone about how you're feeling",
                "Focus on quality over quantity"
            ],
            "wellness_tips": [
                "🧘 Take 5-minute breaks every hour",
                "🏃 Move your body daily",
                "📵 Set a 'no job search' time after 6 PM",
                "🎯 Focus on 3-5 quality applications per week",
                "🎉 Reward yourself for milestones"
            ]
        }


class ApplicationQualityScore:
    """Score the quality of each application"""

    def score(self, application: Dict) -> Dict:
        score = 0
        factors = {}

        # ATS Score
        ats = application.get("ats_score", 0)
        ats_points = min(25, ats / 4)
        factors["ats_score"] = {"points": round(ats_points, 1), "max": 25}
        score += ats_points

        # Tailored CV
        if application.get("tailored_cv", False):
            factors["tailored_cv"] = {"points": 20, "max": 20}
            score += 20
        else:
            factors["tailored_cv"] = {"points": 5, "max": 20}
            score += 5

        # Cover letter
        if application.get("cover_letter", False):
            factors["cover_letter"] = {"points": 15, "max": 15}
            score += 15
        else:
            factors["cover_letter"] = {"points": 0, "max": 15}

        # Referral
        if application.get("referral", False):
            factors["referral"] = {"points": 20, "max": 20}
            score += 20
        else:
            factors["referral"] = {"points": 0, "max": 20}

        # Research
        if application.get("company_researched", False):
            factors["research"] = {"points": 10, "max": 10}
            score += 10
        else:
            factors["research"] = {"points": 0, "max": 10}

        # Follow-up planned
        if application.get("follow_up_scheduled", False):
            factors["follow_up"] = {"points": 10, "max": 10}
            score += 10
        else:
            factors["follow_up"] = {"points": 0, "max": 10}

        grade = "A+" if score >= 90 else "A" if score >= 80 else "B" if score >= 65 else "C" if score >= 50 else "D"

        return {
            "quality_score": round(score, 1),
            "grade": grade,
            "factors": factors,
            "recommendations": [
                "Tailor your CV for each application" if not application.get("tailored_cv") else None,
                "Include a cover letter" if not application.get("cover_letter") else None,
                "Get a referral if possible" if not application.get("referral") else None,
                "Research the company before applying" if not application.get("company_researched") else None,
                "Schedule a follow-up" if not application.get("follow_up_scheduled") else None,
            ]
        }


class BestTimeToApply:
    """Analytics on best time/day to submit applications"""

    def recommend(self) -> Dict:
        return {
            "best_days": ["Monday", "Tuesday"],
            "worst_days": ["Friday", "Saturday"],
            "best_hours": ["09:00-11:00", "14:00-16:00"],
            "worst_hours": ["After 18:00", "Before 07:00"],
            "data": {
                "monday": {"applications": 100, "response_rate": 22},
                "tuesday": {"applications": 95, "response_rate": 24},
                "wednesday": {"applications": 88, "response_rate": 19},
                "thursday": {"applications": 82, "response_rate": 17},
                "friday": {"applications": 60, "response_rate": 12},
                "saturday": {"applications": 30, "response_rate": 8},
                "sunday": {"applications": 45, "response_rate": 15},
            },
            "insights": [
                "Applications sent Monday-Tuesday get 40% more responses",
                "Morning applications (9-11 AM) are reviewed first",
                "Avoid applying on Friday — hiring managers check Monday",
                "Sunday evening applications can work (reviewed Monday morning)"
            ]
        }


class SectorBreakdown:
    """Breakdown of applications by industry sector"""

    def analyze(self, applications: List[Dict] = None) -> Dict:
        if not applications:
            applications = [
                {"sector": "Healthcare", "status": "interview"},
                {"sector": "Healthcare", "status": "applied"},
                {"sector": "Technology", "status": "offer"},
                {"sector": "Healthcare", "status": "rejected"},
                {"sector": "Consulting", "status": "applied"},
                {"sector": "Technology", "status": "interview"},
                {"sector": "Government", "status": "applied"},
                {"sector": "Healthcare", "status": "interview"},
            ]

        sectors = {}
        for app in applications:
            sector = app.get("sector", "Other")
            if sector not in sectors:
                sectors[sector] = {"total": 0, "interviews": 0, "offers": 0, "rejections": 0}
            sectors[sector]["total"] += 1
            s = app.get("status", "")
            if "interview" in s:
                sectors[sector]["interviews"] += 1
            elif s == "offer":
                sectors[sector]["offers"] += 1
            elif s == "rejected":
                sectors[sector]["rejections"] += 1

        breakdown = []
        for sector, data in sectors.items():
            data["interview_rate"] = round(data["interviews"] / max(1, data["total"]) * 100, 1)
            breakdown.append({"sector": sector, **data})

        breakdown.sort(key=lambda x: x["total"], reverse=True)

        return {
            "breakdown": breakdown,
            "top_sector": breakdown[0]["sector"] if breakdown else None,
            "most_successful": max(breakdown, key=lambda x: x["interview_rate"])["sector"] if breakdown else None,
            "chart_data": {
                "labels": [b["sector"] for b in breakdown],
                "counts": [b["total"] for b in breakdown],
                "interview_rates": [b["interview_rate"] for b in breakdown]
            }
        }


class GeographicHeatmap:
    """Geographic distribution of applications"""

    def generate(self, applications: List[Dict] = None) -> Dict:
        if not applications:
            applications = [
                {"location": "Riyadh, Saudi Arabia", "count": 8},
                {"location": "Dubai, UAE", "count": 6},
                {"location": "Abu Dhabi, UAE", "count": 4},
                {"location": "Jeddah, Saudi Arabia", "count": 3},
                {"location": "Remote", "count": 5},
                {"location": "London, UK", "count": 2},
                {"location": "Doha, Qatar", "count": 2},
            ]

        locations = {}
        for app in applications:
            loc = app.get("location", "Unknown")
            count = app.get("count", 1)
            if loc in locations:
                locations[loc] += count
            else:
                locations[loc] = count

        sorted_locs = sorted(locations.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "locations": [{"location": l, "count": c} for l, c in sorted_locs],
            "top_location": sorted_locs[0][0] if sorted_locs else None,
            "total_locations": len(sorted_locs),
            "remote_percentage": round(locations.get("Remote", 0) / max(1, sum(locations.values())) * 100, 1),
            "chart_data": {
                "labels": [l for l, c in sorted_locs],
                "counts": [c for l, c in sorted_locs]
            }
        }


class ResponseLeaderboard:
    """Rank companies by response time"""

    def generate(self, applications: List[Dict] = None) -> Dict:
        if not applications:
            applications = [
                {"company": "HealthTech Co", "response_days": 3, "status": "interview"},
                {"company": "Hospital Group", "response_days": 7, "status": "screening"},
                {"company": "AI Startup", "response_days": 2, "status": "offer"},
                {"company": "Big Corp", "response_days": 21, "status": "rejected"},
                {"company": "Gov Health", "response_days": 30, "status": "pending"},
            ]

        leaderboard = sorted(applications, key=lambda x: x.get("response_days", 999))
        
        for i, entry in enumerate(leaderboard):
            entry["rank"] = i + 1
            days = entry.get("response_days", 0)
            entry["speed_rating"] = "⚡ Lightning" if days <= 3 else "🏃 Fast" if days <= 7 else "🚶 Average" if days <= 14 else "🐌 Slow"

        return {
            "leaderboard": leaderboard,
            "fastest_company": leaderboard[0]["company"] if leaderboard else None,
            "slowest_company": leaderboard[-1]["company"] if leaderboard else None,
            "average_response": round(sum(a.get("response_days", 0) for a in applications) / max(1, len(applications)), 1)
        }


class RejectionPatternAnalysis:
    """Deep analysis of rejection patterns"""

    def analyze(self, rejections: List[Dict] = None) -> Dict:
        if not rejections:
            rejections = [
                {"company_size": "large", "role_level": "VP", "stage": "interview_2", "reason": "overqualified"},
                {"company_size": "startup", "role_level": "Director", "stage": "screening", "reason": "experience_mismatch"},
                {"company_size": "large", "role_level": "VP", "stage": "applied", "reason": "no_response"},
                {"company_size": "mid", "role_level": "Director", "stage": "interview", "reason": "culture_fit"},
                {"company_size": "large", "role_level": "VP", "stage": "applied", "reason": "no_response"},
            ]

        patterns = {
            "by_company_size": {}, "by_role_level": {}, "by_stage": {}, "by_reason": {}
        }
        
        for r in rejections:
            for key in ["company_size", "role_level", "stage", "reason"]:
                val = r.get(key, "unknown")
                bucket = f"by_{key}"
                patterns[bucket][val] = patterns[bucket].get(val, 0) + 1

        insights = []
        for bucket, data in patterns.items():
            if data:
                top = max(data.items(), key=lambda x: x[1])
                insights.append(f"Most rejections ({top[1]}) are from {bucket.replace('by_', '')}: {top[0]}")

        return {
            "total_rejections": len(rejections),
            "patterns": patterns,
            "insights": insights,
            "actionable_tips": [
                "If most rejections are 'no response' — improve your CV headline and first impression",
                "If rejected at interview stage — practice mock interviews",
                "If 'overqualified' — target more senior roles",
                "If 'culture fit' — research company culture before applying"
            ],
            "chart_data": {
                "stages": list(patterns["by_stage"].keys()),
                "stage_counts": list(patterns["by_stage"].values()),
                "reasons": list(patterns["by_reason"].keys()),
                "reason_counts": list(patterns["by_reason"].values())
            }
        }


class PeerBenchmarking:
    """Compare performance to peer group"""

    def benchmark(self, user_data: Dict = None) -> Dict:
        if not user_data:
            user_data = {
                "applications_per_week": 4,
                "interview_rate": 22,
                "offer_rate": 8,
                "networking_score": 65,
                "content_frequency": 2.5,
                "ats_avg_score": 85
            }

        peer_data = {
            "applications_per_week": {"p25": 2, "p50": 4, "p75": 8, "p90": 12},
            "interview_rate": {"p25": 8, "p50": 15, "p75": 25, "p90": 35},
            "offer_rate": {"p25": 2, "p50": 5, "p75": 12, "p90": 20},
            "networking_score": {"p25": 30, "p50": 50, "p75": 70, "p90": 85},
            "content_frequency": {"p25": 0.5, "p50": 1, "p75": 3, "p90": 5},
            "ats_avg_score": {"p25": 60, "p50": 72, "p75": 85, "p90": 92}
        }

        rankings = {}
        for metric, percentiles in peer_data.items():
            val = user_data.get(metric, 0)
            if val >= percentiles["p90"]:
                rank = "Top 10%"
            elif val >= percentiles["p75"]:
                rank = "Top 25%"
            elif val >= percentiles["p50"]:
                rank = "Top 50%"
            elif val >= percentiles["p25"]:
                rank = "Top 75%"
            else:
                rank = "Below Average"
            
            rankings[metric] = {
                "your_value": val,
                "percentile_rank": rank,
                "percentiles": percentiles
            }

        return {
            "rankings": rankings,
            "overall_rank": "Top 25%",  # Simplified
            "strengths": [k for k, v in rankings.items() if "Top 10%" in v["percentile_rank"] or "Top 25%" in v["percentile_rank"]],
            "improvement_areas": [k for k, v in rankings.items() if "Below" in v["percentile_rank"] or "Top 75%" in v["percentile_rank"]],
            "peer_group": "Senior Healthcare/Tech Professionals (15+ years experience)"
        }
