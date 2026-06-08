"""
Central configuration module for Veritas.
Contains thresholds and constants for the scoring and classification pipelines.
"""

# Evidence Sufficiency
MIN_BEHAVIOR_EVENTS: int = 3
MIN_SELF_TALK_EVENTS: int = 2
MIN_TEMPORAL_DAYS: int = 7
MIN_CONFIDENCE: float = 0.60

# Uncertainty
UNCERTAINTY_ABSTAIN_THRESHOLD: float = 0.75

# Classification
ALIGNED_THRESHOLD: float = 0.75
OVERSTATEMENT_THRESHOLD: float = 0.7
UNDERSTATEMENT_THRESHOLD: float = 0.4
ASPIRATION_THRESHOLD: float = 0.3
