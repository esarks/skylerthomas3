#!/usr/bin/env python3
"""
Update chapter markdown files with shortened URLs
"""

from pathlib import Path
import re

WIKI_DIR = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki')

# Chapter to URL mapping
CHAPTER_URLS = {
    1: 'https://go.skylerthomas.com/vTcEr9',
    2: 'https://go.skylerthomas.com/ZazW6B',
    3: 'https://go.skylerthomas.com/wjfV2i',
    4: 'https://go.skylerthomas.com/f1s0eM',
    5: 'https://go.skylerthomas.com/1zoXHD',
    6: 'https://go.skylerthomas.com/LQcPBi',
    7: 'https://go.skylerthomas.com/13Xedv',
    8: 'https://go.skylerthomas.com/oG6qwS',
    9: 'https://go.skylerthomas.com/DsW60X',
    10: 'https://go.skylerthomas.com/rgYmdb',
    11: 'https://go.skylerthomas.com/TmvEwb',
    12: 'https://go.skylerthomas.com/RENVkp',
    13: 'https://go.skylerthomas.com/Q7HEmZ',
    14: 'https://go.skylerthomas.com/FXQXve',
    15: 'https://go.skylerthomas.com/XpS8to',
    16: 'https://go.skylerthomas.com/LizlRn',
    17: 'https://go.skylerthomas.com/uwCkHB',
    18: 'https://go.skylerthomas.com/EcOXbS'
}

# Map chapter numbers to filenames
CHAPTER_FILES = {
    1: 'BeyondTheSwamp_01_Chapter-Named-By-God.md',
    2: 'BeyondTheSwamp_02_Chapter-In-His-Image.md',
    3: 'BeyondTheSwamp_03_Chapter-You-Still-Know-My-Name.md',
    4: 'BeyondTheSwamp_04_Chapter-Why-Didnt-You-Tell-Me.md',
    5: 'BeyondTheSwamp_06_Chapter-Fruit-of-Spirit.md',
    6: 'BeyondTheSwamp_07_Chapter-Rhythm-of-Life.md',
    7: 'BeyondTheSwamp_08_Chapter-I-Will-Serve.md',
    8: 'BeyondTheSwamp_09_Chapter-No-Good-Deed.md',
}

def update_chapter_url(chapter_num, filename, short_url):
    """Update a chapter file with the shortened URL"""

    filepath = WIKI_DIR / filename

    if not filepath.exists():
        print(f"⚠️  File not found: {filename}")
        return False

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match: **Song URL:** *[To be added: https://www.skylerthomas.com/...]*
    # or similar variations
    patterns = [
        r'\*\*Song URL:\*\* \*\[To be added:.*?\]\*',
        r'\*\*Song URL:\*\* \*To be added.*?\*',
        r'\*\*Song URL:\*\*.*?https://www\.skylerthomas\.com/[^\n]*',
    ]

    # Try each pattern
    updated = False
    for pattern in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, f'**Song URL:** {short_url}', content)
            updated = True
            break

    # If no pattern matched, try to add it after **Song:** line
    if not updated:
        song_line_pattern = r'(\*\*Song:\*\*[^\n]*\n)'
        if re.search(song_line_pattern, content):
            content = re.sub(
                song_line_pattern,
                f'\\1\n**Song URL:** {short_url}\n',
                content
            )
            updated = True

    if updated:
        # Write the file back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Chapter {chapter_num:2d}: Updated {filename}")
        return True
    else:
        print(f"⚠️  Chapter {chapter_num:2d}: Could not find URL placeholder in {filename}")
        return False

def main():
    print("Updating chapter files with shortened URLs...")
    print("=" * 70)

    updated_count = 0

    for chapter_num, filename in CHAPTER_FILES.items():
        short_url = CHAPTER_URLS[chapter_num]
        if update_chapter_url(chapter_num, filename, short_url):
            updated_count += 1

    print("=" * 70)
    print(f"✓ Updated {updated_count}/{len(CHAPTER_FILES)} chapter files")

    # Note about chapters 9-18
    print("\nNote: Chapters 9-18 are in BeyondTheSwamp_Complete_Movements_3-5.md")
    print("Those will need to be updated separately or split into individual files.")

if __name__ == '__main__':
    main()
