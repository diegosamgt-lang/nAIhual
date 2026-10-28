/* nAIhual · playlists a pie (Antigua Guatemala)
   Una playlist es una ruta con paradas para ver, comer o descansar, no necesariamente pagadas.
   Hoy las arma nAIhual; con la capa 3 las van a crear los agentes, con su permiso («la playlist de [nombre]»).

   Campos
   - id: fijo (los guardados dependen de él).
   - titulo, momento (cuánto dura o cuándo), intro: { es, en }.
   - autor: quién la armó. guardianes: quién la recomienda.
   - paradas: en orden. Cada una es el id de un lugar del catálogo, o { lugar, hacer: { es, en } } con qué hacer ahí.
     Solo lugares con dirección y en el mapa del centro: si una parada no se puede mostrar, la playlist no aparece.
   - gasto: «gratis» solo si ninguna parada cobra (con fuente); «con_gasto» si hay algo que comprar; vacío = no se sabe.
   - perfiles: para quién sirve primero (local, visitante, turista, mochilero). Solo cambia el orden, nunca esconde.
   Nada inventado: horarios, precios y entradas no se escriben aquí. */
window.NAIHUAL_PLAYLISTS = [
  { id: 'centro', autor: 'nAIhual', guardianes: ['e'], gasto: 'con_gasto', perfiles: ['turista', 'visitante'],
    titulo: { es: 'El corazón de Antigua', en: 'The heart of Antigua' }, momento: { es: 'Una mañana', en: 'A morning' },
    intro: { es: 'La plaza, la Catedral y el Arco, con un café a media mañana.', en: 'The square, the Cathedral and the Arch, with a coffee mid-morning.' },
    paradas: ['parque', 'catedral', { lugar: 'doce', hacer: { es: 'El café de media mañana.', en: 'The mid-morning coffee.' } }, 'palacio', 'arco', 'merced'] },
  { id: 'conventos', autor: 'nAIhual', guardianes: ['kej', 'noj'], gasto: 'con_gasto', perfiles: ['turista', 'visitante'],
    titulo: { es: 'Conventos del oriente', en: 'Convents to the east' }, momento: { es: 'Una tarde', en: 'An afternoon' },
    intro: { es: 'Dos ruinas de conventos y una iglesia viva en el lado oriente. Cierra con cena en un patio.', en: 'Two convent ruins and a living church on the east side. Ends with dinner in a courtyard.' },
    paradas: ['capuchinas', 'santaclara', 'sanfrancisco', { lugar: 'patio', hacer: { es: 'La cena.', en: 'Dinner.' } }] },
  { id: 'norte', autor: 'nAIhual', guardianes: ['kej'], gasto: 'con_gasto', perfiles: ['local', 'visitante'],
    titulo: { es: 'Del Arco a La Merced', en: 'From the Arch to La Merced' }, momento: { es: 'Un par de horas', en: 'A couple of hours' },
    intro: { es: 'La calle del Arco a paso lento, con una pausa para leer.', en: 'The Arch street at an easy pace, with a break to read.' },
    paradas: ['catedral', 'arco', 'merced', { lugar: 'siena', hacer: { es: 'La pausa para leer.', en: 'The break to read.' } }] },
  { id: 'tanque', autor: 'nAIhual', guardianes: ['iq'], gasto: 'con_gasto', perfiles: ['mochilero', 'local'],
    titulo: { es: 'Un café y el Tanque', en: 'A coffee and the Tanque' }, momento: { es: 'Una hora', en: 'An hour' },
    intro: { es: 'Pedí el café para llevar y tomalo sentado en el Tanque La Unión.', en: 'Get your coffee to go and drink it sitting at Tanque La Unión.' },
    paradas: [{ lugar: 'coffea', hacer: { es: 'Pedí tu café para llevar.', en: 'Get your coffee to go.' } },
      { lugar: 'santaclara', hacer: { es: 'Mirá la fachada desde la calle.', en: 'Look at the façade from the street.' } },
      { lugar: 'tanque', hacer: { es: 'Buscá una banca bajo las palmeras.', en: 'Find a bench under the palm trees.' } }] }
];
