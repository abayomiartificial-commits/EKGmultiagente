# PRD — Sistema Multiagente de Análisis de EKG de 12 Derivaciones
**Documento:** Product Requirements Document  
**Versión:** 1.0  
**Fecha:** Abril 2025  
**Estado:** Borrador para desarrollo  
**Plataforma objetivo:** Claude Code  
**Despliegue:** Vercel  
**Idioma del sistema:** Español  

---

## 1. Visión General

### 1.1 Propósito

Construir un sistema de inteligencia artificial multiagente que analice imágenes de electrocardiogramas (EKG) de 12 derivaciones y genere un concepto clínico estructurado como **marco de referencia y segunda opinión** para el médico tratante. El diagnóstico final siempre es responsabilidad exclusiva del médico.

### 1.2 Problema que resuelve

La lectura de un EKG de 12 derivaciones requiere analizar simultáneamente múltiples dimensiones clínicas: ritmo, morfología, intervalos, hallazgos isquémicos y síntesis integradora. Un médico puede omitir hallazgos sutiles bajo presión de tiempo o en condiciones de alta carga asistencial. El sistema actúa como un asistente de revisión sistemática, no como reemplazante del juicio clínico.

### 1.3 Posicionamiento

- **No es** un dispositivo médico certificado ni un sistema de diagnóstico autónomo.
- **Es** una herramienta de apoyo clínico que sistematiza el análisis y reduce el riesgo de pasar por alto hallazgos relevantes.
- **No es** una aplicación comercializable en esta etapa.
- **Es** un MVP de uso interno/académico para validación del concepto.

---

## 2. Usuarios y Contexto de Uso

### 2.1 Usuario primario

Médico general o especialista que dispone de la imagen digital del EKG de un paciente y desea una revisión sistematizada antes de emitir su concepto final.

### 2.2 Flujo de uso esperado

1. El médico accede a la interfaz web del sistema.
2. Sube la imagen del EKG (una sola imagen por sesión de análisis).
3. El sistema valida que la imagen sea un EKG legible.
4. Se lanzan 5 agentes en paralelo, cada uno analiza una dimensión clínica.
5. Los resultados se integran en un concepto clínico estructurado.
6. El médico lee el reporte, emite su diagnóstico final y puede agregar una valoración del análisis del sistema (fase futura).

### 2.3 Lo que el médico NO hace

- No interactúa con los agentes individualmente.
- No configura parámetros técnicos.
- No necesita conocimiento de IA o programación.

---

## 3. Arquitectura del Sistema

### 3.1 Patrón general

El sistema replica el patrón **orquestador + subagentes paralelos** del repositorio `ai-marketing-claude`, adaptado al dominio clínico. La estructura de archivos sigue la misma convención de skills y agentes de Claude Code.

```
ekg-analysis/
├── ekg/SKILL.md                     # Orquestador principal — recibe imagen, coordina agentes
│
├── agents/                          # 5 subagentes paralelos
│   ├── ekg-ritmo.md                 # Agente 1: Ritmo cardíaco y frecuencia
│   ├── ekg-morfologia.md            # Agente 2: Morfología y eje eléctrico
│   ├── ekg-isquemia.md              # Agente 3: Isquemia, lesión y necrosis
│   ├── ekg-intervalos.md            # Agente 4: Intervalos y duración
│   └── ekg-sintesis.md              # Agente 5: Síntesis clínica integradora
│
├── skills/                          # Sub-skills de soporte
│   ├── ekg-validacion/SKILL.md      # Validación de calidad de imagen
│   └── ekg-reporte/SKILL.md         # Generación del reporte en Markdown
│
├── scripts/
│   └── generate_pdf_report.py       # Generador PDF con reportlab (fase post-MVP)
│
├── templates/
│   └── reporte-clinico.md           # Template del concepto clínico estructurado
│
├── api/
│   └── analyze.py                   # Endpoint backend para Vercel
│
├── frontend/
│   ├── index.html                   # Interfaz de carga de imagen
│   └── result.html                  # Vista del reporte generado
│
├── install.sh
└── requirements.txt
```

### 3.2 Los 5 agentes y su responsabilidad clínica

