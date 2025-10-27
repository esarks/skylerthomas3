#!/usr/bin/env python3
"""
Extract songs from posts in MENU order (removing duplicate menu items first)
"""

import re
from pathlib import Path

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-19.xml')
AUDIOIGNITER_TEMPLATE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/AudioIgniterExport.xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/AudioIgniter-All-Songs-Menu-Order.xml')

def extract_postmeta(item_xml):
    """Extract all postmeta key-value pairs"""
    postmeta = {}
    meta_entries = re.findall(r'<wp:postmeta>\s*<wp:meta_key><!\[CDATA\[(.*?)\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>\s*</wp:postmeta>', item_xml, re.DOTALL)
    for key, value in meta_entries:
        postmeta[key] = value
    return postmeta

def get_menu_order():
    """Get the order of posts from the menu (removing duplicates)"""
    print("Reading menu order from export...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)

    menu_items = []
    for item in all_items:
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        if post_type == 'nav_menu_item':
            postmeta = extract_postmeta(item)

            menu_order_match = re.search(r'<wp:menu_order>(\d+)</wp:menu_order>', item)
            menu_order = int(menu_order_match.group(1)) if menu_order_match else 0

            object_id = postmeta.get('_menu_item_object_id', '0')
            menu_type = postmeta.get('_menu_item_type', '')
            object_type = postmeta.get('_menu_item_object', '')

            # Create unique key
            if menu_type == 'post_type':
                unique_key = f"post:{object_type}:{object_id}"
            elif menu_type == 'custom':
                url = postmeta.get('_menu_item_url', '')
                unique_key = f"custom:{url}"
            else:
                unique_key = f"other:{menu_order}"

            if menu_type == 'post_type' and object_id != '0':
                menu_items.append({
                    'object_id': object_id,
                    'menu_order': menu_order,
                    'unique_key': unique_key
                })

    # Remove duplicates - keep first occurrence
    seen_keys = {}
    unique_items = []
    for item in sorted(menu_items, key=lambda x: x['menu_order']):
        if item['unique_key'] not in seen_keys:
            seen_keys[item['unique_key']] = True
            unique_items.append(item)

    print(f"Found {len(menu_items)} total menu items")
    print(f"Removed {len(menu_items) - len(unique_items)} duplicates")
    print(f"Kept {len(unique_items)} unique posts in menu order")

    return [item['object_id'] for item in unique_items]

def get_posts_data():
    """Get all posts with their songs"""
    print("Reading posts and extracting songs...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)

    posts_data = {}

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
            songs = []
            for mp3_url in all_mp3_urls:
                filename = mp3_url.split('/')[-1].replace('.mp3', '')
                song_title = filename.replace('-', ' ').replace('_', ' ')
                song_title = re.sub(r'\s+(Remastered|Edit|FINAL|Version|Studio|Duet|Male|Female|Vocal|A-Cappella|Acappella|Choir|Choral|Group|Opus|Rock|Rap|Remix|x2|III|II|I|4-5|1|2)\s*', ' ', song_title, flags=re.IGNORECASE)
                song_title = ' '.join(song_title.split())

                post_url = f"https://www.skylerthomas.com/?p={post_id}"

                songs.append({
                    'title': f"Song: {song_title}",
                    'artist': 'skylerthomas',
                    'track_url': mp3_url,
                    'buy_link': post_url,
                    'download_url': post_url,
                })

            posts_data[post_id] = {
                'title': post_title,
                'songs': songs
            }

    print(f"Found {len(posts_data)} posts with songs")
    return posts_data

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
        '<title><![CDATA[Complete Songs - Menu Order]]></title>',
        content_updated
    )

    content_updated = re.sub(
        r'<wp:post_name><!\[CDATA\[playlist\]\]></wp:post_name>',
        '<wp:post_name><![CDATA[complete-songs-menu-order]]></wp:post_name>',
        content_updated
    )

    print(f"Writing to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content_updated)

    print(f"✓ Created AudioIgniter import with {len(songs)} songs")
    return True

def main():
    print("=" * 60)
    print("AudioIgniter - Songs in MENU Order (No Duplicates)")
    print("=" * 60)

    # Get menu order (with duplicates removed)
    menu_order = get_menu_order()

    # Get all posts data
    posts_data = get_posts_data()

    # Build song list in menu order
    all_songs = []
    posts_found = 0

    print("\nBuilding playlist in menu order:")
    for post_id in menu_order:
        if post_id in posts_data:
            post = posts_data[post_id]
            posts_found += 1
            print(f"  {posts_found}. {post['title']} ({len(post['songs'])} song(s))")
            all_songs.extend(post['songs'])

    print(f"\n✓ Found {posts_found} posts from menu")
    print(f"✓ Total songs: {len(all_songs)}")

    if not all_songs:
        print("ERROR: No songs found!")
        return

    print(f"\nFirst 5 songs:")
    for i, song in enumerate(all_songs[:5], 1):
        print(f"  {i}. {song['title']}")

    print(f"\nLast 5 songs:")
    for i, song in enumerate(all_songs[-5:], len(all_songs)-4):
        print(f"  {i}. {song['title']}")

    # Create the import
    print("\n" + "=" * 60)
    success = create_audioigniter_import(all_songs)

    if success:
        print("=" * 60)
        print("✓ DONE!")
        print(f"\nImport file: {OUTPUT_FILE}")
        print(f"Total songs: {len(all_songs)}")
        print("\nSongs are in MENU order (with duplicates removed)!")
    else:
        print("ERROR: Failed to create import file")

if __name__ == '__main__':
    main()
