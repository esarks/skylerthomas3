# KDP Document Generation
## Out of the Swamp - Publisher's Review Edition

This directory contains scripts to generate PDF and EPUB versions of the manuscript from the REVISED files in skylerthomas3.wiki.

---

## Quick Start

### Generate All Formats (Recommended)
```bash
python3 kdp/generate_all.py
```

This will:
1. Assemble the manuscript from all REVISED files
2. Generate PDF for Amazon KDP
3. Generate EPUB for ebook readers

### Individual Steps

**Assemble manuscript only:**
```bash
python3 kdp/assemble_manuscript.py
```

**Generate PDF only:**
```bash
python3 kdp/create_pdf_kdp_ready.py
```

**Generate EPUB only:**
```bash
python3 kdp/create_epub.py
```

---

## Requirements

### Python Packages
```bash
pip install reportlab ebooklib
```

### System Requirements
- **pandoc** (for EPUB generation)
  ```bash
  brew install pandoc  # macOS
  ```

### Check Requirements
```bash
python3 -c "import reportlab; print('reportlab:', reportlab.Version)"
python3 -c "import ebooklib; print('ebooklib: installed')"
pandoc --version
```

---

## What Gets Generated

### 1. complete_manuscript.md
**Source:** All REVISED files from skylerthomas3.wiki
**Format:** Single markdown file
**Use:** Source for PDF/EPUB generation

**Includes:**
- REVISED-00_introduction-PUBLISHER.md
- REVISED movement intros
- REVISED chapters
- (Pre/post book content when revised)

### 2. out_of_the_swamp.pdf
**Format:** 6x9 inch PDF for Amazon KDP
**Features:**
- Fully embedded fonts (Times New Roman)
- Page numbers (Roman i-v for front matter, Arabic 1, 2, 3... for content)
- Chapter headers
- QR codes for songs
- Professional formatting

### 3. out_of_the_swamp.epub
**Format:** EPUB3 for ebook readers
**Features:**
- Responsive text
- Clickable QR codes
- Metadata (title, author, etc.)
- TOC navigation

---

## File Structure

```
kdp/
├── README.md                   # This file
├── assemble_manuscript.py      # Combines REVISED files
├── create_pdf_kdp_ready.py     # Generates PDF
├── create_epub.py              # Generates EPUB
├── generate_all.py             # Master script (runs all)
├── complete_manuscript.md      # Output: assembled manuscript
├── out_of_the_swamp.pdf       # Output: KDP-ready PDF
├── out_of_the_swamp.epub      # Output: EPUB ebook
└── image_cache/               # Cached QR code images
```

---

## Customization

### Adding/Removing Chapters

Edit `assemble_manuscript.py`:

```python
MANUSCRIPT_FILES = [
    "REVISED-00_introduction-PUBLISHER.md",
    "REVISED-01_movement-1-intro.md",
    "REVISED-02_chapter-01-my-swamp.md",
    # Add new REVISED files here as you complete them
    "REVISED-16_chapter-12-new-chapter.md",  # New chapter
]
```

### Page Size / Formatting

Edit `create_pdf_kdp_ready.py`:

```python
# Current: 6x9 inches (standard KDP size)
pagesize=(6*inches, 9*inches)

# Alternative: 5.5x8.5 inches
pagesize=(5.5*inches, 8.5*inches)
```

### Font Selection

PDF script tries Times New Roman first, falls back to Helvetica if not available.

To check available fonts on your system:
```bash
ls /System/Library/Fonts/Supplemental/
```

---

## Workflow Integration

### After Adding a New Chapter

1. **Revise chapter** in skylerthomas3.wiki
2. **Update workflow tracking:**
   ```bash
   python3 workflows/update_workflow_progress.py --movement 3 --add-chapter 12
   ```
3. **Add to manuscript list** in `assemble_manuscript.py`
4. **Regenerate documents:**
   ```bash
   python3 kdp/generate_all.py
   ```
5. **Review output** in kdp/ folder

