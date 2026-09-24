from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Node(Base):
    __tablename__ = 'nodes'
    
    id = Column(String, primary_key=True, index=True)
    node_type = Column(String, index=True) # 'dataset_batch', 'model', 'inference', 'detector', 'contributor'
    trust_score = Column(Float, default=0.2)
    crypto_locked = Column(Boolean, default=False)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    
    contributing_evidence = Column(JSON, default=list)
    propagated_from = Column(JSON, default=list)
    propagated_to = Column(JSON, default=list)

class Finding(Base):
    __tablename__ = 'findings'
    
    id = Column(String, primary_key=True, index=True)
    module = Column(String)
    affected_asset_id = Column(String, ForeignKey('nodes.id'))
    reason = Column(String)
    evidence = Column(JSON)
    trust_score_before = Column(Float)
    trust_score_after = Column(Float)
    confidence = Column(Float)
    severity = Column(String)
    recommended_action = Column(String)
    limitations = Column(String)

class InferenceRecord(Base):
    __tablename__ = 'inference_records'
    
    id = Column(String, primary_key=True, index=True)
    input_hash = Column(String)
    model_digest = Column(String)
    preprocessing_config_hash = Column(String)
    inference_config_hash = Column(String)
    output = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    sequence_nonce = Column(String)
    record_hash = Column(String)
    signature = Column(String)
    crypto_verified = Column(Boolean)

class MerkleLog(Base):
    __tablename__ = 'merkle_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    record_hash = Column(String, index=True)
    parent_hash = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