| Agente | Archivo | Dimensión clínica | Analogía en repo marketing |
|---|---|---|---|
| Agente Ritmo | `ekg-ritmo.md` | Frecuencia cardíaca, regularidad, ritmo sinusal vs arritmias, origen del ritmo | `market-content` |
| Agente Morfología | `ekg-morfologia.md` | Eje eléctrico, morfología QRS, ondas P y T, voltajes | `market-conversion` |
| Agente Isquemia | `ekg-isquemia.md` | Segmento ST, cambios isquémicos, patrones de lesión/necrosis, bloqueos de rama | `market-competitive` |
| Agente Intervalos | `ekg-intervalos.md` | Intervalo PR, QT/QTc, duración QRS, síndromes de pre-excitación | `market-technical` |
| Agente Síntesis | `ekg-sintesis.md` | Integra hallazgos de los 4 agentes anteriores, genera concepto clínico estructurado con nivel de urgencia | `market-strategy` |

### 3.3 Flujo de orquestación

```
[Médico sube imagen]
        ↓
[Validación de imagen — ekg-validacion/SKILL.md]
        ↓ (imagen válida)
[Orquestador — ekg/SKILL.md]
        ↓
[Lanzamiento paralelo de 4 agentes]
    ├── Agente Ritmo
    ├── Agente Morfología  
    ├── Agente Isquemia
    └── Agente Intervalos
        ↓ (todos completan)
[Agente Síntesis — recibe outputs de los 4 anteriores]
        ↓
[Reporte Markdown estructurado]
        ↓
[Interfaz web — resultado visible para el médico]
```

---

## 4. Stack Tecnológico

### 4.1 Modelos de lenguaje

| Etapa | Modelo | Proveedor | Justificación |
|---|---|---|---|
| MVP / Pruebas | **GPT-4.1** | OpenAI API | Mejor balance precisión/especificidad en benchmarks de EKG 2025; few-shot learning efectivo en imágenes médicas |
| Producción (cerebro firme) | **Claude Sonnet 4.5** | Anthropic API | Razonamiento estructurado superior para síntesis multiagente; nativo en Claude Code |
| Texto sin imagen (auxiliar) | Configurable | Anthropic / OpenAI | Para subtareas que no requieran visión |

> **Nota sobre Ollama:** Descartado para componentes de visión. Los modelos locales con capacidad multimodal alcanzan hasta 40% de precisión en imágenes médicas según benchmarks recientes (npj Digital Medicine, 2025), lo que contaminaría la validación de la arquitectura. Puede usarse para subtareas de texto puro si se requiere en el futuro.

> **Principio de diseño:** El modelo se pasa como parámetro de configuración en todos los agentes. Esto permite cambiar el cerebro sin reescribir la lógica del sistema.

### 4.2 Infraestructura

| Componente | Tecnología |
|---|---|
| Orquestación de agentes | Claude Code (CLI) |
| Backend API | Python (FastAPI o Flask) |
| Despliegue | Vercel (Serverless Functions) |
| Frontend | HTML/CSS/JS simple — sin frameworks pesados en MVP |
| Generación PDF | reportlab (Python) — fase post-MVP |
| Control de versiones | GitHub |

### 4.3 Entrada de datos

- **Formato aceptado:** Imagen JPG o PNG del trazado EKG impreso o digital (similar al formato de casos clínicos en portales como campuscardio.com)
- **Una imagen por sesión** — si la imagen es rechazada por baja calidad, el médico la reemplaza
- **Tamaño máximo recomendado:** 10 MB
- **Resolución mínima recomendada:** 300 DPI o equivalente legible

---

## 5. Definición de los Agentes

### 5.1 Agente Ritmo (`ekg-ritmo.md`)

**Input:** Imagen EKG completa  
**Responsabilidad:**
- Calcular frecuencia cardíaca (estimación visual por método de los cuadros grandes)
- Determinar regularidad del ritmo (regular, irregular, irregularmente irregular)
- Identificar origen del ritmo: sinusal, auricular, nodal, ventricular
- Detectar arritmias: fibrilación auricular, flutter auricular, taquicardia supraventricular, bloqueos sinoauriculares
- Identificar pausas, escape o ritmos de reemplazo

**Output esperado:** Sección estructurada con hallazgos y nivel de urgencia asociado (Normal / Atención / Urgente)

### 5.2 Agente Morfología (`ekg-morfologia.md`)

**Input:** Imagen EKG completa  
**Responsabilidad:**
- Determinar eje eléctrico (normal, desviación izquierda, desviación derecha, eje indeterminado)
- Describir morfología de onda P (presencia, polaridad, duración)
- Analizar morfología del complejo QRS (ondas Q patológicas, R, S)
- Describir onda T (inversión, aplanamiento, hiperaguda)
- Evaluar voltajes (criterios de hipertrofia ventricular izquierda o derecha)
- Detectar ondas delta (preexcitación)

