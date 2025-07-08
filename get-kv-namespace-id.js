const fs = require('fs');
const toml = require('toml');

function getKvNamespaceId(bindingName) {
  try {
    const tomlContent = fs.readFileSync('wrangler.toml', 'utf-8');
    const config = toml.parse(tomlContent);

    if (!config.kv_namespaces || !Array.isArray(config.kv_namespaces)) {
      console.error("Error: 'kv_namespaces' not found or not an array in wrangler.toml");
      process.exit(1);
    }

    const namespace = config.kv_namespaces.find(ns => ns.binding === bindingName);

    if (namespace && namespace.id) {
      return namespace.id;
    } else {
      console.error(`Error: Could not find KV namespace ID for binding '${bindingName}' in wrangler.toml`);
      process.exit(1);
    }
  } catch (error) {
    console.error("Error reading or parsing wrangler.toml:", error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  const bindingName = process.argv[2];
  if (!bindingName) {
    console.error("Usage: node get-kv-namespace-id.js <bindingName>");
    process.exit(1);
  }
  const kvId = getKvNamespaceId(bindingName);
  console.log(kvId);
}

module.exports = getKvNamespaceId;
