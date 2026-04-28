# SKILL: Validación del EKG

**ROL**: Verifica que la imagen subida corresponde a un EKG de 12 derivaciones legible.

**INSTRUCCIONES**:
1. Detecta si la imagen está borrosa, sobreexpuesta o con artefactos que impidan el análisis.
2. Confirma la presencia de 12 trazas (derivaciones) y la escala típica.
3. En caso de error, devuelve un mensaje explicativo al usuario.

**OUTPUT FORMATO**:
```json
{
  "valido": true|false,
  "mensaje": "...",
  "detalles": "..."
}
```

**EJEMPLOS (few‑shot)**:
- Imagen clara → `{ "valido": true, "mensaje": "Imagen válida.", "detalles": "" }`
- Imagen borrosa → `{ "valido": false, "mensaje": "Imagen no legible.", "detalles": "Desenfoque significativo." }`

**AVISO**: La validación es una ayuda inicial; siempre se requiere revisión clínica.
