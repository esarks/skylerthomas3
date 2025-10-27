# Out of the Swamp - Quick Reference Card

## One-Line Commands

### Generate All KDP Files
```bash
python3 /Users/paulmarshall/Documents/GitHub/skylerthomas3/KDP/generate_all.py
```

### Run Editorial Workflow
```bash
python3 /Users/paulmarshall/Documents/GitHub/skylerthomas3/workflows/publisher_edit_workflow.py
```

---

## Project Stats (Current)

| Metric | Value |
|--------|-------|
| **Chapters** | 11 (from 14) |
| **Songs** | 10 (from 14) |
| **Movements** | 3 (complete) |
| **Manuscript Size** | 137 KB |
| **PDF Size** | 321 KB |
| **EPUB Size** | 91 KB |
| **Status** | ✅ Ready for Publisher |

---

## File Locations

### Source Files
```
/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/
  ├── REVISED-00_*.md (4 front matter files)
  ├── REVISED-##_*.md (14 content files)
  └── REVISED-99_*.md (3 back matter files)
```

### Output Files
```
/Users/paulmarshall/Documents/GitHub/skylerthomas3/KDP/
  ├── COMPLETE-MANUSCRIPT.md
  ├── OUT-OF-THE-SWAMP-PUBLISHER.pdf
  └── OUT-OF-THE-SWAMP-PUBLISHER.epub
```

---

## Build Process (3 Tiers)

1. **Assembly** → `assemble_manuscript.py` → Combines 21 files
2. **PDF** → `create_pdf_kdp_ready.py` → 6x9" KDP-ready
3. **EPUB** → `create_epub.py` → EPUB3 digital

---

## Core Principle

**THE PRIMARY PURPOSE OF THIS BOOK IS TO FEATURE THE AUTHOR'S SONGS**

- Default: **KEEP ALL SONGS**
- Song removal requires **author approval**
- Revise narrative to fit songs, not vice versa

---

## Song Tracking

### Kept (10 songs)
**Movement 1:** My Swamp • Dying Changes Everything
**Movement 2:** Living Waters Edge • Shadow Grace • Amazing Grace • Dig Deeper
**Movement 3:** Unforced Rhythms • Deep Roots • Redemption Story • Nothing Wasted

### Removed (2 songs - with author approval)
- But Then I Prayed (content integrated)
- STOP!! And Make a Decision (tonal clash)

---

## Common Tasks

### After Editing a Chapter
```bash
cd /Users/paulmarshall/Documents/GitHub/skylerthomas3/KDP
python3 generate_all.py
```

### Check File Status
```bash
ls -lh OUT-OF-THE-SWAMP-PUBLISHER.{pdf,epub}
```

### Verify No Metadata
```bash
grep -i "wp_post_id\|last_updated" COMPLETE-MANUSCRIPT.md
# Should return nothing
```

---

## Key Documentation

- **Complete Guide:** `COMPLETE-WORKFLOW-GUIDE.md`
- **Editorial Workflow:** `workflows/WORKFLOW3-GUIDE.md`
- **Project Overview:** `CLAUDE.md`
- **Editorial Feedback:** `publish-editor.md`

---

## Manuscript Assembly Order

```
1. REVISED-00_title-page.md
2. REVISED-00_copyright-page.md
3. REVISED-00_dedication.md
4. REVISED-00_introduction-PUBLISHER.md

5. REVISED-01_movement-1-intro.md
6. REVISED-02_chapter-01-my-swamp.md
7. REVISED-03_chapter-02-but-then-i-prayed.md
8. REVISED-04_chapter-03-dying-changes.md

9. REVISED-06_movement-2-intro.md
10. REVISED-07_chapter-04-living-waters-edge.md
11. REVISED-08_chapter-05-shadow-grace.md
12. REVISED-09_chapter-06-amazing-grace.md
13. REVISED-10_chapter-07-dig-deeper.md

14. REVISED-11_movement-3-intro.md
15. REVISED-12_chapter-08-unforced-rhythms.md
16. REVISED-13_chapter-09-deep-roots.md
17. REVISED-14_chapter-10-redemption-story.md
18. REVISED-15_chapter-11-nothing-wasted.md

19. REVISED-99_epilogue.md
20. REVISED-99_acknowledgments.md
21. REVISED-99_about-author.md
```

---

## PDF Specifications

| Setting | Value |
|---------|-------|
| **Size** | 6" × 9" |
| **Margins** | 0.65" L/R, 0.9" top, 0.65" bottom |
| **Font** | Times New Roman 11pt |
| **Pagination** | Roman (i-v) → Arabic (1+) |
| **Headers** | Chapter titles on content pages |
| **Fonts Embedded** | Yes (KDP requirement) |

---

## EPUB Specifications

| Setting | Value |
|---------|-------|
| **Format** | EPUB3 |
| **TOC** | Auto-generated |
| **Reflowable** | Yes |
| **ISBN** | 979-8-218-83354-1 |
| **Platforms** | Kindle, Apple Books, Kobo, Nook |

---

## Troubleshooting Quick Fixes

### Metadata appearing in PDF
```bash
# Already fixed in assemble_manuscript.py
# Just regenerate
python3 generate_all.py
```

### Blank pages between sections
```bash
# Already fixed in create_pdf_kdp_ready.py
# Regenerate to apply fix
python3 generate_all.py
```

### Wrong output directory
```bash
# Verify you're in correct directory
cd /Users/paulmarshall/Documents/GitHub/skylerthomas3/KDP
```

---

## Quality Checklist

- [ ] No metadata in PDF
- [ ] All movements start on new pages
- [ ] No blank pages
- [ ] Page numbers correct
- [ ] Fonts embedded
- [ ] All 10 songs present
- [ ] Files in KDP/ directory

---

**Last Updated:** October 23, 2025
**Status:** ✅ READY FOR PUBLISHER SUBMISSION
