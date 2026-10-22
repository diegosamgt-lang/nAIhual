# Curtis — traspaso

> Actualizado: 2026-10-22 · versión 8. El estado de cada parte y la bitácora están en `CURTIS_PARTES.md`.

## Qué existe
- **Panel:** https://claude.ai/artifact/E4qZZG4D5jYK85Krv4WyHW — privado, solo el dueño lo lee y escribe.
- **Archivo fuente:** `tablero/curtis.html`. Publicar siempre este mismo archivo en ese mismo link.
- **Fuente de verdad:** el registro propio del panel (se escribe directo desde la página).
- **Capacidades de la página:** registro (`db`), Claude (`sample`, con herramientas e imágenes), conectores del dueño (`mcp`), almacén de archivos (`assets`, miniaturas y archivos sin Drive), permisos (`permissions`).
- **Conectores que usa (con la cuenta del dueño):**
  - Google Drive: `create_file` (carpetas y archivos), `search_files`, `update_file` (mover), `copy_file` (recopilar).
  - Google Calendar: `list_calendars` y `list_events` (por cada calendario activo), solo lectura. Las horas llegan en hora universal; el día se calcula en hora de Guatemala.
  - Zoho Books: `list_contacts`, `create_estimate` (borrador, con descuento), `create_invoice` (borrador), `list_invoices` (leer estado y saldo).
- **Librería:** jsPDF 2.5.1 (cdnjs) para el PDF de links, la propuesta de licencia y la cotización.
- **Zoho:** organización «Creatif» `914134862`, moneda GTQ. La prueba PREMIUM está vencida: crear cotizaciones puede fallar hasta activar un plan.
- **Carpetas que Curtis crea en Drive cuando hace falta:** «Curtis · Ilustraciones», «Curtis · Bandeja», «Curtis · Reuniones / AAAA-MM-DD — cita» y la de cada proyecto.

## Datos
- `items/*`: tipo (tarea | reunion | bitacora | meta-mes | meta-año) · titulo · estado (por hacer, en proceso, esperando, listo) · fecha (AAAA-MM-DD; meta-mes AAAA-MM; meta-año AAAA) · proyecto · seccion · prioridad (''|alta) · etiquetas · con_quien · notas · que_sigue · horas · subtareas[{id,texto,hecho}] · minutosFoco · chat[{rol,texto,at}] (máx 30) · acuerdosEnviados · gcalId (cita de Google Calendar) · padre (tarea dentro de otra) · reunionId (tarea → su reunión) · reunión: tareaId · notasHtml · carpetaId · carpetaUrl · carpetaNombre · adjuntos[{nombre,driveUrl,asset,thumb}] · enviados[pendientes ya pasados a tareas] · creado · actualizado · terminado
- `proyectos/*`: area · clienteId · nombre · icono · color · cliente · categoria · precio (cobro final) · entrega · estado (activo|pausa|terminado) · etiquetas · descripcion · driveUrl · driveFolderId · secciones[{id,nombre}] · cotizaciones[{numero,id,total,fecha,cliente}] (las de Zoho) · chat · ilustraciones[ids] · licencia{producto,n,exclusividad,duracion,territorio,tiraje,modelo,base,diseno,disenoMonto,mayorista,regaliaPct,fx,total,unico,fecha} · entregado · entregaUrl · entregaFolderId
- `servicios/*` (v6): titulo · subtitulo · grupo · precio · unidad · formato · tiempo · descripcion · creado · actualizado
- `cotizaciones/*` (v6): titulo · cliente · proyecto · fecha · validez (días) · contexto (de qué se trata) · lineas[{id, tipo: titulo|subtitulo|servicio|nota|descuento, texto, servicioId, nombre, cantidad, precio, unidad, formato, descripcion, modo: monto|pct, valor}] · notas · estado (borrador|enviada|aceptada|rechazada) · total · pdfUrl · creado · actualizado
- `areas/*` (v7): nombre · icono · color · descripcion · cliente · creado · actualizado
- `clientes/*` (v7): nombre · empresa · contacto · correo · telefono · notas · zohoId
- `facturas/*` (v7): numero (F-001…) · concepto · cotizacion · proyecto · cliente · clienteId · fecha · vence · total · moneda · estado (pendiente|pagada|anulada) · pagadoEl · saldo · parte (total|anticipo) · zohoId · zohoNumero · zohoEstado · fel (número FEL de la SAT, v8) · notas
- `suscripciones/*` (v7): nombre · monto · moneda (Q|US$) · frecuencia (mensual|anual) · categoria · desde · activa
- `movimientos/*` (v7): tipo (gasto|ingreso) · concepto · monto · moneda · fecha · categoria · proyecto
- `archivos/*` (v6): reunion (v7) · nombre · tipo · tamano · proyecto ('' = Bandeja) · driveId · driveUrl · asset (si se guardó en Curtis) · thumb · fecha · creado
- `ilustraciones/*`: titulo · thumb · driveId · driveUrl · archivo · ancho · alto · tema · anio · notas · estado
- `etiquetas/*`: nombre · color · icono
- `memoria/*`: tipo (precio|tiempo|horario|error|mejora|motivacion|pasos|cliente|otro) · texto · origen (auto|curtis|yo) · fecha · proyecto
- `ajustes/general`: horasMin · plantillaSecciones · plantillaCarpetas · plantillaEntrega · plantillaLicencia · checklistEntrega · plantillasCat · firma · zohoOrg · ilusFolderId · bandejaFolderId (v6) · factoresLicencia (v6: multiplicadores «de siempre») · tipoCambio (v7) · calendarios {id: true/false} (v8) · ultimaCopia · ultimaCopiaUrl (v8)
- `resumen/dia`, `frase/dia`: {fecha, texto}
- `curtis/chat`: chat general

