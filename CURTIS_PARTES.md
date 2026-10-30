# CURTIS — resumen del proyecto

> Actualizado: 2026-10-30 · versión 12
> Panel: https://claude.ai/artifact/E4qZZG4D5jYK85Krv4WyHW (privado, solo vos lo abrís y lo editás)
> Archivo: `tablero/curtis.html` · Datos y conexiones: `TABLERO_TRASPASO.md` · Personalidad: `CURTIS_PERSONALIDAD.md`
>
> Leyenda: ✅ funciona y probado · 🟡 construido, falta probarlo de verdad · ⬜ por construir · ❓ falta una decisión tuya

---

## 1. Qué es Curtis
Tu socio de estudio dentro de un panel. Mezcla Asana (tareas y proyectos) con Notion (ideas y notas), pensado para TDAH: primero el resumen, una cosa a la vez, todo se guarda solo. Curtis aprende cómo trabajás, te ayuda a cobrar bien, entrega a tu Drive, cotiza en Zoho y lee tu Google Calendar.

**Tus reglas (siempre):**
- Respuestas cortas, una cosa a la vez, de vos, sin palabras técnicas. Nunca te mando código para pegar.
- PAUSA = solo respondo y anoto. CONSTRUYE = ejecuto.
- Reporto con ✅ verificado · 🟡 construido sin probar · ❓ supongo.
- No invento datos. Audito el código antes de publicar.
- Fechas: siempre el día de hoy, o por lo menos año y mes.
- Nada se borra sin tu sí. Nada se crea ni se mueve en Drive o Zoho sin tu permiso en la página. Nunca se borran archivos de Drive. Google Calendar es solo lectura.
- Firme y seco: si un precio está bajo, te lo digo directo.

## 2. Estado en una mirada
| Parte | Qué hace | Estado |
|---|---|---|
| P1 Núcleo | Anotar, editar, borrar, etiquetas | ✅ |
| P2 Tiempo | Resumen, calendario, fechas límite, reuniones de Google Calendar | ✅ (Calendar 🟡 sin prueba real) |
| P3 Urgencia | Íconos de urgencia calculados solos | ✅ |
| P4 Registro | Reuniones con notas grandes conectadas a la cita o la tarea, bitácoras, metas | ✅ simulado |
| P5 TDAH | Foco, ardillas estacionadas, frases, invitaciones | ✅ |
| P6 Curtis IA | Chats, memoria «Así trabajás», automatizaciones | ✅ (respuestas reales 🟡) |
| P7 Proyectos y entregas | Áreas (sombrilla), proyectos, tareas dentro de tareas, entrega ordenada en Drive | ✅ simulado · 🟡 sin prueba real |
| P8 Dinero | Catálogo, cotizaciones, facturas, cobros, suscripciones, gastos, licencias, Zoho | ✅ simulado · Zoho 🟡 |
| P9 Ilustraciones | Catálogo para licenciar | ✅ simulado |
| P10 Archivos | Un lugar para subir | ✅ simulado · 🟡 sin prueba real |
| P11 Conexiones | Drive, Zoho, Calendar | 🟡 sin prueba real |
| P12 Identidad | Logo, letras, frase que cambia, animaciones, frases | ✅ (falta tu visto bueno) |
| P13 Crecimiento | Clientes ✅ · LinkedIn ⬜ | parcial |

---

## 3. Partes y circuitos

### P1 · Núcleo: anotar y editar
| # | Circuito | Estado |
|---|---|---|
| 1.1 | Anotar con + → queda con fecha de hoy | ✅ |
| 1.2 | Todo editable con guardado automático (tarea, proyecto, sección, pasos) | ✅ |
| 1.3 | Borrar con confirmación; lo terminado queda tachado | ✅ |
| 1.4 | Etiquetas que vos creás (nombre, color, ícono) en tareas y proyectos, con filtro | ✅ |

### P2 · Tiempo
| # | Circuito | Estado |
|---|---|---|
| 2.1 | Resumen arriba que se actualiza solo + resumen del día escrito por Curtis | ✅ |
| 2.2 | Mini calendario en Inicio y calendario grande en Mis tareas; tocás un día y ves todo | ✅ |
| 2.3 | Fechas límite con cuenta regresiva (21 días en Inicio, 45 en el calendario) | ✅ |
| 2.4 | Mis tareas por tiempo: atrasadas · hoy · 1–3 días · semana · después · sin fecha | ✅ |
| 2.5 | Google Calendar solo lectura: «Reuniones de hoy», aviso 1 h antes y al terminar (anotar acuerdos); se actualiza cada 15 min | ✅ simulado · 🟡 sin prueba real |

