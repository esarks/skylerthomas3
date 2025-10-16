# WORKFLOW3 - PUBLISHER VERSION PRODUCTION SYSTEM

**Status:** Production-ready for publisher version
**Trigger Command:** "Execute workflow3"
**Date Created:** October 16, 2025

---

## WHAT IS WORKFLOW3?

WORKFLOW3 is the NEW production system for the **publisher-ready revised version** of "Out of the Swamp: How I Found Truth".

This workflow produces the REVISED book with:
- **Editorial improvements** based on professional review
- **Tighter structure:** 12 chapters (down from 14)
- **50% reduction in Movement 1** (4 chapters → 2 chapters)
- **Eliminated redundancy** throughout
- **Improved pacing and clarity**

---

## DIRECTORY STRUCTURE

```
skylerthomas3/
├── WORKFLOW3-README.md                  ← This file
├── publish-editor.md                    ← Editorial review (from skylerthomas2)
│
├── workflow3_production_scripts/        ← Production scripts
│   ├── run_workflow3.py                 ← MASTER RUNNER
│   ├── create_complete_manuscript.py    ← Step 1
│   ├── create_pdf_kdp_ready.py          ← Step 2
│   └── create_epub.py                   ← Step 3
│
└── KDP/                                 ← Output folder
    ├── COMPLETE-MANUSCRIPT.md           ← Combined manuscript
    ├── OUT-OF-THE-SWAMP-PUBLISHER.pdf   ← Publisher PDF
    └── OUT-OF-THE-SWAMP-PUBLISHER.epub  ← Publisher EPUB

/skylerthomas3.wiki/                     ← Source chapters
├── REVISED-01_movement-1-intro.md
├── REVISED-02_chapter-01-my-swamp.md    ← Merged (Ch 1+2)
├── REVISED-05_chapter-04-dying-changes.md
├── REVISED-06_movement-2-intro.md       ← TO DO
├── REVISED-07_chapter-03-*.md           ← TO DO
└── ... (more chapters as revised)
```

---

## HOW TO USE WORKFLOW3

### TRIGGER COMMAND (In Claude):
Say: **"Execute workflow3"**

### Manual Execution:
```bash
cd /Users/paulmarshall/Documents/GitHub/skylerthomas3/workflow3_production_scripts
python3 run_workflow3.py
```

This runs all 3 steps:
1. ✅ Creates complete manuscript from REVISED chapters
2. ✅ Generates KDP-ready PDF (publisher version)
3. ✅ Generates EPUB (publisher version)

**Output:** All files in `/skylerthomas3/KDP/`

---

## REVISED BOOK STRUCTURE

### Current Status:

| Movement | Chapters | Status |
|----------|----------|--------|
| **Movement 1** | 2 chapters | ✅ REVISED |
| **Movement 2** | 4 chapters | ⏳ TO DO |
| **Movement 3** | 6 chapters | ⏳ TO DO |

### Movement 1: In the Swamp (REVISED ✅)

**Chapter 1: My Swamp**
- File: `REVISED-02_chapter-01-my-swamp.md`
- Status: ✅ Complete (merged from original Ch 1+2)
- Word count: 3,085 (down from 6,100)

**Chapter 2: Dying Changes Everything**
- File: `REVISED-05_chapter-04-dying-changes.md`
- Status: ✅ Complete (light edit from original Ch 4)
- Word count: 2,608 (down from 2,900)

**Deleted:**
- Original Chapter 3 (rap format) - removed

### Movement 2: At the Water's Edge (TO DO ⏳)

Chapters 3-6 to be revised:
- Chapter 3: Living Waters Edge (needs 40% cut)
- Chapter 4: Shadow of Your Grace (needs 25% cut)
- Chapter 5: Amazing Grace (needs 30% cut)
- Chapter 6: Dig a Little Deeper (needs 10% trim)

### Movement 3: Unforced Rhythms (TO DO ⏳)

Chapters 7-12 to be revised:
- Needs more personal narrative
- Less theology lecture
- Concrete "present day" examples

---

## WORKFLOW3 vs WORKFLOW2

