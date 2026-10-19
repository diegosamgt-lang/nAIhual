# nAIhual — Contexto para NotebookLM

> **Para NotebookLM:** este documento explica qué es nAIhual, cómo funciona la app hoy y **dónde y cómo usa los nawales**. Lo escribió Claude, la IA que construye la app, el 19-oct-2026. Claude **no tiene acceso a las fuentes de este cuaderno**. Tu tarea es revisar lo que aquí está contra tus fuentes, corregir, completar y citar (sección 7).

---

## 1. Qué es nAIhual

- Un **agente artesanal turístico-cultural**: un puente entre viajeros y las comunidades, la cultura, la naturaleza y el territorio de Guatemala.
- «Artesanal» = la información la curan personas locales antes de entrar al agente. No inventa lugares, horarios, precios ni significados.
- El nombre junta *nahual* + *IA*. Es un nombre propio del proyecto, no un término de la tradición maya.
- Frase de marca: **«Viaja directo a la raíz.»**
- Piloto: **Antigua Guatemala**. Idiomas: español e inglés.
- Público: turistas nacionales y extranjeros, por igual.
- Gratis para el turista. Lo pagan negocios locales con el Plan Fundador, siempre marcado como patrocinado. No trabaja con plataformas grandes.
- Voz: cálida y directa, cercana, sin tono místico. Lo espiritual aparece solo cuando se habla de cultura.

**Principios**
- Comunidad primero.
- Cultura sin apropiación ni folclor.
- Sostenibilidad y cuidado contra la gentrificación.
- Lo patrocinado siempre visible.
- Nunca inventar.
- No difundir lugares naturales sensibles.

---

## 2. Los nawales como base del concepto

La app no tiene un solo asistente. La atienden **4 guardianes**, cada uno con el nombre de un nawal del Cholq'ij. La idea viene del **número 4**: los cuatro rumbos y los cuatro pilares.

| Guardián | Valor en nAIhual | Rumbo · elemento | Qué hace en la app | Cómo habla | Qué recomienda |
|---|---|---|---|---|---|
| **B'atz'** | El inicio: tejido, chispa creativa | Oriente · fuego | Crear | Juguetón y curioso | Arte y artesanía, talleres, qué contar del viaje, por dónde empezar |
| **Kej** | El equilibrio: cuatro pilares, naturaleza | Norte · tierra | Explorar | Práctico y ordenado | Rutas a pie, naturaleza, pausas y calma, mercados y comunidad |
| **Ajpu** | La fuerza: sol, valentía, protección | Poniente · luz | Decidir | Valiente y retador | La mejor opción directo, aventura, cuidado, comida con carácter |
| **No'j** | La sabiduría: consejo claro | Sur · aire | Comprender | Maestro cercano | Historia, cosmovisión maya, respeto y costumbres, lugares para aprender |

**Cómo se turnan**
- Empieza B'atz'.
- Ese guardián **sigue guiando hasta que el turista pide hablar con otro**.
- Si pide «otro», pasa el siguiente en orden: B'atz' → Kej → Ajpu → No'j.
- También puede nombrar a uno o tocar su ícono.
- Cada guardián responde con **su tono y su propia recomendación**.

⚠️ **Sin validar:** la asignación de rumbos, elementos y valores a estos cuatro nawales salió de una conversación de marca anterior, no de una fuente cultural. Hay una duda concreta. Según el Documento Consolidado, los **cargadores del año** del altiplano son **Iq', Kej, E y No'j**. B'atz' y Ajpu no están entre ellos. ¿Es correcto usar estos cuatro como «guardianes de los rumbos»? (pregunta 7.1)

---

## 3. Dónde aparecen los nawales en la app