### P3 · Urgencia
| # | Circuito | Estado |
|---|---|---|
| 3.1 | Prioridad alta / normal | ✅ |
| 3.2 | Íconos: atrasada · hoy · 1–3 días · semana · después · esperando · sin fecha | ✅ |

### P4 · Registro
| # | Circuito | Estado |
|---|---|---|
| 4.1 | Bitácora con fecha y horas → suma contra el mínimo del mes | ✅ |
| 4.2 | Una reunión, un lugar: en la cita de Inicio o en una tarea, «Activar notas de reunión» crea UNA reunión conectada (la tarea trae sus notas). Desde Registro también se conecta a una cita | ✅ simulado |
| 4.3 | Notas grandes: título, subtítulo, texto, checklist, numerada, viñetas, negrita; se guardan solas | ✅ |
| 4.4 | Imágenes y archivos en las notas (botón, arrastrar o pegar) → Drive, carpeta «Curtis · Reuniones / AAAA-MM-DD — cita» | ✅ simulado · 🟡 sin prueba real |
| 4.5 | Pendientes ☐ de la checklist → tareas (sin duplicar los que ya pasaste) | ✅ |
| 4.6 | Metas del mes y del año | ✅ |

### P5 · TDAH: foco y ganas de volver
| # | Circuito | Estado |
|---|---|---|
| 5.1 | «Ahora»: una sola cosa | ✅ |
| 5.2 | Reloj de foco 15/25/45 que guarda el tiempo | ✅ |
| 5.3 | Estacionamiento de ardillas: anotás la distracción y volvés | ✅ |
| 5.4 | Frase del día: Curtis la escribe una vez al día (estilo Carl Jung con humor); si no puede, usa una de 30 frases propias | ✅ simulado |
| 5.5 | Invitaciones a llenar (bitácora, acuerdos, esperando hace días, entrega cerca, atrasadas) | ✅ |
| 5.6 | Movimiento sutil: curvas de nivel, festejo al terminar, botones con animación suave | ✅ |

### P6 · Curtis: IA y memoria
| # | Circuito | Estado |
|---|---|---|
| 6.1 | Chat en cada tarea, en cada proyecto y uno general (ver «Cómo funcionan los chats») | ✅ simulado · 🟡 respuestas reales |
| 6.2 | Memoria «Lo que recuerdo de vos»: errores, mejoras, precios, tiempos, horario, pasos, clientes; editable | ✅ |
| 6.3 | «Así trabajás»: calculado de tus datos (tiempos, horario, % tarde, foco, precio por categoría) | ✅ |
| 6.4 | Pasos repetidos por categoría → «Usar como plantilla» | 🟡 falta uso real |
| 6.5 | Curtis puede: agregar tareas y pasos, anotar aprendizajes, buscar/crear/mover en Drive, buscar clientes y cotizar en Zoho, leer tu catálogo y escribir descripciones de servicios | ✅ simulado |

### P7 · Proyectos y entregas
| # | Circuito | Estado |
|---|---|---|
| 7.1 | Proyectos con secciones, lista y tablero, cliente, categoría, entrega, cobro final, etiquetas, carpeta de Drive | ✅ |
| 7.1b | **Áreas** (la sombrilla): agrupa proyectos grandes (ej. NIHR). Página propia con proyectos, pendientes, reuniones y dinero del área. «Convertir en área» desde un proyecto. El menú agrupa por área | ✅ |
| 7.1c | **Tareas dentro de tareas**: «Dentro de» en el detalle, «Tareas dentro» con su avance; en la lista se ven agrupadas | ✅ |
| 7.2 | Menú ⋯ en cada proyecto: abrir, renombrar, borrar | ✅ |
| 7.3 | Carpetas de trabajo en Drive (con permiso) | ✅ simulado · 🟡 sin prueba real |
| 7.4 | Entregar: revisión de calidad → subís archivos → Curtis los ordena en la estructura fija → crea todo en Drive → proyecto Entregado | ✅ simulado con tus archivos de Beauty Sleep |
| 7.5 | Revisión automática (nombres, CMYK/RGB, transparencia, resolución, vectores) + opinión visual de Curtis + «Recopilar de Drive» | ✅ simulado |
| 7.6 | Mensaje de entrega con links + «Mejorar con Curtis» + PDF con el link de cada carpeta | ✅ |

