#!/usr/bin/env python3
"""
Create a clean menu with all duplicates removed
"""

import re
from pathlib import Path
from collections import defaultdict

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-18 (3).xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/Menu-Clean-NoDuplicates.xml')

def main():
    print("Reading WordPress export...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract header and footer
    header_match = re.search(r'^(.*?)<item>', content, re.DOTALL)
    header = header_match.group(1) if header_match else ''

    footer = '</channel>\n</rss>'

    # Find all nav_menu_item entries
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)

    nav_menu_items = []
    nav_menu_taxonomy = []

    for item in all_items:
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        # Check if it's a nav_menu taxonomy term
        if '<wp:term_taxonomy>nav_menu</wp:term_taxonomy>' in item:
            nav_menu_taxonomy.append(item)
        elif post_type == 'nav_menu_item':
            nav_menu_items.append(item)

    print(f"Found {len(nav_menu_items)} menu items")
    print(f"Found {len(nav_menu_taxonomy)} menu taxonomy terms")

    # Parse menu items and track duplicates
    menu_data = []
    for item in nav_menu_items:
        # Get object_id (the post this menu item points to)
        obj_id_match = re.search(r'<wp:menu_item_object_id>(\d+)</wp:menu_item_object_id>', item)
        obj_id = obj_id_match.group(1) if obj_id_match else 'NO_ID'

        # Get object type
        obj_type_match = re.search(r'<wp:menu_item_object><!\[CDATA\[(.*?)\]\]></wp:menu_item_object>', item)
        obj_type = obj_type_match.group(1) if obj_type_match else 'NO_TYPE'

        # Get menu item type
        menu_type_match = re.search(r'<wp:menu_item_type><!\[CDATA\[(.*?)\]\]></wp:menu_item_type>', item)
        menu_type = menu_type_match.group(1) if menu_type_match else 'NO_MENU_TYPE'

        # Get item ID
        item_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
        item_id = item_id_match.group(1) if item_id_match else 'NO_ITEM_ID'

        # Get title
        title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
        title = title_match.group(1) if title_match else 'NO_TITLE'

        # Create a unique key for this menu item based on what it points to
        # For custom links, use the URL; for posts/pages, use object_id
        if menu_type == 'custom':
            url_match = re.search(r'<wp:menu_item_url><!\[CDATA\[(.*?)\]\]></wp:menu_item_url>', item)
            url = url_match.group(1) if url_match else ''
            unique_key = f"custom:{url}"
        else:
            unique_key = f"{obj_type}:{obj_id}"

        menu_data.append({
            'item_id': item_id,
            'title': title,
            'object_id': obj_id,
            'object_type': obj_type,
            'menu_type': menu_type,
            'unique_key': unique_key,
            'xml': item
        })

    # Find duplicates by unique_key
    seen_keys = {}
    duplicates_removed = []
    unique_items = []

    for item in menu_data:
        key = item['unique_key']
        if key in seen_keys:
            # This is a duplicate
            duplicates_removed.append(item)
            print(f"  REMOVING DUPLICATE: Item {item['item_id']}: '{item['title']}' (duplicate of item {seen_keys[key]['item_id']})")
        else:
            # First occurrence - keep it
            seen_keys[key] = item
            unique_items.append(item)

    print(f"\n✓ Kept {len(unique_items)} unique menu items")
    print(f"✓ Removed {len(duplicates_removed)} duplicate menu items")

    # Build the output XML
    output = header

    # Add taxonomy terms first
    for term in nav_menu_taxonomy:
        output += term + '\n'

    # Add unique menu items
    for item in unique_items:
        output += item['xml'] + '\n'

    output += footer

    # Write the output
    print(f"\nWriting to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    print("✓ Done!")
    print(f"\nCreated clean menu with {len(unique_items)} unique items")
    print("\nNext steps:")
    print("1. Go to WordPress Admin > Appearance > Menus")
    print("2. Delete the existing 'Menu' completely")
    print("3. Go to WordPress Admin > Tools > Import")
    print("4. Choose 'WordPress' importer")
    print("5. Upload: Menu-Clean-NoDuplicates.xml")
    print("6. Complete the import")
    print("\nYour menu will have all duplicates removed!")

if __name__ == '__main__':
    main()
