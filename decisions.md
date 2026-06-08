# Veritas Design Decisions

## Alignment Method
**Decision:** Use Embeddings + Cosine Similarity.
**Rationale:** Deterministic mathematical scoring is vastly superior to LLM semantic reasoning for core scoring. It guarantees reproducibility, mathematical explainability, easier unit testing, and eliminates the risk of an LLM "hallucinating" alignment or being biased by conversational framing.

## Domain Strategy
**Decision:** Hybrid Discovery + Canonicalization.
**Rationale:** A purely fixed taxonomy forces behaviors into ill-fitting buckets and causes information loss. Purely dynamic clustering leads to massive fragmentation (e.g., "gym" vs "lifting"), breaking longitudinal tracking. The hybrid model preserves the nuance of dynamic discovery while standardizing outputs into stable canonical domains.

## Divergence Categories
**Summary of Categories:**
*   **ALIGNED**: Narrative matches reality.
*   **OVERSTATEMENT**: Narrative claims exceed behavioral reality.
*   **UNDERSTATEMENT**: Behavioral reality exceeds narrative claims.
*   **BLIND_SPOT**: Strong behavioral reality exists with a complete lack of narrative awareness.
*   **ASPIRATION_GAP**: Narrative focuses on future goals while current behavior is absent.
*   **INSUFFICIENT_EVIDENCE**: Data is too sparse, noisy, or recent to classify.

## Evidence Sufficiency
**Decision:** Abstention is a first-class, successful outcome.
**Rationale:** Premature classification on sparse or noisy data is a system failure. By enforcing strict minimums (e.g., 3 behaviors, 2 self-talk statements, 7 days coverage), the system prioritizes accuracy over completion. The system defaults to `INSUFFICIENT_EVIDENCE` when uncertainty is high.

## Explainability
**Decision:** Explicit traceability in output schema.
**Rationale:** Black-box scores are untrustworthy. Every output includes `evidence_used` (the exact observed events/statements) and a `rationale` bridging the math to the final category, ensuring total transparency.

## Safety Guarantees
**Decision:** Structural Safety (By Construction) rather than Prompting/Blacklists.
**Rationale:** Prompting an LLM "not to diagnose" is unreliable and prone to failure. By designing the output schema to strictly accept only `domain`, `score`, `category`, `evidence_used`, and `rationale`, we make it structurally impossible for the system to output a psychological diagnosis or personality trait.

## Key Tradeoffs
*   **Recall vs. Precision**: We heavily bias towards Precision. By enforcing strict sufficiency gates, the system will frequently output `INSUFFICIENT_EVIDENCE` (low recall) to guarantee that when it *does* make a classification, it is highly accurate and defensible.
*   **Nuance vs. Determinism**: We trade the deep semantic nuance of an LLM judge for the hard reproducibility of cosine similarity, accepting that edge cases in human language might occasionally be flattened in favor of mathematical stability.

## What Veritas Refuses To Claim
To maintain ethical boundaries and strict analytical integrity, the Veritas system explicitly:
*   **does not infer personality**
*   **does not assess motivation**
*   **does not diagnose conditions**
*   **does not determine truthfulness**
*   **does not judge character**

It *only* measures the mathematical divergence between observed behavior and self-reported narrative under available evidence.
