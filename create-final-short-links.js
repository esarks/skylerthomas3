require('dotenv').config();
const axios = require('axios');
const fs = require('fs');

const API_KEY = process.env.SHORT_IO_API_KEY;
const SHORT_IO_API = 'https://api.short.io/links';

// Final 3 URLs that need to be shortened
const urlsToShorten = [
  {
    chapter: 6,
    title: 'The Rhythm of Life',
    originalUrl: 'https://www.skylerthomas.com/unforced-rhythms-of-grace/'
  },
  {
    chapter: 7,
    title: 'I Will Serve',
    originalUrl: 'https://www.skylerthomas.com/redemptions-story-a-song/i-will-serve-v4/'
  },
  {
    chapter: 10,
    title: 'What is Prayer?',
    originalUrl: 'https://www.skylerthomas.com/what-is-prayer/'
  }
];

async function createShortLink(originalUrl, title) {
  try {
    const response = await axios.post(
      SHORT_IO_API,
      {
        originalURL: originalUrl,
        domain: 'go.skylerthomas.com',
        title: title
      },
      {
        headers: {
          'Authorization': API_KEY,
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data.shortURL;
  } catch (error) {
    console.error(`Error creating short link for ${title}:`, error.response?.data || error.message);
    return null;
  }
}

async function main() {
  console.log('Creating shortened URLs for final missing chapters...');
  console.log('='.repeat(70));

  const results = [];

  for (const song of urlsToShorten) {
    console.log(`\nChapter ${song.chapter}: ${song.title}`);
    console.log(`Original: ${song.originalUrl}`);

    const shortUrl = await createShortLink(song.originalUrl, song.title);

    if (shortUrl) {
      console.log(`Short URL: ${shortUrl}`);
      results.push({
        chapter: song.chapter,
        title: song.title,
        originalUrl: song.originalUrl,
        shortUrl: shortUrl
      });
    }

    // Add delay to avoid rate limiting
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  console.log('\n' + '='.repeat(70));
  console.log(`✓ Created ${results.length} shortened URLs`);

  // Save results
  fs.writeFileSync(
    'final-short-links.json',
    JSON.stringify(results, null, 2)
  );

  // Also create a formatted text output
  let output = 'Final Shortened URLs (Chapters 6, 7, 10)\n';
  output += '='.repeat(70) + '\n\n';

  results.forEach(result => {
    output += `Chapter ${result.chapter}: ${result.title}\n`;
    output += `Short URL: ${result.shortUrl}\n`;
    output += `Original:  ${result.originalUrl}\n\n`;
  });

  fs.writeFileSync('final-short-links.txt', output);

  console.log('\n✓ Results saved to:');
  console.log('  - final-short-links.json');
  console.log('  - final-short-links.txt');
}

main();
