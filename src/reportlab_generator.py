#!/usr/bin/env python3
"""
ReportLab-based PDF Generator for CVs
Alternative to WeasyPrint when Cairo is not available
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from typing import Dict, List


class ReportLabCVGenerator:
    """Generate professional PDFs using ReportLab"""
    
    def __init__(self, output_dir: str = "/tmp/pdfs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        
        # Name style
        self.styles.add(ParagraphStyle(
            name='CVName',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor("#1a365d"),
            alignment=TA_CENTER,
            spaceAfter=6
        ))
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='CVTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor("#4a5568"),
            alignment=TA_CENTER,
            spaceAfter=12
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='CVSectionHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor("#1a365d"),
            spaceBefore=12,
            spaceAfter=6,
            borderPadding=3,
            backColor=colors.HexColor("#f7fafc")
        ))
        
        # Experience title style
        self.styles.add(ParagraphStyle(
            name='CVExpTitle',
            parent=self.styles['Heading4'],
            fontSize=11,
            textColor=colors.HexColor("#2d3748"),
            spaceBefore=8,
            spaceAfter=2
        ))
        
        # Company style
        self.styles.add(ParagraphStyle(
            name='CVCompany',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor("#4a5568"),
            spaceAfter=2
        ))
        
        # Date style
        self.styles.add(ParagraphStyle(
            name='CVDate',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor("#718096"),
            fontName='Helvetica-Oblique'
        ))
        
        # Bullet style
        self.styles.add(ParagraphStyle(
            name='CVBullet',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor("#333333"),
            spaceBefore=2,
            spaceAfter=2,
            leftIndent=0.5*cm,
            bulletIndent=0.2*cm
        ))
        
        # Contact style
        self.styles.add(ParagraphStyle(
            name='CVContact',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor("#666666"),
            alignment=TA_CENTER
        ))
    
    def generate_cv(self, profile: Dict, filename: str = None) -> str:
        """Generate CV PDF from profile data"""
        
        if not filename:
            safe_name = profile.get('name', 'CV').replace(' ', '_')
            filename = f"{safe_name}_CV.pdf"
        
        output_path = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        story = []
        
        # Header with name and title
        story.append(Paragraph(profile.get('name', ''), self.styles['CVName']))
        story.append(Paragraph(profile.get('title', ''), self.styles['CVTitle']))
        
        # Contact information
        contact_parts = []
        contact = profile.get('contact', {})
        
        if profile.get('location'):
            contact_parts.append(f"📍 {profile['location']}")
        if contact.get('phone_uae'):
            contact_parts.append(f"📱 UAE: {contact['phone_uae']}")
        if contact.get('phone_egypt'):
            contact_parts.append(f"📱 Egypt: {contact['phone_egypt']}")
        if contact.get('email'):
            contact_parts.append(f"✉️ {contact['email']}")
        if contact.get('linkedin'):
            contact_parts.append(f"🔗 {contact['linkedin']}")
        
        contact_text = " | ".join(contact_parts)
        story.append(Paragraph(contact_text, self.styles['CVContact']))
        story.append(Spacer(1, 12))
        
        # Professional Summary
        if profile.get('summary'):
            story.append(Paragraph("Professional Summary", self.styles['CVSectionHeader']))
            story.append(Paragraph(profile['summary'], self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Core Competencies/Skills
        if profile.get('core_skills'):
            story.append(Paragraph("Core Competencies", self.styles['CVSectionHeader']))
            skills_text = ", ".join(profile['core_skills'].get('technical', [])[:10])
            story.append(Paragraph(skills_text, self.styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Professional Experience
        if profile.get('experience'):
            story.append(Paragraph("Professional Experience", self.styles['CVSectionHeader']))
            
            for exp in profile['experience']:
                # Job title and company
                title_text = f"<b>{exp.get('title', '')}</b> | {exp.get('company', '')}"
                story.append(Paragraph(title_text, self.styles['CVExpTitle']))
                
                # Date and location
                date_text = f"{exp.get('period', '')} | {exp.get('location', '')}"
                story.append(Paragraph(date_text, self.styles['CVDate']))
                
                # Achievements as bullets
                for ach in exp.get('achievements', []):
                    # Clean up the achievement text
                    clean_ach = ach.split(': ', 1)[-1] if ': ' in ach else ach
                    story.append(Paragraph(f"• {clean_ach}", self.styles['CVBullet']))
                
                story.append(Spacer(1, 8))
        
        # Education
        if profile.get('education'):
            story.append(Paragraph("Education", self.styles['CVSectionHeader']))
            
            for edu in profile['education']:
                edu_text = f"<b>{edu.get('degree', '')}</b>"
                if edu.get('field'):
                    edu_text += f" - {edu['field']}"
                story.append(Paragraph(edu_text, self.styles['Normal']))
                
                school_text = f"{edu.get('institution', '')} | {edu.get('year', '')}"
                story.append(Paragraph(school_text, self.styles['CVDate']))
                story.append(Spacer(1, 6))
            
            story.append(Spacer(1, 12))
        
        # Certifications
        if profile.get('certifications'):
            story.append(Paragraph("Certifications", self.styles['CVSectionHeader']))
            
            certs = profile['certifications'][:8]
            certs_text = " | ".join(certs)
            story.append(Paragraph(certs_text, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        return output_path


# Convenience function
def generate_cv_pdf(profile: Dict, filename: str = None) -> str:
    """Generate a CV PDF"""
    generator = ReportLabCVGenerator()
    return generator.generate_cv(profile, filename)


if __name__ == "__main__":
    from cv_optimizer import ProfileDatabase
    
    p = ProfileDatabase()
    output = generate_cv_pdf(p.data, "Ahmed_Nasr_CV.pdf")
    print(f"Generated: {output}")
