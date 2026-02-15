#!/usr/bin/env python3
"""
Content Factory - Generate LinkedIn posts and newsletters
Optimized for Ahmed Nasr's HealthTech AI positioning
"""

import json
import random
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ContentTemplate:
    """A content template with variables"""
    name: str
    category: str  # linkedin, newsletter, thought_leadership
    template: str
    variables: List[str]
    hashtags: List[str]
    tone: str  # professional, conversational, provocative


class ContentFactory:
    """Generate content for LinkedIn and newsletters"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.topics = self._load_topics()
    
    def _load_templates(self) -> List[ContentTemplate]:
        """Load content templates"""
        return [
            # LinkedIn Templates - HealthTech Focus
            ContentTemplate(
                name="healthtech_insight",
                category="linkedin",
                template="""{hook}

{insight}

{key_point_1}
{key_point_2}
{key_point_3}

{closing}

What are you seeing in {topic_area}?""",
                variables=["hook", "insight", "key_point_1", "key_point_2", "key_point_3", "closing", "topic_area"],
                hashtags=["HealthTech", "AI", "DigitalTransformation", "Healthcare", "Innovation"],
                tone="professional"
            ),
            
            ContentTemplate(
                name="lessons_learned",
                category="linkedin",
                template="""After {time_period} in {field}, here's what I wish I knew sooner:

1️⃣ {lesson_1}

2️⃣ {lesson_2}

3️⃣ {lesson_3}

{closing}

What's the biggest lesson you've learned in your career?""",
                variables=["time_period", "field", "lesson_1", "lesson_2", "lesson_3", "closing"],
                hashtags=["Leadership", "CareerAdvice", "HealthTech", "Mentorship"],
                tone="conversational"
            ),
            
            ContentTemplate(
                name="industry_trend",
                category="linkedin",
                template="""{trend_statement}

📊 {statistic}

🔍 {analysis}

💡 {implication}

{closing}

Are you preparing for this shift?""",
                variables=["trend_statement", "statistic", "analysis", "implication", "closing"],
                hashtags=["HealthTech", "AI", "FutureOfWork", "DigitalHealth"],
                tone="professional"
            ),
            
            ContentTemplate(
                name="behind_the_scenes",
                category="linkedin",
                template="""A peek behind the curtain at {company}:

{scenario}

{challenge}

{solution}

{result}

{closing}

Transparency builds trust. What do you wish more leaders shared?""",
                variables=["company", "scenario", "challenge", "solution", "result", "closing"],
                hashtags=["Leadership", "HealthTech", "Operations", "Transparency"],
                tone="conversational"
            ),
            
            ContentTemplate(
                name="contrarian_take",
                category="linkedin",
                template="""Unpopular opinion: {opinion}

Here's why:

{argument_1}

{argument_2}

{argument_3}

{nuance}

Agree or disagree? Tell me why. 👇""",
                variables=["opinion", "argument_1", "argument_2", "argument_3", "nuance"],
                hashtags=["HealthTech", "ThoughtLeadership", "DigitalTransformation"],
                tone="provocative"
            ),
            
            # Newsletter Templates
            ContentTemplate(
                name="weekly_roundup",
                category="newsletter",
                template="""# {title}

**{date}** | {author}

---

## This Week in {topic}

### 1. {headline_1}
{summary_1}

**Why it matters:** {implication_1}

---

### 2. {headline_2}
{summary_2}

**Why it matters:** {implication_2}

---

### 3. {headline_3}
{summary_3}

**Why it matters:** {implication_3}

---

## 💡 My Take

{personal_insight}

---

## 📊 Data Point of the Week

{data_point}

---

*Thanks for reading. Forward to a colleague who needs to see this.*

{author_signature}""",
                variables=["title", "date", "author", "topic", "headline_1", "summary_1", "implication_1",
                          "headline_2", "summary_2", "implication_2", "headline_3", "summary_3", "implication_3",
                          "personal_insight", "data_point", "author_signature"],
                hashtags=[],
                tone="professional"
            ),
            
            ContentTemplate(
                name="deep_dive",
                category="newsletter",
                template="""# {title}

**The Future of {topic}**

{opening_hook}

## The Current State

{current_state}

## What's Changing

{change_1}

{change_2}

{change_3}

## What This Means for {audience}

{implication}

## Action Items

✅ {action_1}

✅ {action_2}

✅ {action_3}

---

{closing}

