exports.handler = async (event) => {
  const CHANNEL_ID = 'UCZcR2SVWaGWNlMqPxvQS3vw';
  const RSS_URL = `https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL_ID}`;

  try {
    const response = await fetch(RSS_URL);
    const xml = await response.text();

    // Parse YouTube Atom feed
    const items = [];
    const entryMatches = xml.match(/<entry>([\s\S]*?)<\/entry>/g) || [];

    for (const entryXml of entryMatches.slice(0, 5)) {
      const title = (entryXml.match(/<title>(.*?)<\/title>/) || [])[1] || '';
      const videoId = (entryXml.match(/<yt:videoId>(.*?)<\/yt:videoId>/) || [])[1] || '';
      const published = (entryXml.match(/<published>(.*?)<\/published>/) || [])[1] || '';

      if (title && videoId) {
        items.push({
          title: decodeHTMLEntities(title),
          link: `https://www.youtube.com/watch?v=${videoId}`,
          pubDate: published,
        });
      }
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=300', // Cache for 5 minutes
      },
      body: JSON.stringify({ status: 'ok', items }),
    };
  } catch (error) {
    console.error('Error fetching Hard Fork RSS:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ status: 'error', error: 'Failed to fetch RSS feed' }),
    };
  }
};

function decodeHTMLEntities(text) {
  return text
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'")
    .replace(/&#x2F;/g, '/');
}
