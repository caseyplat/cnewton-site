exports.handler = async (event) => {
  const RSS_URL = 'https://www.platformer.news/rss/';

  try {
    const response = await fetch(RSS_URL);
    const xml = await response.text();

    // Simple XML parsing for RSS feed
    const items = [];
    const itemMatches = xml.match(/<item>([\s\S]*?)<\/item>/g) || [];

    for (const itemXml of itemMatches.slice(0, 5)) {
      const title = (itemXml.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>/) ||
                     itemXml.match(/<title>(.*?)<\/title>/) || [])[1] || '';
      const link = (itemXml.match(/<link>(.*?)<\/link>/) || [])[1] || '';
      const pubDate = (itemXml.match(/<pubDate>(.*?)<\/pubDate>/) || [])[1] || '';

      if (title && link) {
        items.push({ title: decodeHTMLEntities(title), link, pubDate });
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
    console.error('Error fetching Platformer RSS:', error);
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
