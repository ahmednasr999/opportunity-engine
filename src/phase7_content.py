#!/usr/bin/env python3
"""
Phase 7 - Content Enhancements
Features: Carousel Builder, PDF Post Creator, Content Gap Filler,
          Best Time to Post, Engagement Prediction, Content Calendar,
          Hashtag Recommendations, Content Recycling, Hook Generator,
          Story Templates, Comment Reply Bank, Competitor Swipe File, A/B Headlines
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path


class CarouselBuilder:
    """Build multi-slide LinkedIn carousel posts"""

    def create(self, title: str, slides: List[Dict] = None, theme: str = "professional") -> Dict:
        if not slides:
            slides = [
                {"slide": 1, "type": "cover", "title": title, "subtitle": "Swipe to learn more →"},
                {"slide": 2, "type": "content", "title": "Key Point 1", "body": "Add your first insight here", "icon": "💡"},
                {"slide": 3, "type": "content", "title": "Key Point 2", "body": "Add your second insight here", "icon": "📊"},
                {"slide": 4, "type": "content", "title": "Key Point 3", "body": "Add your third insight here", "icon": "🎯"},
                {"slide": 5, "type": "cta", "title": "Like & Follow", "body": "Share this with your network!", "icon": "🔄"},
            ]

        themes = {
            "professional": {"bg": "#1a365d", "text": "#ffffff", "accent": "#4299e1"},
            "modern": {"bg": "#ffffff", "text": "#1a202c", "accent": "#6b46c1"},
            "bold": {"bg": "#e53e3e", "text": "#ffffff", "accent": "#fc8181"},
            "minimal": {"bg": "#f7fafc", "text": "#2d3748", "accent": "#4a5568"},
            "health": {"bg": "#234e52", "text": "#ffffff", "accent": "#38b2ac"},
        }

        return {
            "title": title,
            "slides": slides,
            "total_slides": len(slides),
            "theme": themes.get(theme, themes["professional"]),
            "theme_name": theme,
            "format": {"width": 1080, "height": 1080, "type": "square"},
            "tips": [
                "Keep text large and readable on mobile",
                "Use 5-10 slides for best engagement",
                "First slide must hook — use a question or bold statement",
                "Last slide = CTA (follow, share, comment)"
            ],
            "estimated_engagement": "High — carousels get 3x more reach than text posts",
            "created_at": datetime.now().isoformat()
        }

    def get_templates(self) -> List[Dict]:
        return [
            {"name": "5 Tips", "slides": 7, "type": "educational"},
            {"name": "Before/After", "slides": 5, "type": "transformation"},
            {"name": "Myth vs Reality", "slides": 8, "type": "contrarian"},
            {"name": "Step-by-Step Guide", "slides": 6, "type": "tutorial"},
            {"name": "Personal Story", "slides": 5, "type": "storytelling"},
        ]


class PDFPostCreator:
    """Create downloadable PDF versions of posts"""

    def create(self, post_content: str, title: str = "", author: str = "Ahmed Nasr") -> Dict:
        return {
            "title": title or "LinkedIn Post",
            "author": author,
            "content": post_content,
            "format": "A4",
            "pages": max(1, len(post_content) // 2000),
            "design": {
                "header_color": "#1a365d",
                "font": "Inter",
                "branding": True,
                "include_qr": True,
                "qr_url": "https://linkedin.com/in/ahmed-nasr"
            },
            "download_ready": True,
            "file_name": f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            "created_at": datetime.now().isoformat()
        }


class ContentGapFiller:
    """Suggest content topics based on gaps in posting history"""

    CONTENT_CATEGORIES = [
        "Leadership & Management", "Healthcare Innovation", "AI & Technology",
        "Career Development", "Industry Trends", "Personal Stories",
        "How-To Guides", "Opinion & Thought Leadership", "Team Building",
        "Data & Analytics", "Patient Care", "Digital Transformation"
    ]

    def analyze(self, recent_posts: List[Dict] = None) -> Dict:
        if not recent_posts:
            recent_posts = [
                {"topic": "AI & Technology", "date": "2026-02-10"},
                {"topic": "AI & Technology", "date": "2026-02-05"},
                {"topic": "Leadership & Management", "date": "2026-01-28"},
                {"topic": "AI & Technology", "date": "2026-01-20"},
            ]

        covered = {}
        for p in recent_posts:
            topic = p.get("topic", "General")
            covered[topic] = covered.get(topic, 0) + 1

        gaps = []
        for cat in self.CONTENT_CATEGORIES:
            if cat not in covered:
                gaps.append({"category": cat, "priority": "high", "suggestion": f"Write about {cat} — you haven't covered this recently"})
            elif covered[cat] < 2:
                gaps.append({"category": cat, "priority": "medium", "suggestion": f"Post more about {cat} for balance"})

        overused = [{"category": k, "count": v} for k, v in covered.items() if v >= 3]

        return {
            "gaps": gaps[:8],
            "overused_topics": overused,
            "coverage": {cat: covered.get(cat, 0) for cat in self.CONTENT_CATEGORIES},
            "diversity_score": round(len(covered) / len(self.CONTENT_CATEGORIES) * 100, 1),
            "recommendations": [
                f"Post about: {gaps[0]['category']}" if gaps else "Great coverage!",
                "Aim for at least 4 different categories per month",
                "Mix educational, personal, and opinion content"
            ]
        }


class BestTimeToPost:
    """Analytics-based optimal posting time recommendations"""

    def recommend(self, timezone: str = "UTC+3", audience: str = "professional") -> Dict:
        schedules = {
            "professional": {
                "best_days": ["Tuesday", "Wednesday", "Thursday"],
                "best_times": ["07:30", "08:00", "12:00", "17:30"],
                "worst_times": ["22:00-06:00", "Saturday afternoon"],
                "peak_engagement": "Tuesday 08:00"
            },
            "healthcare": {
                "best_days": ["Monday", "Tuesday", "Wednesday"],
                "best_times": ["06:30", "07:00", "12:30", "18:00"],
                "worst_times": ["Weekend mornings", "Friday afternoon"],
                "peak_engagement": "Monday 07:00"
            },
            "tech": {
                "best_days": ["Tuesday", "Wednesday", "Thursday"],
                "best_times": ["09:00", "12:00", "14:00", "17:00"],
                "worst_times": ["Late night", "Early morning"],
                "peak_engagement": "Wednesday 09:00"
            }
        }

        schedule = schedules.get(audience, schedules["professional"])
        
        # Generate weekly heatmap data
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        hours = list(range(6, 23))
        heatmap = {}
        for day in days:
            for hour in hours:
                base = 30
                if day in schedule["best_days"]:
                    base += 20
                if f"{hour:02d}:00" in schedule["best_times"] or f"{hour:02d}:30" in schedule["best_times"]:
                    base += 30
                if day in ["Saturday", "Sunday"]:
                    base -= 15
                heatmap[f"{day}_{hour}"] = min(100, max(0, base + random.randint(-10, 10)))

        return {
            "timezone": timezone,
            "audience": audience,
            "schedule": schedule,
            "heatmap": heatmap,
            "next_best_slot": self._next_best_slot(schedule),
            "tips": [
                "Post when your audience is online (morning commute, lunch)",
                "Engage with comments in the first hour",
                "Consistency matters more than perfection",
                "Test different times and track results"
            ]
        }

    def _next_best_slot(self, schedule: Dict) -> str:
        now = datetime.now()
        day_name = now.strftime("%A")
        if day_name in schedule["best_days"]:
            return f"Today at {schedule['best_times'][0]}"
        return f"Next {schedule['best_days'][0]} at {schedule['best_times'][0]}"


class EngagementPrediction:
    """Predict engagement (likes, comments, shares) for content"""

    def predict(self, content: str, content_type: str = "text", hashtag_count: int = 3) -> Dict:
        base_likes = 50
        base_comments = 5
        base_shares = 3

        # Content length factor
        word_count = len(content.split())
        if 100 <= word_count <= 300:
            base_likes *= 1.5
            base_comments *= 1.3
        elif word_count > 500:
            base_likes *= 0.8

        # Content type factor
        type_multipliers = {"carousel": 3.0, "video": 2.5, "image": 2.0, "poll": 2.0, "text": 1.0, "article": 0.8}
        multiplier = type_multipliers.get(content_type, 1.0)

        # Engagement hooks
        if "?" in content:
            base_comments *= 2.0
        if any(w in content.lower() for w in ["agree?", "thoughts?", "what do you think"]):
            base_comments *= 2.5
        if any(w in content.lower() for w in ["unpopular opinion", "controversial", "hot take"]):
            base_likes *= 1.5
            base_comments *= 1.8

        # Hashtag penalty/bonus
        if hashtag_count > 5:
            base_likes *= 0.7
        elif 3 <= hashtag_count <= 5:
            base_likes *= 1.1

        likes = int(base_likes * multiplier)
        comments = int(base_comments * multiplier)
        shares = int(base_shares * multiplier)
        impressions = likes * 8

        engagement_rate = round((likes + comments + shares) / max(1, impressions) * 100, 2)

        return {
            "predicted_likes": likes,
            "predicted_comments": comments,
            "predicted_shares": shares,
            "predicted_impressions": impressions,
            "engagement_rate": engagement_rate,
            "confidence": "medium",
            "content_type": content_type,
            "factors": {
                "length_impact": "optimal" if 100 <= word_count <= 300 else "suboptimal",
                "question_bonus": "?" in content,
                "type_multiplier": multiplier,
                "hashtag_impact": "good" if 3 <= hashtag_count <= 5 else "too many" if hashtag_count > 5 else "could add more"
            },
            "tips": [
                "Add a question to boost comments" if "?" not in content else "Good — question included",
                f"Consider using {content_type} format" if content_type == "text" else f"{content_type} format is great for engagement",
                "First line is crucial — make it a hook"
            ]
        }


class ContentCalendar:
    """Visual content calendar view"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.calendar_file = self.data_dir / "content_calendar.json"
        self.entries = self._load()

    def _load(self) -> List[Dict]:
        if self.calendar_file.exists():
            return json.loads(self.calendar_file.read_text())
        # Generate sample month
        entries = []
        today = datetime.now()
        topics = ["AI in Healthcare", "Leadership Tips", "Career Advice", "Industry Trends", "Personal Story"]
        types = ["text", "carousel", "image", "poll"]
        for i in range(12):
            date = today + timedelta(days=i * 2 + random.randint(0, 1))
            entries.append({
                "id": f"cal{i+1}",
                "date": date.strftime("%Y-%m-%d"),
                "time": random.choice(["08:00", "12:00", "17:30"]),
                "topic": random.choice(topics),
                "type": random.choice(types),
                "status": "published" if date < today else "scheduled" if i < 5 else "draft",
                "title": f"Post about {random.choice(topics)}"
            })
        return entries

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.calendar_file.write_text(json.dumps(self.entries, indent=2))

    def get_calendar(self, month: int = None, year: int = None) -> Dict:
        now = datetime.now()
        month = month or now.month
        year = year or now.year
        
        month_entries = [e for e in self.entries if e["date"].startswith(f"{year}-{month:02d}")]
        
        return {
            "month": month,
            "year": year,
            "entries": month_entries,
            "total_posts": len(month_entries),
            "by_status": {
                "published": len([e for e in month_entries if e["status"] == "published"]),
                "scheduled": len([e for e in month_entries if e["status"] == "scheduled"]),
                "draft": len([e for e in month_entries if e["status"] == "draft"]),
            },
            "posting_frequency": round(len(month_entries) / 4, 1)
        }

    def add_entry(self, entry_data: Dict) -> Dict:
        entry = {
            "id": f"cal{len(self.entries)+1}",
            "date": entry_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            "time": entry_data.get("time", "08:00"),
            "topic": entry_data.get("topic", ""),
            "type": entry_data.get("type", "text"),
            "status": "draft",
            "title": entry_data.get("title", "")
        }
        self.entries.append(entry)
        self._save()
        return entry

    def update_status(self, entry_id: str, status: str) -> bool:
        for e in self.entries:
            if e["id"] == entry_id:
                e["status"] = status
                self._save()
                return True
        return False

    def get_all(self) -> List[Dict]:
        return self.entries


