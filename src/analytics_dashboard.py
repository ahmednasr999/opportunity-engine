#!/usr/bin/env python3
"""
Analytics Dashboard - Track revenue pipeline and conversion metrics
Focus on what matters: money in the door, not vanity metrics
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import statistics

@dataclass
class RevenueMetrics:
    """Revenue pipeline metrics"""
    total_applications: int
    interviews: int
    offers: int
    accepted_offers: int
    declined_offers: int
    total_pipeline_value: float  # Sum of all active opportunity salary ranges
    weighted_pipeline_value: float  # Pipeline value × probability
    avg_offer_salary: float
    target_salary: float
    progress_to_target: float  # %

@dataclass
class ConversionFunnel:
    """Conversion funnel metrics"""
    application_to_screen: float  # %
    screen_to_interview: float    # %
    interview_to_offer: float     # %
    offer_to_accept: float        # %
    overall_conversion: float     # Application to accepted offer %

@dataclass
class ActivityMetrics:
    """Activity-based metrics"""
    applications_this_week: int
    applications_this_month: int
    content_pieces_created: int
    network_outreach_sent: int
    follow_ups_completed: int
    avg_ats_score: float
    time_to_apply_minutes: float  # Avg time from job found to application sent


class AnalyticsDashboard:
    """Revenue-focused analytics"""
    
    def __init__(self, data_dir: str = "/root/.openclaw/workspace/tools/cv-optimizer/data"):
        self.data_dir = Path(data_dir)
        self.analytics_file = self.data_dir / "analytics.json"
        self.target_annual_salary = 200000  # Ahmed's target: $200K
        self.load()
    
    def load(self):
        """Load analytics data"""
        if self.analytics_file.exists():
            with open(self.analytics_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "created_at": datetime.now().isoformat(),
                "daily_logs": [],
                "conversion_events": [],
                "revenue_tracking": {
                    "target_annual": self.target_annual_salary,
                    "current_offers": [],
                    "projected_income": 0
                }
            }
    
    def save(self):
        """Save analytics"""
        with open(self.analytics_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def calculate_revenue_metrics(self, job_tracker_data: List[Dict]) -> RevenueMetrics:
        """Calculate revenue-focused metrics"""
        total = len(job_tracker_data)
        interviews = len([j for j in job_tracker_data if j.get('status') == 'Interview'])
        offers = len([j for j in job_tracker_data if j.get('status') == 'Offer'])
        accepted = len([j for j in job_tracker_data if j.get('status') == 'Accepted'])
        declined = len([j for j in job_tracker_data if j.get('status') == 'Declined'])
        
        # Calculate pipeline value
        active_jobs = [j for j in job_tracker_data if j.get('status') not in ['Rejected', 'Declined', 'Ghosted']]
        pipeline_value = 0
        weighted_value = 0
        
        for job in active_jobs:
            # Parse salary range if available
            salary_text = job.get('salary_range', '')
            avg_salary = self._parse_salary(salary_text)
            
            # Weight by stage probability
            stage_weights = {
                'Applied': 0.05,
                'Phone Screen': 0.15,
                'Interview': 0.40,
                'Offer': 0.90
            }
            weight = stage_weights.get(job.get('status', 'Applied'), 0.05)
            
            pipeline_value += avg_salary
            weighted_value += avg_salary * weight
        
        # Calculate average offer salary
        offer_salaries = []
        for job in job_tracker_data:
            if job.get('status') == 'Offer':
                salary = self._parse_salary(job.get('salary_range', ''))
                if salary > 0:
                    offer_salaries.append(salary)
        
        avg_offer = statistics.mean(offer_salaries) if offer_salaries else 0
        
        # Progress to target
        if accepted > 0:
            progress = 100.0
        elif offer_salaries:
            progress = (statistics.mean(offer_salaries) / self.target_annual_salary) * 100
        elif weighted_value > 0:
            progress = (weighted_value / self.target_annual_salary) * 100
        else:
            progress = 0
        
        return RevenueMetrics(
            total_applications=total,
            interviews=interviews,
            offers=offers,
            accepted_offers=accepted,
            declined_offers=declined,
            total_pipeline_value=pipeline_value,
            weighted_pipeline_value=weighted_value,
            avg_offer_salary=avg_offer,
            target_salary=self.target_annual_salary,
            progress_to_target=min(progress, 100)
        )
    
    def _parse_salary(self, salary_text: str) -> float:
        """Parse salary from text"""
        if not salary_text:
            return 150000  # Default assumption
        
        # Look for numbers
        import re
        numbers = re.findall(r'(\d+)', salary_text.replace(',', ''))
        
        if numbers:
            nums = [int(n) for n in numbers]
            if len(nums) >= 2:
                return statistics.mean(nums[:2])
            elif nums:
                return nums[0]
        
        return 150000
    
    def calculate_conversion_funnel(self, job_tracker_data: List[Dict]) -> ConversionFunnel:
        """Calculate conversion rates at each stage"""
        total = len(job_tracker_data)
        if total == 0:
            return ConversionFunnel(0, 0, 0, 0, 0)
        
        screens = len([j for j in job_tracker_data if j.get('status') in ['Phone Screen', 'Interview', 'Offer', 'Accepted']])
        interviews = len([j for j in job_tracker_data if j.get('status') in ['Interview', 'Offer', 'Accepted']])
        offers = len([j for j in job_tracker_data if j.get('status') in ['Offer', 'Accepted']])
        accepted = len([j for j in job_tracker_data if j.get('status') == 'Accepted'])
        
        app_to_screen = (screens / total) * 100 if total > 0 else 0
        screen_to_int = (interviews / screens) * 100 if screens > 0 else 0
        int_to_offer = (offers / interviews) * 100 if interviews > 0 else 0
        offer_to_accept = (accepted / offers) * 100 if offers > 0 else 0
        overall = (accepted / total) * 100 if total > 0 else 0
        
        return ConversionFunnel(
            application_to_screen=app_to_screen,
            screen_to_interview=screen_to_int,
            interview_to_offer=int_to_offer,
            offer_to_accept=offer_to_accept,
            overall_conversion=overall
        )
    
    def calculate_activity_metrics(self, job_tracker_data: List[Dict]) -> ActivityMetrics:
        """Calculate activity metrics"""
        now = datetime.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # Applications this week/month
        this_week = 0
        this_month = 0
        
        for job in job_tracker_data:
            try:
                applied_date = datetime.fromisoformat(job.get('date_applied', ''))
                if applied_date > week_ago:
                    this_week += 1
                if applied_date > month_ago:
                    this_month += 1
            except:
                pass
        
        # ATS scores
        ats_scores = [j.get('ats_score', 0) for j in job_tracker_data if j.get('ats_score', 0) > 0]
        avg_ats = statistics.mean(ats_scores) if ats_scores else 0
        
        return ActivityMetrics(
            applications_this_week=this_week,
            applications_this_month=this_month,
            content_pieces_created=self.data.get('content_created_this_month', 0),
            network_outreach_sent=self.data.get('network_outreach_sent', 0),
            follow_ups_completed=self.data.get('follow_ups_completed', 0),
            avg_ats_score=avg_ats,
            time_to_apply_minutes=self.data.get('avg_time_to_apply', 0)
        )
    
    def generate_executive_summary(self) -> Dict:
        """Generate executive summary for Ahmed"""
        # Load job data
        jobs_file = self.data_dir / "job_applications.json"
        jobs = []
        if jobs_file.exists():
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
        
        revenue = self.calculate_revenue_metrics(jobs)
        funnel = self.calculate_conversion_funnel(jobs)
        activity = self.calculate_activity_metrics(jobs)
        
        summary = {
            "generated_at": datetime.now().isoformat(),
            "revenue": {
                "target_annual_salary": revenue.target_salary,
                "current_pipeline_value": revenue.weighted_pipeline_value,
                "pipeline_coverage": f"{(revenue.weighted_pipeline_value / revenue.target_salary * 100):.0f}%",
                "offers_in_hand": revenue.offers,
                "avg_offer_amount": revenue.avg_offer_salary,
                "progress_to_goal": f"{revenue.progress_to_target:.1f}%"
            },
            "conversion": {
                "application_to_interview": f"{funnel.application_to_screen:.1f}%",
                "interview_to_offer": f"{funnel.interview_to_offer:.1f}%",
                "overall": f"{funnel.overall_conversion:.1f}%",
                "benchmark": "Industry avg: 2-5%"
            },
            "activity": {
                "applications_this_week": activity.applications_this_week,
                "applications_this_month": activity.applications_this_month,
                "target_per_week": 5,
                "on_track": activity.applications_this_week >= 5,
                "avg_ats_score": f"{activity.avg_ats_score:.0f}"
            },
            "recommendations": self._generate_recommendations(revenue, funnel, activity)
        }
        
        return summary
    
    def _generate_recommendations(self, revenue: RevenueMetrics, funnel: ConversionFunnel, activity: ActivityMetrics) -> List[str]:
        """Generate actionable recommendations"""
        recs = []
        
        # Application volume
        if activity.applications_this_week < 5:
            recs.append(f"🔴 LOW VOLUME: Only {activity.applications_this_week} apps this week. Target: 5+")
        else:
            recs.append(f"🟢 VOLUME: {activity.applications_this_week} apps this week. Good pace.")
        
        # ATS scores
        if activity.avg_ats_score < 80:
            recs.append(f"🟡 ATS SCORES: Avg {activity.avg_ats_score:.0f}/100. Review CV optimization.")
        else:
            recs.append(f"🟢 ATS SCORES: Avg {activity.avg_ats_score:.0f}/100. Well optimized.")
        
        # Conversion
        if funnel.application_to_screen < 15:
            recs.append("🟡 CONVERSION: Low response rate. Consider network warm intros.")
        
        if funnel.interview_to_offer < 25:
            recs.append("🟡 INTERVIEWS: Low close rate. Practice interview skills.")
        
        # Pipeline value
        if revenue.weighted_pipeline_value < revenue.target_salary * 0.5:
            recs.append(f"🔴 PIPELINE: ${revenue.weighted_pipeline_value:,.0f} weighted value. Need more high-value targets.")
        
        if revenue.offers > 0:
            recs.append(f"🎉 OFFERS: {revenue.offers} offer(s) in hand! Negotiate aggressively.")
        
        return recs
    
    # ===== WEEKLY REPORT EMAIL - PHASE 1 FEATURE =====
    def generate_weekly_report_email(self) -> Dict:
        """Generate weekly report email content"""
        summary = self.generate_executive_summary()
        
        # Get date range for this week
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        email_subject = f"Weekly Progress Report: {week_start.strftime('%b %d')} - {week_end.strftime('%b %d')}"
        
        # Build email body
        email_body = f"""