## Cómo está armado
- **Asana:** Mis tareas por tiempo, proyectos con secciones, lista y tablero, panel de detalle con pasos.
- **Notion:** proyectos en galería con ícono y color, propiedades editables, notas libres, plantillas.
- **TDAH:** resumen primero; «Ahora» muestra una sola cosa; foco con reloj; anotar sin decidir dónde; pasos chicos; festejo; estacionamiento de ardillas; todo se guarda solo.
- **Precios:** catálogo una sola vez → cotizaciones que se suman solas; Curtis escribe las descripciones.
- **Licencias:** base por ilustración × cantidad × multiplicadores editables (volumen, exclusividad, duración, territorio, tiraje), con mínimo y regalía editables. Capas: valores de Curtis ← «de siempre» del dueño ← los de esa propuesta.

## Reglas
- No se decide la fuente de un dato sin preguntarle al dueño.
- Nada se crea ni se mueve en Drive o Zoho sin que el dueño apruebe en la ventana de permiso. Nunca se borran archivos de Drive.
- Google Calendar solo se lee.
- Nada se borra sin confirmación del dueño.
- Probar antes de publicar; auditar el código antes de entregar.

## Pruebas
- Automáticas en el navegador con conectores simulados: v8 124/124 y la de v4 31/31 sin regresiones.
- Real (de solo lectura, desde esta sesión): Google Calendar devuelve 5 calendarios, incluido el importado de iCloud «Diego - Disart» con sus citas. Drive `search_files` responde como el panel espera. Zoho `list_invoices` responde (todavía sin facturas).
- Falta la primera prueba real con Drive, Calendar y Zoho.

## Historial
- v1: escritura directa, estilo graffiti saturado.
- v2: diseño sobrio, guía, chat con Claude por tarea.
- v3: rehecho como Asana + Notion pensado para TDAH.
- v4: Curtis (estilo NatGeo, memoria, entregas).
- v5: ardilla, Google Calendar, ilustraciones y licencias.
- v6: Precios (catálogo y cotizaciones), multiplicadores de licencia editables, archivos, logo minimalista, frases estilo Jung.
- v7: Áreas, tareas dentro de tareas, reuniones conectadas con notas grandes, clientes, Dinero (facturas, cobros, suscripciones, gastos), jerarquía visual editorial.
- v8: simplificación (Inicio de 4 bloques, 5 pestañas en el celular, una sola forma de pasos y de cotizar), todos los calendarios de Google incluido iCloud, copia de seguridad en Drive, número FEL en facturas.
