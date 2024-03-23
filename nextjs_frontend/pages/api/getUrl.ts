import type { NextApiRequest, NextApiResponse } from 'next';
import postgres from 'postgres';

const sql = postgres(process.env.DATABASE_URL || process.env.POSTGRES_URL!, {
  ssl: 'allow',
});

// Function to get a URL by id from the database, with a default id of 1 if no id is provided
export default async function getUrl(req: NextApiRequest, res: NextApiResponse) {
  // Set id to 1 if it's not provided in the query parameters
  const id = req.query.id || 1;

  try {
    // await sql`CREATE TABLE IF NOT EXISTS urls (id SERIAL PRIMARY KEY, url TEXT NOT NULL)`;

    // Query to select a URL by id
    const data = await sql`SELECT * FROM url_table WHERE id = ${id}`;

    if (data.length === 0) {
      res.status(404).json({ error: 'URL not found' });
    } else {
      // console.log('URL:', data);
      res.status(200).json(data[0]); // Assuming we want to return the first record
    }
  } catch (error) {
    console.error('Failed to get the URL:', error);
    res.status(500).json({ error: 'Failed to get the URL' });
  }
}