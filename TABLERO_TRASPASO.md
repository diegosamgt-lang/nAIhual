# Curtis — traspaso

## Qué existe
- **Tablero:** https://claude.ai/artifact/E4qZZG4D5jYK85Krv4WyHW — privado, solo el dueño lo lee y escribe.
- **Archivo fuente:** `tablero/curtis.html` (publicar siempre este mismo archivo para no cambiar el link).
- **Fuente de verdad:** el registro propio del tablero. Se escribe directo desde la página.
- **Conectores que usa la página (con la cuenta del dueño):** Google Drive (`create_file`, `search_files`, `update_file` para mover, `copy_file` para recopilar), Google Calendar (`list_events`, solo lectura), Zoho Books (`list_contacts`, `create_estimate`), Claude (`sample` con herramientas). Librería jsPDF 2.5.1 (cdnjs) para el PDF de links.
- **Partes y circuitos:** ver `CURTIS_PARTES.md` (fuente principal de estado).
- **Zoho:** organización «Creatif» `914134862`, moneda GTQ. Ojo: en Zoho aparece la prueba PREMIUM vencida; crear cotizaciones puede fallar hasta que se active un plan.
- **Limpieza hecha:** la hoja de Drive «Mi Tablero — registro» está en la papelera (se recupera 30 días). El tablero tipo Dashboard ya no existía.

## Datos
- `items/*`: tipo (tarea | reunion | bitacora | meta-mes | meta-año) · titulo · estado (por hacer, en proceso, esperando, listo) · fecha (AAAA-MM-DD; meta-mes AAAA-MM; meta-año AAAA) · proyecto · seccion · prioridad (''|alta) · con_quien · notas · que_sigue · horas · subtareas[{id,texto,hecho}] · minutosFoco · chat[{rol,texto,at}] (máx 30) · acuerdosEnviados · creado · actualizado · terminado
- `proyectos/*`: nombre · icono · color · cliente · entrega · estado (activo|pausa|terminado) · descripcion · driveUrl · driveFolderId · secciones[{id,nombre}] · cotizaciones[{numero,id,total,fecha,cliente}] · chat
- `ajustes/general`: horasMin · plantillaSecciones · plantillaCarpetas · zohoOrg
- `resumen/dia`, `frase/dia`: {fecha, texto} por día
- `etiquetas/*`: nombre · color · icono
- `memoria/*`: tipo (precio|tiempo|horario|error|mejora|motivacion|pasos|cliente|otro) · texto · origen (auto|curtis|yo) · fecha
- `curtis/chat`: chat general
- `ilustraciones/*`: titulo · thumb (asset) · driveId · driveUrl · archivo · ancho · alto · tema · anio · notas · estado
- proyectos además: ilustraciones[ids] · licencia{producto,n,exclusividad,duracion,territorio,tiraje,modelo,base,diseno,disenoMonto,total,fecha}
- items reunión además: gcalId (evento de Google Calendar)
- ajustes además: firma · plantillaLicencia · ilusFolderId
- proyectos además: categoria · precio · etiquetas · entregado · entregaUrl · entregaFolderId
- ajustes además: plantillaEntrega · checklistEntrega · plantillasCat

## Cómo está armado (ideas tomadas)
- **Asana:** Mis tareas por fecha (De días anteriores / Hoy / Esta semana / Más adelante / Sin fecha / Listas), proyectos con secciones, vista Lista y Tablero, panel de detalle con subtareas.
- **Notion:** proyectos en galería con ícono y color de portada, propiedades editables, notas libres, plantillas (secciones y carpetas).
- **TDAH:** resumen primero; «Ahora» muestra una sola cosa; reloj de foco 15/25/45 que guarda el tiempo dedicado; anotar sin decidir dónde (queda para hoy); «Pasar todo a hoy» sin culpa; pasos chicos; festejo al terminar; colores suaves; todo se guarda solo.

## Circuitos (prueba automática v3: 34 de 34 ✅ con conectores simulados)
| # | Circuito | Estado |
|---|---|---|
| 1 | + anota tarea con fecha de hoy → aparece en Ahora y Hoy | ✅ |
| 2 | Proyecto nuevo con secciones de plantilla; nombre, cliente, entrega, estado, color, ícono, notas editables | ✅ |
| 3 | Secciones: renombrar, agregar, borrar (las tareas se mueven, no se borran) | ✅ |
| 4 | Lista y Tablero (arrastrar entre columnas) en proyecto y en Mis tareas | ✅ |
| 5 | Detalle de tarea: todo editable y se guarda solo; pasos chicos | ✅ |
| 6 | Claude en tarea y en proyecto: agrega tareas y pasos | ✅ simulado |
| 7 | Claude o botón: carpetas de entrega en Drive (pide permiso) y guarda el link | ✅ simulado · ❓ falta prueba real |
| 8 | Cotización en Zoho en borrador (pide permiso, no la envía) y queda en el proyecto | ✅ simulado · ❓ falta prueba real (prueba de Zoho vencida) |
| 9 | Reunión → acuerdos a tareas (una sola vez) | ✅ |
| 10 | Bitácora con horas → suma contra el mínimo | ✅ |
| 11 | Metas con mes/año actual | ✅ |
| 12 | Foco con reloj | ✅ |
| 13 | Resumen local siempre al día + resumen de Claude guardado por día | ✅ |
| 14 | Borrar con confirmación; Esc cierra | ✅ |
| 15 | Celular sin scroll lateral en las 5 vistas; modo oscuro | ✅ |

## Reglas
- No se decide la fuente de un dato sin preguntarle al dueño.
- Nada se crea en Drive o Zoho sin que el dueño apruebe en la ventana de permiso.
- Lo terminado no se borra.
- Probar antes de publicar; auditar el código antes de entregar.

## Historial
- v1: escritura directa, estilo graffiti saturado.
- v2: diseño sobrio, guía, chat con Claude por tarea.
- v3: rehecho como Asana + Notion pensado para TDAH. Resumen estético primero, proyectos con secciones y tablero, todo editable con guardado automático, foco, Claude con herramientas (tareas, pasos, Drive, Zoho). Errores encontrados en la auditoría y corregidos: secciones y menú que salían como texto roto, pasos que se pisaban al agregar varios seguidos, panel que no abría al crear reunión/bitácora, Esc que no cerraba avisos, resumen que redibujaba toda la página.
- v4: Curtis (ver CURTIS_PARTES.md).
- v5: ardilla, Calendar, ilustraciones y licencias (ver CURTIS_PARTES.md).
