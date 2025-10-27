#!/usr/bin/env python3
"""
Extract ALL songs from ALL posts (except Out of the Swamp posts)
"""

import re
from pathlib import Path

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-18 (3).xml')
AUDIOIGNITER_TEMPLATE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/AudioIgniterExport.xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/AudioIgniter-All-Songs.xml')

def extract_songs_from_posts():
    """Extract all songs from all posts"""
    print("Reading WordPress export...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all items
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)

    songs = []
    posts_processed = 0

    for item in all_items:
        # Only process published posts
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        if post_type != 'post':
            continue

        status_match = re.search(r'<wp:status><!\[CDATA\[(.*?)\]\]></wp:status>', item)
        status = status_match.group(1) if status_match else None

        if status != 'publish':
            continue

        # Get post details
        title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
        post_title = title_match.group(1) if title_match else ''

        # Skip "Out of the Swamp" posts
        if 'Out of the Swamp' in post_title:
            continue

        post_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
        post_id = post_id_match.group(1) if post_id_match else None

        # Get post content
        content_match = re.search(r'<content:encoded><!\[CDATA\[(.*?)\]\]></content:encoded>', item, re.DOTALL)
        post_content = content_match.group(1) if content_match else ''

        # Find all audio URLs in the content
        # Pattern 1: [audio src="URL"]
        audio_shortcodes = re.findall(r'\[audio[^\]]*src="([^"]+\.mp3)"[^\]]*\]', post_content)

        # Pattern 2: Direct MP3 URLs
        direct_mp3s = re.findall(r'https://www\.skylerthomas\.com/wp-content/uploads/[^\s"<>]+\.mp3', post_content)

        # Combine both
        all_mp3_urls = list(set(audio_shortcodes + direct_mp3s))

        if all_mp3_urls:
            posts_processed += 1
            print(f"  Post: {post_title}")
            print(f"    Found {len(all_mp3_urls)} song(s)")

            for mp3_url in all_mp3_urls:
                # Extract song title from filename
                filename = mp3_url.split('/')[-1].replace('.mp3', '')
                song_title = filename.replace('-', ' ').replace('_', ' ')
                # Clean up
                song_title = re.sub(r'\s+(Remastered|Edit|FINAL|Version|Studio|Duet|Male|Female|Vocal|A-Cappella|Acappella|Choir|Choral|Group|Opus|Rock|Rap|Remix|x2|III|II|I|4-5|1|2)\s*', ' ', song_title, flags=re.IGNORECASE)
                song_title = ' '.join(song_title.split())

                post_url = f"https://www.skylerthomas.com/?p={post_id}"

                songs.append({
                    'title': f"Song: {song_title}",
                    'artist': 'skylerthomas',
                    'track_url': mp3_url,
                    'buy_link': post_url,
                    'download_url': post_url,
                    'post_title': post_title
                })

    print(f"\n✓ Processed {posts_processed} posts")
    print(f"✓ Found {len(songs)} total songs")
    return songs

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

    # Build the new tracks array
    tracks_serialized = build_audioigniter_tracks(songs)

    # Find and replace the _audioigniter_tracks metadata
    pattern = r'(<wp:meta_key><!\[CDATA\[_audioigniter_tracks\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[)a:\d+:\{.*?\}(\]\]></wp:meta_value>)'

    replacement = f'\\1{tracks_serialized}\\2'

    content_updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if content_updated == content:
        print("⚠️  WARNING: Pattern did not match")
        return False

    # Update the playlist title
    content_updated = re.sub(
        r'<title><!\[CDATA\[Playlist\]\]></title>',
        '<title><![CDATA[Complete Songs - All Posts]]></title>',
        content_updated
    )

    # Update the post name slug
    content_updated = re.sub(
        r'<wp:post_name><!\[CDATA\[playlist\]\]></wp:post_name>',
        '<wp:post_name><![CDATA[complete-songs-all-posts]]></wp:post_name>',
        content_updated
    )

    # Write the output
    print(f"Writing to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content_updated)

    print(f"✓ Created AudioIgniter import with {len(songs)} songs")
    return True

def main():
    print("=" * 60)
    print("AudioIgniter - ALL Songs from Posts")
    print("=" * 60)

    songs = extract_songs_from_posts()

    if not songs:
        print("ERROR: No songs found!")
        return

    print(f"\nFirst 5 songs:")
    for i, song in enumerate(songs[:5], 1):
        print(f"  {i}. {song['title']}")
        print(f"     From: {song['post_title']}")

    print(f"\nLast 5 songs:")
    for i, song in enumerate(songs[-5:], len(songs)-4):
        print(f"  {i}. {song['title']}")
        print(f"     From: {song['post_title']}")

    # Create the import
    print("\n" + "=" * 60)
    success = create_audioigniter_import(songs)

    if success:
        print("=" * 60)
        print("✓ DONE!")
        print(f"\nImport file: {OUTPUT_FILE}")
        print(f"Total songs: {len(songs)}")
        print("\nNext steps:")
        print("1. Go to WordPress Admin > Tools > Import")
        print("2. Upload: AudioIgniter-All-Songs.xml")
        print("3. Complete the import")
    else:
        print("ERROR: Failed to create import file")

if __name__ == '__main__':
    main()
