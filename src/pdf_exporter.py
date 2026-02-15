#!/usr/bin/env python3
"""
PDF Export System - Generate professional PDFs from CVs and cover letters
Uses WeasyPrint for HTML-to-PDF conversion
"""

import os
from datetime import datetime
from typing import Dict, Optional
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

# Professional CV Template with modern styling
CV_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{name}} - {{title}}</title>
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
        
        .ats-score {
            position: absolute;
            top: 20px;
            right: 20px;
            background: #1a365d;
            color: white;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 9pt;
            font-weight: 600;
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
            <span class="contact-item">{{location}}</span>
            <span class="contact-item">{{phone}}</span>
            <span class="contact-item">{{email}}</span>
            <span class="contact-item">{{linkedin}}</span>
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">Professional Summary</div>
        <div class="summary">{{summary}}</div>
    </div>
    
    <div class="section">
        <div class="section-title">Core Competencies</div>
        <div class="skills-grid">
            {{#each skills}}
            <span class="skill-tag">{{this}}</span>
            {{/each}}
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">Professional Experience</div>
        {{#each experience}}
        <div class="experience-item">
            <div class="exp-header">
                <div>
                    <span class="exp-title">{{title}}</span> | 
                    <span class="exp-company">{{company}}</span>
                </div>
                <span class="exp-date">{{date}}</span>
            </div>
            <div class="exp-location">{{location}}</div>
            <div class="exp-description">
                <ul>
                    {{#each bullets}}
                    <li>{{this}}</li>
                    {{/each}}
                </ul>
            </div>
        </div>
        {{/each}}
    </div>
    
    <div class="two-column">
        <div class="column">
            <div class="section">
                <div class="section-title">Education</div>
                {{#each education}}
                <div class="education-item">
                    <div class="edu-degree">{{degree}}</div>
                    <div class="edu-school">{{school}}</div>
                    <div class="edu-year">{{year}}</div>
                </div>
                {{/each}}
            </div>
        </div>
        
        <div class="column">
            <div class="section">
                <div class="section-title">Certifications</div>
                <div class="cert-list">
                    {{#each certifications}}
                    <span class="cert-item">{{this}}</span>
                    {{/each}}
                </div>
            </div>
        </div>
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
    </style>
</head>
<body>
    <div class="header">
        <div class="sender-info">
            <div class="sender-name">{{name}}</div>
            <div class="sender-contact">
                {{address}}<br>
                {{phone}} | {{email}}<br>
                {{linkedin}}
            </div>
        </div>
        
        <div class="date">{{date}}</div>
        
        <div class="recipient">
            Hiring Manager<br>
            {{company}}<br>
            {{company_address}}
        </div>
        
        <div class="salutation">Dear Hiring Manager,</div>
    </div>
    
    <div class="body-text">{{body}}</div>
    
    <div class="closing">
        <p>Thank you for considering my application. I look forward to discussing how my experience in {{highlight}} can contribute to {{company}}'s continued success.</p>
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
        """Generate PDF from CV data"""
        
        # Build HTML from template
        html_content = self._build_cv_html(cv_data)
        
        # Generate filename
        if not filename:
            safe_name = cv_data.get('name', 'CV').replace(' ', '_')
            safe_company = cv_data.get('target_company', 'Generic').replace(' ', '_')
            filename = f"{safe_name}_{safe_company}_CV.pdf"
        
        output_path = os.path.join(self.output_dir, filename)
        
        # Generate PDF
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path
    
    def generate_cover_letter_pdf(self, letter_data: Dict, filename: str = None) -> str:
        """Generate PDF from cover letter data"""
        
        # Build HTML from template
        html_content = self._build_cover_letter_html(letter_data)
        
        # Generate filename
        if not filename:
            safe_name = letter_data.get('name', 'Cover').replace(' ', '_')
            safe_company = letter_data.get('company', 'Company').replace(' ', '_')
            filename = f"{safe_name}_{safe_company}_Cover_Letter.pdf"
        
        output_path = os.path.join(self.output_dir, filename)
        
        # Generate PDF
        HTML(string=html_content).write_pdf(output_path)
        
        return output_path
    
    def _build_cv_html(self, data: Dict) -> str:
        """Build CV HTML from template"""
        
        # Simple template substitution (not using Handlebars for simplicity)
        html = CV_TEMPLATE
        
        # Replace basic fields
        html = html.replace('{{name}}', data.get('name', 'Your Name'))
        html = html.replace('{{headline}}', data.get('headline', 'Professional Title'))
        html = html.replace('{{location}}', data.get('location', 'City, Country'))
        html = html.replace('{{phone}}', data.get('phone', ''))
        html = html.replace('{{email}}', data.get('email', ''))
        html = html.replace('{{linkedin}}', data.get('linkedin', ''))
        html = html.replace('{{summary}}', data.get('summary', ''))
        
        # Replace skills
        skills = data.get('skills', [])
        skills_html = '\n'.join([f'<span class="skill-tag">{skill}</span>' for skill in skills])
        # Simple handlebars replacement
        html = self._replace_section(html, '{{#each skills}}', '{{/each}}', skills_html)
        
        # Replace experience
        experience = data.get('experience', [])
        exp_html = ''
        for exp in experience:
            exp_html += f'''
            <div class="experience-item">
                <div class="exp-header">
                    <div>
                        <span class="exp-title">{exp.get('title', '')}</span> | 
                        <span class="exp-company">{exp.get('company', '')}</span>
                    </div>
                    <span class="exp-date">{exp.get('date', '')}</span>
                </div>
                <div class="exp-location">{exp.get('location', '')}</div>
                <div class="exp-description">
                    <ul>
                        {''.join([f'<li>{b}</li>' for b in exp.get('bullets', [])])}
                    </ul>
                </div>
            </div>
            '''
        html = self._replace_section(html, '{{#each experience}}', '{{/each}}', exp_html)
        
        # Replace education
        education = data.get('education', [])
        edu_html = ''
        for edu in education:
            edu_html += f'''
            <div class="education-item">
                <div class="edu-degree">{edu.get('degree', '')}</div>
                <div class="edu-school">{edu.get('school', '')}</div>
                <div class="edu-year">{edu.get('year', '')}</div>
            </div>
            '''
        html = self._replace_section(html, '{{#each education}}', '{{/each}}', edu_html)
        
        # Replace certifications
        certs = data.get('certifications', [])
        certs_html = '\n'.join([f'<span class="cert-item">{cert}</span>' for cert in certs])
        html = self._replace_section(html, '{{#each certifications}}', '{{/each}}', certs_html)
        
        return html
    
    def _build_cover_letter_html(self, data: Dict) -> str:
        """Build cover letter HTML from template"""
        
        html = COVER_LETTER_TEMPLATE
        
        html = html.replace('{{name}}', data.get('name', 'Your Name'))
        html = html.replace('{{address}}', data.get('address', ''))
        html = html.replace('{{phone}}', data.get('phone', ''))
        html = html.replace('{{email}}', data.get('email', ''))
        html = html.replace('{{linkedin}}', data.get('linkedin', ''))
        html = html.replace('{{date}}', data.get('date', datetime.now().strftime('%B %d, %Y')))
        html = html.replace('{{company}}', data.get('company', 'Company Name'))
        html = html.replace('{{company_address}}', data.get('company_address', ''))
        html = html.replace('{{body}}', data.get('body', '').replace('\n', '</p><p class="body-text">'))
        html = html.replace('{{highlight}}', data.get('highlight', 'healthcare operations'))
        
        return html
    
    def _replace_section(self, html: str, start_tag: str, end_tag: str, content: str) -> str:
        """Replace a template section with content"""
        start_idx = html.find(start_tag)
        end_idx = html.find(end_tag)
        
        if start_idx != -1 and end_idx != -1:
            return html[:start_idx] + content + html[end_idx + len(end_tag):]
        return html


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
    
    output = pdf_exporter.generate_cv_pdf(test_cv, "test_cv.pdf")
    print(f"Test CV PDF generated: {output}")
