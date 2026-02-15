"""
Product Management Tool - Meta-tool to manage Opportunity Engine development
Track missing features, prioritize builds, generate new ideas
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class ProductManager:
    """
    Manages the development of all 14 tools:
    - Catalogs missing features
    - Tracks what's built vs planned
    - Generates new feature ideas
    - Prioritizes based on impact/effort
    """
    
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.features_file = os.path.join(self.data_dir, 'product_features.json')
        self.roadmap_file = os.path.join(self.data_dir, 'product_roadmap.json')
        
        self.features = self._load_features()
        self.roadmap = self._load_json(self.roadmap_file, [])
    
    def _load_json(self, filepath: str, default):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return default
    
    def _save_json(self, filepath: str, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_features(self) -> Dict:
        """Load or initialize feature catalog"""
        if os.path.exists(self.features_file):
            with open(self.features_file, 'r') as f:
                return json.load(f)
        
        # Initialize with comprehensive missing features
        return self._initialize_feature_catalog()
    
    def _initialize_feature_catalog(self) -> Dict:
        """Create initial feature catalog for all 14 tools"""
        catalog = {
            'cv_optimizer': {
                'name': 'CV Optimizer',
                'icon': 'fa-file-alt',
                'built_features': [
                    'PDF export with professional formatting',
                    'LinkedIn job URL import',
                    'ATS scoring algorithm',
                    'AI-powered content rewriting',
                    'Cover letter generation',
                    'Interview Q&A prediction',
                    'Salary negotiation scripts',
                    'Real profile data integration'
                ],
                'missing_features': [
                    {'id': 'cv_001', 'name': 'CV Comparison View', 'description': 'Side-by-side compare 2-3 CV versions for same job', 'effort': 'medium', 'impact': 'high', 'category': 'UX'},
                    {'id': 'cv_002', 'name': 'Version History', 'description': 'Track every change, revert to old versions', 'effort': 'low', 'impact': 'medium', 'category': 'Data'},
                    {'id': 'cv_003', 'name': 'Keyword Heatmap', 'description': 'Visual overlay showing matched keywords in job description', 'effort': 'medium', 'impact': 'high', 'category': 'Visualization'},
                    {'id': 'cv_004', 'name': 'Section Reordering', 'description': 'Drag-drop to reorder experience bullets', 'effort': 'low', 'impact': 'medium', 'category': 'UX'},
                    {'id': 'cv_005', 'name': 'Template Gallery', 'description': '10+ visual templates: HealthTech, FinTech, Academic', 'effort': 'high', 'impact': 'high', 'category': 'Design'},
                    {'id': 'cv_006', 'name': 'Reading Time Estimator', 'description': 'Show recruiter reading time: "Yours is 4 seconds"', 'effort': 'low', 'impact': 'medium', 'category': 'Analytics'},
                    {'id': 'cv_007', 'name': 'DOCX Export', 'description': 'Export to actual Word format, not just HTML', 'effort': 'medium', 'impact': 'high', 'category': 'Export'},
                    {'id': 'cv_008', 'name': 'CV Health Timeline', 'description': 'Track ATS scores over time with trends', 'effort': 'medium', 'impact': 'medium', 'category': 'Analytics'},
                    {'id': 'cv_009', 'name': 'Missing Skills Detector', 'description': '"Job needs Kubernetes - add to CV?"', 'effort': 'high', 'impact': 'high', 'category': 'AI'},
                    {'id': 'cv_010', 'name': 'Bullet Strength Analyzer', 'description': 'Score each bullet: Weak/Good/Strong', 'effort': 'medium', 'impact': 'high', 'category': 'AI'},
                ]
            },
            
            'job_tracker': {
                'name': 'Job Tracker',
                'icon': 'fa-tasks',
                'built_features': [
                    'Kanban pipeline board',
                    'Auto-scrape from job URLs',
                    'Company research aggregation',
                    'Interview question prep',
                    'Timeline view',
                    'Follow-up reminders',
                    'Status tracking'
                ],
                'missing_features': [
                    {'id': 'jt_001', 'name': 'Gantt Timeline View', 'description': 'Visual application timeline with dates', 'effort': 'medium', 'impact': 'medium', 'category': 'Visualization'},
                    {'id': 'jt_002', 'name': 'Interview Checklist', 'description': 'Per-job prep: research, questions, outfit', 'effort': 'low', 'impact': 'high', 'category': 'Productivity'},
                    {'id': 'jt_003', 'name': 'Salary Negotiation Log', 'description': 'Track offers, counter-offers, final numbers', 'effort': 'low', 'impact': 'high', 'category': 'Finance'},
                    {'id': 'jt_004', 'name': 'Source Effectiveness', 'description': '"LinkedIn: 20% interview rate, Indeed: 5%"', 'effort': 'medium', 'impact': 'high', 'category': 'Analytics'},
                    {'id': 'jt_005', 'name': 'Response Time Tracker', 'description': 'Average days to first response by company', 'effort': 'medium', 'impact': 'medium', 'category': 'Analytics'},
                    {'id': 'jt_006', 'name': 'Rejection Analytics', 'description': 'Log reasons, spot patterns in rejections', 'effort': 'low', 'impact': 'medium', 'category': 'Analytics'},
                    {'id': 'jt_007', 'name': 'Referral Tracker', 'description': 'Who referred you, did they get bonus?', 'effort': 'low', 'impact': 'medium', 'category': 'Network'},
                    {'id': 'jt_008', 'name': 'Job Description Diff', 'description': 'Compare 2 similar jobs side-by-side', 'effort': 'medium', 'impact': 'medium', 'category': 'UX'},
                    {'id': 'jt_009', 'name': 'Application Velocity', 'description': 'You\'re applying 3x faster than last month', 'effort': 'medium', 'impact': 'medium', 'category': 'Analytics'},
                    {'id': 'jt_010', 'name': 'Ghost Job Detector', 'description': 'Identify fake/reposted job listings', 'effort': 'high', 'impact': 'high', 'category': 'AI'},
                    {'id': 'jt_011', 'name': 'Offer Comparison Tool', 'description': 'Side-by-side benefits comparison', 'effort': 'medium', 'impact': 'high', 'category': 'Finance'},
                    {'id': 'jt_012', 'name': 'Competitor Job Alerts', 'description': '"Google just hired for similar role"', 'effort': 'high', 'impact': 'medium', 'category': 'Intelligence'},
                ]
            },
            
            'content_factory': {
                'name': 'Content Factory',
                'icon': 'fa-pen-fancy',
                'built_features': [
                    'LinkedIn post generation',
                    'Auto-scheduling',
                    'Optimal timing algorithm',
                    '30-day content calendar',
                    'Trending topic alerts',
                    'Engagement analytics tracking'
                ],
                'missing_features': [
                    {'id': 'cf_001', 'name': 'Quote Image Generator', 'description': 'Create branded quote images for posts', 'effort': 'medium', 'impact': 'high', 'category': 'Design'},
                    {'id': 'cf_002', 'name': 'Carousel Builder', 'description': '10-slide carousel structure generator', 'effort': 'medium', 'impact': 'high', 'category': 'Content'},
                    {'id': 'cf_003', 'name': 'Post Performance Simulator', 'description': '"This style gets 2x engagement"', 'effort': 'high', 'impact': 'medium', 'category': 'AI'},
                    {'id': 'cf_004', 'name': 'Content Recycling', 'description': 'Repurpose posts from 3 months ago', 'effort': 'low', 'impact': 'medium', 'category': 'Productivity'},
                    {'id': 'cf_005', 'name': 'Hook Generator', 'description': '50 attention-grabbing opening lines', 'effort': 'low', 'impact': 'high', 'category': 'Content'},
                    {'id': 'cf_006', 'name': 'Story Templates', 'description': '"Day in the life", "Behind the scenes"', 'effort': 'low', 'impact': 'medium', 'category': 'Content'},
                    {'id': 'cf_007', 'name': 'Comment Reply Bank', 'description': 'Pre-written responses to common comments', 'effort': 'low', 'impact': 'medium', 'category': 'Engagement'},
                    {'id': 'cf_008', 'name': 'Competitor Swipe File', 'description': 'Save and study best posts from others', 'effort': 'low', 'impact': 'medium', 'category': 'Research'},
                    {'id': 'cf_009', 'name': 'A/B Test Headlines', 'description': 'Test 3 versions, auto-pick winner', 'effort': 'high', 'impact': 'medium', 'category': 'Analytics'},
                    {'id': 'cf_010', 'name': 'Content Gap Filler', 'description': '"You haven\'t posted in 5 days - write this:"', 'effort': 'medium', 'impact': 'high', 'category': 'AI'},
                    {'id': 'cf_011', 'name': 'PDF Post Creator', 'description': 'Generate PDF documents for LinkedIn', 'effort': 'medium', 'impact': 'high', 'category': 'Export'},
                    {'id': 'cf_012', 'name': 'Hashtag Performance Tracker', 'description': 'Which hashtags drive most views?', 'effort': 'medium', 'impact': 'medium', 'category': 'Analytics'},
                ]
            },
            
            'network_mapper': {
                'name': 'Network Mapper',
                'icon': 'fa-network-wired',
                'built_features': [
                    'LinkedIn contact import',
                    'Warm intro pathfinding',
                    'AI conversation starters',
                    'Relationship scoring',
                    'News alerts for contacts'
                ],
                'missing_features': [
                    {'id': 'nm_001', 'name': 'Contact Heatmap', 'description': 'Visual: who haven\'t you contacted?', 'effort': 'medium', 'impact': 'high', 'category': 'Visualization'},
                    {'id': 'nm_002', 'name': 'Relationship Graph', 'description': 'Web visualization of all connections', 'effort': 'high', 'impact': 'medium', 'category': 'Visualization'},
                    {'id': 'nm_003', 'name': 'Meeting Notes', 'description': 'Notes per contact, searchable history', 'effort': 'low', 'impact': 'high', 'category': 'Productivity'},
                    {'id': 'nm_004', 'name': 'Follow-up Streak', 'description': '34 day streak contacting 1 person daily', 'effort': 'low', 'impact': 'medium', 'category': 'Gamification'},
                    {'id': 'nm_005', 'name': 'Contact Groups', 'description': 'Groups: HealthTech VPs, Recruiters, Peers', 'effort': 'low', 'impact': 'high', 'category': 'Organization'},
                    {'id': 'nm_006', 'name': 'Introduction Tracker', 'description': 'Who introduced whom, success rate', 'effort': 'medium', 'impact': 'medium', 'category': 'Analytics'},
                    {'id': 'nm_007', 'name': 'Gift Ideas Log', 'description': '"Sarah likes wine - noted for birthday"', 'effort': 'low', 'impact': 'low', 'category': 'CRM'},
                    {'id': 'nm_008', 'name': 'Conversation History', 'description': 'Full chat log per contact', 'effort': 'medium', 'impact': 'high', 'category': 'Data'},
                    {'id': 'nm_009', 'name': 'Network Value Score', 'description': 'Your network reaches 12,000 people', 'effort': 'medium', 'impact': 'medium', 'category': 'Analytics'},
                    {'id': 'nm_010', 'name': 'Cold Email Templates', 'description': '20 proven outreach templates', 'effort': 'low', 'impact': 'high', 'category': 'Content'},
                    {'id': 'nm_011', 'name': 'Birthday/Anniversary Alerts', 'description': 'Never miss important dates', 'effort': 'low', 'impact': 'medium', 'category': 'CRM'},
                    {'id': 'nm_012', 'name': 'Voice Memo Logging', 'description': 'Record post-call notes', 'effort': 'medium', 'impact': 'medium', 'category': 'Productivity'},
                ]
            },
            
            'analytics_dashboard': {
                'name': 'Analytics Dashboard',
                'icon': 'fa-chart-line',
                'built_features': [
                    'Predictive time-to-offer',
                    'Smart targets',
                    'Cohort analysis',
                    'Pipeline visualization',
                    'Benchmarking'
                ],
                'missing_features': [
                    {'id': 'ad_001', 'name': 'Weekly Report Email', 'description': 'Auto-generated Sunday night summary', 'effort': 'low', 'impact': 'high', 'category': 'Automation'},
                    {'id': 'ad_002', 'name': 'Goal Setting Dashboard', 'description': 'Monthly targets with progress tracking', 'effort': 'medium', 'impact': 'high', 'category': 'Productivity'},
                    {'id': 'ad_003', 'name': 'Burnout Detector', 'description': '"50 jobs in 3 days - time to rest"', 'effort': 'medium', 'impact': 'medium', 'category': 'Wellness'},
                    {'id': 'ad_004', 'name': 'Application Quality Score', 'description': 'Not just quantity - quality metric', 'effort': 'high', 'impact': 'high', 'category': 'AI'},
                    {'id': 'ad_005', 'name': 'Best Time to Apply', 'description': 'Tuesday 9am gets fastest responses', 'effort': 'medium', 'impact': 'high', 'category': 'Intelligence'},
                    {'id': 'ad_006', 'name': 'Sector Breakdown', 'description': 'Pie chart: HealthTech vs FinTech apps', 'effort': 'low', 'impact': 'medium', 'category': 'Visualization'},
                    {'id': 'ad_007', 'name': 'Geographic Heatmap', 'description': 'Where are you applying globally?', 'effort': 'medium', 'impact': 'medium', 'category': 'Visualization'},
                    {'id': 'ad_008', 'name': 'Response Time Leaderboard', 'description': 'Which companies respond fastest?', 'effort': 'medium', 'impact': 'medium', 'category': 'Intelligence'},
                    {'id': 'ad_009', 'name': 'Rejection Pattern Analysis', 'description': 'You\'re rejected after 3rd round usually', 'effort': 'high', 'impact': 'high', 'category': 'AI'},
                    {'id': 'ad_010', 'name': 'Peer Benchmarking', 'description': 'How do you compare to other candidates?', 'effort': 'high', 'impact': 'medium', 'category': 'Social'},
                ]
            }
        }
        
        # Add remaining tools with template
        remaining_tools = [
            'calendar_integration', 'notification_hub', 'mission_control',
            'auto_trigger', 'voice_transcription', 'expense_tracker',
            'bookmark_manager', 'search_aggregator', 'second_brain'
        ]
        
        for tool_id in remaining_tools:
            if tool_id not in catalog:
                catalog[tool_id] = {
                    'name': tool_id.replace('_', ' ').title(),
                    'icon': 'fa-cog',
                    'built_features': ['Core functionality'],
                    'missing_features': []
                }
        
        return catalog
    
    def get_all_features(self) -> Dict:
        """Get complete feature catalog"""
        return self.features
    
    def get_tool_features(self, tool_id: str) -> Dict:
        """Get features for specific tool"""
        return self.features.get(tool_id, {})
    
    def generate_more_features(self, tool_id: str) -> List[Dict]:
        """
        Generate additional missing features using AI logic
        """
        tool = self.features.get(tool_id, {})
        existing = tool.get('missing_features', [])
        
        # Feature generation patterns based on tool type
        generators = {
            'cv_optimizer': [
                {'name': 'PDF Accessibility Checker', 'description': 'Ensure PDF is screen-reader friendly', 'category': 'Accessibility'},
                {'name': 'LinkedIn Headline Optimizer', 'description': 'Sync CV with LinkedIn headline', 'category': 'Social'},
                {'name': 'Reference Manager', 'description': 'Track which references used for which job', 'category': 'CRM'},
                {'name': 'Portfolio Link Generator', 'description': 'Create simple portfolio website from CV', 'category': 'Web'},
            ],
            'job_tracker': [
                {'name': 'Application Tracker Export', 'description': 'Export all applications to Excel/CSV', 'category': 'Export'},
                {'name': 'Job Description Keyword Cloud', 'description': 'Visual word cloud of job requirements', 'category': 'Visualization'},
                {'name': 'Company News Digest', 'description': 'Weekly news about applied companies', 'category': 'Intelligence'},
                {'name': 'Application Timeline Sharing', 'description': 'Share progress with mentor/advisor', 'category': 'Social'},
            ],
            'content_factory': [
                {'name': 'Video Script Generator', 'description': 'Scripts for LinkedIn video posts', 'category': 'Video'},
                {'name': 'Meme Generator', 'description': 'Create industry-relevant memes', 'category': 'Design'},
                {'name': 'Poll Question Ideas', 'description': 'Engaging poll questions for audience', 'category': 'Engagement'},
                {'name': 'Newsletter Builder', 'description': 'Compile posts into weekly newsletter', 'category': 'Content'},
            ],
            'network_mapper': [
                {'name': 'LinkedIn Connection Message', 'description': 'Personalized connection request text', 'category': 'Content'},
                {'name': 'Networking Event Planner', 'description': 'Plan who to meet at upcoming events', 'category': 'Events'},
                {'name': 'Referral Request Templates', 'description': 'How to ask for referrals gracefully', 'category': 'Content'},
                {'name': 'Thank You Note Generator', 'description': 'Post-meeting thank you messages', 'category': 'Content'},
            ]
        }
        
        # Get generator for this tool or use generic
        new_features = generators.get(tool_id, [
            {'name': 'Dark Mode Toggle', 'description': 'Switch between light/dark themes', 'category': 'UX'},
            {'name': 'Keyboard Shortcuts', 'description': 'Power-user keyboard commands', 'category': 'UX'},
            {'name': 'Data Export', 'description': 'Export all data to JSON/CSV', 'category': 'Data'},
            {'name': 'Mobile Responsive View', 'description': 'Better mobile experience', 'category': 'Mobile'},
        ])
        
        # Add IDs and effort/impact
        start_idx = len(existing) + 1
        for i, feature in enumerate(new_features):
            feature['id'] = f"{tool_id[:2]}_{start_idx + i:03d}"
            feature['effort'] = 'medium'
            feature['impact'] = 'medium'
        
        # Add to catalog
        tool['missing_features'].extend(new_features)
        self._save_json(self.features_file, self.features)
        
        return new_features
    
    def add_to_roadmap(self, feature_ids: List[str]) -> List[Dict]:
        """Add selected features to build roadmap"""
        added = []
        
        for tool_id, tool_data in self.features.items():
            for feature in tool_data.get('missing_features', []):
                if feature['id'] in feature_ids:
                    roadmap_item = {
                        'id': feature['id'],
                        'tool': tool_data['name'],
                        'feature': feature['name'],
                        'description': feature['description'],
                        'added_at': datetime.now().isoformat(),
                        'status': 'pending',
                        'effort': feature['effort'],
                        'impact': feature['impact']
                    }
                    self.roadmap.append(roadmap_item)
                    added.append(roadmap_item)
        
        self._save_json(self.roadmap_file, self.roadmap)
        return added
    
    def mark_built(self, feature_id: str) -> bool:
        """Mark a feature as built"""
        # Update roadmap
        for item in self.roadmap:
            if item['id'] == feature_id:
                item['status'] = 'built'
                item['built_at'] = datetime.now().isoformat()
        
        # Move from missing to built in catalog
        for tool_id, tool_data in self.features.items():
            missing = tool_data.get('missing_features', [])
            built = tool_data.get('built_features', [])
            
            for i, feature in enumerate(missing):
                if feature['id'] == feature_id:
                    built.append(feature['name'])
                    missing.pop(i)
                    break
        
        self._save_json(self.roadmap_file, self.roadmap)
        self._save_json(self.features_file, self.features)
        return True
    
    def get_roadmap(self) -> List[Dict]:
        """Get current build roadmap"""
        return sorted(self.roadmap, key=lambda x: x.get('added_at', ''), reverse=True)
    
    def get_stats(self) -> Dict:
        """Get product management stats"""
        total_missing = sum(len(t.get('missing_features', [])) for t in self.features.values())
        total_built = sum(len(t.get('built_features', [])) for t in self.features.values())
        
        return {
            'tools_count': len(self.features),
            'total_features_built': total_built,
            'total_features_missing': total_missing,
            'roadmap_pending': len([r for r in self.roadmap if r.get('status') == 'pending']),
            'roadmap_built': len([r for r in self.roadmap if r.get('status') == 'built']),
            'high_impact_features': len([f for t in self.features.values() 
                                        for f in t.get('missing_features', []) 
                                        if f.get('impact') == 'high'])
        }

# Global instance
product_manager = ProductManager()