**Output esperado:** Sección estructurada con hallazgos morfológicos derivación por derivación agrupados por territorio

### 5.3 Agente Isquemia (`ekg-isquemia.md`)

**Input:** Imagen EKG completa  
**Responsabilidad:**
- Evaluar segmento ST en todas las derivaciones: elevación, descenso, morfología (cóncavo, convexo, rectificado)
- Identificar patrones de STEMI (elevación ST con criterios de territorio vascular)
- Detectar isquemia subendocárdica (descenso ST difuso, cambios en aVR)
- Evaluar patrón de Wellens o De Winter (equivalentes isquémicos de alto riesgo)
- Identificar bloqueos de rama izquierda o derecha nuevos o de probable nueva aparición
- Detectar patrones de necrosis establecida (ondas Q patológicas en territorio)

**Output esperado:** Sección con hallazgos isquémicos, territorio probable comprometido y nivel de urgencia (este agente tiene el mayor peso en urgencia)

### 5.4 Agente Intervalos (`ekg-intervalos.md`)

**Input:** Imagen EKG completa  
**Responsabilidad:**
- Medir intervalo PR (normal, corto — preexcitación, prolongado — bloqueo AV de 1°, 2° o 3°)
- Medir duración del QRS (estrecho < 120 ms, ensanchado ≥ 120 ms)
- Medir intervalo QT y calcular QTc (fórmula de Bazett): evaluar prolongación o acortamiento
- Identificar síndrome de Brugada (patrón en V1-V2)
- Detectar síndrome de QT largo o corto congénito vs adquirido

**Output esperado:** Sección con mediciones estimadas de intervalos y su interpretación clínica

### 5.5 Agente Síntesis (`ekg-sintesis.md`)

**Input:** Outputs estructurados de los 4 agentes anteriores  
**Responsabilidad:**
- Integrar todos los hallazgos en un concepto clínico coherente
- Asignar nivel de urgencia global: `NORMAL` / `HALLAZGOS INESPECÍFICOS` / `ATENCIÓN REQUERIDA` / `URGENTE`
- Generar lista de diagnósticos diferenciales ordenados por probabilidad
- Redactar el "Concepto EKG" como texto clínico estructurado en español
- Incluir advertencia explícita de que el concepto es una guía de segunda opinión y no reemplaza el diagnóstico médico
- Señalar limitaciones del análisis cuando aplique (imagen de baja resolución, derivaciones poco visibles, etc.)

**Output esperado:** Reporte clínico completo listo para presentar al médico

---

## 6. Formato del Reporte Clínico

El reporte generado por el Agente Síntesis seguirá esta estructura:

```markdown
# Análisis EKG — Concepto de Segunda Opinión

**Fecha de análisis:** [timestamp]  
**Modelo utilizado:** [nombre del modelo]  
**⚠️ AVISO:** Este reporte es una guía de apoyo clínico generada por IA. 
El diagnóstico final es responsabilidad exclusiva del médico tratante.

---

## Nivel de Urgencia Global
🟢 NORMAL | 🟡 HALLAZGOS INESPECÍFICOS | 🟠 ATENCIÓN REQUERIDA | 🔴 URGENTE

---

## 1. Ritmo
- Frecuencia cardíaca estimada: X lpm
- Regularidad: [regular / irregular]
- Origen: [sinusal / auricular / otro]
- Hallazgos: [descripción]
- Urgencia: [Normal / Atención / Urgente]

## 2. Morfología y Eje
- Eje eléctrico: [X grados — Normal / Desviación I / Desviación D]
- Onda P: [descripción]
- Complejo QRS: [descripción]
- Onda T: [descripción]
- Voltajes: [descripción]

## 3. Hallazgos Isquémicos
- Segmento ST: [descripción por derivación]
- Patrón identificado: [STEMI / isquemia subendocárdica / sin cambios / otro]
- Territorio probable: [anterior / inferior / lateral / posterior / ninguno]
- Urgencia: [Normal / Atención / Urgente]

## 4. Intervalos
- PR: X ms — [Normal / Corto / Prolongado]
- QRS: X ms — [Estrecho / Ensanchado]
- QTc: X ms — [Normal / Prolongado / Corto]
- Hallazgos adicionales: [descripción]

## 5. Concepto Clínico Integrado
[Párrafo narrativo en lenguaje clínico estructurado integrando todos los hallazgos, 
con diagnósticos diferenciales ordenados por probabilidad]

## 6. Limitaciones del Análisis
[Señalar si alguna derivación era ilegible, si la imagen tenía baja resolución, 
o si algún hallazgo requiere correlación clínica adicional]
```

