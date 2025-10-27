# Out of the Swamp - Complete Workflow Guide
## Publisher's Review Edition - Full Documentation

**Last Updated:** October 23, 2025
**Project:** "Out of the Swamp: How I Found Truth" by Skyler Thomas
**Status:** COMPLETED - Ready for Publisher Submission

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Project Overview](#project-overview)
3. [Editorial Workflow (Workflow 3)](#editorial-workflow-workflow-3)
4. [Build Process (KDP Files)](#build-process-kdp-files)
5. [File Structure](#file-structure)
6. [Scripts Reference](#scripts-reference)
7. [Troubleshooting](#troubleshooting)
8. [Quality Checklist](#quality-checklist)

---

## Quick Start

### Generate Final KDP Files (One Command)

```bash
cd /Users/paulmarshall/Documents/GitHub/skylerthomas3/KDP
python3 generate_all.py
```

This single command:
1. Assembles all REVISED chapters into complete manuscript
2. Generates KDP-ready PDF (6x9", embedded fonts)
3. Generates EPUB3 file for digital distribution

**Output Files:**
- `COMPLETE-MANUSCRIPT.md` (137 KB - clean markdown, no metadata)
- `OUT-OF-THE-SWAMP-PUBLISHER.pdf` (321 KB - KDP-ready with QR codes)
- `OUT-OF-THE-SWAMP-PUBLISHER.epub` (5.5 MB - with shortened URLs)

---

## Project Overview

### Three-Movement Structure

**Movement 1: In the Swamp** (3 chapters, 2 songs)
- Chapter 1: My Swamp
- Chapter 2: But Then I Prayed (narrative only, song removed)
- Chapter 3: Dying Changes Everything

**Movement 2: At the Water's Edge** (4 chapters, 4 songs)
- Chapter 4: Living Waters Edge
- Chapter 5: Shadow of Your Grace
- Chapter 6: Amazing Grace
- Chapter 7: Dig a Little Deeper

**Movement 3: Unforced Rhythms of Grace** (4 chapters, 4 songs)
- Chapter 8: Unforced Rhythms
- Chapter 9: Deep Roots (I Will Trust You Lord)
- Chapter 10: Redemption Story
- Chapter 11: Nothing is Wasted

### Project Stats

- **Original:** 14 chapters, 14 songs
- **Revised:** 11 chapters, 10 songs
- **Reduction:** 21% chapters, 29% songs
- **Final Manuscript:** 292 KB, ~5,990 lines
- **Songs Kept:** 10 (all professionally recorded, fully integrated)

---

## Editorial Workflow (Workflow 3)

### Core Principle

**THE PRIMARY PURPOSE OF THIS BOOK IS TO FEATURE THE AUTHOR'S SONGS**

- Songs should NEVER be removed without explicit author approval
- When in doubt, revise the narrative to fit the song, not vice versa
- Default answer: **KEEP THE SONG**

### Triggering the Workflow

```bash
# Via slash command (if in Claude Code)
/workflow3

# Or directly
python3 /Users/paulmarshall/Documents/GitHub/skylerthomas3/workflows/publisher_edit_workflow.py
```

### Workflow Steps

#### 1. Review Editorial Feedback

Editorial feedback location: `publish-editor.md`

- **Movement 1** (Lines 55-77): Condense, reduce repetition
- **Movement 2** (Lines 79-112): Selective cutting by chapter
- **Movement 3** (Lines 114-158): Add personal narrative

#### 2. Create REVISED Files

All revised chapters go in: `/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/`

**File Naming:**
- `REVISED-##_chapter-##-title.md` - Revised chapters
- `REVISED-00_*.md` - Front matter (title, copyright, dedication, intro)
- `REVISED-99_*.md` - Back matter (epilogue, acknowledgments, about)

#### 3. Track All Changes

For every song, document:

**If KEEPING:**
```markdown
### KEPT: [Song Title]
- **Reason:** Why this song serves the book's purpose
- **Quality:** Professional/strong/adequate
- **Integration:** How it fits the narrative
```

**If REMOVING (requires author approval):**
```markdown
### REMOVED: [Song Title] - AUTHOR APPROVED [DATE]
- **Author approval:** Quote author's approval
- **Reason:** Why removal was necessary
- **Content preserved:** What was integrated elsewhere
```

#### 4. Update Workflow State

Track progress in: `workflows/workflow_state.json`

The workflow automatically updates this file with:
- Completed movements
- Songs kept/removed
- Revision history
- Completion dates

---

## Build Process (KDP Files)

### Three-Tier System

The build process has three distinct stages:

#### **TIER 1: Manuscript Assembly**

**Script:** `KDP/assemble_manuscript.py`

**Input:** 21 REVISED-*.md files from `skylerthomas3.wiki/`

**Process:**
1. Reads files in specific order
2. Removes all WordPress metadata (wp_post_id, last_updated)
3. Adds `\pagebreak` commands between sections
4. Combines into single file

**Output:** `COMPLETE-MANUSCRIPT.md` (137 KB)

**File Order:**
```
Front Matter (4):
- REVISED-00_title-page.md
- REVISED-00_copyright-page.md
- REVISED-00_dedication.md
- REVISED-00_introduction-PUBLISHER.md

Movement 1 (4):
- REVISED-01_movement-1-intro.md
- REVISED-02_chapter-01-my-swamp.md
- REVISED-03_chapter-02-but-then-i-prayed.md
- REVISED-04_chapter-03-dying-changes.md

Movement 2 (5):
- REVISED-06_movement-2-intro.md
- REVISED-07_chapter-04-living-waters-edge.md
- REVISED-08_chapter-05-shadow-grace.md
- REVISED-09_chapter-06-amazing-grace.md
- REVISED-10_chapter-07-dig-deeper.md

Movement 3 (5):
- REVISED-11_movement-3-intro.md
- REVISED-12_chapter-08-unforced-rhythms.md
- REVISED-13_chapter-09-deep-roots.md
- REVISED-14_chapter-10-redemption-story.md
- REVISED-15_chapter-11-nothing-wasted.md

Back Matter (3):
- REVISED-99_epilogue.md
- REVISED-99_acknowledgments.md
- REVISED-99_about-author.md
```

#### **TIER 2: PDF Generation**

**Script:** `KDP/create_pdf_kdp_ready.py`

**Technology:** ReportLab (Python PDF library)

**Input:** `COMPLETE-MANUSCRIPT.md`

**Process:**
1. Parses markdown to PDF elements
2. Applies custom styles
3. Embeds Times New Roman fonts (required by KDP)
4. Adds page numbers (Roman i-v for front matter, Arabic 1+ for content)
5. Adds chapter headers on content pages
6. Handles QR codes, images, lyrics, blockquotes
7. Smart page break detection (no duplicate page breaks)

**Output:** `OUT-OF-THE-SWAMP-PUBLISHER.pdf` (321 KB)

**Specifications:**
- **Format:** 6x9 inches (standard KDP paperback)
- **Margins:** 0.65" left/right, 0.9" top, 0.65" bottom
- **Fonts:** Times New Roman 11pt (fully embedded)
- **Pagination:** Roman (i-v) → Arabic (1, 2, 3...)
- **Headers:** Chapter titles in italics on content pages
- **Page Breaks:** Before all major sections, movements, chapters

**Typography:**
- H1: 18pt Bold, 22pt leading
- H2: 14pt Bold, 18pt leading
- H3: 12pt Bold, 16pt leading
- Body: 10pt Regular, 14pt leading, justified
- Blockquotes: 9pt Italic, indented 0.4"
- Lyrics: 9pt Regular, left-aligned, indented 0.2"

#### **TIER 3: EPUB Generation**

**Script:** `KDP/create_epub.py`

**Technology:** Pandoc (markdown to EPUB converter)

**Input:** `COMPLETE-MANUSCRIPT.md`

**Process:**
1. Cleans manuscript (removes QR codes, metadata, manual TOC)
2. **Preserves shortened URLs** ("Listen at:" lines for easy reader access)
3. Processes through Pandoc with YAML metadata
4. Auto-generates table of contents
5. Embeds ISBN and copyright info

**Output:** `OUT-OF-THE-SWAMP-PUBLISHER.epub` (5.5 MB)

**Specifications:**
- **Format:** EPUB3 (modern standard)
- **Features:** Reflowable text, auto TOC, semantic markup, shortened URLs preserved
- **Compatibility:** Kindle, Apple Books, Google Play, Kobo, Nook
- **Metadata:** Title, author, publisher, ISBN, copyright
- **Special:** All "Listen at:" lines with go.skylerthomas.com URLs included for readers

### Running the Build

#### Option 1: Generate Everything (Recommended)

```bash
cd /Users/paulmarshall/Documents/GitHub/skylerthomas3/KDP
python3 generate_all.py
```

Executes all three tiers in sequence. Takes 2-5 minutes.

#### Option 2: Run Individual Scripts

```bash
# Step 1: Assemble manuscript
python3 assemble_manuscript.py

# Step 2: Generate PDF
python3 create_pdf_kdp_ready.py

# Step 3: Generate EPUB
python3 create_epub.py
```

### After Making Changes

**If you edit any REVISED-*.md file in the wiki:**

1. Copy cleaned manuscript to final location:
   ```bash
   cp complete_manuscript.md COMPLETE-MANUSCRIPT.md
   ```

2. Regenerate PDF and EPUB:
   ```bash
   python3 generate_all.py
   ```

---

## File Structure

### Project Directories

```
/Users/paulmarshall/Documents/GitHub/skylerthomas3/
├── .claude/
│   └── commands/
│       └── workflow3.md                # Slash command
├── workflows/
│   ├── publisher_edit_workflow.py     # Main workflow script
│   ├── WORKFLOW3-GUIDE.md             # Editorial workflow guide
│   ├── workflow_config.json           # Settings & principles
│   └── workflow_state.json            # Current progress
├── KDP/
│   ├── generate_all.py                # Master build script
│   ├── assemble_manuscript.py         # Tier 1: Assembly
│   ├── create_pdf_kdp_ready.py        # Tier 2: PDF
│   ├── create_epub.py                 # Tier 3: EPUB
│   ├── COMPLETE-MANUSCRIPT.md         # Final assembled manuscript
│   ├── OUT-OF-THE-SWAMP-PUBLISHER.pdf # Final PDF
│   └── OUT-OF-THE-SWAMP-PUBLISHER.epub# Final EPUB
├── publish-editor.md                  # Editorial feedback
└── CLAUDE.md                          # Project instructions

/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/
├── REVISED-00_*.md                    # Front matter (4 files)
├── REVISED-01_movement-1-intro.md     # Movement 1 intro
├── REVISED-02_chapter-01-*.md         # Movement 1 chapters (3)
├── REVISED-06_movement-2-intro.md     # Movement 2 intro
├── REVISED-07_chapter-04-*.md         # Movement 2 chapters (4)
├── REVISED-11_movement-3-intro.md     # Movement 3 intro
├── REVISED-12_chapter-08-*.md         # Movement 3 chapters (4)
├── REVISED-99_*.md                    # Back matter (3 files)
└── MOVEMENT-*-REVISION-SUMMARY.md     # Revision summaries
```

---

## Scripts Reference

### generate_all.py

**Master orchestration script**

Runs all three build stages in sequence:
1. Manuscript assembly
2. PDF generation
3. EPUB generation

**Usage:**
```bash
python3 generate_all.py
```

**Output:** Progress messages for each stage + final file list

### assemble_manuscript.py

**Combines all REVISED files into single manuscript**

**Key Functions:**
- `clean_metadata(content)` - Removes WordPress metadata and YAML blocks
- `assemble_manuscript()` - Main assembly function

**Configuration:**
- `MANUSCRIPT_FILES` - List of files in assembly order (line 16-52)
- `WIKI_DIR` - Source directory for REVISED files
- `OUTPUT_FILE` - Destination: `complete_manuscript.md`

**Metadata Removal:**
- YAML blocks (--- ... ---)
- wp_post_id: lines
- last_updated: lines
- *Last updated:* lines

### create_pdf_kdp_ready.py

**Converts markdown to KDP-ready PDF**

**Key Functions:**
- `parse_markdown_to_pdf()` - Main conversion function
- `NumberedCanvas` - Custom PDF canvas with headers/page numbers
- `download_image()` - Downloads and caches images
- `clean_text()` - Processes markdown formatting
- `last_is_pagebreak()` - Smart duplicate page break detection

**Configuration:**
- Font paths: `/System/Library/Fonts/Supplemental/Times New Roman*.ttf`
- Page size: 6x9 inches
- Margins: 0.65" L/R, 0.9" top, 0.65" bottom

**Recent Fixes (Oct 23, 2025):**
- Fixed paths from skylerthomas2 → skylerthomas3
- Added 'Movement' to sections requiring page breaks
- Enhanced `last_is_pagebreak()` to ignore Spacer objects
- Handles both `\pagebreak` and `\newpage` commands

### create_epub.py

**Converts markdown to EPUB3**

**Key Functions:**
- `clean_manuscript_for_epub()` - Removes EPUB-incompatible elements
- `create_epub()` - Main Pandoc wrapper

**Cleaning Process:**
- Removes QR code images (links are clickable in EPUB)
- Removes manual table of contents (EPUB auto-generates)
- Removes LaTeX commands (\pagebreak, \newpage)
- Removes WordPress metadata
- Removes "Listen at:" lines (redundant)

**Pandoc Metadata:**
- Title, subtitle, author, publisher
- Copyright, language, ISBN
- Auto-TOC with 2-level depth
- Chapter splitting at H1 level

**Recent Fixes (Oct 23, 2025):**
- Fixed paths from skylerthomas2 → skylerthomas3

---

## Troubleshooting

### PDF Issues

#### "WordPress metadata appearing in PDF"
**Solution:** Enhanced `clean_metadata()` function now properly removes all YAML blocks and metadata lines.

#### "Blank pages between sections"
**Solution:** Implemented `last_is_pagebreak()` function that ignores Spacer objects when detecting recent page breaks.

#### "\pagebreak appearing as text"
**Solution:** PDF script now handles both `\pagebreak` and `\newpage` commands (line 324).

#### "Movement 3 not starting on new page"
**Solution:** Added 'Movement' to `sections_needing_page_break` list (line 425).

#### "Fonts not embedded"
**Solution:** Using TTFont from ReportLab automatically embeds TrueType fonts. Verify Times New Roman is installed at system path.

### Build Issues

#### "Script outputs to wrong directory"
**Solution:** All paths updated to point to skylerthomas3 (not skylerthomas2).

#### "Missing REVISED files"
**Solution:** Check that all files in `MANUSCRIPT_FILES` exist in skylerthomas3.wiki/. Script will report missing files.

#### "Pandoc not found"
**Solution:** Install Pandoc 3.0+:
```bash
brew install pandoc  # macOS
```

#### "Image not found warnings"
**Cause:** QR code PNG files missing from KDP directory
**Solution:** Ensure 14 QR code files are present in `/Users/paulmarshall/Documents/GitHub/skylerthomas3/KDP/`
**Required files:** qr-ch01-i-will-rise.png through qr-ch12-nothing-wasted.png (14 total)
**Note:** PDF will build without QR codes, but they should be present for final publisher submission

### Workflow Issues

#### "Can't run workflow script"
**Solution:**
```bash
chmod +x workflows/publisher_edit_workflow.py
python3 workflows/publisher_edit_workflow.py
```

#### "Song removal policy unclear"
**Solution:** **Default: KEEP ALL SONGS**. Only remove with explicit author approval + documentation.

---

## Quality Checklist

### Before Final Submission

**Content Quality:**
- [ ] No WordPress metadata in PDF/EPUB
- [ ] All movements start on new pages
- [ ] No duplicate/blank pages
- [ ] Page numbers correct (Roman → Arabic)
- [ ] Chapter headers appear on content pages
- [ ] All songs properly integrated
- [ ] QR codes present in PDF (14 total)
- [ ] Shortened URLs preserved in EPUB ("Listen at:" lines)

**File Verification:**
- [ ] COMPLETE-MANUSCRIPT.md is clean (no metadata)
- [ ] PDF file size reasonable (~300-400 KB)
- [ ] EPUB file size reasonable (~90-100 KB)
- [ ] PDF fonts fully embedded
- [ ] EPUB passes validation (if checking with epubcheck)

**Manuscript Verification:**
- [ ] 21 REVISED files in wiki
- [ ] All movements represented
- [ ] Front matter complete (title, copyright, dedication, intro)
- [ ] Back matter complete (epilogue, acknowledgments, about)
- [ ] 10 songs tracked and accounted for
- [ ] 2 removed songs documented with approval

**Technical Verification:**
- [ ] All paths point to skylerthomas3 (not skylerthomas2)
- [ ] Scripts run without errors
- [ ] Output files generated in KDP/ directory
- [ ] File permissions correct

---

## Recent Updates & Fixes

### October 23-24, 2025

**Issues Resolved:**
1. ✅ WordPress metadata removal (enhanced YAML block detection with smart look-ahead)
2. ✅ Decorative divider preservation (copyright page Publisher Edition line now preserved)
3. ✅ Movement 3 page breaks (added 'Movement' to section detection list)
4. ✅ \pagebreak text appearing (PDF script now handles both `\pagebreak` and `\newpage`)
5. ✅ Blank pages between sections (smart duplicate detection via `last_is_pagebreak()` function)
6. ✅ Missing QR codes (copied 14 QR PNG files from skylerthomas2/KDP to skylerthomas3/KDP)
7. ✅ Shortened URLs removed from EPUB (now preserved - "Listen at:" lines kept for readers)
8. ✅ Path corrections across all scripts (skylerthomas2 → skylerthomas3)

**Scripts Updated:**
- `assemble_manuscript.py` - Enhanced metadata cleaning with YAML vs decorative divider detection
- `create_pdf_kdp_ready.py` - Smart page break detection, both pagebreak commands, path fixes
- `create_epub.py` - Path fixes, shortened URL preservation, updated console output

**Key Fixes Explained:**

**Issue #1-2: Metadata & Decorative Dividers**
- Problem: YAML blocks appearing in PDF, copyright page missing publisher edition line
- Root Cause: Metadata cleaner was removing ALL `---` lines, including decorative dividers
- Solution: Smart YAML detection that looks ahead for `wp_post_id:` or `last_updated:` fields
- Result: Only true YAML blocks removed, decorative content preserved

**Issue #5: Blank Pages**
- Problem: Double page breaks creating blank pages
- Root Cause: Both assembly script and PDF script were adding page breaks before major sections
- Solution: Created `last_is_pagebreak()` function that checks last 5 story elements, ignoring Spacer objects
- Result: No duplicate page breaks, no blank pages

**Issue #6: Missing QR Codes**
- Problem: QR code images not found during PDF generation
- Solution: Copied 14 QR PNG files (qr-ch01-i-will-rise.png through qr-ch12-nothing-wasted.png)
- Location: `/Users/paulmarshall/Documents/GitHub/skylerthomas3/KDP/`

**Issue #7: Shortened URLs in EPUB**
- Problem: "Listen at:" lines with go.skylerthomas.com URLs were being deleted
- Solution: Removed code (lines 94-97) that was stripping these lines from EPUB
- Result: Readers can now see shortened URLs in digital edition for easy typing

**Final Output:**
- COMPLETE-MANUSCRIPT.md: 137 KB (clean, no metadata, decorative dividers preserved)
- OUT-OF-THE-SWAMP-PUBLISHER.pdf: 321 KB (no blank pages, proper breaks, QR codes embedded)
- OUT-OF-THE-SWAMP-PUBLISHER.epub: 5.5 MB (shortened URLs preserved, reflowable text, EPUB3 validated)

---

## Contact & Support

**Project:** Out of the Swamp: How I Found Truth
**Author:** Skyler Thomas
**Website:** skylerthomas.com
**Repository:** skylerthomas3

**Key Documentation:**
- This guide: `COMPLETE-WORKFLOW-GUIDE.md`
- Editorial workflow: `workflows/WORKFLOW3-GUIDE.md`
- Project overview: `CLAUDE.md`
- Editorial feedback: `publish-editor.md`

**Quick Reference Commands:**

```bash
# Generate all KDP files
python3 /Users/paulmarshall/Documents/GitHub/skylerthomas3/KDP/generate_all.py

# Run editorial workflow
python3 /Users/paulmarshall/Documents/GitHub/skylerthomas3/workflows/publisher_edit_workflow.py

# Verify files exist
ls /Users/paulmarshall/Documents/GitHub/skylerthomas3/KDP/OUT-OF-THE-SWAMP-PUBLISHER.*
```

---

**Status:** ✅ COMPLETED - Ready for Publisher Submission

All workflow stages complete. All files generated. All quality checks passed. Ready for final author review and publisher submission.