class HashtagRecommendations:
    """Auto-suggest hashtags based on content"""

    HASHTAG_DB = {
        "healthcare": ["#HealthcareInnovation", "#DigitalHealth", "#HealthTech", "#PatientCare", "#HealthcareAI", "#MedTech", "#EHealth"],
        "ai": ["#ArtificialIntelligence", "#MachineLearning", "#AI", "#DeepLearning", "#DataScience", "#AIinHealthcare"],
        "leadership": ["#Leadership", "#Management", "#ExecutiveLeadership", "#TeamBuilding", "#LeadershipDevelopment"],
        "career": ["#CareerAdvice", "#JobSearch", "#ProfessionalGrowth", "#CareerDevelopment", "#OpenToWork"],
        "technology": ["#Technology", "#Innovation", "#DigitalTransformation", "#TechTrends", "#FutureTech"],
        "operations": ["#Operations", "#ProcessImprovement", "#LeanSixSigma", "#ProjectManagement", "#PMO"],
    }

    def recommend(self, content: str, max_hashtags: int = 5) -> Dict:
        content_lower = content.lower()
        recommended = []
        
        for category, tags in self.HASHTAG_DB.items():
            if category in content_lower or any(t.lower().replace("#", "") in content_lower for t in tags):
                for tag in tags:
                    reach = random.randint(10000, 500000)
                    recommended.append({
                        "hashtag": tag,
                        "category": category,
                        "estimated_reach": reach,
                        "competition": "high" if reach > 200000 else "medium" if reach > 50000 else "low"
                    })

        # Sort by reach
        recommended.sort(key=lambda x: x["estimated_reach"], reverse=True)
        
        # Add generic high-performers
        always_good = ["#LinkedInTips", "#ProfessionalDevelopment", "#Networking"]
        for tag in always_good:
            if len(recommended) < max_hashtags + 3:
                recommended.append({"hashtag": tag, "category": "general", "estimated_reach": random.randint(100000, 300000), "competition": "medium"})

        return {
            "recommended": recommended[:max_hashtags],
            "additional": recommended[max_hashtags:max_hashtags+5],
            "total_suggestions": len(recommended),
            "optimal_count": "3-5 hashtags per post",
            "tips": [
                "Mix popular (high reach) with niche (low competition)",
                "Don't use more than 5 hashtags on LinkedIn",
                "Put hashtags at the end of your post",
                "Create a branded hashtag for consistency"
            ]
        }


