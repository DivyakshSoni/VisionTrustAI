from backend.core.schemas.schemas import InferenceRecordSchema
from typing import Dict, Any

def tamper_record_field(record: InferenceRecordSchema, field: str, new_value: Any) -> InferenceRecordSchema:
    """
    Programmatically alters a field in an InferenceRecord without updating the signature or hashes.
    Simulates database-level tampering.
    """
    record_dict = record.model_dump()
    if field in record_dict:
        record_dict[field] = new_value
        
    # Rebuild the record from the dict (keeping the old hashes and signatures intact)
    return InferenceRecordSchema(**record_dict)

def tamper_record_output_label(record: InferenceRecordSchema, new_label: str) -> InferenceRecordSchema:
    """
    Specific tamper function to alter the output label of a record.
    """
    record_dict = record.model_dump()
    if "output" in record_dict and isinstance(record_dict["output"], dict):
        record_dict["output"]["label"] = new_label
        
    return InferenceRecordSchema(**record_dict)
