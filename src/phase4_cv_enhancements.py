#!/usr/bin/env python3
"""
Phase 4 - CV Core Enhancements
Features: Version History, Reading Time, Health Timeline, Missing Skills,
          Section Reordering, Template Preview, Bulk Export,
          PDF Accessibility, LinkedIn Headline, Reference Manager, Portfolio Links
"""

import json
import re
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path


class CVVersionHistory:
    """Track every CV change with revert capability"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.history_file = self.data_dir / "cv_versions.json"
        self.versions = self._load()

    def _load(self) -> List[Dict]:
        if self.history_file.exists():
            return json.loads(self.history_file.read_text())
        return []

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.history_file.write_text(json.dumps(self.versions, indent=2))

    def save_version(self, cv_data: Dict, label: str = "", job_title: str = "") -> Dict:
        version = {
            "id": f"v{len(self.versions)+1}",
            "timestamp": datetime.now().isoformat(),
            "label": label or f"Version {len(self.versions)+1}",
            "job_title": job_title,
            "cv_data": cv_data,
            "ats_score": cv_data.get("ats_score", 0),
            "word_count": len(str(cv_data).split()),
        }
        self.versions.append(version)
        self._save()
        return version

    def get_versions(self) -> List[Dict]:
        return [
            {k: v for k, v in ver.items() if k != "cv_data"}
            for ver in self.versions
        ]

    def get_version(self, version_id: str) -> Optional[Dict]:
        for ver in self.versions:
            if ver["id"] == version_id:
                return ver
        return None

    def revert_to(self, version_id: str) -> Optional[Dict]:
        ver = self.get_version(version_id)
        if ver:
            reverted = {
                "id": f"v{len(self.versions)+1}",
                "timestamp": datetime.now().isoformat(),
                "label": f"Reverted to {ver['label']}",
                "job_title": ver.get("job_title", ""),
                "cv_data": ver["cv_data"],
                "ats_score": ver.get("ats_score", 0),
                "word_count": ver.get("word_count", 0),
                "reverted_from": version_id,
            }
            self.versions.append(reverted)
            self._save()
            return reverted
        return None

    def diff_versions(self, v1_id: str, v2_id: str) -> Dict:
        v1 = self.get_version(v1_id)
        v2 = self.get_version(v2_id)
        if not v1 or not v2:
            return {"error": "Version not found"}
        return {
            "v1": {"id": v1["id"], "label": v1["label"], "ats_score": v1.get("ats_score", 0)},
            "v2": {"id": v2["id"], "label": v2["label"], "ats_score": v2.get("ats_score", 0)},
            "ats_diff": v2.get("ats_score", 0) - v1.get("ats_score", 0),
            "word_diff": v2.get("word_count", 0) - v1.get("word_count", 0),
        }


class ReadingTimeEstimator:
    """Estimate recruiter reading time for CVs"""

    RECRUITER_WPM = 250  # Average reading speed
    SCAN_WPM = 600       # Quick scan speed
    AVERAGE_CV_REVIEW_SECONDS = 7.4  # Industry average

    def estimate(self, cv_text: str) -> Dict:
        words = len(cv_text.split())
        sentences = max(1, len(re.split(r'[.!?]+', cv_text)))
        
        full_read_seconds = (words / self.RECRUITER_WPM) * 60
        scan_seconds = (words / self.SCAN_WPM) * 60
        
        # Complexity factors
        avg_sentence_len = words / sentences
        complexity = "simple" if avg_sentence_len < 15 else "moderate" if avg_sentence_len < 25 else "complex"
        
        return {
            "word_count": words,
            "sentence_count": sentences,
            "full_read_time_seconds": round(full_read_seconds, 1),
            "scan_time_seconds": round(scan_seconds, 1),
            "industry_average_seconds": self.AVERAGE_CV_REVIEW_SECONDS,
            "complexity": complexity,
            "recommendation": self._get_recommendation(words, full_read_seconds),
            "formatting_tips": [
                "Use bullet points for easy scanning",
                "Bold key achievements and numbers",
                "Keep summary under 3 sentences",
                "Use white space between sections"
            ]
        }

    def _get_recommendation(self, words: int, read_time: float) -> str:
        if words > 800:
            return "CV is too long. Recruiters spend ~7 seconds on first scan. Trim to under 600 words."
        elif words < 200:
            return "CV may be too short. Add more detail about achievements and skills."
        elif words <= 600:
            return "Good length! Fits within typical recruiter attention span."
        return "Slightly long. Consider trimming less relevant experiences."


class CVHealthTimeline:
    """Track ATS scores over time with chart data"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.timeline_file = self.data_dir / "cv_health_timeline.json"
        self.entries = self._load()

    def _load(self) -> List[Dict]:
        if self.timeline_file.exists():
            return json.loads(self.timeline_file.read_text())
        # Generate sample data
        return self._generate_sample_data()

    def _generate_sample_data(self) -> List[Dict]:
        entries = []
        base_date = datetime.now() - timedelta(days=90)
        scores = [62, 65, 68, 71, 74, 72, 76, 78, 80, 82, 85, 87, 89, 91]
        for i, score in enumerate(scores):
            entries.append({
                "date": (base_date + timedelta(days=i * 7)).strftime("%Y-%m-%d"),
                "ats_score": score,
                "job_title": f"Application #{i+1}",
                "changes_made": ["Updated skills", "Added metrics"][i % 2],
            })
        return entries

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.timeline_file.write_text(json.dumps(self.entries, indent=2))

    def add_entry(self, ats_score: int, job_title: str = "", changes: str = "") -> Dict:
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "ats_score": ats_score,
            "job_title": job_title,
            "changes_made": changes,
        }
        self.entries.append(entry)
        self._save()
        return entry

    def get_timeline(self) -> Dict:
        if not self.entries:
            return {"entries": [], "trend": "no_data", "chart_data": {"labels": [], "scores": []}}
        
        labels = [e["date"] for e in self.entries]
        scores = [e["ats_score"] for e in self.entries]
        
        trend = "improving" if len(scores) > 1 and scores[-1] > scores[0] else "declining" if len(scores) > 1 and scores[-1] < scores[0] else "stable"
        avg_score = round(sum(scores) / len(scores), 1)
        
        return {
            "entries": self.entries[-20:],
            "trend": trend,
            "average_score": avg_score,
            "best_score": max(scores),
            "latest_score": scores[-1],
            "improvement": scores[-1] - scores[0] if len(scores) > 1 else 0,
            "chart_data": {"labels": labels[-20:], "scores": scores[-20:]}
        }


