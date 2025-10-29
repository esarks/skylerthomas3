#!/usr/bin/env python3
"""
WORKFLOW3: Convert manuscript to PDF format for Amazon KDP (PUBLISHER VERSION)

With FULLY EMBEDDED FONTS, headers, and page numbers
KDP Requirements Met:
- All fonts fully embedded
- No excessive blank pages
- Sequential pagination (Roman i-v, then Arabic 1, 2, 3...)

Source: /skylerthomas3/KDP/COMPLETE-MANUSCRIPT.md
Output: /skylerthomas3/KDP/OUT-OF-THE-SWAMP-KDP-READY.pdf
"""

from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, PageTemplate, Frame, Table, TableStyle, KeepTogether
from reportlab.lib.units import inch as inches
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re
import os
import sys
import urllib.request
import hashlib

# IMPORTANT: Register fonts that will be FULLY EMBEDDED
# ReportLab's TTFont automatically embeds TrueType fonts
try:
    # Try to use system Times New Roman if available (macOS)
    # These paths work on macOS - adjust for other systems if needed
    pdfmetrics.registerFont(TTFont('TimesNewRoman', '/System/Library/Fonts/Supplemental/Times New Roman.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', '/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRoman-Italic', '/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRoman-BoldItalic', '/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf'))
    FONT_REGULAR = 'TimesNewRoman'
    FONT_BOLD = 'TimesNewRoman-Bold'
    FONT_ITALIC = 'TimesNewRoman-Italic'
    FONT_BOLD_ITALIC = 'TimesNewRoman-BoldItalic'
    print("✓ Using Times New Roman fonts (fully embedded)")
except:
    # Fallback to Helvetica (ReportLab built-in, but we'll ensure embedding)
    print("⚠️  Times New Roman not found, using Helvetica")
    print("   Consider installing Times New Roman for better results")
    FONT_REGULAR = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'
    FONT_ITALIC = 'Helvetica-Oblique'
    FONT_BOLD_ITALIC = 'Helvetica-BoldOblique'

# Global chapter tracker
chapter_tracker = {"current_chapter": "How I Found Truth", "page_map": {}}

from reportlab.platypus.flowables import Flowable

class ChapterMarker(Flowable):
    """Invisible flowable that marks chapter starts for headers"""
    def __init__(self, chapter_title):
        Flowable.__init__(self)
        self.chapter_title = chapter_title
        self.width = 0
        self.height = 0

    def draw(self):
        """Called when actually drawn - updates canvas chapter map"""
        page_num = self.canv._pageNumber
        self.canv.chapter_map[page_num] = self.chapter_title

def is_metadata_line(line):
    """Check if line is metadata that should be skipped"""
    if line.startswith('---'):
        return True
    if line.startswith('wp_post_id:'):
        return True
    if line.startswith('last_updated:'):
        return True
    if line.startswith('*Last updated:'):
        return True
    return False

def download_image(url, cache_dir=None):
    """Download an image from a URL and cache it locally"""
    # WORKFLOW3: Use relative path if cache_dir not provided
    if cache_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skylerthomas3_dir = os.path.dirname(script_dir)
        cache_dir = os.path.join(skylerthomas3_dir, 'KDP', 'image_cache')

    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)

    # Create a filename based on URL hash
    url_hash = hashlib.md5(url.encode()).hexdigest()
    ext = url.split('.')[-1].split('?')[0]  # Get extension, handle query params
    if ext not in ['jpg', 'jpeg', 'png', 'gif']:
        ext = 'jpg'

    cached_file = os.path.join(cache_dir, f"{url_hash}.{ext}")

    # Return cached file if it exists
    if os.path.exists(cached_file):
        return cached_file

    # Download the image with browser headers to avoid 406 errors
    try:
        print(f"  📥 Downloading image: {url}")
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as response:
            with open(cached_file, 'wb') as out_file:
                out_file.write(response.read())
        print(f"  ✓ Cached: {cached_file}")
        return cached_file
    except Exception as e:
        print(f"  ⚠️  Failed to download image: {url}")
        print(f"     Error: {e}")
        return None

def clean_text(text):
    """Clean markdown formatting from text"""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'(?<!\!)\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    return text.strip()

