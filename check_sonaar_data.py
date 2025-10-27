#!/usr/bin/env python3
"""
Check if the Sonaar playlist XML has valid serialized PHP data
"""

import re
from pathlib import Path

SONAAR_FILE = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/SonaarImport.xml')

def extract_tracklist(xml_content):
    """Extract the alb_tracklist serialized data"""
    match = re.search(r'<wp:meta_key><!\[CDATA\[alb_tracklist\]\]></wp:meta_key>\s*<wp:meta_value><!\[CDATA\[(.*?)\]\]></wp:meta_value>', xml_content, re.DOTALL)
    if match:
        return match.group(1)
    return None

def validate_serialized_string_lengths(data):
    """Check if all string length declarations match actual strings"""
    issues = []

    # Find all s:LENGTH:"STRING" patterns
    pattern = r's:(\d+):"([^"]*)"'
    matches = re.finditer(pattern, data)

    for match in matches:
        declared_length = int(match.group(1))
        actual_string = match.group(2)
        actual_length = len(actual_string.encode('utf-8'))

        if declared_length != actual_length:
            issues.append({
                'position': match.start(),
                'declared': declared_length,
                'actual': actual_length,
                'string': actual_string[:100] + ('...' if len(actual_string) > 100 else '')
            })

    return issues

def count_tracks(data):
    """Count the number of tracks in the playlist"""
    # Look for the array declaration a:NUMBER:{
    match = re.search(r'^a:(\d+):\{', data)
    if match:
        declared_count = int(match.group(1))

        # Count actual track entries (i:NUMBER;a:22:{)
        actual_tracks = len(re.findall(r'i:\d+;a:22:\{', data))

        return declared_count, actual_tracks
    return None, None

def main():
    print("Reading SonaarImport.xml...")
    with open(SONAAR_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("\nExtracting playlist data...")
    tracklist = extract_tracklist(content)

    if not tracklist:
        print("ERROR: Could not find alb_tracklist in the XML file!")
        return

    print(f"✓ Found tracklist data ({len(tracklist)} bytes)")

    # Check track count
    declared, actual = count_tracks(tracklist)
    print(f"\nTrack count:")
    print(f"  Declared: {declared}")
    print(f"  Actual:   {actual}")

    if declared != actual:
        print(f"  ⚠️  MISMATCH! Declared {declared} but found {actual} tracks")
    else:
        print(f"  ✓ Count matches")

    # Validate string lengths
    print("\nValidating PHP serialized string lengths...")
    issues = validate_serialized_string_lengths(tracklist)

    if issues:
        print(f"⚠️  Found {len(issues)} string length mismatches:")
        for i, issue in enumerate(issues[:10], 1):  # Show first 10
            print(f"\n  Issue #{i}:")
            print(f"    Position: {issue['position']}")
            print(f"    Declared: {issue['declared']} bytes")
            print(f"    Actual:   {issue['actual']} bytes")
            print(f"    String:   {issue['string']}")

        if len(issues) > 10:
            print(f"\n  ... and {len(issues) - 10} more issues")
    else:
        print("✓ All string lengths are valid")

    # Check for specific issues
    print("\nChecking for common issues...")

    # Check if there's a Dig-a-Little-Deeper track
    if 'Dig-a-Little-Deeper' in tracklist:
        print("✓ Found Dig-a-Little-Deeper track")
    else:
        print("⚠️  No Dig-a-Little-Deeper track found")

    # Check for p=600
    p600_count = len(re.findall(r'\?p=600', tracklist))
    print(f"  Tracks pointing to p=600: {p600_count}")

    # Check for p=2284
    p2284_count = len(re.findall(r'\?p=2284', tracklist))
    print(f"  Tracks pointing to p=2284: {p2284_count}")

    print("\n" + "="*60)
    if issues:
        print("RESULT: Issues found - the serialized data may be corrupted")
        print("This could prevent WordPress from parsing the playlist correctly")
    else:
        print("RESULT: No issues detected with the serialized data")
        print("The problem may be elsewhere (import settings, plugin version, etc.)")

if __name__ == '__main__':
    main()
