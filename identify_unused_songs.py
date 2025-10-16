#!/usr/bin/env python3
"""
Identify songs used in chapters vs unused songs from WordPress export
"""

import re
from pathlib import Path

EXPORT_FILE = '/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-14.xml'

# Songs used in the 17 chapters
SONGS_IN_CHAPTERS = [
    'Named By God',
    'In His Image',
    'You Still Know My Name',
    'Why Didn\'t You Tell Me About Jesus',
    'Fruit of His Spirit',
    'The Rhythm of Life',
    'Unforced Rhythms of Grace',  # Same as Rhythm of Life
    'No Good Deed',
    'What is Prayer',
    'One Note',
    'Holy Communion',
    'Lord We Lift Our Hearts',
    'When the Promise Hurts',
    'Slip and Slide',  # Check if this is in chapters
    'The Heart of Glass',
    'Heart of Glass',  # Variation
    'Forgiveness Requires Remembrance',
    'The Battle Is Won',
    'What\'s Heaven Like',
    'The Rose',
]

def extract_unique_songs(export_file):
    """Extract unique song titles from WordPress export"""

    with open(export_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all title tags
    titles = re.findall(r'<title><!\[CDATA\[(.*?)\]\]></title>', content)

    # Filter to songs and devotional entries
    songs = set()
    for title in titles:
        title = title.strip()
        # Include items with "Song" or "Devotional and Song"
        if 'Song' in title or 'Devotional' in title:
            # Clean up title
            title = title.replace('(Devotional and Song)', '').strip()
            title = title.replace('(Song)', '').strip()
            title = title.replace('Song:', '').strip()

            # Remove version indicators
            title = re.sub(r' - (Duet|Male Vocal|Female Vocal|A Cappella|Remastered|Instrumental|Remix|Studio Version|Acappella|Choral|Vocal Band).*', '', title)
            title = re.sub(r' \(Remastered\)', '', title)
            title = re.sub(r' V\d+$', '', title)  # Remove version numbers
            title = re.sub(r' \d+-\d+$', '', title)  # Remove version numbers like 4-5
            title = title.strip()

            if title and title != 'Songs Playlist':
                songs.add(title)

    return sorted(songs)

def normalize_song_name(name):
    """Normalize song name for comparison"""
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)  # Remove punctuation
    name = re.sub(r'\s+', ' ', name).strip()  # Normalize whitespace
    return name

def identify_used_and_unused(all_songs, songs_in_chapters):
    """Identify which songs are used vs unused"""

    # Normalize chapter songs for comparison
    normalized_chapter_songs = {normalize_song_name(s): s for s in songs_in_chapters}

    used_songs = []
    unused_songs = []

    for song in all_songs:
        normalized = normalize_song_name(song)

        # Check if this song matches any in chapters
        is_used = False
        for chapter_normalized, chapter_original in normalized_chapter_songs.items():
            if chapter_normalized in normalized or normalized in chapter_normalized:
                used_songs.append((song, chapter_original))
                is_used = True
                break

        if not is_used:
            unused_songs.append(song)

    return used_songs, unused_songs

def main():
    print("Analyzing songs from WordPress export...")
    print("=" * 70)

    # Extract all unique songs
    all_songs = extract_unique_songs(EXPORT_FILE)

    print(f"Total unique songs found: {len(all_songs)}\n")

    # Identify used vs unused
    used_songs, unused_songs = identify_used_and_unused(all_songs, SONGS_IN_CHAPTERS)

    print(f"Songs used in chapters: {len(used_songs)}")
    print(f"Songs NOT used in chapters: {len(unused_songs)}")
    print("=" * 70)

    # Display used songs
    print("\n=== SONGS USED IN CHAPTERS ===\n")
    for wordpress_title, chapter_title in sorted(set(used_songs)):
        print(f"✓ {wordpress_title}")
        if wordpress_title.lower() != chapter_title.lower():
            print(f"  (In chapters as: {chapter_title})")

    # Display unused songs
    print("\n\n=== UNUSED SONGS ===\n")
    for song in sorted(unused_songs):
        print(f"• {song}")

    return used_songs, unused_songs

if __name__ == '__main__':
    used, unused = main()