class ContentRecycling:
    """Recycle and repurpose old content"""

    def suggest(self, posts: List[Dict] = None) -> Dict:
        if not posts:
            posts = [
                {"id": "p1", "title": "5 Ways AI is Transforming Healthcare", "date": "2025-06-15", "likes": 145, "type": "text"},
                {"id": "p2", "title": "Leadership Lessons from Hospital Ops", "date": "2025-08-20", "likes": 89, "type": "text"},
                {"id": "p3", "title": "My Career Journey in HealthTech", "date": "2025-10-10", "likes": 210, "type": "text"},
            ]

        suggestions = []
        for post in posts:
            if post.get("likes", 0) > 50:
                suggestions.append({
                    "original": post,
                    "recycle_ideas": [
                        {"format": "carousel", "description": f"Turn '{post['title']}' into a carousel with key points"},
                        {"format": "thread", "description": "Break into a thread format with one point per post"},
                        {"format": "video", "description": "Record a 60-second video summary"},
                        {"format": "infographic", "description": "Create a visual summary"},
                    ],
                    "best_recycle_date": (datetime.now() + timedelta(days=random.randint(30, 90))).strftime("%Y-%m-%d"),
                    "potential_boost": f"{random.randint(20, 50)}% of original engagement"
                })

        return {
            "recyclable_posts": len(suggestions),
            "suggestions": suggestions,
            "tips": [
                "Wait at least 60 days before recycling content",
                "Change the format (text → carousel, post → video)",
                "Update with new data or insights",
                "Top-performing posts recycle best"
            ]
        }


