# KDP Build Guide
## Technical Documentation for PDF & EPUB Generation

**Last Updated:** October 23, 2025

---

## Overview

This directory contains scripts to generate Amazon KDP (Kindle Direct Publishing) ready files from markdown source files.

**One-Command Build:**
```bash
python3 generate_all.py
```

**Output:**
- `COMPLETE-MANUSCRIPT.md` - Assembled manuscript
- `OUT-OF-THE-SWAMP-PUBLISHER.pdf` - KDP-ready PDF (6×9")
- `OUT-OF-THE-SWAMP-PUBLISHER.epub` - EPUB3 digital edition

---

## Build Pipeline

### Stage 1: Manuscript Assembly

**Script:** `assemble_manuscript.py`

**Source Files:** 21 REVISED-*.md files from `skylerthomas3.wiki/`

**Process:**
1. Reads files in predefined order
2. Removes all WordPress metadata
3. Adds `\pagebreak` between sections
4. Combines into single markdown file

**Output:** `COMPLETE-MANUSCRIPT.md`

**Metadata Removed:**
- YAML blocks (`---` ... `---`) containing WordPress metadata
- `wp_post_id:` lines
- `last_updated:` lines
- `*Last updated:*` lines

**Metadata Preserved:**
- Decorative `---` dividers (outside YAML blocks)
- `*Publisher Edition:*` version lines
- All other content

**Code Structure:**
```python
def clean_metadata(content):
    """Removes WordPress/YAML metadata while preserving decorative dividers"""
    # Smart YAML block detection (looks ahead for wp_post_id/last_updated)
    # Only removes YAML blocks, preserves decorative dividers
    # Returns cleaned content

def assemble_manuscript():
    """Main assembly function"""
    # Iterates through MANUSCRIPT_FILES list
    # Cleans each file
    # Adds page breaks
    # Writes combined output
```

**To Add a New Chapter:**
1. Create `REVISED-##_chapter-##-title.md` in wiki
2. Add filename to `MANUSCRIPT_FILES` list (line 16-52)
3. Run `python3 assemble_manuscript.py`

---

### Stage 2: PDF Generation

**Script:** `create_pdf_kdp_ready.py`

**Technology:** ReportLab 4.4.4+

**Input:** `COMPLETE-MANUSCRIPT.md`

**Output:** `OUT-OF-THE-SWAMP-PUBLISHER.pdf`

#### PDF Specifications

| Setting | Value | KDP Requirement |
|---------|-------|-----------------|
| Page Size | 6" × 9" | Standard paperback |
| Margins | 0.65" L/R, 0.9" T, 0.65" B | Within guidelines |
| Font | Times New Roman 11pt | Embedded |
| Pagination | Roman (i-v) → Arabic (1+) | Sequential |
| Headers | Chapter titles, italic | Professional |
| Color Mode | Grayscale | Standard |

#### Font Embedding

**Critical for KDP:** All fonts MUST be fully embedded.

```python
# Fonts registered with TTFont (auto-embeds)
pdfmetrics.registerFont(TTFont('TimesNewRoman',
    '/System/Library/Fonts/Supplemental/Times New Roman.ttf'))
```

**Font Paths (macOS):**
- Regular: `Times New Roman.ttf`
- Bold: `Times New Roman Bold.ttf`
- Italic: `Times New Roman Italic.ttf`
- Bold Italic: `Times New Roman Bold Italic.ttf`

**Fallback:** Helvetica (if Times New Roman not found)

#### Page Numbering

**Front Matter (Pages 1-5):**
- Roman numerals: i, ii, iii, iv, v
- No chapter headers
- Contents: Title, Copyright, Dedication, (TOC), Introduction

**Main Content (Pages 6+):**
- Arabic numerals: 1, 2, 3, ...
- Chapter headers in italics
- Contents: Movements, Chapters, Epilogue

**Implementation:**
```python
class NumberedCanvas(canvas.Canvas):
    def draw_page_decorations(self, page_count):
        if page_num <= 5:
            # Roman numerals, no headers
            roman = ['i', 'ii', 'iii', 'iv', 'v'][page_num - 1]
        else:
            # Arabic numerals + chapter headers
            arabic = page_num - 5
            chapter = self.chapter_map.get(page_num, "")
```

#### Typography Styles

```python
# Heading 1 (Chapters, Major Sections)
H1: 18pt Bold, 22pt leading, centered

# Heading 2 (Subsections)
H2: 14pt Bold, 18pt leading, left-aligned

# Heading 3 (Minor subsections)
H3: 12pt Bold, 16pt leading, left-aligned

# Body Text
Body: 10pt Regular, 14pt leading, justified

# Blockquotes
Quote: 9pt Italic, 13pt leading, indented 0.4"

# Lyrics
Lyrics: 9pt Regular, 13pt leading, left-aligned, indented 0.2"
```

#### Page Break Logic

**Smart Duplicate Detection:**

The PDF generator adds page breaks before major sections (Movements, Chapters, etc.), but the manuscript also contains `\pagebreak` commands. To avoid blank pages:

```python
def last_is_pagebreak():
    """Check if we recently added a PageBreak (ignoring Spacers)"""
    # Look back through last 5 items
    # Ignore Spacer objects (from blank lines)
    # Return True if PageBreak found
    # Return False if other content found
```

**Page Break Triggers:**
- `\pagebreak` command in markdown
- `\newpage` command in markdown
- H1 headings containing: 'Dedication', 'Introduction', 'Movement', 'Chapter', 'Epilogue', 'About the Author', 'Acknowledgments'
- H2 heading "A Final Word"

**Duplicate Prevention:**
```python
if any(section in text for section in sections_needing_page_break):
    if len(story) > 0 and not last_is_pagebreak():
        story.append(PageBreak())
```

#### Markdown Processing

**Supported Elements:**
- Headings (H1-H6)
- Bold (`**text**` → bold)
- Italic (`*text*` → italic)
- Links (`[text](url)` → hyperlinks)
- Images (`![alt](url)` → embedded images)
- Blockquotes (`> text` → indented italic)
- Lyrics blocks (detected by context)
- Horizontal rules (`---`)
- Tables (basic support)

**Image Handling:**
```python
# URLs: Download and cache
if img_src.startswith('http'):
    img_path = download_image(img_src)
    # Cached in: KDP/image_cache/

# Local: Load directly
else:
    img_path = os.path.join('/path/to/KDP', img_src)

# Auto-scale to fit page
max_width = 4.5 * inches
max_height = 6.5 * inches
```

**QR Codes:**
- Size: 1.3" × 1.3"
- Position: Centered
- Color: Black & white
- Format: PNG

---

### Stage 3: EPUB Generation

**Script:** `create_epub.py`

**Technology:** Pandoc 3.0+

**Input:** `COMPLETE-MANUSCRIPT.md` (cleaned)

**Output:** `OUT-OF-THE-SWAMP-PUBLISHER.epub`

#### EPUB Specifications

| Setting | Value |
|---------|-------|
| Format | EPUB3 |
| TOC | Auto-generated, 2 levels |
| Reflowable | Yes |
| Images | Embedded, optimized |
| Fonts | Reader-selectable |
| ISBN | 979-8-218-83354-1 |

#### Cleaning Process

**Elements Removed for EPUB:**
```python
# 1. YAML metadata blocks
# 2. Manual table of contents (EPUB auto-generates)
# 3. QR code images (not functional in EPUB - readers can click links)
# 4. LaTeX commands (\pagebreak, \newpage)
# 5. WordPress metadata
```

**Elements Preserved in EPUB:**
- **"Listen at:" shortened URL lines** - Provide easy-to-type URLs for readers
- All song links (clickable in EPUB)
- All content and formatting

**Why Remove QR Codes?**
- EPUB readers can click links directly
- QR codes don't work in digital format
- Shortened URLs provide the same access

#### Pandoc Command

```python
cmd = [
    "pandoc",
    temp_file,
    "-o", output_file,
    "--metadata", "title=Out of the Swamp: How I Found Truth",
    "--metadata", "subtitle=A Wayfarer's Journey Through Grace",
    "--metadata", "author=Skyler Thomas",
    "--metadata", "publisher=Skyler Thomas Publishing",
    "--metadata", "rights=Copyright © 2025 by Skyler Thomas...",
    "--metadata", "language=en-US",
    "--metadata", "identifier=979-8-218-83354-1",
    "--toc",              # Generate table of contents
    "--toc-depth=2",      # H1 and H2 in TOC
    "--split-level=1",    # Split at H1 (chapters)
]
```

#### EPUB Structure

```
OUT-OF-THE-SWAMP-PUBLISHER.epub/
├── META-INF/
│   └── container.xml
├── OEBPS/
│   ├── content.opf      # Metadata & manifest
│   ├── toc.ncx          # Navigation
│   ├── nav.xhtml        # EPUB3 navigation
│   ├── text/
│   │   ├── ch001.xhtml  # Title page
│   │   ├── ch002.xhtml  # Copyright
│   │   ├── ch003.xhtml  # Dedication
│   │   └── ...          # All chapters
│   ├── images/
│   │   └── ...          # Embedded images
│   └── styles/
│       └── stylesheet.css
└── mimetype
```

#### Platform Compatibility

**Tested/Compatible:**
- Amazon Kindle (via KDP upload)
- Apple Books (iOS, macOS)
- Google Play Books
- Kobo eReaders
- Barnes & Noble Nook
- Calibre (EPUB reader)
- Any EPUB3-compatible reader

---

## Dependencies

### Python Packages

```bash
pip install reportlab>=4.4.4
pip install Pillow>=10.0.0
```

**reportlab:** PDF generation
- Platypus (high-level layout)
- Canvas (low-level drawing)
- TTFont (TrueType font embedding)

**Pillow (PIL):** Image processing
- Image resizing
- Format conversion
- QR code handling

### System Requirements

**Pandoc:**
```bash
# macOS
brew install pandoc

# Verify installation
pandoc --version
# Should show 3.0 or higher
```

**Fonts:**
- Times New Roman (installed by default on macOS)
- Location: `/System/Library/Fonts/Supplemental/`
- Fallback: Helvetica (built into ReportLab)

---

## Configuration

### Manuscript File Order

**File:** `assemble_manuscript.py`, lines 16-52

```python
MANUSCRIPT_FILES = [
    # Pre-Book Content
    "REVISED-00_title-page.md",
    "REVISED-00_copyright-page.md",
    "REVISED-00_dedication.md",
    "REVISED-00_introduction-PUBLISHER.md",

    # Movement 1
    "REVISED-01_movement-1-intro.md",
    "REVISED-02_chapter-01-my-swamp.md",
    # ... etc
]
```

**To add/remove files:** Edit this list, then rebuild.

### PDF Page Size

**File:** `create_pdf_kdp_ready.py`, line 180-195

```python
# Custom page size
PAGE_WIDTH = 6 * inch
PAGE_HEIGHT = 9 * inch

# Custom margins
LEFT_MARGIN = 0.65 * inch
RIGHT_MARGIN = 0.65 * inch
TOP_MARGIN = 0.9 * inch
BOTTOM_MARGIN = 0.65 * inch
```

### Sections Requiring Page Breaks

**File:** `create_pdf_kdp_ready.py`, line 423-425

```python
sections_needing_page_break = [
    'Dedication',
    'Table of Contents',
    'Introduction',
    'Epilogue',
    'About the Author',
    'Acknowledgments',
    'The Road Ahead',
    'Chapter',
    'Movement'
]
```

**To add new sections:** Add to this list.

---

## Debugging

### Enable Verbose Output

**Assembly:**
```python
# Line 106: Already prints file names
print(f"✓ Adding: {filename}")
```

**PDF:**
```python
# Add after line 275:
print(f"Processing line {i}: {line[:50]}...")
```

**EPUB:**
```python
# Add after line 129:
print(f"Cleaned {len(cleaned_lines)} lines")
```

### Check Intermediate Files

**Manuscript (after assembly):**
```bash
# View first 100 lines
head -100 COMPLETE-MANUSCRIPT.md

# Search for metadata
grep -n "wp_post_id\|last_updated" COMPLETE-MANUSCRIPT.md

# Count page breaks
grep -c "\\\\pagebreak" COMPLETE-MANUSCRIPT.md
```

**PDF (check structure):**
```bash
# Install pdfinfo (part of poppler)
brew install poppler

# Check PDF info
pdfinfo OUT-OF-THE-SWAMP-PUBLISHER.pdf

# Check fonts
pdffonts OUT-OF-THE-SWAMP-PUBLISHER.pdf
# Should show Times New Roman as "embedded subset"
```

**EPUB (validate):**
```bash
# Install epubcheck
brew install epubcheck

# Validate EPUB
epubcheck OUT-OF-THE-SWAMP-PUBLISHER.epub
```

### Common Errors

#### "File not found: REVISED-XX"
**Cause:** Missing file in wiki directory
**Fix:** Create the file or remove from MANUSCRIPT_FILES list

#### "Font not found"
**Cause:** Times New Roman not installed
**Fix:** Script falls back to Helvetica (works, but not ideal)

#### "Pandoc not found"
**Cause:** Pandoc not installed
**Fix:** `brew install pandoc`

#### "Image not found: qr-XX.png"
**Cause:** QR code images missing from skylerthomas3/KDP directory
**Fix:** Ensure QR code PNG files are in `/Users/paulmarshall/Documents/GitHub/skylerthomas3/KDP/`
**Required files:** 14 QR codes (qr-ch01-i-will-rise.png through qr-ch12-nothing-wasted.png)

#### "Blank pages in PDF"
**Cause:** Duplicate page breaks
**Fix:** Already fixed in `last_is_pagebreak()` function

---

## Performance

### Build Times

| Stage | Time | Bottleneck |
|-------|------|------------|
| Assembly | <1 sec | File I/O |
| PDF | 2-3 sec | Font rendering |
| EPUB | 1-2 sec | Pandoc processing |
| **Total** | **3-5 sec** | - |

### File Sizes

| File | Size | Notes |
|------|------|-------|
| COMPLETE-MANUSCRIPT.md | 137 KB | Plain text |
| OUT-OF-THE-SWAMP-PUBLISHER.pdf | 321 KB | Embedded fonts |
| OUT-OF-THE-SWAMP-PUBLISHER.epub | 91 KB | Compressed |

**Why PDF is larger:**
- Embedded TrueType fonts (~200 KB)
- Embedded images
- PDF structure overhead

### Optimization

**Already Optimized:**
- Image caching (avoid re-downloading)
- Single-pass markdown parsing
- Efficient font subset embedding

**Further Optimization (if needed):**
- Pre-process images to smaller sizes
- Use font subsetting (only embed used characters)
- Compress images before embedding

---

## Testing

### Pre-Upload Checklist

**PDF:**
- [ ] Open in Adobe Reader (free)
- [ ] Check page numbers (Roman → Arabic)
- [ ] Verify fonts (should be crisp, not jagged)
- [ ] Check all page breaks (no blanks)
- [ ] Verify chapter headers appear
- [ ] Check all images/QR codes
- [ ] Print test page (optional)

**EPUB:**
- [ ] Open in Calibre
- [ ] Test on Kindle Previewer (KDP tool)
- [ ] Check TOC navigation
- [ ] Verify all links work
- [ ] Test on mobile device
- [ ] Validate with epubcheck

### KDP Upload Test

**Before final upload:**
1. Upload PDF to KDP as draft
2. Use KDP's preview tool
3. Check for warnings/errors
4. Download preview PDF
5. Compare to original

**Common KDP Warnings:**
- Fonts not embedded → Fixed (using TTFont)
- Excessive blank pages → Fixed (smart page breaks)
- Low-resolution images → Acceptable (QR codes)

---

## Maintenance

### Updating Scripts

**When to update:**
- Adding new sections requiring page breaks
- Changing page size/margins
- Updating metadata (ISBN, copyright year)
- Adding new markdown elements

**Testing after changes:**
```bash
# Full rebuild
python3 generate_all.py

# Verify output
ls -lh OUT-OF-THE-SWAMP-PUBLISHER.*
```

### Version Control

**Track these files:**
- `generate_all.py`
- `assemble_manuscript.py`
- `create_pdf_kdp_ready.py`
- `create_epub.py`

**Don't track:**
- `COMPLETE-MANUSCRIPT.md` (generated)
- `OUT-OF-THE-SWAMP-PUBLISHER.pdf` (generated)
- `OUT-OF-THE-SWAMP-PUBLISHER.epub` (generated)
- `image_cache/` (cached downloads)
- `TEMP-MANUSCRIPT-CLEAN.md` (temporary)

---

## Future Enhancements

**Potential Improvements:**
- [ ] Automatic TOC generation for PDF
- [ ] Cover image support
- [ ] MOBI generation (older Kindle format)
- [ ] Print-specific bleeds/crop marks
- [ ] Automated KDP upload via API
- [ ] Multi-format build (5×8", 6×9", 8×10")
- [ ] Interactive configuration wizard

---

## Recent Fixes (October 23-24, 2025)

### Issue 1: WordPress Metadata in PDF
**Problem:** YAML blocks with `wp_post_id:` and `last_updated:` appearing in final PDF
**Solution:** Enhanced `clean_metadata()` in `assemble_manuscript.py` with smart YAML detection
**Result:** Only true YAML blocks removed, decorative dividers preserved

### Issue 2: Missing Publisher Edition Line
**Problem:** Copyright page missing `*Publisher Edition: v20251023a*` line
**Cause:** Metadata cleaner was removing decorative `---` dividers
**Solution:** Modified YAML detection to distinguish between metadata blocks and decorative dividers
**Result:** All decorative content preserved

### Issue 3: Movement Headers Not Starting New Pages
**Problem:** Movement 3 didn't start on a new page
**Solution:** Added 'Movement' to `sections_needing_page_break` list in `create_pdf_kdp_ready.py`
**Result:** All movements now start on fresh pages

### Issue 4: `\pagebreak` Appearing as Text
**Problem:** Command showed as literal text in PDF
**Cause:** PDF script only checked for `\newpage`, not `\pagebreak`
**Solution:** Updated line 324 to handle both commands
**Result:** Both page break commands work correctly

### Issue 5: Blank Pages Between Sections
**Problem:** Double page breaks creating blank pages
**Cause:** Both assembly script and PDF script adding page breaks
**Solution:** Created `last_is_pagebreak()` function that checks recent story elements, ignoring Spacers
**Result:** No more duplicate page breaks

### Issue 6: Missing QR Codes
**Problem:** QR code images not found during PDF generation
**Cause:** Files were in skylerthomas2/KDP instead of skylerthomas3/KDP
**Solution:** Copied 14 QR PNG files to correct location
**Result:** All song QR codes now embedded in PDF

### Issue 7: Shortened URLs Removed from EPUB
**Problem:** "Listen at:" lines with shortened URLs being deleted
**Cause:** EPUB cleaning script was removing these lines (lines 94-97)
**Solution:** Removed the code that deleted "Listen at:" lines
**Result:** Shortened URLs now preserved in EPUB for reader convenience

### Issue 8: Hardcoded Wrong Paths
**Problem:** Scripts pointing to skylerthomas2 instead of skylerthomas3
**Solution:** Updated all paths to use skylerthomas3
**Files changed:** `create_pdf_kdp_ready.py`, `create_epub.py`
**Result:** All scripts now use correct repository

---

## Support

**For build issues:**
1. Check this guide
2. Review `COMPLETE-WORKFLOW-GUIDE.md`
3. Verify all dependencies installed
4. Check file paths (skylerthomas3, not skylerthomas2)

**For content issues:**
1. Edit REVISED-*.md files in wiki
2. Rebuild using `generate_all.py`
3. Verify output files

---

**Last Updated:** October 23, 2025
**Build System Version:** 2.0 (October 2025 fixes applied)
**Status:** ✅ Production Ready
