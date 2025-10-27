#!/usr/bin/env python3
"""
Fix the SonaarImport.xml playlist to correct the song/post mappings
"""

import re
from pathlib import Path

SONAAR_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/SonaarImport.xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/SonaarImport_FIXED.xml')

def fix_sonaar_playlist():
    """Fix the incorrect song-to-post mappings"""

    print("Reading SonaarImport.xml...")
    with open(SONAAR_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Issue 1: Track with Great-is-Your-Faithfulness-Rock.mp3 pointing to p=600
    # Should be: Dig-a-Little-Deeper.mp3 pointing to p=600

    # Find and replace the specific track entry
    # The pattern matches the track that has Great-is-Your-Faithfulness-Rock.mp3 and store-link p=600

    # Old MP3 URL
    old_mp3_url = "https://www.skylerthomas.com/wp-content/uploads/2025/02/Great-is-Your-Faithfulness-Rock.mp3"
    # New MP3 URL
    new_mp3_url = "https://www.skylerthomas.com/wp-content/uploads/2025/10/Dig-a-Little-Deeper.mp3"

    # Strategy: Find the track entry that has Great-is-Your-Faithfulness-Rock.mp3
    # and links to p=600, then replace just that MP3 URL

    # First, let's find the specific track section
    pattern = r'(i:\d+;a:22:\{[^}]*?track_mp3";s:\d+:")' + re.escape(old_mp3_url) + r'("[^}]*?store-link";s:\d+:"https://www\.skylerthomas\.com/\?p=600"[^}]*?\})'

    def replace_track(match):
        """Replace the MP3 URL and adjust the string length"""
        prefix = match.group(1)
        suffix = match.group(2)

        # Calculate the new string length for the MP3 URL
        new_length = len(new_mp3_url)

        # Replace the old length with new length in the prefix
        prefix_fixed = re.sub(r's:\d+:"$', f's:{new_length}:"', prefix)

        return prefix_fixed + new_mp3_url + suffix

    # Apply the replacement
    content_fixed = re.sub(pattern, replace_track, content)

    if content_fixed == content:
        print("⚠️  Warning: No changes made. Pattern might not match.")
        print("   Trying alternative approach...")

        # Alternative: Just replace the URL wherever it appears with p=600
        # This is less precise but will work
        if old_mp3_url in content and '?p=600' in content:
            # Find the track entry more broadly
            lines = content.split('track_mp3"')
            fixed_lines = []

            for i, line in enumerate(lines):
                if old_mp3_url in line:
                    # Check if this track links to p=600
                    # Look ahead in the same track entry
                    if 'p=600' in line:
                        print(f"✓ Found problematic track entry")
                        # Replace the MP3 URL
                        line = line.replace(old_mp3_url, new_mp3_url)
                        # Update the string length
                        line = re.sub(r's:91:', f's:{len(new_mp3_url)}:', line)
                fixed_lines.append(line)

            content_fixed = 'track_mp3"'.join(fixed_lines)

    # Verify the change
    if new_mp3_url in content_fixed:
        print(f"✓ Successfully replaced MP3 URL")
        print(f"  Old: {old_mp3_url}")
        print(f"  New: {new_mp3_url}")
    else:
        print(f"⚠️  Failed to replace MP3 URL")

    # Write the fixed content
    print(f"\nWriting fixed playlist to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content_fixed)

    print(f"✓ Done! Fixed file saved.")
    print(f"\nNext steps:")
    print(f"1. Review the changes in: {OUTPUT_FILE}")
    print(f"2. If correct, replace the original file:")
    print(f"   mv {OUTPUT_FILE} {SONAAR_FILE}")

if __name__ == '__main__':
    fix_sonaar_playlist()
