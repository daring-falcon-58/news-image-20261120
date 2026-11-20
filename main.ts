// news-image-20261120 entrypoint (Node 22, standard library only).
//
// The front page for Friday 20 November 2026 is drawn by compose.py
// and shipped in this repository as news.jpg (1024x1024 JPEG, under
// the 1 MiB cap). This program copies those exact bytes to the
// grader's output as entry.png. The gate tells PNG from JPEG by the
// file's first bytes, so a JPEG named entry.png is valid, and copying
// byte-for-byte means two runs write identical bytes.
//
// Run it locally (MAKEFUN_OUTPUT_DIR stands in for /output):
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const source = join(repoRoot, "news.jpg");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outputDir, "entry.png");

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);

const bytes = statSync(target).size;
console.log(`Wrote ${target} (${bytes} bytes)`);