### P8 · Precios y dinero (nuevo en v6)
| # | Circuito | Estado |
|---|---|---|
| 8.1 | Pestaña **Precios → Catálogo**: cada servicio con nombre, subtítulo, grupo (título), precio, cómo se cobra, formato de entrega, tiempo y descripción | ✅ |
| 8.2 | Curtis escribe o mejora la descripción de un servicio (para el cliente, de usted, sin inventar) | ✅ simulado |
| 8.3 | «Que Curtis revise mi catálogo»: qué está barato o caro, qué no se entiende, qué servicio falta | ✅ simulado |
| 8.4 | Cotización rápida: marcás servicios y se suman; o la armás con líneas de tipo Título, Subtítulo, Servicio (cantidad × precio + formato + descripción), Nota y Descuento (Q o %). Subir/bajar/quitar líneas. Se guarda sola | ✅ |
| 8.5 | «De qué se trata el proyecto» → Curtis escribe las descripciones de cada línea | ✅ simulado |
| 8.6 | Copiar texto, PDF (a Drive o a Curtis), duplicar, borrar, estado (borrador · enviada · aceptada · no se dio) | ✅ simulado |
| 8.7 | Pasar a Zoho con descripción, formato y descuento (queda en borrador) | ✅ simulado · 🟡 Zoho con la prueba vencida |
| 8.8 | Desde cada proyecto: «Cotización rápida» con cliente, proyecto y notas ya llenos | ✅ |
| 8.9 | Licencias: cada multiplicador (volumen, exclusividad, duración, territorio, tiraje) muestra su ×, explica qué suma y por qué, cuánto dinero mueve, se edita y se apaga. Mínimo y regalía editables. «Usar siempre estos valores» / «Volver a los de Curtis» | ✅ |
| 8.10 | Cada cotización y propuesta se anota en la memoria de precios | ✅ |
| 8.11 | La pestaña se llama **Dinero**: Resumen · Cotizaciones · Facturas · Catálogo · Gastos | ✅ |
| 8.12 | Cada cotización termina en factura (total o anticipo 50% + saldo). Marcar pagada → entra a tus números y a la memoria | ✅ |
| 8.13 | Factura a Zoho «Creatif» en borrador y «Leer facturas de Zoho»: las pagadas se marcan solas y trae las que no están en Curtis | ✅ simulado · 🟡 sin prueba real |
| 8.14 | Cobro final por proyecto + franja Cobro final · Cotizado · Facturado · Cobrado | ✅ |
| 8.15 | Resumen: cobrado del mes y del año, por cobrar, gastos, lo que te queda, gráfica de 6 meses con tabla, tabla por proyecto | ✅ |
| 8.16 | Suscripciones (mensual/anual, Q o US$) y gastos/inversiones/ingresos sueltos; tipo de cambio para sumar dólares | ✅ |

### P9 · Ilustraciones
| # | Circuito | Estado |
|---|---|---|
| 9.1 | Catálogo: subir → miniatura en Curtis + original en Drive («Curtis · Ilustraciones»); nombre, tema, año, estado, tamaño de impresión | ✅ simulado |
| 9.2 | Elegir ilustraciones para un proyecto de licencia | ✅ |
| 9.3 | Propuesta de licencia: copiar, PDF en Drive, pasar a Zoho | ✅ simulado |
| 9.4 | Entrega de licencia con estructura propia (00 Licencia… 04 Crédito y uso) | ✅ simulado |

### P10 · Archivos (nuevo en v6)
| # | Circuito | Estado |
|---|---|---|
| 10.1 | **Proyectos → Archivos**: arrastrás o elegís archivos; elegís proyecto o «Bandeja» | ✅ simulado |
| 10.2 | Dentro de cada proyecto: «Archivos del proyecto» sube a la carpeta del proyecto en Drive | ✅ simulado |
| 10.3 | Pide permiso y dice adónde va cada archivo; sin carpeta de proyecto van a «Curtis · Bandeja» | ✅ |
| 10.4 | Sin Drive en esa vista, se guardan en Curtis (imágenes, PDF, video, texto; hasta 20 MB) | ✅ simulado |
| 10.5 | Quitar de la lista no borra nada en Drive | ✅ |