---

## 7. Interfaz de Usuario (MVP)

### 7.1 Pantalla de carga

- Campo de carga de imagen (drag & drop o botón de selección)
- Indicación clara del formato aceptado (JPG, PNG)
- Botón "Analizar EKG"
- Indicador de progreso durante el análisis
- Mensaje de estado por agente (opcional en MVP, recomendado para transparencia)

### 7.2 Pantalla de resultado

- Nivel de urgencia destacado visualmente (color semáforo)
- Reporte clínico estructurado en secciones colapsables
- Imagen del EKG analizado visible junto al reporte
- Botón "Nuevo análisis"
- Espacio reservado para "Valoración del médico" (campo desactivado en MVP, activo en v2)

### 7.3 Principios de diseño de la interfaz

- Interfaz limpia, sin distracciones
- Tipografía legible (mínimo 16px para texto clínico)
- Sin publicidad ni elementos comerciales
- Responsive para tablets (médicos frecuentemente usan tablets en consulta)
- Sin necesidad de registro o autenticación en MVP

---

## 8. Prompts Clínicos — Estrategia de Diseño

### 8.1 Por qué los prompts son el componente más crítico

La precisión del sistema depende directamente de cuán bien estén redactados los prompts de cada agente. Un prompt clínico mal estructurado generará hallazgos vagos o incorrectos independientemente del modelo usado.

### 8.2 Estrategia de construcción de prompts

Cada agente usará la estrategia **few-shot learning**: incluir en el prompt ejemplos reales de análisis correctos por dimensión. Esto mejora significativamente el rendimiento sobre el enfoque zero-shot, según benchmarks de EKG publicados en 2025.

**Fuentes para construir los prompts clínicos (investigación requerida):**

- Manual de electrocardiografía de Dubin (interpretación sistematizada)
- Criterios de Sokolow-Lyon y Cornell (hipertrofia ventricular)
- Criterios de Sgarbossa (STEMI en bloqueo de rama izquierda)
- Guías ESC/AHA de síndrome coronario agudo vigentes
- Casos clínicos de portales como CampusCardio, ECGpedia, Life in the Fast Lane (ECG Library)
- Criterios de medición de intervalos según estándares internacionales (intervalo QTc por Bazett)

### 8.3 Estructura base de cada prompt de agente

```
ROL: Eres un especialista en [dimensión específica] de electrocardiografía...

CONTEXTO: Estás analizando la dimensión de [X] de un EKG de 12 derivaciones 
como parte de un sistema de segunda opinión para un médico...

INSTRUCCIONES DE ANÁLISIS:
1. [Paso clínico específico]
2. [Paso clínico específico]
...

EJEMPLOS DE REFERENCIA (few-shot):
Ejemplo 1: [imagen de referencia + análisis correcto]
Ejemplo 2: [imagen de referencia + análisis correcto]

FORMATO DE SALIDA REQUERIDO:
[estructura exacta del output esperado]

LIMITACIONES A REPORTAR:
- Si [condición], indica explícitamente que [limitación]
...

ADVERTENCIA PERMANENTE:
Siempre concluir con: "Este análisis es una guía de apoyo. El diagnóstico 
clínico es responsabilidad del médico tratante."
```

---

## 9. Fases de Desarrollo

### Fase 1 — Estructura base y orquestador (MVP mínimo viable)

**Objetivo:** Sistema funcional que reciba una imagen y genere un reporte en texto

- [ ] Crear estructura de carpetas del proyecto en Claude Code
- [ ] Desarrollar `ekg/SKILL.md` (orquestador)
- [ ] Desarrollar `ekg-validacion/SKILL.md` (validador de imagen)
- [ ] Configurar acceso a API de OpenAI (GPT-4.1) para pruebas
- [ ] Desarrollar los 5 archivos de agentes con prompts iniciales
- [ ] Probar con 5-10 imágenes de EKG de casos públicos (CampusCardio, PhysioNet)
- [ ] Generar reporte en Markdown en terminal

**Criterio de éxito:** El sistema produce un reporte estructurado coherente para un EKG normal y uno con hallazgos evidentes (ej. STEMI o fibrilación auricular)

### Fase 2 — Interfaz web y despliegue en Vercel

**Objetivo:** El médico puede usar el sistema desde el navegador

- [ ] Desarrollar endpoint API en Python (FastAPI)
- [ ] Desarrollar frontend HTML/CSS/JS de carga de imagen
- [ ] Desarrollar vista de resultado con reporte estructurado
- [ ] Configurar proyecto en Vercel
- [ ] Desplegar y probar en URL pública
- [ ] Ajustar prompts basándose en resultados reales

