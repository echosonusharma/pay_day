"""Pydantic schema for extracted_json.

Validates 12-field canonical JSON per doc/data_extrcataed_sms_.md
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# Allowed enums - Currency kept as str (not strict Literal) to allow future ISO codes (GBP, THB, etc.)
KNOWN_CURRENCIES = {"INR", "USD", "AED", "SAR", "ETB", "TZS", "NGN", "NPR", "EGP", "KES", "BDT", "OMR", "PKR", "LKR", "EUR", "TRY", "RUB", "CZK", "MZN", "GBP", "THB", "IRR", "BYN", "BHD", "KWD", "QAR"}

Currency = str | None
Direction = Literal["debit", "credit"] | None
TxnKind = Literal["upi", "card", "atm", "neft", "imps", "wallet", "transfer", "other"] | None
ExpenseType = Literal["food", "groceries", "travel", "fuel", "shopping", "bills", "entertainment", "health", "transfer", "income", "cash", "unknown"] | None
Status = Literal["posted", "failed", "otp", "info"] | None
Instrument = Literal["account", "card", "wallet"] | None


class ExtractedJson(BaseModel):
    amount: str | None = Field(default=None, description="digits with optional decimal, no currency")
    currency: str | None = Field(default=None)
    direction: Direction = None
    txn_kind: TxnKind = Field(default=None, alias="txn_kind")
    expense_type: ExpenseType = None
    status: Status = None
    account_last4: str | None = None
    instrument: Instrument = None
    counterparty: str | None = None
    reference: str | None = None
    balance: str | None = None
    txn_date: str | None = None

    model_config = {"populate_by_name": True, "extra": "forbid"}

    @field_validator("amount", "balance")
    @classmethod
    def validate_money(cls, v):
        if v is None:
            return v
        if not re.fullmatch(r"\d+(?:\.\d+)?", str(v)):
            raise ValueError(f"must be digits with optional decimal, got {v!r}")
        return str(v)

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v):
        if v is None:
            return v
        v = str(v).upper().strip()
        if not re.fullmatch(r"[A-Z]{3}", v):
            raise ValueError(f"currency must be 3-letter ISO-4217, got {v!r}")
        # strict warning for unknown but allow - keeps Literal-like safety without blocking GBP/THB
        # if v not in KNOWN_CURRENCIES: raise ValueError(f"unknown currency {v!r}")
        return v

    @field_validator("account_last4")
    @classmethod
    def validate_last4(cls, v):
        if v is None:
            return v
        if not re.fullmatch(r"\d{4}", str(v)):
            raise ValueError(f"account_last4 must be 4 digits, got {v!r}")
        return str(v)

    @field_validator("txn_date")
    @classmethod
    def validate_date(cls, v):
        if v is None:
            return v
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(v)):
            raise ValueError(f"txn_date must be YYYY-MM-DD, got {v!r}")
        return str(v)

    @field_validator("reference", "counterparty")
    @classmethod
    def validate_strip(cls, v):
        if v is None:
            return v
        v = str(v).strip()
        return v if v else None
