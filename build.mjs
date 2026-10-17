import { cp, mkdir, rm, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root=path.dirname(fileURLToPath(import.meta.url));
const out=path.join(root,'dist');
await rm(out,{recursive:true,force:true});await mkdir(path.join(out,'lib'),{recursive:true});
for(const name of ['index.html','styles.css','app.js','data','vendor','c0']) await cp(path.join(root,name),path.join(out,name),{recursive:true});
await cp(path.join(root,'lib/core.mjs'),path.join(out,'lib/core.mjs'));
await writeFile(path.join(out,'_headers'),`/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(self), microphone=(), camera=()
`);
console.log('Publicación estática preparada en dist/. No contiene claves ni backend de IA.');
