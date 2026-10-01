/**
 * index.js - Entrypoint untuk Cloud Bot Panel (Bot-Hosting.net / Pterodactyl)
 */
require("dotenv").config();
const { spawn } = require("child_process");
const path = require("path");

console.log("=======================================================");
console.log("🚀 EXPEDIENT 43 - BOT-HOSTING.NET CLOUD RUNNER");
console.log("📦 Node.js Version:", process.version);
console.log("=======================================================");

const child = spawn("npx", ["tsx", "scripts/wa-gateway.ts"], {
  stdio: "inherit",
  env: process.env,
  shell: true,
});

child.on("exit", (code) => {
  console.log(`⚠️ Bot process exited with code ${code}`);
  process.exit(code || 0);
});

child.on("error", (err) => {
  console.error("❌ Failed to start gateway:", err);
  process.exit(1);
});
