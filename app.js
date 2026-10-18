import { validateCatalog, validCoordinate, guidedReply, parseRoute, nearestOnRoute, instruction, distance } from './lib/core.mjs';

const $ = id => document.getElementById(id);
const state = { map:null, catalog:[], catalogReady:false, selected:null, destinationMarker:null, locationMarker:null, accuracyCircle:null, location:null, watch:null, locationEpoch:0, route:null, routeLayer:null, routeController:null, routeVersion:0, lastRouteAt:0, history:[], picking:false, apiAvailable:true, busy:false, chatEpoch:0, chatController:null, locationError:false, startedLocation:false };
const mapMessage = text => { $('map-message').textContent=text; $('map-message').hidden=!text; };

function refreshJourney() {
  const fresh=state.location&&!state.locationError&&Date.now()-state.location.timestamp<=30000&&state.location.accuracy<=80;
  const show=(id,text,status)=>{const box=$(id),label=box.querySelector('strong');if(label.textContent!==text)label.textContent=text;if(box.dataset.state!==status)box.dataset.state=status;};
  show('journey-destination',state.selected?'Elegido':'Sin elegir',state.selected?'done':'pending');
  show('journey-location',fresh?'Señal recibida':state.startedLocation?'Esperando señal':'Desactivada',fresh?'done':state.startedLocation?'caution':'pending');
  show('journey-route',state.route?(fresh?'Ruta calculada':'Seguimiento pausado'):state.routeController?'Calculando…':'Sin calcular',state.route?(fresh?'done':'caution'):'pending');
}

function message(role,text) {
  const el=document.createElement('div'); el.className=`message ${role}`;
  const label=document.createElement('span'); label.className='speaker'; label.textContent=role==='user'?'Vos':'nAIhual';
  const p=document.createElement('p');p.textContent=text;el.append(label,p);$('chat-log').append(el);
  // Memoria efímera y limitada; nunca localStorage ni envío automático.
  state.history.push({role,text});state.history=state.history.slice(-12);
  while($('chat-log').children.length>30) $('chat-log').firstElementChild.remove();
  $('chat-log').scrollTop=$('chat-log').scrollHeight;
}

function clearRoute() {
  state.routeVersion++;
  state.routeController?.abort();state.routeController=null;
  if(state.routeLayer) state.map?.removeLayer(state.routeLayer);
  state.routeLayer=null;state.route=null;$('route-panel').hidden=true;$('route-steps').replaceChildren();
  $('route-button').disabled=false;
  $('route-status').textContent=state.location?'Podés calcular un nuevo recorrido.':'Activá tu ubicación para calcular el recorrido.';
  refreshJourney();
}

function drawDestination(place) {
  if(state.destinationMarker) state.map?.removeLayer(state.destinationMarker);
  if(state.map) {
    const icon=L.divIcon({className:'destination-icon',html:'<svg aria-hidden="true" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 18 18 6M6 6h12v12"/></svg>',iconSize:[30,30],iconAnchor:[15,15]});
    state.destinationMarker=L.marker([place.lat,place.lng],{icon,title:place.name}).addTo(state.map);
    const label=document.createElement('span');label.textContent=place.name;state.destinationMarker.bindPopup(label);
    state.map.panTo([place.lat,place.lng]);
  }
}

function selectDestination(place) {
  clearRoute();state.selected=place;state.picking=false;$('pick-button').setAttribute('aria-pressed','false');
  drawDestination(place);
  $('destination-panel').hidden=false;$('destination-title').textContent=place.name;
  $('destination-detail').textContent=place.status==='verified' ? [place.address,place.city,`Revisado: ${place.reviewedAt}`].filter(Boolean).join(' · ') : `${place.lat.toFixed(5)}, ${place.lng.toFixed(5)} · Punto elegido por vos; no es una ficha curada.`;
  $('selection-summary').textContent=`Destino: ${place.name}. Coordenadas: ${place.lat.toFixed(5)}, ${place.lng.toFixed(5)}.`;
  mapMessage('Destino elegido. Activá tu ubicación y calculá una ruta a pie.');
  refreshJourney();
}

function placeButton(place,container) {
  const b=document.createElement('button');b.type='button';b.className='place-button';
  const name=document.createElement('strong');name.textContent=place.name;
  const detail=document.createElement('small');detail.textContent=`${place.category} · ${place.city}`;b.append(name,detail);
  b.addEventListener('click',()=>{selectDestination(place);$('destination-panel').scrollIntoView({block:'nearest',behavior:'auto'});});container.append(b);
}

