# nAIhual · Prototipo 1 — Guardianes

Fecha: 18-oct-2026. Un solo archivo: `index.html`. Se abre directo en el navegador.
Basado en `docs/CONCEPTO.md`. El Prototipo 0 sigue intacto en `prototipo-0/`.

## Qué tiene
- Pantalla 1: el chat. Saluda el guardián de turno.
- Los 4 guardianes se turnan en orden fijo: B'atz' → Kej → Ajpu → No'j. Cada pregunta la contesta el siguiente.
- Cada uno responde con su tono y su propia recomendación. Ej. «Quiero un café»:
  - B'atz': Artista de Café.
  - Kej: tres cafés cercanos.
  - Ajpu: uno solo, Coffea.
  - No'j: Siena Luz.
- El turista puede pedir uno: tocando su ícono arriba, o escribiendo su nombre («quiero hablar con No'j»).
- 7 preguntas listas: por dónde empiezo, 3 horas, café, dónde como, plan de un día, cultura maya, respeto.
- Reglas fijas, sin IA y sin costo. Solo usa lugares con dirección verificada.
- Si no hay datos (naturaleza, talleres, mercados, aventura, seguridad), el guardián lo dice y no inventa.
- ES / EN, Google Maps por lugar y ruta completa a pie, panel «¿Quiénes son los guardianes?».

## Marcas
- `*` = cultural, por confirmar con un Ajq'ij.
- `†` = histórico, por confirmar con fuente oficial.

## Propuestas de Claude, por corregir
- Qué lugar recomienda cada guardián en cada pregunta.
- Las frases de cada guardián.
- Las frases de presentación: «Soy Kej, el equilibrio. Yo te ordeno el camino.», etc.
- Arte neutro y provisional: cada guardián tiene un color solo para distinguirlo.

## Estado
- ✅ Probado en Chromium a 390 px: carga en menos de 1 s. Probadas 10 preguntas: el turno rota bien y pedir un guardián funciona. También ES/EN, modo oscuro y panel. Sin errores ni scroll de lado.
- 🟡 Sin probar en un celular real ni con otra persona.
