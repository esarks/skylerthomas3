#!/usr/bin/env python3
"""
Populate Beyond the Swamp chapter outlines with extracted song lyrics

Uses the extracted lyrics files to populate chapter outline markdown files.
Author owns copyright to all songs.
"""

import os
import re

LYRICS_DIR = '/Users/paulmarshall/Documents/GitHub/skylerthomas3/extracted_lyrics'
WIKI_DIR = '/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki'

# Song-to-chapter file mapping
CHAPTER_MAPPING = {
    'Named_By_God': 'BeyondTheSwamp_01_Chapter-Named-By-God.md',
    'In_His_Image': 'BeyondTheSwamp_02_Chapter-In-His-Image.md',
    'You_Still_Know_My_Name': 'BeyondTheSwamp_03_Chapter-You-Still-Know-My-Name.md',
    'Why_Didnt_You_Tell_Me': 'BeyondTheSwamp_04_Chapter-Why-Didnt-You-Tell-Me.md',
    'Fruit_of_His_Spirit': 'BeyondTheSwamp_06_Chapter-Fruit-of-Spirit.md',
    'I_Will_Serve': 'BeyondTheSwamp_08_Chapter-I-Will-Serve.md',
    'No_Good_Deed': 'BeyondTheSwamp_09_Chapter-No-Good-Deed.md',
    'The_Rose': 'BeyondTheSwamp_Complete_Movements_3-5.md',
}

# Also add short URLs to chapters
SHORT_URLS = {
    'In_His_Image': 'https://go.skylerthomas.com/ZazW6B',
    'You_Still_Know_My_Name': 'https://go.skylerthomas.com/wjfV2i',
    'Why_Didnt_You_Tell_Me': 'https://go.skylerthomas.com/f1s0eM',
    'Fruit_of_His_Spirit': 'https://go.skylerthomas.com/1zoXHD',
    'What_is_Prayer': 'https://go.skylerthomas.com/DsW60X',
    'Holy_Communion': 'https://go.skylerthomas.com/TmvEwb',
    'Lord_We_Lift_Our_Hearts': 'https://go.skylerthomas.com/RENVkp',
    'When_the_Promise_Hurts': 'https://go.skylerthomas.com/Q7HEmZ',
    'Forgiveness_Requires_Remembrance': 'https://go.skylerthomas.com/XpS8to',
    'The_Rose': 'https://go.skylerthomas.com/EcOXbS',
}

def read_lyrics_file(song_key):
    """Read extracted lyrics from file"""
    filepath = os.path.join(LYRICS_DIR, f"{song_key}.txt")

    if not os.path.exists(filepath):
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip header lines
    lines = content.split('\n')
    lyrics_lines = []
    skip_header = True

    for line in lines:
        if skip_header and '=' in line:
            skip_header = False
            continue
        if not skip_header:
            lyrics_lines.append(line)

    return '\n'.join(lyrics_lines).strip()

def update_chapter_file(chapter_file, song_key):
    """Update chapter file with lyrics and short URL"""
    filepath = os.path.join(WIKI_DIR, chapter_file)

    if not os.path.exists(filepath):
        print(f"  ⚠️  File not found: {chapter_file}")
        return False

    # Read chapter file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get lyrics
    lyrics = read_lyrics_file(song_key)
    if not lyrics:
        print(f"  ⚠️  No lyrics file for {song_key}")
        return False

    modified = False

    # Update song URL if available
    if song_key in SHORT_URLS:
        short_url = SHORT_URLS[song_key]

        # Replace URL placeholder
        if '*[To be added:' in content and 'skylerthomas.com' in content:
            content = re.sub(
                r'\*\[To be added: https://www\.skylerthomas\.com/\.\.\.\]\*',
                short_url,
                content
            )
            modified = True

    # Update lyrics
    if '*[To be added: Full lyrics' in content:
        # Replace lyrics placeholder
        content = re.sub(
            r'\*\[To be added: Full lyrics.*?\]\*',
            lyrics,
            content,
            flags=re.DOTALL
        )
        modified = True

    if modified:
        # Write updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    else:
        print(f"  ℹ️  No placeholders found in {chapter_file}")
        return False

def main():
    print("="*70)
    print("POPULATING CHAPTER FILES WITH LYRICS")
    print("="*70)
    print()

    if not os.path.exists(LYRICS_DIR):
        print(f"❌ Lyrics directory not found: {LYRICS_DIR}")
        print("   Run extract_lyrics_from_export.py first")
        return

    updated_count = 0

    for song_key, chapter_file in CHAPTER_MAPPING.items():
        print(f"Processing: {song_key.replace('_', ' ')}")

        if update_chapter_file(chapter_file, song_key):
            print(f"  ✅ Updated: {chapter_file}")
            updated_count += 1
        else:
            print(f"  ⚠️  Not updated: {chapter_file}")
        print()

    print("="*70)
    print(f"SUMMARY: Updated {updated_count} chapter files")
    print("="*70)
    print()
    print("Next steps:")
    print("1. Review updated chapter files in skylerthomas3.wiki")
    print("2. Check lyrics formatting (verse/chorus labels)")
    print("3. Verify short URLs are correct")
    print("="*70)

if __name__ == '__main__':
    main()
