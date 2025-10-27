#!/usr/bin/env python3
"""
Reorder posts to match menu order
"""

import re
from pathlib import Path

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-19 (1).xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/WordPress-Export-Posts-Reordered.xml')

def extract_postmeta(item_xml):
    """Extract all postmeta key-value pairs"""
    postmeta = {}
    meta_entries = re.findall(r'<wp:postmeta>\s*<wp:meta_key><!\[CDATA\[(.*?)\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>\s*</wp:postmeta>', item_xml, re.DOTALL)
    for key, value in meta_entries:
        postmeta[key] = value
    return postmeta

def get_menu_order():
    """Get the order of posts from the menu"""
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

    print(f"Found {len(unique_items)} unique posts in menu order")

    # Create mapping of post_id to menu position
    post_order_map = {}
    for i, item in enumerate(unique_items, 1):
        post_order_map[item['object_id']] = i

    return post_order_map

def main():
    print("=" * 60)
    print("Reorder Posts by Menu Order")
    print("=" * 60)

    # Get menu order mapping
    post_order_map = get_menu_order()

    print(f"\nReading export file...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract header and footer
    header_match = re.search(r'^(.*?)<item>', content, re.DOTALL)
    header = header_match.group(1) if header_match else ''
    footer = '</channel>\n</rss>'

    # Find all items
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)

    updated_items = []
    posts_reordered = 0
    attachments_skipped = 0

    for item in all_items:
        # Get post ID
        post_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
        post_id = post_id_match.group(1) if post_id_match else None

        # Get post type
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        # Skip attachments (they cause null byte errors)
        if post_type == 'attachment':
            attachments_skipped += 1
            continue

        # If this post is in our menu order map, update its menu_order
        if post_id in post_order_map and post_type == 'post':
            new_order = post_order_map[post_id]

            # Update the menu_order field
            updated_item = re.sub(
                r'<wp:menu_order>\d+</wp:menu_order>',
                f'<wp:menu_order>{new_order}</wp:menu_order>',
                item
            )

            updated_items.append(updated_item)
            posts_reordered += 1
        else:
            updated_items.append(item)

    print(f"✓ Reordered {posts_reordered} posts to match menu order")
    print(f"✓ Skipped {attachments_skipped} attachments (to avoid null byte errors)")

    # Build output
    output = header
    for item in updated_items:
        output += item + '\n'
    output += footer

    # Write output
    print(f"\nWriting to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    print("✓ Done!")
    print(f"\nCreated export with posts reordered to match menu")
    print("\nTo apply this order in WordPress:")
    print("1. Delete all posts (or backup your site)")
    print("2. Import this file")
    print("3. Posts will be in the same order as your menu")
    print("\nOR use APTO plugin to reorder manually in WordPress")

if __name__ == '__main__':
    main()
