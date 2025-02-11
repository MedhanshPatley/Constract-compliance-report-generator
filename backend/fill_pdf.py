# import re
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.lib.units import inch
# from reportlab.lib import colors
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont

# # Register a font (replace with your desired font file if needed)
# try:
#     pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
# except Exception as e:
#     print(f"Warning: Could not register Arial font. Using default. Error: {e}")


# def create_contract_pdf(contract_text, output_filename="contract_reportlab.pdf"):
#     """Creates a PDF contract using ReportLab from the contract text."""

#     doc = SimpleDocTemplate(output_filename, pagesize=letter)
#     story = []

#     # Define custom styles (without inheriting from getSampleStyleSheet)
#     title_style = ParagraphStyle(
#         name='TitleStyle',
#         fontSize=14,
#         alignment=1,  # Centered
#         fontName='Arial',
#         spaceAfter=0.2 * inch
#     )

#     normal_style = ParagraphStyle(
#         name='NormalStyle',
#         fontSize=10,
#         leading=12,
#         fontName='Arial',
#         spaceAfter=0.2 * inch
#     )

#     bullet_style = ParagraphStyle(
#         name='BulletStyle',
#         fontSize=10,
#         leading=12,
#         leftIndent=24,
#         bulletIndent=12,
#         fontName='Arial',
#         spaceAfter=0.2 * inch
#     )

#     # Remove extra characters, also fixes the bullet points since bulletPoints often has weird encoding issues.
#     # formatted_contract_text = contract_text.replace("o", "-").replace("▪", "-").replace("•", "-") #if bullet encoding breaks, use this

#     #Added date text fix and also bullet encoding fixes all in one implementation.
#     date_phrase = "THIS CONTRACT is made and entered into as of this"
#     start_index = contract_text.find(date_phrase) #Get starting Index to be used
#     if start_index > -1: # If index exists, remove the underscores.

#         line_end = contract_text[start_index:].find('\n')  # Find the end of the first line for clean
#         if line_end == -1: # if there is no end, use the len so no errors are involved.
#             line_end = len(contract_text) - start_index
#         textWithCleanDates = re.sub(r"_", "", contract_text[start_index: start_index + line_end])  # Clean just date portion, added bullet encoding fixes here
#         bulletEncodingFix = textWithCleanDates.replace("o", "-").replace("▪", "-").replace("•", "-") #Bullet point replace here
#         formatted_contract_text = contract_text[:start_index] + bulletEncodingFix + contract_text[start_index + line_end:] #Rebuild

#     else:
#         # if no "THIS CONTRACT is made and entered into as of this" is found
#         formatted_contract_text = contract_text.replace("o", "-").replace("▪", "-").replace("•", "-")

#     # Split the text into paragraphs
#     paragraphs = formatted_contract_text.split('\n\n')

#     for paragraph in paragraphs:
#         paragraph = paragraph.strip()
#         if paragraph:  # Skip empty paragraphs
#             if paragraph.startswith("ARTICLE") or paragraph.startswith("DEVELOPER-CONTRACTOR AGREEMENT") or \
#                     paragraph.startswith("Developer:") or paragraph.startswith("Contractor:"):
#                 story.append(Paragraph(paragraph, title_style))
#             elif paragraph.startswith("*"):  # simpler way to add Bullet point implementations, remove the previous non-standard implementation as there are too many issues there for type management.
#                 story.append(Paragraph(paragraph.replace("*", "-"), bullet_style))
#             else:
#                 story.append(Paragraph(paragraph, normal_style))
#             #story.append(Spacer(1, 0.2 * inch)) #removing spacer, handled with `spaceAfter` on the styles

#     # Build the PDF
#     doc.build(story)
#     print(f"PDF '{output_filename}' created successfully.")

import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register a font (replace with your desired font file if needed)
try:
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
except Exception as e:
    print(f"Warning: Could not register Arial font. Using default. Error: {e}")

def format_date_line(text):
    """
    Specifically formats the contract date line while preserving the date format.
    Returns the formatted text.
    """
    date_phrase = "THIS CONTRACT is made and entered into"
    if text.startswith(date_phrase):
        # Use a more precise regex to clean up the date line while preserving the date format
        # This will preserve date formatting like "1st of October, 2025"
        cleaned = re.sub(r'(?<=into)\s+(?:as of)?\s*this\s+', ' as of this ', text)
        cleaned = re.sub(r'(?<=\d)(st|nd|rd|th)?(?=\s+(?:day\s+)?of\s+)', 'st', cleaned)  # Ensures proper ordinal
        cleaned = re.sub(r'\s+day\s+of\s+', ' of ', cleaned)  # Cleans up "day of" format
        cleaned = re.sub(r'([A-Za-z]+)[,\s]+(\d{4})', r'\1, \2', cleaned)  # Ensures proper comma before year
        cleaned = re.sub(r"_", "",cleaned)
        # cleaned = re.sub(r"_", "",cleaned)
        return cleaned
    return text

def create_contract_pdf(contract_text, output_filename="contract_reportlab.pdf"):
    """Creates a PDF contract using ReportLab from the contract text with consistent formatting."""
    
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    story = []
    
    # Define styles hierarchy
    styles = {
        'document_title': ParagraphStyle(
            'DocumentTitle',
            fontSize=16,
            leading=20,
            alignment=1,
            fontName='Arial',
            spaceAfter=0.3 * inch,
            spaceBefore=0.2 * inch,
            bold=True
        ),
        'article_title': ParagraphStyle(
            'ArticleTitle',
            fontSize=12,
            leading=16,
            alignment=0,
            fontName='Arial',
            spaceAfter=0.2 * inch,
            spaceBefore=0.2 * inch,
            bold=True
        ),
        'section_title': ParagraphStyle(
            'SectionTitle',
            fontSize=11,
            leading=14,
            alignment=0,
            fontName='Arial',
            spaceAfter=0.15 * inch,
            spaceBefore=0.15 * inch,
            bold=True
        ),
        'normal_text': ParagraphStyle(
            'NormalText',
            fontSize=10,
            leading=14,
            alignment=0,
            fontName='Arial',
            spaceAfter=0.1 * inch
        ),
        'bullet_text': ParagraphStyle(
            'BulletText',
            fontSize=10,
            leading=14,
            leftIndent=24,
            bulletIndent=12,
            fontName='Arial',
            spaceAfter=0.1 * inch
        )
    }

    # Split the text into paragraphs and process each one
    paragraphs = contract_text.split('\n\n')
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # Format date line if this is the contract header
        if paragraph.startswith("THIS CONTRACT"):
            paragraph = format_date_line(paragraph)
            
        # Convert bullet points while preserving the rest of the text
        if paragraph.startswith("*") or paragraph.startswith("-"):
            paragraph = paragraph.replace("*", "•").replace("-", "•")
            style = styles['bullet_text']
        elif "DEVELOPER-CONTRACTOR AGREEMENT" in paragraph:
            style = styles['document_title']
        elif paragraph.startswith("ARTICLE"):
            style = styles['article_title']
        elif paragraph.startswith("Developer:") or paragraph.startswith("Contractor:"):
            style = styles['section_title']
        else:
            style = styles['normal_text']

        story.append(Paragraph(paragraph, style))

    # Build the PDF
    doc.build(story)
    print(f"PDF '{output_filename}' created successfully with consistent formatting.")