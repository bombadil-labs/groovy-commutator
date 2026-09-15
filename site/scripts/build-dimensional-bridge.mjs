import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { gunzipSync } from 'node:zlib';

const here = dirname(fileURLToPath(import.meta.url));
const site = resolve(here, '..');
const payloadDir = resolve(site, 'content/dimensional-bridge');
const payload = [1, 2, 3, 4]
  .map((part) => readFileSync(resolve(payloadDir, `bridge-v6.b64.${part}`), 'utf8').trim())
  .join('');
const html = gunzipSync(Buffer.from(payload, 'base64'));
const output = resolve(site, 'dimensional-bridge.html');
writeFileSync(output, html);
console.log(`built ${output} (${html.byteLength.toLocaleString()} bytes)`);
