from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import base64
import json
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# ── Configuración: leer env vars ANTES de crear la app ──────────────────────
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "sk-or-dummy")
MODEL_NAME      = os.getenv("MODEL_NAME", "google/gemini-2.5-flash")
if MODEL_NAME == "google/gemini-2.5-flash-preview":
    MODEL_NAME = "google/gemini-2.5-flash"
# CORS: acepta todos los orígenes por defecto (configurable via ALLOWED_ORIGINS)
_raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()] or ["*"]

client = AsyncOpenAI(
    base_url=OPENAI_API_BASE,
    api_key=OPENAI_API_KEY
)

app = FastAPI(title="EKG Multi-Agente API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,   # False es compatible con wildcard y orígenes específicos
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "service": "EKG Multi-Agente API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "model": MODEL_NAME, "base_url": OPENAI_API_BASE}


def encode_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def read_skill_prompt(skill_name):
    path = os.path.join(os.path.dirname(__file__), f"../ekg/agents/{skill_name}.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

async def call_agent(skill_name: str, base64_image: str):
    prompt = read_skill_prompt(skill_name)
    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt + "\n\nResponde SOLO en formato JSON válido, sin usar markdown, codeblocks ni ningún otro texto adicional. Solo las llaves y el contenido JSON."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=600,
            temperature=0.2
        )
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"):
            content = content.replace("```json\n", "", 1).replace("```", "")
        elif content.startswith("```"):
            content = content.replace("```\n", "", 1).replace("```", "")
            
        return json.loads(content)
    except Exception as e:
        print(f"Error in agent {skill_name}: {e}")
        return {
            "hallazgos": [f"Error al analizar: {e}"],
            "urgencia": "Atención",
            "comentario": "El agente falló al procesar la imagen."
        }

@app.post("/analyze")
async def analyze_ekg(file: UploadFile = File(...)):
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Tipo de archivo no soportado. Usa JPG o PNG.")
    
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="El archivo excede el límite de 10 MB.")
    
    # Manejo de paths para Windows y Linux
    tmp_dir = "/tmp" if os.name != 'nt' else os.environ.get("TEMP", ".")
    temp_filename = os.path.join(tmp_dir, f"{uuid.uuid4().hex}_{file.filename}")
        
    with open(temp_filename, "wb") as f:
        f.write(contents)
        
    try:
        base64_image = encode_image(temp_filename)
        
        # 1. Ejecutar los 4 agentes básicos en paralelo
        agents = ["ekg-ritmo", "ekg-morfologia", "ekg-isquemia", "ekg-intervalos"]
        tasks = [call_agent(agent, base64_image) for agent in agents]
        results = await asyncio.gather(*tasks)
        
        combined_findings = {
            "ritmo": results[0],
            "morfologia": results[1],
            "isquemia": results[2],
            "intervalos": results[3]
        }
        
        # 2. Ejecutar el Agente de Síntesis (solo texto, no necesita la imagen)
        synthesis_prompt = read_skill_prompt("ekg-sintesis")
        synthesis_content = (
            f"{synthesis_prompt}\n\n"
            f"HALLAZGOS DE LOS AGENTES ESPECIALIZADOS:\n{json.dumps(combined_findings, indent=2, ensure_ascii=False)}\n\n"
            "Genera el reporte final en JSON válido estricto. Sin bloques de código, sin texto adicional."
        )
        
        try:
            synth_response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": synthesis_content   # solo texto, sin imagen
                    }
                ],
                max_tokens=800,
                temperature=0.2
            )
            synth_content = synth_response.choices[0].message.content.strip()
            # Limpiar cualquier wrapper markdown que el modelo pueda agregar
            if "```json" in synth_content:
                synth_content = synth_content.split("```json")[1].split("```")[0].strip()
            elif "```" in synth_content:
                synth_content = synth_content.split("```")[1].split("```")[0].strip()
                
            try:
                final_report = json.loads(synth_content)
            except json.JSONDecodeError as je:
                print(f"JSONDecodeError en síntesis: {je} | Contenido: {synth_content[:200]}")
                final_report = {
                     "diagnostico_principal": "Revisión manual requerida",
                     "urgencia": "Atención",
                     "recomendacion": "El modelo no devolvió un JSON válido. Revisa los hallazgos individuales.",
                     "aviso": "Este informe es una ayuda clínica y no reemplaza la valoración médica."
                }
        except Exception as synth_error:
            print(f"Error in synthesis agent: {synth_error}")
            final_report = {
                 "diagnostico_principal": "Error en el Agente de Síntesis",
                 "urgencia": "Atención",
                 "recomendacion": f"El agente de síntesis falló al procesar los hallazgos: {synth_error}",
                 "aviso": "Este informe es una ayuda clínica y no reemplaza la valoración médica."
            }
        
        # Asegurar que los hallazgos individuales estén presentes
        final_report["hallazgos"] = combined_findings
            
        return JSONResponse(content=final_report)
        
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error en la orquestación: {e}")
    finally:
        try:
            os.remove(temp_filename)
        except OSError:
            pass