class MissingSkillsDetector:
    """Detect skills in job descriptions missing from CV"""

    SKILL_CATEGORIES = {
        "technical": ["python", "java", "javascript", "react", "node.js", "sql", "aws", "azure",
                      "docker", "kubernetes", "machine learning", "ai", "data science", "tensorflow",
                      "pytorch", "tableau", "power bi", "excel", "sap", "salesforce", "jira",
                      "confluence", "git", "ci/cd", "api", "rest", "graphql", "mongodb", "postgresql"],
        "leadership": ["leadership", "management", "strategic planning", "team building",
                       "stakeholder management", "cross-functional", "c-suite", "board",
                       "mentoring", "coaching", "organizational design", "change management"],
        "healthcare": ["hipaa", "hl7", "fhir", "ehr", "emr", "clinical", "patient safety",
                       "healthcare operations", "hospital management", "jci", "quality improvement",
                       "lean six sigma", "patient experience"],
        "soft_skills": ["communication", "problem solving", "analytical", "presentation",
                        "negotiation", "collaboration", "innovation", "agile", "scrum"]
    }

    def detect(self, cv_text: str, job_description: str) -> Dict:
        cv_lower = cv_text.lower()
        jd_lower = job_description.lower()
        
        missing = []
        matched = []
        
        for category, skills in self.SKILL_CATEGORIES.items():
            for skill in skills:
                if skill in jd_lower:
                    if skill in cv_lower:
                        matched.append({"skill": skill, "category": category})
                    else:
                        missing.append({"skill": skill, "category": category, "priority": "high" if skill in jd_lower[:500] else "medium"})
        
        # Also extract custom keywords from JD
        jd_words = set(re.findall(r'\b[a-z][a-z+#.]{2,}\b', jd_lower))
        cv_words = set(re.findall(r'\b[a-z][a-z+#.]{2,}\b', cv_lower))
        
        custom_missing = jd_words - cv_words - {"the", "and", "for", "with", "that", "this", "from", "have", "will", "are", "our", "you", "your"}
        
        return {
            "matched_skills": matched,
            "missing_skills": missing[:15],
            "match_rate": round(len(matched) / max(1, len(matched) + len(missing)) * 100, 1),
            "recommendations": [
                f"Add '{s['skill']}' to your CV — required by this role"
                for s in missing[:5]
            ],
            "custom_keywords_missing": list(custom_missing)[:10],
            "action_items": len(missing)
        }


