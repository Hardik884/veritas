# Veritas Technical Design

## Problem Statement
Traditional behavioral assessments rely heavily on subjective self-reporting, which is prone to bias, blind spots, and overstatement. Conversely, purely behavioral tracking lacks the context of an individual's intent, goals, or self-awareness. There is a need for a system that can objectively score the divergence between what an individual *does* (behavior) and what they *say* (self-talk) without making subjective psychological judgments.

## Goals
*   Quantify the alignment between observed behavior and self-reported narrative.
*   Categorize divergences into explicit, actionable categories (e.g., Overstatement, Blind Spot).
*   Provide deterministic, reproducible, and explainable scoring.
*   Enforce strict structural safety guarantees to prevent the generation of psychological diagnoses or character judgments.
*   Handle incomplete or noisy data gracefully through robust abstention logic (Insufficient Evidence).

## Non-Goals
*   Diagnosing clinical conditions or mental health issues.
*   Inferring deep personality traits (e.g., Big Five).
*   Judging an individual's moral character or truthfulness.
*   Operating as an open-ended chatbot or interactive conversational agent.

## System Architecture
The system operates as a data processing pipeline that ingests, canonicalizes, and scores evidence.

**Behavioral Evidence & Self-Talk** $\rightarrow$ **Domain Discovery** $\rightarrow$ **Canonicalization** $\rightarrow$ **Evidence Sufficiency Gate** $\rightarrow$ **Alignment Scoring** $\rightarrow$ **Divergence Classification** $\rightarrow$ **Safety Layer** $\rightarrow$ **Output Generation**

## Data Flow
1.  **Ingestion**: Raw behavioral logs and self-talk transcripts are loaded into memory and parsed into `BehavioralEvidence` and `SelfTalkStatement` models.
2.  **Domain Mapping**: Evidence is clustered into dynamic domains and mapped to canonical domains to ensure consistency.
3.  **Sufficiency Check**: For each domain, the system checks if enough high-confidence data exists to make a reliable assessment.
4.  **Embedding & Scoring**: Summaries of behaviors and self-talk are embedded and compared using cosine similarity to generate an alignment score.
5.  **Classification**: The alignment score, combined with aggregated behavioral intensity ($B$) and self-talk sentiment ($T$), determines the final `DivergenceCategory`.
6.  **Safety & Output**: Outputs are structurally validated against a safe schema before being finalized as `DomainAnalysisResult` payloads.

## Data Models
*   **BehavioralEvidence**: Represents an observed action. Fields: `id`, `description`, `timestamp`, `confidence`, `intensity_score`.
*   **SelfTalkStatement**: Represents a narrative claim. Fields: `id`, `text`, `timestamp`, `sentiment_score`.
*   **DomainAnalysisResult**: The final output per domain. Fields: `domain`, `divergence_score`, `category`, `uncertainty`, `evidence_used`, `rationale`.

## Domain Strategy
*   **Dynamic Discovery**: Uses embeddings and clustering (e.g., HDBSCAN) to group evidence based on actual content, preserving the user's specific activities.
*   **Canonicalization**: A mapping layer canonicalizes these dynamic clusters into stable, consistent domains (e.g., "gym", "running" $\rightarrow$ "fitness").
*   **Domain Consistency & Fragmentation Prevention**: This hybrid approach prevents the fragmentation of fully dynamic clustering while avoiding the information loss associated with rigid, fixed taxonomies.

## Evidence Sufficiency
*   **Minimum Behavior Observations**: At least 3 distinct events.
*   **Minimum Self-Talk Observations**: At least 2 relevant statements.
*   **Temporal Coverage**: Evidence must span a minimum of 7 days.
*   **Confidence Thresholds**: Average source confidence must be $\ge 0.6$.
*   **Uncertainty Override**: If calculated total uncertainty $> 0.75$, the system overrides classification to `INSUFFICIENT_EVIDENCE`.
*   **Blind Spot Exception**: A domain may be classified as `BLIND_SPOT` even if self-talk observations are zero, provided behavioral sufficiency is met.

## Alignment Method
*   **Summary Generation**: All behavioral evidence for a domain is summarized factually, as is all self-talk.
*   **Embeddings**: Summaries are converted into dense vectors using an embedding model.
*   **Cosine Similarity & Deterministic Scoring**: Alignment score is calculated as the mathematical cosine similarity between the two vectors, ensuring reproducibility and testability.

## Divergence Classification
*   **ALIGNED**: Self-talk accurately reflects behavioral reality (`abs(T - B) <= 0.20`, score $\ge 0.75$). *Example: "I exercise regularly" and workouts are consistently logged.*
*   **OVERSTATEMENT**: Claim exceeds observed behavior ($T > 0.7$, $B < 0.4$). *Example: "I am highly productive" but task completion is low.*
*   **UNDERSTATEMENT**: Behavior exceeds self-description ($T < 0.4$, $B > 0.7$). *Example: "I haven't done much" but output is consistently high.*
*   **BLIND_SPOT**: Prominent behavior, zero or near-zero self-talk. *Example: User constantly interrupts (high B) but never mentions communication skills.*
*   **ASPIRATION_GAP**: Future-oriented goals stated, behavior absent ($B < 0.3$). *Example: "I want to start running" but 0 runs are logged.*
*   **INSUFFICIENT_EVIDENCE**: Sufficiency gate fails due to low volume, confidence, or time span.

## Explainability
*   **evidence_used**: Explicitly lists the strictly observed behaviors and statements used to make the classification.
*   **rationale**: Provides the logical explanation tracing the classification decision directly to the `evidence_used`.

## Safety Architecture
Structural safety guarantees are enforced by construction. The output schema (`DomainAnalysisResult`) fundamentally lacks fields for personality traits, diagnoses, or character judgments. The system uses strict Pydantic validation to ensure the `evidence_used` and `rationale` fields only describe observed behaviors, self-talk, and divergence calculations, rendering unsafe outputs structurally impossible.

## Uncertainty Model
Uncertainty scales based on data sparsity (low volume), source noise (low confidence scores), and internal behavioral variance within the domain. High uncertainty triggers automatic abstention.

## Failure Modes
*   **Sarcasm**: May skew self-talk sentiment; mitigated by high-confidence thresholding.
*   **Incomplete Logging**: Artificially lowers $B$; mitigated by data sparsity uncertainty triggering abstention.
*   **Domain Discovery Errors**: Disparate behaviors map incorrectly; mitigated by variance uncertainty checks overriding to abstention.
*   **Short Observation Windows**: Caught by the 7-day temporal coverage requirement.
*   **Private Behaviors**: Causes a partial picture; defaults to abstention if behavioral minimums aren't met.

## Testing Strategy
Focuses on boundary testing the mathematical thresholds, parameterizing abstention scenarios, fuzzing the canonicalization mapper, and running adversarial schemas to verify structural safety catches diagnostic attempts.

## Future Improvements
*   Enhanced temporal decay weighting (giving more weight to recent behaviors).
*   Integration with live-streaming behavioral data sources.
