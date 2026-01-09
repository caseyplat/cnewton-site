exports.handler = async (event) => {
  const LASTFM_API_KEY = process.env.LASTFM_API_KEY;
  const LASTFM_USER = 'caseyswan';

  if (!LASTFM_API_KEY) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'API key not configured' }),
    };
  }

  const url = `https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=${LASTFM_USER}&api_key=${LASTFM_API_KEY}&limit=1&format=json`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=30',
      },
      body: JSON.stringify(data),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to fetch Last.fm data' }),
    };
  }
};