Hi Ahmed,

Here's your weekly progress report for the week of {week_start.strftime('%B %d')} - {week_end.strftime('%B %d')}.

{'=' * 50}
📊 PIPELINE OVERVIEW
{'=' * 50}

🎯 Target Salary: ${summary['revenue']['target_annual_salary']:,}
💰 Pipeline Value: ${summary['revenue']['current_pipeline_value']:,.0f} ({summary['revenue']['pipeline_coverage']} of target)
📋 Active Offers: {summary['revenue']['offers_in_hand']}
💵 Average Offer: ${summary['revenue']['avg_offer_amount']:,.0f}

{'=' * 50}
📈 CONVERSION METRICS
{'=' * 50}

📨 Application → Interview: {summary['conversion']['application_to_interview']}
🎤 Interview → Offer: {summary['conversion']['interview_to_offer']}
📊 Overall Conversion: {summary['conversion']['overall']}
📏 Industry Benchmark: {summary['conversion']['benchmark']}

{'=' * 50}
⚡ ACTIVITY TRACKER
{'=' * 50}

📝 This Week: {summary['activity']['applications_this_week']} applications
📅 This Month: {summary['activity']['applications_this_month']} applications
🎯 Weekly Target: {summary['activity']['target_per_week']}
📈 Status: {"✅ ON TRACK" if summary['activity']['on_track'] else "⚠️ NEEDS ATTENTION"}
📊 Average ATS Score: {summary['activity']['avg_ats_score']}

