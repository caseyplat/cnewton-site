exports.handler = async (event) => {
  const RSS_URL = 'https://feeds.simplecast.com/l2i9YnTd';

  try {
    const response = await fetch(RSS_URL);
    const xml = await response.text();

    // Parse podcast RSS feed
    const items = [];
    const itemMatches = xml.match(/<item>([\s\S]*?)<\/item>/g) || [];

    for (const itemXml of itemMatches.slice(0, 5)) {
      const title = (itemXml.match(/<title><!\[CDATA\[(.*?)\]\]><\/title>/) ||
                     itemXml.match(/<title>(.*?)<\/title>/) || [])[1] || '';
      const link = (itemXml.match(/<link>(.*?)<\/link>/) || [])[1] || '';
      const pubDate = (itemXml.match(/<pubDate>(.*?)<\/pubDate>/) || [])[1] || '';

      if (title) {
        items.push({
          title: decodeHTMLEntities(title),
          link: link || 'https://www.nytimes.com/column/hard-fork',
          pubDate,
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
    console.error('Error fetching Hard Fork podcast RSS:', error);
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