### P11 · Conexiones
| # | Conexión | Estado |
|---|---|---|
| 11.1 | Google Drive: crear carpetas, subir, buscar, mover, copiar | 🟡 sin prueba real |
| 11.2 | Zoho Books «Creatif»: clientes y cotizaciones en borrador | 🟡 la prueba de Zoho está vencida |
| 11.3 | Google Calendar: solo lectura | 🟡 sin prueba real |
| 11.4 | Apple Calendar | — descartado |
| 11.5 | Gmail / Zoom | ⬜ existen en tu cuenta, no están en Curtis |

### P12 · Identidad y personalidad
| # | Circuito | Estado |
|---|---|---|
| 12.1 | Estilo National Geographic: papel cálido, bosque, musgo, tierra, lago y el marco amarillo | ✅ |
| 12.2 | Logo v6: ícono minimalista, marco amarillo y una ardilla que se asoma con la cola detrás; la cola se mueve de vez en cuando | 🟡 falta tu visto bueno |
| 12.3 | «CURTIS» en mayúsculas condensadas y espaciadas, estilo revista (inspiración, no copia) | 🟡 falta tu visto bueno |
| 12.4 | La frase de abajo cambia cada 9 segundos (12 frases tipo guía de campo) | ✅ |
| 12.5 | Botones con animación tipo Apple (se hunden al tocar, tarjetas que suben); se apaga si tu equipo pide menos movimiento | ✅ |
| 12.6 | Frases estilo Carl Jung con humor (30 propias + la del día de Curtis) | ✅ |
| 12.7 | v7 jerarquía editorial: títulos más grandes, regla negra sobre cada sección, etiquetas en mayúsculas espaciadas, números grandes en serif, marco amarillo en lo activo, tarjetas con borde fino | 🟡 falta tu visto bueno |

### P13 · Crecimiento: clientes y LinkedIn
| # | Circuito | Estado |
|---|---|---|
| 13.0 | **Clientes** (Proyectos → Clientes): ficha con contacto, notas, conexión con Zoho, proyectos, cotizaciones, cuánto te ha pagado y cuánto te debe. Detecta nombres sueltos y los guarda con un toque. En el proyecto: elegir cliente y «Ver cliente» | ✅ |
| 13.1 | Al entregar, Curtis propone un caso de estudio o post para LinkedIn | ⬜ |
| 13.2 | Consejos para tu perfil (titular, acerca de, destacados) | ⬜ |
| 13.3 | Lista de prospectos con seguimiento | ⬜ |

---

## 4. Cómo funcionan los chats con Curtis
- Hay tres tipos: uno en **cada tarea**, uno en **cada proyecto** y uno **general** en la página «Curtis».
- Cada chat vive guardado en su tarea, su proyecto o en la página Curtis. Cuando volvés, sigue donde lo dejaste (guarda los últimos 30 mensajes). No es un chat nuevo cada vez.
- Cada vez que preguntás, el panel le manda a Curtis esa conversación + lo que está pasando (tus pendientes, el proyecto, reuniones de hoy, tu catálogo) + «Lo que recuerdo de vos». Por eso parece que se acuerda.
- «Lo que recuerdo de vos» es compartido por todos los chats. Ahí queda lo importante, aunque el chat se borre.
- Usa tu cuenta de claude.ai. Es aparte de esta conversación donde construimos Curtis: yo aquí no veo tus chats del panel, salvo que me pidás revisar tus datos.

## 5. Decisiones tuyas
- Escribís directo en el panel (nada de hojas de cálculo).
- Estilo National Geographic, minimal pero orgánico y vivo.
- Entrega: vos subís, Curtis ordena en una estructura fija, crea el mensaje y el PDF de links.
- Memoria amplia: errores, mejoras, horario, tiempos, precios, clientes, pasos.
- LinkedIn es el primer canal para clientes (pendiente).
- Google Calendar solo lectura.
- Logo con ardilla en el marco; v6: más minimalista, sin «una ardilla a la vez».
- Proyecto NIHR, hoja de Drive y tablero viejo: borrados con tu sí.
- Licencias: primer producto de prueba con pago único, no exclusiva, 1 año, Guatemala, hasta 1,000 unidades.

