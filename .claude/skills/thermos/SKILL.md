---
name: thermos
description: "Lanza en paralelo las dos revisiones termonucleares (fallas y seguridad; calidad del código) y junta lo que encuentran. Para «thermos», revisión doble o auditoría de una rama."
disable-model-invocation: true
---

# Thermos

Dos revisiones en paralelo, en segundo plano, y una síntesis al final.

## Pasos

1. **Alcance.** Lo que pidió Diego; si no dijo, la rama actual o los archivos que cambiaron desde la última revisión.
2. **Contexto.** Juntá el diff y los pedazos de archivo que los revisores necesitan para no adivinar.
3. **Lanzamiento.** Los dos subagentes en el mismo mensaje, con `run_in_background: true`:
   - `thermo-nuclear-review-subagent`: fallas, cosas que se rompen, seguridad, privacidad, funciones a medio terminar que se cuelan y lo que le complica el trabajo a quien sigue.
   - `thermo-nuclear-code-quality-review-subagent`: mantenimiento, estructura, archivos que crecen sin control, código enredado y abstracciones de más o de menos.
   Si esos tipos no están cargados en la sesión, usá `general-purpose` con el texto de `.claude/agents/<nombre>.md` como instrucciones.
4. **Mismo encargo a los dos.** El mismo alcance y contexto; que devuelvan hallazgos ordenados por gravedad, con archivo, línea y evidencia.
5. **Síntesis.** Cuando terminen los dos:
   - Primero los hallazgos, sin repetidos.
   - Lo que encontraron los dos pesa más.
   - Si no coinciden, decidí vos y decí por qué.
   - Resúmenes cortos.

Si Diego ya vio el resumen de cada revisor, no lo repitás: dale el veredicto, lo más importante y lo que queda en duda.

## En nAIhual

- A Diego se le habla en español de Guatemala, corto y sin palabras técnicas (`CLAUDE.md`). Reportá con ✅ verificado · 🟡 sin probar · ❓ supongo.
- Revisar no es arreglar: nada se cambia sin CONSTRUYE.
- Los hallazgos que importan van a la Parte 2 (Abierto) de `docs/nAIhual.md`.
