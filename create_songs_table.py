#!/usr/bin/env python3
"""
Create a table of all songs with check marks for those in the current book
"""

import re
from pathlib import Path

EXPORT_FILE = '/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-14.xml'
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/unusedsongs.md')

# Songs in the CURRENT book "Out of the Swamp" (Book 1)
SONGS_IN_CURRENT_BOOK = [
    'My Swamp',
    'But Then I Prayed',
    'STOP!!! And Make a Decision',
    'Dying Changes Everything',
    'Living Waters Edge',
    'In the Shadow of Your Grace',
    'Amazing Grace',
    'Dig a Little Deeper',
    'Unforced Rhythms of Grace',
    'Deep Roots, Strong Growth',
    'Redemptions Story',
    'Redemption Story',
    'Nothing is Wasted',
    'Devil\'s On The Run',
    'This Moment is Enough',
    'Living in the Moment',
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
            title = title.replace('(Devotional &amp; Song)', '').strip()
            title = title.replace('(Devotional &amp; Rap)', '').strip()

            # Remove version indicators
            title = re.sub(r' - (Duet|Male Vocal|Female Vocal|A Cappella|Remastered|Instrumental|Remix|Studio Version|Acappella|Choral|Vocal Band|Rock|Rap Instrumental|Mixed Vocal Instrumental).*', '', title)
            title = re.sub(r' \(Remastered\)', '', title)
            title = re.sub(r' \(Remix\)', '', title)
            title = re.sub(r' V\d+$', '', title)  # Remove version numbers
            title = re.sub(r' \d+-\d+$', '', title)  # Remove version numbers like 4-5
            title = re.sub(r' III$', '', title)  # Remove roman numerals
            title = re.sub(r' II$', '', title)
            title = title.strip()

            if title and title != 'Songs Playlist':
                songs.add(title)

    return sorted(songs, key=str.lower)

def normalize_song_name(name):
    """Normalize song name for comparison"""
    name = name.lower()
    name = name.replace('…', '...')  # Normalize ellipsis
    name = re.sub(r'[^\w\s]', '', name)  # Remove punctuation
    name = re.sub(r'\s+', ' ', name).strip()  # Normalize whitespace
    return name

def is_in_current_book(song_title, current_book_songs):
    """Check if song is in the current book"""
    normalized = normalize_song_name(song_title)

    for book_song in current_book_songs:
        book_normalized = normalize_song_name(book_song)
        if normalized == book_normalized or book_normalized in normalized or normalized in book_normalized:
            return True
    return False

def create_markdown_table(all_songs, current_book_songs):
    """Create markdown table with check marks"""

    lines = []
    lines.append("# Song Usage Analysis")
    lines.append("")
    lines.append("**Status:** All songs from WordPress export")
    lines.append("**✓** = Song is in the current book \"Out of the Swamp\"")
    lines.append("**( )** = Song is NOT in the current book (available for Beyond the Swamp)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("| In Book? | Song Title |")
    lines.append("|----------|-----------|")

    in_book_count = 0
    not_in_book_count = 0

    for song in all_songs:
        if is_in_current_book(song, current_book_songs):
            check = "✓"
            in_book_count += 1
        else:
            check = " "
            not_in_book_count += 1

        lines.append(f"| {check} | {song} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"**Total unique songs:** {len(all_songs)}")
    lines.append(f"**In current book:** {in_book_count}")
    lines.append(f"**Available for new book:** {not_in_book_count}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Songs in Current Book \"Out of the Swamp\"")
    lines.append("")

    for song in all_songs:
        if is_in_current_book(song, current_book_songs):
            lines.append(f"- ✓ {song}")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Songs Available for \"Beyond the Swamp\"")
    lines.append("")

    for song in all_songs:
        if not is_in_current_book(song, current_book_songs):
            lines.append(f"- {song}")

    return "\n".join(lines)

def main():
    print("Creating songs usage table...")
    print("=" * 70)

    # Extract all unique songs
    all_songs = extract_unique_songs(EXPORT_FILE)

    print(f"Total unique songs found: {len(all_songs)}")

    # Create markdown table
    markdown_content = create_markdown_table(all_songs, SONGS_IN_CURRENT_BOOK)

    # Write to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"✓ Created: {OUTPUT_FILE}")
    print("=" * 70)

    # Count songs in current book
    in_book = sum(1 for song in all_songs if is_in_current_book(song, SONGS_IN_CURRENT_BOOK))
    available = len(all_songs) - in_book

    print(f"\n✓ Total songs: {len(all_songs)}")
    print(f"✓ In current book: {in_book}")
    print(f"✓ Available for new book: {available}")

if __name__ == '__main__':
    main()
