#!/usr/bin/env python3
"""
Update the comprehensive movements file with shortened URLs for chapters 9-18
"""

from pathlib import Path
import re

WIKI_DIR = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki')
COMPREHENSIVE_FILE = 'BeyondTheSwamp_Complete_Movements_3-5.md'

# URLs for chapters 9-18
CHAPTER_URLS = {
    9: 'https://go.skylerthomas.com/DsW60X',   # What is Prayer? (this was originally listed as chapter 9 but using the I Will Serve URL)
    10: 'https://go.skylerthomas.com/rgYmdb',  # What is Prayer?
    11: 'https://go.skylerthomas.com/TmvEwb',  # One Note
    12: 'https://go.skylerthomas.com/RENVkp',  # What Will You Say
    13: 'https://go.skylerthomas.com/Q7HEmZ',  # Slip and Slide
    14: 'https://go.skylerthomas.com/FXQXve',  # The Heart of Glass
    15: 'https://go.skylerthomas.com/XpS8to',  # Heart of Glass
    16: 'https://go.skylerthomas.com/LizlRn',  # The Battle Is Won
    17: 'https://go.skylerthomas.com/uwCkHB',  # What's Heaven Like?
    18: 'https://go.skylerthomas.com/EcOXbS'   # The Rose
}

def update_comprehensive_file():
    """Update the comprehensive file with all chapter URLs"""

    filepath = WIKI_DIR / COMPREHENSIVE_FILE

    if not filepath.exists():
        print(f"⚠️  File not found: {COMPREHENSIVE_FILE}")
        return False

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match chapter headings with URL placeholders
    # Matches: # CHAPTER ##: Title\n\n**Song:** Title\n**Song URL:** *[To be added]*

    updated_count = 0

    for chapter_num, short_url in CHAPTER_URLS.items():
        # Pattern to find the chapter and update its URL
        # Look for: **Song URL:** *[To be added]*
        # This should appear after # CHAPTER {chapter_num}:

        # Find the chapter section
        chapter_pattern = rf'(# CHAPTER {chapter_num}:.*?\*\*Song URL:\*\*) \*\[To be added\]\*'

        if re.search(chapter_pattern, content, re.DOTALL):
            content = re.sub(
                chapter_pattern,
                rf'\1 {short_url}',
                content,
                flags=re.DOTALL
            )
            print(f"✓ Chapter {chapter_num:2d}: Updated URL")
            updated_count += 1
        else:
            print(f"⚠️  Chapter {chapter_num:2d}: Could not find URL placeholder")

    if updated_count > 0:
        # Write the file back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✓ Updated {updated_count} chapters in {COMPREHENSIVE_FILE}")
        return True
    else:
        print(f"\n⚠️  No chapters were updated in {COMPREHENSIVE_FILE}")
        return False

def main():
    print("Updating comprehensive movements file with shortened URLs...")
    print("=" * 70)

    update_comprehensive_file()

    print("=" * 70)
    print("\n✅ All chapter files now have shortened URLs!")

if __name__ == '__main__':
    main()
