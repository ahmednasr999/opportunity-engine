"""
CV PDF Generator - Create professional PDF resumes
"""
import os
from datetime import datetime
from typing import Dict, Any

class CVPDFGenerator:
    """Generate professional PDF CVs from tailored CV data"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or os.path.join(
            os.path.dirname(__file__), '..', 'output'
        )
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_html_cv(self, cv_data: Dict[str, Any], filename: str = None) -> str:
        """Generate a professional HTML CV that can be printed to PDF"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"CV_Ahmed_Nasr_{timestamp}.html"
        
        filepath = os.path.join(self.output_dir, filename)
        
        html_content = self._create_html_template(cv_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def _create_html_template(self, cv_data: Dict[str, Any]) -> str:
        """Create professional HTML CV template"""
        
        sections = cv_data.get('sections', [])
        ats_score = cv_data.get('ats_score', 0)
        job_title = cv_data.get('target_title', 'Executive Position')
        company = cv_data.get('target_company', 'Target Company')
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahmed Nasr - {job_title}</title>
    <style>
        @page {{
            size: A4;
            margin: 15mm;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.4;
            color: #333;
            background: white;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 15px;
            margin-bottom: 20px;
        }}
        
        .name {{
            font-size: 24pt;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 5px;
        }}
        
        .title {{
            font-size: 14pt;
            color: #2563eb;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        
        .contact {{
            font-size: 9pt;
            color: #666;
        }}
        
        .contact span {{
            margin: 0 10px;
        }}
        
        .section {{
            margin-bottom: 18px;
        }}
        
        .section-title {{
            font-size: 11pt;
            font-weight: 700;
            color: #1a1a1a;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
            margin-bottom: 10px;
        }}
        
        .job {{
            margin-bottom: 12px;
        }}
        
        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 3px;
        }}
        
        .job-title {{
            font-weight: 700;
            font-size: 10.5pt;
            color: #1a1a1a;
        }}
        
        .job-date {{
            font-size: 9pt;
            color: #666;
            font-style: italic;
        }}
        
        .company {{
            font-weight: 600;
            color: #2563eb;
            font-size: 10pt;
            margin-bottom: 5px;
        }}
        
        .job-description {{
            font-size: 9.5pt;
            color: #444;
            text-align: justify;
        }}
        
        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }}
        
        .skill-item {{
            font-size: 9pt;
            padding: 4px 8px;
            background: #f3f4f6;
            border-radius: 3px;
            text-align: center;
        }}
        
        .summary {{
            font-size: 10pt;
            color: #444;
            text-align: justify;
            line-height: 1.5;
        }}
        
        .highlight {{
            background: #fef3c7;
            padding: 2px 4px;
            border-radius: 2px;
        }}
        
        .ats-score {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: {"#dcfce7" if ats_score >= 90 else "#fef3c7"};
            color: {"#166534" if ats_score >= 90 else "#92400e"};
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 9pt;
            font-weight: 600;
        }}
        
        @media print {{
            body {{
                padding: 0;
            }}
            .no-print {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="ats-score no-print">ATS Score: {ats_score}/100</div>
    
    <div class="header">
        <div class="name">Ahmed Nasr</div>
        <div class="title">{job_title}</div>
        <div class="contact">
            <span>📧 ahmed.nasr@email.com</span>
            <span>📱 +1 (555) 123-4567</span>
            <span>💼 linkedin.com/in/ahmednasr</span>
            <span>🌐 ahmednasr.com</span>
        </div>
    </div>
'''
        
        # Add sections
        for section in sections:
            section_type = section.get('type', 'text')
            title = section.get('title', '')
            content = section.get('content', '')
            
            html += f'    <div class="section">\n'
            html += f'        <div class="section-title">{title}</div>\n'
            
            if section_type == 'summary':
                html += f'        <div class="summary">{content}</div>\n'
            
            elif section_type == 'experience':
                jobs = section.get('jobs', [])
                for job in jobs:
                    html += self._format_job_html(job)
            
            elif section_type == 'skills':
                skills = section.get('skills', [])
                html += '        <div class="skills-grid">\n'
                for skill in skills:
                    html += f'            <div class="skill-item">{skill}</div>\n'
                html += '        </div>\n'
            
            else:
                html += f'        <div>{content}</div>\n'
            
            html += '    </div>\n'
        
        html += '''</body>
</html>'''
        
        return html
    
    def _format_job_html(self, job: Dict) -> str:
        """Format a job entry as HTML"""
        title = job.get('title', '')
        company = job.get('company', '')
        dates = job.get('dates', '')
        description = job.get('description', '')
        
        return f'''
        <div class="job">
            <div class="job-header">
                <span class="job-title">{title}</span>
                <span class="job-date">{dates}</span>
            </div>
            <div class="company">{company}</div>
            <div class="job-description">{description}</div>
        </div>
'''
    
    def generate_pdf(self, cv_data: Dict[str, Any], filename: str = None) -> str:
        """Generate PDF using browser print-to-PDF capability"""
        # Generate HTML first
        html_path = self.generate_html_cv(cv_data, filename)
        
        # Return just the filename (not full path) for URL construction
        return os.path.basename(html_path)
