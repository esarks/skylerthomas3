#!/bin/bash

# WordPress Sync File List for Publisher Edition (skylerthomas3)
# Includes: 3 movement intros, 12 chapters, and epilogue
# Excludes: Title, copyright, dedication, introduction, about author
# Comment out files you don't want to sync (add # at the beginning of the line)
# Uncomment files you want to sync (remove # from the beginning of the line)

FILES=(
    # INTRODUCTION
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-00_introduction-PUBLISHER.md"

    # MOVEMENT 1: IN THE SWAMP
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-01_movement-1-intro.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-02_chapter-01-my-swamp.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-03_chapter-02-but-then-i-prayed.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-04_chapter-03-dying-changes.md"

    # MOVEMENT 2: AT THE WATER'S EDGE
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-06_movement-2-intro.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-07_chapter-04-living-waters-edge.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-08_chapter-05-shadow-grace.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-09_chapter-06-amazing-grace.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-10_chapter-07-dig-deeper.md"

    # MOVEMENT 3: UNFORCED RHYTHMS
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-11_movement-3-intro.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-12_chapter-08-unforced-rhythms.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-13_chapter-09-deep-roots.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-14_chapter-10-redemption-story.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-15_chapter-11-nothing-wasted.md"
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-16_chapter-12-this-moment.md"

    # Epilogue
    "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki/REVISED-99_epilogue.md"
)

# EXCLUDED (not included in sync):
# - REVISED-00_title-page.md (front matter)
# - REVISED-00_copyright-page.md (front matter)
# - REVISED-00_dedication.md (front matter)
# - REVISED-99_about-author.md (back matter)

# INCLUDED:
# - 1 introduction
# - 3 movement intros
# - 12 chapters
# - 1 epilogue
# Total: 17 files
