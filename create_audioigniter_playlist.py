#!/usr/bin/env python3
"""
Create a complete AudioIgniter playlist import with all 41 songs
"""

import re
from pathlib import Path
from urllib.parse import urlparse

SONAAR_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/SonaarImport.xml')
AUDIOIGNITER_TEMPLATE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/AudioIgniterExport.xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/AudioIgniterImport.xml')

def extract_songs_from_sonaar():
    """Extract all songs from the Sonaar XML"""
    print("Reading Sonaar XML...")
    with open(SONAAR_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the tracklist
    match = re.search(r'<wp:meta_key><!\[CDATA\[alb_tracklist\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>', content, re.DOTALL)

    if not match:
        print("ERROR: Could not find tracklist in Sonaar XML")
        return []

    tracklist = match.group(1)

    # Extract track info: mp3 URL and store link (post URL)
    pattern = r'track_mp3";s:\d+:"(https://www\.skylerthomas\.com/wp-content/uploads/[^"]+\.mp3)"[^}]*?store-link";s:\d+:"(https://www\.skylerthomas\.com/\?p=\d+)"'

    matches = re.findall(pattern, tracklist)

    songs = []
    for mp3_url, post_url in matches:
        # Extract song title from MP3 filename
        filename = mp3_url.split('/')[-1].replace('.mp3', '')
        # Clean up the filename to make a title
        title = filename.replace('-', ' ').replace('_', ' ')
        # Remove extra version info
        title = re.sub(r'\s+(Remastered|Edit|FINAL|Version|Studio|Duet|Male|Female|Vocal|A-Cappella|Acappella|Choir|Choral|Group|Opus|Rock|Rap|Remix|Duet|x2|III|II|I|4-5|1|2)(\s+|$)', ' ', title, flags=re.IGNORECASE)
        title = ' '.join(title.split())  # Normalize whitespace

        # Convert ?p=ID to slug URL
        post_id = post_url.split('=')[-1]
        # Create a slug from the title
        slug = filename.lower()
        post_slug_url = f"https://www.skylerthomas.com/{slug}/"

        songs.append({
            'title': f"Song: {title}",
            'artist': 'skylerthomas',
            'track_url': mp3_url,
            'buy_link': post_slug_url,
            'download_url': post_slug_url,
        })

    print(f"✓ Extracted {len(songs)} songs from Sonaar XML")
    return songs

def build_audioigniter_tracks(songs):
    """Build the PHP serialized array for AudioIgniter tracks"""

    # Build the serialized array
    tracks_array = f"a:{len(songs)}:{{"

    for i, song in enumerate(songs):
        tracks_array += f'i:{i};a:7:{{'
        tracks_array += f's:8:"cover_id";s:1:"0";'
        tracks_array += f's:5:"title";s:{len(song["title"])}:"{song["title"]}";'
        tracks_array += f's:6:"artist";s:{len(song["artist"])}:"{song["artist"]}";'
        tracks_array += f's:9:"track_url";s:{len(song["track_url"])}:"{song["track_url"]}";'
        tracks_array += f's:8:"buy_link";s:{len(song["buy_link"])}:"{song["buy_link"]}";'
        tracks_array += f's:12:"download_url";s:{len(song["download_url"])}:"{song["download_url"]}";'
        tracks_array += f's:23:"download_uses_track_url";s:1:"0";'
        tracks_array += '}'

    tracks_array += '}'

    return tracks_array

def create_audioigniter_import(songs):
    """Create the complete AudioIgniter import XML"""

    print("Reading AudioIgniter template...")
    with open(AUDIOIGNITER_TEMPLATE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Build the new tracks array
    tracks_serialized = build_audioigniter_tracks(songs)

    print(f"Built serialized tracks data ({len(tracks_serialized)} bytes)")

    # Find and replace the _audioigniter_tracks metadata
    pattern = r'(<wp:meta_key><!\[CDATA\[_audioigniter_tracks\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[)a:\d+:\{.*?\}(\]\]></wp:meta_value>)'

    replacement = f'\\1{tracks_serialized}\\2'

    content_updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if content_updated == content:
        print("⚠️  WARNING: Pattern did not match - tracks may not have been replaced")
        return False

    # Update the playlist title
    content_updated = re.sub(
        r'<title><!\[CDATA\[Playlist\]\]></title>',
        '<title><![CDATA[Complete Songs Playlist - AudioIgniter]]></title>',
        content_updated
    )

    # Update the post name slug
    content_updated = re.sub(
        r'<wp:post_name><!\[CDATA\[playlist\]\]></wp:post_name>',
        '<wp:post_name><![CDATA[complete-songs-audioigniter]]></wp:post_name>',
        content_updated
    )

    # Write the output
    print(f"Writing to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content_updated)

    print(f"✓ Created AudioIgniter import with {len(songs)} songs")
    return True

def main():
    print("="*60)
    print("AudioIgniter Playlist Builder")
    print("="*60)

    # Extract songs from Sonaar XML
    songs = extract_songs_from_sonaar()

    if not songs:
        print("ERROR: No songs found!")
        return

    print(f"\nFirst 3 songs:")
    for i, song in enumerate(songs[:3], 1):
        print(f"  {i}. {song['title']}")
        print(f"     URL: {song['track_url']}")
        print(f"     Post: {song['buy_link']}")

    print(f"\nLast 3 songs:")
    for i, song in enumerate(songs[-3:], len(songs)-2):
        print(f"  {i}. {song['title']}")
        print(f"     URL: {song['track_url']}")
        print(f"     Post: {song['buy_link']}")

    # Create the import
    print("\n" + "="*60)
    success = create_audioigniter_import(songs)

    if success:
        print("="*60)
        print("✓ DONE!")
        print(f"\nImport file created: {OUTPUT_FILE}")
        print("\nNext steps:")
        print("1. Go to WordPress Admin > Tools > Import")
        print("2. Choose 'WordPress' importer")
        print("3. Upload: AudioIgniterImport.xml")
        print("4. Complete the import")
        print(f"5. You should see a playlist with {len(songs)} songs!")
    else:
        print("ERROR: Failed to create import file")

if __name__ == '__main__':
    main()
