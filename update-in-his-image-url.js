require('dotenv').config();
const axios = require('axios');

const API_KEY = process.env.SHORT_IO_API_KEY;
const SHORT_IO_API = 'https://api.short.io/links';

// New MP3 URL for In His Image
const originalUrl = 'https://www.skylerthomas.com/wp-content/uploads/2017/08/In-His-Image-Duet-Vocal-4-5.mp3';
const title = 'In His Image - Duet Vocal';

async function createShortLink() {
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

    console.log('='.repeat(70));
    console.log('Chapter 2: In His Image - MP3 Direct Link');
    console.log('Original URL:', originalUrl);
    console.log('Short URL:', response.data.shortURL);
    console.log('='.repeat(70));

    return response.data.shortURL;
  } catch (error) {
    console.error('Error creating short link:', error.response?.data || error.message);
    return null;
  }
}

createShortLink();
