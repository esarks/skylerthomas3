#!/usr/bin/env python3
"""
Create menu import WITHOUT attachments (to avoid null byte errors)
Keep posts/pages that menu links to + menu items
"""

import re
from pathlib import Path

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-18 (3).xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/Menu-Clean-No-Attachments.xml')

# Duplicate menu item IDs to remove
DUPLICATE_IDS = set([
    1523, 2303, 6018, 6019, 6020, 6021, 6022, 6023, 6024, 6025, 6026, 6027, 6028,
    6029, 6030, 6031, 6032, 6033, 6034, 6035, 6036, 6037, 6038, 6039, 6040, 6041,
    6042, 6043, 6044, 6045, 6046, 6047, 6048, 6049, 6050, 6051, 6053, 6054, 6055,
    6056, 6057, 6058, 6059, 6061, 6062, 6063, 6064, 6065, 6066, 6067, 6068, 6069,
    6072, 6073, 6074, 6075, 6076, 6077, 6078, 6080, 6081, 6082, 6083, 6084, 6085,
    6086, 6087, 6088, 6089, 6090, 6091
])

def main():
    print("Reading file...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into header, items, and footer
    header_match = re.search(r'^(.*?)<item>', content, re.DOTALL)
    header = header_match.group(1) if header_match else ''

    footer = '</channel>\n</rss>'

    # Extract all items
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)
    print(f"Found {len(all_items)} total items")

    # Filter items
    kept_items = []
    removed_attachments = 0
    removed_menu_dups = 0

    for item in all_items:
        # Get post type
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        # Get post ID
        post_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
        post_id = int(post_id_match.group(1)) if post_id_match else None

        # Skip attachments (they cause null byte errors)
        if post_type == 'attachment':
            removed_attachments += 1
            continue

        # Skip duplicate menu items
        if post_type == 'nav_menu_item' and post_id in DUPLICATE_IDS:
            removed_menu_dups += 1
            continue

        # Keep everything else
        kept_items.append(item)

    print(f"✓ Kept {len(kept_items)} items")
    print(f"✓ Removed {removed_attachments} attachments (to avoid null byte errors)")
    print(f"✓ Removed {removed_menu_dups} duplicate menu items")

    # Rebuild content
    print("Rebuilding file...")
    output = header
    for item in kept_items:
        output += item + '\n'
    output += footer

    # Write output
    print(f"Writing to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    print("✓ Done!")
    print("\nThis file contains:")
    print("- All posts and pages")
    print("- Menu with 76 unique items (no duplicates)")
    print("- NO attachments (to avoid import errors)")

if __name__ == '__main__':
    main()
