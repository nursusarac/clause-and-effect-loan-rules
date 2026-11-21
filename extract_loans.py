import json
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

CSV_PATH = Path("New Commercial Credit Agreements (Jul-Nov 2026 Signings).csv")
OUTPUT_PATH = Path("loan_rows.json")
FREE_MODEL = "openrouter/free"  # veya OpenRouter'daki aktif ücretsiz model kimliği

EXTRACTION_PROMPT = """
You are a commercial credit data extraction assistant.
Read the full agreement_text carefully (never stop at the first clause, because later amendments like Section 2.03 in AGR-2026-019 can override earlier terms, and borrower names in text like AGR-2026-016 can differ from agreement_title).

Extract the loan fields following the project's Pydantic validation rules, convert amounts to exact integers and dates to YYYY-MM-DD (computing anniversary/term dates from Closing Date / signed_date when needed), and include an exact verbatim quote from agreement_text as proof for every extracted field.
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
    results = []

    for _, row in df.iterrows():
        payload = {
            "agreement_id": row["agreement_id"],
            "agreement_title": row["agreement_title"],
            "facility_type": row["facility_type"],
            "signed_date": str(row["signed_date"]),
            "agreement_text": row["agreement_text"],
        }

        response = client.chat.completions.create(
            model=FREE_MODEL,
            messages=[
                {"role": "system", "content": EXTRACTION_PROMPT},
                {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
            ],
        )

        content = response.choices[0].message.content or ""
        results.append(
            {
                "agreement_id": row["agreement_id"],
                "raw_model_output": content,
            }
        )

    OUTPUT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Processed {len(results)} agreements -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()