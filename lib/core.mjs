export const normalize = value => String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
export const validCoordinate = point => point && typeof point.lat === 'number' && Number.isFinite(point.lat) && Math.abs(point.lat) <= 90 && typeof point.lng === 'number' && Number.isFinite(point.lng) && Math.abs(point.lng) <= 180;

export function validateCatalog(input) {
  if (!Array.isArray(input)) throw new Error('El catálogo debe ser una lista.');
  const ids = new Set();
  return input.map(place => {
    if (!place || !/^[a-z0-9-]{1,80}$/.test(place.id) || ids.has(place.id) || !validCoordinate(place) || typeof place.name !== 'string' || !place.name.trim() || typeof place.category !== 'string' || typeof place.city !== 'string' || !/^https:\/\//.test(place.sourceUrl || '') || !/^\d{4}-\d{2}-\d{2}$/.test(place.reviewedAt || '') || place.status !== 'verified') {
      throw new Error('Hay una ficha incompleta, duplicada o sin verificación.');
    }
    ids.add(place.id);
    return { id: place.id, name: place.name.trim().slice(0, 160), category: place.category.slice(0, 80), city: place.city.slice(0, 80), address: String(place.address || '').slice(0, 250), lat: place.lat, lng: place.lng, sourceUrl: new URL(place.sourceUrl).href, reviewedAt: place.reviewedAt, status: 'verified' };
  });
}

export function guidedReply(message, places, classification = null) {
  const query = normalize(message);
  const base = { mode: 'guided', action: 'none', places: [] };
  if (/\b(mejor|peor|bonito|seguro|peligroso|opinion|precio|horario|abierto)\b/.test(query)) return { ...base, text: 'Puedo ayudarte con ubicaciones y direcciones. No tengo opiniones, horarios, precios ni información de seguridad verificada.' };
  if (/\b(gracias|hola|buenas|buenos dias)\b/.test(query)) return { ...base, text: '¡Hola! Decime qué punto querés encontrar. También podés elegir un destino directamente en el mapa.' };
  if (classification?.intent === 'directions' || /\b(llegar|llego|direccion|direcciones|ruta|caminar|guiame)\b/.test(query)) {
    const matches = places.filter(p => query.includes(normalize(p.name)) || classification?.placeIds?.includes(p.id));
    return { ...base, action: 'directions', places: matches.slice(0, 3), text: matches.length ? 'Seleccioná el destino y después calculá la ruta a pie. Tu ubicación se pide solo cuando vos la activás.' : 'Elegí un punto en el mapa o en la lista. Después activá tu ubicación y pulsá «Calcular ruta a pie».' };
  }
  if (!places.length) return { ...base, text: 'Todavía no hay puntos curados cargados. Podés elegir un destino en el mapa para probar el recorrido. No voy a inventar lugares.' };
  const matches = places.filter(p => query.includes(normalize(p.name)) || query.includes(normalize(p.category)) || classification?.placeIds?.includes(p.id));
  const all = /\b(puntos|lugares|mostrar|todos|ver)\b/.test(query);
  const found = (matches.length ? matches : all ? places : []).slice(0, 3);
  return { ...base, places: found, text: found.length ? 'Encontré estos puntos en la selección cargada. Te muestro su ubicación, sin calificarlos.' : 'No encontré un punto que coincida en la selección cargada. Podés decirme otro nombre o elegirlo en el mapa.' };
}

export function distance(a, b) {
  const rad = Math.PI / 180;
  const dlat = (b.lat - a.lat) * rad, dlng = (b.lng - a.lng) * rad;
  const h = Math.sin(dlat / 2) ** 2 + Math.cos(a.lat * rad) * Math.cos(b.lat * rad) * Math.sin(dlng / 2) ** 2;
  return 6371000 * 2 * Math.atan2(Math.sqrt(h), Math.sqrt(Math.max(0, 1 - h)));
}

export function nearestOnRoute(point, coordinates) {
  const scale = Math.cos(point.lat * Math.PI / 180);
  let best = { distance: Infinity, along: 0, total: 0, point: null };
  let traversed = 0;
  for (let i = 1; i < coordinates.length; i++) {
    const a = { lng: coordinates[i-1][0], lat: coordinates[i-1][1] }, b = { lng: coordinates[i][0], lat: coordinates[i][1] };
    const x = (b.lng-a.lng) * scale, y = b.lat-a.lat;
    const t = Math.max(0, Math.min(1, ((point.lng-a.lng)*scale*x + (point.lat-a.lat)*y) / (x*x+y*y || 1)));
    const candidate = { lat: a.lat + (b.lat-a.lat)*t, lng: a.lng + (b.lng-a.lng)*t };
    const d = distance(point, candidate), length = distance(a,b);
    if (d < best.distance) best = { distance: d, along: traversed+length*t, point: candidate };
    traversed += length;
  }
  return { ...best, total: traversed };
}

export function parseRoute(payload, origin, destination) {
  const raw = payload?.routes?.[0];
  if (payload?.code !== 'Ok' || !raw || raw.geometry?.type !== 'LineString' || !Array.isArray(raw.geometry.coordinates) || raw.geometry.coordinates.length < 2 || !Number.isFinite(raw.distance) || raw.distance < 0) throw new Error('El servicio no devolvió una ruta válida.');
  const coordinates = raw.geometry.coordinates;
  if (coordinates.length > 100000 || coordinates.some(c => !Array.isArray(c) || !validCoordinate({lng:c[0],lat:c[1]}))) throw new Error('La ruta contiene coordenadas inválidas.');
  if (distance(origin, {lng:coordinates[0][0],lat:coordinates[0][1]}) > 120 || distance(destination, {lng:coordinates.at(-1)[0],lat:coordinates.at(-1)[1]}) > 120) throw new Error('La ruta no llega suficientemente cerca del origen o destino elegido.');
  const steps = raw.legs?.flatMap(leg => leg.steps || []) || [];
  if (!steps.length || steps.some(s => !s.maneuver || !validCoordinate({lng:s.maneuver.location?.[0],lat:s.maneuver.location?.[1]}))) throw new Error('Faltan las indicaciones del recorrido.');
  return { coordinates, distance: raw.distance, steps: steps.map(s => ({ name: String(s.name || '').slice(0, 200), type: s.maneuver.type, modifier: s.maneuver.modifier, along: nearestOnRoute({lng:s.maneuver.location[0],lat:s.maneuver.location[1]}, coordinates).along })) };
}

export function instruction(step) {
  if (step.type === 'arrive') return 'Llegá al final del recorrido trazado';
  const way = step.name ? ` por ${step.name}` : '';
  const modifiers = { left: 'a la izquierda', right: 'a la derecha', 'slight left': 'levemente a la izquierda', 'slight right': 'levemente a la derecha', 'sharp left': 'hacia la izquierda', 'sharp right': 'hacia la derecha', 'uturn': 'y regresá' };
  if (['roundabout','rotary','roundabout turn'].includes(step.type)) return `Seguí el recorrido por la rotonda${way}`;
  if (modifiers[step.modifier]) return `Girá ${modifiers[step.modifier]}${way}`;
  return `Seguí${way || ' el recorrido marcado'}`;
}
