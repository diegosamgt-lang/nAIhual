/* nAIhual · registro de fuentes de conocimiento.
   Cada fuente: id fijo, título, URL o archivo, fecha, responsable, tema, versión y estado de revisión.
   estado: "borrador" | "pendiente de validación cultural" | "pendiente de fuente oficial" | "revisada" | "retirada".
   Solo una fuente "revisada" respalda un dato como confirmado. Los archivos internos no se publican. */
window.NAIHUAL_FUENTES = [
  { id: 'consolidado', titulo: 'Documento Consolidado del proyecto y la cosmovisión (PDF del fundador)', url_o_archivo: 'Archivo interno del fundador (no se publica)',
    fecha: '', responsable: 'Fundador', tema: 'Cosmovisión maya, calendario y los 20 nawales', version: '', estado: 'pendiente de validación cultural' },
  { id: 'notebooklm-cargadores', titulo: 'Respuesta de NotebookLM sobre los cargadores del año', url_o_archivo: 'Archivo interno del proyecto (no se publica)',
    fecha: '2026-10', responsable: 'Fundador (cuaderno de NotebookLM); resumen de Claude', tema: "Cargadores del año: No'j, Iq', Kej, E'", version: '', estado: 'pendiente de validación cultural' }
];
