# Veritas

## Project Overview
Veritas is a Behavioral-Narrative Divergence Scoring assessment system. It evaluates the alignment between an individual's self-reported narrative (self-talk) and their objectively observed behavioral evidence. 

## Architecture Summary
The system operates as a robust data processing pipeline designed to calculate deterministic alignment without subjective psychological judgments:
1. **Domain Canonicalization Engine**: Dynamically clusters evidence and maps to stable domains.
2. **Evidence Sufficiency Gate**: Ensures strict data minimums to avoid premature classification.
3. **Alignment & Divergence Scorer**: Uses deterministic cosine similarity on embedded factual summaries.
4. **Structural Safety Layer**: Guarantees outputs contain only factual observed evidence.

## Repository Structure
```
veritas/
├── src/
│   ├── models/        # Pydantic schemas
│   ├── domains/       # Domain discovery and canonicalization
│   ├── gates/         # Evidence sufficiency logic
│   ├── scoring/       # Cosine alignment scoring
│   ├── classifier/    # Divergence boundary logic
│   ├── safety/        # Structural safety enforcement
│   └── utils/         # Configuration and helpers
├── tests/             # Pytest suite
├── results/           # Output folder for worked examples
├── data/              # Sample JSON data
├── docs/              # Technical documentation
├── decisions.md       # Architecture Decision Records
├── requirements.txt   # Dependencies
├── main.py            # Entrypoint script
└── README.md
```

## Setup Instructions
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment.
4. Install dependencies: `pip install -r requirements.txt`