class SectionReorderer:
    """Drag-drop section reordering for CV"""

    DEFAULT_ORDER = ["summary", "experience", "skills", "education", "certifications", "projects", "languages"]

    def get_sections(self, cv_data: Dict = None) -> List[Dict]:
        sections = []
        for i, section in enumerate(self.DEFAULT_ORDER):
            sections.append({
                "id": section,
                "name": section.replace("_", " ").title(),
                "order": i,
                "visible": True,
                "bullet_count": len(cv_data.get(section, [])) if cv_data and isinstance(cv_data.get(section), list) else 0
            })
        return sections

    def reorder(self, new_order: List[str]) -> List[Dict]:
        return [
            {"id": section, "name": section.replace("_", " ").title(), "order": i, "visible": True}
            for i, section in enumerate(new_order)
        ]

    def toggle_section(self, sections: List[Dict], section_id: str) -> List[Dict]:
        for s in sections:
            if s["id"] == section_id:
                s["visible"] = not s["visible"]
        return sections


class TemplatePreview:
    """Preview CV templates before generating PDF"""

    TEMPLATES = {
        "executive": {
            "name": "Executive Professional",
            "colors": {"primary": "#1a365d", "accent": "#2b6cb0", "bg": "#ffffff"},
            "font": "Georgia, serif",
            "layout": "two-column",
            "preview_html": "<div style='font-family:Georgia;color:#1a365d;padding:20px'><h1 style='border-bottom:3px solid #2b6cb0'>NAME</h1><p>SUMMARY</p></div>"
        },
        "modern": {
            "name": "Modern Minimal",
            "colors": {"primary": "#2d3748", "accent": "#4299e1", "bg": "#f7fafc"},
            "font": "Inter, sans-serif",
            "layout": "single-column",
            "preview_html": "<div style='font-family:sans-serif;color:#2d3748;padding:20px;background:#f7fafc'><h1>NAME</h1><hr style='border-color:#4299e1'><p>SUMMARY</p></div>"
        },
        "creative": {
            "name": "Creative Bold",
            "colors": {"primary": "#553c9a", "accent": "#d53f8c", "bg": "#faf5ff"},
            "font": "Poppins, sans-serif",
            "layout": "sidebar",
            "preview_html": "<div style='font-family:sans-serif;color:#553c9a;padding:20px;background:#faf5ff'><h1 style='color:#d53f8c'>NAME</h1><p>SUMMARY</p></div>"
        },
        "healthtech": {
            "name": "HealthTech Professional",
            "colors": {"primary": "#234e52", "accent": "#38b2ac", "bg": "#e6fffa"},
            "font": "Roboto, sans-serif",
            "layout": "two-column",
            "preview_html": "<div style='font-family:sans-serif;color:#234e52;padding:20px;background:#e6fffa'><h1 style='border-left:4px solid #38b2ac;padding-left:12px'>NAME</h1><p>SUMMARY</p></div>"
        },
        "fintech": {
            "name": "FinTech Executive",
            "colors": {"primary": "#1a202c", "accent": "#48bb78", "bg": "#ffffff"},
            "font": "Source Sans Pro, sans-serif",
            "layout": "single-column",
            "preview_html": "<div style='font-family:sans-serif;color:#1a202c;padding:20px'><h1 style='color:#48bb78'>NAME</h1><p>SUMMARY</p></div>"
        },
        "academic": {
            "name": "Academic Research",
            "colors": {"primary": "#2d3748", "accent": "#744210", "bg": "#fffff0"},
            "font": "Times New Roman, serif",
            "layout": "single-column",
            "preview_html": "<div style='font-family:serif;color:#2d3748;padding:20px;background:#fffff0'><h1 style='font-size:20px'>NAME</h1><p>SUMMARY</p></div>"
        },
        "startup": {
            "name": "Startup Hustler",
            "colors": {"primary": "#1a202c", "accent": "#ed8936", "bg": "#fffaf0"},
            "font": "Nunito, sans-serif",
            "layout": "sidebar",
            "preview_html": "<div style='font-family:sans-serif;color:#1a202c;padding:20px;background:#fffaf0'><h1 style='color:#ed8936'>NAME</h1><p>SUMMARY</p></div>"
        },
        "consulting": {
            "name": "Consulting Pro",
            "colors": {"primary": "#1a365d", "accent": "#3182ce", "bg": "#ebf8ff"},
            "font": "Calibri, sans-serif",
            "layout": "two-column",
            "preview_html": "<div style='font-family:sans-serif;color:#1a365d;padding:20px;background:#ebf8ff'><h1>NAME</h1><p>SUMMARY</p></div>"
        },
        "government": {
            "name": "Government/Public Sector",
            "colors": {"primary": "#2d3748", "accent": "#2b6cb0", "bg": "#ffffff"},
            "font": "Arial, sans-serif",
            "layout": "single-column",
            "preview_html": "<div style='font-family:Arial;color:#2d3748;padding:20px'><h1 style='font-size:18px;text-transform:uppercase'>NAME</h1><p>SUMMARY</p></div>"
        },
        "remote": {
            "name": "Remote Worker",
            "colors": {"primary": "#2d3748", "accent": "#6b46c1", "bg": "#faf5ff"},
            "font": "Lato, sans-serif",
            "layout": "single-column",
            "preview_html": "<div style='font-family:sans-serif;color:#2d3748;padding:20px;background:#faf5ff'><h1 style='color:#6b46c1'>🌍 NAME</h1><p>SUMMARY</p></div>"
        }
    }

    def get_all_templates(self) -> List[Dict]:
        return [
            {"id": tid, "name": t["name"], "colors": t["colors"], "font": t["font"],
             "layout": t["layout"], "preview_html": t["preview_html"]}
            for tid, t in self.TEMPLATES.items()
        ]

    def preview(self, template_id: str, cv_data: Dict) -> Dict:
        template = self.TEMPLATES.get(template_id, self.TEMPLATES["modern"])
        name = cv_data.get("name", "Your Name")
        summary = cv_data.get("summary", "Professional summary goes here...")
        
        preview_html = template["preview_html"].replace("NAME", name).replace("SUMMARY", summary)
        
        return {
            "template": template_id,
            "template_name": template["name"],
            "preview_html": preview_html,
            "colors": template["colors"],
            "font": template["font"],
            "layout": template["layout"]
        }


