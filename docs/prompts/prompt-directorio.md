# Prompts · inventario (Gemini) y libretas (NotebookLM)

**Más fácil:** la página con un prompt por categoría y botón «Copiar» está en el visor privado (claude.ai/artifact/3UpapUFaV6uFu8UDjLNFuw) y en `docs/prompts/prompts-gemini.html`.

Versión del 7-nov-2026. Lo que te devuelvan, pasáselo a Claude: «cargá el directorio» (inventario) o pegalo en «Memoria» de la beta (libretas).

## Orden y clasificación
1. **Una categoría por vez, máximo 20 lugares** (por defecto).
2. **Orden:** hospedaje → comida → cafés → pan y postres → de noche → transporte → mercados y comedores → artesanos y talleres → miradores y naturaleza → fiestas y eventos (con fecha).
3. **Etiqueta `origen`:** lo que trae Gemini va `ia`. Lo que agregás vos, `diego`. En la app, «Registro» los separa: «IA · 20» y «Diego».
4. **Columnas tuyas para curar** (las llenás vos, no Gemini): `para` (local, turista, mochilero, separados por coma) · `confirmo` (fecha en que confirmaste que existe y es así) · `estado` (activo, reserva o fuera).

## Instrucciones fijas de Gemini (10-nov-2026)

Texto completo en `docs/prompts/instrucciones-gemini.txt` (y con botón «Copiar» en la página de prompts). Es la versión de nAIhual de las instrucciones que Diego tenía en Gemini: sin calificaciones, reseñas, horarios ni precios; máximo 20 por categoría; con bitácora de búsqueda y «Casos aparte».

## Prompt para Gemini (inventario)

> Armá un inventario de **[categoría]** en Antigua Guatemala para nAIhual, una guía de turismo consciente. **Máximo 20 lugares**, empezando por los de tradición y familiares.
>
> Reglas:
> - Solo lugares que aparezcan en una fuente pública que puedas citar (Google Maps, la web o las redes del negocio, guías de viaje, medios). No inventes nada.
> - **Sin calificaciones, estrellas ni número de reseñas.** Sin copiar reseñas.
> - Sin horarios, sin precios y sin datos de personas (nombres de empleados, teléfonos personales).
> - Sin significados mayas ni ceremonias.
> - El «contexto» son datos, no opiniones: de quién es (familiar, nacional, cadena, extranjero), desde cuándo y qué lo hace distinto, según la fuente.
> - Incluí también cadenas, marcadas como cadena: sirven de contexto.
> - `maps_url`: el enlace del lugar en Google Maps (Compartir → Copiar enlace), no un enlace de búsqueda.
> - Si un dato no está en la fuente, dejalo vacío.
>
> Devolvé una tabla (o una línea JSON por lugar) con estas columnas, en este orden:
> `nombre · categoria · tipo · zona · direccion · maps_url · contexto · redes_o_web · redes_actividad · fuente · fuente_url · fecha_consulta (AAAA-MM-DD) · origen (siempre «ia») · para (vacío) · confirmo (vacío) · estado (vacío)`
>
> `categoria` es una de: hospedaje, comida, cafe, postres, noche, transporte, mercado, artesania, mirador, evento.

## Prompt para NotebookLM (libretas por categoría)

Para que nAIhual aprenda siempre en el mismo orden: **una libreta por categoría**, con el mismo nombre que en la Memoria de la app (hospedaje, comida, cafés, pan y postres, de noche, parques, monumentos, historia y cultura, consejos, transporte, fiestas y eventos, otros).

> Con las fuentes de este cuaderno, armá un informe de **[categoría]** para nAIhual (Antigua Guatemala).
> - Solo lo que dicen las fuentes; al final de cada párrafo, entre paréntesis, la fuente.
> - Párrafos cortos, uno por tema o por lugar, separados por una línea en blanco.
> - Sin opiniones como verdad, sin calificaciones, sin precios ni horarios.
> - Lo maya o cultural, marcado con * (falta que lo valide un tata).
> - Al principio, una línea: «Categoría: [categoría] · fecha: [hoy]».

Lo que te devuelva, pegalo en **Beta → Memoria**, eligiendo la misma categoría.