| Lugar de la app | Qué muestra | De dónde salió |
|---|---|---|
| **Guía** (chat, pantalla de inicio) | Los 4 guardianes. Cada uno se presenta: «Soy B'atz', el inicio: el hilo con el que empieza todo» · «Soy Kej, el equilibrio. Yo te ordeno el camino» · «Soy Ajpu, la fuerza del sol. Yo te reto a ir» · «Soy No'j, la sabiduría. Yo te cuento el porqué» | Frases de Claude sobre el valor de cada uno |
| **Panel «¿Quiénes son los guardianes?»** | Valor, función, forma de hablar, recomendaciones y el dato del nawal según el PDF (símbolo y animal) | Documento Consolidado |
| **Explorar** (muro) | Un pin «Los 20 nawales del Cholq'ij» y un pin por cada nawal, con su filtro | Tabla del Documento Consolidado |
| **Ficha de cada nawal** | Número (1–20), símbolo/elemento, animal, luz/vocación, sombra/desafío. Si es guardián, un botón para hablar con él | Tabla del Documento Consolidado |
| **Consejos de cosmovisión** (muro y chat de No'j) | Cholq'ij (260 días = 13 × 20), Winaq (20), Ruk'u'x Kaj y Ruk'u'x Ulew, humanidad de maíz (Popol Wuj), Nik'aj (cero como plenitud), Ab' y Wayeb', Rueda Calendárica (52 años, 18,980 días), cargadores del año (Iq', Kej, E, No'j) | Documento Consolidado |

**Reglas que la app ya cumple**
- Todo texto cultural lleva **\*** («por confirmar con un Ajq'ij»).
- Cada nawal muestra este aviso: *«Estos son los significados de los días, no una descripción de personas. nAIhual no te dice "cuál es tu nawal": eso lo hace un Ajq'ij.»*
- La app **no** calcula el nawal de nacimiento ni el nawal del día.
- No convierte lo ritual en espectáculo. Separa lo práctico (direcciones, horarios) de lo tradicional.

---

## 4. Los 20 nawales tal como están hoy en la app

Copiados del Documento Consolidado. **Revisalos contra tus fuentes.**

| # | Nawal | Símbolo / elemento | Animal | Luz | Sombra |
|---|---|---|---|---|---|
| 1 | B'atz' | Hilo del tiempo, tejido, origen | Mono | Maestro de artes, tejedor del tiempo, guía familiar | Terquedad, ambición material, sarcasmo |
| 2 | E | Camino, destino, estructura corporal | Gato de monte, puma | Guía de viajeros, líder nato, orador | Impaciencia, inestabilidad emocional |
| 3 | Aj | Cañaveral, hogar, linaje, autoridad | Armadillo | Protector de niños, mediador, sabio | Chisme, celos, manipulación |
| 4 | I'x | Jaguar, energía terrestre, altar | Jaguar | Intuición, sagacidad, fuerza de la Tierra | Orgullo, impulsividad, reserva excesiva |
| 5 | Tz'ikin | Pájaro, quetzal, abundancia | Aves rapaces, quetzal | Visión a larga distancia, imán de fortuna | Inconstancia, egoísmo, dispersión |
| 6 | Ajmaq | Búho, perdón, ancestros, sabiduría | Búho, abeja, buitre | Conciencia de faltas, perdón, mente analítica | Autocomplacencia, cobardía, lentitud |
| 7 | No'j | Mente, pensamiento, sabiduría | Coyote, lobo, pájaro carpintero | Inteligencia analítica, buen consejo, ciencia | Inflexibilidad, orgullo intelectual |
| 8 | Tijax | Obsidiana, filo de la verdad, sanación | Peztucán, pez espada | Discernimiento radical, capacidad médica | Carácter tajante, pleitos, franqueza hiriente |
| 9 | Kawoq | Tormenta, lluvia de bendición, familia | Tortuga | Integración familiar, fertilidad, sanación | Temperamento explosivo, conflictos |
| 10 | Ajpu | El Sol, cazador célebre, autoridad | Espíritu humano / Sol | Autoridad moral, fuerza renovadora, metas | Autocracia, soberbia, exigencia extrema |
| 11 | Imox | Aguas primordiales, subconsciente | Cocodrilo | Receptividad espiritual, intuición poética | Inestabilidad emocional, confusión mental |
| 12 | Iq' | Viento, aliento de vida, purificación | Colibrí | Dinamismo, limpieza energética, comunicación | Volubilidad, carácter impetuoso |
| 13 | Aq'ab'al | Amanecer, aurora, luz renovadora | Murciélago, guacamaya | Claridad mental, renovación de esperanza | Indecisión, propensión al ocultamiento |
| 14 | K'at | Red, cautiverio, reunión de la cosecha | Lagartija, araña | Organización, abundancia, resolución | Atadura por apegos, enredos emocionales |
| 15 | Kan | Serpiente de fuego, fuerza vital | Serpiente | Sabiduría profunda, transformación, justicia | Impulsividad violenta, rencor, irascibilidad |
| 16 | Kame | Mente ritual, transición, antepasados | Tecolote, búho | Serenidad ante crisis, protección ancestral | Melancolía, vulnerabilidad física |
| 17 | Kej | Venado, 4 pilares del cosmos | Venado | Solidez moral, sostén comunitario, agilidad | Rigidez de juicio, dominación autoritaria |
| 18 | Q'anil | Semilla, germinación, estrella | Conejo | Fertilidad, amor incondicional, prosperidad | Impaciencia por ver frutos de inmediato |
| 19 | Toj | Ofrenda, pago divino, ceremonia | Puma, jaguar negro | Restablecimiento del equilibrio, devoción | Padecimiento por falta de pago espiritual |
| 20 | Tz'i' | Perro, guardián de la ley y justicia | Perro, mapache | Lealtad inquebrantable, sentido de equidad | Juzgamiento severo, venganza, celos |

---

## 5. Lo que la app NO hace (y no debe hacer sin validación)

- Decirle a una persona cuál es su nawal, ni describir su personalidad por su nawal.
- Calcular fechas del Cholq'ij.
- Recomendar ceremonias, altares o sitios sagrados como atracción turística.
- Traducir términos mayas sin fuente.
- Mezclar tradiciones de distintos pueblos mayas como si fueran una sola.

---

## 6. Dónde estamos (19-oct-2026)

- Existe la **App 1.0**, con 3 pestañas: Guía (chat de guardianes), Explorar (muro con lugares, rutas, consejos y nawales) y Para vos (plan a pie con Google Maps).
- Responde con **reglas fijas**, sin IA todavía. Más adelante, **Gemini** será la voz de los guardianes.
- El catálogo tiene 8 cafés y restaurantes verificados, 8 monumentos y 3 rutas a pie en Antigua.
- Falta:
  - que otra persona pruebe la app en su celular;
  - validar lo cultural con un Ajq'ij;
  - pasar los lugares a Google Sheets;
  - conectar Gemini.

---

## 7. Lo que necesitamos de vos, NotebookLM

Respondé **solo con tus fuentes**. Después de cada dato, citá la fuente. Si algo no está en tus fuentes, escribí «no está en las fuentes». No completes con suposiciones.

1. **Los 4 guardianes:**
   - ¿Tus fuentes asocian B'atz', Kej, Ajpu y No'j a los rumbos (oriente, norte, poniente, sur) y a los elementos que usamos?
   - ¿Qué nawales asocian tus fuentes a cada rumbo?
   - ¿Hay alguna razón cultural para elegir otros cuatro, por ejemplo los cargadores Iq', Kej, E y No'j?
2. **Valor de cada guardián:** ¿«inicio», «equilibrio», «fuerza» y «sabiduría» son fieles a lo que dicen tus fuentes de cada uno? Proponé otra palabra si hace falta.
3. **Tabla de los 20 nawales (sección 4):** marcá cada celda que **no coincida** con tus fuentes y escribí la versión de la fuente. Señalá también las diferencias entre fuentes.
4. **Ortografía:** ¿cómo escriben tus fuentes cada nombre (B'atz', Aq'ab'al, Tz'i'…)? ¿Qué idioma maya usan (K'iche', Kaqchikel…)?
5. **Cosmovisión (sección 3):** confirmá o corregí cada punto, con fuente:
   - Cholq'ij;
   - Winaq;
   - Ruk'u'x Kaj y Ruk'u'x Ulew;
   - maíz;
   - Nik'aj como cero;
   - Ab' y Wayeb';
   - Rueda Calendárica;
   - cargadores del año.
6. **Para turistas:** ¿qué dicen tus fuentes que un visitante **sí** puede saber y hacer con respeto? ¿Y qué **no** se debe compartir o mostrar?
7. **Contexto de Antigua:** ¿hay en tus fuentes lugares, comunidades o iniciativas en Antigua o cerca relacionados con la cultura maya viva que un guardián como No'j podría recomendar?
8. **Algo que nos falte:** ¿qué hay en tus 46 fuentes, importante para nAIhual, que no aparece en este documento?

Organizá la respuesta con los mismos números (1 a 8). Si no cabe, esperá a que te escriban «sigue».