**Criterio de éxito:** Un médico puede subir una imagen desde el navegador y obtener un reporte en menos de 60 segundos

### Fase 3 — Refinamiento clínico y calibración de modelos

**Objetivo:** Mejorar calidad clínica del reporte y validar modelo definitivo

- [ ] Comparar outputs de GPT-4.1 vs Claude Sonnet 4.5 con el mismo set de EKGs
- [ ] Refinar prompts con estrategia few-shot (agregar ejemplos clínicos)
- [ ] Definir modelo de producción basándose en resultados propios
- [ ] Agregar manejo de errores robusto (imagen ilegible, timeout de API, etc.)
- [ ] Revisar reporte con un médico para validar utilidad clínica del concepto

**Criterio de éxito:** Un médico considera el reporte útil como marco de referencia en al menos 7 de 10 EKGs de prueba

### Fase 4 — Generación PDF y retroalimentación del médico (post-MVP)

**Objetivo:** Agregar funcionalidades de valor adicional

- [ ] Implementar generación de PDF con reportlab
- [ ] Agregar campo de "Valoración del médico" en la interfaz
- [ ] Diseñar estructura de almacenamiento de valoraciones para retroalimentación futura del modelo
- [ ] Evaluar posibilidad de fine-tuning con valoraciones acumuladas

---

## 10. Restricciones y Consideraciones

### 10.1 Éticas y legales

- El sistema debe incluir en todo reporte una advertencia clara de que **no es un dispositivo médico** y que el diagnóstico es responsabilidad del médico.
- No almacenar imágenes de pacientes sin consentimiento explícito (en MVP, no hay almacenamiento persistente).
- El sistema no debe emitir nunca un diagnóstico categórico sin calificación de incertidumbre.

### 10.2 Técnicas

- Los LLMs generales tienen limitaciones documentadas en interpretación de EKG (precisión ~65% en estudios de 2025). El sistema está diseñado para operar dentro de esas limitaciones siendo un **asistente**, no un árbitro.
- La calidad del análisis depende directamente de la calidad de la imagen subida. Imágenes de baja resolución, con artefactos o mal encuadradas producirán análisis de menor calidad.
- El sistema no tiene acceso a historia clínica, medicamentos ni contexto del paciente — trabaja exclusivamente con la imagen.

### 10.3 De alcance (fuera del MVP)

- Análisis de EKG en serie (comparación evolutiva)
- Integración con sistemas de historia clínica electrónica
- Certificación como dispositivo médico
- Análisis de señal digital (solo imagen en esta versión)
- Soporte multiidioma

---

## 11. Métricas de Validación del MVP

| Métrica | Definición | Meta MVP |
|---|---|---|
| Tasa de rechazo correcto | % de imágenes no-EKG o ilegibles correctamente rechazadas | ≥ 90% |
| Tiempo de análisis | Tiempo desde carga hasta reporte disponible | ≤ 60 segundos |
| Coherencia del reporte | Reporte sin contradicciones internas entre agentes | ≥ 80% de casos |
| Utilidad clínica percibida | Valoración del médico revisor (escala 1-5) | ≥ 3.5/5 |
| Detección de hallazgos críticos | % de casos con STEMI o arritmia grave identificados como "Urgente" | ≥ 85% |

---

## 12. Referencias Técnicas y Clínicas

### Repositorio base
- `ai-marketing-claude` — https://github.com/zubair-trabzada/ai-marketing-claude (patrón arquitectónico)

### Benchmarks de modelos en EKG
- JMIR AI (2025): *Effectiveness of the GPT-4o Model in Interpreting ECG Images for Cardiac Diagnostics*
- npj Digital Medicine (2025): *Benchmarking vision-language models for diagnostics in emergency and critical care settings*
- PMC (2025): *Comparative Diagnostic Performance of a Multimodal LLM Versus a Dedicated ECG AI in Detecting Myocardial Infarction*

### Recursos clínicos para construcción de prompts
- ECGpedia — https://en.ecgpedia.org
- Life in the Fast Lane ECG Library — https://litfl.com/ecg-library/
- CampusCardio — https://campuscardio.com/casos-clinicos-electrocardiogramas/
- PhysioNet ECG datasets — https://physionet.org (EKGs de acceso público para pruebas)

---

*Documento generado como guía de desarrollo. Sujeto a revisión y actualización conforme avance el proyecto.*