## 6. Límites que tenés que saber
- Subir desde el panel: hasta 16 MB por archivo a Drive (20 MB si se guarda en Curtis). Carpetas pesadas: subilas directo a Drive y Curtis las ordena.
- Drive, Zoho y Calendar solo están probados con simulación. Falta una prueba real.
- Zoho tiene la prueba vencida: crear cotizaciones puede fallar hasta activar un plan.
- Curtis no puede entrar a LinkedIn ni navegar internet desde el panel.
- Las letras CURTIS son una aproximación: la fuente de National Geographic es de pago y su logo es un dibujo a medida.

## 6b. Dónde se guardan las cosas
- Todo lo que escribís: en el registro privado de Curtis (solo vos).
- Imágenes de reuniones y archivos: en tu Google Drive. Si instalás «Google Drive para escritorio», esas carpetas también aparecen en tu compu. El panel no puede escribir directo en tu compu (el navegador no lo deja).

## 7. Lo que sigue
1. Tu visto bueno a la nueva jerarquía visual, áreas, notas y Dinero.
2. ¿Borro la reunión vacía del 21 oct? (Nada se borra sin tu sí.)
3. ¿En qué calendario están tus reuniones? Tu Google Calendar principal no tiene citas del 14 oct al 3 nov.
4. Llenar tu catálogo, tus clientes y tus suscripciones (con datos reales).
5. Primera prueba real: una carpeta en Drive, subir un archivo, una entrega chica, una cotización y una factura en Zoho.
6. P13 LinkedIn.
7. Confirmar día exacto de entrega NIHR.

## 8. Bitácora
- 2026-10-20 · v1: escritura directa, estilo graffiti saturado. v2: diseño sobrio, guía, chat por tarea. v3: rehecho como Asana + Notion para TDAH.
- 2026-10-20 · Auditoría por partes y decisiones (estilo NatGeo, entrega ordenada, memoria amplia, LinkedIn primero).
- 2026-10-20 · **v4 Curtis**: etiquetas, urgencia, calendario, fechas límite, frase del día, invitaciones, memoria, entregas, chat general. 31/31 pruebas.
- 2026-10-20 · **v5**: logo ardilla, personalidad, Google Calendar solo lectura, menú de proyectos, Ajustes explicados, revisión de entregas, ilustraciones y licencias. 35/35 + 31/31 pruebas. Proyecto Tienda aeropuerto · Naipes cargado.
- 2026-10-21 · **v6**: pestaña Precios (catálogo + cotizaciones rápidas con títulos, subtítulos, servicios, notas y descuentos; Curtis escribe y revisa descripciones; PDF, Zoho, duplicar), multiplicadores de licencia editables y explicados, lugar para subir archivos (general y por proyecto), logo minimalista, «CURTIS» estilo revista, frase que cambia, animaciones tipo Apple, frases estilo Jung con humor, cada chat dice dónde se guarda. Error que ya venía de antes y quedó corregido: las descripciones se perdían al pasar una cotización a Zoho. Encontrados en las pruebas y corregidos antes de publicar: la cotización nueva se cerraba sola, un signo menos que el PDF no podía dibujar y el chat de una tarea podía recibir más herramientas de las permitidas. Pruebas: 74/74 nuevas + 31/31 de v4.
- 2026-10-21 · **v7**: Áreas (sombrilla de proyectos; NIHR convertida en área con «NIHR · General» adentro), tareas dentro de tareas (la propuesta del naipe quedó dentro de «Diseñar el naipe»), reuniones con notas grandes conectadas a la cita o la tarea (títulos, checklist, numerada, fotos a Drive), clientes, Dinero (facturas por cotización, Zoho facturas, cobro final, resumen con gráfica, suscripciones y gastos), jerarquía visual editorial. La reunión con Daisy quedó conectada a su tarea con las notas más completas. Corregidos: la ventana de notas se cerraba al pedir permiso para subir una imagen; la checklist se encogía por un choque de estilos; las tareas agregadas con «Agregar tarea» no aparecían hasta tocar afuera (venía de antes); el tipo de cambio no se aplicaba al momento. Pruebas: 108/108 nuevas + 31/31 de v4.

