#!/usr/bin/env python3
"""
Remove all trashed posts from WordPress export
"""

import re
from pathlib import Path

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-18 (3).xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/WordPress-Export-NoTrash.xml')

def main():
    print("Reading WordPress export...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original file size: {len(content):,} bytes")

    # Find all items
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)
    print(f"Total items in export: {len(all_items)}")

    removed_count = 0
    trashed_items = []

    for item in all_items:
        # Check status
        status_match = re.search(r'<wp:status><!\[CDATA\[(.*?)\]\]></wp:status>', item)
        status = status_match.group(1) if status_match else None

        if status == 'trash':
            # Get post details for logging
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            title = title_match.group(1) if title_match else 'UNKNOWN'

            post_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
            post_id = post_id_match.group(1) if post_id_match else 'UNKNOWN'

            post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
            post_type = post_type_match.group(1) if post_type_match else 'UNKNOWN'

            trashed_items.append({
                'id': post_id,
                'title': title,
                'type': post_type
            })

            # Remove this item from the content
            content = content.replace(item, '')
            removed_count += 1

    print(f"\nRemoved {removed_count} trashed items:")
    for item in trashed_items[:10]:  # Show first 10
        print(f"  - ID {item['id']} ({item['type']}): {item['title'][:60]}")

    if len(trashed_items) > 10:
        print(f"  ... and {len(trashed_items) - 10} more")

    print(f"\nNew file size: {len(content):,} bytes")

    # Write the cleaned export
    print(f"\nWriting to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ Done!")
    print("\nThis export file has all trashed items removed.")
    print("You can import this to avoid any conflicts from trashed posts.")

if __name__ == '__main__':
    main()
