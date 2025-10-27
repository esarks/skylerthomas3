#!/usr/bin/env python3
"""
Remove duplicate posts from WordPress export
"""

import re
from pathlib import Path

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-14.xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/WordPress-Export-NoDuplicatePosts.xml')

# Posts to remove (keep the higher ID, remove the lower ID)
POSTS_TO_REMOVE = [
    1555,  # Duplicate of 1557: INTRODUCTION: The Wayfarer's Anthem
    1593,  # Duplicate of 1945: Dying Changes Everything: A Wayfarers Journey (Chapter 7)
]

def main():
    print("Reading WordPress export...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original file size: {len(content):,} bytes")

    # Find all items
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)
    print(f"Total items in export: {len(all_items)}")

    removed_count = 0
    for post_id in POSTS_TO_REMOVE:
        # Find the item with this post_id
        pattern = rf'(<item>.*?<wp:post_id>{post_id}</wp:post_id>.*?</item>)'
        matches = re.findall(pattern, content, re.DOTALL)

        if matches:
            for match in matches:
                # Get the title for logging
                title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', match)
                title = title_match.group(1) if title_match else 'UNKNOWN'

                print(f"  Removing post ID {post_id}: {title}")
                content = content.replace(match, '')
                removed_count += 1
        else:
            print(f"  ⚠️  Post ID {post_id} not found")

    print(f"\nRemoved {removed_count} duplicate posts")
    print(f"New file size: {len(content):,} bytes")

    # Write the cleaned export
    print(f"\nWriting to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ Done!")
    print("\nIMPORTANT: Before importing this file:")
    print("1. Go to WordPress Admin > Appearance > Menus")
    print("2. Delete the existing 'Menu' completely")
    print("3. Go to WordPress Admin > Posts")
    print("4. Delete ALL duplicate 'Out of the Swamp' posts")
    print("5. THEN import this file")
    print("\nThis will prevent duplicates from appearing in your menu.")

if __name__ == '__main__':
    main()
