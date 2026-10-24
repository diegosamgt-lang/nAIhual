---
title: "nAIhual · Entrega vNext (preparación del piloto)"
---

# nAIhual · Entrega vNext — preparación del piloto

**Fecha:** 23-oct-2026 (hora de Guatemala) · **Versión de la app:** App 1.1 piloto · **Rama:** `claude/awesome-carson-sz5k9i`
**Estado:** cambios locales. **Sin commit, sin push, sin publicar.** El piloto **no está lanzado ni validado**.

Marcas: ✅ comprobado (con prueba) · 🟡 construido, falta prueba externa · ❓ supuesto o por decidir · \* cultural, pendiente de validación · † histórico, pendiente de fuente oficial.

---

## 1. Qué cambió y por qué

| Cambio | Por qué |
|---|---|
| Los guardianes ahora son **No'j, Iq', Kej y E'**, en ese orden. Empieza No'j. «Otro guía» sigue ese orden. | Decisión aprobada del fundador (24-oct, sección 3c del documento único). La app todavía mostraba B'atz' y Ajpu. |
| Voces y respuestas de Iq' y E' reescritas según lo que decidió el fundador (Iq': pausas, qué contar, hablar con la gente, primeros pasos · E': la mejor opción, comida con carácter, artesanos). No'j sin cambios. Kej sin «pausas». | Mismo origen. Son propuesta de Claude, por corregir. |
| Rumbo y color de cada guardián en el panel «¿Quiénes son los guardianes?», con \* y un aviso: *pendiente de validación cultural*. Colores de los íconos: rojo, blanco, negro y amarillo, también con \*. | El fundador pidió rumbo y color en la app con \*. No hay fuente verificada todavía. |
| B'atz' y Ajpu siguen en la app **solo como 2 de los 20 nawales** (Explorar). | El fundador dijo que salen como guardianes, no del calendario. |
| Los lugares salieron del programa a un archivo aparte: `app/data/lugares.js`. | Recomendación del mapa (7.2): cada cambio de un lugar ya no exige tocar el programa. |
| Cada lugar tiene ahora: id fijo, nombre, categoría, dirección, enlace de Maps, fuente, enlace de la fuente, fecha de verificación, quién verificó, estado (borrador · publicado · pausado · retirado), patrocinado, horario + su fuente, precio + su fuente. | Campos mínimos del mapa (5.1). |
| Los 21 lugares actuales quedaron en **borrador**. Ninguno tiene fuente, fecha ni persona que verificó. | Regla «nunca inventar». No se convirtió ninguno en verificado. |
| **«Quiero un café»** es ahora el primer botón del chat, resaltado. Muestra **hasta 3 cafés publicados**, cada uno con fuente, fecha y quién verificó, y su botón **«Cómo llegar»**. | Recorrido del piloto (mapa, sección 4). |
| Si no hay cafés publicados, aparece **«Selección en revisión»**: explica que todavía no hay cafés comprobados y no muestra ningún botón. **Hoy es lo que se ve**, porque no hay ningún café publicado. | No inventar ni elegir cafés por el fundador. |
| Los lugares en borrador se siguen viendo en Explorar, en las rutas y en Para vos, ahora con la etiqueta **«En revisión»** y una nota: «todavía sin fuente ni fecha de verificación registradas». Nunca muestran fuente ni «comprobado». | Conservar el contenido sin hacerlo pasar por verificado. |
| Un lugar **pausado o retirado** no se ve en ninguna parte (tampoco en rutas). | Para corregir un error el mismo día (mapa 5.2). |
| «Patrocinado» solo agrega una etiqueta visible. **No cambia el orden**: el orden es el de la lista del catálogo. | Regla de autonomía del turista. El patrocinio sigue siendo hipótesis. |
| Horario y precio solo se muestran si tienen su propia fuente. Hoy no hay ninguno. | Regla «nunca inventar horarios ni precios». |
| «Cómo llegar» usa el mismo enlace universal de Google Maps que ya existía (sin llave, sin costo). Sin dirección, no hay botón. Si una ficha trae su propio enlace, solo se acepta si es de Google Maps. | Evitar botones rotos. Sin servicios nuevos. |
| Detalles: ícono vacío de pestaña (evita un error en la consola), nombre accesible en el grupo de guardianes y en cada «Cómo llegar». | Calidad mínima pedida. |