{'=' * 50}
💡 RECOMMENDATIONS
{'=' * 50}

"""
        
        for rec in summary['recommendations']:
            email_body += f"{rec}\n"
        
        email_body += f"""
{'=' * 50}
📅 NEXT WEEK FOCUS
{'=' * 50}

1. {"Continue at current pace" if summary['activity']['on_track'] else "Increase application volume to 5+/week"}
2. Focus on network warm intros for better conversion
3. Schedule mock interviews to improve close rate
4. Target {summary['revenue']['target_annual_salary']:,.0f}+ roles

---
Generated: {today.strftime('%Y-%m-%d %H:%M')}
"""
        
        return {
            "subject": email_subject,
            "body": email_body,
            "summary": summary,
            "generated_at": datetime.now().isoformat()
        }
    
    def export_weekly_report(self) -> str:
        """Export weekly report"""
        summary = self.generate_executive_summary()
        
        report_lines = [
            "=" * 60,
            "WEEKLY EXECUTIVE REPORT",
            f"Generated: {summary['generated_at'][:10]}",
            "=" * 60,
            "",
            "💰 REVENUE PIPELINE",
            f"  Target Annual Salary: ${summary['revenue']['target_annual_salary']:,.0f}",
            f"  Weighted Pipeline: ${float(summary['revenue']['current_pipeline_value']):,.0f}",
            f"  Pipeline Coverage: {summary['revenue']['pipeline_coverage']}",
            f"  Offers in Hand: {summary['revenue']['offers_in_hand']}",
            f"  Progress to Goal: {summary['revenue']['progress_to_goal']}",
            "",
            "📈 CONVERSION METRICS",
            f"  App → Interview: {summary['conversion']['application_to_interview']}",
            f"  Interview → Offer: {summary['conversion']['interview_to_offer']}",
            f"  Overall: {summary['conversion']['overall']}",
            "",
            "📊 ACTIVITY",
            f"  Apps This Week: {summary['activity']['applications_this_week']}",
            f"  Apps This Month: {summary['activity']['applications_this_month']}",
            f"  Avg ATS Score: {summary['activity']['avg_ats_score']}",
            "",
            "💡 RECOMMENDATIONS",
        ]
        
        for rec in summary['recommendations']:
            report_lines.append(f"  {rec}")
        
        report_lines.extend(["", "=" * 60])
        
        report_text = "\n".join(report_lines)
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d")
        report_file = self.data_dir / f"weekly_report_{timestamp}.txt"
        with open(report_file, 'w') as f:
            f.write(report_text)
        
        return report_text


def main():
    """CLI interface"""
    import sys
    
    dashboard = AnalyticsDashboard()
    
    if len(sys.argv) < 2:
        # Generate and display report
        report = dashboard.export_weekly_report()
        print(report)
        return
    
    command = sys.argv[1]
    
    if command == "summary":
        summary = dashboard.generate_executive_summary()
        print(json.dumps(summary, indent=2))
    
    elif command == "revenue":
        # Load jobs
        jobs_file = dashboard.data_dir / "job_applications.json"
        jobs = []
        if jobs_file.exists():
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
        
        metrics = dashboard.calculate_revenue_metrics(jobs)
        print(f"\n💰 Revenue Metrics")
        print(f"Target: ${metrics.target_salary:,.0f}")
        print(f"Pipeline Value: ${metrics.weighted_pipeline_value:,.0f}")
        print(f"Offers: {metrics.offers}")
        print(f"Avg Offer: ${metrics.avg_offer_salary:,.0f}")
    
    elif command == "funnel":
        jobs_file = dashboard.data_dir / "job_applications.json"
        jobs = []
        if jobs_file.exists():
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
        
        funnel = dashboard.calculate_conversion_funnel(jobs)
        print(f"\n📈 Conversion Funnel")
        print(f"App → Screen: {funnel.application_to_screen:.1f}%")
        print(f"Screen → Interview: {funnel.screen_to_interview:.1f}%")
        print(f"Interview → Offer: {funnel.interview_to_offer:.1f}%")
        print(f"Offer → Accept: {funnel.offer_to_accept:.1f}%")
        print(f"Overall: {funnel.overall_conversion:.1f}%")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