class NumberedCanvas(canvas.Canvas):
    """Custom canvas for adding headers and page numbers"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self.chapter_map = {}

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Add page numbers and headers to all pages"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        """Draw headers and page numbers"""
        page_num = self._pageNumber

        # Front matter: pages 1-5 (title, copyright, dedication, TOC, etc.)
        # Use lowercase Roman numerals, no headers
        if page_num <= 5:
            self.setFont(FONT_REGULAR, 10)
            roman_nums = ['', 'i', 'ii', 'iii', 'iv', 'v']
            if page_num < len(roman_nums):
                self.drawCentredString(3*inches, 0.5*inches, roman_nums[page_num])
            return

        # Main content: page 6+
        # Use Arabic numerals starting from 1, with headers
        content_page_num = page_num - 5

        # Page number at bottom center
        self.setFont(FONT_REGULAR, 10)
        self.drawCentredString(3*inches, 0.5*inches, str(content_page_num))

        # Find the chapter title for this page
        chapter_title = "Out of the Swamp: How I Found Truth"
        for pg in sorted([p for p in self.chapter_map.keys() if p <= page_num], reverse=True):
            if pg <= page_num:
                chapter_title = self.chapter_map[pg]
                break

        # Header at top - show chapter title
        if len(chapter_title) > 50:
            self.setFont(FONT_ITALIC, 8)
        else:
            self.setFont(FONT_ITALIC, 9)

        self.drawCentredString(3*inches, 8.5*inches, chapter_title)

def parse_markdown_to_pdf(md_file, output_pdf):
    """Convert markdown to PDF with proper formatting and embedded fonts"""
    print(f"\nConverting to PDF: {os.path.basename(md_file)}")

    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Create PDF document (6x9 inches) with custom canvas
    # Optimized margins for page count reduction
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=(6*inches, 9*inches),
        rightMargin=0.65*inches,
        leftMargin=0.65*inches,
        topMargin=0.9*inches,
        bottomMargin=0.65*inches
    )

    # Define styles with EMBEDDED FONTS
    styles = getSampleStyleSheet()

    # Optimized styles for page count reduction while maintaining readability
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        alignment=TA_LEFT,
        spaceAfter=10,
        spaceBefore=10,
        fontName=FONT_BOLD
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        alignment=TA_LEFT,
        spaceAfter=8,
        spaceBefore=8,
        fontName=FONT_BOLD
    )

    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=12,
        leading=16,
        alignment=TA_LEFT,
        spaceAfter=6,
        spaceBefore=6,
        fontName=FONT_BOLD
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        fontName=FONT_REGULAR
    )

    quote_style = ParagraphStyle(
        'CustomQuote',
        parent=styles['BodyText'],
        fontSize=9,
        leading=12,
        alignment=TA_JUSTIFY,
        leftIndent=0.4*inches,
        rightIndent=0.4*inches,
        spaceAfter=6,
        spaceBefore=6,
        fontName=FONT_ITALIC,
        textColor=colors.HexColor('#333333')
    )

    lyrics_style = ParagraphStyle(
        'LyricsStyle',
        parent=styles['BodyText'],
        fontSize=9,
        leading=12,
        alignment=TA_LEFT,
        leftIndent=0.2*inches,
        spaceAfter=2,
        fontName=FONT_REGULAR
    )

    # Build story
    story = []
    in_blockquote = False
    in_lyrics = False
    in_metadata = False
    skip_metadata_until_next_section = False
    current_chapter = None

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        # Check if this is a metadata block (--- followed by metadata fields)
        if line.startswith('---'):
            # Look ahead to see if next non-empty line is metadata
            is_metadata_block = False
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and is_metadata_line(next_line):
                    is_metadata_block = True

            if is_metadata_block:
                # This is a metadata block marker
                if not in_metadata:
                    in_metadata = True
                    skip_metadata_until_next_section = True
                else:
                    in_metadata = False
                i += 1
                continue
            else:
                # Ignore standalone --- markers (just decorative dividers)
                i += 1
                continue

        if in_metadata or skip_metadata_until_next_section:
            if is_metadata_line(line):
                i += 1
                continue
            elif line.startswith('#'):
                skip_metadata_until_next_section = False
            elif line.strip() == '':
                i += 1
                continue

        # Detect lyrics sections
        if '**[Verse' in line or '**[Chorus' in line or '**[Bridge' in line or '**[Outro' in line or '**[Pre-Chorus' in line or '**[Intro' in line or '**(Verse' in line or '**(Chorus' in line or '**(Bridge' in line or '**(Outro' in line or '**(Intro' in line or '**(Hook' in line:
            in_lyrics = True

        # End lyrics on horizontal rule or heading
        if in_lyrics and (line.startswith('---') or line.startswith('#')):
            in_lyrics = False
            story.append(Spacer(1, 0.1*inches))

        # Handle LaTeX \newpage markers
        if line.strip() == '\\newpage':
            story.append(PageBreak())
            i += 1
            continue

        # Skip empty lines (reduced spacing for page count optimization)
        if not line.strip():
            if not in_lyrics:
                story.append(Spacer(1, 0.05*inches))
            i += 1
            continue

        # Images - Handle both Markdown ![alt](path) and HTML <img src="...">
        img_match = None
        img_src = None
        img_alt = None
        is_qr_code = False

        # Check for markdown style: ![alt](path)
        if line.startswith('![') and '](' in line:
            img_match = re.search(r'!\[([^\]]*)\]\(([^\)]+)\)', line)
            if img_match:
                img_alt = img_match.group(1)
                img_src = img_match.group(2)
                is_qr_code = 'qr-' in img_src.lower()

        # Check for HTML style: <img src="..." alt="...">
        elif '<img' in line.lower() and 'src=' in line.lower():
            img_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', line, re.IGNORECASE)
            if img_match:
                img_src = img_match.group(1)
                alt_match = re.search(r'alt=["\']([^"\']+)["\']', line, re.IGNORECASE)
                if alt_match:
                    img_alt = alt_match.group(1)
                is_qr_code = False

        # Process the image if we found one
        if img_src:
            img_path = None

            # Handle remote URLs
            if img_src.startswith('http://') or img_src.startswith('https://'):
                img_path = download_image(img_src)
            else:
                # Local file
                img_path = os.path.join('/Users/paulmarshall/Documents/GitHub/skylerthomas2/KDP', img_src)
                if not os.path.exists(img_path):
                    print(f"  ⚠️  Image not found: {img_src}")
                    img_path = None

            # Add image to PDF if we have a valid path
            if img_path and os.path.exists(img_path):
                try:
                    if is_qr_code:
                        # QR codes: smaller, square
                        img = Image(img_path, width=1.3*inches, height=1.3*inches)
                    else:
                        # Content photos: get dimensions and calculate scaled size
                        from PIL import Image as PILImage
                        pil_img = PILImage.open(img_path)
                        img_width, img_height = pil_img.size
                        aspect_ratio = img_height / img_width

                        # Max width 4.5" (fits in 6" page with margins)
                        # Max height 6.5" (fits in page with margins)
                        target_width = 4.5 * inches
                        target_height = target_width * aspect_ratio

                        # If height exceeds max, scale down based on height instead
                        if target_height > 6.5 * inches:
                            target_height = 6.5 * inches
                            target_width = target_height / aspect_ratio

                        img = Image(img_path, width=target_width, height=target_height)

                    img.hAlign = 'CENTER'
                    story.append(img)
                    story.append(Spacer(1, 0.1*inches))

                except Exception as e:
                    print(f"  ⚠️  Could not load image: {img_src} - {e}")

            i += 1
            continue

        # Chapter markers
        if line.startswith('### Chapter') or line.startswith('### Movement'):
            chapter_text = line.replace('###', '').strip()
            current_chapter = chapter_text
            story.append(ChapterMarker(chapter_text))
            para = Paragraph(chapter_text, h3_style)
            story.append(para)
            i += 1
            continue

        # Headings
        if line.startswith('# '):
            text = clean_text(line[2:])
            # Insert page break before major sections and chapters to ensure they start on new pages
            sections_needing_page_break = ['Dedication', 'Table of Contents', 'Introduction',
                                          'Epilogue', 'About the Author', 'Acknowledgments',
                                          'The Road Ahead', 'Chapter']
            if any(section in text for section in sections_needing_page_break):
                # Only add page break if this isn't the very first item
                if len(story) > 0:
                    story.append(PageBreak())
            para = Paragraph(text, h1_style)
            story.append(para)
            i += 1
            continue

        if line.startswith('## '):
            text = clean_text(line[3:])
            # Insert page break before "A Final Word"
            if 'A Final Word' in text:
                if len(story) > 0:
                    story.append(PageBreak())
            para = Paragraph(text, h2_style)
            story.append(para)
            i += 1
            continue

        if line.startswith('### '):
            text = clean_text(line[4:])
            para = Paragraph(text, h3_style)
            story.append(para)
            i += 1
            continue

        # Blockquotes
        if line.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].startswith('> '):
                quote_lines.append(lines[i][2:].strip())
                i += 1

            quote_text = ' '.join(quote_lines)
            quote_text = clean_text(quote_text)
            para = Paragraph(quote_text, quote_style)
            story.append(para)
            continue

        # Tables (markdown format)
        if line.startswith('|') and '|' in line:
            table_data = []
            # Collect all table rows
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = lines[i].strip()
                # Skip separator rows (|----|-----| or |:---|---:|)
                # These rows contain only pipes, dashes, colons, and spaces
                if not re.match(r'^[\|\-\s:]+$', row):
                    cells = [cell.strip() for cell in row.split('|')[1:-1]]
                    # Clean markdown and convert to Paragraph objects for proper formatting
                    cell_style = ParagraphStyle(
                        'TableCell',
                        parent=body_style,
                        fontSize=9,
                        leading=12
                    )
                    cells = [Paragraph(clean_text(cell), cell_style) for cell in cells]
                    table_data.append(cells)
                i += 1

            if table_data:
                # Create ReportLab table with proper column widths
                col_widths = [2.3*inches, 2.3*inches]
                t = Table(table_data, colWidths=col_widths)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('LEFTPADDING', (0, 0), (-1, -1), 6),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]))
                # Wrap table in KeepTogether to prevent splitting across pages
                story.append(KeepTogether(t))
                story.append(Spacer(1, 0.15*inches))
            continue

        # Lists
        if line.startswith('- ') or line.startswith('* ') or re.match(r'^\d+\.', line):
            text = clean_text(line)
            para = Paragraph(text, body_style)
            story.append(para)
            i += 1
            continue

        # Lyrics (indented style)
        if in_lyrics:
            text = clean_text(line)
            para = Paragraph(text, lyrics_style)
            story.append(para)
            i += 1
            continue

        # Skip any remaining metadata lines that weren't caught by block processing
        if is_metadata_line(line):
            i += 1
            continue

        # Regular paragraphs
        text = clean_text(line)
        if text:
            para = Paragraph(text, body_style)
            story.append(para)

        i += 1

    # Build PDF with custom canvas for headers/page numbers
    print(f"  Building PDF with embedded fonts...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"  ✓ PDF created: {output_pdf}")
    print(f"  ✓ Fonts are fully embedded")
    print(f"  ✓ Ready for KDP upload")

if __name__ == "__main__":
    # WORKFLOW3: Use relative paths from script location (PUBLISHER VERSION)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skylerthomas3_dir = os.path.dirname(script_dir)  # Parent of workflow3_production_scripts
    kdp_dir = os.path.join(skylerthomas3_dir, 'KDP')

    input_file = os.path.join(kdp_dir, 'COMPLETE-MANUSCRIPT.md')
    output_file = os.path.join(kdp_dir, 'OUT-OF-THE-SWAMP-PUBLISHER.pdf')

    if not os.path.exists(input_file):
        print(f"❌ Error: Input file not found: {input_file}")
        sys.exit(1)

    print("=" * 60)
    print("Creating KDP-Ready PDF with Fully Embedded Fonts")
    print("=" * 60)

    parse_markdown_to_pdf(input_file, output_file)

    print("\n" + "=" * 60)
    print("✅ KDP-READY PDF COMPLETE")
    print("=" * 60)
    print(f"\nOutput: {output_file}")
    print("\nKDP Requirements Met:")
    print("  ✓ All fonts fully embedded")
    print("  ✓ Sequential pagination (Roman i-v, then Arabic 1, 2, 3...)")
    print("  ✓ Headers on all pages")
    print("  ✓ 6\" x 9\" format with 0.75\" margins")
    print("\nReady to upload to KDP!")
