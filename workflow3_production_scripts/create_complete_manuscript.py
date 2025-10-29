#!/usr/bin/env python3
"""
WORKFLOW3: Create complete manuscript for PUBLISHER VERSION

This script combines all revised chapters for the NEW publisher-ready version.

Structure:
- Movement 1: 3 chapters with 3 songs (revised from original 4)
- Movement 2: 4 chapters with 4 songs (revised)
- Movement 3: 5 chapters with 5 songs (revised from original 6 - removed Devil's Run)

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
        # Front Matter
        ('wiki', 'REVISED-00_title-page.md', True),
        ('wiki', 'REVISED-00_copyright-page.md', True),
        ('wiki', 'REVISED-00_dedication.md', True),
        ('front', '00_table-of-contents.md', False),
        ('wiki', 'REVISED-00_introduction-PUBLISHER.md', True),  # REVISED - condensed by 42%

        # MOVEMENT 1: IN THE SWAMP (3 chapters with 3 songs - REVISED)
        ('wiki', 'REVISED-01_movement-1-intro.md', True),
        ('wiki', 'REVISED-02_chapter-01-my-swamp.md', True),  # Song: "I Will Rise"
        ('wiki', 'REVISED-03_chapter-02-but-then-i-prayed.md', True),  # Song: "But Then I Prayed"
        ('wiki', 'REVISED-04_chapter-03-dying-changes.md', True),  # Song: "Dying Changes Everything"

        # MOVEMENT 2: AT THE WATER'S EDGE (4 chapters - REVISED)
        ('wiki', 'REVISED-06_movement-2-intro.md', True),
        ('wiki', 'REVISED-07_chapter-04-living-waters-edge.md', True),  # Song: "Living Waters Edge"
        ('wiki', 'REVISED-08_chapter-05-shadow-grace.md', True),  # Song: "Shadow of Your Grace"
        ('wiki', 'REVISED-09_chapter-06-amazing-grace.md', True),  # Song: "Amazing Grace"
        ('wiki', 'REVISED-10_chapter-07-dig-deeper.md', True),  # Song: "Dig a Little Deeper"

        # MOVEMENT 3: UNFORCED RHYTHMS (5 chapters - REVISED)
        ('wiki', 'REVISED-11_movement-3-intro.md', True),
        ('wiki', 'REVISED-12_chapter-08-unforced-rhythms.md', True),  # Song: "Mindful Bliss of Grace"
        ('wiki', 'REVISED-13_chapter-09-deep-roots.md', True),  # Song: "I Will Trust You Lord"
        ('wiki', 'REVISED-14_chapter-10-redemption-story.md', True),  # Song: "Redemption Story"
        ('wiki', 'REVISED-15_chapter-11-nothing-wasted.md', True),  # Song: "Nothing is Wasted"
        ('wiki', 'REVISED-16_chapter-12-this-moment.md', True),  # Song: "This Moment is Enough"

        # Back Matter
        ('wiki', 'REVISED-99_epilogue.md', True),
        ('wiki', 'REVISED-99_acknowledgments.md', True),
        ('wiki', 'REVISED-99_about-author.md', True),
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

            # Add page break before each section (except first)
            if found_count > 0:
                combined_content.append("\n\n\\pagebreak\n\n")

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
    final_content = '\n'.join(combined_content)

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
