import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

load_dotenv()

CSV_PATH = Path("New Commercial Credit Agreements (Jul-Nov 2026 Signings).csv")
OUTPUT_PATH = Path("loan_rows.json")
MODEL_NAME = "openrouter/free"

EXTRACTION_PROMPT = """
You are a commercial credit agreement extraction engine.
Read the entire agreement_text before extracting fields so later amendments or overriding clauses (such as a Section 2.03 amendment changing a margin tier in AGR-2026-019) supersede earlier statements.

Rules:
1. Handle varying clause numbering, clause ordering, and borrower labels ("Borrower" vs. "Company"), and extract borrower names from agreement_text even when agreement_title differs (as in AGR-2026-016).
2. Normalize commitment amounts into exact integer values and maturity dates into YYYY-MM-DD (calculating dates from closing/signing dates when expressed as an anniversary or term duration).
3. Follow the project's Pydantic validation rules (from rules.py) and include exact verbatim quotes from agreement_text as proof for every extracted field.
4. Return valid JSON only.
"""


def main() -> None:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing in environment/.env")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    df = pd.read_csv(CSV_PATH)
    extracted_rows = []

    for _, row in df.iterrows():
        payload = {
            "agreement_id": row["agreement_id"],
            "agreement_title": row["agreement_title"],
            "facility_type": row["facility_type"],
            "signed_date": str(row["signed_date"]),
            "agreement_text": row["agreement_text"],
        }

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": EXTRACTION_PROMPT.strip()},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
        )

        content = response.choices[0].message.content or ""
        extracted_rows.append(
            {
                "agreement_id": row["agreement_id"],
                "raw_response": content,
            }
        )

    OUTPUT_PATH.write_text(
        json.dumps(extracted_rows, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Extracted {len(extracted_rows)} agreements to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
