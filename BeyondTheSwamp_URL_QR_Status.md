# Beyond the Swamp: URL & QR Code Status

**Last Updated:** October 14, 2025

## Complete (10 chapters)

| Ch | Song Title | Shortened URL | QR Code | Lyrics |
|----|-----------|---------------|---------|--------|
| 2 | In His Image | ✅ https://go.skylerthomas.com/ZazW6B | ✅ qr-bts02-in-his-image.png | ✅ |
| 3 | You Still Know My Name | ✅ https://go.skylerthomas.com/wjfV2i | ✅ qr-bts03-you-still-know-my-name.png | ✅ |
| 4 | Why Didn't You Tell Me | ✅ https://go.skylerthomas.com/f1s0eM | ✅ qr-bts04-why-didnt-you-tell-me.png | ✅ |
| 5 | Fruit of His Spirit | ✅ https://go.skylerthomas.com/1zoXHD | ✅ qr-bts05-fruit-of-his-spirit.png | ⚠️ Needs manual population |
| 9 | I Will Serve | ✅ https://go.skylerthomas.com/DsW60X | ✅ qr-bts09-i-will-serve.png | ✅ |
| 11 | One Note | ✅ https://go.skylerthomas.com/TmvEwb | ✅ qr-bts11-one-note.png | ⚠️ Needs manual population |
| 12 | What Will You Say | ✅ https://go.skylerthomas.com/RENVkp | ✅ qr-bts12-what-will-you-say.png | ⚠️ Needs manual population |
| 13 | Slip and Slide | ✅ https://go.skylerthomas.com/Q7HEmZ | ✅ qr-bts13-slip-and-slide.png | ⚠️ Needs manual population |
| 15 | Heart of Glass | ✅ https://go.skylerthomas.com/XpS8to | ✅ qr-bts15-heart-of-glass.png | ⚠️ Needs manual population |
| 18 | The Rose | ✅ https://go.skylerthomas.com/EcOXbS | ✅ qr-bts18-the-rose.png | ⚠️ Needs manual population |

## Missing URLs (8 chapters)

| Ch | Song Title | Shortened URL | QR Code | Lyrics |
|----|-----------|---------------|---------|--------|
| 1 | Named By God | ❌ Missing | ❌ Pending | ✅ |
| 6 | The Rhythm of Life | ❌ Missing | ❌ Pending | ⚠️ Needs manual population |
| 7 | Rhythm of Life (alt) | ❌ Missing | ❌ Pending | ❌ Not in export |
| 8 | No Good Deed | ❌ Missing | ❌ Pending | ✅ |
| 10 | One Note (duplicate?) | ❌ Missing | ❌ Pending | See Ch 11 |
| 14 | The Heart of Glass | ❌ Missing | ❌ Pending | See Ch 15 |
| 16 | The Battle Is Won | ❌ Missing | ❌ Pending | ⚠️ Needs manual population |
| 17 | What's Heaven Like? | ❌ Missing | ❌ Pending | ⚠️ Needs manual population |

## QR Code Details

- **Format:** PNG, 290x290 pixels
- **Error Correction:** High (30%)
- **Location:** `/Users/paulmarshall/Documents/GitHub/skylerthomas3/qr-codes/`
- **Naming Convention:** `qr-bts##-song-name.png`

## Next Steps

1. **Find/Create Missing Song URLs:**
   - Check WordPress for existing song pages for chapters 1, 6, 7, 8, 10, 14, 16, 17
   - Create new shortened URLs using `create-short-links.js`
   - Update `generate_qr_codes.py` SONG_URLS dictionary
   - Re-run script to generate remaining 8 QR codes

2. **Populate Missing Lyrics:**
   - Manually add lyrics for chapters: 5, 6, 7, 11, 12, 13, 15, 16, 17, 18
   - Use chapter outline placeholders to locate insertion points
   - Maintain consistent formatting (Verse/Chorus/Bridge labels)

3. **Verify Chapter Outline Files:**
   - Check that all 18 chapters have proper structure
   - Ensure song URLs are updated in chapter files
   - Verify QR code references are correct

## Scripts Available

- `create-short-links.js` - Generate shortened URLs using Short.io API
- `generate_qr_codes.py` - Generate QR code images from URLs
- `extract_lyrics_from_export.py` - Extract lyrics from WordPress export
- `populate_chapters_with_lyrics.py` - Auto-populate lyrics into chapter files
