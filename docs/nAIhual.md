# nAIhual — Documento único del proyecto

Actualizado: 18-oct-2026 · Este es **el único documento vivo**: concepto, estado, circuitos, fuentes, decisiones e historial. Se actualiza este mismo archivo; no se crean otros.

**Marcas**
- ✅ = lo dijo el fundador / verificado.
- 🟡 = construido, sin probar.
- ❓ = supuesto o por confirmar.
- ❌ = quitado por una orden más nueva.
- \* = cultural, por validar con un Ajq'ij.
- † = histórico, por confirmar con fuente oficial.

**Método (intocable, del fundador):** `0_PROMPT_MAESTRO.md` · `1_PROCESO.md` · `2_REGLAS.md` · `3_PREGUNTAS.md` · `4_LECCIONES.md`. Comandos: PAUSA = solo responder y anotar · CONSTRUYE = ejecutar.

---

## 1. Qué es

- ✅ Agente de IA **artesanal** turístico-cultural: un puente entre viajeros y comunidades de Guatemala.
- ✅ «Artesanal» = la información la curan personas locales antes de entrar al agente. Así no se inventa nada.
- ✅ Piloto en Antigua Guatemala; después, otras ciudades y países. Hoy ES + EN; visión: app y voz multilingüe.
- ✅ La gente y la cultura son el centro. Crear contenido viene después (15-oct).
- ✅ «nAIhual» = nahual + IA. Es el nombre propio del proyecto, no un término tradicional.
- ✅ Frase de marca: **«Viaja directo a la raíz.»** (18-oct)

**Principios** (PDF Consolidado):
- Comunidad primero, antes que las cadenas.
- Cultura sin apropiación ni folclor.
- Sostenibilidad y anti-gentrificación (❓ criterios por definir).
- Autonomía del turista: lo patrocinado siempre se marca.
- Nunca inventar lugares, horarios, precios ni significados.
- No difundir lugares naturales sensibles.

**Marca** (resumen viejo, vigente salvo lo marcado):
- Propósito: puente entre culturas, preservar lo vivo, turismo responsable.
- Misión: orientación verificada y cercana que conecta con el corazón cultural y fortalece economías locales.
- Visión: agente de referencia, en texto y voz, en varios países.
- Valores: protección, guía espiritual, integración, amor, luz, autenticidad, aceptación, tolerancia.
- ✅ Voz: **cálida y directa**, cercana, sin tono místico. Lo espiritual solo cuando se habla de cultura. Orgullosamente guatemalteca, cero venta agresiva.

## 2. Personas

| Quién | Rol |
|---|---|
| Fundador (artista) | Decide. Aporta lugares y frases con su voz. Hace el arte final. Consigue negocios fundadores y la validación cultural. |
| Red de contactos del fundador | Aportan y corrigen datos locales. |
| Ajq'ij (por contactar) | Valida lo cultural (\*). ❓ El 18-oct no se marcó como curador: falta confirmar que la regla sigue. |
| Fuentes oficiales | Validan lo histórico (†): UNESCO, Consejo Nacional para la Protección de La Antigua, Ministerio de Cultura. |
| Claude | Construye, prueba, cuida la verdad (✅🟡❓) y asesora. |
| Gemini (futuro) | Será la voz del agente con los turistas. |

## 3. Los 4 guardianes (corazón del concepto)

Nacen del resumen viejo: simbología del número 4 y las direcciones.

| Guardián | Es (valor\*) | Hace | Habla | Recomienda |
|---|---|---|---|---|
| **B'atz'** | El inicio: tejido, chispa creativa · Oriente, fuego\* | Crear | Juguetón y curioso: «¡Empecemos por algo que te vas a llevar en las manos!» | Arte y artesanía, talleres, qué contar del viaje, por dónde empezar |
| **Kej** | El equilibrio: cuatro pilares, naturaleza · Norte, tierra\* | Explorar | Práctico y ordenado: «Cuatro paradas, a pie, en este orden.» | Rutas a pie, naturaleza, pausas y calma, comunidad y mercados |
| **Ajpu** | La fuerza: sol, valentía, protección · Poniente, luz\* | Decidir | Valiente y retador: «¿Te animás? Esto vale la pena.» | La mejor opción directo, aventura, seguridad y cuidado, comida con carácter |
| **No'j** | La sabiduría: consejo claro · Sur, aire\* | Comprender | Maestro cercano: «¿Sabías que…? Mirá este detalle.» | Historia y monumentos, cosmovisión maya, respeto, lugares para aprender |

