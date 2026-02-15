"""
Enhanced Analytics Dashboard - Predictive models, benchmarking, smart targets
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from statistics import mean, stdev

class EnhancedAnalyticsDashboard:
    """
    Advanced analytics with:
    - Predictive modeling
    - Cohort analysis
    - Industry benchmarking
    - Smart targets
    """
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.analytics_file = os.path.join(self.data_dir, 'enhanced_analytics.json')
        self.benchmarks_file = os.path.join(self.data_dir, 'industry_benchmarks.json')
        
        self.data = self._load_json(self.analytics_file, {
            'applications': [],
            'interviews': [],
            'offers': [],
            'daily_stats': []
        })
        
        self.benchmarks = self._load_benchmarks()
    
    def _load_json(self, filepath: str, default):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filepath: str, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_benchmarks(self) -> Dict:
        """Industry benchmarks for executive job search"""
        return {
            'executive_healthtech': {
                'avg_applications_to_offer': 25,
                'avg_interview_rate': 0.15,  # 15% of apps get interviews
                'avg_offer_rate': 0.25,      # 25% of interviews get offers
                'avg_time_to_offer_weeks': 12,
                'target_salary_range': {'min': 200000, 'max': 350000},
                'top_channels': ['LinkedIn', 'Executive Recruiters', 'Referrals', 'Company Websites']
            },
            'executive_general': {
                'avg_applications_to_offer': 30,
                'avg_interview_rate': 0.12,
                'avg_offer_rate': 0.20,
                'avg_time_to_offer_weeks': 16
            }
        }
    
    def add_application(self, job_data: Dict):
        """Track a new job application"""
        application = {
            'id': f"app_{len(self.data['applications']) + 1}",
            'company': job_data.get('company', ''),
            'title': job_data.get('title', ''),
            'date_applied': datetime.now().isoformat(),
            'source': job_data.get('source', 'direct'),
            'salary_listed': job_data.get('salary', 0),
            'sector': job_data.get('sector', 'unknown'),
            'referral': job_data.get('referral', False),
            'ats_score': job_data.get('ats_score', 0),
            'status': 'applied',
            'stage_dates': {
                'applied': datetime.now().isoformat()
            }
        }
        
        self.data['applications'].append(application)
        self._save_json(self.analytics_file, self.data)
    
    def update_application_status(self, app_id: str, new_status: str, notes: str = ''):
        """Update status of an application"""
        for app in self.data['applications']:
            if app['id'] == app_id:
                app['status'] = new_status
                app['stage_dates'][new_status] = datetime.now().isoformat()
                if notes:
                    app['notes'] = notes
                
                # If offer received, track it
                if new_status == 'offer':
                    self.data['offers'].append({
                        'application_id': app_id,
                        'company': app['company'],
                        'title': app['title'],
                        'date_received': datetime.now().isoformat(),
                        'salary': app.get('salary_listed', 0)
                    })
                
                self._save_json(self.analytics_file, self.data)
                return True
        return False
    
    def predict_time_to_offer(self) -> Dict:
        """
        Predict when you'll get an offer based on current activity
        """
        # Get application velocity
        recent_apps = [a for a in self.data['applications'] 
                      if (datetime.now() - datetime.fromisoformat(a['date_applied'])).days <= 30]
        
        apps_per_week = len(recent_apps) / 4 if recent_apps else 0
        
        # Get conversion rates
        total_apps = len(self.data['applications'])
        interviews = len([a for a in self.data['applications'] if a['status'] in ['interview', 'offer']])
        offers = len(self.data['offers'])
        
        interview_rate = interviews / total_apps if total_apps > 0 else 0.15
        offer_rate = offers / interviews if interviews > 0 else 0.25
        
        # Industry benchmark
        benchmark = self.benchmarks['executive_healthtech']
        
        # Calculate predictions
        if apps_per_week == 0:
            return {
                'prediction': 'No recent activity',
                'recommendation': 'Apply to at least 5 jobs this week to start momentum',
                'confidence': 'N/A'
            }
        
        # Expected timeline
        apps_needed = benchmark['avg_applications_to_offer']
        weeks_to_offer = apps_needed / apps_per_week if apps_per_week > 0 else 99
        
        # Adjust based on your actual rates vs benchmarks
        if interview_rate > benchmark['avg_interview_rate']:
            weeks_to_offer *= 0.8  # 20% faster
        if offer_rate > benchmark['avg_offer_rate']:
            weeks_to_offer *= 0.8  # Another 20% faster
        
        estimated_date = datetime.now() + timedelta(weeks=int(weeks_to_offer))
        
        return {
            'prediction': f"Estimated offer by {estimated_date.strftime('%B %d, %Y')}",
            'weeks_estimate': int(weeks_to_offer),
            'applications_needed': int(apps_needed - total_apps),
            'confidence': 'High' if total_apps > 10 else 'Medium' if total_apps > 5 else 'Low',
            'factors': [
                f"Current application rate: {apps_per_week:.1f} per week",
                f"Your interview rate: {interview_rate:.1%} (benchmark: {benchmark['avg_interview_rate']:.1%})",
                f"Your offer rate: {offer_rate:.1%} (benchmark: {benchmark['avg_offer_rate']:.1%})"
            ],
            'recommendation': self._generate_recommendation(apps_per_week, interview_rate, offer_rate)
        }
    
    def _generate_recommendation(self, apps_per_week: float, interview_rate: float, offer_rate: float) -> str:
        """Generate personalized recommendation"""
        benchmark = self.benchmarks['executive_healthtech']
        
        if apps_per_week < 2:
            return "🚨 Low volume: Apply to at least 5 jobs this week"
        elif interview_rate < benchmark['avg_interview_rate']:
            return "⚠️ Low interview rate: Review your CV and application quality"
        elif offer_rate < benchmark['avg_offer_rate']:
            return "📞 Interview skills: Practice with mock interviews"
        else:
            return "✅ On track: Keep current momentum!"
    
    def get_cohort_analysis(self) -> Dict:
        """
        Analyze which channels/strategies work best
        """
        cohorts = {
            'by_source': {},
            'by_referral': {'referral': [], 'direct': []},
            'by_sector': {},
            'by_ats_score': {'high': [], 'medium': [], 'low': []}
        }
        
        for app in self.data['applications']:
            # By source
            source = app.get('source', 'direct')
            if source not in cohorts['by_source']:
                cohorts['by_source'][source] = {'total': 0, 'interviews': 0, 'offers': 0}
            cohorts['by_source'][source]['total'] += 1
            if app['status'] in ['interview', 'offer']:
                cohorts['by_source'][source]['interviews'] += 1
            if app['status'] == 'offer':
                cohorts['by_source'][source]['offers'] += 1
            
            # By referral
            ref_type = 'referral' if app.get('referral') else 'direct'
            cohorts['by_referral'][ref_type].append(app)
            
            # By ATS score
            ats = app.get('ats_score', 0)
            if ats >= 85:
                cohorts['by_ats_score']['high'].append(app)
            elif ats >= 70:
                cohorts['by_ats_score']['medium'].append(app)
            else:
                cohorts['by_ats_score']['low'].append(app)
        
        # Calculate conversion rates
        analysis = {}
        for source, data in cohorts['by_source'].items():
            analysis[source] = {
                'total': data['total'],
                'interview_rate': data['interviews'] / data['total'] if data['total'] > 0 else 0,
                'offer_rate': data['offers'] / data['interviews'] if data['interviews'] > 0 else 0
            }
        
        # Referral vs direct comparison
        ref_interviews = len([a for a in cohorts['by_referral']['referral'] if a['status'] in ['interview', 'offer']])
        ref_total = len(cohorts['by_referral']['referral'])
        dir_interviews = len([a for a in cohorts['by_referral']['direct'] if a['status'] in ['interview', 'offer']])
        dir_total = len(cohorts['by_referral']['direct'])
        
        return {
            'by_source': analysis,
            'referral_vs_direct': {
                'referral_interview_rate': ref_interviews / ref_total if ref_total > 0 else 0,
                'direct_interview_rate': dir_interviews / dir_total if dir_total > 0 else 0,
                'referral_advantage': f"{(ref_interviews / ref_total) / (dir_interviews / dir_total):.1f}x" if ref_total and dir_total else "N/A"
            },
            'key_insight': self._generate_cohort_insight(analysis)
        }
    
    def _generate_cohort_insight(self, analysis: Dict) -> str:
        """Generate insight from cohort analysis"""
        if not analysis:
            return "Apply to more jobs to see patterns"
        
        # Find best source
        best_source = max(analysis.items(), key=lambda x: x[1]['interview_rate'])
        
        return f"Your best channel is {best_source[0]} with {best_source[1]['interview_rate']:.1%} interview rate. Focus here!"
    
    def get_smart_targets(self) -> List[Dict]:
        """
        Generate personalized weekly targets
        """
        targets = []
        
        # Get current activity
        recent_apps = len([a for a in self.data['applications']
                          if (datetime.now() - datetime.fromisoformat(a['date_applied'])).days <= 7])
        
        # Get conversion rates
        total_apps = len(self.data['applications'])
        interviews = len([a for a in self.data['applications'] if a['status'] in ['interview', 'offer']])
        interview_rate = interviews / total_apps if total_apps > 0 else 0
        
        # Target 1: Application volume
        if recent_apps < 5:
            targets.append({
                'type': 'volume',
                'target': 5,
                'current': recent_apps,
                'message': f"Apply to {5 - recent_apps} more jobs this week",
                'priority': 'high'
            })
        else:
            targets.append({
                'type': 'volume',
                'target': 5,
                'current': recent_apps,
                'message': f"✅ Great! You've applied to {recent_apps} jobs this week",
                'priority': 'completed'
            })
        
        # Target 2: Interview rate
        benchmark = self.benchmarks['executive_healthtech']['avg_interview_rate']
        if interview_rate < benchmark:
            targets.append({
                'type': 'quality',
                'target': f"{benchmark:.0%}",
                'current': f"{interview_rate:.0%}",
                'message': "Review CV quality - aim for ATS scores 85+",
                'priority': 'medium'
            })
        
        # Target 3: Network activity
        targets.append({
            'type': 'network',
            'target': 3,
            'current': 0,  # Would track separately
            'message': "Reach out to 3 contacts at target companies",
            'priority': 'medium'
        })
        
        # Target 4: Content
        targets.append({
            'type': 'content',
            'target': 2,
            'current': 0,
            'message': "Post 2 LinkedIn updates this week",
            'priority': 'low'
        })
        
        return targets
    
    def get_pipeline_visualization(self) -> Dict:
        """
        Get data for visual funnel chart
        """
        stages = {
            'applied': len(self.data['applications']),
            'screening': len([a for a in self.data['applications'] if a['status'] in ['screening', 'phone_screen']]),
            'interview': len([a for a in self.data['applications'] if a['status'] in ['interview', 'second_interview']]),
            'final': len([a for a in self.data['applications'] if a['status'] in ['final_round', 'onsite']]),
            'offer': len(self.data['offers'])
        }
        
        # Calculate conversion rates between stages
        conversions = {}
        prev_stage = stages['applied']
        for stage, count in stages.items():
            if prev_stage > 0:
                conversions[f"to_{stage}"] = count / prev_stage
            else:
                conversions[f"to_{stage}"] = 0
            prev_stage = count if count > 0 else prev_stage
        
        return {
            'stages': stages,
            'conversions': conversions,
            'benchmark_comparison': self._compare_to_benchmark(stages)
        }
    
    def _compare_to_benchmark(self, stages: Dict) -> Dict:
        """Compare to industry benchmarks"""
        benchmark = self.benchmarks['executive_healthtech']
        
        return {
            'applications': {
                'yours': stages['applied'],
                'target_for_offer': benchmark['avg_applications_to_offer'],
                'status': 'on_track' if stages['applied'] >= benchmark['avg_applications_to_offer'] / 2 else 'needs_more'
            }
        }
    
    def get_executive_summary(self) -> Dict:
        """
        Get high-level summary for dashboard
        """
        total_apps = len(self.data['applications'])
        active_apps = len([a for a in self.data['applications'] if a['status'] not in ['rejected', 'withdrawn']])
        offers = len(self.data['offers'])
        
        # This week's activity
        week_apps = len([a for a in self.data['applications']
                        if (datetime.now() - datetime.fromisoformat(a['date_applied'])).days <= 7])
        
        return {
            'total_applications': total_apps,
            'active_applications': active_apps,
            'total_offers': offers,
            'this_week_applications': week_apps,
            'prediction': self.predict_time_to_offer(),
            'top_target': self._get_top_target(),
            'weekly_goal_progress': min(week_apps / 5 * 100, 100),  # Goal: 5 apps/week
            'status': 'on_track' if week_apps >= 3 else 'needs_attention' if week_apps > 0 else 'urgent'
        }
    
    def _get_top_target(self) -> str:
        """Get top company to focus on"""
        active = [a for a in self.data['applications'] if a['status'] in ['interview', 'second_interview']]
        if active:
            return f"Focus on {active[0]['company']} - you're in interview stage!"
        return "Apply to 5 target companies this week"
