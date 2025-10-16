# Out of the Swamp - Publisher's Review Edition

## Project Overview

This repository contains the publisher's review version of **"Out of the Swamp: How I Found Truth"** by Skyler Thomas. This is a Christian memoir/spiritual journey that integrates original songs throughout the narrative, following a three-movement structure: In the Swamp → At the Water's Edge → Unforced Rhythms of Grace.

This project (skylerthomas3) represents a revision from the previous version (skylerthomas2), focusing on preparing the manuscript for publisher review.

## Book Structure

**Three-Movement Narrative:**
- **Movement 1: In the Swamp** (Chapters 1-4) - Crisis, burnout, and the cry for help
- **Movement 2: At the Water's Edge** (Chapters 5-8) - Encountering grace and transformation
- **Movement 3: Unforced Rhythms of Grace** (Chapters 9+) - Sustainable spiritual practices

**Key Features:**
- Original songs integrated as chapter foundations
- QR codes linking to song recordings
- Personal narrative woven with theological reflection
- Target audience: burned out, broken, skeptical readers

## Key Files

### Main Manuscript
- `publish-editor.md` - Editorial review and analysis of the complete manuscript (~336KB, ~6,600 lines)

### Python Scripts (Song & Lyrics Management)
- `populate_song_lyrics.py` - Populates database with song lyrics
- `extract_lyrics_from_export.py` - Extracts lyrics from WordPress export
- `populate_chapters_with_lyrics.py` - Adds lyrics to chapter content
- `extract_playlist.py` - Extracts playlist information
- `identify_unused_songs.py` - Finds songs not used in chapters
- `create_songs_table.py` - Creates songs database table

### Python Scripts (URL & QR Code Management)
- `generate_qr_codes.py` - Generates QR codes for song URLs
- `add_qr_codes_to_chapters.py` - Embeds QR codes in chapter documents
- `add_qr_codes_to_comprehensive.py` - Adds QR codes to comprehensive version
- `update_chapter_urls.py` - Updates URLs in chapter content
- `update_comprehensive_urls.py` - Updates URLs in comprehensive document
- `update_in_his_image.py` - Updates specific chapter URLs

### JavaScript Scripts (URL Shortening)
- `create-missing-short-links.js` - Creates new shortened URLs via Short.io
- `create-final-short-links.js` - Generates final shortened URLs
- `update-in-his-image-url.js` - Updates specific chapter URL

### Workflow Files (Publisher Editing)
- `workflows/publisher_edit_workflow.py` - Main workflow orchestration script
- `workflows/WORKFLOW3-GUIDE.md` - Complete workflow guide and documentation
- `workflows/QUICK-REFERENCE.md` - Quick reference card for workflow
- `workflows/workflow_config.json` - Workflow configuration and settings
- `workflows/workflow_state.json` - Current workflow state tracking
- `.claude/commands/workflow3.md` - Slash command to execute workflow

### Documentation
- `COMPLETE_URL_QR_Summary.md` - Summary of URL and QR code implementation
- `BeyondTheSwamp_URL_QR_Status.md` - Status of URL/QR updates
- `Chapter-7-Removal-Summary.md` - Documentation of Chapter 7 removal
- `FINAL_COMPLETION_Summary.md` - Final completion notes
- `In-His-Image-Update-Summary.md` - Updates to specific chapter
- `unusedsongs.md` - List of songs not currently used
- `skylerthomas3.wiki/MOVEMENT-1-REVISION-SUMMARY.md` - Completed Movement 1 revisions

### Data Files
- `extracted_song_urls.json` - Song URLs extracted from WordPress
- `final-short-links.json/txt` - Final shortened URLs
- `new-short-links.json/txt` - Newly created shortened URLs
- `extracted_lyrics/` - Directory containing individual song lyrics

### Generated Content
- `qr-codes/` - QR code images for songs
- `archived_chapters/` - Previous chapter versions

## WordPress Integration

The project integrates with a WordPress site at **skylerthomas.com** where songs are hosted.

### Environment Variables (.env)
```
WP_SITE_URL - WordPress site URL
WP_USERNAME - WordPress admin username
WP_APP_PASSWORD - WordPress application password
SHORT_IO_API_KEY - Short.io API key for URL shortening
```

**Note:** The `.env` file contains sensitive credentials and should never be committed to version control.

## Technical Dependencies

### Python
- Used for database operations, lyrics extraction, QR code generation
- Scripts interact with WordPress API
- QR code generation (likely using `qrcode` library)

### Node.js
- Package dependencies in `package.json`
- Used for Short.io API integration
- Axios and dotenv for API calls

## Workflow Overview

### Technical Workflow
1. **Song Management**: Songs are hosted on WordPress, lyrics are extracted and stored
2. **URL Shortening**: Short.io creates memorable short links for each song
3. **QR Code Generation**: QR codes are generated for each song URL
4. **Document Integration**: QR codes and links are embedded in chapter documents
5. **Version Control**: Changes tracked through summary documents

### Publisher Editing Workflow (Workflow 3)

**Execute with:** `/workflow3` or `python3 workflows/publisher_edit_workflow.py`

This is the structured editorial revision process for the publisher's review edition.

**Core Principle:** THE PRIMARY PURPOSE OF THIS BOOK IS TO FEATURE THE AUTHOR'S SONGS
- Songs should NOT be removed without explicit author approval
- When in doubt, revise the narrative to fit the song, not vice versa

**Workflow Steps:**
1. Check current status and movement progress
2. Review editorial feedback from `publish-editor.md`
3. Make revisions in `skylerthomas3.wiki/`
4. Track all changes (especially song decisions)
5. Generate comprehensive revision summaries

**Key Files:**
- `workflows/publisher_edit_workflow.py` - Main orchestration script
- `workflows/WORKFLOW3-GUIDE.md` - Complete workflow documentation
- `workflows/QUICK-REFERENCE.md` - Quick reference card
- `workflows/workflow_config.json` - Configuration settings
- `workflows/workflow_state.json` - Current workflow state

**Movement Status:**
- ✓ Movement 1: Completed (4 chapters → 2 chapters, 2 songs kept)
- ○ Movement 2: Pending (4 chapters, all songs strong)
- ○ Movement 3: Pending (6 chapters, needs personal narrative)

See `workflows/WORKFLOW3-GUIDE.md` for complete documentation.

## Current Status

This is the publisher's review version. The editorial review (in `publish-editor.md`) provides comprehensive feedback on:
- Overall coherence and narrative arc
- Structural issues by movement/chapter
- Content recommendations for revision
- Publication readiness assessment

**Overall Grade: B-/C+** - Significant potential but requires substantial editing before publication.

## Development Notes

### Key Changes from skylerthomas2
- Migration to publisher's review format
- Chapter 7 was removed (documented in Chapter-7-Removal-Summary.md)
- URL structure updates
- QR code implementation
- Comprehensive editing review

### Working with This Repository

When making changes:
1. Update relevant Python/JS scripts if changing song/URL structure
2. Regenerate QR codes if URLs change
3. Document significant changes in appropriate summary files
4. Test WordPress integration after credential/URL changes
5. Keep .env file secure and never commit it

## Contact & Publishing

**Author:** Skyler Thomas
**Website:** skylerthomas.com
**Project Stage:** Publisher's Review
**Repository:** skylerthomas3 (current) ← skylerthomas2 (previous)
