/**
 * Cloudflare Worker for the Citation Tracker (Read-Only)
 *
 * - Handles GET requests to serve citation data from KV.
 * - Serves the index.html file for all other paths.
 *
 * Data is now written directly by the GitHub Action using wrangler.
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // API route for fetching data
    if (url.pathname === '/api/citations') {
      if (request.method === 'GET') {
        return this.handleGet(env);
      }
      // Handle CORS pre-flight requests for the GET endpoint
      if (request.method === 'OPTIONS') {
        return this.handleOptions();
      }
      return new Response('Method Not Allowed', { status: 405 });
    }

    // For any other path, serve the static index.html file from assets
    try {
      return await env.ASSETS.fetch(request);
    } catch (e) {
      // If the asset is not found, serve index.html as a fallback for SPA routing
      // This ensures that refreshing on a path like /some/page still loads the app
      const notFoundResponse = await env.ASSETS.fetch(new Request(new URL('/index.html', request.url)));
      return new Response(notFoundResponse.body, {
          ...notFoundResponse,
          status: 200,
      });
    }
  },

  /**
   * Handles GET requests to retrieve the citation data.
   */
  async handleGet(env) {
    // Retrieve the data string from the KV namespace.
    const data = await env.CITATIONS_KV.get('citations_data', { type: 'text' });

    if (data === null) {
      return new Response(JSON.stringify({ error: 'No citation data found. Run the update action.' }), {
        status: 404,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }

    // Return the stored data with the correct content type.
    return new Response(data, {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*', // Allow cross-origin requests
      },
    });
  },

  /**
   * Handles CORS pre-flight OPTIONS requests.
   */
  handleOptions() {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  },
};