## 9. Auditoría honesta (2026-10-21, PAUSA, después de la v7)
- **Nota:** la idea va 8/10 y el uso real 4/10. Hay 7 secciones y unas 4,000 líneas de código, pero en el panel solo hay 11 cosas anotadas y la primera reunión real quedó repetida 3 veces. Lo que falla es la claridad, no la falta de funciones.
- **Lo más importante:**
  1. Probar Drive, Zoho y Calendar con tu cuenta real antes de construir nada nuevo. Tu calendario principal está vacío.
  2. Revisar si las facturas de Zoho valen como factura legal (FEL de la SAT). Si no, Curtis solo lleva el control y la factura legal sale de otro lado.
  3. Respaldo: hoy todo vive solo dentro del panel. Falta un botón «Guardar copia en Drive», sobre todo por el dinero.
- **Simplificar:**
  - Inicio tiene unos 12 bloques. Dejar solo «Ahora», «Hoy», «Citas de hoy» y un aviso.
  - Hay cosas repetidas: «Pasos chicos» y «Tareas dentro»; tres botones distintos para cotizar; archivos en 3 lugares.
  - 7 pestañas en el celular son demasiadas.
- **Poco útil o que distrae:**
  - La frase que cambia cada 9 segundos: es una ardilla en movimiento.
  - La frase del día escrita por Curtis gasta tu cuenta todos los días.
  - Las bitácoras NIHR, si ya no las usás.
- **Lo que quedó pendiente:** conseguir clientes y LinkedIn, que era la meta del inicio.
- **Propuesta:** 2 semanas sin funciones nuevas. Usarlo todos los días y después cortar lo que no usaste.
- 2026-10-22 · **v8 (simplificar, según la auditoría)**:
  - Google Calendar lee todos tus calendarios, incluido iCloud («Diego - Disart»), menos los feriados; se eligen en Ajustes. Corregido: las citas en hora universal podían caer en el día equivocado de noche. Verificado con tu cuenta real: la lista de calendarios y las citas de iCloud llegan bien.
  - Inicio con 4 cosas: Ahora, un solo aviso, Citas de hoy y Hoy (los pasos agrupados bajo su tarea). El calendario y las fechas límite viven en Mis tareas → Calendario. La guía y el resumen de Curtis pasaron a la página Curtis.
  - En el celular, 5 pestañas: la última es «Más» (Registro, Foco, Curtis y Ajustes).
  - La frase de abajo del nombre ya no se mueve (cambia una vez al día). La frase del día ya no la pide Curtis solo.
  - Pasos chicos y tareas dentro son ahora una sola cosa: «Pasos (tareas dentro)». Curtis también parte en pasos de esa forma.
  - Un solo botón para cotizar en el proyecto. La licencia pasa a una cotización de Curtis, y de ahí a Zoho y a la factura.
  - Las bitácoras NIHR se esconden si no ponés mínimo de horas ni tenés ninguna.
  - Copia de seguridad: Ajustes → «Guardar copia en Drive» (archivo en «Curtis · Copias»). Si pasan 7 días sin copia, aparece un aviso.
  - Factura legal: no encontré que Zoho emita la FEL de Guatemala. Curtis lleva el control y cada factura tiene un campo para el número FEL de la SAT.
  - Pruebas: 124/124 nuevas + 31/31 de v4. Drive: comprobado con una búsqueda real (solo lectura) que responde como el panel espera.
- 2026-10-27 · Tus pedidos, ordenados:
  1. Un botón para actualizar los proyectos.
  2. Curtis en Inicio.
  3. Saludo más tuyo: «¿Qué onda?» en vez de «Buenos días».
  4. En cada proyecto, un desplegable de Curtis: escribís una idea, duda o problema; Curtis te hace hasta 5 preguntas para entenderlo y después te sugiere. Cada proyecto tiene un contexto corto en .md que se actualiza solo con tus avances.
  5. Que Curtis sea una inteligencia aparte con contexto de todo lo que hacés, como Jarvis, sin nada caro ni complicado.
  6. Un apartado más grande que un proyecto: tu página web, tu portafolio y tu curaduría.
  7. Límite de autoría: lo gráfico y creativo es tuyo. Si Curtis está haciendo casi todo por vos, que lance el aviso y aprenda hasta dónde puede llegar sin ser el autor.
  8. Más emojis; la barrita de color de cada proyecto con el color de su etiqueta; más colores para etiquetas.
