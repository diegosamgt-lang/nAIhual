import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validateCatalog } from './lib/core.mjs';

// Derivado de las mismas fuentes de la web: no mantiene otra implementación.
const root = path.dirname(fileURLToPath(import.meta.url));
const read = file => readFile(path.join(root,file),'utf8');
const scriptSafe = text => text.replace(/<\/script/gi,'<\\/script');
let html = await read('index.html');
let leafletCss = await read('vendor/leaflet/leaflet.css');
for (const match of [...leafletCss.matchAll(/url\(images\/([a-z0-9-]+\.png)\)/g)]) {
  const bytes = await readFile(path.join(root,'vendor/leaflet/images',match[1]));
  leafletCss = leafletCss.replaceAll(match[0],`url(data:image/png;base64,${bytes.toString('base64')})`);
}
const styles = leafletCss+'\n'+await read('styles.css');
const leaflet = (await read('vendor/leaflet/leaflet.js')).replace(/\/\/# sourceMappingURL=.*$/gm,'');
const core = (await read('lib/core.mjs')).replace(/^export /gm,'');
let app = await read('app.js');
const importLine = "import { validateCatalog, validCoordinate, guidedReply, parseRoute, nearestOnRoute, instruction, distance } from './lib/core.mjs';";
const catalogLine = "const res=await fetch('./data/places.json',{cache:'no-store'});if(!res.ok)throw new Error();\n    state.catalog=validateCatalog(await res.json());";
const coordinateHandler = "$('coordinate-form').addEventListener('submit',event=>";
const chatHandler = "$('chat-form').addEventListener('submit',event=>";
if(!app.includes(importLine) || !app.includes(catalogLine) || !app.includes('apiAvailable:true') || !app.includes(coordinateHandler) || !app.includes(chatHandler))throw new Error('Cambió la fuente; revisar el generador antes de empaquetar.');
const catalog = validateCatalog(JSON.parse(await read('data/places.json')));
app = app.replace(importLine,'').replace(catalogLine,`state.catalog=validateCatalog(${JSON.stringify(catalog).replace(/</g,'\\u003c')});`).replace('apiAvailable:true','apiAvailable:false');
// Los visores pueden permitir scripts y bloquear el envío de formularios.
app = app.replace(coordinateHandler,"$('preview-coordinate-apply').addEventListener('click',event=>").replace(chatHandler,"$('send-button').addEventListener('click',event=>");
html = html.replace('type="submit">Usar punto</button>','type="button" id="preview-coordinate-apply">Usar punto</button>').replace('id="send-button" type="submit"','id="send-button" type="button"');
html = html.replace('  <link rel="stylesheet" href="vendor/leaflet/leaflet.css">','').replace('  <link rel="stylesheet" href="styles.css">',`  <style>${styles}</style>`).replace('  <script defer src="vendor/leaflet/leaflet.js"></script>','').replace('  <script type="module" src="app.js"></script>','');
html = html.replace('<a href="c0/">Consultar C0 original</a>','<span>Vista HTML · C0 original conservada en el proyecto</span>');
html = html.replace('<body>','<body>\n  <aside class="notice" style="margin:12px 16px;padding:10px 16px;font-size:12px" role="note">Vista HTML integrada. Podés navegar y conversar aquí. El mapa y las rutas requieren Internet; la ubicación depende de los permisos del visor.</aside>');
const inlineNavigation = `document.addEventListener('click',event=>{const link=event.target.closest('a[href^="#"]');const hash=link?.getAttribute('href');if(['#inicio','#explorar','#resumen','#proposito'].includes(hash)){event.preventDefault();location.hash=hash;}});document.addEventListener('keydown',event=>{if(event.key!=='Enter')return;if(event.target.id==='chat-input'){event.preventDefault();document.getElementById('send-button').click();}else if(event.target.closest('#coordinate-form')){event.preventDefault();document.getElementById('preview-coordinate-apply').click();}});`;
html = html.replace('</body>',`<script>${scriptSafe(leaflet)}</script>\n<script>(function(){\n${scriptSafe(core)}\n${inlineNavigation}\nif(!location.hash)location.hash='explorar';\n${scriptSafe(app)}\n})();</script>\n</body>`);
await mkdir(path.join(root,'entregas'),{recursive:true});
await writeFile(path.join(root,'entregas/naihual-editor.html'),html);
console.log('HTML único preparado: entregas/naihual-editor.html; estilos, catálogo y JavaScript incluidos.');
