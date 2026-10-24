/* nAIhual · configuración de esta copia de la app (se edita aquí, no en el programa). */
window.NAIHUAL_CONFIG = {
  // "vista_previa" = solo para el fundador: muestra todo, también lo que está por verificar,
  //                  con la vista interna del equipo y con Claude respondiendo dentro del visor de Claude.
  // "publica"      = para visitantes: solo lo verificado, sin vista interna y sin Claude.
  modo: 'vista_previa',
  // Fecha del lanzamiento público (AAAA-MM-DD). Vacía = sin fecha. No se inventa.
  // La ventana de 3 meses de Aliados Fundadores solo corre en modo "publica" y con esta fecha ya pasada.
  fecha_lanzamiento: '',
  // true = muestra la tarjeta y la página de Aliados Fundadores (propuesta piloto).
  mostrar_aliados: true,
  // true = en vista previa, dentro del visor de Claude, Claude responde las preguntas libres (con la cuenta de quien abre la página).
  claude_responde: true
};
