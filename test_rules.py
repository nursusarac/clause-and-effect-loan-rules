<<<<<<< HEAD
import csv
import json
from pathlib import Path
from rules import LoanFieldRules

csv_path = Path("Hand-Checked Loan Terms Answer Key (20 Agreements).csv")

valid_count = 0
with csv_path.open(mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

    for row in rows:
        payload = {
            "agreement_id": row["agreement_id"],
            "borrower_name": row["borrower_name"],
            "commitment_amount": float(row["commitment_amount"]),
            "maturity_date": row["maturity_date"],
            "margin_type": row["margin_type"],
            "flat_margin_bps": float(row["flat_margin_bps"]) if row["flat_margin_bps"] else None,
            "pricing_grid": json.loads(row["pricing_grid"]) if row["pricing_grid"] else None,
            "max_leverage_ratio": float(row["max_leverage_ratio"]) if row["max_leverage_ratio"] else None,
            "min_interest_coverage_ratio": float(row["min_interest_coverage_ratio"]) if row["min_interest_coverage_ratio"] else None,
        }

        model = LoanFieldRules(**payload)
        valid_count += 1

=======
import csv
import json
from pathlib import Path
from rules import LoanFieldRules

csv_path = Path("Hand-Checked Loan Terms Answer Key (20 Agreements).csv")

valid_count = 0
with csv_path.open(mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

    for row in rows:
        payload = {
            "agreement_id": row["agreement_id"],
            "borrower_name": row["borrower_name"],
            "commitment_amount": float(row["commitment_amount"]),
            "maturity_date": row["maturity_date"],
            "margin_type": row["margin_type"],
            "flat_margin_bps": float(row["flat_margin_bps"]) if row["flat_margin_bps"] else None,
            "pricing_grid": json.loads(row["pricing_grid"]) if row["pricing_grid"] else None,
            "max_leverage_ratio": float(row["max_leverage_ratio"]) if row["max_leverage_ratio"] else None,
            "min_interest_coverage_ratio": float(row["min_interest_coverage_ratio"]) if row["min_interest_coverage_ratio"] else None,
        }

        model = LoanFieldRules(**payload)
        valid_count += 1

>>>>>>> 004e59bc490355f02e6d1d751370178a00e0b1fd
print(f"Success! {valid_count} / {len(rows)} loan agreements passed Pydantic validation.")