**No se agregó:** IA ni Gemini, cuentas, perfiles, datos personales, analítica, rastreo, formularios, Google Sheets, APIs de pago, Places API, pagos, comisiones, publicidad nueva, agentes, reseñas, playlists, QR, categorías nuevas ni número de emergencia.

---

## 2. Archivos

| Archivo | Qué pasó |
|---|---|
| `app/index.html` | Modificado (guardianes, recorrido de café, etiquetas «En revisión», lectura del catálogo). |
| `app/data/lugares.js` | **Nuevo.** Catálogo de 21 lugares, todos en borrador. |
| `pruebas/prueba_piloto.py` | **Nuevo.** Pruebas automáticas. Queda fuera de `app/` para que no se publique con la app. |
| `docs/nAIhual-vNext-handoff.md` | **Nuevo.** Este informe (y su PDF). |
| `docs/nAIhual.md` | Actualizado (estado de guardianes, catálogo, circuitos, historial). |

---

## 3. Pruebas ejecutadas

**Comando:** `python3 pruebas/prueba_piloto.py` (desde la raíz del repositorio).
**Herramienta:** Playwright con Chromium, que ya viene en el entorno de Claude en la nube. No se agregó ninguna dependencia al proyecto.
**Resultado observado (23-oct-2026):** **81 de 81 pruebas pasan.** La primera corrida dio 80/81: la consola marcaba un error porque el navegador pedía un ícono de pestaña inexistente. Se corrigió y se volvió a correr.

Qué cubre (pantalla de 390 × 844 px, modo claro y oscuro):

- La app carga con el catálogo real (21 lugares), por servidor local y abriendo el archivo directo.
- Aparecen exactamente 4 guardianes: No'j, Iq', Kej, E', en ese orden, en la Guía y en el panel. Empieza No'j. B'atz' y Ajpu no aparecen como guardianes.
- «Otro guía» recorre Iq' → Kej → E' → No'j. Pedir por nombre funciona («quiero hablar con E'», «Iq'», «kej», «No'j»). Pedir a B'atz' no lo vuelve guardián.
- Las tres pestañas (Guía, Explorar, Para vos) funcionan. Los 20 nawales siguen en Explorar. Para vos arma un plan.
- Con el catálogo real, «Quiero un café» muestra «Selección en revisión», sin enlaces.
- Con catálogos **de prueba** (inventados solo para la prueba, nunca se publican):
  - 0 cafés válidos → estado vacío;
  - 1 café válido entre 11 incompletos → muestra 1;
  - 4 cafés válidos → muestra 3, en el orden de la lista. El patrocinado lleva su etiqueta y no sube.
- Fichas incompletas que **no** entran: sin fuente, sin fecha, fecha imposible, fecha futura, sin quién verificó, sin dirección, enlace de Maps que no es de Google, borrador, pausado y retirado. Pausado y retirado no aparecen en ninguna parte. Sin dirección o con enlace inválido no hay botón de Maps. Un horario sin fuente no se muestra.
- Cada café mostrado tiene fuente y «Comprobado el [fecha] por [persona]», también en inglés.
- «Cómo llegar» arma un enlace de Google Maps con nombre + dirección + «Antigua Guatemala», o respeta el enlace propio de la ficha.
- Sin desplazamiento horizontal a 390 px: Guía, panel, recorrido con 3 fichas, Explorar, ficha y Para vos.
- Teclado: Tab llega a «Quiero un café», Enter abre el recorrido y «Cómo llegar» recibe el foco.
- Accesibilidad básica: todos los controles visibles tienen nombre, no hay id repetidos y el idioma de la página está declarado. El contraste del texto de los íconos de guardián y del botón de café es de 4.5 o más, en claro y en oscuro.
- Consola sin errores en todos los casos.

