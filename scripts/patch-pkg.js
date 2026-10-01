const fs = require("fs");
const path = require("path");

const candidates = [
  path.join(process.cwd(), "node_modules", "whatsapp-rust-bridge", "package.json"),
  path.join(process.cwd(), "node_modules", "@whiskeysockets", "baileys", "node_modules", "whatsapp-rust-bridge", "package.json"),
];

for (const pkgPath of candidates) {
  try {
    if (fs.existsSync(pkgPath)) {
      const data = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
      data.main = "./dist/index.js";
      if (!data.exports) data.exports = {};
      if (typeof data.exports === "string") {
        data.exports = { ".": { import: data.exports, require: data.exports, default: data.exports } };
      } else if (data.exports["."]) {
        data.exports["."].import = "./dist/index.js";
        data.exports["."].require = "./dist/index.js";
        data.exports["."].default = "./dist/index.js";
        data.exports["."].types = "./dist/index.d.ts";
      } else {
        data.exports["."] = {
          types: "./dist/index.d.ts",
          import: "./dist/index.js",
          require: "./dist/index.js",
          default: "./dist/index.js",
        };
      }
      fs.writeFileSync(pkgPath, JSON.stringify(data, null, 2), "utf8");
      console.log(`✅ [PATCH-PKG] Successfully patched exports in ${pkgPath}`);
    }
  } catch (err) {
    console.warn(`⚠️ [PATCH-PKG] Could not patch ${pkgPath}:`, err.message);
  }
}