async function loadCatalog() {
  try {
    const res=await fetch('./data/places.json',{cache:'no-store'});if(!res.ok)throw new Error();
    state.catalog=validateCatalog(await res.json());state.catalogReady=true;
    $('place-count').textContent=`${state.catalog.length} punto${state.catalog.length===1?'':'s'}`;
    $('catalog-status').textContent=state.catalog.length?'Seleccioná un punto para ubicarlo.':'Todavía no hay puntos curados cargados. Podés probar el mapa eligiendo un destino.';
    for(const place of state.catalog) {
      placeButton(place,$('places-list'));
      const source=document.createElement('a');source.href=place.sourceUrl;source.target='_blank';source.rel='noopener noreferrer';source.className='source-link';source.textContent=`Fuente de ${place.name} · ${place.reviewedAt}`;$('places-list').append(source);
      if(state.map) {
        const marker=L.circleMarker([place.lat,place.lng],{radius:8,color:'#183d33',fillColor:'#d9edac',fillOpacity:1,weight:2}).addTo(state.map);
        const b=document.createElement('button');b.type='button';b.textContent=place.name;b.addEventListener('click',()=>selectDestination(place));marker.bindPopup(b);
      }
    }
  } catch {
    state.catalogReady=false;$('catalog-status').textContent='No pude cargar los puntos. No voy a mostrar datos incompletos. Podés elegir un destino en el mapa.';
  }
}

function initMap() {
  if(!window.L) { mapMessage('No pude cargar el mapa. Recargá la página; también podés indicar coordenadas.');return; }
  state.map=L.map('map',{scrollWheelZoom:false}).setView([14.5586,-90.7336],15);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).on('tileerror',()=>mapMessage('No pude cargar el fondo del mapa. Revisá tu conexión. No se puede confirmar el recorrido visualmente.')).on('load',()=>{
    if(!state.map.getPane('tilePane').querySelector('.leaflet-tile-loaded'))return;
    if(!state.selected)mapMessage('Mové el mapa y pulsá «Elegir destino en el mapa».');
  }).addTo(state.map);
  state.map.on('click',event=>{
    if(!state.picking)return;
    selectDestination({name:'Punto elegido en el mapa',lat:event.latlng.lat,lng:event.latlng.lng,status:'manual'});
  });
  mapMessage('Mové el mapa y pulsá «Elegir destino en el mapa».');
  if(state.selected)drawDestination(state.selected);
}

function stopLocation(reason='Ubicación detenida. Tu posición se borró de esta sesión.') {
  state.locationEpoch++;
  if(state.watch!==null)navigator.geolocation?.clearWatch(state.watch);
  state.watch=null;state.location=null;state.startedLocation=false;state.locationError=false;clearRoute();
  if(state.locationMarker)state.map?.removeLayer(state.locationMarker);
  if(state.accuracyCircle)state.map?.removeLayer(state.accuracyCircle);
  state.locationMarker=null;state.accuracyCircle=null;
  $('locate-button').hidden=false;$('locate-button').disabled=false;$('stop-button').hidden=true;$('location-badge').textContent='Ubicación desactivada';mapMessage(reason);
  refreshJourney();
}

function locationFailure(error) {
  state.locationError=true;
  const text={1:'No diste permiso de ubicación. Podés habilitarlo en tu navegador y volver a intentar.',2:'El dispositivo no pudo determinar tu ubicación. Probá donde haya mejor señal.',3:'La ubicación tardó demasiado. Podés volver a intentar.'}[error.code]||'No pude leer tu ubicación.';
  if(error.code===1){stopLocation(text);return;}
  $('location-badge').textContent='Ubicación sin señal';$('route-status').textContent=text;
  if(state.route)$('next-instruction').textContent='Seguimiento pausado: no hay una posición actual confiable.';
  mapMessage(text);
  if(!state.location){$('locate-button').hidden=false;$('locate-button').disabled=false;}
  refreshJourney();
}

