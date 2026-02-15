# Opportunity Engine 🚀

**Your complete job search and career optimization system**

Built for Ahmed Nasr's executive transition to HealthTech AI leadership roles.

---

## 🎯 What This Is

The Opportunity Engine is a 4-tool integrated system that helps you:
1. **Optimize CVs** for specific job postings (ATS score >90)
2. **Track job applications** through the entire pipeline
3. **Generate content** for LinkedIn and newsletters
4. **Search** across all your knowledge (CVs, jobs, notes)

---

## 📦 Tools Included

### 1. CV Optimizer
Parse job descriptions → Generate tailored CVs → ATS scoring

```bash
python3 src/opportunity_engine.py process data/sample_job.txt --company "Company Name" --title "Job Title"
```

**Features:**
- Keyword matching against job requirements
- ATS score (target: 90+)
- Specific improvement suggestions
- Auto-generates tailored CV text

### 2. Job Tracker
Track applications from "Applied" → "Offer"

```bash
# Add job
python3 src/job_tracker.py add "Company" "Title" "Location" "Source" "Sector"

# View pipeline
python3 src/opportunity_engine.py jobs --list

# Update status
python3 src/opportunity_engine.py jobs --update JOB_ID "Interview" "Had phone screen"

# View follow-ups
python3 src/opportunity_engine.py jobs --followups
```

**Features:**
- Visual pipeline (Applied → Phone Screen → Interview → Offer)
- Follow-up reminders
- Statistics and conversion rates
- Priority scoring

### 3. Content Factory
Generate LinkedIn posts and newsletters

```bash
# Generate LinkedIn post
python3 src/content_factory.py linkedin healthtech_ai

# Generate newsletter
python3 src/content_factory.py newsletter weekly_roundup

# Generate content calendar
python3 src/content_factory.py calendar 30
```

**Features:**
- HealthTech AI focused content
- Multiple templates (insights, lessons, trends, contrarian takes)
- Newsletter generator
- 30-day content calendar

### 4. 2nd Brain
Semantic search across all your documents

```bash
# Search knowledge base
python3 src/opportunity_engine.py search "AI healthcare"

# View stats
python3 src/second_brain.py stats
```

**Features:**
- Search CVs, job postings, notes
- Find similar jobs to your CV
- Export knowledge base

---

## 🚀 Quick Start

### Full Dashboard
```bash
python3 src/opportunity_engine.py dashboard
```

### Process a Job Posting
1. Save job description to a file (e.g., `job.txt`)
2. Run:
```bash
python3 src/opportunity_engine.py process job.txt --company "Company Name" --title "Job Title"
```

This will:
- ✅ Parse the job description
- ✅ Generate a tailored CV
- ✅ Calculate ATS score
- ✅ Add to job tracker
- ✅ Index in knowledge base

### Generate Weekly Content
```bash
python3 src/opportunity_engine.py content --topic healthtech_ai
```

---

## 📊 Your Profile Data

The system is pre-loaded with your profile:

- **Name:** Ahmed Nasr
- **Title:** PMO & AI Automation Leader
- **Current Role:** Saudi German Hospital Group (TopMed)
- **Experience:** 20+ years (Intel, Microsoft, Consulting)
- **Certifications:** MBA, PMP, CSM, CSPO, Lean Six Sigma, CBAP, MCAD, MCP
- **Sectors:** HealthTech, FinTech, Technology
- **Location:** Egypt (Work: UAE, KSA)
- **Visa:** UAE Permanent Work Visa

---

## 📁 Directory Structure

```
cv-optimizer/
├── src/
│   ├── cv_optimizer.py          # CV generation & ATS scoring
│   ├── job_tracker.py            # Application pipeline tracking
│   ├── content_factory.py        # LinkedIn & newsletter generator
│   ├── second_brain.py           # Semantic search & knowledge base
│   └── opportunity_engine.py     # Master integration
├── data/
│   ├── sample_job.txt            # Example job posting
│   ├── job_applications.json     # Your job tracker data
│   └── second_brain.json         # Your knowledge base
└── output/
    ├── cv_*.txt                  # Generated CVs
    └── content/
        ├── linkedin_*.txt        # LinkedIn posts
        └── newsletter_*.md       # Newsletters
```

---

## 🎯 Workflow Examples

### Daily Workflow
```bash
# 1. Check dashboard
python3 src/opportunity_engine.py dashboard

# 2. Process new job
python3 src/opportunity_engine.py process job.txt --company "ACME Health" --title "VP Digital Transformation"

# 3. Generate content for the day
python3 src/opportunity_engine.py content
```

### Weekly Workflow
```bash
# Review pipeline
python3 src/opportunity_engine.py jobs --list

# Check follow-ups
python3 src/opportunity_engine.py jobs --followups

# Generate week's content
python3 src/content_factory.py calendar 7
```

---

## 💡 Tips for Best Results

### CV Optimization
- Target ATS score >90
- Add missing keywords to your master profile
- Use generated suggestions to improve match

### Job Tracking
- Update status immediately after each interaction
- Set priorities (1-5) for high-value opportunities
- Check follow-ups weekly

### Content Generation
- Post 3x/week (Mon, Wed, Fri) for algorithm boost
- Mix HealthTech (70%) with FinTech bridge (30%)
- Use "contrarian_take" template for engagement

### Knowledge Base
- Ingest every job you apply to
- Search before interviews for talking points
- Find patterns across similar jobs

---

## 🔧 Advanced Usage

### Custom CV Generation
```python
from cv_optimizer import CVGenerator, ProfileDatabase

profile = ProfileDatabase()
generator = CVGenerator(profile)

tailored_cv = generator.generate(job_text, "Job Title", "Company")
print(f"ATS Score: {tailored_cv.ats_score}")
print(tailored_cv.suggestions)
```

### Batch Job Processing
```bash
for job in jobs/*.txt; do
    python3 src/opportunity_engine.py process "$job" --company "$(head -1 $job)" --title "$(head -2 $job | tail -1)"
done
```

### Content Calendar Export
```bash
python3 src/content_factory.py calendar 30 > content_calendar.txt
```

---

## 📈 Metrics to Track

**Weekly Goals:**
- [ ] 5 job applications processed
- [ ] ATS score >85 for each
- [ ] 3 LinkedIn posts published
- [ ] 1 newsletter sent
- [ ] 10 follow-ups completed

**Target Conversion:**
- Applications → Phone Screen: 20%
- Phone Screen → Interview: 50%
- Interview → Offer: 30%

---

## 🆘 Troubleshooting

**"Module not found" errors:**
```bash
cd /root/.openclaw/workspace/tools/cv-optimizer
python3 -m src.opportunity_engine dashboard
```

**Reset job tracker:**
```bash
rm data/job_applications.json
```

**Reset knowledge base:**
```bash
rm data/second_brain.json
```

---

## 🎓 Next Steps

1. **Process 5 jobs today** using the workflow above
2. **Post generated LinkedIn content** this week
3. **Update your LinkedIn headline** to match new positioning
4. **Track all applications** in the job tracker
5. **Review dashboard weekly** for follow-ups

---

## 📞 Usage

All commands work from the `cv-optimizer` directory:

```bash
cd /root/.openclaw/workspace/tools/cv-optimizer
```

Then use any command from this README.

---

**Built with MiniMax M2.1 during 6-day low-cost trial period**  
**For:** Ahmed Nasr - Executive transition to HealthTech AI leadership  
**Date:** February 2026