**Cómo funcionan (decisiones del 18-oct)**
- ✅ Cada guardián es un personaje con su tono **y su propia recomendación**. Cada respuesta muestra su nombre e ícono.
- ✅ **Turno:**
  - Empieza B'atz'.
  - El guardián **sigue contestando hasta que el turista pida hablar con otro**.
  - Si pide «otro» sin decir cuál, pasa el siguiente en orden fijo: B'atz' → Kej → Ajpu → No'j → B'atz'.
  - Si nombra a uno («quiero hablar con No'j») o toca su ícono, pasa ese.
  - ❌ Reemplaza «cada pregunta la contesta uno distinto» (ronda 2) y «aparece el que corresponde» (ronda 1).
- ⚠️ Ajpu «seguridad» exige fuente oficial (regla 7); hasta tenerla, lo dice y no aconseja.
- ⚠️ «Volcanes» quedó fuera del primer bloque (Documento Rector).
- \* Direcciones, elementos y valores sin validar. Ojo: los cargadores del año del altiplano (PDF) son Iq', Kej, E y No'j; B'atz' y Ajpu no están entre ellos. Preguntarle al Ajq'ij.
- ❓ El cuaderno 7144 dice que la fecha del fundador cae en 11 No'j. ¿Tiene que ver con No'j?
- Cada lugar del catálogo lleva la etiqueta de qué guardián lo recomienda (propuesta de Claude, sección 7).

## 4. Producto (lo que existe)

**App vigente:** `app/index.html`. Un solo archivo, se abre directo en el navegador.

| Pestaña | Qué hace |
|---|---|
| **Guía** (pantalla 1) | Chat con el guardián de turno. 7 preguntas listas + texto libre. Reglas fijas, sin IA. Responde solo con lugares verificados del catálogo; si no tiene datos, lo dice. ♥ para guardar desde el chat. |
| **Explorar** | Muro de pines: rutas, lugares, consejos, cosmovisión y los 20 nawales. Buscador, filtros y ficha de cada pin con «Preguntale a [guardián]». Tarjeta Plan Fundador (Patrocinado). |
| **Para vos** | Lo guardado con ♥ arma un plan de 5 paradas a pie con Google Maps. |

Además: ES/EN, modo claro/oscuro y panel «¿Quiénes son los guardianes?».

- ✅ Visual: **neutro y provisional**. Ninguna paleta vieja sigue; el fundador hará el arte final.
- Versiones anteriores, solo como referencia: `versiones/prototipo-0` (muro) y `versiones/prototipo-1` (chat).

## 5. Tablero de circuitos

Un circuito = algo pasa → resultado verificable. **Antes de construir: «¿qué circuito cierra esto?»**

| # | Circuito | Algo pasa → resultado | Estado |
|---|---|---|---|
| C1 | Entrar | Otra persona abre la app en su celular y la entiende sin ayuda | ⬜ **bloqueo, prioridad 1** |
| C2 | Preguntar | Escribe o toca una pregunta → el guardián responde con lugares reales y su tono | 🟡 |
| C3 | Cambiar de guardián | Pide otro (nombre, ícono u «otro») → cambia y ese sigue hasta el próximo pedido | 🟡 |
| C4 | Llegar | Toca «Cómo llegar» → Google Maps abre el lugar o la ruta a pie correcta | 🟡 sin probar en celular |
| C5 | Explorar | Ve el muro, filtra, busca y abre fichas | 🟡 |
| C6 | Para vos | Guarda con ♥ → recibe un plan armado | 🟡 |
| C7 | Idioma | Mismo contenido en ES y EN | 🟡 falta revisión del inglés |
| C8 | Cultura validada | Cada texto con \* queda confirmado o se quita | ⬜ depende del Ajq'ij |
| C9 | Catálogo vivo | El fundador agrega un lugar en una hoja de Google Sheets → aparece en la app | ⬜ |
| C10 | Registro | Cada pregunta del turista queda anotada (para aprender qué buscan) | ⬜ |
| C11 | Gemini | Pregunta libre → Gemini entiende y responde como el guardián, solo con el catálogo | ⬜ necesita API y presupuesto |
| C12 | Plan Fundador | Un negocio paga Q250 → aparece marcado como fundador | ⬜ sin fundadores |
| C13 | Wix | La app vive en Wix y abre en el celular | ⬜ ❓ probar ♥ y Maps dentro del iframe |
| C14 | Opiniones | El turista deja un comentario → queda registrado | ⬜ |

**Conteo:**
- ✅ cerrados: 0
- 🟡 abiertos: 6 (C2–C7)
- ⬜ pendientes: 8

**Orden recomendado:** C1 → C4 → C2/C3 → C9 → C10 → C8 → C11 → C12 → C13.
C1 va primero porque es la lección #1: nadie más ha abierto la app.

## 6. Fuentes de verdad

| Dato | Dónde vive hoy | Quién lo escribe | ¿Se toca? |
|---|---|---|---|
| Método y reglas | `0_…` a `4_….md` | Fundador | No |
| Concepto, estado, circuitos | Este documento | Claude con el fundador | Sí |
| Lugares, rutas, consejos, nawales | Dentro de `app/index.html` (temporal) | Fundador (frases) + Claude (direcciones) | Sí. Pasa a Google Sheets en C9 |
| Respuestas de los guardianes | Dentro de `app/index.html` | Claude (propuesta) | Sí, el fundador corrige |
| Cosmovisión y 20 nawales | PDF Consolidado | Fundador | No; en la app con \* |
| Fuentes originales | NotebookLM (Claude no tiene acceso) | Fundador | Propuesta: copiarlas a Google Drive, carpeta «nAIhual fuentes» |
| Diseño editable | Figma: «nAIhual · App 1.0» https://www.figma.com/design/K67raFNTRvhkSOAEpWtByE · 3 páginas (Leeme y fundamentos · Componentes · Pantallas y textos). Capas «#…» = textos que usa la app | Fundador (diseño) + Claude (lee y pasa a la app) | Sí. El fundador rediseña; Claude copia los cambios a la app |
| Línea gráfica | Figma: 6 pantallas para que el fundador las rediseñe (Entrar, Inicio, Guardianes, Chat, Muro, Ficha) https://www.figma.com/design/tw3f3T31gReovmpb5bGcxi | Fundador | Sí. Lo que el fundador dibuje aquí define el estilo visual (fase 10) |
| Contexto para NotebookLM | `docs/contexto-notebooklm.md`. Se sube al cuaderno como fuente; NotebookLM revisa los nawales contra sus 46 fuentes | Claude | Sí, cuando cambie la app |
| Web C0 vieja | Netlify (gregarious-tulumba-42cb05) | — | No tocar |

## 7. Catálogo (Antigua)

**Lugares** (frases textuales del fundador; inglés traducido por Claude, sin revisar). La columna «Guardián» es una propuesta de Claude, por corregir.

| Lugar | Tipo | Dirección | Guardián |
|---|---|---|---|
| 12 Onzas | Café | ✅ 4a Calle Oriente 5 | Kej |
| Artista de Café | Café | ✅ 5a Avenida Sur 34B | B'atz' |
| Siena Luz | Café | ✅ 6a Avenida Norte | No'j |
| Fat Cat Coffee House | Café | ✅ 4a Calle Oriente, frente a 12 Onzas | Kej |
| Coffea Cafés Especiales | Café | ✅ 6a Calle Oriente 18A | Ajpu |
| El Cazador Italiano | Comida | ✅ 3a Avenida Norte 1B | Ajpu |
| Once Once | Comida | ✅ 2a Calle Oriente 22 | Kej |
| Patio de la Primera | Comida | ✅ 1a Avenida Sur 17C | B'atz' |
| Komori · Alegría Café · Hector's Bistro · Nikolo · Y Tu Piña También | Café / comida | ❓ sin verificar: se ven en el muro, nunca en rutas, planes ni chat | — |

**Monumentos y rutas**
- 8 monumentos †: Parque Central, Catedral, Palacio de los Capitanes, Arco de Santa Catalina, La Merced, Capuchinas, Santa Clara y San Francisco el Grande.
- 3 rutas a pie †:
  - El corazón de Antigua (mañana).
  - Conventos del oriente (tarde).
  - Del Arco a La Merced (un par de horas).

**Cultura \***
- Cholq'ij, Winaq, Ruk'u'x Kaj y Ruk'u'x Ulew, maíz (Popol Wuj), Nik'aj, Ab' y Wayeb', Rueda de 52 años, cargadores del año.
- Los 20 nawales: tabla del PDF, con aviso de que no describen personas.

**Sin datos todavía:** naturaleza, talleres y artesanía, mercados, aventura y seguridad. Los guardianes lo dicen y no inventan.

## 8. Tecnología

- ✅ Destino final: app en **Wix** (verificado: acepta HTML propio con «Embed HTML»; para apps avanzadas, Velo). ❌ Netlify no.
- ✅ Voz del agente: **Gemini** (18-oct). Claude construye.
- ✅ Motor actual: **reglas fijas, gratis** (lección #6). Gemini entra en C11.
- ✅ Lugares: Google Sheets (C9).
- ❓ NotebookLM no se conecta a apps (hasta donde sé; falta verificar con fuente oficial). Propuesta: Google Drive como casa única de las fuentes.
- ❌ n8n en VPS, OpenAI, Redis, Zapier, 360dialog, Zoho, Stripe: fuera, por decisiones más nuevas o por el Documento Rector.
- Código en GitHub: `diegosamgt-lang/nAIhual`, rama `claude/awesome-carson-sz5k9i`.

## 9. Dinero

- ✅ Turista: nacional y extranjero, por igual. Usa nAIhual **gratis**; premium (WhatsApp, voz, alertas) **después**, sin precios.
- ✅ Fase 1: **Plan Fundador**, Q250/mes × 3 meses, 5 lugares, siempre marcado Patrocinado. Lo pagan los negocios. Fundadores: ninguno todavía.
- ✅ Solo negocios locales. ❌ Afiliados de Booking, Expedia u OpenTable. ❌ Paywall desde el inicio.
- ❓ Criterios para aceptar un fundador (propuesta: local, de dueños guatemaltecos, sin cadenas). ❓ Falta el número de WhatsApp para el botón.
- Idea vigente: publicidad ética, «destacado» siempre marcado.

## 10. Lo que no sé todavía

1. ¿Lo cultural sigue con \* hasta que lo valide un Ajq'ij? → fundador.
2. ¿Qué guardián recomienda cada lugar? (propuesta en la sección 7) → fundador.
3. ¿Las frases de cada guardián suenan bien? → fundador.
4. ¿Quién prueba la app en su celular esta semana (C1)? → fundador.
5. Dirección de los 5 lugares sin verificar → fundador o su red.
6. Segunda ciudad después de Antigua (¿Atitlán? ¿Ciudad de Guatemala?) → fundador.
7. Revisión del inglés por un hablante nativo → red de contactos.
8. Si NotebookLM se puede conectar a una app → Claude, con fuente oficial de Google.

## 11. Comparación con apps parecidas (investigado 24-oct-2026)

| App | Qué hace | Cómo gana dinero | Qué le sirve a nAIhual |
|---|---|---|---|
| **Withlocals** | Experiencias con anfitriones locales verificados | Comisión por reserva completada; el anfitrión pone su precio (tasa no publicada). 2022: más de €8.1M para anfitriones y negocios locales | El modelo más cercano a «comunidad primero»: cobrar solo cuando el local gana |
| **Spotted by Locals** | Guías de ciudad escritas por locales | Guía pagada por ciudad (≈ $3.99 al inicio) y licencia de contenido a medios. Los locales escriben sin cobrar. Sin inversionistas | La curaduría de locales es el producto; el contenido se puede licenciar |
| **Mindtrip** | Planificador de viajes con IA | Comisión por reservas + vende su IA a oficinas de turismo para ponerla en sus webs | Cliente B2B posible: entes de turismo (❓ INGUAT, Municipalidad, Observatorio de Antigua) |
| **GPSmyCity / Visit A City** | Caminatas e itinerarios | App gratis + pago anual (GPSmyCity $14.99/año) o contenido premium | Confirma el «gratis ahora, premium después» |
| **GetYourGuide** | Gran vendedor de tours | Cobra 20–30 % al proveedor | ❌ Lo que nAIhual no quiere ser: plataforma grande que se queda con el margen |

**Hallazgo:** no se encontró una app oficial de guía de Antigua Guatemala. INGUAT tiene audioguía en la Catedral, guías de Semana Santa, Guatemala 360° y la línea 1500. ❓ Hueco posible, falta confirmarlo en las tiendas de apps.

**Modelo propuesto (por decidir con el fundador), en 3 escalones:**
1. **Ahora:** Plan Fundador (negocios locales pagan, siempre marcado). Ya decidido.
2. **Después:** experiencias con locales (talleres, caminatas guiadas) con una comisión baja y transparente, como Withlocals. ❓
3. **Después:** licencia del agente o de su contenido curado a entes de turismo, como Mindtrip y Spotted by Locals. ❓

Turista: gratis siempre en lo básico; premium (WhatsApp, voz, sin conexión) cuando haya uso real.

Fuentes:
- [Withlocals: centro de ayuda para anfitriones](https://helpcenter.withlocals.com/en/articles/627960-what-is-withlocals-for-hosts)
- [Withlocals: reporte de impacto 2023](https://withlocals-com-res.cloudinary.com/image/upload/v1686227144/sustainability/impact_report_2023.pdf)
- [PhocusWire: Spotted by Locals](https://www.phocuswire.com/Spotted-by-Locals-celebrates-a-decade-without-outside-investors)
- [Skift: Mindtrip](https://skift.com/?p=707391)
- [GPSmyCity en App Store](https://apps.apple.com/app/id417207307)
- [GetYourGuide: comisión a proveedores](https://www.getyourguide.supply/join/how-much-does-getyourguide-charge)
- [Emisoras Unidas: INGUAT](https://emisorasunidas.com/nacional/2025/04/03/inguat-presenta-pregon-con-guias-de-cortejos-procesionales/)
- [La Hora: Catedral de San José](https://lahora.gt/?p=466398)

## 12. Ruta actualizada (24-oct-2026)

**Fase actual:** 7 · Construcción (App 1.0). La **fase 5 · Acceso** sigue bloqueada: nadie más ha abierto la app. La fase 10 (diseño) empezó con las 6 pantallas de Figma.

| Paso | Qué | Circuito | Quién |
|---|---|---|---|
| 1 | Enlace público gratis para la app (propuesta: GitHub Pages) y que 1 persona la abra en su celular | C1, C4 | Claude publica · fundador consigue a la persona |
| 2 | Registrar cada pregunta que hacen los turistas | C10 | Claude |
| 3 | Lugares en una hoja de Google Sheets | C9 | Claude arma · fundador llena |
| 4 | Respuesta de NotebookLM → corregir nawales y guardianes | C8 | Fundador pega · Claude corrige |
| 5 | Rediseño del fundador en Figma → pasar a la app | fase 10 | Fundador · Claude |
| 6 | Vender el Plan Fundador a los primeros 5 negocios | C12 | Fundador |
| 7 | Gemini como voz de los guardianes | C11 | Cuando haya uso real y presupuesto |

## 13. Historial de versiones

**App 1.0 — 18-oct-2026** (`app/index.html`)
- Junta todo en una app con 3 pestañas: Guía (chat de guardianes), Explorar (muro) y Para vos.
- Nueva regla de turno: el guardián sigue hasta que el turista pida otro.
- ♥ desde el chat; fichas con «Preguntale a [guardián]»; guardián en cada pin.
- 🟡 Probada en Chromium a 390 px; sin probar en celular real.

**Prototipo 1 — 18-oct** (`versiones/prototipo-1`): chat de los 4 guardianes, uno por pregunta.

**Prototipo 0 — 18-oct** (`versiones/prototipo-0`): la v2.1 más los 20 nawales y la cosmovisión.

**Antes del 18-oct**
- v2.1, v2 y v1 en Claude Design (17-oct): muro tipo Pinterest, Para vos y ES/EN.
- C0 y 0.1.x en ChatGPT/Codex (15–17 oct): mapa OpenStreetMap; diseño rechazado por el fundador.

## 14. Para quien siga (prompt de continuación)

> Leé `CLAUDE.md` y este documento completo, y respetá el método `0_…`–`4_….md`. La app vigente es `app/index.html`; no rehagás desde cero ni toqués lo que funciona. Antes de construir, preguntá «¿qué circuito cierra esto?». Nunca inventes datos ni significados culturales. Reportá con ✅ 🟡 ❓. Esperá CONSTRUYE. Siguiente paso: C1, que una persona que no sea el fundador abra la app en su celular.
