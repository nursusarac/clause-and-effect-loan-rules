# Clause and Effect — Loan Field Validation Rules

Pydantic validation models and test scripts for automated loan agreement field checks.

## Project Structure
- `rules.py`: Pydantic schema and validation rules (`PricingTier` and `LoanFieldRules`) for borrower name, commitment amount, maturity date, flat/grid margin rules, and covenants.
- `test_rules.py`: Validation runner testing the schema against the 20-agreement answer key CSV.
- `Hand-Checked Loan Terms Answer Key (20 Agreements).csv`: Reference dataset of 20 loan agreements.

## Setup & Usage
```bash
python -m pip install pydantic
python test_rules.py
```