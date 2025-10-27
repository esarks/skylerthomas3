#!/usr/bin/env python3
"""
Extract songs from posts sorted ALPHABETICALLY by song name
"""

import re
from pathlib import Path

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-19 (1).xml')
AUDIOIGNITER_TEMPLATE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/AudioIgniterExport.xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/AudioIgniter-Songs-Alphabetical.xml')

def get_posts_data():
    """Get all posts with their songs"""
    print("Reading posts and extracting songs...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)

    all_songs = []

    for item in all_items:
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        if post_type != 'post':
            continue

        status_match = re.search(r'<wp:status><!\[CDATA\[(.*?)\]\]></wp:status>', item)
        status = status_match.group(1) if status_match else None

        if status != 'publish':
            continue

        title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
        post_title = title_match.group(1) if title_match else ''

        # Skip "Out of the Swamp" posts
        if 'Out of the Swamp' in post_title:
            continue

        post_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
        post_id = post_id_match.group(1) if post_id_match else None

        content_match = re.search(r'<content:encoded><!\[CDATA\[(.*?)\]\]></content:encoded>', item, re.DOTALL)
        post_content = content_match.group(1) if content_match else ''

        # Find all audio URLs
        audio_shortcodes = re.findall(r'\[audio[^\]]*src="([^"]+\.mp3)"[^\]]*\]', post_content)
        direct_mp3s = re.findall(r'https://www\.skylerthomas\.com/wp-content/uploads/[^\s"<>]+\.mp3', post_content)
        all_mp3_urls = list(dict.fromkeys(audio_shortcodes + direct_mp3s))  # Remove duplicates, preserve order

        if all_mp3_urls:
            for mp3_url in all_mp3_urls:
                filename = mp3_url.split('/')[-1].replace('.mp3', '')
                song_title = filename.replace('-', ' ').replace('_', ' ')
                song_title = re.sub(r'\s+(Remastered|Edit|FINAL|Version|Studio|Duet|Male|Female|Vocal|A-Cappella|Acappella|Choir|Choral|Group|Opus|Rock|Rap|Remix|x2|III|II|I|4-5|1|2)\s*', ' ', song_title, flags=re.IGNORECASE)
                song_title = ' '.join(song_title.split())

                post_url = f"https://www.skylerthomas.com/?p={post_id}"

                all_songs.append({
                    'title': f"Song: {song_title}",
                    'artist': 'skylerthomas',
                    'track_url': mp3_url,
                    'buy_link': post_url,
                    'download_url': post_url,
                    'sort_key': song_title.lower()  # For sorting
                })

    print(f"Found {len(all_songs)} total songs")
    return all_songs

def build_audioigniter_tracks(songs):
    """Build the PHP serialized array for AudioIgniter tracks"""
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
    print("\nReading AudioIgniter template...")
    with open(AUDIOIGNITER_TEMPLATE, 'r', encoding='utf-8') as f:
        content = f.read()

    tracks_serialized = build_audioigniter_tracks(songs)

    pattern = r'(<wp:meta_key><!\[CDATA\[_audioigniter_tracks\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[)a:\d+:\{.*?\}(\]\]></wp:meta_value>)'
    replacement = f'\\1{tracks_serialized}\\2'
    content_updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if content_updated == content:
        print("⚠️  WARNING: Pattern did not match")
        return False

    content_updated = re.sub(
        r'<title><!\[CDATA\[Playlist\]\]></title>',
        '<title><![CDATA[Songs Alphabetical]]></title>',
        content_updated
    )

    content_updated = re.sub(
        r'<wp:post_name><!\[CDATA\[playlist\]\]></wp:post_name>',
        '<wp:post_name><![CDATA[songs-alphabetical]]></wp:post_name>',
        content_updated
    )

    # Set post_id to 0 so WordPress creates a new one
    content_updated = re.sub(
        r'<wp:post_id>\d+</wp:post_id>',
        '<wp:post_id>0</wp:post_id>',
        content_updated
    )

    print(f"Writing to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content_updated)

    print(f"✓ Created AudioIgniter import with {len(songs)} songs")
    return True

def main():
    print("=" * 60)
    print("AudioIgniter - Songs Sorted ALPHABETICALLY")
    print("=" * 60)

    # Get all songs
    all_songs = get_posts_data()

    if not all_songs:
        print("ERROR: No songs found!")
        return

    # Sort alphabetically by song title
    all_songs.sort(key=lambda x: x['sort_key'])

    print(f"\n✓ Total songs: {len(all_songs)}")

    print(f"\nFirst 10 songs:")
    for i, song in enumerate(all_songs[:10], 1):
        print(f"  {i}. {song['title']}")

    print(f"\nLast 10 songs:")
    for i, song in enumerate(all_songs[-10:], len(all_songs)-9):
        print(f"  {i}. {song['title']}")

    # Create the import
    print("\n" + "=" * 60)
    success = create_audioigniter_import(all_songs)

    if success:
        print("=" * 60)
        print("✓ DONE!")
        print(f"\nImport file: {OUTPUT_FILE}")
        print(f"Total songs: {len(all_songs)}")
        print("\nSongs are sorted ALPHABETICALLY by song name!")
    else:
        print("ERROR: Failed to create import file")

if __name__ == '__main__':
    main()
