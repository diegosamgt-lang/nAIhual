# Mi Tablero — traspaso

## Qué existe
- **Tablero:** https://claude.ai/artifact/SgXX8BWzG2rXP3jvmtfdEm (privado)
- **Fuente de verdad:** hoja de Google «Mi Tablero — registro» en Drive
  https://docs.google.com/spreadsheets/d/1_SsCYLfQgNdrUaAgV7drgXE9H3HwiLWr1BDt_MtFByQ/edit
- El tablero lee la hoja en vivo cada vez que se abre o se refresca. No guarda copia.

## Columnas de la hoja
tipo · que · estado · fecha · con_quien · notas · que_sigue · horas
- tipo: meta-mes, meta-año, tarea, proyecto, reunion, bitacora
- estado: por hacer, en proceso, esperando, listo
- fecha: año-mes-día (también acepta día/mes/año)

## Circuitos
| # | Circuito | Estado |
|---|---|---|
| 1 | Anoto una tarea o proyecto → aparece en «Qué sigue» | 🟡 |
| 2 | Pongo algo en «esperando» → aparece en «Trabado» | 🟡 |
| 3 | Anoto una reunión con acuerdos → queda en «Reuniones» | 🟡 |
| 4 | Anoto una bitácora NIHR con horas → suma en «Horas este mes» | 🟡 |
| 5 | Metas del mes y del año visibles | 🟡 |
| 6 | Estilo graffiti NY 90 (Fase 10) | ⬜ |

## Lo que falta saber
- Mínimo de horas NIHR por mes.
- Si Google Sheets cambia el formato de las fechas al escribirlas.
- Si las reuniones también deben salir de Google Calendar o Zoom.

## Reglas
- El diseño nunca cambia qué datos se muestran ni de dónde salen.
- No duplicar datos: todo se anota en la hoja.
