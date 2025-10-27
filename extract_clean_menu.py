#!/usr/bin/env python3
"""
Extract clean menu from WordPress export - preserving exact XML structure
"""

import re
from pathlib import Path
from collections import defaultdict

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-18 (3).xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/Menu-Import-Clean.xml')

def extract_postmeta(item_xml):
    """Extract all postmeta key-value pairs from a menu item"""
    postmeta = {}
    meta_entries = re.findall(r'<wp:postmeta>\s*<wp:meta_key><!\[CDATA\[(.*?)\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>\s*</wp:postmeta>', item_xml, re.DOTALL)
    for key, value in meta_entries:
        postmeta[key] = value
    return postmeta

def main():
    print("Reading WordPress export...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract the entire header up to the first wp:term
    header_match = re.search(r'^(.*?)<wp:term>', content, re.DOTALL)
    if not header_match:
        print("ERROR: Could not find header")
        return
    header = header_match.group(1)

    # Find the nav_menu term
    print("Finding nav_menu taxonomy term...")
    nav_menu_term = None
    all_terms = re.findall(r'(<wp:term>.*?</wp:term>)', content, re.DOTALL)
    for term in all_terms:
        if '<wp:term_taxonomy>nav_menu</wp:term_taxonomy>' in term:
            nav_menu_term = term
            print(f"✓ Found nav_menu term")
            break

    if not nav_menu_term:
        print("ERROR: Could not find nav_menu term")
        return

    # Find all items
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)

    nav_menu_items = []
    for item in all_items:
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        if post_type == 'nav_menu_item':
            item_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
            item_id = item_id_match.group(1) if item_id_match else 'NO_ITEM_ID'

            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            title = title_match.group(1) if title_match else ''

            postmeta = extract_postmeta(item)

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
                'unique_key': unique_key,
                'xml': item
            })

    print(f"Found {len(nav_menu_items)} total menu items")

    # Remove duplicates
    seen_keys = {}
    unique_items = []
    duplicates_count = 0

    for item in nav_menu_items:
        key = item['unique_key']
        if key in seen_keys:
            duplicates_count += 1
        else:
            seen_keys[key] = item
            unique_items.append(item)

    print(f"✓ Keeping {len(unique_items)} unique items")
    print(f"✓ Removing {duplicates_count} duplicates")

    # Build output
    output = header
    output += nav_menu_term + '\n'

    for item in unique_items:
        output += item['xml'] + '\n'

    output += '</channel>\n</rss>'

    # Write output
    print(f"\nWriting to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    print("✓ Done!")
    print(f"\nCreated: Menu-Import-Clean.xml")
    print(f"Contains: {len(unique_items)} unique menu items")
    print("\nIMPORTANT:")
    print("1. Make sure Menu is DELETED in WordPress")
    print("2. Go to Tools > Import")
    print("3. Upload: Menu-Import-Clean.xml")
    print("4. After import, go to Appearance > Menus")
    print("5. Assign menu to theme location and Save")

if __name__ == '__main__':
    main()
