#!/usr/bin/env python3
"""
Assemble complete manuscript from REVISED files in skylerthomas3.wiki
Creates a single markdown file ready for PDF/EPUB conversion
"""

import os
from pathlib import Path

# Paths
WIKI_DIR = Path(__file__).parent.parent.parent / "skylerthomas3.wiki"
OUTPUT_DIR = Path(__file__).parent
OUTPUT_FILE = OUTPUT_DIR / "complete_manuscript.md"

# File order for manuscript assembly
MANUSCRIPT_FILES = [
    # Pre-Book Content
    "REVISED-00_title-page.md",
    "REVISED-00_copyright-page.md",
    "REVISED-00_dedication.md",

    # Introduction
    "REVISED-00_introduction-PUBLISHER.md",

    # Movement 1: In the Swamp
    "REVISED-01_movement-1-intro.md",
    "REVISED-02_chapter-01-my-swamp.md",
    "REVISED-03_chapter-02-but-then-i-prayed.md",
    "REVISED-04_chapter-03-dying-changes.md",

    # Movement 2: At the Water's Edge
    "REVISED-06_movement-2-intro.md",
    "REVISED-07_chapter-04-living-waters-edge.md",
    "REVISED-08_chapter-05-shadow-grace.md",
    "REVISED-09_chapter-06-amazing-grace.md",
    "REVISED-10_chapter-07-dig-deeper.md",

    # Movement 3: Unforced Rhythms
    "REVISED-11_movement-3-intro.md",
    "REVISED-12_chapter-08-unforced-rhythms.md",
    "REVISED-13_chapter-09-deep-roots.md",
    "REVISED-14_chapter-10-redemption-story.md",
    "REVISED-15_chapter-11-nothing-wasted.md",

    # More chapters as you add them...
    # Add new REVISED files here as you complete them

    # Post-Book Content
    "REVISED-99_epilogue.md",
    "REVISED-99_acknowledgments.md",
    "REVISED-99_about-author.md",
]

def clean_metadata(content):
    """Remove WordPress metadata from content"""
    lines = content.split('\n')
    cleaned_lines = []
    skip_metadata = False

    for line in lines:
        # Skip YAML metadata blocks
        if line.strip() == '---':
            if not skip_metadata:
                skip_metadata = True
                continue
            else:
                skip_metadata = False
                continue

        if skip_metadata:
            continue

        # Skip WordPress metadata
        if line.startswith('wp_post_id:') or line.startswith('last_updated:'):
            continue
        if line.startswith('*Last updated:'):
            continue

        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

def assemble_manuscript():
    """Assemble all REVISED files into a single manuscript"""
    print("\n" + "="*70)
    print("ASSEMBLING PUBLISHER REVIEW MANUSCRIPT")
    print("="*70)
    print(f"\nSource: {WIKI_DIR}")
    print(f"Output: {OUTPUT_FILE}")

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    manuscript_content = []
    manuscript_content.append("# Out of the Swamp: How I Found Truth")
    manuscript_content.append("\n## Publisher's Review Edition\n")
    manuscript_content.append("\n---\n")

    files_added = 0
    files_missing = []

    for filename in MANUSCRIPT_FILES:
        filepath = WIKI_DIR / filename

        if filepath.exists():
            print(f"✓ Adding: {filename}")

            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Clean metadata
            content = clean_metadata(content)

            # Add page break before each section (except first)
            if files_added > 0:
                manuscript_content.append("\n\n---\n\\pagebreak\n\n")

            manuscript_content.append(content)
            files_added += 1
        else:
            files_missing.append(filename)
            print(f"⚠️  Missing: {filename}")

    # Write complete manuscript
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(manuscript_content))

    print("\n" + "-"*70)
    print("ASSEMBLY COMPLETE")
    print("-"*70)
    print(f"Files added: {files_added}")
    if files_missing:
        print(f"Files missing: {len(files_missing)}")
        for f in files_missing:
            print(f"  - {f}")

    # Calculate file size
    file_size = os.path.getsize(OUTPUT_FILE)
    if file_size < 1024:
        size_str = f"{file_size} bytes"
    elif file_size < 1024*1024:
        size_str = f"{file_size/1024:.1f} KB"
    else:
        size_str = f"{file_size/(1024*1024):.1f} MB"

    print(f"\nOutput file: {OUTPUT_FILE}")
    print(f"File size: {size_str}")
    print("\n" + "="*70 + "\n")

    return OUTPUT_FILE

if __name__ == "__main__":
    assemble_manuscript()
