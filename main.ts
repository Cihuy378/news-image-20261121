// news-image-20261121 — the entry program.
//
// The finished front page lives in this repo as entry.png, already
// composed by compose.py. All this program does is copy that file,
// byte for byte, to the grader's output directory.
//
// It reads nothing else and needs nothing else: no network, no clock,
// no random numbers, no dependencies beyond the Node standard library.
// Two runs therefore always write the exact same bytes, which is what
// the grader checks.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const sourcePath = join(here, "entry.png");
const targetPath = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });

const bytes = readFileSync(sourcePath);
writeFileSync(targetPath, bytes);

// Fail loudly instead of shipping a bad copy: re-read what we wrote
// and compare it with the source, byte for byte.
const written = readFileSync(targetPath);
if (written.length !== bytes.length || !written.equals(bytes)) {
  throw new Error(
    `entry.png copy mismatch: wrote ${written.length} bytes, source is ${bytes.length}`
  );
}
