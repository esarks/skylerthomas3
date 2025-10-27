#!/usr/bin/env python3
"""
Sort menu alphabetically except for Playlist, This Blog, and book chapters
"""

import re
from pathlib import Path

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-18 (4).xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/Menu-Sorted-Alphabetically.xml')

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

    # Find nav_menu term
    nav_menu_term = None
    all_terms = re.findall(r'(<wp:term>.*?</wp:term>)', content, re.DOTALL)
    for term in all_terms:
        if '<wp:term_taxonomy>nav_menu</wp:term_taxonomy>' in term:
            nav_menu_term = term
            break

    # Find all items
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)

    # Get all menu items with their data
    menu_items = []
    non_menu_items = []

    for item in all_items:
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        if post_type == 'nav_menu_item':
            # Get title
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            title = title_match.group(1) if title_match else ''

            # Get menu order
            menu_order_match = re.search(r'<wp:menu_order>(\d+)</wp:menu_order>', item)
            menu_order = int(menu_order_match.group(1)) if menu_order_match else 0

            # Get item ID
            item_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
            item_id = item_id_match.group(1) if item_id_match else 'NO_ID'

            # Get object_id to fetch actual post title
            postmeta = extract_postmeta(item)
            object_id = postmeta.get('_menu_item_object_id', '0')
            menu_type = postmeta.get('_menu_item_type', '')

            menu_items.append({
                'item_id': item_id,
                'title': title,
                'menu_order': menu_order,
                'object_id': object_id,
                'menu_type': menu_type,
                'xml': item
            })

    print(f"Found {len(menu_items)} menu items")

    # Get actual post titles for items that link to posts
    posts_titles = {}
    for item in all_items:
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        if post_type in ['post', 'page']:
            post_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
            post_id = post_id_match.group(1) if post_id_match else None

            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            title = title_match.group(1) if title_match else ''

            if post_id:
                posts_titles[post_id] = title

    # Update menu items with actual post titles
    for item in menu_items:
        if item['object_id'] in posts_titles:
            item['display_title'] = posts_titles[item['object_id']]
        elif item['title']:
            item['display_title'] = item['title']
        else:
            item['display_title'] = f"Menu Item {item['item_id']}"

    # Separate items to exclude from sorting
    excluded_items = []
    sortable_items = []

    for item in menu_items:
        if should_exclude_from_sort(item['display_title']):
            excluded_items.append(item)
            print(f"  Excluding from sort: {item['display_title']}")
        else:
            sortable_items.append(item)

    print(f"\n✓ {len(excluded_items)} items excluded from sorting")
    print(f"✓ {len(sortable_items)} items to sort alphabetically")

    # Sort the sortable items alphabetically
    sortable_items.sort(key=lambda x: x['display_title'].lower())

    # Combine: excluded items first (in original order), then sorted items
    excluded_items.sort(key=lambda x: x['menu_order'])

    final_menu_items = excluded_items + sortable_items

    # Update menu_order for all items
    for i, item in enumerate(final_menu_items, 1):
        # Update the menu_order in the XML
        item['xml'] = re.sub(
            r'<wp:menu_order>\d+</wp:menu_order>',
            f'<wp:menu_order>{i}</wp:menu_order>',
            item['xml']
        )

    print(f"\nFinal menu order:")
    print("First 10 items:")
    for i, item in enumerate(final_menu_items[:10], 1):
        print(f"  {i}. {item['display_title']}")

    print(f"\nLast 10 items:")
    for i, item in enumerate(final_menu_items[-10:], len(final_menu_items)-9):
        print(f"  {i}. {item['display_title']}")

    # Build output
    output = header
    if nav_menu_term:
        output += nav_menu_term + '\n'

    for item in final_menu_items:
        output += item['xml'] + '\n'

    output += footer

    # Write output
    print(f"\nWriting to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    print("✓ Done!")
    print(f"\nCreated menu with:")
    print(f"  - {len(excluded_items)} items kept in original position")
    print(f"  - {len(sortable_items)} items sorted alphabetically")
    print(f"  - Total: {len(final_menu_items)} items")

if __name__ == '__main__':
    main()
