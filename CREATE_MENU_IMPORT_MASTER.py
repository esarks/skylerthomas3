#!/usr/bin/env python3
"""
MASTER SCRIPT: Create WordPress Menu Import File
================================================

This is THE definitive script for creating a WordPress import file with a clean,
sorted menu that will actually import correctly.

WHY THIS WORKS:
1. Includes BOTH posts AND menu items (menu items reference posts by ID)
2. Removes duplicate menu items
3. Sorts alphabetically (except special items: playlists, blog, book chapters)
4. Excludes attachments (they cause null byte errors in WordPress import)

HOW TO USE:
1. Get a fresh WordPress export and put it in Downloads folder
2. Update EXPORT_FILE path below to point to your latest export
3. Run: python3 CREATE_MENU_IMPORT_MASTER.py
4. Import the generated file: WordPress-Menu-Import-FINAL.xml

WHAT IT CREATES:
- Complete WordPress import file with posts + clean sorted menu
- Ready to import into WordPress
- No errors, no empty menus
"""

import re
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION - UPDATE THIS PATH TO YOUR LATEST EXPORT
# ============================================================================
EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-19 (1).xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/WordPress-Menu-Import-FINAL.xml')

# Items to keep in original order (not sorted alphabetically)
EXCLUDE_FROM_SORT = [
    'playlist',
    'this blog',
    'out of the swamp',
    'dying changes everything',
    'chapter',
    'movement',
    'introduction',
    'epilogue'
]

# ============================================================================
# FUNCTIONS
# ============================================================================

def extract_postmeta(item_xml):
    """Extract all postmeta key-value pairs from a WordPress item"""
    postmeta = {}
    meta_entries = re.findall(
        r'<wp:postmeta>\s*<wp:meta_key><!\[CDATA\[(.*?)\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>\s*</wp:postmeta>',
        item_xml,
        re.DOTALL
    )
    for key, value in meta_entries:
        postmeta[key] = value
    return postmeta

def should_exclude_from_sort(title):
    """Check if this menu item should NOT be sorted alphabetically"""
    title_lower = title.lower()
    for keyword in EXCLUDE_FROM_SORT:
        if keyword in title_lower:
            return True
    return False

def create_unique_key(item, postmeta):
    """Create a unique key for deduplication"""
    menu_type = postmeta.get('_menu_item_type', '')
    object_id = postmeta.get('_menu_item_object_id', '0')
    object_type = postmeta.get('_menu_item_object', '')
    url = postmeta.get('_menu_item_url', '')

    if menu_type == 'custom':
        return f"custom:{url}"
    elif menu_type == 'post_type':
        return f"post:{object_type}:{object_id}"
    elif menu_type == 'taxonomy':
        return f"tax:{object_type}:{object_id}"
    else:
        item_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
        item_id = item_id_match.group(1) if item_id_match else 'NO_ID'
        return f"other:{item_id}"

# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    print("=" * 70)
    print("MASTER SCRIPT: Create WordPress Menu Import File")
    print("=" * 70)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Export file: {EXPORT_FILE}")

    if not EXPORT_FILE.exists():
        print(f"\n❌ ERROR: Export file not found: {EXPORT_FILE}")
        print("Please update EXPORT_FILE path in this script.")
        return

    # Read export file
    print("\n📖 Reading WordPress export...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract header and footer
    header_match = re.search(r'^(.*?)<item>', content, re.DOTALL)
    header = header_match.group(1) if header_match else ''
    footer = '</channel>\n</rss>'

    # Find nav_menu term (required for menu import)
    nav_menu_term = None
    all_terms = re.findall(r'(<wp:term>.*?</wp:term>)', content, re.DOTALL)
    for term in all_terms:
        if '<wp:term_taxonomy>nav_menu</wp:term_taxonomy>' in term:
            nav_menu_term = term
            break

    # Find all items
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)

    # Separate items by type
    menu_items = []
    other_items = []
    posts_titles = {}
    attachments_count = 0

    print("📋 Processing items...")
    for item in all_items:
        post_type_match = re.search(r'<wp:post_type><!\[CDATA\[(.*?)\]\]></wp:post_type>', item)
        post_type = post_type_match.group(1) if post_type_match else None

        # SKIP ATTACHMENTS - they cause null byte errors
        if post_type == 'attachment':
            attachments_count += 1
            continue

        # Extract menu items
        if post_type == 'nav_menu_item':
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            title = title_match.group(1) if title_match else ''

            menu_order_match = re.search(r'<wp:menu_order>(\d+)</wp:menu_order>', item)
            menu_order = int(menu_order_match.group(1)) if menu_order_match else 0

            postmeta = extract_postmeta(item)
            unique_key = create_unique_key(item, postmeta)
            object_id = postmeta.get('_menu_item_object_id', '0')

            menu_items.append({
                'title': title,
                'menu_order': menu_order,
                'unique_key': unique_key,
                'object_id': object_id,
                'xml': item
            })
        else:
            # Keep all other items (posts, pages, etc.)
            other_items.append(item)

            # Build title map for menu sorting
            if post_type in ['post', 'page']:
                post_id_match = re.search(r'<wp:post_id>(\d+)</wp:post_id>', item)
                post_id = post_id_match.group(1) if post_id_match else None

                title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
                title = title_match.group(1) if title_match else ''

                if post_id:
                    posts_titles[post_id] = title

    print(f"  ✓ Found {len(menu_items)} menu items")
    print(f"  ✓ Found {len(other_items)} other items (posts, pages, etc.)")
    print(f"  ✓ Skipped {attachments_count} attachments")

    # Remove duplicates
    print("\n🔍 Removing duplicates...")
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

    print(f"  ✓ Removed {duplicates_removed} duplicate menu items")
    print(f"  ✓ {len(unique_menu_items)} unique menu items")

    # Update menu items with actual post titles for sorting
    for item in unique_menu_items:
        object_id = item['object_id']
        if object_id in posts_titles:
            item['display_title'] = posts_titles[object_id]
        elif item['title']:
            item['display_title'] = item['title']
        else:
            item['display_title'] = f"Menu Item"

    # Separate items: excluded from sort vs. sortable
    print("\n📂 Sorting menu...")
    excluded_items = []
    sortable_items = []

    for item in unique_menu_items:
        if should_exclude_from_sort(item['display_title']):
            excluded_items.append(item)
        else:
            sortable_items.append(item)

    # Sort
    excluded_items.sort(key=lambda x: x['menu_order'])  # Keep original order
    sortable_items.sort(key=lambda x: x['display_title'].lower())  # Alphabetical

    print(f"  ✓ {len(excluded_items)} items kept in original order")
    print(f"  ✓ {len(sortable_items)} items sorted alphabetically")

    # Combine: excluded first, then alphabetical
    final_menu_items = excluded_items + sortable_items

    # Update menu_order values
    for i, item in enumerate(final_menu_items, 1):
        item['xml'] = re.sub(
            r'<wp:menu_order>\d+</wp:menu_order>',
            f'<wp:menu_order>{i}</wp:menu_order>',
            item['xml']
        )

    # Show preview
    print("\n📋 Menu preview (first 10 items):")
    for i, item in enumerate(final_menu_items[:10], 1):
        print(f"  {i}. {item['display_title']}")

    print("\n📋 Menu preview (last 5 items):")
    for i, item in enumerate(final_menu_items[-5:], len(final_menu_items)-4):
        print(f"  {i}. {item['display_title']}")

    # Build output file
    print("\n📝 Building output file...")
    output = header

    # Add nav_menu term (required)
    if nav_menu_term:
        output += nav_menu_term + '\n'

    # Add all posts/pages/etc FIRST
    for item in other_items:
        output += item + '\n'

    # Add sorted menu items
    for item in final_menu_items:
        output += item['xml'] + '\n'

    output += footer

    # Write output
    print(f"\n💾 Writing to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output)

    # Summary
    print("\n" + "=" * 70)
    print("✅ SUCCESS!")
    print("=" * 70)
    print(f"\nCreated: {OUTPUT_FILE}")
    print(f"\nContains:")
    print(f"  • {len(other_items)} posts/pages/other items")
    print(f"  • {len(final_menu_items)} unique menu items (sorted)")
    print(f"  • NO attachments (prevents import errors)")
    print(f"\nMenu structure:")
    print(f"  • {len(excluded_items)} items in original order (playlists, blog, chapters)")
    print(f"  • {len(sortable_items)} items sorted A-Z")
    print(f"\nReady to import into WordPress!")
    print("=" * 70)

if __name__ == '__main__':
    main()
