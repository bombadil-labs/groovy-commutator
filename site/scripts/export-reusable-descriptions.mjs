// Export the exact site visualization as a self-contained conversation fragment.
// Usage: node site/scripts/export-reusable-descriptions.mjs /workspace/name.html
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const site = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const destination = process.argv[2];
if (!destination || !path.isAbsolute(destination)) throw new Error('An absolute output path is required.');
const read = p => fs.readFileSync(path.join(site, p), 'utf8');
const model = read('src/lib/reusable-description-model.mjs').replace(/^export /gm, '');
const view = read('src/visuals/reusable-descriptions-view.mjs').replace(/^import .*;\n/m, '');
const fragment = read('src/visuals/reusable-descriptions.html') + '\n<style>\n' + read('src/styles/reusable-descriptions.css') + '\n</style>\n<script>\n(() => {\n' + model + '\n' + view + '\n})();\n</script>\n';
fs.writeFileSync(destination, fragment);
console.log(destination);
