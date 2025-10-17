# WordPress Sync Scripts - Publisher Edition

## Overview

This directory contains WordPress sync scripts for the **Publisher Edition** (12 chapters, revised).

## Files Created

### sync2.sh
Main sync script that processes all files in sync-list2.sh and uploads them to WordPress.

### sync-list2.sh
File list containing **movement intros, chapters, and epilogue** from skylerthomas3.wiki:
- 3 movement intros (REVISED-01, REVISED-06, REVISED-11)
- 12 chapters (REVISED-02 through REVISED-16)
- 1 epilogue (REVISED-99)
- **Total: 16 files**

## What's Excluded

The following files are **NOT** synced to WordPress:
- ❌ Title page
- ❌ Copyright page
- ❌ Dedication
- ❌ Introduction
- ❌ About Author page

## Dependencies

### Shared Dependency
Both the old sync.sh and new sync2.sh use the **same** wp-sync-rest.js script located at:
```
/Users/paulmarshall/Documents/GitHub/SkylerThomas/wp-sync-rest.js
```

### Original Files (UNCHANGED)
The original sync system remains intact:
- `/Users/paulmarshall/Documents/GitHub/SkylerThomas/sync.sh`
- `/Users/paulmarshall/Documents/GitHub/SkylerThomas/sync-list.sh`
- `/Users/paulmarshall/Documents/GitHub/SkylerThomas/wp-sync-rest.js`

## How to Use

### Sync Publisher Edition Chapters
```bash
cd /Users/paulmarshall/Documents/GitHub/skylerthomas3
./sync2.sh
```

### Sync Original Version (14 chapters)
```bash
cd /Users/paulmarshall/Documents/GitHub/SkylerThomas
./sync.sh
```

## Environment Setup

Required: `.env` file in the SkylerThomas directory with:
```
WP_SITE_URL=https://www.skylerthomas.com
WP_USERNAME=your-username
WP_APP_PASSWORD=your-app-password
```

## Verification Method

The sync-list2.sh file includes:
1. Movement intros: `REVISED-01`, `REVISED-06`, `REVISED-11`
2. All chapters: `REVISED-*chapter*.md` files
3. Epilogue: `REVISED-99_epilogue.md`
4. Verified count: 16 files (3 movement intros + 12 chapters + 1 epilogue)

## File Mapping

| File | WordPress Post |
|------|---------------|
| REVISED-01_movement-1-intro.md | Movement 1: In the Swamp |
| REVISED-02_chapter-01-my-swamp.md | Chapter 1: My Swamp |
| REVISED-03_chapter-02-but-then-i-prayed.md | Chapter 2: But Then I Prayed |
| REVISED-04_chapter-03-dying-changes.md | Chapter 3: Dying Changes |
| REVISED-06_movement-2-intro.md | Movement 2: At the Water's Edge |
| REVISED-07_chapter-04-living-waters-edge.md | Chapter 4: Living Water's Edge |
| REVISED-08_chapter-05-shadow-grace.md | Chapter 5: Shadow Grace |
| REVISED-09_chapter-06-amazing-grace.md | Chapter 6: Amazing Grace |
| REVISED-10_chapter-07-dig-deeper.md | Chapter 7: Dig a Little Deeper |
| REVISED-11_movement-3-intro.md | Movement 3: Unforced Rhythms |
| REVISED-12_chapter-08-unforced-rhythms.md | Chapter 8: Unforced Rhythms |
| REVISED-13_chapter-09-deep-roots.md | Chapter 9: Deep Roots |
| REVISED-14_chapter-10-redemption-story.md | Chapter 10: Redemption Story |
| REVISED-15_chapter-11-nothing-wasted.md | Chapter 11: Nothing Wasted |
| REVISED-16_chapter-12-this-moment.md | Chapter 12: This Moment |
| REVISED-99_epilogue.md | Epilogue |

## Notes

- Each file's frontmatter contains `wp_post_id` linking it to the WordPress post
- The sync script automatically updates the `last_updated` timestamp
- The first H1 heading becomes the WordPress post title
- Markdown is converted to HTML with MP3 links converted to WordPress audio shortcodes