**Revisión a ojo:** capturas a 390 px del inicio, el estado vacío, el panel de guardianes (claro y oscuro), el recorrido con 3 fichas y la ficha publicada. Se ven ordenadas y legibles.

**Lo que NO se probó (lo tiene que hacer una persona):**

- Un celular real. Todo fue en un navegador simulado.
- Que cada enlace de Maps caiga en el lugar correcto.
- Una auditoría completa de accesibilidad: no se hizo; solo las comprobaciones básicas de arriba. Tampoco se probó con lector de pantalla.
- Ningún negocio fue verificado.
- Ninguna persona externa usó la app.

---

## 4. Estado

### ✅ Implementado y comprobado (pruebas automáticas + revisión local)
- Los 4 guardianes aprobados, en orden, con su turno y su cambio.
- Catálogo separado, con los campos mínimos y los 4 estados.
- Recorrido «Quiero un café»: 0, 1 o hasta 3 fichas, según los datos. Estado vacío cuando no hay.
- Fuente, fecha y quién verificó en cada café publicado. «En revisión» en lo que no cumple.
- «Cómo llegar» solo cuando se puede armar el enlace.
- Patrocinio etiquetado, sin cambiar el orden.
- 390 px sin desplazamiento horizontal, uso con teclado, consola limpia.

### 🟡 Implementado, pendiente de prueba externa
- Que «Cómo llegar» abra el lugar correcto desde un celular real (C4).
- Que una persona que no sea el fundador entienda la app sin ayuda (C1).
- Que funcione igual en el alojamiento que se elija (hoy son 2 archivos: `index.html` y `data/lugares.js`).
- Inglés sin revisar por un hablante nativo.

