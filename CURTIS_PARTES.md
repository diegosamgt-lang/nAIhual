# CURTIS — partes, circuitos y bitácora

> Curtis es el asistente. El panel es cómo se ve. Va a ir evolucionando con el dueño.
> Leyenda: ✅ funciona y probado · 🟡 construido sin probar de verdad · ⬜ por construir · ❓ falta una decisión del dueño

---

## P1 · Núcleo: anotar y editar
| # | Circuito | Estado |
|---|---|---|
| 1.1 | Anotar con + → queda con fecha de hoy | ✅ |
| 1.2 | Todo editable con guardado automático (tarea, proyecto, sección, pasos) | ✅ |
| 1.3 | Borrar con confirmación; lo terminado queda tachado | ✅ |
| 1.4 | Etiquetas que el dueño crea (nombre + color + ícono), en tareas y proyectos, con filtro | ✅ probado |

## P2 · Tiempo: resumen, calendario y fechas límite
| # | Circuito | Estado |
|---|---|---|
| 2.1 | Resumen arriba que se actualiza solo | ✅ |
| 2.2 | Mini calendario en Inicio y en Mis tareas: puntos por día; tocás un día y ves qué hay | ✅ probado |
| 2.3 | Fechas límite (21 días en Inicio, 45 en calendario grande) con cuenta regresiva | ✅ probado |
| 2.4 | Mis tareas por tiempo: atrasadas · hoy · próximos 3 días · resto de la semana · después · sin fecha | ✅ |

## P3 · Urgencia
| # | Circuito | Estado |
|---|---|---|
| 3.1 | Prioridad alta / normal | ✅ |
| 3.2 | Íconos de urgencia calculados solos: atrasada · hoy · 1–3 días · semana · después · esperando · sin fecha | ✅ probado |

## P4 · NIHR y registro
| # | Circuito | Estado |
|---|---|---|
| 4.1 | Bitácora con fecha y horas → suma contra el mínimo | ✅ |
| 4.2 | Reunión → acuerdos se vuelven tareas (una vez) | ✅ |
| 4.3 | Metas del mes y del año | ✅ |

## P5 · TDAH: foco y ganas de volver
| # | Circuito | Estado |
|---|---|---|
| 5.1 | «Ahora»: una sola cosa | ✅ |
| 5.2 | Reloj de foco 15/25/45 que guarda el tiempo | ✅ |
| 5.3 | Frase del día: Curtis la escribe sola una vez al día (si ya diste permiso) según lo que hacés; si no, una de 30 frases propias | ✅ probado (simulado) |
| 5.4 | Invitaciones a llenar (bitácora de hoy, acuerdos, esperando hace días, entrega cerca, proyecto sin tareas, atrasadas) | ✅ |
| 5.5 | Movimiento sutil: curvas de nivel que cambian cada día y se mueven despacio, festejo al terminar | ✅ |

## P6 · Curtis: IA y memoria
| # | Circuito | Estado |
|---|---|---|
| 6.1 | Chat en cada tarea y proyecto con contexto | 🟡 probado con respuesta simulada |
| 6.2 | Resumen del día por Curtis | 🟡 |
| 6.3 | Memoria «Así trabajás»: calculada de tus datos (tiempos, horario, % tarde, foco, precio y días por categoría, pasos repetidos) + lo que anota Curtis + lo que anotás vos; editable | ✅ probado |
| 6.4 | Automatización: pasos repetidos por categoría → «Usar como plantilla» → proyecto nuevo de esa categoría carga los pasos | 🟡 construido, falta uso real |
| 6.5 | Nombre e identidad «Curtis» en todo el panel | ✅ |

## P7 · Entregas
| # | Circuito | Estado |
|---|---|---|
| 7.1 | Carpetas de trabajo en Drive (con permiso) | 🟡 simulado |
| 7.2 | Entregar proyecto: revisión de calidad → subís archivos (o carpeta) → Curtis los acomoda en la estructura fija → crea todo en Drive con permiso → proyecto Entregado | ✅ simulado con tus archivos reales de Beauty Sleep · ❓ falta prueba real |
| 7.3 | Mensaje de entrega con link y qué hay en cada carpeta; copiar; «Mejorar con Curtis» | ✅ |
| 7.4 | PDF con el link de cada carpeta, guardado en «00 Léeme» | ✅ simulado |
| 7.5 | NIHR: proyecto «Carpeta final» con 5 pasos hasta el 1 de diciembre (fecha aproximada). Curtis lista, crea carpetas y mueve archivos con permiso; nunca borra | 🟡 herramientas simuladas · ❓ día exacto de entrega |
| Límite | Subir archivos desde el panel: hasta 16 MB por archivo. Carpetas muy pesadas conviene subirlas directo a Drive y que Curtis las ordene después. ❓ por confirmar en la primera prueba real | — |

