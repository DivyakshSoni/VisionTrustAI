from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import inference, findings, trust_graph
from backend.core.orchestrator import run_demo_pipeline

app = FastAPI(title="VisionTrust AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inference.router)
app.include_router(findings.router)
app.include_router(trust_graph.router)

@app.post("/demo/run")
def trigger_demo():
    return run_demo_pipeline()

@app.get("/")
def read_root():
    return {"message": "VisionTrust AI - Zero-Trust AI Assurance Framework (ZTAAF) is running."}
