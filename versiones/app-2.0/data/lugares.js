/* nAIhual · catálogo de lugares (Antigua Guatemala)
   Única fuente de los lugares que usa app/index.html. Se edita aquí, no en el programa.

   Reglas
   - "id" es fijo: no se cambia nunca (los guardados del visitante dependen de él).
   - estado: "borrador" | "publicado" | "pausado" | "retirado".
       borrador  → no lo ve el visitante; solo aparece en la vista interna de revisión.
       publicado → solo cuenta como publicado si además tiene: nombre, dirección, enlace de Maps
                   que funcione (o dirección para armarlo), fuente, fecha_verificacion (AAAA-MM-DD)
                   y verifico. Si le falta algo, la app lo trata como «En revisión».
       pausado / retirado → no se ve en ninguna parte.
   - El recorrido «Quiero un café» muestra hasta 3 cafés publicados, en el orden de esta lista.
     «patrocinado: true» solo agrega la etiqueta «Patrocinado»; no cambia el orden.
   - horario y precio solo se muestran si tienen su fuente (fuente_horario / fuente_precio).
   - maps_url vacío = la app arma el enlace universal de Google Maps con nombre + dirección.
   - Nada inventado: si un dato no se sabe, queda vacío.
   - "mapa": dónde cae en el mapa esquemático de la cuadrícula (avenida 1 = oriente … 7 = poniente; calle 1 = norte … 9 = sur),
     calculado con la dirección. aprox: true = la dirección no da la esquina exacta. Es un esquema, no a escala. Sin mapa = no se dibuja.
   - "pendiente": nota interna para el equipo (qué falta o qué se retiró). No la ve el visitante.
   - El visitante solo ve lugares publicados. Los borradores se revisan en la «Vista interna del equipo».

   Estado al 23-oct-2026: ningún registro tiene fuente, fecha ni persona que verificó.
   Las frases son del fundador. Las direcciones las escribió Claude en oct-2026 sin fuente registrada.
   Por eso todos quedan en "borrador". */