{author_signature}""",
                variables=["title", "topic", "opening_hook", "current_state", "change_1", "change_2", "change_3",
                          "audience", "implication", "action_1", "action_2", "action_3", "closing", "author_signature"],
                hashtags=[],
                tone="professional"
            )
        ]
        
        # HOOK GENERATOR - PHASE 1 FEATURE - Initialize in __init__
        self.hook_templates = []
        self.hook_variables = {}
        self._init_hook_generator()
    
    def _init_hook_generator(self):
        """Initialize hook generator templates"""
        self.hook_templates = [
            {"type": "question", "template": "What if I told you {surprising_statement}?", "engagement": "high"},
            {"type": "question", "template": "What does {industry} look like in 2030? Here's my take:", "engagement": "high"},
            {"type": "question", "template": "Why do {percentage}% of {industry} projects fail? {years} years later, I finally understand.", "engagement": "high"},
            {"type": "question", "template": "The biggest mistake I see in {role}s? It's not what you think.", "engagement": "high"},
            {"type": "question", "template": "How do you {common_task}? Most people do it wrong.", "engagement": "medium"},
            {"type": "stat", "template": "{stat}% of {audience} don't know this about {topic}. You probably don't either.", "engagement": "high"},
            {"type": "stat", "template": "I analyzed {number} {industry} leaders. Here's what the top {percentage}% have in common:", "engagement": "high"},
            {"type": "stat", "template": "{years} ago, I made a ${loss} mistake. Here's what I'd do differently:", "engagement": "high"},
            {"type": "story", "template": "I almost quit {industry} when {event}. I'm glad I didn't.", "engagement": "high"},
            {"type": "story", "template": "The best career advice I ever got? From a {role} at {company}.", "engagement": "medium"},
            {"type": "story", "template": "After {years} years in {industry}, here's what actually matters:", "engagement": "high"},
            {"type": "contrarian", "template": "Unpopular opinion: {contrarian_statement}", "engagement": "high"},
            {"type": "contrarian", "template": "Everyone says {common_belief}. They're wrong. Here's why:", "engagement": "high"},
            {"type": "contrarian", "template": "Stop doing {common_mistake}. Instead, do this:", "engagement": "medium"},
            {"type": "list", "template": "{number} things I wish I knew before {milestone}:", "engagement": "high"},
            {"type": "list", "template": "{number} signs you're ready for {next_step}:", "engagement": "medium"},
            {"type": "list", "template": "The {number} best {industry} strategies I've seen in {years} years:", "engagement": "high"},
            {"type": "howto", "template": "How to {desired_outcome} in {timeframe}:", "engagement": "high"},
            {"type": "howto", "template": "A step-by-step guide to {common_goal}:", "engagement": "high"},
            {"type": "problem", "template": "If you're struggling with {problem}, you're not alone. Here's the fix:", "engagement": "high"},
            {"type": "problem", "template": "The real reason you can't {desired_ability}? It's not what you think.", "engagement": "medium"},
        ]
        
        self.hook_variables = {
            "surprising_statement": ["most hospitals are sitting on data gold mines but can't extract value", "the biggest barrier to HealthTech isn't technology - it's culture"],
            "industry": ["HealthTech", "healthcare", "digital transformation", "AI in healthcare"],
            "percentage": ["70", "80", "90", "50"],
            "topic": ["leadership", "digital transformation", "AI adoption", "change management"],
            "role": ["CTO", "VP", "PM", "manager", "leader"],
            "company": ["Google", "Microsoft", "Amazon", "a startup", "a Fortune 500"],
            "common_task": ["interview candidates", "build teams", "prioritize projects", "handle conflict"],
            "audience": ["founders", "engineers", "healthcare leaders", "recruiters"],
            "stat": ["80", "90", "70", "60"],
            "number": ["10", "5", "7", "3"],
            "years": ["5", "10", "15", "20"],
            "event": ["my startup failed", "I got fired", "I almost gave up"],
            "milestone": ["becoming a VP", "starting my own company", "moving to leadership"],
            "common_belief": ["you need more experience to advance", "networking is the key", "it's all about who you know"],
            "common_mistake": ["sending cold emails", "networking without strategy", "applying to jobs blindly"],
            "next_step": ["your next promotion", "leadership role", "bigger responsibilities"],
            "desired_outcome": ["land your dream job", "negotiate a higher salary", "build a powerful network"],
            "timeframe": ["30 days", "90 days", "6 months"],
            "common_goal": ["networking", "job search", "salary negotiation"],
            "problem": ["getting interviews", "building relationships", "staying motivated"],
            "desired_ability": ["network effectively", "get referrals", "close opportunities"],
            "loss": ["100K", "500K", "1M"],
            "contrarian_statement": ["AI won't replace healthcare workers - it will replace those who don't adapt", "the best hire is rarely the most experienced candidate", "working harder is the worst career advice"]
        }
    
    def _load_topics(self) -> Dict:
        """Load content topics"""
        return {
            "healthtech_ai": {
                "hooks": [
                    "AI in healthcare isn't about replacing doctors—it's about amplifying their impact.",
                    "I just watched an AI system reduce hospital readmissions by 30%. Here's how:",
                    "The biggest barrier to HealthTech adoption isn't technology. It's change management.",
                    "What if I told you the most expensive part of healthcare isn't medicine?",
                    "Hospitals are sitting on gold mines of data. Most don't know how to extract value."
                ],
                "insights": [
                    "After implementing AI automation across 15+ hospitals, I've noticed a pattern:\n\nThe organizations that succeed don't have the best technology.\n\nThey have the best change management.",
                    "Healthcare AI adoption follows a predictable curve:\n\nInnovators (5%) → Early Adopters (15%) → Early Majority (35%) → Late Majority (35%) → Laggards (10%)\n\nWe're currently moving from Early Adopters to Early Majority. This is where scale happens.",
                    "The ROI on HealthTech isn't just financial:\n\n• Reduced physician burnout\n• Better patient outcomes\n• Faster diagnosis\n• Fewer errors\n• Happier staff\n\nMeasure all of it."
                ],
                "lessons": [
                    "Start with clinical champions, not technology.\n\nFind the doctors who stay up late reading about AI. They'll drag the organization forward.",
                    "Integration beats innovation.\n\nA mediocre system that works with existing workflows beats a brilliant system that requires disruption.",
                    "Data quality > Data quantity.\n\nClean data from 100 patients beats messy data from 100,000."
                ],
                "trends": [
                    "AI-powered clinical decision support will be standard of care by 2027.",
                    "Remote patient monitoring is shifting from reactive to predictive.",
                    "The line between 'digital health' and 'healthcare' is disappearing."
                ],
                "statistics": [
                    "The HealthTech market in MENA is projected to reach $10B by 2027.",
                    "AI adoption in healthcare grew 47% year-over-year in 2025.",
                    "Hospitals using AI report 35% reduction in administrative costs."
                ]
            },
            "digital_transformation": {
                "hooks": [
                    "Digital transformation fails 70% of the time. Here's what the 30% do differently:",
                    "I spent 20 years on digital transformation. The technology was never the hard part.",
                    "Your 'digital strategy' is useless if it ignores the humans who have to execute it."
                ],
                "insights": [
                    "Digital transformation isn't about technology. It's about reimagining how work gets done.",
                    "The organizations that succeed treat digital transformation as a continuous journey, not a destination."
                ],
                "lessons": [
                    "Culture eats strategy for breakfast. Process eats technology for lunch.",
                    "The best technology is the one people actually use.",
                    "Start small, prove value, then scale. Don't boil the ocean."
                ]
            },
            "leadership": {
                "hooks": [
                    "The best leaders I know don't have all the answers. They ask better questions.",
                    "Managing a PMO taught me that alignment beats talent. Every time.",
                    "Your team doesn't need a hero. They need clarity."
                ],
                "insights": [
                    "Leadership in 2026 looks different than 2016:\n\n• Decisions happen faster\n• Information flows openly\n• Authority is earned, not given\n• Results matter more than presence",
                    "The best teams I've built had one thing in common:\n\nPsychological safety. People could disagree without fear."
                ],
                "lessons": [
                    "Hire for attitude, train for skill. You can't teach curiosity.",
                    "Your job as a leader is to remove obstacles, not create them.",
                    "Delegate outcomes, not tasks. Give people ownership."
                ]
            },
            "fintech_bridge": {
                "hooks": [
                    "What FinTech taught me about HealthTech:",
                    "Healthcare is 10 years behind banking in digital maturity. Here's the opportunity:",
                    "The same patterns that revolutionized payments are coming to healthcare."
                ],
                "insights": [
                    "FinTech solved 'how do we move money faster?' HealthTech needs to solve 'how do we deliver care better?'",
                    "The patient experience gap in healthcare is what banking looked like before mobile apps."
                ],
                "lessons": [
                    "Regulatory complexity isn't an excuse. FinTech proved you can innovate in regulated industries.",
                    "User experience matters in healthcare too. Patients are consumers.",
                    "Data interoperability is the foundation. Everything else builds on it."
                ]
            }
        }
    
    def generate_linkedin_post(self, topic: str = "healthtech_ai", template_name: str = None) -> Dict:
        """Generate a LinkedIn post"""
        if template_name is None:
            template_name = random.choice([
                "healthtech_insight", "lessons_learned", "industry_trend", 
                "behind_the_scenes", "contrarian_take"
            ])
        
        template = next((t for t in self.templates if t.name == template_name), None)
        if not template:
            return {"error": f"Template {template_name} not found"}
        
        topic_data = self.topics.get(topic, self.topics["healthtech_ai"])
        
        # Fill template variables
        content = template.template
        
        if template_name == "healthtech_insight":
            content = content.format(
                hook=random.choice(topic_data["hooks"]),
                insight=random.choice(topic_data["insights"]),
                key_point_1=f"✓ {random.choice(topic_data.get('lessons', ['Focus on outcomes']))}",
                key_point_2=f"✓ {random.choice(topic_data.get('lessons', ['Build incrementally']))}",
                key_point_3=f"✓ {random.choice(topic_data.get('lessons', ['Measure everything']))}",
                closing="The future of healthcare is being written now. Be part of writing it.",
                topic_area=topic.replace("_", " ").title()
            )
        
        elif template_name == "lessons_learned":
            lessons = random.sample(topic_data.get("lessons", ["Learn continuously"]), min(3, len(topic_data.get("lessons", []))))
            content = content.format(
                time_period="20 years",
                field=topic.replace("_", " ").title(),
                lesson_1=lessons[0] if len(lessons) > 0 else "Keep learning",
                lesson_2=lessons[1] if len(lessons) > 1 else "Stay humble",
                lesson_3=lessons[2] if len(lessons) > 2 else "Focus on impact",
                closing="The best investment you can make is in your own growth."
            )
        
        elif template_name == "industry_trend":
            content = content.format(
                trend_statement=random.choice(topic_data.get("trends", ["Change is accelerating"])),
                statistic=random.choice(topic_data.get("statistics", ["Growth is strong"])),
                analysis="This represents a fundamental shift in how healthcare operates. Organizations that adapt will thrive. Those that don't will struggle to compete for both patients and talent.",
                implication="For leaders, this means building adaptive organizations. For professionals, this means developing digital fluency alongside clinical expertise.",
                closing="The question isn't whether to embrace this change. It's how fast you can move."
            )
        
        elif template_name == "contrarian_take":
            content = content.format(
                opinion="We focus too much on AI capabilities and not enough on AI adoption.",
                argument_1="The best AI system that sits unused delivers zero value.",
                argument_2="Change management is harder than model development.",
                argument_3="Physician buy-in determines success more than algorithm accuracy.",
                nuance="That's not to say capabilities don't matter. They do. But adoption is the bottleneck we should be optimizing for."
            )
        
        # Add hashtags
        hashtags = " ".join([f"#{tag}" for tag in template.hashtags[:5]])
        full_content = f"{content}\n\n{hashtags}"
        
        return {
            "content": full_content,
            "template": template_name,
            "topic": topic,
            "tone": template.tone,
            "character_count": len(full_content),
            "hashtags": template.hashtags
        }
    
    def generate_newsletter(self, edition_type: str = "weekly_roundup") -> Dict:
        """Generate a newsletter edition"""
        template = next((t for t in self.templates if t.name == edition_type), None)
        if not template:
            return {"error": f"Template {edition_type} not found"}
        
        today = datetime.now().strftime("%B %d, %Y")
        
        if edition_type == "weekly_roundup":
            content = template.template.format(
                title="HealthTech AI Weekly",
                date=today,
                author="Ahmed Nasr",
                topic="HealthTech AI",
                headline_1="GCC HealthTech Investment Reaches Record Highs",
                summary_1="Saudi Arabia and UAE led the region with $2.3B in HealthTech investments this quarter, focusing on AI-driven diagnostics and telemedicine platforms.",
                implication_1="For healthcare leaders: The funding environment is strong. If you're considering technology investments, the window is open.",
                headline_2="AI Diagnostic Tools Gain Regulatory Approval",
                summary_2="Three new AI diagnostic tools received FDA and regional approvals this week, marking accelerated acceptance of AI in clinical workflows.",
                implication_2="This validates the technology and reduces adoption barriers. Expect faster deployment timelines.",
                headline_3="Hospital Staffing Crisis Drives Automation Demand",
                summary_3="With nurse shortages continuing, hospitals are turning to automation for administrative tasks, freeing clinical staff for patient care.",
                implication_3="The ROI case for automation just got stronger. Administrative AI is becoming essential, not optional.",
                personal_insight="I've seen this pattern before in FinTech. When regulatory clarity meets market pressure, adoption accelerates dramatically. We're entering that phase in HealthTech AI. The next 18 months will be transformative.",
                data_point="Hospitals using AI for administrative tasks report 40% reduction in documentation time, allowing nurses to spend 25% more time with patients.",
                author_signature="— Ahmed Nasr\nPMO & AI Automation Leader\nSaudi German Hospital Group"
            )
        
        elif edition_type == "deep_dive":
            content = template.template.format(
                title="The State of AI in GCC Healthcare",
                topic="Healthcare AI Adoption",
                opening_hook="In 2024, AI in GCC healthcare was experimental. In 2026, it's becoming essential. Here's what changed.",
                current_state="Most GCC hospitals are in early stages of AI adoption. Pilots are common. Production deployments are rare. But that's changing fast.",
                change_1="**Regulatory clarity**: Saudi FDA and UAE health authorities have issued clear guidelines for AI medical devices, reducing uncertainty.",
                change_2="**Proven ROI**: Early adopters are showing measurable results—cost reductions, improved outcomes, happier staff.",
                change_3="**Talent availability**: The region is attracting HealthTech talent from Europe and Asia, filling critical skill gaps.",
                audience="Healthcare Leaders",
                implication="This isn't just about technology. It's about competitive positioning. Hospitals that move fast will attract better staff, serve more patients, and operate more profitably.",
                action_1="Audit your current processes for automation opportunities",
                action_2="Build relationships with HealthTech vendors (don't just evaluate products)",
                action_3="Invest in change management capability—it's the bottleneck",
                closing="The organizations that lead this transformation will define healthcare in the GCC for the next decade. The question is: Will you be leading or following?",
                author_signature="— Ahmed Nasr\nPMO & AI Automation Leader\nSaudi German Hospital Group"
            )
        
        return {
            "content": content,
            "template": edition_type,
            "subject": f"HealthTech AI Weekly - {today}",
            "generated_at": datetime.now().isoformat()
        }
    
    # ===== HOOK GENERATOR - PHASE 1 FEATURE =====
    def generate_hooks(self, count: int = 5, hook_type: str = None, 
                       industry: str = "HealthTech", role: str = "leader") -> List[Dict]:
        """Generate attention-grabbing hooks for LinkedIn posts"""
        import random
        
        hooks = []
        available_hooks = self.hook_templates
        
        # Filter by type if specified
        if hook_type:
            available_hooks = [h for h in self.hook_templates if h['type'] == hook_type]
        
        # Generate hooks
        for _ in range(count):
            if not available_hooks:
                break
            
            template = random.choice(available_hooks)
            hook_text = template["template"]
            
            # Fill in variables
            for key, values in self.hook_variables.items():
                if "{" + key + "}" in hook_text and values:
                    replacement = random.choice(values)
                    hook_text = hook_text.replace("{" + key + "}", replacement)
            
            # Replace remaining placeholders with defaults
            hook_text = hook_text.replace("{industry}", industry)
            hook_text = hook_text.replace("{role}", role)
            hook_text = hook_text.replace("{years}", str(random.randint(5, 20)))
            hook_text = hook_text.replace("{percentage}", str(random.randint(30, 90)))
            hook_text = hook_text.replace("{number}", str(random.randint(3, 10)))
            hook_text = hook_text.replace("{timeframe}", random.choice(["30 days", "90 days", "6 months"]))
            
            hooks.append({
                "hook": hook_text,
                "type": template["type"],
                "engagement": template["engagement"],
                "ready_to_use": "{" not in hook_text
            })
        
        return hooks
    
    def get_hook_templates_by_type(self) -> Dict[str, List[str]]:
        """Get all hook templates grouped by type"""
        by_type = {}
        for hook in self.hook_templates:
            if hook["type"] not in by_type:
                by_type[hook["type"]] = []
            by_type[hook["type"]].append(hook["template"])
        return by_type
    
    def generate_content_calendar(self, days: int = 30) -> List[Dict]:
        """Generate a content calendar"""
        calendar = []
        topics = ["healthtech_ai", "digital_transformation", "leadership", "fintech_bridge"]
        templates = ["healthtech_insight", "lessons_learned", "industry_trend", "behind_the_scenes"]
        
        for day in range(days):
            date = datetime.now() + __import__('datetime').timedelta(days=day)
            
            # 3 LinkedIn posts per week (Mon, Wed, Fri)
            if date.weekday() in [0, 2, 4]:  # Monday, Wednesday, Friday
                topic = topics[day % len(topics)]
                template = templates[day % len(templates)]
                
                post = self.generate_linkedin_post(topic, template)
                calendar.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "type": "LinkedIn Post",
                    "topic": topic,
                    "content_preview": post["content"][:100] + "...",
                    "full_content": post["content"]
                })
            
            # 1 Newsletter per week (Sunday)
            if date.weekday() == 6:  # Sunday
                newsletter = self.generate_newsletter("weekly_roundup")
                calendar.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "type": "Newsletter",
                    "subject": newsletter["subject"],
                    "content_preview": newsletter["content"][:100] + "...",
                    "full_content": newsletter["content"]
                })
        
        return calendar
    
    def save_content(self, content: Dict, filename: str = None):
        """Save generated content to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"content_{timestamp}.txt"
        
        output_dir = Path("/root/.openclaw/workspace/tools/cv-optimizer/output/content")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / filename
        with open(filepath, 'w') as f:
            f.write(content.get("content", ""))
        
        return filepath


