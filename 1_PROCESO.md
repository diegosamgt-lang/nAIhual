# 1 · EL PROCESO — fases en orden

> Cada fase tiene una **salida**: algo concreto que tiene que existir antes de pasar a la
> siguiente. Si la salida no existe, no se avanza. Saltarse fases fue lo que más tiempo
> costó la primera vez.

---

## FASE 0 — Quién, qué y para quién
**Objetivo:** entender el negocio antes de pensar en tecnología.

- Quiénes son las personas, qué hace cada una, quién decide.
- Qué estructura legal o formal hay (empresa, marcas, socios).
- Qué ya funciona hoy, aunque sea a mano.

**Salida:** un párrafo que describa el negocio y una tabla de personas con su rol.

---

## FASE 1 — El objetivo en una frase y la prueba final
**Objetivo:** saber exactamente cuándo el proyecto está terminado.

- El objetivo, en palabras del dueño, en una o dos frases.
- **La prueba final:** una escena concreta que demuestra que funciona.
  *Ejemplo de forma:* «Una persona pregunta X y en 10 segundos recibe Y, sin que nadie intervenga.»

**Salida:** la frase del objetivo y la escena de la prueba final, escritas.

---

## FASE 2 — Inventario: qué existe y qué es la fuente de verdad
**Objetivo:** no reconstruir lo que ya sirve.

- Listar cada herramienta, archivo, cuenta, calendario, formulario o canal que ya se usa.
- Para cada dato importante: **¿dónde vive la versión verdadera?** Solo puede haber una.
- Marcar qué es **intocable** (lo que funciona y no se debe modificar).

**Salida:** tabla «dato → dónde vive → quién lo escribe → ¿se puede tocar?».

---

## FASE 3 — Auditoría con datos reales
**Objetivo:** construir sobre lo que de verdad existe, no sobre lo que suponemos.

- Abrir **por lo menos 3 ejemplos reales** de cada cosa (mensajes, reservas, documentos…).
- Anotar cómo vienen escritos de verdad: formatos, idiomas, errores, excepciones.
- Preguntar ante cada ejemplo: **¿esto es REGLA o es UNA VEZ?**

**Salida:** lista de hallazgos reales, cada uno marcado como regla o excepción.

---

## FASE 4 — Circuitos
**Objetivo:** dividir el proyecto en flujos chicos que se puedan terminar uno por uno.

- Un **circuito** = algo pasa en la vida real → termina en un resultado verificable.
- Numerarlos (1, 2, 3…). Cada uno con: disparador, pasos, resultado, quién lo usa.
- Tablero de estado: ✅ corriendo · 🟡 a medias · ⬜ sin empezar.

**La alarma anti-desvío:** antes de construir cualquier cosa, preguntar
**«¿qué circuito cierra esto?»**. Si no hay número, es desvío y no se construye.

**Salida:** el tablero de circuitos.

---

## FASE 5 — Acceso, cuentas e identidad (HACERLO TEMPRANO)
**Objetivo:** que las personas reales puedan entrar desde el día uno.

- ¿Quién va a usarlo? ¿Desde qué dispositivo y qué cuenta?
- ¿Cómo sabe el sistema quién es cada persona?
- **Probar la entrada con una persona real que NO sea el dueño, antes de construir el resto.**

**Salida:** captura de pantalla de una persona real entrando con éxito.

---

## FASE 6 — Plan en PAUSA
**Objetivo:** acumular decisiones sin construir a ciegas.

- En PAUSA se responde, se anota y se acumula la lista de cambios.
- Se ordena por prioridad: primero lo que desbloquea a otros.
- Nada se construye hasta que el dueño diga **CONSTRUYE**.

**Salida:** lista numerada de cambios para la próxima versión.

---

## FASE 7 — Construcción por bloques
**Objetivo:** avanzar sin romper lo que ya funciona.

- Un bloque a la vez. No se empieza el siguiente sin cerrar el anterior.
- **Una sola mano edita cada archivo.** Si dos IA o dos personas tocan lo mismo, se pierde trabajo.
- Lo que funciona no se toca.

**Salida:** el bloque construido y publicado.

---

## FASE 8 — Verificación de punta a punta
**Objetivo:** que «listo» signifique listo.

Un bloque se cierra solo si:
- produce el resultado correcto en el lugar correcto;
- no duplica si se repite;
- se probó **después** de publicar, con datos reales;
- se midió (tiempo, cantidad) y se anotó el número.

**Salida:** evidencia (captura, número, conteo) de que funciona.

---

## FASE 9 — Prueba con usuarios reales
**Objetivo:** que lo use quien lo va a usar, no quien lo construyó.

- Darle acceso a 1 o 2 personas reales con instrucciones simples.
- Recoger su feedback tal cual (capturas, mensajes).
- Ajustar solo lo que ellas reporten.

**Salida:** feedback real y lista de ajustes.

---

## FASE 10 — Diseño visual (AL FINAL, no al principio)
**Objetivo:** que se vea bien sin romper la lógica.

- Primero que funcione. Después que se vea bien.
- Definir un sistema: pocos tamaños de letra, una escala de espacios, colores con significado.
- El diseño nunca cambia qué datos se muestran ni de dónde salen.

**Salida:** sistema visual aplicado y probado en celular y computadora.

---

## FASE 11 — Traspaso y memoria del proyecto
**Objetivo:** que cualquiera (persona o IA) pueda continuar sin la conversación original.

- **Documento de traspaso:** qué existe, dónde, reglas, errores conocidos, qué falta.
- **Historial de versiones:** un solo archivo que se va actualizando, nunca uno nuevo por versión.
- **Prompt de continuación:** qué hizo el anterior, qué no se debe deshacer, qué sigue.

**Salida:** los tres documentos actualizados.

---

## Resumen en una línea por fase

| # | Fase | Pregunta clave |
|---|---|---|
| 0 | Quién y qué | ¿Quién hace qué en este negocio? |
| 1 | Objetivo | ¿Cuál es la escena que prueba que funciona? |
| 2 | Inventario | ¿Dónde vive la versión verdadera de cada dato? |
| 3 | Auditoría | ¿Esto es regla o fue una vez? |
| 4 | Circuitos | ¿Qué circuito cierra esto? |
| 5 | Acceso | ¿Ya entró una persona real que no sea el dueño? |
| 6 | Pausa | ¿Está en la lista y priorizado? |
| 7 | Construcción | ¿Hay una sola mano en este archivo? |
| 8 | Verificación | ¿Lo probé después de publicar, con datos reales? |
| 9 | Usuarios | ¿Qué dijo quien lo usa de verdad? |
| 10 | Diseño | ¿Funciona primero? |
| 11 | Traspaso | ¿Otro podría seguir sin preguntarme nada? |
