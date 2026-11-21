// Smoke test for the news-image-20261121 entry.
//
// Verifies the kit's gate conditions locally:
//   - main.ts and entry.png exist at the repository root
//   - entry.png is a whole PNG (magic bytes), its IHDR dimensions are
//     at most 1024x1024, and the file is at most 1 MiB
//   - running main.ts twice with MAKEFUN_OUTPUT_DIR writes
//     byte-identical output (sha256), equal to the repo's entry.png
//   - main.ts makes no network calls
//
// Run: node smoke.test.mjs

import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
let failures = 0;

function check(label, ok, detail = "") {
  console.log(`${ok ? "PASS" : "FAIL"}  ${label}${detail ? ` (${detail})` : ""}`);
  if (!ok) failures += 1;
}

const sha256 = (buf) => createHash("sha256").update(buf).digest("hex");

// --- files at root -----------------------------------------------------------
const mainPath = join(root, "main.ts");
const pngPath = join(root, "entry.png");
check("main.ts exists at root", existsSync(mainPath));
check("entry.png exists at root", existsSync(pngPath));
if (!existsSync(mainPath) || !existsSync(pngPath)) process.exit(1);

const png = readFileSync(pngPath);

// --- PNG shape ----------------------------------------------------------------
const MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
check("entry.png has PNG magic bytes", MAGIC.every((b, i) => png[i] === b));
check("first chunk is IHDR", png.toString("ascii", 12, 16) === "IHDR");
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
check("IHDR dimensions at most 1024x1024", width <= 1024 && height <= 1024, `${width}x${height}`);
check("file size at most 1 MiB", png.length <= 1_048_576, `${png.length} bytes`);

// --- main.ts is offline ---------------------------------------------------------
const mainSrc = readFileSync(mainPath, "utf8");
check(
  "no network calls in main.ts",
  !/fetch\s*\(|XMLHttpRequest|node:http|node:https|node:net|node:tls|WebSocket/.test(mainSrc),
);

// --- determinism: two runs, identical bytes --------------------------------------
const runs = [];
for (let i = 0; i < 2; i += 1) {
  const outDir = mkdtempSync(join(tmpdir(), `news-image-run${i}-`));
  execFileSync(process.execPath, [mainPath], {
    env: { ...process.env, MAKEFUN_OUTPUT_DIR: outDir },
    stdio: "pipe",
  });
  const produced = join(outDir, "entry.png");
  check(`run ${i + 1} wrote entry.png`, existsSync(produced));
  runs.push(readFileSync(produced));
}
check("two runs are byte-identical", sha256(runs[0]) === sha256(runs[1]), sha256(runs[0]).slice(0, 16));
check("output equals the repo entry.png", sha256(runs[0]) === sha256(png));

if (failures > 0) {
  console.error(`\n${failures} check(s) failed.`);
  process.exit(1);
}
console.log("\nAll smoke tests passed.");