## P8 · Dinero
| # | Circuito | Estado |
|---|---|---|
| 8.1 | Cotización en Zoho en borrador | 🟡 simulado · la prueba de Zoho está vencida |
| 8.2 | Precio por proyecto + promedio por categoría en «Así trabajás»; cada cotización y entrega se anota en la memoria | ✅ |

## P9 · Crecimiento: clientes y LinkedIn
| # | Circuito | Estado |
|---|---|---|
| 9.1 | Al terminar un proyecto, Curtis propone un caso de estudio o un post para LinkedIn | ⬜ |
| 9.2 | Consejos para el perfil de LinkedIn (titular, acerca de, destacados) | ⬜ |
| 9.3 | Lista de prospectos en **LinkedIn** (empresas a contactar) con seguimiento — primer canal decidido | ⬜ |
| Límite | Curtis no puede entrar a LinkedIn ni navegar internet desde el panel. Sí puede escribir, ordenar y darte seguimiento. | — |

## P10 · Identidad visual
| # | Circuito | Estado |
|---|---|---|
| 10.1 | Estilo inspirado en National Geographic: papel cálido, bosque, musgo, tierra, lago y el marco amarillo; Newsreader + Instrument Sans | 🟡 falta que el dueño lo vea |

---

## Auditoría de la v3 (lo que hay hoy)
- **Fuerte:** registro completo, todo editable, guardado automático, proyectos tipo Asana/Notion, foco, permisos antes de Drive y Zoho, 34/34 pruebas.
- **Débil:** fechas límite poco visibles; urgencia solo «alta»; sin etiquetas; sin calendario; Curtis no recuerda nada entre conversaciones; no hay flujo de entrega; Drive y Zoho nunca probados de verdad; arrastrar no funciona en celular; fuentes y colores no le gustan al dueño.

## Orden de construcción (con las decisiones del dueño)
1. **Bloque A** — P10 (estilo NatGeo) + P6.5 (Curtis) + P2 (mini calendario, fechas límite) + P3 (íconos de urgencia) + P1.4 (etiquetas propias)
2. **Bloque B** — P7.5 (ordenar Drive NIHR, fecha límite diciembre) + P7.2–7.4 (entregar proyecto)
3. **Bloque C** — P6.3–6.4 (memoria «Así trabajás» y automatizaciones) + P5.3–5.4 (frase del día, invitaciones a llenar)
4. **Bloque D** — P9 (LinkedIn: perfil, posts desde proyectos, prospectos) + P8.2 (precios)


## P11 · Conexiones
| # | Conexión | Estado |
|---|---|---|
| 11.1 | Google Drive (crear carpetas, subir, buscar, mover) | 🟡 conectado a Curtis, sin prueba real |
| 11.2 | Zoho Books (clientes, cotizaciones) | 🟡 conectado a Curtis; la prueba de Zoho está vencida |
| 11.3 | Google Calendar solo lectura: reuniones en el calendario, «Reuniones de hoy», aviso 1 h antes y al terminar (anotar acuerdos), Curtis las conoce. Se actualiza cada 15 min | ✅ simulado · ❓ falta prueba real |
| 11.4 | Apple Calendar | — descartado: las reuniones viven en Google Calendar |
| 11.5 | Gmail / Zoom (mensaje de entrega, acuerdos de reuniones) | ⬜ conectores existen en la cuenta, no están en Curtis |


## P12 · Personalidad y marca de Curtis
| # | Circuito | Estado |
|---|---|---|
| 12.1 | Personalidad aplicada (chat, frases, festejos, avisos) | ✅ |
| 12.2 | Logo B: ardilla que se asoma por el marco amarillo, «una ardilla a la vez» | 🟡 falta que el dueño lo vea |
| 12.3 | Técnicas TDAH: estacionamiento de ardillas en Foco; Curtis usa las técnicas en el chat | ✅ |

