import test from 'node:test';
import assert from 'node:assert/strict';
import { validateCatalog, guidedReply, distance, nearestOnRoute, parseRoute, instruction } from '../lib/core.mjs';
import { chatReply } from '../lib/chat-service.mjs';

const place={id:'punto-prueba',name:'Punto de prueba',category:'museo',city:'Antigua',lat:14.5586,lng:-90.7336,sourceUrl:'https://example.org/fuente',reviewedAt:'2026-10-17',status:'verified'};
const origin={lat:14.5586,lng:-90.7336}, destination={lat:14.5606,lng:-90.7326};
const payload={code:'Ok',routes:[{distance:330,geometry:{type:'LineString',coordinates:[[-90.7336,14.5586],[-90.7336,14.5606],[-90.7326,14.5606]]},legs:[{steps:[{name:'Tramo de prueba',maneuver:{location:[-90.7336,14.5586],type:'depart',modifier:'straight'}},{name:'Otro tramo',maneuver:{location:[-90.7336,14.5606],type:'turn',modifier:'right'}},{name:'',maneuver:{location:[-90.7326,14.5606],type:'arrive'}}]}]}]};

test('rechaza fichas sin fuente, coordenadas inválidas y IDs duplicados',()=>{
  assert.equal(validateCatalog([place])[0].name,place.name);
  for(const bad of [{...place,sourceUrl:''},{...place,lat:91},{...place,lng:'-90'},{...place,status:'pending'}])assert.throws(()=>validateCatalog([bad]));
  assert.throws(()=>validateCatalog([place,place]));
});
test('catálogo vacío y búsquedas sin coincidencia nunca inventan puntos',()=>{
  assert.deepEqual(guidedReply('museos',[]).places,[]);
  assert.match(guidedReply('museos',[]).text,/Todavía no hay/);
  assert.deepEqual(guidedReply('café desconocido',[place]).places,[]);
  assert.equal(guidedReply('Busco un museo',[place]).places[0].id,place.id);
});
test('no produce opiniones, horarios ni supuesta seguridad',()=>{
  for(const query of ['el mejor museo','está abierto','un sitio seguro']){
    const reply=guidedReply(query,[place]);assert.equal(reply.places.length,0);assert.match(reply.text,/No tengo opiniones/);
  }
});
test('medición y avance siguen la geometría del recorrido',()=>{
  assert.equal(distance(origin,origin),0);
  const route=parseRoute(payload,origin,destination);
  const progress=nearestOnRoute({lat:14.5596,lng:-90.7336},route.coordinates);
  assert.ok(progress.distance<1);assert.ok(progress.along>100&&progress.along<120);
  assert.ok(route.steps[1].along>200);assert.match(instruction(route.steps[1]),/derecha/);
});
test('rechaza rutas sin recorrido, sin pasos o alejadas de los puntos elegidos',()=>{
  assert.throws(()=>parseRoute({code:'NoRoute'},origin,destination));
  assert.throws(()=>parseRoute(payload,{lat:0,lng:0},destination));
  const invalid=structuredClone(payload);invalid.routes[0].legs=[];assert.throws(()=>parseRoute(invalid,origin,destination));
  const nan=structuredClone(payload);nan.routes[0].geometry.coordinates[0][0]=null;assert.throws(()=>parseRoute(nan,origin,destination));
});
test('sin credenciales ni catálogo no se envían mensajes a IA',async()=>{
  let calls=0;const fetcher=async()=>{calls++;throw new Error();};
  assert.equal((await chatReply({message:'Museo'},[place],{},fetcher)).mode,'guided');
  assert.equal((await chatReply({message:'Museo'},[],{GEMINI_API_KEY:'test',GEMINI_MODEL:'modelo-prueba'},fetcher)).mode,'guided');
  assert.equal(calls,0);
});
test('la IA solo puede seleccionar IDs existentes; texto inventado no llega al usuario',async()=>{
  const config={GEMINI_API_KEY:'test',GEMINI_MODEL:'modelo-prueba'};
  const mock=value=>async()=>({ok:true,json:async()=>({candidates:[{content:{parts:[{text:JSON.stringify(value)}]}}]})});
  const valid=await chatReply({message:'algo de historia'},[place],config,mock({intent:'find',placeIds:[place.id],text:'Dato inventado'}));
  assert.equal(valid.mode,'ai');assert.equal(valid.places[0].id,place.id);assert.ok(!valid.text.includes('Dato inventado'));
  const invalid=await chatReply({message:'algo de historia'},[place],config,mock({intent:'find',placeIds:['inventado']}));
  assert.equal(invalid.mode,'guided');assert.deepEqual(invalid.places,[]);
});
test('valida mensajes y conserva búsqueda guiada si el proveedor falla',async()=>{
  await assert.rejects(()=>chatReply({message:'x'.repeat(501)},[],{}));
  const reply=await chatReply({message:'museo'},[place],{GEMINI_API_KEY:'test',GEMINI_MODEL:'modelo-prueba'},async()=>({ok:false}));
  assert.equal(reply.mode,'guided');assert.match(reply.notice,/No pude conectar/);
});
