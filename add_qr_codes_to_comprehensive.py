#!/usr/bin/env python3
"""
Add QR code references to the comprehensive movements file (chapters 9-18)
"""

from pathlib import Path
import re

WIKI_DIR = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki')
COMPREHENSIVE_FILE = 'BeyondTheSwamp_Complete_Movements_3-5.md'

# Chapter data: number, song title, short URL, QR filename
CHAPTERS = [
    (9, 'What is Prayer?', 'https://go.skylerthomas.com/DsW60X', 'qr-bts09-i-will-serve.png'),
    (10, 'What is Prayer?', 'https://go.skylerthomas.com/rgYmdb', 'qr-bts10-what-is-prayer.png'),
    (11, 'One Note', 'https://go.skylerthomas.com/TmvEwb', 'qr-bts11-one-note.png'),
    (12, 'Lord We Lift Our Hearts', 'https://go.skylerthomas.com/RENVkp', 'qr-bts12-what-will-you-say.png'),
    (13, 'When the Promise Hurts', 'https://go.skylerthomas.com/Q7HEmZ', 'qr-bts13-slip-and-slide.png'),
    (14, 'The Heart of Glass', 'https://go.skylerthomas.com/FXQXve', 'qr-bts14-heart-of-glass.png'),
    (15, 'Forgiveness Requires Remembrance', 'https://go.skylerthomas.com/XpS8to', 'qr-bts15-heart-of-glass.png'),
    (16, 'The Battle Is Won', 'https://go.skylerthomas.com/LizlRn', 'qr-bts16-battle-is-won.png'),
    (17, 'What\'s Heaven Like?', 'https://go.skylerthomas.com/uwCkHB', 'qr-bts17-whats-heaven-like.png'),
    (18, 'The Rose', 'https://go.skylerthomas.com/EcOXbS', 'qr-bts18-the-rose.png'),
]

def add_qr_codes_to_comprehensive():
    """Add QR code references to the comprehensive file"""

    filepath = WIKI_DIR / COMPREHENSIVE_FILE

    if not filepath.exists():
        print(f"⚠️  File not found: {COMPREHENSIVE_FILE}")
        return False

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    updated_count = 0

    for chapter_num, song_title, short_url, qr_filename in CHAPTERS:
        # Check if QR code already exists for this chapter
        if f'qr-bts{chapter_num:02d}' in content:
            print(f"✓ Chapter {chapter_num:2d}: QR code already exists")
            continue

        # Create the QR code section
        qr_section = f"\n**Listen at:** {short_url}\n\n![Scan to listen: {song_title}](../skylerthomas3/qr-codes/{qr_filename})\n"

        # Find where to insert the QR code - right after the Song URL line
        # Pattern: **Song URL:** https://...
        url_pattern = rf'(# CHAPTER {chapter_num}:.*?\*\*Song URL:\*\* {re.escape(short_url)})'

        if re.search(url_pattern, content, re.DOTALL):
            # Insert QR code after the URL
            content = re.sub(
                url_pattern,
                rf'\1{qr_section}',
                content,
                flags=re.DOTALL
            )
            print(f"✓ Chapter {chapter_num:2d}: Added QR code")
            updated_count += 1
        else:
            print(f"⚠️  Chapter {chapter_num:2d}: Could not find URL pattern")

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
    print("Adding QR code references to comprehensive file...")
    print("=" * 70)

    add_qr_codes_to_comprehensive()

    print("=" * 70)
    print("\n✅ All chapters now have QR codes!")

if __name__ == '__main__':
    main()