function onPosition(position) {
  const point={lat:position.coords.latitude,lng:position.coords.longitude,accuracy:position.coords.accuracy,timestamp:position.timestamp};
  if(!validCoordinate(point)||!Number.isFinite(point.accuracy)||point.accuracy<0||!Number.isFinite(point.timestamp))return locationFailure({code:2});
  state.locationError=false;state.location=point;
  $('locate-button').hidden=true;$('locate-button').disabled=false;$('stop-button').hidden=false;
  $('location-badge').textContent=`Ubicación activa · precisión ±${Math.round(point.accuracy)} m`;
  if(state.map) {
    if(!state.locationMarker){state.locationMarker=L.circleMarker([point.lat,point.lng],{radius:7,color:'white',weight:3,fillColor:'#2668c4',fillOpacity:1}).addTo(state.map);state.accuracyCircle=L.circle([point.lat,point.lng],{radius:point.accuracy,color:'#2668c4',weight:1,fillOpacity:.08}).addTo(state.map);state.map.panTo([point.lat,point.lng]);}
    else {state.locationMarker.setLatLng([point.lat,point.lng]);state.accuracyCircle.setLatLng([point.lat,point.lng]).setRadius(point.accuracy);}
  }
  if(!state.route){$('route-status').textContent=point.accuracy>80?'La precisión es baja. Esperá una mejor señal antes de calcular la ruta.':'Ubicación recibida. Elegí un destino y calculá el recorrido.';mapMessage('Tu ubicación está activa. Podés detenerla cuando querás.');}
  updateProgress();
}

function startLocation() {
  if(!window.isSecureContext){mapMessage('La ubicación necesita una conexión HTTPS.');return;}
  if(!navigator.geolocation){mapMessage('Este navegador no ofrece ubicación.');return;}
  if(state.watch!==null)navigator.geolocation.clearWatch(state.watch);
  const epoch=++state.locationEpoch;
  state.locationError=false;state.startedLocation=true;$('locate-button').disabled=true;$('stop-button').hidden=false;$('location-badge').textContent='Pidiendo permiso…';
  refreshJourney();
  state.watch=navigator.geolocation.watchPosition(p=>{if(epoch===state.locationEpoch)onPosition(p);},e=>{if(epoch===state.locationEpoch)locationFailure(e);},{enableHighAccuracy:true,timeout:20000,maximumAge:0});
}

function updateProgress() {
  refreshJourney();
  if(!state.route || !state.location)return;
  if(state.locationError || Date.now()-state.location.timestamp>30000 || state.location.accuracy>80) {$('next-instruction').textContent='Seguimiento pausado: esperando una ubicación reciente y precisa.';return;}
  const progress=nearestOnRoute(state.location,state.route.coordinates);
  if(progress.distance>Math.max(45,state.location.accuracy)) {$('next-instruction').textContent='Tu ubicación se alejó del recorrido. Revisá el mapa y pulsá «Calcular ruta a pie» para actualizarlo.';return;}
  if(distance(state.location,state.selected)<=Math.max(20,Math.min(state.location.accuracy,35)) && progress.total-progress.along<50){$('next-instruction').textContent='Estás cerca del destino elegido. Confirmá el punto en el mapa.';return;}
  const next=state.route.steps.find(s=>s.along>progress.along+12)||state.route.steps.at(-1);
  const meters=Math.max(0,Math.round(next.along-progress.along));
  $('next-instruction').textContent=`${meters>15?`En ${meters} m: `:''}${instruction(next)}.`;
}

