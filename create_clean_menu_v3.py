#!/usr/bin/env python3
"""
Create a clean menu with taxonomy term and all duplicates removed
"""

import re
from pathlib import Path
from collections import defaultdict

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-18 (3).xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/Menu-Clean-NoDuplicates.xml')

def extract_postmeta(item_xml):
    """Extract all postmeta key-value pairs from a menu item"""
    postmeta = {}

    # Find all postmeta entries
    meta_entries = re.findall(r'<wp:postmeta>\s*<wp:meta_key><!\[CDATA\[(.*?)\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>\s*</wp:postmeta>', item_xml, re.DOTALL)

    for key, value in meta_entries:
        postmeta[key] = value

    return postmeta

def main():
    print("Reading WordPress export...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract header
    header_match = re.search(r'^(.*?)<wp:term>', content, re.DOTALL)
    header = header_match.group(1) if header_match else ''

    footer = '</channel>\n</rss>'

    # Extract the nav_menu taxonomy term
    print("Finding menu taxonomy term...")
    nav_menu_term = None
    all_terms = re.findall(r'(<wp:term>.*?</wp:term>)', content, re.DOTALL)
    for term in all_terms:
        if 'nav_menu' in term and 'Menu' in term:
            nav_menu_term = term
            print("✓ Found 'Menu' taxonomy term")
            break

    # Find all items
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)

    nav_menu_items = []

    for item in all_items:
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        if post_type == 'nav_menu_item':
            # Get item ID
            item_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
            item_id = item_id_match.group(1) if item_id_match else 'NO_ITEM_ID'

            # Get title
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            title = title_match.group(1) if title_match else ''

            # Extract postmeta
            postmeta = extract_postmeta(item)

            # Get menu item properties from postmeta
            menu_type = postmeta.get('_menu_item_type', '')
            object_id = postmeta.get('_menu_item_object_id', '0')
            object_type = postmeta.get('_menu_item_object', '')
            url = postmeta.get('_menu_item_url', '')

            # Create unique key
            if menu_type == 'custom':
                unique_key = f"custom:{url}"
            elif menu_type == 'post_type':
                unique_key = f"post:{object_type}:{object_id}"
            elif menu_type == 'taxonomy':
                unique_key = f"tax:{object_type}:{object_id}"
            else:
                unique_key = f"other:{item_id}"

            nav_menu_items.append({
                'item_id': item_id,
                'title': title,
                'menu_type': menu_type,
                'object_id': object_id,
                'object_type': object_type,
                'url': url,
                'unique_key': unique_key,
                'xml': item
            })

    print(f"Found {len(nav_menu_items)} menu items")

    # Find duplicates by unique_key
    seen_keys = {}
    duplicates_removed = []
    unique_items = []

    for item in nav_menu_items:
        key = item['unique_key']
        if key in seen_keys:
            # This is a duplicate
            duplicates_removed.append(item)
            first_item = seen_keys[key]
            print(f"  REMOVING DUPLICATE: Item {item['item_id']}: '{item['title'] if item['title'] else '(no title)'}' → {item['menu_type']} {item['object_id']}")
        else:
            # First occurrence - keep it
            seen_keys[key] = item
            unique_items.append(item)

    print(f"\n✓ Kept {len(unique_items)} unique menu items")
    print(f"✓ Removed {len(duplicates_removed)} duplicate menu items")

    # Build the output XML
    output = header

    # Add the nav_menu taxonomy term
    if nav_menu_term:
        output += nav_menu_term + '\n'
    else:
        print("⚠️  WARNING: No nav_menu term found - adding default")
        output += '<wp:term><wp:term_id>23</wp:term_id><wp:term_taxonomy>nav_menu</wp:term_taxonomy><wp:term_slug><![CDATA[menu]]></wp:term_slug><wp:term_name><![CDATA[Menu]]></wp:term_name></wp:term>\n'

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
    print("7. Go back to Appearance > Menus and your clean menu should be there!")

if __name__ == '__main__':
    main()