class BulkExport:
    """Export all CVs at once"""

    def export_all(self, versions: List[Dict]) -> Dict:
        export_data = {
            "export_date": datetime.now().isoformat(),
            "total_cvs": len(versions),
            "versions": versions,
            "format": "json",
            "size_estimate_kb": round(len(json.dumps(versions)) / 1024, 1)
        }
        return export_data

    def export_summary(self, versions: List[Dict]) -> Dict:
        return {
            "total_versions": len(versions),
            "date_range": {
                "earliest": versions[0]["timestamp"] if versions else None,
                "latest": versions[-1]["timestamp"] if versions else None,
            },
            "average_ats_score": round(
                sum(v.get("ats_score", 0) for v in versions) / max(1, len(versions)), 1
            ),
            "best_version": max(versions, key=lambda v: v.get("ats_score", 0))["id"] if versions else None,
            "formats_available": ["json", "pdf", "html"]
        }


class PDFAccessibilityChecker:
    """Check CV PDF for accessibility compliance"""

    def check(self, cv_data: Dict) -> Dict:
        issues = []
        score = 100

        # Check for alt text on images
        if cv_data.get("has_images") and not cv_data.get("alt_texts"):
            issues.append({"severity": "high", "issue": "Images without alt text", "fix": "Add descriptive alt text to all images"})
            score -= 15

        # Check heading hierarchy
        sections = cv_data.get("sections", [])
        if len(sections) < 3:
            issues.append({"severity": "medium", "issue": "Few section headings", "fix": "Use clear section headings for screen readers"})
            score -= 10

        # Check color contrast
        if cv_data.get("template", "") in ["creative"]:
            issues.append({"severity": "medium", "issue": "Potential color contrast issues", "fix": "Ensure 4.5:1 contrast ratio for text"})
            score -= 10

        # Check font size
        if cv_data.get("font_size", 11) < 10:
            issues.append({"severity": "high", "issue": "Font size too small", "fix": "Use minimum 10pt font for readability"})
            score -= 15

        # Check for tables
        issues.append({"severity": "low", "issue": "Consider linear layout", "fix": "Avoid complex tables — use simple lists for ATS compatibility"})
        score -= 5

        return {
            "accessibility_score": max(0, score),
            "issues": issues,
            "compliant": score >= 80,
            "wcag_level": "AA" if score >= 90 else "A" if score >= 70 else "Non-compliant",
            "recommendations": [
                "Use semantic headings (H1, H2, H3)",
                "Ensure sufficient color contrast",
                "Add alt text to any images or logos",
                "Use readable font sizes (10pt+)",
                "Keep layout simple and linear"
            ]
        }


