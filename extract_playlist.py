#!/usr/bin/env python3
"""
Extract playlist information from WordPress export
"""

import re
from pathlib import Path
import html

EXPORT_FILE = '/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-14.xml'
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/playlist.md')

def extract_playlist_data(export_file):
    """Extract playlist page content from WordPress export"""

    with open(export_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the playlist section
    playlist_match = re.search(
        r'<title><!\[CDATA\[Playlist\]\]></title>.*?<content:encoded><!\[CDATA\[(.*?)\]\]></content:encoded>',
        content,
        re.DOTALL
    )

    if not playlist_match:
        return None

    playlist_content = playlist_match.group(1)

    # Extract music videos
    videos = []
    video_pattern = r'Music Video: ([^\n<]+).*?<video controls src="([^"]+)"'
    for match in re.finditer(video_pattern, playlist_content, re.DOTALL):
        videos.append({
            'title': match.group(1).strip(),
            'url': match.group(2).strip()
        })

    # Extract YouTube playlist
    youtube_match = re.search(r'https://youtube\.com/playlist\?list=([^"&\s]+)', playlist_content)
    youtube_playlist = youtube_match.group(0) if youtube_match else None

    return {
        'videos': videos,
        'youtube_playlist': youtube_playlist
    }

def extract_songs_playlist_tracks(export_file):
    """Extract individual tracks from Songs Playlist post"""

    with open(export_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the Songs Playlist custom post type
    songs_playlist_match = re.search(
        r'<title><!\[CDATA\[Songs Playlist\]\]></title>.*?<wp:post_type><!\[CDATA\[sr_playlist\]\]>.*?<wp:postmeta>.*?<wp:meta_key><!\[CDATA\[alb_tracklist\]\]></wp:meta_key>',
        content,
        re.DOTALL
    )

    if not songs_playlist_match:
        return []

    # Find all track MP3 URLs in the playlist metadata section
    # Look for patterns like track_mp3";s:XX:"URL"
    track_section = content[songs_playlist_match.end():songs_playlist_match.end() + 50000]

    tracks = []

    # Extract MP3 URLs and their store links
    mp3_pattern = r'track_mp3";s:\d+:"([^"]+\.mp3)".*?store-link";s:\d+:"([^"]+)"'

    for match in re.finditer(mp3_pattern, track_section):
        mp3_url = match.group(1)
        store_url = match.group(2)

        # Extract song name from URL
        song_name = mp3_url.split('/')[-1].replace('.mp3', '').replace('-', ' ')
        song_name = song_name.replace('  ', ' ').strip()

        tracks.append({
            'name': song_name,
            'mp3': mp3_url,
            'page': store_url
        })

    return tracks

def create_playlist_markdown(playlist_data, tracks):
    """Create markdown content for playlist"""

    lines = []
    lines.append("# Skyler Thomas - Songs Playlist")
    lines.append("")
    lines.append("**Source:** https://www.skylerthomas.com/playlist/")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Music Videos section
    if playlist_data and playlist_data.get('videos'):
        lines.append("## Music Videos")
        lines.append("")
        for video in playlist_data['videos']:
            lines.append(f"### {video['title']}")
            lines.append(f"**Video URL:** {video['url']}")
            lines.append("")

    # YouTube Playlist
    if playlist_data and playlist_data.get('youtube_playlist'):
        lines.append("## YouTube Playlist")
        lines.append("")
        lines.append(f"**URL:** {playlist_data['youtube_playlist']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Audio Tracks
    if tracks:
        lines.append("## Audio Tracks")
        lines.append("")
        lines.append(f"**Total Tracks:** {len(tracks)}")
        lines.append("")
        lines.append("| # | Song Title | MP3 | Page |")
        lines.append("|---|-----------|-----|------|")

        for i, track in enumerate(tracks, 1):
            mp3_link = f"[MP3]({track['mp3']})"
            page_link = f"[Info]({track['page']})"
            lines.append(f"| {i} | {track['name']} | {mp3_link} | {page_link} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**Total Songs in Playlist:** {len(tracks)}")
    lines.append("")

    return "\n".join(lines)

def main():
    print("Extracting playlist from WordPress export...")
    print("=" * 70)

    # Extract playlist page data
    playlist_data = extract_playlist_data(EXPORT_FILE)

    # Extract tracks from Songs Playlist
    tracks = extract_songs_playlist_tracks(EXPORT_FILE)

    print(f"Found {len(tracks)} audio tracks")
    if playlist_data:
        print(f"Found {len(playlist_data.get('videos', []))} music videos")

    # Create markdown
    markdown_content = create_playlist_markdown(playlist_data, tracks)

    # Write to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print("=" * 70)
    print(f"✓ Created: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
