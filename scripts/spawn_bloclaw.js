#!/usr/bin/env node
/**
 * spawn_bloclaw.js
 * 
 * Wrapper for sub-agent spawning using BloClaw Dual-Track Routing.
 * Enforces XML-wrapped task payloads for high-robustness communication.
 * Implements "Skill Loader" pattern (arXiv:2604.21910).
 */

const fs = require('fs');
const path = require('path');

const STRATEGY_DIR = path.join(__dirname, '..', 'strategies');

/**
 * Loads the strategy doc based on intent.
 */
function loadStrategy(intent) {
  const strategyPath = path.join(STRATEGY_DIR, `${intent.toUpperCase()}.md`);
  if (fs.existsSync(strategyPath)) {
    return fs.readFileSync(strategyPath, 'utf8');
  }
  return null;
}

/**
 * Wraps a task payload in the BloClaw XML format.
 */
function wrapBloClaw(intent, task, tools) {
  const strategyDoc = loadStrategy(intent);
  const payload = {
    intent,
    task,
    tools: tools || []
  };

  return `
<bloclaw_routing_protocol>
  <intent>${intent}</intent>
  <payload>${JSON.stringify(payload)}</payload>
  ${strategyDoc ? `<strategy_doc>\n${strategyDoc}\n</strategy_doc>` : ''}
  <command_stream>
    RUN_TASK: "${task}"
    USING_TOOLS: [${payload.tools.join(", ")}]
  </command_stream>
</bloclaw_routing_protocol>
`.trim();
}

/**
 * Mocks the session_spawn tool call with BloClaw wrapping.
 */
function spawnSubAgent(intent, task, tools) {
  const wrappedTask = wrapBloClaw(intent, task, tools);
  
  console.log(`[BloClaw] Spawning sub-agent with wrapped task...`);
  console.log(`[BloClaw] Intent: ${intent}`);
  if (wrappedTask.includes("<strategy_doc>")) {
    console.log(`[BloClaw] Skill Loader: Strategy doc attached.`);
  }
  
  console.log("--- WRAPPED TASK CONTENT ---");
  console.log(wrappedTask);
}

// Example
const task = "Search for latest Lumma Stealer variants on X.";
const tools = ["grok-search", "web_fetch"];
spawnSubAgent("RESEARCH", task, tools);
