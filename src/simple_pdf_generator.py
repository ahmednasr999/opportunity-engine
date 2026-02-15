#!/usr/bin/env python3
"""
Simple PDF Generator for CVs
Generates PDFs with proper text embedding
"""

import os
from typing import Dict, List


class SimpleCVPDFGenerator:
    """Generate simple but effective CV PDFs"""
    
    def __init__(self, output_dir: str = "/tmp/pdfs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def _escape_pdf_text(self, text: str) -> str:
        """Escape special characters for PDF"""
        return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
    
    def _generate_font_dict(self) -> str:
        """Generate font dictionary"""
        return """5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj"""
    
    def generate_cv(self, profile: Dict, filename: str = None) -> str:
        """Generate CV PDF from profile data"""
        
        if not filename:
            safe_name = profile.get('name', 'CV').replace(' ', '_')
            filename = f"{safe_name}_CV.pdf"
        
        output_path = os.path.join(self.output_dir, filename)
        
        # Build content
        name = self._escape_pdf_text(profile.get('name', ''))
        title = self._escape_pdf_text(profile.get('title', ''))
        
        # Contact info
        contact = profile.get('contact', {})
        contact_parts = []
        if profile.get('location'):
            contact_parts.append(profile['location'])
        if contact.get('phone_uae'):
            contact_parts.append(f"UAE: {contact['phone_uae']}")
        if contact.get('phone_egypt'):
            contact_parts.append(f"Egypt: {contact['phone_egypt']}")
        if contact.get('email'):
            contact_parts.append(contact['email'])
        if contact.get('linkedin'):
            contact_parts.append(contact['linkedin'])
        
        contact_text = " | ".join(contact_parts)
        
        # Summary
        summary = self._escape_pdf_text(profile.get('summary', ''))
        
        # Build content stream
        content_stream = f"""BT
/F1 24 Tf
306 700 Td
({name}) Tj
0 -8 Td
/F1 14 Tf
({title}) Tj
0 -15 Td
/F1 10 Tf
({contact_text}) Tj
0 -30 Td
/F1 12 Tf
(PROFESSIONAL SUMMARY) Tj
0 -15 Td
/F1 10 Tf
({summary[:200]}) Tj
"""
        
        y_pos = 520
        
        # Experience
        for exp in profile.get('experience', []):
            if y_pos < 100:
                # New page
                content_stream += """ET
endstream
endobj
6 0 obj << /Length 50 >> stream BT /F1 10 Tf 50 750 Td (Page 2) Tj ET endstream endobj
7 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 8 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
8 0 obj << /Length 50 >> stream BT /F1 10 Tf 50 750 Td (Page 2) Tj ET endstream endobj
"""
                y_pos = 720
            
            exp_title = self._escape_pdf_text(exp.get('title', ''))
            exp_company = self._escape_pdf_text(exp.get('company', ''))
            exp_period = self._escape_pdf_text(exp.get('period', ''))
            
            content_stream += f"""0 -20 Td
/F1 12 Tf
({exp_title} | {exp_company}) Tj
0 -12 Td
/F1 10 Tf
({exp_period}) Tj
"""
            y_pos -= 40
            
            # Achievements
            for ach in exp.get('achievements', [])[:3]:
                clean_ach = ach.split(': ', 1)[-1] if ': ' in ach else ach
                clean_ach = self._escape_pdf_text(clean_ach[:80])
                content_stream += f"""0 -12 Td
/F1 10 Tf
(bullet {clean_ach}) Tj
"""
                y_pos -= 15
            
            y_pos -= 10
        
        # Education
        content_stream += """0 -20 Td
/F1 12 Tf
(EDUCATION) Tj
"""
        y_pos -= 25
        
        for edu in profile.get('education', []):
            degree = self._escape_pdf_text(edu.get('degree', ''))
            institution = self._escape_pdf_text(edu.get('institution', ''))
            year = self._escape_pdf_text(edu.get('year', ''))
            
            content_stream += f"""0 -15 Td
/F1 10 Tf
({degree} - {institution}, {year}) Tj
"""
        
        content_stream += "ET"
        
        # Build complete PDF
        pdf = f"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj
4 0 obj << /Length {len(content_stream)} >> stream
{content_stream}
endstream
endobj
{self._generate_font_dict()}
xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000266 00000 n 
0000000558 00000 n 
trailer << /Size 6 /Root 1 0 R >>
startxref
%%EOF"""
        
        with open(output_path, 'w') as f:
            f.write(pdf)
        
        return output_path


def generate_cv_pdf(profile: Dict, filename: str = None) -> str:
    """Generate CV PDF"""
    generator = SimpleCVPDFGenerator()
    return generator.generate_cv(profile, filename)
