/* nAIhual · configuración de esta copia de la app (se edita aquí, no en el programa). */
window.NAIHUAL_CONFIG = {
  // "vista_previa" = hoy: muestra todo lo cargado y responde la IA. El visitante ve la app limpia;
  //                  el agente entra con «Soy agente» y ve el taller y la vista interna.
  // "publica"      = solo lo verificado, sin IA, sin buzón y sin taller.
  modo: 'vista_previa',
  // true = en vista previa, dentro del visor de Claude, Claude responde las preguntas libres (con la cuenta de quien abre la página).
  claude_responde: true,
  // true = en vista previa se leen las publicaciones y fotos del buzón, y los agentes pueden publicar y anotar.
  beta: true,
  // Mapas de Diego hechos en Google My Maps (compartidos «cualquiera con el enlace»). Salen en «Rutas».
  // Ejemplo: { titulo: 'Cafés de Antigua', url: 'https://www.google.com/maps/d/edit?mid=...' }
  mapas: [],
  // Dirección del servidor de la IA (Gemini) para cuando la app vive afuera del visor de Claude (servidor/gemini-worker.js).
  // Vacío = sin IA afuera del visor (contestan las reglas fijas). Si cambia, cambiá también la dirección en la política de seguridad de app/index.html (CSP).
  servidor_ia: 'https://naihual-ia.diegosamgt.workers.dev'
};
