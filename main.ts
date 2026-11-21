import { copyFileSync, mkdirSync } from "node:fs";

const out = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
mkdirSync(out, { recursive: true });
copyFileSync(new URL("./news.jpg", import.meta.url), `${out}/entry.png`);
