# Mi Tablero — traspaso

## Qué existe
- **Tablero (el que se usa):** https://claude.ai/artifact/E4qZZG4D5jYK85Krv4WyHW — privado, solo el dueño lo lee y escribe.
- **Archivo fuente:** `tablero/mi-tablero.html` (publicar siempre este mismo archivo para no cambiar el link).
- **Fuente de verdad:** el registro propio del tablero (colección `items` + `ajustes/general`). Se escribe directo desde la página. No hay hoja de cálculo.
- **Viejo, para borrar si el dueño confirma:** tablero tipo Dashboard https://claude.ai/artifact/SgXX8BWzG2rXP3jvmtfdEm y la hoja de Drive «Mi Tablero — registro». Fue un error: se decidió sin preguntar.

## Cómo se guarda cada cosa (`items`)
tipo · titulo · estado · fecha · con_quien · notas · que_sigue · horas · creado · actualizado · terminado · acuerdosEnviados · chat
- chat: lista de `{rol: yo|claude, texto, at}`, máximo 30 mensajes por tarea
- tipo: tarea, proyecto, reunion, bitacora, meta-mes, meta-año
- estado: por hacer, en proceso, esperando, listo (reunión y bitácora se guardan como listo)
- `ajustes/general.horasMin` = mínimo de horas NIHR al mes

## Circuitos
| # | Circuito | Estado |
|---|---|---|
| 1 | Anoto una tarea → aparece en AHORA o en «Qué sigue» | ✅ probado |
| 2 | Empezar → queda «en proceso» | ✅ probado |
| 3 | «Me trabé» → pide a quién espero → va a «Trabado» | ✅ probado |
| 4 | ¡Listo! → sale de la fila, queda en pestaña Listo, suma en «Listo esta semana» | ✅ probado |
| 5 | Reunión con acuerdos → queda guardada; «Pasar acuerdos a tareas» crea una tarea por línea, una sola vez | ✅ probado |
| 6 | Bitácora NIHR con fecha y horas → suma contra el mínimo del mes | ✅ probado |
| 7 | Metas del mes y del año | ✅ probado |
| 8 | Proyecto con fecha vencida → sube a AHORA con etiqueta VENCIDA | ✅ probado |
| 9 | Editar y borrar (con confirmación) | ✅ probado |
| 10 | Preguntarle a Claude dentro de cada tarea → responde con contexto de la tarea y la lista; la conversación queda guardada | ✅ probado con respuesta simulada |
| 11 | Guía «Cómo funciona este tablero» arriba (se puede ocultar) | ✅ |
| 12 | Estilo v2: limpio tipo Apple, colores apagados, graffiti solo en acentos | 🟡 falta que el dueño lo revise |

«Probado» = prueba automática (28 de 28) en navegador con un registro de prueba, en compu y celular (390 px), modo claro y oscuro, 0 errores, abre en <1 s.
Falta: prueba del dueño con su cuenta en el tablero publicado.

## Reglas
- El diseño nunca cambia qué datos se muestran ni de dónde salen.
- No se decide la fuente de un dato sin preguntarle al dueño.
- Lo terminado no se borra: queda en la pestaña Listo.

## Historial
- v1: tablero con escritura directa, estilo graffiti saturado.
- v2: rediseño sobrio (pedido del dueño: «Apple con graffiti, no tan saturado»), guía de uso, chat con Claude por tarea, arreglos: fecha «mañana» mal calculada, texto «null» suelto, mayúsculas en fechas, campo de mínimo de horas que se borraba al escribir.
