/* nAIhual · referencias del paisaje en el mapa (Antigua Guatemala)
   Solo para ubicarse: un ícono al borde del mapa dice que algo está AFUERA del centro y hacia dónde.
   No es una ficha ni una recomendación. El mapa del centro es un esquema, no a escala.

   - rumbo: grados desde el norte, en el sentido del reloj, medidos desde el Parque Central (14.55689, -90.73368).
     Sale de las coordenadas de la fuente. aprox: true = la fuente no da el punto exacto (lleva ≈).
   - mapa: para lo que cae en el borde del centro (avenida, calle), como en lugares.js.
   - lugar: si ya está en el catálogo, se usa su punto del mapa.
   - tipo: volcan · cerro · pueblo · ruina. */
window.NAIHUAL_REFERENCIAS = [
  { id: 'cerro', tipo: 'cerro', nombre: 'Cerro de la Cruz', rumbo: 10, aprox: true, fuente: 'Sin coordenadas publicadas; ángulo de la brújula del paisaje (≈)' },
  { id: 'jocotenango', tipo: 'pueblo', nombre: 'Jocotenango', rumbo: 339, fuente: 'Wikipedia · Jocotenango (14°34′55″N 90°44′37″W)', fuente_url: 'https://en.wikipedia.org/wiki/Jocotenango' },
  { id: 'santaana', tipo: 'pueblo', nombre: 'Santa Ana', rumbo: 138, fuente: 'HMDB · marcador frente a la iglesia de Santa Ana (14°32.882′N 90°43.532′W)', fuente_url: 'https://hmdb.org/m.asp?m=95876' },
  { id: 'sancristobalbajo', tipo: 'pueblo', nombre: 'San Cristóbal El Bajo', rumbo: 146, fuente: 'Bamwor (14.5376, -90.7203)', fuente_url: 'https://bamwor.com/en/countries/guatemala/cities/san-cristobal-el-bajo' },
  { id: 'sancristobalalto', tipo: 'pueblo', nombre: 'San Cristóbal El Alto', rumbo: 135, aprox: true, fuente: 'ONU Turismo · Best Tourism Villages: a unos 5 km al sureste del centro', fuente_url: 'https://tourism-villages.unwto.org/en/villages/san-cristobal-el-alto/' },
  { id: 'agua', tipo: 'volcan', nombre: 'Volcán de Agua', rumbo: 185.6, fuente: 'Wikipedia · coordenadas del volcán (como la brújula)' },
  { id: 'fuego', tipo: 'volcan', nombre: 'Volcán de Fuego', rumbo: 240, fuente: 'Wikipedia · coordenadas del volcán (como la brújula)' },
  { id: 'santodomingo', tipo: 'ruina', nombre: 'Santo Domingo', mapa: { avenida: 0.7, calle: 3, aprox: true }, fuente: 'INGUAT · 3a Calle Oriente #28', fuente_url: 'https://selloq.inguat.gob.gt/index.php/en/zoo/item/hotel-casa-santo-domingo' },
  { id: 'sanjeronimo', tipo: 'ruina', nombre: 'San Jerónimo', mapa: { avenida: 7.35, calle: 2.2, aprox: true }, fuente: 'GPSmyCity · ruinas de Antigua (borde poniente)', fuente_url: 'https://gpsmycity.com/tours/the-ruins-of-antigua-4154.html' },
  { id: 'recoleccion', tipo: 'ruina', nombre: 'La Recolección', mapa: { avenida: 7.35, calle: 1, aprox: true }, fuente: 'GPSmyCity · al final de la 1a Calle Poniente', fuente_url: 'https://www.gpsmycity.com/attractions/ruins-of-recoleccion-34260.html' },
  { id: 'catedral', tipo: 'ruina', lugar: 'catedral' },
  { id: 'capuchinas', tipo: 'ruina', lugar: 'capuchinas' },
  { id: 'santaclara', tipo: 'ruina', lugar: 'santaclara' },
  { id: 'tanque', tipo: 'parque', lugar: 'tanque' }
];
