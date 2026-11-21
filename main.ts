// news-image-20261121 entry program (Node 22, standard library only).
//
// The finished picture of 21 November 2026's world news lives in this
// repository as entry.png, drawn beforehand by generate_image.py from
// the sourced stories in data/stories.json. All this program has to do
// at grading time is deliver those exact bytes to the output folder:
//
//   /output/entry.png            inside the grader's container
//   $MAKEFUN_OUTPUT_DIR/entry.png   everywhere else
//
// Run it locally the same way the kit does:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Copying (rather than redrawing) is what makes the two grading runs
// produce byte-identical files.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });

const destination = join(outDir, "entry.png");
copyFileSync(join(repoDir, "entry.png"), destination);

console.log(`news-image-20261121: entry.png copied to ${destination}`);