async function calculateRoute() {
  if(!state.selected)return;
  if(!state.location || state.locationError || Date.now()-state.location.timestamp>30000){$('route-status').textContent='Activá tu ubicación y esperá una posición reciente antes de calcular.';return;}
  if(state.location.accuracy>80){$('route-status').textContent='La ubicación tiene poca precisión. Esperá una mejor señal.';return;}
  if(distance(state.location,state.selected)>30000){$('route-status').textContent='Esta primera prueba admite recorridos a pie de hasta 30 km en línea recta. Elegí un destino más cercano.';return;}
  const now=Date.now();if(now-state.lastRouteAt<5500){$('route-status').textContent='Esperá unos segundos antes de volver a consultar el servicio de rutas.';return;}
  clearRoute();state.lastRouteAt=now;const version=state.routeVersion;
  const origin={...state.location},destination={...state.selected};
  const controller=new AbortController();state.routeController=controller;
  const timer=setTimeout(()=>controller.abort(),15000);$('route-button').disabled=true;$('route-status').textContent='Consultando recorrido a pie…';
  refreshJourney();
  try {
    // Backend explícitamente peatonal. No usar router OSRM de automóvil como ruta a pie.
    const url=`https://routing.openstreetmap.de/routed-foot/route/v1/foot/${origin.lng},${origin.lat};${destination.lng},${destination.lat}?overview=full&geometries=geojson&steps=true`;
    const response=await fetch(url,{signal:controller.signal,referrerPolicy:'strict-origin-when-cross-origin'});
    if(!response.ok)throw new Error('El servicio de rutas no está disponible.');
    const route=parseRoute(await response.json(),origin,destination);
    if(version!==state.routeVersion)return;
    state.route=route;
    if(state.map){state.routeLayer=L.polyline(route.coordinates.map(c=>[c[1],c[0]]),{color:'#366b4b',weight:6,opacity:.9}).addTo(state.map);state.map.fitBounds(state.routeLayer.getBounds(),{padding:[25,25]});}
    $('route-panel').hidden=false;$('route-distance').textContent=`${route.distance>=1000?(route.distance/1000).toFixed(1)+' km':Math.round(route.distance)+' m'} · recorrido a pie estimado`;
    for(const step of route.steps){const li=document.createElement('li');li.textContent=instruction(step)+'.';$('route-steps').append(li);}
    $('route-status').textContent='Ruta recibida. El indicador se actualiza mientras la ubicación esté activa. Si te desviás, recalculá.';
    mapMessage('Recorrido experimental a pie. Confirmá el camino y las condiciones en el lugar.');updateProgress();
  } catch(error) {
    if(version===state.routeVersion){$('route-status').textContent=error.name==='AbortError'?'La consulta tardó demasiado. Volvé a intentar.':(error instanceof TypeError?'No pude conectar con el servicio de rutas. Revisá tu conexión e intentá de nuevo.':error.message);}
  } finally {clearTimeout(timer);if(version===state.routeVersion){$('route-button').disabled=false;state.routeController=null;refreshJourney();}}
}

async function sendChat(text) {
  text=text.trim().slice(0,500);if(!text||state.busy)return;
  state.busy=true;$('send-button').disabled=true;
  const epoch=++state.chatEpoch;
  const history=state.history.slice(-6);message('user',text);$('chat-input').value='';
  try {
    const local=guidedReply(text,state.catalog);
    let reply=['coordinates','invalid-coordinates','help','show-destination','show-location'].includes(local.action)?local:null;
    if(!reply&&state.apiAvailable){
      try {
        state.chatController=new AbortController();
        const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text,history}),signal:AbortSignal.any([state.chatController.signal,AbortSignal.timeout(15000)])});
        if(!res.ok)throw new Error();reply=await res.json();
        if(typeof reply.text!=='string'||!['guided','ai'].includes(reply.mode))throw new Error();
      } catch {if(epoch!==state.chatEpoch)return;state.apiAvailable=false;reply=null;}
    }
    if(epoch!==state.chatEpoch)return;
    if(!reply)reply=local;
    if(!state.catalogReady && !reply.places?.length && !['coordinates','invalid-coordinates','help','show-destination','show-location'].includes(reply.action))reply={...reply,text:'No pude cargar la selección de puntos. Podés elegir un destino en el mapa, pero no puedo confirmar búsquedas en el catálogo.'};
    if(reply.action==='show-destination'&&state.selected)reply.text=`Tu destino es ${state.selected.name}: ${state.selected.lat.toFixed(5)}, ${state.selected.lng.toFixed(5)}. Podés cambiarlo desde el mapa o indicar otras coordenadas.`;
    if(reply.action==='show-location'&&state.location){
      reply.text=!state.locationError&&Date.now()-state.location.timestamp<=30000&&state.location.accuracy<=80?`Tu dispositivo indica ${state.location.lat.toFixed(5)}, ${state.location.lng.toFixed(5)}, con precisión aproximada de ±${Math.round(state.location.accuracy)} m. Esa posición no se guarda.`:'No tengo una posición reciente y precisa para mostrarte. Esperá una mejor señal de ubicación.';
    }
    $('chat-mode').textContent=reply.mode==='ai'?'IA para interpretar · ubicaciones de tu selección':'Conversación guiada · sin IA conectada';
    if(reply.action==='directions'&&state.selected&&!reply.places?.length)reply.text=`Tu destino elegido es ${state.selected.name}. Activá tu ubicación y pulsá «Calcular ruta a pie».`;
    message('assistant',reply.text+(reply.notice?'\n'+reply.notice:''));
    if(reply.action==='coordinates'&&validCoordinate(reply.destination)){
      const button=document.createElement('button');button.type='button';button.className='button coordinate-confirm';button.textContent='Usar este destino';
      button.addEventListener('click',()=>{selectDestination(reply.destination);button.disabled=true;button.textContent='Destino elegido';message('assistant',state.startedLocation?'Destino elegido. La ubicación sigue activada; no calculé una ruta nueva. Pulsá «Calcular ruta a pie» cuando querás continuar.':'Destino elegido. La ubicación sigue desactivada y no calculé la ruta; esos pasos los decidís vos.');});
      $('chat-log').lastElementChild.append(button);
    }
    for(const candidate of reply.places||[]){const place=state.catalog.find(p=>p.id===candidate.id);if(place)placeButton(place,$('chat-log').lastElementChild);}
  } finally {if(epoch===state.chatEpoch){state.busy=false;state.chatController=null;$('send-button').disabled=false;}}
}

