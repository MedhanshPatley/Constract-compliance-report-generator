from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # Added getSampleStyleSheet here
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime  # Also added datetime for timestamps

def create_compliance_report_pdf(compliance_report_text, output_filename="compliance_report.pdf"):
    """Generates a PDF compliance report using ReportLab."""
    
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    story = []
    
    # Get the default styles
    styles = getSampleStyleSheet()
    
    # Define custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#2C3E50')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceBefore=6,
        spaceAfter=12
    )

    # Add title
    story.append(Paragraph("Contract Compliance Report", title_style))
    story.append(Spacer(1, 20))

    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"Generated on: {timestamp}", normal_style))
    story.append(Spacer(1, 20))

    # Process the compliance report text
    sections = compliance_report_text.split('\n\n')
    for section in sections:
        if section.strip().startswith("Clause Description:"):
            # Format clause descriptions as headings
            story.append(Paragraph(section.strip(), heading_style))
        else:
            # Format analysis text with proper paragraph styling
            paragraphs = section.split('\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), normal_style))

    # Build the PDF
    try:
        doc.build(story)
        print(f"Compliance report PDF '{output_filename}' created successfully.")
    except Exception as e:
        print(f"Error building PDF: {e}")
        raise

if __name__ == "__main__":
    sample_text = """
    Clause Description: Commencement and Term (Article I)

    This clause outlines the start date and duration of the contract. 
    The clause is compliant with standard contract practices.

    Clause Description: Scope of Work (Article II)

    This section defines the tasks, deliverables, and responsibilities.
    The scope of work aligns with industry best practices.
    """
    create_compliance_report_pdf(sample_text)