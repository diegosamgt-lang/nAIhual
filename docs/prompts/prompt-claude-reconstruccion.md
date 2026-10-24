# CONSTRUYE · nAIhual 2.0 — reconstrucción total en 4 ciclos

Claude: esta instrucción autoriza reconstruir la app por completo, ejecutar pruebas, actualizar el visor privado de Claude (artifact «nAIhual»: https://claude.ai/artifact/NJt1c96dAwFtpTki932Ded) y guardar en la rama de trabajo `claude/awesome-carson-sz5k9i` al final de cada ciclo. No autoriza hacer pública la app, compartir enlaces, abrir pull requests, contratar servicios, generar gastos ni contactar personas o negocios.

## 0. Antes de empezar

1. Leé completos `CLAUDE.md`, `docs/nAIhual.md`, `1_PROCESO.md`, `2_REGLAS.md`, `4_LECCIONES.md`, `docs/fuentes/notebooklm-contexto-completo-2026-10.md` y `docs/prompts/prompt-gemini-nAIhual.md`. Este último tiene el contexto completo, las reglas, el negocio y los datos. Vale también para vos, salvo donde este prompt diga otra cosa.
2. Revisá la app actual (`app/index.html`, `app/data/`) y el visor. Guardá una copia en `versiones/app-1.2/` antes de tocar nada.
3. Corré `python3 pruebas/prueba_piloto.py` y anotá el resultado de partida.

**Qué se conserva (decisiones aprobadas):**
- Los 4 guardianes: **No'j, Iq', Kej, E'**, en ese orden. Empieza No'j. Turno: el guardián sigue hasta que la persona pide otro; «otro» pasa al siguiente; nombrarlo o tocar su ícono lo trae. No se tocan.
- El recorrido piloto: «Quiero un café» → hasta 3 cafés publicados con fuente y fecha → «Cómo llegar» con el enlace universal de Google Maps.
- Los datos y sus reglas: catálogo, fuentes y configuración en `app/data/`; publicado solo con fuente, fecha y quién verificó; \* cultural y † histórico pendientes; patrocinado siempre marcado y sin cambiar el orden.
- Aliados Fundadores (propuesta piloto pendiente de aprobación), las 4 etapas de ingreso como hipótesis, el ciclo de aprendizaje y la arquitectura Gemini/NotebookLM: el contenido se conserva y se rediseña.
- Claude responde en el visor privado (`claude_responde`), con sus reglas y su filtro de lugares no publicados.
- La memoria de turno, ES/EN, ♥ guardado solo en el teléfono, modo claro y oscuro.

**Qué se reconstruye desde cero:** toda la experiencia del visitante (pantallas, navegación, textos, diseño visual) y la presentación de la vista interna.

## 1. El problema, en palabras del fundador

«Siento que todo lo que pregunto vs lo que me responde es muy amateur, muy principiante, demasiado IA… parece un chatbot. "Tips para caminar con respeto"… malísimo. No veo la parte gráfica, veo demasiado texto, no veo rutas, algo que resalte o que sea atractivo. Necesito algo mucho mejor.»

**Diagnóstico que tenés que resolver:**
- Se diseñó para cumplir reglas, no para el viajero. El visitante ve el «detrás de cámaras»: «en revisión», asteriscos, «reglas fijas, sin IA», avisos legales.
- Los guardianes suenan a asistente genérico y a sermón.
- Todo es texto en burbujas: no hay fotos, mapa ni rutas visibles, y los íconos son letras en círculos.
- Con todos los lugares en borrador, el modo visitante queda vacío. Así no se puede juzgar el diseño.

## 2. Decisiones de reconstrucción (ya tomadas; aplicalas)

1. **Dos modos, un interruptor en `config.js`:**
   - **Vista previa** (visor privado): muestra todo, también los borradores, con una marca discreta «por verificar», para diseñar con contenido real. Incluye la vista interna y «Claude responde».
   - **Pública**: solo lo publicado, sin marcas de borrador, sin vista interna y sin Claude.
   Las pruebas cubren los dos modos.
2. **La verificación se ve como un sello, no como un aviso:** «Verificado · fecha · fuente» en la ficha, que se abre al tocarlo. Lo cultural pendiente se avisa con un ⓘ por tarjeta. No uses asteriscos dentro de las frases ni notas al pie repetidas.
3. **Lo visual va primero:** cada pantalla tiene una imagen, un mapa o una ilustración que la protagoniza. El texto acompaña.
4. **Mapa esquemático propio de Antigua:** cuadrícula de calles y avenidas, con las paradas de cada ruta ubicadas por su dirección y numeradas, y la ruta dibujada. Va marcado «esquema, no a escala» y tiene el botón «Abrir ruta a pie en Google Maps». ❓ Confirmá la orientación de la cuadrícula antes de dibujar. Avenidas norte-sur, numeradas desde el oriente; calles oriente-poniente, numeradas desde el norte; Parque Central entre la 4a y la 5a Calle y la 4a y la 5a Avenida. Si no podés confirmarla, decilo.
5. **Fotos:** solo del fundador o con licencia libre y crédito visible (monumentos públicos). Nunca fotos de negocios sin permiso. Mientras no haya, espacios diseñados y marcados como provisionales. Pedile al fundador que te mande fotos en el chat; van en `app/img/` y en los archivos del visor.
6. **Iconografía:** una sola familia lineal (estilo Lucide, en SVG dentro de la página). Nada de glifos mayas, patrones de güipil ni símbolos ceremoniales. La silueta del Volcán de Agua sí se puede usar.
7. **Guardianes:** dejá espacio para el arte final del fundador. Mientras, un retrato abstracto con su color por rumbo \*, nunca una letra sola.
8. **Navegación propuesta:** Inicio · Rutas (mapa) · Guía (chat) · Guardados. Explorar, nawales, guardianes y Aliados entran desde Inicio. Si encontrás algo mejor, justificalo en una línea.
9. **Textos nuevos:** cortos, concretos, de vos, con algo que se pueda ver o hacer. Sin sermones, sin lenguaje de sistema y sin «¿En qué te ayudo?». Todo texto nuevo es una propuesta y se lista para que el fundador lo apruebe. Ejemplos:
   - «¿Cómo me porto con respeto?» → «Costumbres de aquí»
   - «Caminá con respeto: estas calles son casa de mucha gente» → eliminar
   - «Soy No'j\*. Yo te cuento el porqué.» → etiqueta «No'j · te cuenta el porqué», sin autopresentación
   - «Esa selección está en revisión: todavía no tengo lugares con fuente…» → «Estoy probando los cafés uno por uno. Mientras, esta ruta ya está lista:», solo si hay algo listo que ofrecer
10. **Emergencias:** el botón existe en el diseño y muestra «Pendiente de números oficiales» en la vista previa. En la versión pública no aparece hasta que el fundador confirme los números con fuente oficial.

## 3. Los 4 ciclos

Cada ciclo termina con: pruebas corriendo, visor actualizado, guardado en la rama y un reporte de 5 líneas como máximo al fundador (✅ 🟡 ❓). Pasá al siguiente ciclo sin esperar, salvo que encuentres una decisión que solo el fundador puede tomar. En ese caso, una pregunta de opción múltiple y seguís con lo demás.

### Ciclo 1 · Construcción estructural
**Objetivo:** la app nueva funciona de punta a punta, aunque todavía no esté pulida.
- Nueva estructura de pantallas y navegación (punto 2.8).
- Los dos modos (2.1) desde `config.js`.
- Datos solo desde `app/data/`. Nada de datos de lugares escritos dentro del programa.
- Guardianes, turno, chat con reglas fijas y Claude en vista previa, «Quiero un café», «Cómo llegar», rutas, ♥ y plan, ES/EN.
- Sistema de tokens (color, tipo, espacio, forma, movimiento) en un solo lugar.
- Pruebas automáticas nuevas para todo lo anterior, en los dos modos.
**Sale cuando:** todas las pruebas pasan, sin errores en consola, a 390 px sin desplazamiento horizontal.

### Ciclo 2 · Flujo, arquitectura y validación
**Objetivo:** que un turista entienda y use la app sin ayuda.
- Recorré como turista los 5 recorridos: llegar sin saber nada · «Quiero un café» · elegir una ruta y abrirla en Maps · preguntar algo libre · guardar y ver el plan. Anotá cada fricción y corregila.
- Revisá cada enlace: cada «Cómo llegar» y cada «Abrir ruta» se arma bien. Sin dirección, no hay botón.
- Revisá la arquitectura: capas separadas, proveedor intercambiable, registro de cada respuesta y filtros de seguridad de Claude.
- Validá que en modo público no se cuele ningún borrador, ni por nombre, ni en el chat.
- Jerarquía de lectura: en cada pantalla, qué se ve primero, segundo y tercero.
**Sale cuando:** los 5 recorridos se completan en 3 toques o menos desde Inicio (el café, en 1) y no queda ninguna fricción anotada sin resolver o justificar.

### Ciclo 3 · Dirección visual
**Objetivo:** que se vea como una app de viaje premium y propia de Antigua, no como un chat.
- Carga el skill `artifact-design` antes de diseñar.
- Un par tipográfico con carácter, paleta de piedra y cal más los 4 colores de los guardianes, en claro y oscuro.
- Mapa esquemático con rutas animadas al entrar. Fotos o espacios provisionales con buen recorte. Íconos lineales.
- Tarjetas con imagen protagonista, sello de verificación, ⓘ cultural y etiqueta «Patrocinado» cuando corresponda.
- Efectos simples: entrada suave, transición entre pantallas, la ruta que se dibuja. Respetá «reducir movimiento».
- Estados vacíos diseñados, no solo texto.
**Sale cuando:** capturas a 390 px de cada pantalla, en claro y oscuro, revisadas a ojo y comparadas con la versión 1.2: cada pantalla tiene un elemento visual protagonista y menos texto que antes.

### Ciclo 4 · Auditoría y corrección
**Objetivo:** encontrar y corregir errores, incoherencias y decisiones flojas.
- Revisá cada texto contra las reglas: nada inventado, nada de sermones, nada de lenguaje de sistema, nada de chatbot.
- Revisá cada dato: ¿viene del catálogo? ¿lleva su marca? ¿algún borrador quedó a la vista en modo público?
- Revisá las decisiones vagas o débiles («propuesta», «por definir» sin dueño) y convertí cada una en una pregunta concreta para el fundador o en una decisión justificada.
- Accesibilidad básica: contraste AA, nombres de controles, teclado, tamaños táctiles. No digas que hiciste una auditoría completa si no la hiciste.
- Rendimiento: la app carga rápido sin servicios externos salvo la tipografía.
- Corré todas las pruebas y corregí lo que falle. Repetí este ciclo una vez más si encontraste más de 5 problemas.
**Sale cuando:** las pruebas pasan y la lista de problemas encontrados queda en cero o justificada.

## 4. Entrega final

1. App 2.0 en el visor privado y guardada en la rama.
2. Actualizá `docs/nAIhual.md`: producto, decisiones, historial. No crees otros documentos vivos.
3. Reporte al fundador, corto y sin palabras técnicas:
   - Qué cambió, con 3 capturas.
   - Pruebas: comando y resultado, separando lo automático, lo revisado a ojo y lo pendiente de una persona (celular real, persona externa, Ajq'ij).
   - Textos nuevos para aprobar.
   - Lo que necesitás de él, en orden: fotos, arte de los guardianes, hasta 3 cafés verificados, alojamiento y canal de errores.
4. No marques el piloto como lanzado ni validado.
