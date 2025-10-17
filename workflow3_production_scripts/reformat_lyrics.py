#!/usr/bin/env python3
"""
Reformat song lyrics from multi-line format to continuous paragraph format
Converts from:
    **[Verse 1]**
    Line 1
    Line 2

To:
    [Verse 1] Line 1 Line 2 [Chorus] Line 3 Line 4
"""

import re
import os

def reformat_lyrics_section(text):
    """Convert lyrics from multi-line format to paragraph format"""
    lines = text.split('\n')
    result = []
    current_section = []

    for line in lines:
        line = line.strip()

        # Check if line is a section marker like **[Verse 1]** or **[Chorus]**
        marker_match = re.match(r'\*\*\[(.*?)\]\*\*', line)

        if marker_match:
            # If we have accumulated lines, join them
            if current_section:
                result.append(' '.join(current_section))
                current_section = []
            # Add the marker WITH bold formatting
            result.append(f"**[{marker_match.group(1)}]**")
        elif line and not line.startswith('##'):
            # Add lyric line to current section
            current_section.append(line)

    # Add final section
    if current_section:
        result.append(' '.join(current_section))

    # Join everything into one paragraph with space between markers and lyrics
    return ' '.join(result)

def process_chapter_file(filepath):
    """Process a single chapter file"""
    print(f"Processing: {os.path.basename(filepath)}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find lyrics sections (various heading formats)
    pattern = r'(## (?:Song )?Lyrics:? [^\n]+\n\n)(.*?)(\n\n---|\n\n##|\Z)'

    def replace_lyrics(match):
        heading = match.group(1)
        lyrics = match.group(2)
        ending = match.group(3)

        # Reformat the lyrics
        reformatted = reformat_lyrics_section(lyrics)

        # Return heading + reformatted lyrics + ending
        return heading + reformatted + '\n' + ending

    # Apply the replacement
    new_content = re.sub(pattern, replace_lyrics, content, flags=re.DOTALL)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  ✓ Reformatted lyrics in {os.path.basename(filepath)}")

def main():
    # Path to wiki files
    wiki_path = "/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki"

    # Get all chapter files
    chapter_files = []
    for filename in os.listdir(wiki_path):
        if filename.startswith('REVISED-') and 'chapter' in filename and filename.endswith('.md'):
            chapter_files.append(os.path.join(wiki_path, filename))

    chapter_files.sort()

    print(f"\nFound {len(chapter_files)} chapter files")
    print("="*60)

    for filepath in chapter_files:
        process_chapter_file(filepath)

    print("="*60)
    print(f"✓ Completed! Reformatted lyrics in {len(chapter_files)} files")
    print("\nRun workflow3 to regenerate the PDF and EPUB")

if __name__ == '__main__':
    main()
