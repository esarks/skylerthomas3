#!/usr/bin/env python3
"""
Add QR code references to chapter markdown files
Uses the same format as Book 1
"""

from pathlib import Path
import re

WIKI_DIR = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki')

# Chapter data: number, filename, song title, short URL, QR filename
CHAPTERS = [
    (1, 'BeyondTheSwamp_01_Chapter-Named-By-God.md', 'Named By God',
     'https://go.skylerthomas.com/vTcEr9', 'qr-bts01-named-by-god.png'),
    (2, 'BeyondTheSwamp_02_Chapter-In-His-Image.md', 'In His Image',
     'https://go.skylerthomas.com/ZazW6B', 'qr-bts02-in-his-image.png'),
    (3, 'BeyondTheSwamp_03_Chapter-You-Still-Know-My-Name.md', 'You Still Know My Name',
     'https://go.skylerthomas.com/wjfV2i', 'qr-bts03-you-still-know-my-name.png'),
    (4, 'BeyondTheSwamp_04_Chapter-Why-Didnt-You-Tell-Me.md', 'Why Didn\'t You Tell Me About Jesus',
     'https://go.skylerthomas.com/f1s0eM', 'qr-bts04-why-didnt-you-tell-me.png'),
    (5, 'BeyondTheSwamp_06_Chapter-Fruit-of-Spirit.md', 'The Fruit of His Spirit',
     'https://go.skylerthomas.com/1zoXHD', 'qr-bts05-fruit-of-his-spirit.png'),
    (6, 'BeyondTheSwamp_07_Chapter-Rhythm-of-Life.md', 'The Rhythm of Life',
     'https://go.skylerthomas.com/LQcPBi', 'qr-bts06-rhythm-of-life.png'),
    (7, 'BeyondTheSwamp_08_Chapter-I-Will-Serve.md', 'I Will Serve',
     'https://go.skylerthomas.com/13Xedv', 'qr-bts07-i-will-serve.png'),
    (8, 'BeyondTheSwamp_09_Chapter-No-Good-Deed.md', 'No Good Deed',
     'https://go.skylerthomas.com/oG6qwS', 'qr-bts08-no-good-deed.png'),
]

def add_qr_code_to_chapter(chapter_num, filename, song_title, short_url, qr_filename):
    """Add QR code reference to a chapter file"""

    filepath = WIKI_DIR / filename

    if not filepath.exists():
        print(f"⚠️  File not found: {filename}")
        return False

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if QR code already exists
    if qr_filename in content:
        print(f"✓ Chapter {chapter_num:2d}: QR code already exists")
        return True

    # Create the QR code section
    qr_section = f"\n**Listen at:** {short_url}\n\n![Scan to listen: {song_title}](../skylerthomas3/qr-codes/{qr_filename})\n"

    # Find where to insert the QR code - right after the Song URL line
    # Pattern: **Song URL:** https://...
    url_pattern = rf'(\*\*Song URL:\*\* {re.escape(short_url)})'

    if re.search(url_pattern, content):
        # Insert QR code after the URL
        content = re.sub(
            url_pattern,
            rf'\1{qr_section}',
            content
        )

        # Write the file back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✓ Chapter {chapter_num:2d}: Added QR code to {filename}")
        return True
    else:
        print(f"⚠️  Chapter {chapter_num:2d}: Could not find URL in {filename}")
        return False

def main():
    print("Adding QR code references to chapter files...")
    print("=" * 70)

    updated_count = 0

    for chapter_num, filename, song_title, short_url, qr_filename in CHAPTERS:
        if add_qr_code_to_chapter(chapter_num, filename, song_title, short_url, qr_filename):
            updated_count += 1

    print("=" * 70)
    print(f"✓ Added QR codes to {updated_count}/{len(CHAPTERS)} chapter files")

if __name__ == '__main__':
    main()
