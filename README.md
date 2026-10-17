# nAIhual — base de mapa y conversación

Sitio móvil con mapa integrado Leaflet/OpenStreetMap, selección de destino, seguimiento GPS en primer plano y rutas peatonales experimentales. C0 original conservada en `c0/`.

## Descargar para Netlify

El archivo `entregas/naihual-para-netlify.zip` contiene los archivos públicos preparados. Descomprimir y subir la carpeta resultante con el mismo método de Netlify Drop usado para C0. No subir toda esta rama: incluye código del servidor y fuentes de referencia.

## Estado comprobado

Nueve pruebas de Node y ocho escenarios de Chromium con GPS, teselas y rutas simulados. Pendientes: proveedores públicos de mapa y ruta, recorrido caminando en un teléfono y API real de IA. Catálogo inicialmente vacío; no hay lugares inventados. Esta rama no actualiza la web publicada.

## Desarrollo

Node >=22. Sin instalación de paquetes. `npm start` inicia el servidor de desarrollo; `npm test` ejecuta las pruebas y `npm run build` genera `dist/`. Leaflet 1.9.4 está incluido localmente con licencia y registro de integridad.

La conversación es guiada hasta configurar un backend seguro con `GEMINI_API_KEY` y `GEMINI_MODEL`, confirmar disponibilidad del modelo y presupuesto. Nunca agregar claves al frontend o Git. La IA solo interpreta intención e IDs del catálogo. Netlify Drop no ejecuta el servidor Node; la web estática usa reglas locales.

`data/places.json` es la fuente pública de puntos. Cada ficha requiere `id`, `name`, `category`, `city`, coordenadas numéricas `lat` y `lng`, `sourceUrl` HTTPS, `reviewedAt` AAAA-MM-DD y `status` verified. Verificar los datos antes de cargarlos; no publicar datos privados ni lugares sensibles.

La ubicación requiere permiso voluntario y HTTPS; el proveedor de rutas recibe origen y destino al calcular. La posición posterior se procesa localmente, sin guardar historial. La precisión baja pausa indicaciones y los desvíos requieren recálculo manual. No hay navegación con pantalla bloqueada, voz ni garantía de seguridad o accesibilidad.