| Feature | WORKFLOW2 | WORKFLOW3 |
|---------|-----------|-----------|
| **Version** | Original | Publisher-ready |
| **Chapters** | 14 | 12 (target) |
| **Word Count** | ~70,000 | ~50,000 (target) |
| **Movement 1** | 4 chapters | 2 chapters ✅ |
| **Status** | FROZEN | IN PROGRESS |
| **Location** | skylerthomas2 | skylerthomas3 |
| **Output** | OUT-OF-THE-SWAMP-KDP-READY.pdf | OUT-OF-THE-SWAMP-PUBLISHER.pdf |

---

## EDITORIAL IMPROVEMENTS (from publish-editor.md)

WORKFLOW3 implements the following improvements:

### ✅ Completed (Movement 1):
- Merged Ch 1+2 → single powerful opening
- Deleted Ch 3 (rap format) - tonal clash
- Cut 50% of redundancy
- Reduced theologian quotes by 65%
- Eliminated "Three R's of Prayer" gimmick
- Added decision moment to Ch 1 ending

### ⏳ In Progress (Movements 2-3):
- Cut 30-40% from Movement 2 chapters
- Add personal narrative to Movement 3
- Expand Lake Hefner scene
- Add "present day" concrete examples
- Remove spiritual warfare chapter (Ch 13) or move to appendix

### Target Metrics:
- **Total word count:** 50,000-55,000 (from 70,000)
- **Total chapters:** 12 (from 14)
- **Redundancy:** Eliminated (each concept appears once)
- **Voice:** Consistent vulnerable memoir throughout

---

## FILES NEEDED (TO DO)

WORKFLOW3 is waiting for these files to be created in `skylerthomas3.wiki/`:

### Front Matter (copy/adapt from skylerthomas2):
- 00_title-page.md
- 00_copyright-page.md
- 00_dedication.md
- 00_table-of-contents.md
- 00_introduction.md

### Movement 2 (4 chapters to revise):
- REVISED-06_movement-2-intro.md
- REVISED-07_chapter-03-living-waters-edge.md
- REVISED-08_chapter-04-shadow-grace.md
- REVISED-09_chapter-05-amazing-grace.md
- REVISED-10_chapter-06-dig-deeper.md

### Movement 3 (6 chapters to revise):
- REVISED-11_movement-3-intro.md
- REVISED-12_chapter-07-unforced-rhythms.md
- REVISED-13_chapter-08-deep-roots.md
- REVISED-14_chapter-09-redemptions-story.md
- REVISED-15_chapter-10-nothing-wasted.md
- REVISED-16_chapter-11-this-moment.md

### Back Matter (copy/adapt from skylerthomas2):
- 99_epilogue.md
- 99_about-author.md

---

## RUNNING PARTIAL BUILDS

You can run WORKFLOW3 even with incomplete chapters. The workflow will:
1. ✅ Include all REVISED files that exist
2. ⚠️ Note which files are still pending
3. ✅ Build PDF/EPUB with available content

This lets you test the build process as chapters are revised.

---

## TRIGGER COMMANDS

| Command | Action |
|---------|--------|
| **"Execute workflow3"** | Run complete publisher workflow |
| **"Run workflow2"** | Run original 14-chapter workflow |
| **"Build the current book"** | Run WORKFLOW2 (original) |
| **"Build the publisher version"** | Run WORKFLOW3 (revised) |

---

## NEXT STEPS

To complete WORKFLOW3:

1. ✅ **Movement 1** - DONE
2. ⏳ **Create front matter** - Copy/adapt from skylerthomas2
3. ⏳ **Revise Movement 2** - Chapters 3-6 (Phase 1, Week 3-4)
4. ⏳ **Revise Movement 3** - Chapters 7-12 (Phase 1, Week 5-6)
5. ⏳ **Create back matter** - Copy/adapt from skylerthomas2
6. ✅ **Final build** - Complete publisher-ready version

Estimated timeline: **3-6 months** following editorial roadmap in `publish-editor.md`

---

## IMPORTANT NOTES

- **WORKFLOW2 stays frozen** - Original 14-chapter version preserved
- **WORKFLOW3 is active** - Publisher version in progress
- **No conflicts** - Completely separate systems
- **Both work** - Can build either version independently

---

**WORKFLOW3 Status:** ACTIVE - Ready for publisher version production
**Last Updated:** October 16, 2025
**Trigger:** "Execute workflow3"
