#!/usr/bin/env python3
"""
Correct fix for SonaarImport.xml:
1. Change Great-is-Your-Faithfulness-Rock.mp3 post link from p=600 to p=2284
2. Add Dig-a-Little-Deeper.mp3 as a new track pointing to p=600
"""

import re
from pathlib import Path

BACKUP_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/SonaarImport_BACKUP.xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/SonaarImport.xml')

def fix_playlist():
    """Apply the correct fixes"""

    print("Reading backup file...")
    with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step 1: Change Great-is-Your-Faithfulness post link from p=600 to p=2284
    print("\nStep 1: Changing Great-is-Your-Faithfulness post link from p=600 to p=2284...")

    # Find the track with Great-is-Your-Faithfulness-Rock.mp3 and p=600
    # and change the post ID to 2284

    pattern = r'(Great-is-Your-Faithfulness-Rock\.mp3[^}]*?store-link";s:)35(:"https://www\.skylerthomas\.com/\?p=)600(")'

    def fix_post_id(match):
        prefix = match.group(1)
        middle = match.group(2)
        suffix = match.group(3)
        # New post ID is 2284 (37 characters: "https://www.skylerthomas.com/?p=2284")
        return f'{prefix}37{middle}2284{suffix}'

    content = re.sub(pattern, fix_post_id, content)

    # Step 2: Add Dig-a-Little-Deeper.mp3 as a new track at p=600
    print("Step 2: Adding Dig-a-Little-Deeper.mp3 track at p=600...")

    # Create the new track entry
    dig_deeper_track = '''i:41;a:22:{s:12:"FileOrStream";s:3:"mp3";s:12:"track_mp3_id";i:1512;s:9:"track_mp3";s:79:"https://www.skylerthomas.com/wp-content/uploads/2025/10/Dig-a-Little-Deeper.mp3";s:11:"stream_link";b:0;s:12:"stream_title";s:0:"";s:12:"stream_album";s:0:"";s:11:"artist_name";s:0:"";s:13:"stream_lenght";s:0:"";s:12:"icecast_link";b:0;s:12:"icecast_json";b:0;s:13:"icecast_mount";s:0:"";s:13:"icecast_title";s:0:"";s:13:"icecast_album";s:0:"";s:16:"icecast_hostname";s:0:"";s:23:"post_audiopreview_promo";s:8:"disabled";s:17:"track_description";s:0:"";s:14:"track_image_id";s:0:"";s:11:"track_image";b:0;s:15:"track_lyrics_id";s:0:"";s:12:"track_lyrics";b:0;s:15:"song_store_list";a:1:{i:0;a:2:{s:10:"store-icon";s:11:"fas fa-plus";s:10:"store-link";s:35:"https://www.skylerthomas.com/?p=600";}}s:11:"track_peaks";s:0:"";}'''

    # Find the end of the track list (before the closing }}]])
    # and insert the new track
    content = content.replace('a:41:{', 'a:42:{')  # Increment track count from 41 to 42
    content = content.replace('i:40;a:22:', f'{dig_deeper_track}i:40;a:22:')  # Insert before last track

    print("✓ Changes applied successfully!")
    print("\nSummary:")
    print("  1. Great-is-Your-Faithfulness-Rock.mp3 now points to p=2284")
    print("  2. Dig-a-Little-Deeper.mp3 added as new track pointing to p=600")
    print(f"  3. Total tracks: 42 (was 41)")

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✓ Fixed file saved to: {OUTPUT_FILE}")

if __name__ == '__main__':
    fix_playlist()