class LinkedInHeadlineOptimizer:
    """Optimize LinkedIn headlines for visibility"""

    def optimize(self, current_headline: str, target_role: str = "", skills: List[str] = None) -> Dict:
        skills = skills or []
        suggestions = []

        # Generate headline variants
        if target_role:
            suggestions.append(f"{target_role} | {' | '.join(skills[:3])}")
            suggestions.append(f"{target_role} — Driving Results in {skills[0] if skills else 'Operations'}")
            suggestions.append(f"Passionate {target_role} | {skills[0] if skills else 'Innovation'} & {skills[1] if len(skills) > 1 else 'Strategy'}")
        
        suggestions.extend([
            f"Experienced Leader in {skills[0] if skills else 'Healthcare'} | Open to Opportunities",
            f"Helping organizations transform through {skills[0] if skills else 'technology'} & {skills[1] if len(skills) > 1 else 'innovation'}"
        ])

        # Score current headline
        current_score = 50
        if len(current_headline) > 40:
            current_score += 10
        if "|" in current_headline or "—" in current_headline:
            current_score += 10
        if any(s.lower() in current_headline.lower() for s in skills[:3]):
            current_score += 15
        if any(w in current_headline.lower() for w in ["helping", "driving", "leading", "building"]):
            current_score += 10

        return {
            "current_headline": current_headline,
            "current_score": min(100, current_score),
            "suggestions": suggestions[:5],
            "best_suggestion": suggestions[0] if suggestions else current_headline,
            "tips": [
                "Include your target role title for SEO",
                "Use | or — to separate key points",
                "Mention 2-3 key skills or specialties",
                "Keep it under 120 characters",
                "Use keywords recruiters search for"
            ]
        }


