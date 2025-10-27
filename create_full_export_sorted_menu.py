#!/usr/bin/env python3
"""
Create full export with clean, sorted menu (no attachments)
"""

import re
from pathlib import Path

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-19 (1).xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/WordPress-Full-Export-Sorted-Menu.xml')

def extract_postmeta(item_xml):
    """Extract all postmeta key-value pairs"""
    postmeta = {}
    meta_entries = re.findall(r'<wp:postmeta>\s*<wp:meta_key><!\[CDATA\[(.*?)\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>\s*</wp:postmeta>', item_xml, re.DOTALL)
    for key, value in meta_entries:
        postmeta[key] = value
    return postmeta

def should_exclude_from_sort(title):
    """Check if this item should be excluded from alphabetical sorting"""
    exclude_keywords = [
        'playlist',
        'this blog',
        'out of the swamp',
        'dying changes everything',
        'chapter',
        'movement',
        'introduction',
        'epilogue'
    ]
    title_lower = title.lower()
    for keyword in exclude_keywords:
        if keyword in title_lower:
            return True
    return False

def main():
    print("Reading WordPress export...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract header and footer
    header_match = re.search(r'^(.*?)<item>', content, re.DOTALL)
    header = header_match.group(1) if header_match else ''
    footer = '</channel>\n</rss>'

    # Find all items
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)

    # Separate items by type
    menu_items = []
    other_items = []

    for item in all_items:
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        # Skip attachments (they cause null byte errors)
        if post_type == 'attachment':
            continue

        if post_type == 'nav_menu_item':
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            title = title_match.group(1) if title_match else ''

            menu_order_match = re.search(r'<wp:menu_order>(\d+)</wp:menu_order>', item)
            menu_order = int(menu_order_match.group(1)) if menu_order_match else 0

            item_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
            item_id = item_id_match.group(1) if item_id_match else 'NO_ID'

            postmeta = extract_postmeta(item)
            object_id = postmeta.get('_menu_item_object_id', '0')
            object_type = postmeta.get('_menu_item_object', '')
            menu_type = postmeta.get('_menu_item_type', '')
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

            menu_items.append({
                'item_id': item_id,
                'title': title,
                'menu_order': menu_order,
                'unique_key': unique_key,
                'object_id': object_id,
                'xml': item
            })
        else:
            other_items.append(item)

    print(f"Found {len(menu_items)} menu items")
    print(f"Found {len(other_items)} other items (posts, pages, etc.)")

    # Remove duplicate menu items
    seen_keys = {}
    unique_menu_items = []
    duplicates_removed = 0

    for item in menu_items:
        key = item['unique_key']
        if key in seen_keys:
            duplicates_removed += 1
        else:
            seen_keys[key] = item
            unique_menu_items.append(item)

    print(f"✓ Removed {duplicates_removed} duplicate menu items")

    # Get post titles for sorting
    posts_titles = {}
    for item_xml in other_items:
        post_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item_xml)
        post_id = post_id_match.group(1) if post_id_match else None

        title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item_xml)
        title = title_match.group(1) if title_match else ''

        if post_id:
            posts_titles[post_id] = title

    # Update menu items with display titles
    for item in unique_menu_items:
        if item['object_id'] in posts_titles:
            item['display_title'] = posts_titles[item['object_id']]
        elif item['title']:
            item['display_title'] = item['title']
        else:
            item['display_title'] = f"Menu Item {item['item_id']}"

    # Separate excluded and sortable items
    excluded_items = []
    sortable_items = []

    for item in unique_menu_items:
        if should_exclude_from_sort(item['display_title']):
            excluded_items.append(item)
        else:
            sortable_items.append(item)

    print(f"✓ {len(excluded_items)} items excluded from sorting")
    print(f"✓ {len(sortable_items)} items to sort alphabetically")

    # Sort
    sortable_items.sort(key=lambda x: x['display_title'].lower())
    excluded_items.sort(key=lambda x: x['menu_order'])

    # Combine
    final_menu_items = excluded_items + sortable_items

    # Update menu_order
    for i, item in enumerate(final_menu_items, 1):
        item['xml'] = re.sub(
            r'<wp:menu_order>\d+</wp:menu_order>',
            f'<wp:menu_order>{i}</wp:menu_order>',
            item['xml']
        )

    print(f"\nFirst 10 menu items:")
    for i, item in enumerate(final_menu_items[:10], 1):
        print(f"  {i}. {item['display_title']}")

    # Build output
    output = header

    # Add all non-menu items first
    for item in other_items:
        output += item + '\n'

    # Add sorted menu items
    for item in final_menu_items:
        output += item['xml'] + '\n'

    output += footer

    # Write output
    print(f"\nWriting to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    print("✓ Done!")
    print(f"\nCreated full export with:")
    print(f"  - {len(other_items)} posts/pages/other items")
    print(f"  - {len(final_menu_items)} unique menu items (sorted)")
    print(f"  - NO attachments (to avoid errors)")

if __name__ == '__main__':
    main()