function renderPage() {
  let hash;try{hash=decodeURIComponent(location.hash.slice(1));}catch{hash='inicio';}
  const page=['inicio','explorar','resumen','proposito'].includes(hash)?hash:'inicio';
  document.querySelectorAll('.page').forEach(el=>{el.hidden=el.id!==`page-${page}`;});
  document.querySelectorAll('[data-nav]').forEach(el=>{if(el.dataset.nav===(page==='resumen'?'explorar':page))el.setAttribute('aria-current','page');else el.removeAttribute('aria-current');});
  document.title=`${{inicio:'Inicio',explorar:'Explorar',resumen:'Tu consulta',proposito:'Propósito'}[page]} · nAIhual`;
  if(page==='explorar')setTimeout(()=>state.map?.invalidateSize(),0);
  else if(state.startedLocation)stopLocation();
  window.scrollTo({top:0,behavior:'instant'});
}

$('locate-button').addEventListener('click',startLocation);
$('stop-button').addEventListener('click',()=>stopLocation());
$('center-button').addEventListener('click',()=>{
  if(!state.map){mapMessage('El mapa todavía no está disponible. Podés seguir conversando o indicar coordenadas.');return;}
  const current=state.location&&!state.locationError&&Date.now()-state.location.timestamp<=30000&&state.location.accuracy<=80?state.location:null;
  if(current&&state.selected)state.map.fitBounds([[current.lat,current.lng],[state.selected.lat,state.selected.lng]],{padding:[35,35],maxZoom:17});
  else if(current||state.selected){const point=current||state.selected;state.map.setView([point.lat,point.lng],16);}
  else state.map.setView([14.5586,-90.7336],15);
});
$('clear-chat').addEventListener('click',()=>{state.chatEpoch++;state.chatController?.abort();state.chatController=null;state.busy=false;$('send-button').disabled=false;state.history=[];$('chat-log').replaceChildren();message('assistant','La conversación se borró de esta pantalla. Podés empezar otra consulta. Tu destino y la ubicación no cambian; para detener el GPS usá «Detener ubicación».');});
$('pick-button').addEventListener('click',()=>{if(!state.map){mapMessage('El mapa no está disponible. Usá las coordenadas para elegir un destino.');return;}state.picking=!state.picking;$('pick-button').setAttribute('aria-pressed',String(state.picking));mapMessage(state.picking?'Tocá un punto del mapa para elegir tu destino.':'Selección de destino cancelada.');});
$('clear-destination').addEventListener('click',()=>{clearRoute();state.selected=null;if(state.destinationMarker)state.map?.removeLayer(state.destinationMarker);state.destinationMarker=null;$('destination-panel').hidden=true;$('selection-summary').textContent='Todavía no elegiste un destino.';refreshJourney();});
$('coordinate-form').addEventListener('submit',event=>{event.preventDefault();const lat=$('destination-lat').value,lng=$('destination-lng').value;const point={lat:Number(lat),lng:Number(lng)};if(!lat||!lng||!validCoordinate(point))return;selectDestination({...point,name:'Punto indicado por coordenadas',status:'manual'});});
$('route-button').addEventListener('click',calculateRoute);
$('chat-form').addEventListener('submit',event=>{event.preventDefault();sendChat($('chat-input').value);});
document.querySelectorAll('[data-prompt]').forEach(b=>b.addEventListener('click',()=>sendChat(b.dataset.prompt)));
window.addEventListener('hashchange',renderPage);
document.querySelector('.skip').addEventListener('click',event=>{event.preventDefault();$('principal').focus();});
window.addEventListener('pagehide',()=>stopLocation());
document.addEventListener('visibilitychange',()=>{if(document.hidden&&state.startedLocation)stopLocation('La ubicación se detuvo al salir de esta pantalla. Activala de nuevo para continuar.');});
setInterval(updateProgress,5000);
initMap();renderPage();loadCatalog();refreshJourney();