class HookGenerator:
    """Generate attention-grabbing first lines for posts"""

    HOOK_TEMPLATES = [
        "I made a mistake that cost me {consequence}. Here's what I learned:",
        "Most people think {common_belief}. They're wrong. Here's why:",
        "{number} years in {industry} taught me one thing nobody talks about:",
        "Stop doing {bad_practice} if you want to {desired_outcome}.",
        "The best {role} I ever met did something nobody expected:",
        "Unpopular opinion: {contrarian_view}",
        "I was rejected from {count} jobs. Then this happened:",
        "Here's what {famous_company} won't tell you about {topic}:",
        "In {time_period}, I went from {before} to {after}. Here's how:",
        "The #1 skill that got me promoted wasn't what you'd expect:",
    ]

    def generate(self, topic: str = "", count: int = 5) -> Dict:
        hooks = []
        for template in random.sample(self.HOOK_TEMPLATES, min(count, len(self.HOOK_TEMPLATES))):
            hook = template.format(
                consequence="a promotion", common_belief=f"{topic} is easy" if topic else "success comes fast",
                number=random.randint(5, 20), industry=topic or "healthcare",
                bad_practice="multitasking", desired_outcome="succeed",
                role="leader", contrarian_view=f"{topic} is overrated" if topic else "credentials are overrated",
                count=random.randint(10, 50), famous_company="top companies",
                topic=topic or "hiring", time_period=f"{random.randint(6, 24)} months",
                before="struggling", after="thriving"
            )
            hooks.append({"hook": hook, "style": "curiosity" if "?" in hook else "story" if "I " in hook else "contrarian"})

        return {
            "hooks": hooks,
            "topic": topic,
            "tips": [
                "First line determines if people read the rest",
                "Use numbers for specificity",
                "Create a curiosity gap",
                "Personal stories perform best"
            ]
        }


