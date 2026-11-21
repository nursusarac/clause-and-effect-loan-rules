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
```## Claude Code Prompt Used
```text
Create `rules.py` and `test_rules.py` using Pydantic and `Hand-Checked Loan Terms Answer Key (20 Agreements).csv` with these validation rules:
- `agreement_id`: non-empty string (`str`).
- `borrower_name`: non-empty string (`str`) after stripping whitespace.
- `commitment_amount`: integer (`int`) strictly greater than `0` and up to `50,000,000,000`.
- `maturity_date`: valid calendar date (`YYYY-MM-DD`).
- `margin_type`: `"flat"` or `"grid"`.
  - If `"flat"`: require `flat_margin_bps` (`> 0`, `<= 2000`) and require `pricing_grid` to be `None`.
  - If `"grid"`: require a non-empty `pricing_grid` sorted in strictly ascending order by `leverage_threshold` (`> 0`), ending with a `99.00` catch-all tier carrying the highest `margin_bps` in the grid, and require `flat_margin_bps` to be `None`.
- Optional covenants (`max_leverage_ratio`, `min_interest_coverage_ratio`): `float | None` allowing `None` when absent, and validating `> 0` within a sensible upper bound when present.
<<<<<<< HEAD
In `test_rules.py`, load all 20 rows from `Hand-Checked Loan Terms Answer Key (20 Agreements).csv`, validate every row with `LoanFieldRules`, and print the result in English.
## Extraction Script Prompt
Read New Commercial Credit Agreements (Jul-Nov 2026 Signings).csv and extract structured loan rows for all 40 agreements using a free OpenRouter model with OPENROUTER_API_KEY loaded from .env. Read the entire greement_text so mid-text amendments (such as AGR-2026-019) supersede earlier rates, extract borrower details from the text even when greement_title differs (such as AGR-2026-016), normalize amounts and YYYY-MM-DD maturity dates (including relative anniversary terms), validate rows with the ules.py Pydantic models, and attach exact verbatim quotes from greement_text as proof for every field.

## Extraction Script Prompt
Read New Commercial Credit Agreements (Jul-Nov 2026 Signings).csv and extract standardized loan rows for all 40 agreements using a free OpenRouter model with OPENROUTER_API_KEY loaded from .env. Read the full greement_text so mid-text amendments (such as AGR-2026-019) replace earlier margins, extract borrower names from the text even when greement_title differs (such as AGR-2026-016), normalize integer amounts and YYYY-MM-DD maturity dates (including relative anniversary calculations), validate outputs with the Pydantic models in ules.py, and include exact verbatim quotes from greement_text for every field.
=======
In `test_rules.py`, load all 20 rows from `Hand-Checked Loan Terms Answer Key (20 Agreements).csv`, validate every row with `LoanFieldRules`, and print the result in English.
>>>>>>> 004e59bc490355f02e6d1d751370178a00e0b1fd
