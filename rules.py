from datetime import date
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class PricingTier(BaseModel):
    leverage_threshold: float = Field(..., gt=0)
    margin_bps: float = Field(..., gt=0, le=2000)


class LoanFieldRules(BaseModel):
    agreement_id: str = Field(..., min_length=1)
    borrower_name: str = Field(..., min_length=1)
    commitment_amount: int = Field(..., gt=0, le=50_000_000_000)
    maturity_date: date
    margin_type: Literal["flat", "grid"]
    flat_margin_bps: Optional[float] = Field(default=None, gt=0, le=2000)
    pricing_grid: Optional[List[PricingTier]] = Field(default=None)
    max_leverage_ratio: Optional[float] = Field(default=None, gt=0, le=50)
    min_interest_coverage_ratio: Optional[float] = Field(default=None, gt=0, le=50)

    @field_validator("borrower_name")
    @classmethod
    def validate_borrower_name(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("borrower_name cannot be empty")
        return cleaned

    @model_validator(mode="after")
    def validate_margin_structure(self) -> "LoanFieldRules":
        if self.margin_type == "flat":
            if self.flat_margin_bps is None:
                raise ValueError("flat_margin_bps is required when margin_type is 'flat'")
            if self.pricing_grid is not None:
                raise ValueError("pricing_grid must be None when margin_type is 'flat'")
        elif self.margin_type == "grid":
            if not self.pricing_grid or len(self.pricing_grid) == 0:
                raise ValueError("pricing_grid must be non-empty when margin_type is 'grid'")
            if self.flat_margin_bps is not None:
                raise ValueError("flat_margin_bps must be None when margin_type is 'grid'")

            thresholds = [tier.leverage_threshold for tier in self.pricing_grid]
            if thresholds != sorted(thresholds) or len(set(thresholds)) != len(thresholds):
                raise ValueError("pricing_grid tiers must be strictly sorted by leverage_threshold")

            if self.pricing_grid[-1].leverage_threshold != 99.0:
                raise ValueError("pricing_grid must end with the 99.00 catch-all tier")

            max_bps = max(tier.margin_bps for tier in self.pricing_grid)
            if self.pricing_grid[-1].margin_bps != max_bps:
                raise ValueError("catch-all tier (99.00) must carry the highest margin_bps in the grid")

        return self