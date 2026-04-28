from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os
import uuid

app = FastAPI()

# Configuration – adjust the orchestrator command or service URL as needed
ORCHESTRATOR_URL = os.getenv("ORCHESTRATOR_URL", "http://localhost:8001/execute")

@app.post("/analyze")
async def analyze_ekg(file: UploadFile = File(...)):
    # Basic validation – ensure image type
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(status_code=400, detail="Unsupported file type. Use JPG or PNG.")
    # Read file content into memory (max 10 MB as per frontend)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 10 MB limit.")
    # Store temporarily to pass to orchestrator (could be a path or base64)
    temp_filename = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
    with open(temp_filename, "wb") as f:
        f.write(contents)
    # Call the orchestrator (Claude Code CLI) – placeholder using httpx
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                ORCHESTRATOR_URL,
                json={"image_path": temp_filename},
                timeout=60,
            )
        resp.raise_for_status()
        result = resp.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Orchestrator error: {e}")
    finally:
        # Clean up temporary file
        try:
            os.remove(temp_filename)
        except OSError:
            pass
    return JSONResponse(content=result)
