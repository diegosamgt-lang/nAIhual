import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';

test('servidor entrega la web, responde sin IA y protege archivos privados',async t=>{
  const child=spawn(process.execPath,['server.mjs'],{cwd:new URL('..',import.meta.url),env:{...process.env,PORT:'0',GEMINI_API_KEY:'',GEMINI_MODEL:''},stdio:['ignore','pipe','pipe']});
  t.after(()=>child.kill());
  const [chunk]=await once(child.stdout,'data');const port=String(chunk).match(/Puerto: (\d+)/)?.[1];assert.ok(port);
  const base=`http://127.0.0.1:${port}`;
  const html=await fetch(base);assert.equal(html.status,200);assert.match(await html.text(),/Explorá a tu ritmo/);
  const module=await fetch(base+'/lib/core.mjs');assert.match(module.headers.get('content-type'),/javascript/);
  const c0=await fetch(base+'/c0/');assert.match(await c0.text(),/Beta C0/);
  for(const file of ['/.env','/server.mjs','/lib/chat-service.mjs','/docs/nAIhual_TRASPASO_MAESTRO.md','/.git/config'])assert.equal((await fetch(base+file)).status,404);
  const chat=await fetch(base+'/api/chat',{method:'POST',body:JSON.stringify({message:'Mostrar puntos'})});
  const reply=await chat.json();assert.equal(reply.mode,'guided');assert.deepEqual(reply.places,[]);assert.match(reply.text,/Todavía no hay puntos/);
  assert.equal((await fetch(base+'/api/chat',{method:'POST',body:JSON.stringify({message:''})})).status,400);
  assert.equal((await fetch(base+'/api/chat',{method:'POST',headers:{Origin:'https://otro.example'},body:JSON.stringify({message:'hola'})})).status,403);
  assert.equal((await fetch(base+'/api/chat',{method:'POST',body:'x'.repeat(7000)})).status,413);
});
