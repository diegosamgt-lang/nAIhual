/* nAIhual · configuración de esta copia de la app (se edita aquí, no en el programa). */
window.NAIHUAL_CONFIG = {
  // "vista_previa" = para Diego y quien pruebe la beta: muestra todo lo cargado, la vista interna del equipo,
  //                  la beta y Claude respondiendo dentro del visor de Claude.
  // "publica"      = para visitantes: solo lo verificado, sin vista interna, sin beta y sin Claude.
  modo: 'vista_previa',
  // true = en vista previa, dentro del visor de Claude, Claude responde las preguntas libres (con la cuenta de quien abre la página).
  claude_responde: true,
  // true = en vista previa se puede anotar «me gustó», «dato mal», notas, visitas y lugares nuevos (beta).
  beta: true,
  // Mapas de Diego hechos en Google My Maps (compartidos «cualquiera con el enlace»). Salen en «Rutas».
  // Ejemplo: { titulo: 'Cafés de Antigua', url: 'https://www.google.com/maps/d/edit?mid=...' }
  mapas: [],
  // Dirección del servidor de la IA (Gemini) para cuando la app vive afuera del visor de Claude (servidor/gemini-worker.js).
  // Vacío = sin IA afuera del visor (contestan las reglas fijas).
  servidor_ia: 'https://naihual-ia.diegosamgt.workers.dev'
};