class ReferenceManager:
    """Manage professional references"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.refs_file = self.data_dir / "references.json"
        self.references = self._load()

    def _load(self) -> List[Dict]:
        if self.refs_file.exists():
            return json.loads(self.refs_file.read_text())
        return [
            {"id": "ref1", "name": "Dr. Sarah Al-Rashid", "title": "CEO", "company": "MENA HealthTech",
             "relationship": "Former supervisor", "email": "sarah@example.com", "phone": "+966-xxx",
             "strength": "strong", "last_contact": "2026-01-15", "notes": "Great rapport, knows my AI work"},
            {"id": "ref2", "name": "Mark Johnson", "title": "VP Engineering", "company": "TechCorp",
             "relationship": "Colleague", "email": "mark@example.com", "phone": "+1-xxx",
             "strength": "medium", "last_contact": "2025-12-20", "notes": "Worked on healthcare platform together"},
        ]

    def _save(self):
        self.data_dir.mkdir(exist_ok=True)
        self.refs_file.write_text(json.dumps(self.references, indent=2))

    def get_all(self) -> List[Dict]:
        return self.references

    def add(self, ref_data: Dict) -> Dict:
        ref = {
            "id": f"ref{len(self.references)+1}",
            "name": ref_data.get("name", ""),
            "title": ref_data.get("title", ""),
            "company": ref_data.get("company", ""),
            "relationship": ref_data.get("relationship", ""),
            "email": ref_data.get("email", ""),
            "phone": ref_data.get("phone", ""),
            "strength": ref_data.get("strength", "medium"),
            "last_contact": datetime.now().strftime("%Y-%m-%d"),
            "notes": ref_data.get("notes", ""),
        }
        self.references.append(ref)
        self._save()
        return ref

    def remove(self, ref_id: str) -> bool:
        self.references = [r for r in self.references if r["id"] != ref_id]
        self._save()
        return True

    def suggest_for_role(self, job_title: str) -> List[Dict]:
        # Return strongest references first
        sorted_refs = sorted(self.references, key=lambda r: {"strong": 3, "medium": 2, "weak": 1}.get(r.get("strength", ""), 0), reverse=True)
        return sorted_refs[:3]


class PortfolioLinkGenerator:
    """Generate portfolio/project links for CV"""

    def generate(self, projects: List[Dict] = None) -> Dict:
        projects = projects or [
            {"name": "Healthcare AI Platform", "url": "https://github.com/example/health-ai", "type": "github"},
            {"name": "Hospital Operations Dashboard", "url": "https://portfolio.example.com/ops-dashboard", "type": "portfolio"},
            {"name": "PMO Framework", "url": "https://docs.example.com/pmo", "type": "documentation"},
        ]
        
        links = []
        for p in projects:
            links.append({
                "name": p["name"],
                "url": p.get("url", "#"),
                "type": p.get("type", "other"),
                "icon": {"github": "fab fa-github", "portfolio": "fas fa-briefcase",
                         "documentation": "fas fa-file-alt", "linkedin": "fab fa-linkedin"}.get(p.get("type", ""), "fas fa-link"),
                "qr_data": f"QR:{p.get('url', '#')}"
            })
        
        return {
            "links": links,
            "total": len(links),
            "portfolio_url": "https://portfolio.example.com/ahmed-nasr",
            "shortlink": "https://cv.link/ahmed",
            "tips": [
                "Include GitHub for technical roles",
                "Add a personal portfolio site",
                "Link relevant project documentation",
                "Use short URLs for printed CVs"
            ]
        }
