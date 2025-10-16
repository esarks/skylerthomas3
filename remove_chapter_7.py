#!/usr/bin/env python3
"""
Remove Chapter 7 (I Will Serve) and renumber subsequent chapters
"""

from pathlib import Path
import shutil

WIKI_DIR = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki')
ARCHIVE_DIR = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/archived_chapters')

# Create archive directory
ARCHIVE_DIR.mkdir(exist_ok=True)

# Chapter 7 file to remove
CHAPTER_7_FILE = 'BeyondTheSwamp_08_Chapter-I-Will-Serve.md'

def archive_chapter_7():
    """Archive Chapter 7 file"""

    source = WIKI_DIR / CHAPTER_7_FILE
    destination = ARCHIVE_DIR / CHAPTER_7_FILE

    if source.exists():
        shutil.move(str(source), str(destination))
        print(f"✓ Archived: {CHAPTER_7_FILE}")
        print(f"  Location: {destination}")
        return True
    else:
        print(f"⚠️  File not found: {CHAPTER_7_FILE}")
        return False

def update_comprehensive_file():
    """Remove Chapter 7 from comprehensive file and renumber chapters 8-18"""

    filepath = WIKI_DIR / 'BeyondTheSwamp_Complete_Movements_3-5.md'

    if not filepath.exists():
        print(f"⚠️  Comprehensive file not found")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The comprehensive file has chapters 9-18
    # After removing chapter 7, these become chapters 8-17

    # Renumber chapters in the comprehensive file
    # Chapter 9 → Chapter 8
    # Chapter 10 → Chapter 9
    # Chapter 11 → Chapter 10
    # Chapter 12 → Chapter 11
    # Chapter 13 → Chapter 12
    # Chapter 14 → Chapter 13
    # Chapter 15 → Chapter 14
    # Chapter 16 → Chapter 15
    # Chapter 17 → Chapter 16
    # Chapter 18 → Chapter 17

    replacements = [
        ('# CHAPTER 9:', '# CHAPTER 8:'),
        ('# CHAPTER 10:', '# CHAPTER 9:'),
        ('# CHAPTER 11:', '# CHAPTER 10:'),
        ('# CHAPTER 12:', '# CHAPTER 11:'),
        ('# CHAPTER 13:', '# CHAPTER 12:'),
        ('# CHAPTER 14:', '# CHAPTER 13:'),
        ('# CHAPTER 15:', '# CHAPTER 14:'),
        ('# CHAPTER 16:', '# CHAPTER 15:'),
        ('# CHAPTER 17:', '# CHAPTER 16:'),
        ('# CHAPTER 18:', '# CHAPTER 17:'),
        ('Chapter 9:', 'Chapter 8:'),
        ('Chapter 10:', 'Chapter 9:'),
        ('Chapter 11:', 'Chapter 10:'),
        ('Chapter 12:', 'Chapter 11:'),
        ('Chapter 13:', 'Chapter 12:'),
        ('Chapter 14:', 'Chapter 13:'),
        ('Chapter 15:', 'Chapter 14:'),
        ('Chapter 16:', 'Chapter 15:'),
        ('Chapter 17:', 'Chapter 16:'),
        ('Chapter 18:', 'Chapter 17:'),
    ]

    for old, new in replacements:
        content = content.replace(old, new)

    # Update total chapter count
    content = content.replace('18 chapters', '17 chapters')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated comprehensive file with renumbered chapters")
    return True

def update_individual_chapters():
    """Update chapter headings in individual chapter files"""

    # Files to update (chapters 8 becomes 7)
    chapter_updates = [
        ('BeyondTheSwamp_09_Chapter-No-Good-Deed.md', 'Chapter 8:', 'Chapter 7:'),
    ]

    for filename, old_text, new_text in chapter_updates:
        filepath = WIKI_DIR / filename
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            content = content.replace(old_text, new_text)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✓ Updated: {filename}")

def main():
    print("Removing Chapter 7 (I Will Serve)...")
    print("This chapter is already in the current book")
    print("=" * 70)

    # Archive Chapter 7
    if archive_chapter_7():
        print(f"\n✓ Chapter 7 archived successfully")

    # Update comprehensive file with renumbered chapters
    update_comprehensive_file()

    # Update individual chapter files
    update_individual_chapters()

    print("=" * 70)
    print("\n✅ Chapter 7 removed and subsequent chapters renumbered")
    print("\nNew chapter structure:")
    print("  Chapters 1-6: Unchanged")
    print("  Chapter 7: No Good Deed (was Chapter 8)")
    print("  Chapters 8-17: Renumbered from 9-18")
    print("\nTotal chapters: 17 (was 18)")

if __name__ == '__main__':
    main()
