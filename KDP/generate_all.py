#!/usr/bin/env python3
"""
Master script to generate all document formats
Runs: assemble -> PDF -> EPUB
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ASSEMBLE_SCRIPT = SCRIPT_DIR / "assemble_manuscript.py"
PDF_SCRIPT = SCRIPT_DIR / "create_pdf_kdp_ready.py"
EPUB_SCRIPT = SCRIPT_DIR / "create_epub.py"
MANUSCRIPT_FILE = SCRIPT_DIR / "complete_manuscript.md"
PDF_OUTPUT = SCRIPT_DIR / "out_of_the_swamp.pdf"
EPUB_OUTPUT = SCRIPT_DIR / "out_of_the_swamp.epub"

def run_script(script_path, description):
    """Run a Python script and handle errors"""
    print("\n" + "="*70)
    print(f"RUNNING: {description}")
    print("="*70)

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.returncode != 0:
            print(f"\n❌ ERROR in {description}")
            print(result.stderr)
            return False

        print(f"✓ {description} completed successfully")
        return True

    except Exception as e:
        print(f"\n❌ EXCEPTION in {description}: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("OUT OF THE SWAMP - DOCUMENT GENERATION")
    print("Publisher's Review Edition")
    print("="*70)

    # Step 1: Assemble manuscript
    if not run_script(ASSEMBLE_SCRIPT, "Manuscript Assembly"):
        print("\n❌ Failed to assemble manuscript. Stopping.")
        return False

    if not MANUSCRIPT_FILE.exists():
        print(f"\n❌ Manuscript file not found: {MANUSCRIPT_FILE}")
        return False

    # Step 2: Generate PDF
    print("\n" + "-"*70)
    print("Generating PDF...")
    print("-"*70)
    if not run_script(PDF_SCRIPT, "PDF Generation"):
        print("\n⚠️  PDF generation failed, but continuing...")
    elif PDF_OUTPUT.exists():
        size_mb = PDF_OUTPUT.stat().st_size / (1024*1024)
        print(f"\n✓ PDF created: {PDF_OUTPUT}")
        print(f"  Size: {size_mb:.2f} MB")

    # Step 3: Generate EPUB
    print("\n" + "-"*70)
    print("Generating EPUB...")
    print("-"*70)
    if not run_script(EPUB_SCRIPT, "EPUB Generation"):
        print("\n⚠️  EPUB generation failed, but continuing...")
    elif EPUB_OUTPUT.exists():
        size_kb = EPUB_OUTPUT.stat().st_size / 1024
        print(f"\n✓ EPUB created: {EPUB_OUTPUT}")
        print(f"  Size: {size_kb:.2f} KB")

    # Summary
    print("\n" + "="*70)
    print("GENERATION COMPLETE")
    print("="*70)

    files_created = []
    if MANUSCRIPT_FILE.exists():
        files_created.append(f"✓ {MANUSCRIPT_FILE.name}")
    if PDF_OUTPUT.exists():
        files_created.append(f"✓ {PDF_OUTPUT.name}")
    if EPUB_OUTPUT.exists():
        files_created.append(f"✓ {EPUB_OUTPUT.name}")

    if files_created:
        print("\nFiles created:")
        for f in files_created:
            print(f"  {f}")
    else:
        print("\n⚠️  No files were created")

    print(f"\nOutput directory: {SCRIPT_DIR}")
    print("\n" + "="*70 + "\n")

    return len(files_created) > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