### ❓ Pendiente de decisión o información del fundador
1. **Alojamiento** (ver sección 6).
2. **Hasta 3 cafés** con todos sus datos (ver sección 5).
3. **Qué nombre se muestra en «verificó»**. Va a ser público: tu nombre, solo tu primer nombre o «Equipo nAIhual».
4. **Canal para reportar errores**: WhatsApp o correo. Hoy no hay. Tampoco hay número para el botón de negocios.
5. **Tarjeta «Plan Fundador» (Q250)** en Explorar. Ya estaba antes de esta versión. ¿Se queda visible durante el piloto? El mapa trata precios y planes como hipótesis.
6. **Validación cultural** (Ajq'ij) de rumbos, colores, valores y frases de los guardianes. No cambia la selección de los cuatro.
7. **Frases con afirmaciones**: «Coffea… entre las 100 mejores coffee shops del mundo» necesita fuente o hay que quitarla antes de publicar esa ficha.
8. **Persona y fecha** de la primera prueba externa.

### Hipótesis futuras que **no** se implementaron
Gemini o cualquier IA · Google Sheets como catálogo (C9) · registro de preguntas (C10) · Places API · Plan Fundador con pagos · comisiones · Fondo Raíz · agentes, playlists, reseñas · QR para hoteles · emergencias (falta fuente oficial vigente) · eventos de Iq' · red social · actualizar la tabla de los 20 nawales con la versión de NotebookLM · documento rector v1.2.

---

## 5. Qué necesito para publicar cada café (máximo 3)

Para **cada** café:

| Dato | Ejemplo de forma (no es un dato real) |
|---|---|
| Nombre, como aparece en el local | «Nombre del café» |
| Dirección exacta | «4a Calle Oriente #00» |
| Enlace de Google Maps (opcional) | El que sale en Maps → Compartir. Si no lo das, la app lo arma con nombre + dirección. |
| Fuente | «Visita del fundador» o un enlace público (Maps, página oficial) |
| Fecha en que lo comprobaste | 2026-10-25 |
| Quién lo comprobó | El nombre que aceptás que sea público |
| ¿Patrocinado? | Sí o no. Para el piloto se recomienda **no**. |
| Horario y precio | Solo si tenés la fuente. Si no, se dejan vacíos. |

Los cafés que **ya están en el catálogo como borrador**, con tu frase, son estos. Vos decidís cuáles confirmar; yo no elijo:

- 12 Onzas
- Artista de Café
- Siena Luz
- Fat Cat Coffee House
- Coffea Cafés Especiales (ver punto 7 de la sección 4)
- Komori y Alegría Café: también están, pero sin dirección.

Las direcciones de esos cafés las escribí yo en octubre, sin una fuente registrada. Hay que confirmarlas.

Con esos datos, el cambio es solo en `app/data/lugares.js`: llenar los campos y poner `estado: 'publicado'`. La app los muestra sola. Si falta un dato, sigue en «En revisión».

---

## 6. Alojamiento: qué falta y recomendación (no ejecutado)

**Qué falta para elegir:** tu decisión. También saber si la app tiene que quedar dentro de Wix desde el piloto o si basta un enlace aparte.

**Qué se publica:** solo la carpeta `app/` (2 archivos). No hay datos personales en ella. El número de WhatsApp está vacío. La página carga la letra desde Google Fonts, como ya lo hacía.

| Opción | A favor | En contra |
|---|---|---|
| **GitHub Pages, en un repositorio nuevo y público que solo tenga `app/`** (recomendada) | Gratis. El enlace es fijo y abre en cualquier celular, sin cuenta. Los documentos privados quedan en el repositorio actual. | Lo que esté en ese repositorio nuevo queda público. |
| Wix (Embed HTML) | Es el destino final que elegiste (sección 8 del documento único). | Hay que pegar todo en un solo bloque (el catálogo iría adentro). Nadie ha probado el corazón ♥ ni Maps dentro de Wix (C13). Puede tener costo. |
| Vista compartida de Claude | Rápida. | ❓ No verifiqué si quien la abre necesita cuenta. No sirve como casa definitiva. |

**Pasos para la opción recomendada** (cuando digás que sí; nada de esto está hecho):

1. En github.com, tocá **+** → **New repository**.
2. Nombre: por ejemplo `naihual-piloto`. Marcá **Public**. Tocá **Create repository**.
3. Subí solo `index.html` y la carpeta `data` (con `lugares.js`). Ojo: no el repositorio completo.
4. En el repositorio nuevo: **Settings** → **Pages** → en «Branch» elegí `main` y la carpeta `/ (root)` → **Save**.
5. Esperá unos minutos. GitHub te da un enlace del tipo `https://<tu-usuario>.github.io/naihual-piloto/`.
6. Abrilo en tu celular y en el de otra persona. Probá «Quiero un café» → «Cómo llegar».

Si me autorizás, los pasos 1 a 4 los puedo hacer yo. Necesito tu «sí» y que el repositorio nuevo esté dentro de lo que me dejás tocar.

---

## 7. Tus próximas acciones, en orden

1. **Elegí el alojamiento** (recomendado: GitHub Pages en un repositorio nuevo y público, solo con la app).
2. **Pasame hasta 3 cafés** con fuente, fecha y quién verificó (tabla de la sección 5), y el nombre público para «verificó».
3. **Probá cada «Cómo llegar» desde tu celular** y anotá si cae en el lugar correcto.
4. **Elegí a la persona y la fecha** de la primera prueba externa. Que no seas vos.
5. **Definí el canal para reportar errores** (WhatsApp o correo).
6. Decidí si la tarjeta «Plan Fundador» se queda visible durante el piloto.

**El piloto cuenta como hecho** solo cuando una persona externa complete el recorrido desde un enlace público, en su celular, y esa prueba quede anotada. Las 3 preguntas del mapa se hacen en persona, fuera de la app.
