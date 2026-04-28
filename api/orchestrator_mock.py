import json
from pathlib import Path

# Mock orchestrator: reads the SKILL files (which are just markdown prompts) and returns a dummy combined report.

def mock_orchestrate(image_path: str) -> dict:
    # In a real system, this would invoke Claude Code agents.
    # Here we return a static example payload.
    report = {
        "diagnostico_principal": "Hipertrofia ventricular izquierda",
        "urgencia": "Atención",
        "hallazgos": {
            "ritmo": {
                "frecuencia": "78 lpm",
                "regularidad": "regular",
                "origen": "sinusal",
                "arritmias": [],
                "urgencia": "Normal",
                "comentario": "Ritmo sinusal normal."
            },
            "morfologia": {
                "hallazgos": ["ondas Q patológicas en V1‑V3"],
                "diagnostico": "infarto anterior",
                "urgencia": "Urgente",
                "comentario": "Signos de infarto agudo."
            },
            "isquemia": {
                "hallazgos": ["depresión del ST 0.2 mV en V2‑V3"],
                "territorio": "antero‑septal",
                "tipo": "agudo",
                "urgencia": "Urgente",
                "comentario": "Isquemia aguda."
            },
            "intervalos": {
                "PR": "160 ms",
                "QRS": "90 ms",
                "QTc": "410 ms",
                "hallazgos": [],
                "urgencia": "Normal",
                "comentario": "Intervalos dentro de rangos normales."
            }
        },
        "recomendacion": "Monitorizar y valorar intervención cardiológica."
    }
    return report