- 2026-10-27 · **v9**:
  - «Actualizar» en Proyectos y en cada proyecto.
  - Caja «Preguntale a Curtis» en Inicio.
  - El saludo ahora es «¿Qué onda?» y cambia según la hora.
  - «Curtis del proyecto»: desplegable con cuestionario de 2 a 5 preguntas, sugerencia, pasos que agregás vos con un toque, contexto .md (editar, subir .md, guardar en Drive, deshacer) y «Así va», que se arma solo. El contexto de cada proyecto entra en todos los chats.
  - Límites de autoría: aviso en chats y consultas, contador, aviso de delegación y listas editables. Curtis las respeta siempre.
  - Área principal «Mi estudio» con Página web, Portafolio y Curaduría.
  - 12 colores y 60 emojis. La barrita de color de cada proyecto (en el menú y en las tarjetas) usa el color de su primera etiqueta.
  - Pruebas: 142/142 nuevas + 31/31 de v4.
- 2026-10-29 · Pedido: «está muy saturado; menos texto junto, más tranquilidad, espacio y menos gritado». Además: incorporar tu página web (https://diegosam.wixsite.com/diegosamgt), donde va a entrar NAIHUAL y todo tu trabajo.
- 2026-10-29 · **v10 (calma)**:
  - Más espacio entre bloques y dentro de las tarjetas. Títulos más chicos y suaves. Sin reglas negras ni etiquetas en mayúsculas. Bordes y sombras más suaves. Marco amarillo más delgado.
  - 18 explicaciones largas acortadas o quitadas. La caja de Curtis en Inicio quedó sin atajos.
  - En el proyecto, a la vista: cliente, entrega, cobro final, estado, botones y tareas. Plegado: «Más detalles», Curtis del proyecto, Dinero, Notas y Archivos. Los colores del encabezado aparecen al pasar el mouse.
  - Tu sitio: leído desde tu Wix (solo lectura). Es «diegosamgt», publicado, con plan gratis, en español y con contacto hello@diegosam.com. El proyecto «Página web» tiene el link «🌐 Abrir el sitio» y su contexto con esos datos y «Lo que va a entrar: NAIHUAL».
  - Pruebas: 142/142 + 31/31.
- 2026-10-29 · Zoho conectado a «CREATIF» `877643427` (Zoho Invoice). Verificado antes de cambiar: existe, sos admin, y lee tus clientes y facturas reales. Se dejó de usar `914134862` (Books, prueba vencida).
- 2026-10-30 · Pedido: cargar el paquete de «Mi estudio» que armaste en otro chat; que todas las ventanas se puedan plegar; ordenar mejor el Inicio jugando con tamaños; títulos de proyectos más grandes e íconos de un solo color.
- 2026-10-30 · **v11**:
  - Inicio en dos columnas en pantallas grandes: a la izquierda Resumen y Hoy; a la derecha Curtis, Citas de hoy y Próximas entregas (nuevo).
  - Toda sección con título se pliega con su flechita y se recuerda en ese equipo.
  - Íconos de proyectos y áreas en un solo color: el de su etiqueta o el del proyecto.
  - Títulos de proyectos más grandes.
  - Datos cargados:
    - «Mi estudio» con su descripción nueva.
    - Página web (sitio www.disartstudio.com), Portafolio y Curaduría, cada uno con su contexto .md y la etiqueta «Disart».
    - 21 tareas sin fecha en su sección. Las 7 creativas llevan la etiqueta «Es mío».
    - Proyectos nuevos: «CV y LinkedIn» (en Mi estudio) y «NAIHUAL» (fuera del área, en pausa).
    - «Orden del disco duro» no se creó como proyecto: ya es una tarea de Curaduría.
  - Pruebas: 146/146 + 31/31.
- 2026-10-30 · Pedido: poder elegir si el menú va abajo o a la izquierda (abajo no te gusta, pero a veces sirve); la diagramación en dos columnas no te gustó.
- 2026-10-30 · **v12**:
  - Menú abajo o a la izquierda: se elige en «Más» → «Menú» y aplica en celular y pantallas medianas. En la compu el menú ya está a la izquierda.
  - El Inicio vuelve a una columna por defecto, en este orden: Resumen, Curtis, Citas de hoy, Hoy y Próximas entregas. Arriba a la derecha hay un selector para cambiar a dos columnas.
  - Las dos preferencias se recuerdan en cada equipo.
  - Arreglado: los títulos de las secciones de un proyecto se salían de la pantalla en pantallas angostas.
  - Pruebas: 149/149 + 31/31.
