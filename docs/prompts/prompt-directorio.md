# Prompt · directorio de Antigua (agente aparte)

Pegá esto en el agente que va a armar el directorio. Lo que devuelva, pasáselo a Claude («cargá el directorio») para que lo revise y lo pase al catálogo de nAIhual.

> Armá un directorio de lugares de Antigua Guatemala para nAIhual, una guía de turismo consciente. Empezá por esta categoría: **[categoría]** (cafe, comida, postres, noche, parque, cultura, hotel, transporte o tienda).
>
> Reglas:
> - Solo lugares que aparezcan en una fuente pública que puedas citar (Google Maps, la web o las redes del negocio, guías de viaje, medios). No inventes nada.
> - Sin horarios, sin precios y sin datos de personas (nombres de empleados, teléfonos personales).
> - Sin significados mayas ni ceremonias.
> - El «contexto» son datos, no opiniones: de quién es (familiar, nacional, cadena, extranjero), desde cuándo y qué lo hace distinto, según la fuente.
> - Si un dato no está en la fuente, dejalo vacío.
> - Incluí también cadenas (Pollo Campero, San Martín…), marcadas como cadena: sirven de contexto.
>
> Devolvé una línea JSON por lugar, exactamente con estos campos:
> `{"nombre": "", "categoria": "", "momento": "", "direccion": "", "maps_url": "", "contexto": "", "redes_o_web": "", "fuente": "", "fuente_url": "", "fecha_consulta": "AAAA-MM-DD"}`
>
> `momento` es uno de: llegue, transporte, hotel, comida, cerca, noche.
