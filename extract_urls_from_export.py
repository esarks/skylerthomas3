#!/usr/bin/env python3
"""
Extract song URLs from WordPress export
"""

import re
from pathlib import Path

EXPORT_FILE = '/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-14.xml'

# Song titles to search for (from chapter outlines)
SONGS_TO_FIND = {
    'Named By God': 1,
    'In His Image': 2,
    'You Still Know My Name': 3,
    'Why Didn\'t You Tell Me': 4,
    'Why Didn\'t You Tell Me About Jesus': 4,  # alternate title
    'Fruit of His Spirit': 5,
    'The Rhythm of Life': 6,
    'Rhythm of Life': 7,
    'I Will Serve': 9,
    'No Good Deed': 8,
    'One Note': 11,
    'What Will You Say': 12,
    'Slip and Slide': 13,
    'The Heart of Glass': 14,
    'Heart of Glass': 15,
    'The Battle Is Won': 16,
    'What\'s Heaven Like': 17,
    'The Rose': 18
}

def extract_song_urls(export_file):
    """Extract URLs for all songs from WordPress export"""

    with open(export_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into items
    items = content.split('<item>')

    song_urls = {}

    for item in items[1:]:  # Skip first split (before first item)
        # Extract title
        title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
        if not title_match:
            continue

        title = title_match.group(1).strip()

        # Extract link/URL
        link_match = re.search(r'<link>(.*?)</link>', item)
        if not link_match:
            continue

        url = link_match.group(1).strip()

        # Check if this is one of our songs
        for song_title, chapter_num in SONGS_TO_FIND.items():
            if song_title.lower() in title.lower():
                song_urls[chapter_num] = {
                    'title': title,
                    'url': url,
                    'chapter': chapter_num
                }
                print(f"Found Chapter {chapter_num:2d}: {title}")
                print(f"  URL: {url}")
                break

    return song_urls

def main():
    print("Extracting song URLs from WordPress export...")
    print("=" * 70)

    song_urls = extract_song_urls(EXPORT_FILE)

    print("=" * 70)
    print(f"\nFound {len(song_urls)} song URLs\n")

    # Display organized list
    print("Chapter | Title | URL")
    print("-" * 70)
    for chapter_num in sorted(song_urls.keys()):
        song = song_urls[chapter_num]
        print(f"{chapter_num:2d} | {song['title'][:30]:30s} | {song['url']}")

    # Save to JSON for use in other scripts
    import json
    output_file = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/extracted_song_urls.json')
    with open(output_file, 'w') as f:
        json.dump(song_urls, f, indent=2)

    print(f"\n✓ Saved to: {output_file}")

if __name__ == '__main__':
    main()
