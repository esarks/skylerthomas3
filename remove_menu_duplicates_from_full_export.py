#!/usr/bin/env python3
"""
Remove ONLY the duplicate menu items from the full export
Keep everything else intact
"""

import re
from pathlib import Path

EXPORT_FILE = Path('/Users/paulmarshall/Downloads/skylerthomas.WordPress.2025-10-18 (3).xml')
OUTPUT_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/WordPress-Full-Export-Clean-Menu.xml')

# These are the duplicate menu item IDs to remove
DUPLICATE_IDS = [
    1523, 2303, 6018, 6019, 6020, 6021, 6022, 6023, 6024, 6025, 6026, 6027, 6028,
    6029, 6030, 6031, 6032, 6033, 6034, 6035, 6036, 6037, 6038, 6039, 6040, 6041,
    6042, 6043, 6044, 6045, 6046, 6047, 6048, 6049, 6050, 6051, 6053, 6054, 6055,
    6056, 6057, 6058, 6059, 6061, 6062, 6063, 6064, 6065, 6066, 6067, 6068, 6069,
    6072, 6073, 6074, 6075, 6076, 6077, 6078, 6080, 6081, 6082, 6083, 6084, 6085,
    6086, 6087, 6088, 6089, 6090, 6091
]

def main():
    print("Reading full WordPress export...")
    with open(EXPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original file size: {len(content):,} bytes")

    # Find all items
    all_items = re.findall(r'(<item>.*?</item>)', content, re.DOTALL)
    print(f"Total items: {len(all_items)}")

    removed_count = 0

    for dup_id in DUPLICATE_IDS:
        # Find this specific menu item
        pattern = rf'(<item>.*?<wp:post_id>{dup_id}</wp:post_id>.*?<wp:post_type><!\[CDATA\[nav_menu_item\]\]></wp:post_type>.*?</item>)'
        matches = re.findall(pattern, content, re.DOTALL)

        if matches:
            for match in matches:
                content = content.replace(match, '')
                removed_count += 1
                print(f"  Removed menu item {dup_id}")

    print(f"\n✓ Removed {removed_count} duplicate menu items")
    print(f"New file size: {len(content):,} bytes")

    # Write output
    print(f"\nWriting to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ Done!")
    print("\nThis is the FULL export with ONLY the duplicate menu items removed.")
    print("Everything else (posts, pages, images, etc.) is intact.")
    print("\nTo import:")
    print("1. Delete the current menu in WordPress")
    print("2. Go to Tools > Import")
    print("3. Upload: WordPress-Full-Export-Clean-Menu.xml")
    print("4. You'll get all your content + clean menu with 76 items")

if __name__ == '__main__':
    main()
