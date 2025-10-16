#!/usr/bin/env python3
"""
Generate QR codes for Beyond the Swamp song URLs
Creates 290x290 pixel QR codes with high error correction
"""

import qrcode
import os
from pathlib import Path

# Output directory for QR codes
QR_OUTPUT_DIR = Path('/Users/paulmarshall/Documents/GitHub/skylerthomas3/qr-codes')

# Chapter to URL mapping (ALL 18 shortened URLs)
SONG_URLS = {
    1: {
        'url': 'https://go.skylerthomas.com/vTcEr9',
        'title': 'Named By God',
        'filename': 'qr-bts01-named-by-god.png'
    },
    2: {
        'url': 'https://go.skylerthomas.com/ZazW6B',
        'title': 'In His Image',
        'filename': 'qr-bts02-in-his-image.png'
    },
    3: {
        'url': 'https://go.skylerthomas.com/wjfV2i',
        'title': 'You Still Know My Name',
        'filename': 'qr-bts03-you-still-know-my-name.png'
    },
    4: {
        'url': 'https://go.skylerthomas.com/f1s0eM',
        'title': 'Why Didn\'t You Tell Me',
        'filename': 'qr-bts04-why-didnt-you-tell-me.png'
    },
    5: {
        'url': 'https://go.skylerthomas.com/1zoXHD',
        'title': 'Fruit of His Spirit',
        'filename': 'qr-bts05-fruit-of-his-spirit.png'
    },
    6: {
        'url': 'https://go.skylerthomas.com/LQcPBi',
        'title': 'The Rhythm of Life',
        'filename': 'qr-bts06-rhythm-of-life.png'
    },
    7: {
        'url': 'https://go.skylerthomas.com/13Xedv',
        'title': 'I Will Serve',
        'filename': 'qr-bts07-i-will-serve.png'
    },
    8: {
        'url': 'https://go.skylerthomas.com/oG6qwS',
        'title': 'No Good Deed',
        'filename': 'qr-bts08-no-good-deed.png'
    },
    9: {
        'url': 'https://go.skylerthomas.com/DsW60X',
        'title': 'I Will Serve',
        'filename': 'qr-bts09-i-will-serve.png'
    },
    10: {
        'url': 'https://go.skylerthomas.com/rgYmdb',
        'title': 'What is Prayer?',
        'filename': 'qr-bts10-what-is-prayer.png'
    },
    11: {
        'url': 'https://go.skylerthomas.com/TmvEwb',
        'title': 'One Note',
        'filename': 'qr-bts11-one-note.png'
    },
    12: {
        'url': 'https://go.skylerthomas.com/RENVkp',
        'title': 'What Will You Say',
        'filename': 'qr-bts12-what-will-you-say.png'
    },
    13: {
        'url': 'https://go.skylerthomas.com/Q7HEmZ',
        'title': 'Slip and Slide',
        'filename': 'qr-bts13-slip-and-slide.png'
    },
    14: {
        'url': 'https://go.skylerthomas.com/FXQXve',
        'title': 'The Heart of Glass',
        'filename': 'qr-bts14-heart-of-glass.png'
    },
    15: {
        'url': 'https://go.skylerthomas.com/XpS8to',
        'title': 'Heart of Glass',
        'filename': 'qr-bts15-heart-of-glass.png'
    },
    16: {
        'url': 'https://go.skylerthomas.com/LizlRn',
        'title': 'The Battle Is Won',
        'filename': 'qr-bts16-battle-is-won.png'
    },
    17: {
        'url': 'https://go.skylerthomas.com/uwCkHB',
        'title': 'What\'s Heaven Like?',
        'filename': 'qr-bts17-whats-heaven-like.png'
    },
    18: {
        'url': 'https://go.skylerthomas.com/EcOXbS',
        'title': 'The Rose',
        'filename': 'qr-bts18-the-rose.png'
    }
}

def generate_qr_code(url, output_path):
    """
    Generate a QR code for the given URL

    Args:
        url: The URL to encode
        output_path: Path to save the QR code image
    """
    qr = qrcode.QRCode(
        version=1,  # Auto-adjust size
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction (30%)
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    # Create image
    img = qr.make_image(fill_color="black", back_color="white")

    # Resize to 290x290 to match Book 1 format
    img = img.resize((290, 290))

    # Save the image
    img.save(output_path)
    print(f"✓ Generated: {output_path.name}")

def main():
    """Generate all QR codes"""
    # Create output directory if it doesn't exist
    QR_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Generating QR codes for Beyond the Swamp...")
    print(f"Output directory: {QR_OUTPUT_DIR}")
    print("=" * 60)

    # Generate QR codes for all songs
    for chapter_num, song_data in sorted(SONG_URLS.items()):
        output_path = QR_OUTPUT_DIR / song_data['filename']
        print(f"Chapter {chapter_num:2d}: {song_data['title']}")
        generate_qr_code(song_data['url'], output_path)

    print("=" * 60)
    print(f"✓ Successfully generated {len(SONG_URLS)} QR codes")
    print(f"\n🎉 All 18 chapters now have QR codes!")

if __name__ == '__main__':
    main()
