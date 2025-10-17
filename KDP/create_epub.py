#!/usr/bin/env python3
"""
Convert manuscript to EPUB format for ebook readers
Uses pandoc for conversion with proper metadata
"""

import subprocess
import os
import sys
import re

def clean_manuscript_for_epub(input_file, output_file):
    """Remove YAML metadata blocks, TOC, and WordPress-specific content"""

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    in_metadata = False
    in_toc = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check if this is a metadata block (--- followed by metadata fields)
        if line.strip() == '---':
            if not in_metadata:
                # Not currently in metadata, check if this starts a metadata block
                is_metadata_block = False
                for j in range(i + 1, min(i + 5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line:  # Found first non-empty line
                        if next_line.startswith('wp_post_id:') or next_line.startswith('last_updated:'):
                            is_metadata_block = True
                        break

                if is_metadata_block:
                    # This opens a metadata block
                    in_metadata = True
                    i += 1
                    continue
                else:
                    # Just a decorative divider, skip it but preserve spacing
                    # Add a blank line to ensure proper markdown parsing
                    cleaned_lines.append('\n')
                    i += 1
                    continue
            else:
                # Currently in metadata, this closes the metadata block
                in_metadata = False
                i += 1
                continue

        if in_metadata:
            i += 1
            continue

        # Detect Table of Contents section
        if line.startswith('# Table of Contents'):
            in_toc = True
            i += 1
            continue

        # Exit TOC when we hit the next H1 heading
        if in_toc and line.startswith('# '):
            in_toc = False
            # Fall through to add this line

        # Skip everything in TOC section
        if in_toc:
            i += 1
            continue

        # Skip WordPress metadata lines
        if line.startswith('wp_post_id:') or line.startswith('last_updated:'):
            i += 1
            continue

        if line.startswith('*Last updated:'):
            i += 1
            continue

        # Skip \newpage commands
        if line.strip() == '\\newpage':
            i += 1
            continue

        # Skip QR code images (not useful in digital EPUB - readers can click links directly)
        if line.startswith('![') and 'qr-' in line.lower():
            i += 1
            continue

        # Skip "Listen at:" lines (redundant in EPUB - song title is already a clickable link)
        if line.startswith('**Listen at:**') or line.startswith('Listen at:'):
            i += 1
            continue

        cleaned_lines.append(line)
        i += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

def create_epub():
    """Convert markdown to EPUB using pandoc"""

    input_file = "/Users/paulmarshall/Documents/GitHub/skylerthomas2/KDP/COMPLETE-MANUSCRIPT.md"
    temp_file = "/Users/paulmarshall/Documents/GitHub/skylerthomas2/KDP/TEMP-MANUSCRIPT-CLEAN.md"
    output_file = "/Users/paulmarshall/Documents/GitHub/skylerthomas2/KDP/OUT-OF-THE-SWAMP.epub"

    if not os.path.exists(input_file):
        print(f"❌ Error: Input file not found: {input_file}")
        sys.exit(1)

    print("=" * 60)
    print("Creating EPUB from Manuscript")
    print("=" * 60)
    print(f"\nInput: {os.path.basename(input_file)}")
    print(f"Output: {os.path.basename(output_file)}")

    # Clean manuscript first
    print("\n🔄 Cleaning manuscript for EPUB...")
    print("   • Removing metadata blocks")
    print("   • Removing manual Table of Contents (EPUB auto-generates it)")
    print("   • Removing QR code images (links are clickable in EPUB)")
    print("   • Removing 'Listen at:' lines (song titles are already clickable)")
    print("   • Removing LaTeX commands")
    clean_manuscript_for_epub(input_file, temp_file)

    # Pandoc command with metadata
    cmd = [
        "pandoc",
        temp_file,
        "-o", output_file,
        "--metadata", "title=Out of the Swamp: How I Found Truth",
        "--metadata", "subtitle=A Wayfarer's Journey Through Grace",
        "--metadata", "author=Skyler Thomas",
        "--metadata", "publisher=Skyler Thomas Publishing",
        "--metadata", "rights=Copyright © 2025 by Skyler Thomas. All rights reserved.",
        "--metadata", "language=en-US",
        "--metadata", "identifier=979-8-218-83354-1",
        "--toc",
        "--toc-depth=2",
        "--split-level=1",
    ]

    print("🔄 Converting to EPUB format...")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Clean up temp file
        os.remove(temp_file)

        # Check file size
        size_kb = os.path.getsize(output_file) / 1024

        print(f"\n✅ EPUB created successfully!")
        print(f"   File: {output_file}")
        print(f"   Size: {size_kb:.1f} KB")

        print("\n" + "=" * 60)
        print("EPUB READY FOR DISTRIBUTION")
        print("=" * 60)
        print("\n📚 Compatible with:")
        print("   • Amazon Kindle (via KDP)")
        print("   • Apple Books")
        print("   • Google Play Books")
        print("   • Kobo")
        print("   • Nook")
        print("   • Any EPUB reader")

        print("\n✅ Features:")
        print("   • Reflowable text (adapts to screen size)")
        print("   • Table of contents with navigation")
        print("   • All metadata embedded")
        print("   • ISBN included")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error creating EPUB:")
        print(e.stderr)
        if os.path.exists(temp_file):
            os.remove(temp_file)
        sys.exit(1)

if __name__ == "__main__":
    create_epub()
