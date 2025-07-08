import { Hono } from "hono";

// Hono instance with a base path of /api
const app = new Hono().basePath("/api");

// --- API Route ---
// This route now handles GET requests to /api/citations
app.get("/citations", async (c) => {
  // Check if the KV namespace binding is configured
  if (!c.env.CITATIONS_KV) {
    return c.json(
      {
        error:
          "KV namespace binding not configured. Please set up CITATIONS_KV in your Cloudflare Pages project settings.",
      },
      500
    );
  }

  // CITATIONS_KV is automatically bound in the Pages environment
  const data = await c.env.CITATIONS_KV.get("citations_data", { type: "text" });

  if (data === null) {
    return c.json(
      { error: "No citation data found. Run the update action." },
      404
    );
  }

  return c.body(data, 200, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*", // You might want to restrict this in production
  });
});

// The `onRequest` export is the entry point for Cloudflare Pages Functions
export const onRequest = app.fetch;
