require('dotenv').config();
const axios = require('axios');
const fs = require('fs');

const API_KEY = process.env.SHORT_IO_API_KEY;
const SHORT_IO_API = 'https://api.short.io/links';

// URLs that still need to be shortened (extracted from WordPress export)
const urlsToShorten = [
  {
    chapter: 1,
    title: 'Named By God',
    originalUrl: 'https://www.skylerthomas.com/named-by-god/'
  },
  {
    chapter: 8,
    title: 'No Good Deed',
    originalUrl: 'https://www.skylerthomas.com/no-good-deed/'
  },
  {
    chapter: 14,
    title: 'The Heart of Glass',
    originalUrl: 'https://www.skylerthomas.com/75/'
  },
  {
    chapter: 16,
    title: 'The Battle Is Won',
    originalUrl: 'https://www.skylerthomas.com/the-battle-is-won/'
  },
  {
    chapter: 17,
    title: "What's Heaven Like?",
    originalUrl: 'https://www.skylerthomas.com/whats-heaven-like-devotional/'
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
  console.log('Creating shortened URLs for missing chapters...');
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
    'new-short-links.json',
    JSON.stringify(results, null, 2)
  );

  // Also create a formatted text output
  let output = 'New Shortened URLs\n';
  output += '='.repeat(70) + '\n\n';

  results.forEach(result => {
    output += `Chapter ${result.chapter}: ${result.title}\n`;
    output += `Short URL: ${result.shortUrl}\n`;
    output += `Original:  ${result.originalUrl}\n\n`;
  });

  fs.writeFileSync('new-short-links.txt', output);

  console.log('\n✓ Results saved to:');
  console.log('  - new-short-links.json');
  console.log('  - new-short-links.txt');
}

main();
