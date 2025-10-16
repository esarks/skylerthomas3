#!/usr/bin/env python3
"""
WORKFLOW3 - PUBLISHER VERSION Production Pipeline

This script runs the complete WORKFLOW3 production pipeline for the
REVISED publisher-ready version of "Out of the Swamp".

Steps:
1. Create complete manuscript from revised chapters
2. Generate KDP-ready PDF with embedded fonts
3. Generate EPUB for distribution

Source files: /skylerthomas3.wiki/REVISED-*.md
Output: /skylerthomas3/KDP/

TRIGGER COMMAND: "Execute workflow3"
"""

import os
import sys
import subprocess

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("\n" + "="*70)
    print("WORKFLOW3 - PUBLISHER VERSION PRODUCTION PIPELINE")
    print("="*70)
    print("\nThis workflow produces the REVISED publisher-ready version")
    print("Source: skylerthomas3.wiki/REVISED-*.md")
    print("Output: skylerthomas3/KDP/")
    print("\n" + "="*70)

    # Step 1: Create manuscript
    print("\n[1/3] Creating complete manuscript from revised chapters...")
    result = subprocess.run([sys.executable, os.path.join(script_dir, "create_complete_manuscript.py")])
    if result.returncode != 0:
        print("\n❌ Error creating manuscript")
        print("Note: Some files may not be revised yet. Check output above.")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

    # Step 2: Create PDF
    print("\n[2/3] Creating KDP-ready PDF...")
    result = subprocess.run([sys.executable, os.path.join(script_dir, "create_pdf_kdp_ready.py")])
    if result.returncode != 0:
        print("\n❌ Error creating PDF")
        print("Check manuscript file and try again.")
        sys.exit(1)

    # Step 3: Create EPUB
    print("\n[3/3] Creating EPUB...")
    result = subprocess.run([sys.executable, os.path.join(script_dir, "create_epub.py")])
    if result.returncode != 0:
        print("\n❌ Error creating EPUB")
        print("Check manuscript file and pandoc installation.")
        sys.exit(1)

    print("\n" + "="*70)
    print("✅ WORKFLOW3 COMPLETE - PUBLISHER VERSION")
    print("="*70)
    print("\nAll files generated in: skylerthomas3/KDP/")
    print("  • COMPLETE-MANUSCRIPT.md")
    print("  • OUT-OF-THE-SWAMP-PUBLISHER.pdf")
    print("  • OUT-OF-THE-SWAMP-PUBLISHER.epub")
    print("\n" + "="*70)
    print("\nIMPORTANT: This is the REVISED publisher-ready version")
    print("For the original 14-chapter version, use WORKFLOW2")
    print("="*70)

if __name__ == "__main__":
    main()
