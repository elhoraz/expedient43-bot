require("dotenv").config();
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

console.log("=======================================================");
console.log("🚀 EXPEDIENT 43 - WHATSAPP BOT RUNNER");
console.log("📦 Node.js Version:", process.version);
console.log("📁 CWD:", process.cwd());
console.log("🌐 PORT:", process.env.PORT || 10000);
console.log("🔑 Supabase URL Configured:", !!process.env.NEXT_PUBLIC_SUPABASE_URL);
console.log("=======================================================");

// Find tsx binary
const tsxLocal = path.join(__dirname, "node_modules", ".bin", process.platform === "win32" ? "tsx.cmd" : "tsx");
const cmd = fs.existsSync(tsxLocal) ? tsxLocal : "npx";
const args = fs.existsSync(tsxLocal) ? ["scripts/wa-gateway.ts"] : ["tsx", "scripts/wa-gateway.ts"];

console.log(`Starting: ${cmd} ${args.join(" ")}`);

const child = spawn(cmd, args, {
  stdio: "inherit",
  env: process.env,
  shell: process.platform === "win32",
});

child.on("exit", (code) => {
  console.log(`⚠️ Bot process exited with code ${code}`);
  if (code !== 0) {
    setTimeout(() => process.exit(code || 1), 5000);
  } else {
    process.exit(0);
  }
});

child.on("error", (err) => {
  console.error("❌ Failed to start gateway:", err);
  setTimeout(() => process.exit(1), 5000);
});
