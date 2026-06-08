from typing import List

from src.models.schemas import BehavioralEvidence, SelfTalkStatement, SufficiencyResult, SufficiencyReason
from src.utils.config import (
    MIN_BEHAVIOR_EVENTS,
    MIN_SELF_TALK_EVENTS,
    MIN_TEMPORAL_DAYS,
    MIN_CONFIDENCE
)


def _check_behavior_count(behaviors: List[BehavioralEvidence]) -> bool:
    """Check if the minimum behavioral events requirement is met."""
    return len(behaviors) >= MIN_BEHAVIOR_EVENTS


def _check_self_talk_count(statements: List[SelfTalkStatement]) -> bool:
    """Check if the minimum self-talk statements requirement is met."""
    return len(statements) >= MIN_SELF_TALK_EVENTS


def _check_temporal_coverage(
    behaviors: List[BehavioralEvidence],
    statements: List[SelfTalkStatement]
) -> bool:
    """
    Check if the temporal coverage of all evidence spans the required minimum days.
    """
    all_timestamps = [b.timestamp for b in behaviors] + [s.timestamp for s in statements]
    
    if not all_timestamps:
        return False
        
    earliest_timestamp = min(all_timestamps)
    latest_timestamp = max(all_timestamps)
    coverage_days = (latest_timestamp - earliest_timestamp).days
    
    return coverage_days >= MIN_TEMPORAL_DAYS


def _check_confidence(behaviors: List[BehavioralEvidence]) -> bool:
    """Check if the average behavioral confidence meets the minimum threshold."""
    if not behaviors:
        return False
    avg_confidence = sum(b.confidence for b in behaviors) / len(behaviors)
    return avg_confidence >= MIN_CONFIDENCE


def evaluate_sufficiency(
    behaviors: List[BehavioralEvidence],
    statements: List[SelfTalkStatement],
    allow_blind_spot: bool = False
) -> SufficiencyResult:
    """
    Evaluates whether there is enough evidence to be analyzed.
    Executes deterministic checks against globally configured minimums.
    
    Args:
        behaviors: List of observed behavioral evidence.
        statements: List of self-talk statements.
        allow_blind_spot: If True, bypasses the minimum self-talk requirement.
        
    Returns:
        SufficiencyResult indicating pass/fail and the specific reason.
    """
    if not _check_behavior_count(behaviors):
        return SufficiencyResult(
            sufficient=False,
            reason=SufficiencyReason.INSUFFICIENT_BEHAVIOR_EVENTS
        )
        
    if not allow_blind_spot and not _check_self_talk_count(statements):
        return SufficiencyResult(
            sufficient=False,
            reason=SufficiencyReason.INSUFFICIENT_SELF_TALK
        )
            
    if not _check_temporal_coverage(behaviors, statements):
        return SufficiencyResult(
            sufficient=False,
            reason=SufficiencyReason.INSUFFICIENT_TEMPORAL_COVERAGE
        )
            
    if not _check_confidence(behaviors):
        return SufficiencyResult(
            sufficient=False,
            reason=SufficiencyReason.INSUFFICIENT_CONFIDENCE
        )
            
    return SufficiencyResult(
        sufficient=True,
        reason=SufficiencyReason.PASSED
    )