def main():
    """CLI interface"""
    import sys
    
    factory = ContentFactory()
    
    if len(sys.argv) < 2:
        print("Content Factory - Generate LinkedIn posts and newsletters")
        print()
        print("Usage:")
        print("  python content_factory.py linkedin [topic] [template]")
        print("  python content_factory.py newsletter [type]")
        print("  python content_factory.py calendar [days]")
        print()
        print("Topics: healthtech_ai, digital_transformation, leadership, fintech_bridge")
        print("Templates: healthtech_insight, lessons_learned, industry_trend, behind_the_scenes, contrarian_take")
        print("Newsletter types: weekly_roundup, deep_dive")
        return
    
    command = sys.argv[1]
    
    if command == "linkedin":
        topic = sys.argv[2] if len(sys.argv) > 2 else "healthtech_ai"
        template = sys.argv[3] if len(sys.argv) > 3 else None
        
        result = factory.generate_linkedin_post(topic, template)
        print("=" * 60)
        print(f"LINKEDIN POST - {topic.upper()}")
        print(f"Template: {result.get('template', 'random')}")
        print(f"Tone: {result.get('tone', 'professional')}")
        print(f"Characters: {result['character_count']}")
        print("=" * 60)
        print()
        print(result["content"])
        print()
        
        # Save
        filepath = factory.save_content(result, f"linkedin_{topic}_{datetime.now().strftime('%Y%m%d')}.txt")
        print(f"✅ Saved to: {filepath}")
    
    elif command == "newsletter":
        edition_type = sys.argv[2] if len(sys.argv) > 2 else "weekly_roundup"
        
        result = factory.generate_newsletter(edition_type)
        print("=" * 60)
        print(f"NEWSLETTER - {edition_type.upper()}")
        print(f"Subject: {result.get('subject', '')}")
        print(f"Words: {result['word_count']} | Characters: {result['character_count']}")
        print("=" * 60)
        print()
        print(result["content"])
        print()
        
        # Save
        filepath = factory.save_content(result, f"newsletter_{edition_type}_{datetime.now().strftime('%Y%m%d')}.md")
        print(f"✅ Saved to: {filepath}")
    
    elif command == "calendar":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        
        calendar = factory.generate_content_calendar(days)
        print("=" * 60)
        print(f"CONTENT CALENDAR - Next {days} Days")
        print("=" * 60)
        print()
        
        for item in calendar[:10]:  # Show first 10
            print(f"📅 {item['date']} | {item['type']}")
            if item['type'] == 'Newsletter':
                print(f"   Subject: {item.get('subject', 'N/A')}")
            else:
                print(f"   Topic: {item['topic']}")
            print()
        
        print(f"... and {len(calendar) - 10} more items")
        print(f"\n✅ Generated {len(calendar)} content pieces")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
