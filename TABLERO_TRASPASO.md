# Mi Tablero — traspaso

## Qué existe
- **Tablero (el que se usa):** https://claude.ai/artifact/E4qZZG4D5jYK85Krv4WyHW — privado, solo el dueño lo lee y escribe.
- **Archivo fuente:** `tablero/mi-tablero.html` (publicar siempre este mismo archivo para no cambiar el link).
- **Fuente de verdad:** el registro propio del tablero (colección `items` + `ajustes/general`). Se escribe directo desde la página. No hay hoja de cálculo.
- **Viejo, para borrar si el dueño confirma:** tablero tipo Dashboard https://claude.ai/artifact/SgXX8BWzG2rXP3jvmtfdEm y la hoja de Drive «Mi Tablero — registro». Fue un error: se decidió sin preguntar.

## Cómo se guarda cada cosa (`items`)
tipo · titulo · estado · fecha · con_quien · notas · que_sigue · horas · creado · actualizado · terminado · acuerdosEnviados
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
| 10 | Estilo graffiti NY 90: pared, tags, contornos, goteos, stickers HELLO, flecha | 🟡 aplicado, falta que el dueño lo revise |

«Probado» = prueba automática en navegador con un registro de prueba, en compu y celular (390 px), modo claro y oscuro, 0 errores, abre en <1 s.
Falta: prueba del dueño con su cuenta en el tablero publicado.

## Reglas
- El diseño nunca cambia qué datos se muestran ni de dónde salen.
- No se decide la fuente de un dato sin preguntarle al dueño.
- Lo terminado no se borra: queda en la pestaña Listo.
