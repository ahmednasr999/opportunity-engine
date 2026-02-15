#!/usr/bin/env python3
"""
PDF Export System - Generate professional PDFs from CVs and cover letters
Uses Jinja2 + WeasyPrint for HTML-to-PDF conversion
"""

import os
from datetime import datetime
from typing import Dict, Optional
from jinja2 import Template
from weasyprint import HTML

# Professional CV Template with Jinja2
CV_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{name}} - {{headline}}</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
            @bottom-center {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #666;
            }
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #333;
        }
        
        .header {
            text-align: center;
            padding-bottom: 20px;
            border-bottom: 2px solid #1a365d;
            margin-bottom: 20px;
        }
        
        .name {
            font-size: 28pt;
            font-weight: 700;
            color: #1a365d;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }
        
        .title {
            font-size: 14pt;
            color: #4a5568;
            margin-bottom: 12px;
            font-weight: 500;
        }
        
        .contact {
            font-size: 10pt;
            color: #666;
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .contact-item {
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }
        
        .section {
            margin-bottom: 20px;
        }
        
        .section-title {
            font-size: 12pt;
            font-weight: 700;
            color: #1a365d;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 5px;
            margin-bottom: 12px;
        }
        
        .summary {
            text-align: justify;
            font-size: 10.5pt;
            line-height: 1.6;
        }
        
        .experience-item {
            margin-bottom: 15px;
        }
        
        .exp-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 4px;
        }
        
        .exp-title {
            font-weight: 700;
            font-size: 11pt;
            color: #2d3748;
        }
        
        .exp-company {
            font-weight: 600;
            color: #4a5568;
        }
        
        .exp-date {
            font-size: 9pt;
            color: #718096;
            font-style: italic;
        }
        
        .exp-location {
            font-size: 9pt;
            color: #718096;
        }
        
        .exp-description {
            margin-top: 6px;
            font-size: 10pt;
            padding-left: 0;
        }
        
        .exp-description ul {
            margin-left: 18px;
        }
        
        .exp-description li {
            margin-bottom: 4px;
            line-height: 1.5;
        }
        
        .skills-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        
        .skill-tag {
            background: #edf2f7;
            color: #2d3748;
            padding: 4px 10px;
            border-radius: 3px;
            font-size: 9pt;
            font-weight: 500;
        }
        
        .education-item {
            margin-bottom: 10px;
        }
        
        .edu-degree {
            font-weight: 700;
            color: #2d3748;
        }
        
        .edu-school {
            color: #4a5568;
        }
        
        .edu-year {
            font-size: 9pt;
            color: #718096;
        }
        
        .cert-list {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }
        
        .cert-item {
            font-size: 10pt;
        }
        
        .two-column {
            display: flex;
            gap: 30px;
        }
        
        .column {
            flex: 1;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="name">{{name}}</div>
        <div class="title">{{headline}}</div>
        <div class="contact">
            {% if location %}<span class="contact-item">{{location}}</span>{% endif %}
            {% if phone_uae %}<span class="contact-item">📱 UAE: {{phone_uae}}</span>{% endif %}
            {% if phone_egypt %}<span class="contact-item">📱 Egypt: {{phone_egypt}}</span>{% endif %}
            {% if email %}<span class="contact-item">{{email}}</span>{% endif %}
            {% if linkedin %}<span class="contact-item">{{linkedin}}</span>{% endif %}
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">Professional Summary</div>
        <div class="summary">{{summary}}</div>
    </div>
    
    {% if skills %}
    <div class="section">
        <div class="section-title">Core Competencies</div>
        <div class="skills-grid">
            {% for skill in skills %}
            <span class="skill-tag">{{skill}}</span>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    
    {% if experience %}
    <div class="section">
        <div class="section-title">Professional Experience</div>
        {% for exp in experience %}
        <div class="experience-item">
            <div class="exp-header">
                <div>
                    <span class="exp-title">{{exp.title}}</span> | 
                    <span class="exp-company">{{exp.company}}</span>
                </div>
                <span class="exp-date">{{exp.date}}</span>
            </div>
            <div class="exp-description">
                <ul>
                    {% for bullet in exp.bullets %}
                    <li>{{bullet}}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}
    
    <div class="two-column">
        {% if education %}
        <div class="column">
            <div class="section">
                <div class="section-title">Education</div>
                {% for edu in education %}
                <div class="education-item">
                    <div class="edu-degree">{{edu.degree}}</div>
                    <div class="edu-school">{{edu.school}}</div>
                    <div class="edu-year">{{edu.year}}</div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        {% if certifications %}
        <div class="column">
            <div class="section">
                <div class="section-title">Certifications</div>
                <div class="cert-list">
                    {% for cert in certifications %}
                    <span class="cert-item">{{cert}}</span>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

COVER_LETTER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Cover Letter - {{company}}</title>
    <style>
        @page {
            size: A4;
            margin: 2.5cm;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }
        
        .header {
            margin-bottom: 30px;
        }
        
        .sender-info {
            margin-bottom: 20px;
        }
        
        .sender-name {
            font-size: 14pt;
            font-weight: 700;
            color: #1a365d;
        }
        
        .sender-contact {
            font-size: 10pt;
            color: #666;
            margin-top: 5px;
        }
        
        .date {
            margin-bottom: 20px;
            color: #4a5568;
        }
        
        .recipient {
            margin-bottom: 25px;
        }
        
        .salutation {
            margin-bottom: 20px;
        }
        
        .body-text {
            text-align: justify;
            margin-bottom: 15px;
        }
        
        .closing {
            margin-top: 30px;
        }
        
        .signature {
            margin-top: 40px;
            font-weight: 600;
        }
        
        .body-text p {
            margin-bottom: 12px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="sender-info">
            <div class="sender-name">{{name}}</div>
            <div class="sender-contact">
                {% if address %}{{address}}<br>{% endif %}
                {% if phone %}{{phone}}<br>{% endif %}
                {% if email %}{{email}}<br>{% endif %}
                {% if linkedin %}{{linkedin}}{% endif %}
            </div>
        </div>
        
        <div class="date">{{date}}</div>
        
        {% if company %}
        <div class="recipient">
            Hiring Manager<br>
            {{company}}<br>
            {% if company_address %}{{company_address}}{% endif %}
        </div>
        {% endif %}
        
        <div class="salutation">Dear Hiring Manager,</div>
    </div>
    
    <div class="body-text">
        {{body}}
    </div>
    
    <div class="closing">
        <p>Thank you for considering my application. I look forward to discussing how my experience in {{highlight}} can contribute to {% if company %}{{company}}{% endif %}'s continued success.</p>
    </div>
    
    <div class="signature">
        Sincerely,<br><br>
        {{name}}
    </div>
</body>
</html>
"""

class PDFExporter:
    """Export CVs and cover letters as professional PDFs"""
    
    def __init__(self, output_dir: str = "/tmp/pdfs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_cv_pdf(self, cv_data: Dict, filename: str = None) -> str:
        """Generate PDF from CV data using Jinja2"""
        
        # Build HTML from template using Jinja2
        template = Template(CV_TEMPLATE)
        html_content = template.render(**cv_data)
        
        # Generate filename
        if not filename:
            safe_name = cv_data.get('name', 'CV').replace(' ', '_')
            safe_company = cv_data.get('company', 'Generic').replace(' ', '_')
            filename = f"{safe_name}_{safe_company}_CV.pdf"
        
        output_path = os.path.join(self.output_dir, filename)
        
        # Generate PDF
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path
    
    def generate_cover_letter_pdf(self, letter_data: Dict, filename: str = None) -> str:
        """Generate PDF from cover letter data using Jinja2"""
        
        # Build HTML from template using Jinja2
        template = Template(COVER_LETTER_TEMPLATE)
        
        # Format date
        letter_data['date'] = letter_data.get('date', datetime.now().strftime('%B %d, %Y'))
        
        html_content = template.render(**letter_data)
        
        # Generate filename
        if not filename:
            safe_name = letter_data.get('name', 'Cover').replace(' ', '_')
            safe_company = letter_data.get('company', 'Company').replace(' ', '_')
            filename = f"{safe_name}_{safe_company}_Cover_Letter.pdf"
        
        output_path = os.path.join(self.output_dir, filename)
        
        # Generate PDF
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path


# Singleton for easy import
pdf_exporter = PDFExporter()

if __name__ == "__main__":
    # Test generation
    test_cv = {
        "name": "Ahmed Nasr",
        "headline": "VP Healthcare AI & Operations",
        "location": "Dubai, UAE",
        "phone": "+971 50 281 4490",
        "email": "ahmed.nasr@example.com",
        "linkedin": "linkedin.com/in/ahmednasr",
        "summary": "Senior technology executive with 20+ years in operational leadership, specializing in healthcare AI and digital transformation.",
        "skills": ["AI/ML", "Healthcare Operations", "Digital Transformation", "PMO", "PMP", "Agile", "Strategic Planning"],
        "experience": [
            {
                "title": "Chief of PMO",
                "company": "Saudi German Hospital",
                "date": "2022 - Present",
                "location": "Dubai, UAE",
                "bullets": [
                    "Led $25M P&L healthcare transformation initiative",
                    "Achieved 40% efficiency gains through AI implementation"
                ]
            }
        ],
        "education": [
            {
                "degree": "MBA (In Progress)",
                "school": "Business School",
                "year": "Expected 2026"
            },
            {
                "degree": "Bachelor of Commerce",
                "school": "Sadat Academy for Management Sciences",
                "year": "2005"
            }
        ],
        "certifications": ["PMP", "ITIL", "Six Sigma Green Belt", "Prosci Change Management"]
    }
    
    output = pdf_exporter.generate_cv_pdf(test_cv, "test_cv_fixed.pdf")
    print(f"Test CV PDF generated: {output}")