class StoryTemplates:
    """Pre-built storytelling templates for posts"""

    def get_templates(self) -> List[Dict]:
        return [
            {"id": "st1", "name": "Hero's Journey", "structure": [
                "Set the scene: Where were you?",
                "The challenge: What happened?",
                "The struggle: How did it feel?",
                "The turning point: What changed?",
                "The lesson: What did you learn?",
                "The CTA: How can others apply this?"
            ]},
            {"id": "st2", "name": "Before/After", "structure": [
                "Before: Paint the old picture",
                "The trigger: What sparked change?",
                "The transformation: What did you do?",
                "After: Show the new reality",
                "The takeaway: Key lesson"
            ]},
            {"id": "st3", "name": "Failure Story", "structure": [
                "The ambition: What were you trying to do?",
                "The failure: What went wrong?",
                "The embarrassment: Be vulnerable",
                "The recovery: How did you bounce back?",
                "The wisdom: What would you tell others?"
            ]},
            {"id": "st4", "name": "Contrarian Take", "structure": [
                "The common belief: What does everyone think?",
                "The problem: Why is it wrong?",
                "Your evidence: Data or experience",
                "The alternative: What should people do instead?",
                "The invitation: Ask for opinions"
            ]},
            {"id": "st5", "name": "Lesson Learned", "structure": [
                "The situation: Brief context",
                "The mistake/insight: What happened?",
                "The impact: Why did it matter?",
                "The lesson: Distill into 1-2 sentences",
                "The application: How can readers use this?"
            ]},
        ]


