#!/usr/bin/env python3
"""
Extract song lyrics from WordPress export (text-based parsing)
Handles malformed XML by reading as plain text
"""

import re
import os

EXPORT_FILE = '/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-14.xml'
OUTPUT_DIR = '/Users/paulmarshall/Documents/GitHub/skylerthomas3/extracted_lyrics'

# Songs we're looking for
SONG_TITLES = [
    'Named By God',
    'In His Image',
    'You Still Know My Name',
    'Why Didn\'t You Tell Me',
    'Fruit of His Spirit',
    'Fruit of the Spirit',
    'Rhythm of Life',
    'I Will Serve',
    'No Good Deed',
    'What is Prayer',
    'One Note',
    'Holy Communion',
    'Lord We Lift Our Hearts',
    'When the Promise Hurts',
    'Heart of Glass',
    'Forgiveness Requires Remembrance',
    'Battle Is Won',
    'What\'s Heaven Like',
    'The Rose',
]

def extract_lyrics_from_text():
    """Read export as text and extract song content"""

    print(f"Reading export file: {EXPORT_FILE}\n")

    with open(EXPORT_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split into items (posts)
    items = content.split('<item>')

    print(f"Found {len(items)} items in export\n")

    found_songs = {}

    for item in items:
        # Extract title
        title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
        if not title_match:
            continue

        title = title_match.group(1)

        # Check if this is a song we're looking for
        is_target_song = False
        matched_song = None

        for song_title in SONG_TITLES:
            if song_title.lower() in title.lower():
                is_target_song = True
                matched_song = song_title
                break

        if is_target_song:
            print(f"Found: {title}")

            # Extract content
            content_match = re.search(r'<content:encoded><!\[CDATA\[(.*?)\]\]></content:encoded>', item, re.DOTALL)

            if content_match:
                song_content = content_match.group(1)

                # Clean up HTML
                song_content = re.sub(r'<[^>]+>', '\n', song_content)
                song_content = re.sub(r'\[.*?\]', '', song_content)
                song_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', song_content)
                song_content = song_content.strip()

                # Store with cleaned title
                clean_title = re.sub(r'[^\w\s-]', '', matched_song).strip()
                found_songs[clean_title] = {
                    'title': title,
                    'content': song_content
                }

                print(f"  ✓ Extracted lyrics ({len(song_content)} characters)\n")

    return found_songs

def save_extracted_lyrics(songs_dict):
    """Save extracted lyrics to individual files"""

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"\nSaving lyrics to: {OUTPUT_DIR}\n")

    for song_key, song_data in songs_dict.items():
        filename = f"{song_key.replace(' ', '_')}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Song: {song_data['title']}\n")
            f.write("="*60 + "\n\n")
            f.write(song_data['content'])

        print(f"  ✓ Saved: {filename}")

    # Also create a summary file
    summary_file = os.path.join(OUTPUT_DIR, '_SUMMARY.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("Extracted Song Lyrics Summary\n")
        f.write("="*60 + "\n\n")
        f.write(f"Total songs extracted: {len(songs_dict)}\n\n")

        for song_key in sorted(songs_dict.keys()):
            f.write(f"  - {song_key}\n")

    print(f"\n  ✓ Created summary: _SUMMARY.txt")

def main():
    print("="*70)
    print("EXTRACTING SONG LYRICS FROM WORDPRESS EXPORT")
    print("="*70)
    print()

    # Extract lyrics
    songs = extract_lyrics_from_text()

    if not songs:
        print("\n❌ No song lyrics found")
        return

    print(f"\n{'='*70}")
    print(f"EXTRACTED {len(songs)} SONGS")
    print("="*70)

    # Save to files
    save_extracted_lyrics(songs)

    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print(f"1. Review extracted lyrics in: {OUTPUT_DIR}")
    print("2. Check formatting and verse/chorus labels")
    print("3. Manually copy lyrics into chapter outline files")
    print("   (Look for '*[To be added: Full lyrics...]' sections)")
    print("="*70)

if __name__ == '__main__':
    main()
