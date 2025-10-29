#!/usr/bin/env python3
"""
WORKFLOW3: Complete Publisher Edition Build Script

This script runs the complete workflow to build the publisher edition:
1. Assembles complete manuscript from REVISED chapters
2. Generates KDP-ready PDF with embedded fonts
3. Generates EPUB for digital distribution

Usage:
    python3 Workflow3.py

    or make it executable:
    chmod +x Workflow3.py
    ./Workflow3.py
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and report results"""
    print(f"\n{'='*70}")
    print(f"WORKFLOW3: {description}")
    print('='*70)

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            check=True,
            capture_output=False
        )
        print(f"\n✅ {description} - COMPLETE")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FAILED")
        print(f"Error: {e}")
        return False

def main():
    """Run complete Workflow3 build process"""

    print("\n" + "="*70)
    print("WORKFLOW3: PUBLISHER EDITION BUILD")
    print("="*70)
    print("\nThis will:")
    print("  1. Assemble manuscript from REVISED chapters")
    print("  2. Generate KDP-ready PDF")
    print("  3. Generate EPUB for distribution")
    print("\n" + "="*70)

    # Step 1: Assemble manuscript
    if not run_script('create_complete_manuscript.py', 'Step 1: Assemble Manuscript'):
        print("\n❌ Build failed at manuscript assembly")
        sys.exit(1)

    # Step 2: Generate PDF
    if not run_script('create_pdf_kdp_ready.py', 'Step 2: Generate PDF'):
        print("\n❌ Build failed at PDF generation")
        sys.exit(1)

    # Step 3: Generate EPUB
    if not run_script('create_epub.py', 'Step 3: Generate EPUB'):
        print("\n❌ Build failed at EPUB generation")
        sys.exit(1)

    # Success!
    print("\n" + "="*70)
    print("✅ WORKFLOW3 BUILD COMPLETE")
    print("="*70)
    print("\nGenerated files:")
    print("  • COMPLETE-MANUSCRIPT.md")
    print("  • OUT-OF-THE-SWAMP-PUBLISHER.pdf")
    print("  • OUT-OF-THE-SWAMP-PUBLISHER.epub")
    print("\nAll files ready for publisher review and KDP submission!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
