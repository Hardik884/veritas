from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

class DivergenceCategory(str, Enum):
    """Enumeration of possible divergence categories."""
    ALIGNED = "aligned"
    OVERSTATEMENT = "overstatement"
    UNDERSTATEMENT = "understatement"
    BLIND_SPOT = "blind_spot"
    ASPIRATION_GAP = "aspiration_gap"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"

class BehavioralEvidence(BaseModel):
    """Objective description of an observed behavior."""
    id: str = Field(..., description="Unique identifier for the evidence.")
    description: str = Field(..., description="Objective description of the behavior.")
    timestamp: datetime = Field(..., description="When the behavior occurred.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the observation.")
    intensity_score: float = Field(..., ge=-1.0, le=1.0, description="Direction and magnitude of the behavior.")

class SelfTalkStatement(BaseModel):
    """A verbatim self-talk statement provided by the subject."""
    id: str = Field(..., description="Unique identifier for the statement.")
    text: str = Field(..., description="The verbatim self-talk statement.")
    timestamp: datetime = Field(..., description="When the statement was made.")
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="Expressed sentiment or magnitude.")

class DomainAnalysisResult(BaseModel):
    """The final analysis result for a specific canonical domain."""
    domain: str = Field(..., description="The canonical domain.")
    divergence_score: float = Field(..., ge=-1.0, le=1.0, description="The calculated alignment score.")
    category: DivergenceCategory = Field(..., description="The assigned divergence category.")
    uncertainty: float = Field(..., ge=0.0, le=1.0, description="The calculated uncertainty metric.")
    evidence_used: List[str] = Field(..., description="Strictly observed behaviors and statements used for scoring.")
    rationale: str = Field(..., description="Explanation tracing the classification to specific evidence.")

class SufficiencyReason(str, Enum):
    INSUFFICIENT_BEHAVIOR_EVENTS = "insufficient_behavior_events"
    INSUFFICIENT_SELF_TALK = "insufficient_self_talk"
    INSUFFICIENT_TEMPORAL_COVERAGE = "insufficient_temporal_coverage"
    INSUFFICIENT_CONFIDENCE = "insufficient_confidence"
    PASSED = "passed"

class SufficiencyResult(BaseModel):
    """Result of an evidence sufficiency gate evaluation."""
    sufficient: bool = Field(..., description="Whether the evidence passed the sufficiency gate.")
    reason: SufficiencyReason | None = Field(None, description="The reason for the evaluation outcome.")