### For Publisher Submission

1. **Ensure all chapters revised** and in REVISED- format
2. **Update manuscript file list** in assemble_manuscript.py
3. **Generate final versions:**
   ```bash
   python3 kdp/generate_all.py
   ```
4. **Review generated PDF/EPUB**
5. **Submit to publisher**

---

## Output Specifications

### PDF (Amazon KDP)
- **Size:** 6x9 inches
- **Margins:** 0.65" left/right, 0.9" top, 0.65" bottom
- **Font:** Times New Roman 11pt (body), 14pt (headings)
- **Page Numbers:** Roman numerals (i-v) for front matter, Arabic (1+) for content
- **Headers:** Chapter titles in italics
- **File Size:** Typically 2-5 MB depending on images

### EPUB (Ebook)
- **Format:** EPUB3
- **Text:** Reflowable
- **Images:** Embedded and compressed
- **Metadata:** Title, author, language, date
- **File Size:** Typically 500KB-2MB

---

## Troubleshooting

### "No module named 'reportlab'"
```bash
pip install reportlab
```

### "No module named 'ebooklib'"
```bash
pip install ebooklib
```

### "pandoc: command not found"
```bash
brew install pandoc  # macOS
```

### "Font not found" errors
The script will fall back to Helvetica if Times New Roman is not found. This is acceptable but not optimal.

To install Times New Roman on macOS:
1. It should be in /System/Library/Fonts/Supplemental/
2. If not, download from Microsoft

### PDF is too large
- Check image sizes (QR codes should be small)
- Image cache is at kdp/image_cache/
- Large images will be downloaded and cached

### EPUB won't open
- Ensure pandoc is installed
- Check complete_manuscript.md for formatting errors
- Try regenerating: `python3 kdp/create_epub.py`

### Missing chapters in output
Check `assemble_manuscript.py`:
1. Is the REVISED file listed in MANUSCRIPT_FILES?
2. Does the file exist in skylerthomas3.wiki/?
3. Is it spelled correctly (case-sensitive)?

---

## Current Manuscript Status

### Included (as of last update)
- Introduction (REVISED publisher version)
- Movement 1: 3 chapters
- Movement 2: 4 chapters
- Movement 3: 4 chapters (as you add them)

### Not Yet Included
- Pre-book content (using ORIGINAL- versions for now)
- Post-book content (using ORIGINAL- versions for now)
- Additional chapters as they're revised

### To Add Next
Edit `assemble_manuscript.py` and add:
```python
"REVISED-16_chapter-12-your-new-chapter.md",
```

Then regenerate:
```bash
python3 kdp/generate_all.py
```

---

## Quality Checklist

Before submitting to publisher:

- [ ] All chapters revised and in REVISED- format
- [ ] All chapters listed in assemble_manuscript.py
- [ ] Manuscript assembles without errors
- [ ] PDF generates successfully
- [ ] EPUB generates successfully
- [ ] Page numbers are sequential
- [ ] Chapter headers display correctly
- [ ] QR codes are present and functional
- [ ] No missing images
- [ ] File sizes are reasonable (<10MB)
- [ ] Fonts are embedded (check PDF properties)
- [ ] Spelling/grammar reviewed
- [ ] Song lyrics included
- [ ] Movement introductions included

---

## Support

### Documentation
- Complete workflow guide: `workflows/WORKFLOW3-GUIDE.md`
- Quick reference: `workflows/QUICK-REFERENCE.md`
- Project overview: `CLAUDE.md`

### Dependencies
- Python 3.8+
- reportlab 4.4.4+
- ebooklib
- pandoc 3.0+

### File Locations
- **Source:** `/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/`
- **Output:** `/Users/paulmarshall/Documents/GitHub/skylerthomas3/kdp/`
- **Workflow:** `/Users/paulmarshall/Documents/GitHub/skylerthomas3/workflows/`

---

**Ready to generate your publisher review edition!**

Run: `python3 kdp/generate_all.py`
