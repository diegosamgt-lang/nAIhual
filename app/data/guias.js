/* nAIhual · ramas de los guardianes y perfiles del visitante.
   Se edita aquí, no en el programa.

   ramas: de qué habla cada guardián primero y de dónde salen sus ideas en «Hoy te sugiere…».
   - tema: su rama, en pocas palabras (también se la dice a Claude).
   - voz: cómo arranca su idea.
   - cats: categorías del catálogo donde busca primero.
   - consejos: «cultura» (los consejos culturales), «costumbre» (los prácticos) o una lista de ids de consejos.
   - playlists: true = también propone playlists a pie.

   perfiles: los interruptores de «¿Cómo venís a Antigua?». Cambian qué se muestra primero, nunca el trato (B3).
   enfoque: cómo recomienda nAIhual a quien tiene ese perfil (se lo dice a Claude). Perfiles de Diego, 29-oct.
   «Agente» no está aquí: necesita permiso y cuenta propia (capa 3). */
window.NAIHUAL_GUIAS = {
  ramas: {
    noj: { tema: { es: 'historia, cultura y el porqué de las cosas', en: 'history, culture and the why of things' }, voz: { es: 'Para entender Antigua:', en: 'To understand Antigua:' }, cats: ['cultura'], consejos: 'cultura' },
    iq: { tema: { es: 'primeros pasos, pausas, cafés, eventos y fiestas', en: 'first steps, breaks, cafés, events and festivities' }, voz: { es: 'Un primer paso:', en: 'A first step:' }, cats: ['cafe', 'parque'], consejos: 'costumbre' },
    kej: { tema: { es: 'rutas a pie, naturaleza, mercados y cuidarse', en: 'walking routes, nature, markets and staying safe' }, voz: { es: 'Un camino en orden:', en: 'A path in order:' }, cats: ['parque', 'cultura'], playlists: true },
    e: { tema: { es: 'artesanos, comida con carácter, pan y noche, comunidades', en: 'artisans, food with character, bread and night, communities' }, voz: { es: 'Directo a lo bueno:', en: 'Straight to the good stuff:' }, cats: ['comida', 'postres', 'noche'] }
  },
  perfiles: [
    { id: 'local', label: { es: 'Local', en: 'Local' }, que: { es: 'vive en Antigua o cerca', en: 'lives in or near Antigua' },
      enfoque: { es: 'Motivalo a crear experiencias culturales para los visitantes y a apoyar el desarrollo de su comunidad: tours, talleres, artesanía. Dale tips para recibir bien. No le expliqués lo básico.', en: 'Encourage them to create cultural experiences for visitors and support community development: tours, workshops, crafts. Give hosting tips. Skip the basics.' } },
    { id: 'nacional', label: { es: 'Turismo nacional', en: 'From Guatemala' }, que: { es: 'viene de otra parte de Guatemala', en: 'comes from elsewhere in Guatemala' },
      enfoque: { es: 'Que conozca más de su propio país: historia, comunidades, lo de tradición. Hacé conciencia de lo local; evitá lo comercial y lo que desplaza a la gente, mostrando hechos (familiar, desde cuándo, si es cadena).', en: 'Help them know their own country better: history, communities, tradition. Raise local awareness; avoid the commercial and what displaces people, showing facts (family-run, since when, chain or not).' } },
    { id: 'internacional', label: { es: 'Turismo internacional', en: 'From abroad' }, que: { es: 'viene de otro país; puede no hablar español', en: 'comes from abroad; may not speak Spanish' },
      enfoque: { es: 'Contexto y respeto: de quién es, desde cuándo, cómo portarse. Lo local y de tradición antes que lo comercial, con hechos y sin juzgar.', en: 'Context and respect: whose it is, since when, how to behave. Local and traditional before commercial, with facts and no judging.' } },
    { id: 'regular', label: { es: 'Visita regular', en: 'Regular visitor' }, que: { es: 'viene seguido (por ejemplo, fines de semana)', en: 'comes often (for example, on weekends)' },
      enfoque: { es: 'Ya conoce lo básico: lo nuevo, lo que cambió, lo que no ha probado, eventos con fecha.', en: 'Knows the basics: what is new, what changed, what they have not tried, dated events.' } },
    { id: 'mochilero', label: { es: 'Mochilero', en: 'Backpacker' }, que: { es: 'viaja con poco presupuesto y más tiempo', en: 'travels on a small budget with more time' },
      enfoque: { es: 'Hostales, fiestas y actividades, lo que cuesta poco o nada. Sin afirmar precios: «confirmalo».', en: 'Hostels, parties and activities, what costs little or nothing. Never state prices: «check it».' } }
  ]
};
