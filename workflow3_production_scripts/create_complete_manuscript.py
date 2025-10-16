#!/usr/bin/env python3
"""
WORKFLOW3: Create complete manuscript for PUBLISHER VERSION

This script combines all revised chapters for the NEW publisher-ready version.

Structure:
- Movement 1: 3 chapters with 3 songs (revised from original 4)
- Movement 2: 4 chapters (to be revised)
- Movement 3: 6 chapters (to be revised)

Source files: /skylerthomas3.wiki/REVISED-*.md
Output: /skylerthomas3/KDP/COMPLETE-MANUSCRIPT.md
"""

import os

def combine_manuscript():
    """Combine all content files in order"""

    # Paths relative to this script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skylerthomas3_dir = os.path.dirname(script_dir)  # Parent of workflow3_production_scripts
    skylerthomas3_wiki = os.path.join(os.path.dirname(skylerthomas3_dir), 'skylerthomas3.wiki')
    kdp_dir = os.path.join(skylerthomas3_dir, 'KDP')

    # Ensure KDP directory exists
    os.makedirs(kdp_dir, exist_ok=True)

    print("\n" + "="*70)
    print("WORKFLOW3: CREATING PUBLISHER VERSION MANUSCRIPT")
    print("="*70)
    print(f"\nSource: {skylerthomas3_wiki}")
    print(f"Output: {kdp_dir}")
    print("\n" + "="*70)

    # Define the order of files for REVISED publisher version
    file_order = [
        # Front Matter (to be created)
        ('front', '00_title-page.md', False),
        ('front', '00_copyright-page.md', False),
        ('front', '00_dedication.md', False),
        ('front', '00_table-of-contents.md', False),
        ('front', '00_introduction.md', False),

        # MOVEMENT 1: IN THE SWAMP (3 chapters with 3 songs - REVISED)
        ('wiki', 'REVISED-01_movement-1-intro.md', True),
        ('wiki', 'REVISED-02_chapter-01-my-swamp.md', True),  # Song: "I Will Rise"
        ('wiki', 'REVISED-03_chapter-02-but-then-i-prayed.md', True),  # Song: "But Then I Prayed"
        ('wiki', 'REVISED-04_chapter-03-dying-changes.md', True),  # Song: "Dying Changes Everything"

        # MOVEMENT 2: AT THE WATER'S EDGE (4 chapters - TO BE REVISED)
        ('front', 'REVISED-06_movement-2-intro.md', False),
        ('front', 'REVISED-07_chapter-03-living-waters-edge.md', False),
        ('front', 'REVISED-08_chapter-04-shadow-grace.md', False),
        ('front', 'REVISED-09_chapter-05-amazing-grace.md', False),
        ('front', 'REVISED-10_chapter-06-dig-deeper.md', False),

        # MOVEMENT 3: UNFORCED RHYTHMS (6 chapters - TO BE REVISED)
        ('front', 'REVISED-11_movement-3-intro.md', False),
        ('front', 'REVISED-12_chapter-07-unforced-rhythms.md', False),
        ('front', 'REVISED-13_chapter-08-deep-roots.md', False),
        ('front', 'REVISED-14_chapter-09-redemptions-story.md', False),
        ('front', 'REVISED-15_chapter-10-nothing-wasted.md', False),
        ('front', 'REVISED-16_chapter-11-this-moment.md', False),

        # Back Matter (to be created)
        ('front', '99_epilogue.md', False),
        ('front', '99_about-author.md', False),
    ]

    combined_content = []
    found_count = 0
    missing_count = 0
    missing_files = []

    for location, filename, exists in file_order:
        if location == 'wiki':
            filepath = os.path.join(skylerthomas3_wiki, filename)
        else:
            filepath = os.path.join(skylerthomas3_dir, filename)

        if os.path.exists(filepath):
            print(f"✓ Adding: {filename}")
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                combined_content.append(content)
            found_count += 1
        else:
            if exists:
                print(f"✗ MISSING (expected): {filename}")
            else:
                print(f"○ TO DO: {filename}")
            missing_count += 1
            missing_files.append(filename)

    # Join all content
    final_content = '\n\n'.join(combined_content)

    # Write to output
    output_file = os.path.join(kdp_dir, 'COMPLETE-MANUSCRIPT.md')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

    # Get file size
    file_size = os.path.getsize(output_file)
    file_size_kb = file_size / 1024

    print("\n" + "="*70)
    print("MANUSCRIPT STATUS")
    print("="*70)
    print(f"✓ Files included: {found_count}")
    print(f"○ Files pending: {missing_count}")
    print(f"\n✓ Created: COMPLETE-MANUSCRIPT.md ({file_size_kb:.1f} KB)")
    print(f"Location: {output_file}")

    if missing_files:
        print("\n" + "="*70)
        print("PENDING FILES (still need to be created/revised):")
        print("="*70)
        for f in missing_files:
            print(f"  ○ {f}")

    print("="*70)

if __name__ == '__main__':
    combine_manuscript()