window.NAIHUAL_LUGARES = [
  { id: 'parque', mapa: { avenida: 4.5, calle: 4.5, aprox: false }, nombre: 'Parque Central', categoria: 'cultura', historico: true, direccion: 'Entre 4a y 5a Calle, 4a y 5a Avenida', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['iq', 'noj'],
    frase: { es: 'La plaza principal. A su alrededor están la Catedral, el Palacio de los Capitanes Generales y el Ayuntamiento.', en: 'The main square, framed by the Cathedral, the Palace of the Captains General and City Hall.' } },
  { id: 'catedral', mapa: { avenida: 3.55, calle: 4.65, aprox: false }, nombre: 'Catedral de San José', categoria: 'cultura', historico: true, direccion: 'Lado oriente del Parque Central', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['noj'],
    frase: { es: 'Se empezó a construir en 1545. Los terremotos de 1773 la dañaron: una parte sigue siendo iglesia y otra quedó en ruinas.', en: 'Construction began in 1545. After the 1773 earthquakes, part is still a church and part remains in ruins.' } },
  { id: 'palacio', mapa: { avenida: 4.5, calle: 5.4, aprox: false }, nombre: 'Palacio de los Capitanes Generales', categoria: 'cultura', historico: true, direccion: 'Lado sur del Parque Central', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['noj'],
    frase: { es: 'Fue la sede del gobierno colonial de la Capitanía General de Guatemala.', en: 'Seat of the colonial government of the Captaincy General of Guatemala.' } },
  { id: 'arco', mapa: { avenida: 5, calle: 2, aprox: true }, nombre: 'Arco de Santa Catalina', categoria: 'cultura', historico: true, direccion: '5a Avenida Norte', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['kej', 'iq'],
    frase: { es: 'Del siglo XVII. Unía dos partes de un convento para que las monjas cruzaran la calle sin ser vistas.', en: 'From the 17th century. It joined two parts of a convent so the nuns could cross the street unseen.' } },
  { id: 'merced', mapa: { avenida: 6, calle: 1, aprox: false }, nombre: 'Iglesia de La Merced', categoria: 'cultura', historico: true, direccion: '1a Calle Poniente y 6a Avenida Norte', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['kej', 'noj'],
    frase: { es: 'Iglesia barroca del siglo XVIII, amarilla y con su fachada cubierta de relieves blancos.', en: 'An 18th-century baroque church, yellow, its façade covered in white relief work.' } },
  { id: 'capuchinas', mapa: { avenida: 2, calle: 2, aprox: false }, nombre: 'Convento de las Capuchinas', categoria: 'cultura', historico: true, direccion: '2a Avenida Norte y 2a Calle Oriente', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['e', 'noj'],
    frase: { es: 'Ruinas de un convento del siglo XVIII con una torre circular de celdas.', en: 'Ruins of an 18th-century convent with a circular tower of cells.' } },
  { id: 'santaclara', mapa: { avenida: 2, calle: 6, aprox: false }, nombre: 'Ruinas de Santa Clara', categoria: 'cultura', historico: true, direccion: '2a Avenida Sur y 6a Calle Oriente', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['noj', 'kej'],
    frase: { es: 'Convento de las clarisas. Enfrente está el tanque Unión, lavaderos públicos de la época colonial.', en: 'Convent of the Poor Clares. Across the street is Tanque Unión, the colonial-era public washbasins.' } },
  { id: 'sanfrancisco', mapa: { avenida: 1, calle: 7, aprox: false }, nombre: 'Iglesia de San Francisco el Grande', categoria: 'cultura', historico: true, direccion: '1a Avenida Sur y 7a Calle Oriente', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['noj'],
    frase: { es: 'Aquí está la tumba del Santo Hermano Pedro de San José de Betancur.', en: 'Home to the tomb of Saint Hermano Pedro de San José de Betancur.' } },
  { id: 'doce', mapa: { avenida: 3.7, calle: 3.85, aprox: true }, nombre: '12 Onzas', categoria: 'cafe', direccion: '4a Calle Oriente 5', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['kej'],
    frase: { es: 'No falla con el café, expertos catadores.', en: 'Never misses with coffee. Expert cuppers.' } },
  { id: 'artista', mapa: { avenida: 5, calle: 7.5, aprox: true }, nombre: 'Artista de Café', categoria: 'cafe', direccion: '5a Avenida Sur 34B', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['iq'],
    frase: { es: 'No falla con el café, expertos catadores, pero con una forma super aesthetic de comunicar el amor por el café.', en: 'Never misses with coffee, with a super aesthetic way of sharing their love for it.' } },
  { id: 'komori', nombre: 'Komori', categoria: 'cafe', direccion: '', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: [],
    frase: { es: 'Literal el mejor matcha.', en: 'Literally the best matcha.' } },
  { id: 'siena', mapa: { avenida: 6, calle: 2.5, aprox: true }, nombre: 'Siena Luz', categoria: 'cafe', direccion: '6a Avenida Norte', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['noj'],
    frase: { es: 'La vibe con filosofía y literatura combinada con el mejor café es una experiencia top.', en: 'Philosophy and literature vibes plus the best coffee: a top experience.' } },
  { id: 'fatcat', mapa: { avenida: 3.6, calle: 4.1, aprox: true }, nombre: 'Fat Cat Coffee House', categoria: 'cafe', direccion: '4a Calle Oriente, frente a 12 Onzas', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['kej'],
    frase: { es: 'Especialistas en café.', en: 'Coffee specialists.' } },
  { id: 'alegria', nombre: 'Alegría Café', categoria: 'cafe', direccion: '', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: [],
    frase: { es: 'Especialistas en café.', en: 'Coffee specialists.' } },
  { id: 'coffea', mapa: { avenida: 2.7, calle: 6, aprox: true }, nombre: 'Coffea Cafés Especiales', categoria: 'cafe', direccion: '6a Calle Oriente 18A', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['e', 'kej'],
    pendiente: 'Afirmación retirada hasta tener fuente: «Entre las 100 mejores coffee shops del mundo».',
    frase: { es: 'Especialistas en café.', en: 'Coffee specialists.' } },
  { id: 'cazador', mapa: { avenida: 3, calle: 4.4, aprox: true }, nombre: 'El Cazador Italiano', categoria: 'comida', direccion: '3a Avenida Norte 1B, detrás de la Catedral', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['e'],
    frase: { es: 'Lo mejor si querés la mejor pizza tradicional italiana o panadería italiana.', en: 'The place for the best traditional Italian pizza or Italian bakery.' } },
  { id: 'once', mapa: { avenida: 2.5, calle: 2, aprox: true }, nombre: 'Once Once', categoria: 'comida', direccion: '2a Calle Oriente 22', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['kej'],
    frase: { es: 'Lugar vegano/vegetariano que recomiendo sobre todas las cosas. Cualquier plato de ahí es perfecto.', en: 'A vegan/vegetarian spot I recommend above all. Any dish there is perfect.' } },
  { id: 'hectors', nombre: 'Hector’s Bistro', categoria: 'comida', direccion: '', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: [],
    frase: { es: 'Un 10 en casi todos los platos, aparte de buen ambiente y una cervecería artesanal dentro.', en: 'A 10 on almost every dish, plus a great vibe and a craft brewery inside.' } },
  { id: 'nikolo', nombre: 'Nikolo', categoria: 'comida', direccion: '', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: [],
    frase: { es: 'Fancy cuisine literal. No decepciona.', en: 'Literally fancy cuisine. Never disappoints.' } },
  { id: 'pina', nombre: 'Y Tu Piña También', categoria: 'comida', direccion: '', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: [],
    frase: { es: 'Todo con piña y punto. Perfecto si querés algo diferentemente chill.', en: 'Everything with pineapple, period. Perfect for something differently chill.' } },
  { id: 'patio', mapa: { avenida: 1, calle: 6.3, aprox: true }, nombre: 'Patio de la Primera', categoria: 'comida', direccion: '1a Avenida Sur 17C', maps_url: '', fuente: '', fuente_url: '', fecha_verificacion: '', verifico: '', estado: 'borrador', patrocinado: false, horario: '', fuente_horario: '', precio: '', fuente_precio: '', guardianes: ['iq'],
    frase: { es: 'De todo un poco, pero sobresale el ambiente y lo instagrameable del lugar.', en: 'A bit of everything, but the vibe and how photogenic it is stand out.' } }
];
