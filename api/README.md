# API Documentation for EKG Multi‑Agent Backend

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server locally
uvicorn api.analyze:app --reload
```

The server exposes a single endpoint:
- **POST `/analyze`** – accepts a multipart image (`.jpg`/`.png`).
  - Validates file type and size (max 10 MB).
  - Stores the file temporarily and forwards the path to the orchestrator service.
  - Returns a JSON payload with the agent outputs (or an error).

## Configuration
- `ORCHESTRATOR_URL` – environment variable pointing to the Claude Code orchestrator (default: `http://localhost:8001/execute`).

## Testing
Run the test suite:
```bash
pytest
```

## Deployment
For Vercel, add a `vercel.json` at the repo root defining the Python serverless function.
