import json
from typing import Dict, Any

# In a real offline deployment, this would use a local model like llama.cpp or Ollama.
# For demo/placeholder purposes, we mock the local LLM response or define the prompt structure.

def generate_finding_summary(finding: Dict[str, Any]) -> str:
    """
    Takes a structured Finding object and uses a local LLM to generate a concise, human-readable
    summary for the analyst.
    
    CRITICAL: The LLM prompt strictly instructs the model NOT to choose or change the disposition.
    """
    
    prompt = f"""
    You are an AI assurance analyst assistant running in an offline air-gapped environment.
    Your task is to summarize the following structured security finding for a human reviewer.
    
    Rules:
    1. Explain what the finding means in plain English.
    2. Mention the affected asset, the reason, the evidence, and the severity.
    3. DO NOT change or recommend a different disposition (recommended_action). Only report the one provided.
    
    Finding Data:
    {json.dumps(finding, indent=2)}
    
    Summary:
    """
    
    # Placeholder for local LLM inference call (e.g., via llama-cpp-python)
    # return local_llm_pipeline(prompt)
    
    # Mock return for the current setup
    asset_id = finding.get("affected_asset", {}).get("id", "Unknown")
    reason = finding.get("reason", "")
    severity = finding.get("severity", "unknown").upper()
    disposition = finding.get("recommended_action", "unknown").upper()
    
    summary = f"[{severity}] A finding was generated for asset '{asset_id}'. The system detected that: {reason}. " \
              f"The current ZTAAF disposition is set to {disposition}. Please review the attached evidence."
              
    return summary
