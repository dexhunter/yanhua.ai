import { Hono } from "hono";
import { serveStatic } from "hono/cloudflare-workers";

const app = new Hono();

// --- API Route ---
// This route handles GET requests to /api/citations and fetches data from the KV namespace.
app.get("/api/citations", async (c) => {
  const data = await c.env.CITATIONS_KV.get("citations_data", { type: "text" });

  if (data === null) {
    return c.json(
      { error: "No citation data found. Run the update action." },
      404
    );
  }

  return c.body(data, 200, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  });
});

// --- Static Asset Serving ---
// Serve static files from the root directory. This should be placed after specific API routes.
app.get("/", serveStatic({ path: "./index.html" }));
app.get("*", serveStatic({ root: "./" }));


// --- SPA Fallback ---
// If a requested file is not found, serve index.html. This is crucial for single-page applications.
app.notFound((c) => {
  return serveStatic({ path: "./index.html" })(c);
});

export default app;