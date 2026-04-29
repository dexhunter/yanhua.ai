#!/usr/bin/env node
/**
 * bloclaw_router.js
 * 
 * Implements "BloClaw Dual-Track Routing" (arXiv:2604.00550).
 */

function wrapDualTrack(intent, task, tools) {
  const payload = { intent, task, tools };
  return `<bloclaw><intent>${intent}</intent><payload>${JSON.stringify(payload)}</payload></bloclaw>`;
}

function extractDualTrack(message) {
  const match = message.match(/<payload>(.*?)<\/payload>/);
  if (match) return JSON.parse(match[1]);
  return null;
}

const outgoing = wrapDualTrack("RESEARCH", "Audit RSI Bench", ["web_search"]);
console.log("Outgoing:", outgoing);
console.log("Extracted:", extractDualTrack(outgoing));