## Cambios pedidos (construidos en v5)
1. ✅ Proyectos: menú ⋯ en cada tarjeta para renombrar, abrir y borrar.
2. ✅ Hecho: proyecto NIHR y sus 5 tareas borrados (confirmado por el dueño). La hoja «Mi Tablero — registro» enviada a la papelera de Drive. El tablero viejo ya no existía.
3. ✅ Ajustes explicados: cada sección dice qué hace y trae un ejemplo.
4. ✅ Entrega: «Que Curtis revise» (revisión automática: nombres, CMYK/RGB, transparencia, resolución, vectores, carpetas vacías + opinión visual mirando las imágenes) y «Recopilar de Drive» (copia de la carpeta del proyecto y del catálogo; los originales no se tocan).
5. ✅ Google Calendar solo lectura (P11.3).

## P13 · Ilustraciones y licencias
| # | Circuito | Estado |
|---|---|---|
| 13.1 | Catálogo de ilustraciones: subir → miniatura en Curtis + original en Drive («Curtis · Ilustraciones»); nombre, tema, año, link, estado, tamaño de impresión | ✅ simulado |
| 13.2 | Elegir ilustraciones del catálogo para un proyecto (o subir nuevas desde ahí) | ✅ |
| 13.3 | Paquete y precio de licencia: producto, cantidad, exclusividad, duración, territorio, tiraje; pago único / regalía / mixto; diseño aparte; avisos de precio malo; opinión de Curtis | ✅ |
| 13.4 | Propuesta para el cliente (copiar, PDF en Drive, pasar a Zoho) y memoria del precio | ✅ simulado |
| 13.5 | Entrega de licencia con estructura propia (00 Licencia… 04 Crédito y uso) | ✅ simulado |
| 13.6 | Proyecto «Tienda aeropuerto · Naipes» con 5 pasos | ✅ cargado |

## Lo que sigue (bloque D y pendientes)
- P9.1–9.3 LinkedIn: perfil, post desde cada entrega, lista de prospectos con seguimiento. Hoy Curtis ya da consejos en el chat; falta la sección propia.
- Primera prueba real: crear una carpeta en Drive, una entrega chica, una cotización (Zoho tiene la prueba vencida).
- Confirmar día exacto de entrega NIHR.

## Bitácora de actualizaciones
- 2026-10-20 · v1–v3 construidas (ver TABLERO_TRASPASO.md).
- 2026-10-20 · Auditoría por partes. Decisiones del dueño: estilo NatGeo; entrega con archivos subidos + estructura fija + mensaje o PDF de links; memoria amplia (incluye errores y mejoras); LinkedIn primero. Nuevo: ordenar Drive NIHR antes de diciembre. Esperando CONSTRUYE.
- 2026-10-20 · **v4 Curtis** construida: estilo NatGeo, etiquetas, urgencia, calendario, fechas límite, frase del día, invitaciones, memoria «Así trabajás», entrega con estructura fija y PDF de links, orden de Drive NIHR, chat general con Curtis. Prueba: 31/31 nueva + prueba de v3 sin regresiones. Migrado «Logo de nahual» a proyecto. Cargados 8 aprendizajes del paquete Beauty Sleep y el proyecto NIHR.
- 2026-10-20 · PAUSA: pregunta sobre conexiones. Anotado P11.
- 2026-10-20 · PAUSA: Google Calendar solo lectura; personalidad y logo de Curtis; renombrar/borrar proyectos; quitar NIHR; Ajustes confuso; botón de revisión. Anotado P12 y cambios 1–5.
- 2026-10-20 · Decisiones: logo B (ardilla), Ajustes explicado, revisión = opinión visual + recopilar de Drive. Borrados con confirmación: proyecto NIHR + 5 tareas, hoja de Drive (papelera). Esperando CONSTRUYE.
- 2026-10-20 · **v5** construida: logo ardilla, personalidad, Google Calendar solo lectura, menú de proyectos, Ajustes explicados, revisión y recopilación en entregas, catálogo de ilustraciones, licencias con precio y propuesta, estacionamiento de ardillas. Corregido: doble redibujo al salir de un campo (error real). Prueba: 35/35 nueva + 31/31 de v4. Cargado proyecto Tienda aeropuerto · Naipes.
