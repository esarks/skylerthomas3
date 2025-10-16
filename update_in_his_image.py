#!/usr/bin/env python3
"""
Update In His Image chapter with new MP3 URL and regenerate QR code
"""

import qrcode
from pathlib import Path

# New URL
NEW_SHORT_URL = 'https://go.skylerthomas.com/0XcUMN'
OLD_SHORT_URL = 'https://go.skylerthomas.com/ZazW6B'

# Paths
WIKI_DIR = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3.wiki')
QR_DIR = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/qr-codes')
CHAPTER_FILE = 'BeyondTheSwamp_02_Chapter-In-His-Image.md'
QR_FILE = 'qr-bts02-in-his-image.png'

def regenerate_qr_code():
    """Generate new QR code with updated URL"""

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(NEW_SHORT_URL)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((290, 290))

    output_path = QR_DIR / QR_FILE
    img.save(output_path)
    print(f"✓ Regenerated QR code: {QR_FILE}")

def update_chapter_file():
    """Update chapter file with new URL"""

    filepath = WIKI_DIR / CHAPTER_FILE

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace old URL with new URL
    content = content.replace(OLD_SHORT_URL, NEW_SHORT_URL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated chapter file: {CHAPTER_FILE}")

def main():
    print("Updating In His Image with MP3 direct link...")
    print("=" * 70)
    print(f"Old URL: {OLD_SHORT_URL}")
    print(f"New URL: {NEW_SHORT_URL}")
    print("=" * 70)

    regenerate_qr_code()
    update_chapter_file()

    print("=" * 70)
    print("✅ In His Image updated successfully!")
    print(f"\nNew URL points to MP3 file:")
    print("https://www.skylerthomas.com/wp-content/uploads/2017/08/In-His-Image-Duet-Vocal-4-5.mp3")

if __name__ == '__main__':
    main()
