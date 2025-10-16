#!/usr/bin/env python3
"""
Populate Beyond the Swamp chapter outlines with song lyrics from WordPress export

This script extracts song lyrics from the WordPress export and adds them to
the appropriate chapter outline files.

Author owns copyright to all songs.
"""

import xml.etree.ElementTree as ET
import re
import os

# Path to WordPress export
EXPORT_FILE = '/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-14.xml'

# Path to chapter outline files
WIKI_DIR = '/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki'

# Song-to-chapter mapping
SONGS = {
    'Named By God': 'BeyondTheSwamp_01_Chapter-Named-By-God.md',
    'In His Image': 'BeyondTheSwamp_02_Chapter-In-His-Image.md',
    'You Still Know My Name': 'BeyondTheSwamp_03_Chapter-You-Still-Know-My-Name.md',
    'Why Didn\'t You Tell Me': 'BeyondTheSwamp_04_Chapter-Why-Didnt-You-Tell-Me.md',
    'Fruit of His Spirit': 'BeyondTheSwamp_06_Chapter-Fruit-of-Spirit.md',
    'Rhythm of Life': 'BeyondTheSwamp_07_Chapter-Rhythm-of-Life.md',
    'I Will Serve': 'BeyondTheSwamp_08_Chapter-I-Will-Serve.md',
    'No Good Deed': 'BeyondTheSwamp_09_Chapter-No-Good-Deed.md',
    'What is Prayer': 'BeyondTheSwamp_Complete_Movements_3-5.md',  # In comprehensive file
    'One Note': 'BeyondTheSwamp_Complete_Movements_3-5.md',
    'Holy Communion': 'BeyondTheSwamp_Complete_Movements_3-5.md',
    'Lord We Lift Our Hearts': 'BeyondTheSwamp_Complete_Movements_3-5.md',
    'When the Promise Hurts': 'BeyondTheSwamp_Complete_Movements_3-5.md',
    'Heart of Glass': 'BeyondTheSwamp_Complete_Movements_3-5.md',
    'Forgiveness Requires Remembrance': 'BeyondTheSwamp_Complete_Movements_3-5.md',
    'Battle Is Won': 'BeyondTheSwamp_Complete_Movements_3-5.md',
    'What\'s Heaven Like': 'BeyondTheSwamp_Complete_Movements_3-5.md',
    'The Rose': 'BeyondTheSwamp_Complete_Movements_3-5.md',
}

def extract_lyrics_from_export(export_file):
    """
    Extract song lyrics from WordPress export XML

    Returns dict: {song_title: lyrics_text}
    """
    print(f"Reading export file: {export_file}")

    try:
        tree = ET.parse(export_file)
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return {}

    # WordPress uses namespaces
    namespaces = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'wp': 'http://wordpress.org/export/1.2/'
    }

    lyrics_dict = {}

    # Find all items (posts)
    for item in root.findall('.//item'):
        title_elem = item.find('title')
        content_elem = item.find('content:encoded', namespaces)

        if title_elem is not None and content_elem is not None:
            title = title_elem.text or ''
            content = content_elem.text or ''

            # Look for song-related posts
            if 'Song:' in title or 'Lyrics' in title:
                # Try to extract lyrics from content
                # Lyrics are often in specific format - adjust as needed

                # Clean title
                clean_title = title.replace('Song:', '').replace('Lyrics:', '').strip()

                # Store content (may need cleaning)
                lyrics_dict[clean_title] = content
                print(f"  Found: {clean_title}")

    return lyrics_dict

def find_lyrics_in_content(content):
    """
    Extract formatted lyrics from WordPress content

    WordPress content includes HTML - need to extract just lyrics
    """
    # Remove HTML tags
    content = re.sub(r'<[^>]+>', '', content)

    # Remove WordPress shortcodes
    content = re.sub(r'\[.*?\]', '', content)

    # Clean up extra whitespace
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)

    return content.strip()

def update_chapter_file(chapter_file, song_title, lyrics):
    """
    Update chapter outline file with song lyrics

    Finds the "Song Lyrics" placeholder and replaces with actual lyrics
    """
    file_path = os.path.join(WIKI_DIR, chapter_file)

    if not os.path.exists(file_path):
        print(f"  ⚠️  File not found: {chapter_file}")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if lyrics already added
    if '*[To be added: Full lyrics' not in content:
        print(f"  ℹ️  Lyrics may already be added to {chapter_file}")
        return False

    # Find the lyrics placeholder section
    lyrics_section_pattern = r'\*\[To be added: Full lyrics.*?\]\*'

    if re.search(lyrics_section_pattern, content):
        # Format lyrics nicely
        formatted_lyrics = f"\n{lyrics}\n"

        # Replace placeholder
        new_content = re.sub(
            lyrics_section_pattern,
            formatted_lyrics,
            content
        )

        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  ✅ Updated: {chapter_file}")
        return True
    else:
        print(f"  ⚠️  Lyrics placeholder not found in {chapter_file}")
        return False

def main():
    print("="*70)
    print("POPULATING BEYOND THE SWAMP WITH SONG LYRICS")
    print("="*70)
    print()

    # Check if export file exists
    if not os.path.exists(EXPORT_FILE):
        print(f"❌ Export file not found: {EXPORT_FILE}")
        return

    # Extract lyrics from export
    print("Step 1: Extracting lyrics from WordPress export...")
    lyrics_dict = extract_lyrics_from_export(EXPORT_FILE)

    if not lyrics_dict:
        print("❌ No lyrics found in export file")
        return

    print(f"\n✓ Found {len(lyrics_dict)} songs in export\n")

    # Match and update chapter files
    print("Step 2: Updating chapter files...")
    print()

    updated = 0
    not_found = []

    for song_title, chapter_file in SONGS.items():
        print(f"Processing: {song_title}")

        # Try to find matching lyrics in export
        lyrics = None
        for export_title, export_content in lyrics_dict.items():
            if song_title.lower() in export_title.lower():
                lyrics = find_lyrics_in_content(export_content)
                break

        if lyrics:
            if update_chapter_file(chapter_file, song_title, lyrics):
                updated += 1
        else:
            print(f"  ⚠️  Lyrics not found in export for: {song_title}")
            not_found.append(song_title)

    # Summary
    print()
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"✓ Updated: {updated} chapter files")
    print(f"⚠️  Not found: {len(not_found)} songs")

    if not_found:
        print("\nSongs without lyrics in export:")
        for song in not_found:
            print(f"  - {song}")

    print("\n" + "="*70)
    print("NOTE: Please review the updated files to ensure lyrics")
    print("formatting is correct. You may need to manually adjust")
    print("verse/chorus labels and line breaks.")
    print("="*70)

if __name__ == '__main__':
    main()
