# Curtis → Google Apps Script (camino de salida)

> Escrito el 2026-11-04, con la versión 15. Esto es un plan: todavía no se ha migrado nada.

## Por qué
Hoy Curtis vive en claude.ai, que le da:
- el registro de datos;
- los conectores (Drive, Calendar y Zoho);
- a Claude.

Si Curtis pasa a un Google Apps Script, queda en tu cuenta de Google, abre desde un link tuyo y no depende de esta página.

## Qué cambia y qué se queda
| Pieza | Hoy (claude.ai) | En Apps Script |
|---|---|---|
| Página | `tablero/curtis.html` | La misma página, servida con `HtmlService` (`doGet`) |
| Datos (`S.db`) | Registro de la página (`db`) | Una Google Sheet (una hoja por colección) o Firestore; JSON por fila |
| Google Drive | Conector `mcp` | `DriveApp` (nativo, sin permisos extra) |
| Google Calendar | Conector `mcp`, solo lectura | `CalendarApp` / Calendar Advanced Service (solo lectura) |
| Zoho Invoice | Conector `mcp` | `UrlFetchApp` + OAuth de Zoho (librería OAuth2 de Apps Script); el token se guarda en `PropertiesService` |
| Claude (`sample`) | Incluido en claude.ai | API de Anthropic con `UrlFetchApp`; la llave va en `PropertiesService`, nunca en la página |
| Archivos subidos (`assets`) | Almacén de la página | Una carpeta de Drive |

## Cómo está preparado el código
Toda la página habla con el exterior por **cuatro puertas**. Migrar es cambiar lo que hay detrás de cada una, no reescribir Curtis:
1. **`S.db`**: `collection(...)`, `doc(...)`, `get`, `set`, `update`, `delete` y `onSnapshot`. En Apps Script se reemplaza por un adaptador con la misma forma que llama a `google.script.run`. `onSnapshot` se imita releyendo cada pocos segundos o al volver a la pestaña.
2. **`S.mcp.callTool(servidor, herramienta, args)`**: devuelve `{ payload }`. El adaptador traduce cada nombre a una función del servidor:
   - `list_events` → `CalendarApp`;
   - `create_file` → `DriveApp`;
   - `list_estimates` y `get_estimate` → Zoho por `UrlFetchApp`.

   Se puede devolver la misma forma de `payload`, así el resto del código no cambia.
3. **`S.sample(prompt, opts)`**: una función del servidor que llama a la API de Anthropic. Las herramientas (`tools`) siguen definidas en la página; el servidor solo pasa los mensajes.
4. **`S.assets.upload(blob)`**: sube a una carpeta de Drive y devuelve un link.

Lo que se guarda en el navegador sigue igual (`localStorage`: widgets, bloques de Mis tareas, menú, plegados).

## Pasos sugeridos (en orden)
1. **Copia de seguridad.** Exportar todo desde Ajustes → Copia de seguridad (JSON en Drive). Ese archivo es la semilla de la Sheet.
2. **Proyecto de Apps Script** con `doGet()` que sirve `curtis.html` y un archivo `Datos.gs` (leer y escribir filas JSON en la Sheet).
3. **Adaptador `S.db`** en la página (`if (google && google.script) usar Apps Script; si no, claude.ai`). Probar solo con tareas.
4. **Calendar y Drive** con servicios nativos.
5. **Zoho**: registrar una app en la consola de Zoho (Self Client o Server-based) y guardar el token. Primero solo lectura: `list_estimates`, `get_estimate` y `list_invoices`.
6. **Claude**: llave de la API de Anthropic en propiedades del script. Ojo: esto **sí cuesta** por uso, aparte de tu plan Pro.
7. **Publicar como app web** («Ejecutar como: yo», «Acceso: solo yo»).

## Riesgos y decisiones que son tuyas
- **Costo de Claude.** En claude.ai está incluido en tu plan; en Apps Script se paga por uso con una llave de la API.
- **Dónde viven los datos.** La Sheet es simple y la ves; Firestore aguanta más volumen. Para tu tamaño, la Sheet alcanza.
- **Límites de Apps Script.** Unos 6 minutos por ejecución y cuotas diarias de `UrlFetchApp`. Leer todas las cotizaciones de Zoho hay que hacerlo por partes (ya se lee solo lo que cambió).
- **Seguridad.** Nunca poner llaves ni tokens dentro de `curtis.html`.