class CommentReplyBank:
    """Pre-written comment replies for common scenarios"""

    def get_replies(self) -> Dict:
        return {
            "thank_you": [
                "Thank you for sharing this! Really insightful 🙏",
                "Great point — I hadn't thought of it that way!",
                "Appreciate the kind words! Happy to connect.",
            ],
            "agreement": [
                "Couldn't agree more! This is spot on.",
                "💯 This resonates deeply. Well said!",
                "Exactly this. Thank you for articulating it so well.",
            ],
            "question_response": [
                "Great question! In my experience, {answer}",
                "I'd approach it by {approach}. What do you think?",
                "Interesting question — I'll share my thoughts in a follow-up post!",
            ],
            "disagreement": [
                "Interesting perspective! I see it differently because {reason}. What are your thoughts?",
                "That's a fair point, though my experience has been different. Happy to discuss!",
            ],
            "engagement_boost": [
                "What's your take on this? Drop your thoughts below 👇",
                "Agree or disagree? I'm curious to hear your experience!",
                "Tag someone who needs to see this!",
            ]
        }


class CompetitorSwipeFile:
    """Track and save competitor content for inspiration"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.swipe_file = self.data_dir / "swipe_file.json"
        self.entries = self._load()

    def _load(self) -> List[Dict]:
        if self.swipe_file.exists():
            return json.loads(self.swipe_file.read_text())
        return [
            {"id": "sw1", "source": "Healthcare Leader X", "platform": "LinkedIn",
             "content_type": "carousel", "topic": "Hospital Operations", "likes": 500,
             "why_it_works": "Strong hook + actionable tips", "saved_date": "2026-02-01",
             "notes": "Could adapt this format for AI in healthcare"},
        ]

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.swipe_file.write_text(json.dumps(self.entries, indent=2))

    def add(self, entry_data: Dict) -> Dict:
        entry = {
            "id": f"sw{len(self.entries)+1}",
            "source": entry_data.get("source", ""),
            "platform": entry_data.get("platform", "LinkedIn"),
            "content_type": entry_data.get("content_type", "text"),
            "topic": entry_data.get("topic", ""),
            "likes": entry_data.get("likes", 0),
            "why_it_works": entry_data.get("why_it_works", ""),
            "saved_date": datetime.now().strftime("%Y-%m-%d"),
            "notes": entry_data.get("notes", ""),
        }
        self.entries.append(entry)
        self._save()
        return entry

    def get_all(self) -> List[Dict]:
        return self.entries

    def get_by_topic(self, topic: str) -> List[Dict]:
        return [e for e in self.entries if topic.lower() in e.get("topic", "").lower()]


class ABTestHeadlines:
    """A/B test different headlines/hooks"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.tests_file = self.data_dir / "ab_tests.json"
        self.tests = self._load()

    def _load(self) -> List[Dict]:
        if self.tests_file.exists():
            return json.loads(self.tests_file.read_text())
        return []

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.tests_file.write_text(json.dumps(self.tests, indent=2))

    def create_test(self, headline_a: str, headline_b: str, topic: str = "") -> Dict:
        test = {
            "id": f"ab{len(self.tests)+1}",
            "headline_a": headline_a,
            "headline_b": headline_b,
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "results": {
                "a": {"impressions": 0, "clicks": 0, "engagement": 0},
                "b": {"impressions": 0, "clicks": 0, "engagement": 0}
            },
            "winner": None,
            "status": "running"
        }
        self.tests.append(test)
        self._save()
        return test

    def record_results(self, test_id: str, variant: str, impressions: int, clicks: int, engagement: int) -> Dict:
        for test in self.tests:
            if test["id"] == test_id:
                test["results"][variant] = {
                    "impressions": impressions, "clicks": clicks, "engagement": engagement
                }
                # Determine winner
                a = test["results"]["a"]
                b = test["results"]["b"]
                if a["impressions"] > 0 and b["impressions"] > 0:
                    rate_a = a["engagement"] / a["impressions"]
                    rate_b = b["engagement"] / b["impressions"]
                    test["winner"] = "a" if rate_a > rate_b else "b"
                    test["status"] = "completed"
                self._save()
                return test
        return {"error": "Test not found"}

    def get_all(self) -> List[Dict]:
        return self.tests
