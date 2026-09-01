# PAY DAY - Data Extraction Spec (simple)

Extract 12 fields from a single bank/wallet SMS. No sender/metadata. Two outputs: JSON (truth) and condensed text (12 lines, empty = null, derived from JSON).

## Schema (12 keys, null if not in text)

```json
{
  "amount": "512.75",
  "currency": "INR",
  "direction": "debit",
  "txn_kind": "upi",
  "expense_type": "food",
  "status": "posted",
  "account_last4": "7391",
  "instrument": "account",
  "counterparty": "Sharma Sweets",
  "reference": "123",
  "balance": "1000.00",
  "txn_date": "2026-08-18"
}
```

| field | type | note |
| ------- | ------ | ------ |
| amount,balance | string\|null | digits + `.` only, strip Rs/₹/$/Ksh/Tk/, normalize `,`->`.` for CZK/TRY/RUB |
| currency | string\|null | ISO 4217 (INR,USD,AED...), Rs→INR, $→USD |
| direction | debit/credit/null | debit=spent/sent/paid, credit=credited/received |
| txn_kind | upi/card/atm/neft/imps/wallet/transfer/other/null | most specific hint in text |
| expense_type | food/groceries/travel/fuel/shopping/bills/entertainment/health/transfer/income/cash/unknown/null | deterministic from template; credit→income, atm→cash |
| status | posted/failed/otp/info/null | |
| account_last4 | string\|null | 4 digits from `*7391` |
| instrument | account/card/wallet/null | A/c→account, card→card, wallet→wallet |
| counterparty | string\|null | merchant/payee, strip boilerplate |
| reference | string\|null | best ID (RRN>UPI>TxnId) |
| txn_date | string\|null | ISO YYYY-MM-DD, 24-26→2024-2026 |

Null = do not invent.

## Condensed (inference, 12 lines fixed order)

Keys: `amt,cur,dir,kind,exp,stat,acct,inst,cp,ref,bal,date`

```text
amt:512.75
cur:INR
dir:d
kind:u
exp:f
stat:p
acct:7391
inst:a
cp:Sharma Sweets
ref:123
bal:1000.00
date:2026-08-18
```

Enum codes: `dir d/c`, `kind u/cd/a/n/i/w/t/o`, `exp f/g/tr/fu/s/b/e/h/t/in/ca/x`, `stat p/f/otp/i`, `inst a/c/w`. Empty after `:` = null (e.g. `amt:`). Escape `:`→`\:` `\\`→`\\` `\n`→`\n`. Parser `condensed_to_json` handles `""` and legacy `"nl"`.

Example null row:

```text
amt:
cur:
dir:
kind:
exp:
stat:
acct:
inst:
cp:
ref:
bal:
date:
```

## Dataset Row (NDJSON)

| field | type | desc |
| ------- | ------ | ------ |
| sequence | string | SMS body |
| uuid | string | custom `syn_012hex` / `hs_...` / `ext_...` via `rng.getrandbits(48)` |
| source | enum | `synthetic` / `ham_spam` / `external_ham_spam_v1` |
| is_synthetic | bool | |
| bank,country,currency,template_key | string\|null | from template if synthetic |
| class_label | enum | `financial` / `non_financial` |
| label_source | enum | `template_slots` / `heuristic` |
| extracted_json | object | 12-field truth (all null for non_financial) |
| extracted_condensed | string | `json_to_condensed` |
| field_density | float | non-null/12 (1.0 for financial, 0 for non_financial) |
| expected_data_detail_level | enum | `very_detailed` / `null` (all synthetic very_detailed now) |
| char_len, word_count | int | for filtering |
| split | enum | train/val/test (80/10/10 stratified) |

## Pipeline (build_dataset.py globals, no CLI)

Globals in `build_dataset.py:32`:

```python
SYNTH_N = 5000
SEED = 42
NEG_RATIO = 0.3
OUT_PATH = None  # -> data/payday_YYYYMMDD.ndjson
```

1. **Synthetic**: `synth_templates.py` (115 templates, 19 locales) -> `generate_synth.py:188` `make_slots` + `pennywise_regex.json` gate `labels_ok:78` -> `extracted_json` all 12 fields (`very_detailed` only) -> `synth_msg.ndjson`
2. **Negatives**: `raw_data/ham_spam_dataset.json` (184) + `raw_data/sms-spam-collection-llama2-5k.json` sampled 2000 via `rng.sample` -> all-null JSON
3. **Mix**: negatives = positives * `NEG_RATIO` sampled from pool (oversample with `rng.choices` if needed) -> interleaved mix
4. **Dedup**: key `norm + source + detail + json_hash` (`build_dataset.py:144`)
5. **Split**: stratified by `(country,bank,class_label,txn_kind)` 80/10/10
6. **Write**: `data/payday_*.ndjson` + `.meta.json`

Run: `uv run python build_dataset.py` (edit globals then run)

## Validation

- Pydantic `schema.py:24` `ExtractedJson` (money regex `\d+(?:\.\d+)?`, currency `^[A-Z]{3}$`, last4 `^\d{4}$`, date `^\d{4}-\d{2}-\d{2}$`)
- Money/balance digits must match span in sequence
- Reference substring must appear in sequence
- `condensed` round-trip asserts `json == condensed_to_json(json_to_condensed(json))`

## Files

`schema.py` schema, `condensed.py` parser, `generate_synth.py` generator+gate, `synth_templates.py` templates, `build_dataset.py` orchestrator, `zen_api.py` (unused, for real data later).
