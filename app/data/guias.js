/* nAIhual · ramas de los guardianes y perfiles del visitante.
   Se edita aquí, no en el programa.

   ramas: de qué habla cada guardián primero y de dónde salen sus ideas en «Hoy te sugiere…».
   - tema: su rama, en pocas palabras (también se la dice a Claude).
   - voz: cómo arranca su idea.
   - cats: categorías del catálogo donde busca primero.
   - consejos: «cultura» (los consejos culturales), «costumbre» (los prácticos) o una lista de ids de consejos.
   - playlists: true = también propone playlists a pie.

   perfiles: los interruptores de «¿Cómo venís a Antigua?». Cambian qué se muestra primero, nunca el trato (B3).
   ❓ «Vengo de Guatemala» / «Vengo de otro país» como visitante y turista: propuesta de Claude, falta que Diego la confirme.
   «Agente» no está aquí: necesita permiso y cuenta propia (capa 3). */
window.NAIHUAL_GUIAS = {
  ramas: {
    noj: { tema: { es: 'historia, cultura y el porqué de las cosas', en: 'history, culture and the why of things' }, voz: { es: 'Para entender Antigua:', en: 'To understand Antigua:' }, cats: ['cultura'], consejos: 'cultura' },
    iq: { tema: { es: 'primeros pasos, pausas, cafés, eventos y fiestas', en: 'first steps, breaks, cafés, events and festivities' }, voz: { es: 'Un primer paso:', en: 'A first step:' }, cats: ['cafe', 'parque'], consejos: 'costumbre' },
    kej: { tema: { es: 'rutas a pie, naturaleza, mercados y cuidarse', en: 'walking routes, nature, markets and staying safe' }, voz: { es: 'Un camino en orden:', en: 'A path in order:' }, cats: ['parque', 'cultura'], playlists: true },
    e: { tema: { es: 'artesanos, comida con carácter, pan y noche, comunidades', en: 'artisans, food with character, bread and night, communities' }, voz: { es: 'Directo a lo bueno:', en: 'Straight to the good stuff:' }, cats: ['comida', 'postres', 'noche'] }
  },
  perfiles: [
    { id: 'local', label: { es: 'Vivo aquí', en: 'I live here' }, que: { es: 'vive en Antigua o cerca; ya conoce lo básico', en: 'lives in or near Antigua; already knows the basics' } },
    { id: 'visitante', label: { es: 'Vengo de Guatemala', en: 'I’m from Guatemala' }, que: { es: 'viene de otra parte de Guatemala', en: 'comes from elsewhere in Guatemala' } },
    { id: 'turista', label: { es: 'Vengo de otro país', en: 'I’m from abroad' }, que: { es: 'viene de otro país; puede no hablar español', en: 'comes from abroad; may not speak Spanish' } },
    { id: 'mochilero', label: { es: 'Viajo con poco', en: 'Travelling light' }, que: { es: 'viaja con poco presupuesto y más tiempo', en: 'travels on a small budget with more time' } }
  ]
};
