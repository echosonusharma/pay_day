"""
Build PAY DAY dataset: synthetic + ham/spam → NDJSON with stratified split.
Handles all generation - no separate generate_synth.py needed.
uv run python build_dataset.py 
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import string
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(ROOT))

from condensed import json_to_condensed
from schema import ExtractedJson
from synth_templates import AMOUNT_RANGE, LOCALES, PREFIXES, TEMPLATES, Locale, Template

RAW = ROOT / "raw_data"
OUT_DIR = ROOT / "data"
OUT_DIR.mkdir(exist_ok=True)
PENNYWISE_PATH = RAW / "pennywise_regex.json"

FIELD_KEYS = list(ExtractedJson.model_fields.keys())

# ========= Global config - edit here =========
SYNTH_N = 5000  # number of base synthetic rows to generate
SEED = 42
NEG_RATIO = 0.3  # negatives = positives * NEG_RATIO, sampled from ham_spam + external pool
OUT_PATH: Path | None = None  # if None, auto uses data/payday_YYYYMMDD.ndjson
RETRIES = 12  # retries per template for Pennywise gate
# =============================================

Compiled = list[tuple[dict, re.Pattern[str]]]


def _gen_uuid(rng: random.Random, prefix: str) -> str:
    val = rng.getrandbits(48)
    return f"{prefix}_{val:012x}"


# ---- Synthetic generation (inlined from generate_synth.py) ----

def load_bank_regexes() -> dict[str, list[dict]]:
    data = json.loads(PENNYWISE_PATH.read_text())
    by_bank: dict[str, list[dict]] = {}
    for row in data["regexes"]:
        bank = row.get("bank")
        if bank:
            by_bank.setdefault(bank, []).append(row)
    return by_bank


def compile_flags(options: str | None) -> int:
    flags = 0
    if not options:
        return flags
    if "IGNORE_CASE" in options:
        flags |= re.IGNORECASE
    if "MULTILINE" in options:
        flags |= re.MULTILINE
    if "DOT_MATCHES_ALL" in options:
        flags |= re.DOTALL
    return flags


def compile_bank(regexes: list[dict]) -> Compiled:
    compiled: Compiled = []
    for row in regexes:
        if row.get("category") in ("sender_validation", "cleaning"):
            continue
        try:
            compiled.append((row, re.compile(row["pattern"], compile_flags(row.get("options")))))
        except re.error:
            continue
    return compiled


def extract_hits(body: str, compiled: Compiled) -> list[dict]:
    hits: list[dict] = []
    for row, cre in compiled:
        m = cre.search(body)
        if m:
            hits.append({"id": row["id"], "category": row.get("category"), "groups": list(m.groups())})
    return hits


def digits_only(s: str) -> str:
    s = s.strip()
    if "," in s and "." not in s:
        s = s.replace(",", ".")
    else:
        s = s.replace(",", "")
    return re.sub(r"[^\d.]", "", s)


def labels_ok(labels: dict[str, str], hits: list[dict], required: tuple[str, ...]) -> bool:
    groups = [g for h in hits for g in h["groups"] if g]
    for key in required:
        val = labels[key]
        if key in ("amount", "balance"):
            target = digits_only(val)
            if not any(digits_only(g) == target for g in groups):
                return False
        elif key == "last4":
            if not any(val in g.replace("X", "").replace("*", "") for g in groups if "." not in g):
                return False
        elif not any(val in g for g in groups):
            return False
    return True


def fmt_money(rng: random.Random, lo: float, hi: float) -> str:
    n = round(rng.uniform(lo, hi), 2)
    return f"{n:.2f}"


def pick_merchant(rng: random.Random, tmpl: Template, locale: Locale) -> str:
    if tmpl.one_word_merchant:
        name = rng.choice(locale.brands + locale.surnames).split()[0]
    else:
        roll = rng.random()
        if roll < 0.28:
            name = rng.choice(locale.brands)
        elif roll < 0.65:
            name = f"{rng.choice(locale.surnames)} {rng.choice(locale.shops)}"
        else:
            name = f"{rng.choice(locale.firsts)} {rng.choice(locale.surnames)}"
    name = name.replace(".", " ").strip()
    if tmpl.merchant_upper:
        name = name.upper()
    return name


def random_dates(rng: random.Random) -> dict[str, str]:
    year = rng.choice((24, 25, 26))
    month = rng.randint(1, 12)
    day = rng.randint(1, 28)
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    mon = months[month - 1]
    hour = rng.randint(8, 21)
    minute = rng.randint(0, 59)
    ampm = "AM" if hour < 12 else "PM"
    hour12 = hour % 12 or 12
    return {
        "date_dmy": f"{day:02d}-{month:02d}-{year:02d}",
        "date_dmy4": f"{day:02d}-{month:02d}-20{year:02d}",
        "date_mon": f"{day:02d}-{mon}-{year:02d}",
        "date_day_mon": f"{day} {mon}",
        "date_us": f"{mon} {day}, 20{year:02d}",
        "date_slash": f"{day:02d}/{month:02d}/20{year:02d}",
        "date_mash": f"{day}-{mon.upper()}-20{year:02d} {hour12}:{minute:02d} {ampm}",
        "date_dmon4": f"{day:02d}-{mon}-20{year:02d}",
        "time": f"{hour:02d}:{minute:02d}:{rng.randint(0, 59):02d}",
        "time_hm": f"{hour:02d}:{minute:02d}",
    }


EXPENSE_KEYWORDS: dict[str, str] = {
    "sweets": "food", "cafe": "food", "zomato": "food", "swiggy": "food", "restaurant": "food", "diner": "food", "hotel": "food", "java house": "food",
    "kirana": "groceries", "grocery": "groceries", "supermarket": "groceries", "mini market": "groceries", "panda": "groceries", "carrefour": "groceries", "lulu": "groceries", "spinneys": "groceries", "walmart": "groceries",
    "uber": "travel", "careem": "travel", "irctc": "travel", "travel": "travel",
    "fuel": "fuel", "petrol": "fuel", "adnoc": "fuel", "pso": "fuel", "gas station": "fuel", "fuel station": "fuel",
    "amazon": "shopping", "flipkart": "shopping", "walmart": "shopping", "target": "shopping", "costco": "shopping", "daraz": "shopping", "noon": "shopping", "trendyol": "shopping", "wildberries": "shopping", "ozon": "shopping", "alza": "shopping",
    "electricity": "bills", "recharge": "bills", "bharat": "bills", "dstv": "bills", "ooredoo": "bills",
    "pharmacy": "health", "medical": "health", "lekarn": "health", "apteka": "health", "health": "health",
    "cinema": "entertainment", "entertainment": "entertainment",
}


def infer_expense_type(merchant: str, fallback: str) -> str:
    if fallback != "unknown":
        return fallback
    low = merchant.lower()
    for kw, cat in EXPENSE_KEYWORDS.items():
        if kw in low:
            return cat
    return "unknown"


def make_slots(rng: random.Random, tmpl: Template) -> dict[str, str]:
    locale = LOCALES.get(tmpl.country, LOCALES["United States"])
    lo, hi = AMOUNT_RANGE.get(tmpl.currency, (10.0, 5_000.0))
    amount = fmt_money(rng, lo, hi)
    balance = fmt_money(rng, hi * 0.9, hi * 6)
    if tmpl.currency in {"CZK", "TRY", "RUB"} or tmpl.key == "sparkasse_eur":
        amount = amount.replace(".", ",")
        balance = balance.replace(".", ",")
    last4 = f"{rng.randint(1000, 9999)}"
    rrn = "".join(str(rng.randint(0, 9)) for _ in range(12))
    rrn10 = "QH" + "".join(rng.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    merchant = pick_merchant(rng, tmpl, locale)
    slug = re.sub(r"[^a-z0-9]", "", merchant.lower())[:10] or "pay"
    slots = {
        "last4": last4,
        "rrn": rrn,
        "rrn10": rrn10,
        "amount": amount,
        "balance": balance,
        "merchant": merchant,
        "upi": f"{slug}@okicici",
    }
    slots.update(random_dates(rng))
    return slots


def generate_one(rng: random.Random, tmpl: Template, compiled: Compiled) -> dict | None:
    slots = make_slots(rng, tmpl)
    body = tmpl.body.format(**slots)
    hits = extract_hits(body, compiled)
    ref = slots["rrn10"] if "{rrn10}" in tmpl.body else slots["rrn"]
    expense_type = infer_expense_type(slots["merchant"], tmpl.expense_type)
    if tmpl.txn_type == "atm" and expense_type == "unknown":
        expense_type = "cash"
    labels = {
        "txn_type": tmpl.txn_type,
        "amount": slots["amount"],
        "account": f"*{slots['last4']}",
        "last4": slots["last4"],
        "merchant": slots["merchant"],
        "reference": ref,
        "balance": slots["balance"],
        "date": slots["date_dmy"],
        "expense_type": expense_type,
    }
    if not labels_ok(labels, hits, tmpl.required):
        return None
    direction = "credit" if tmpl.txn_type == "credit" else "debit"
    if tmpl.txn_type == "atm":
        direction = "debit"
    txn_kind_map = {"debit": "transfer", "credit": "transfer", "atm": "atm"}
    body_low = body.lower()
    if "upi" in body_low or "vpa" in body_low:
        txn_kind = "upi"
    elif "card" in body_low or "pos" in body_low or "spent" in body_low:
        txn_kind = "card"
    elif "atm" in body_low or "withdrawn" in body_low or "withdrawal" in body_low:
        txn_kind = "atm"
    elif "neft" in body_low or "rtgs" in body_low:
        txn_kind = "neft"
    elif "imps" in body_low:
        txn_kind = "imps"
    elif any(w in body_low for w in ("m-pesa", "mpesa", "bkash", "tigo", "opay", "wallet", "telebirr")):
        txn_kind = "wallet"
    else:
        txn_kind = txn_kind_map.get(tmpl.txn_type, "other")
    instrument = "wallet" if txn_kind == "wallet" else "card" if txn_kind == "card" else "account"
    try:
        d, m, y = slots["date_dmy"].split("-")
        txn_date = f"20{y}-{m}-{d}"
    except Exception:
        txn_date = None
    extracted_json = {
        "amount": slots["amount"].replace(",", "."),
        "currency": tmpl.currency,
        "direction": direction,
        "txn_kind": txn_kind,
        "expense_type": expense_type,
        "status": "posted",
        "account_last4": slots["last4"],
        "instrument": instrument,
        "counterparty": slots["merchant"],
        "reference": ref,
        "balance": slots["balance"].replace(",", "."),
        "txn_date": txn_date,
    }
    return {
        "bank": tmpl.bank,
        "country": tmpl.country,
        "currency": tmpl.currency,
        "template": tmpl.key,
        "body": body,
        "extracted_json": extracted_json,
    }


def try_until(rng: random.Random, tmpl: Template, compiled: Compiled) -> tuple[dict | None, int]:
    for i in range(1, RETRIES + 1):
        rec = generate_one(rng, tmpl, compiled)
        if rec is not None:
            return rec, i
    return None, RETRIES


# ---- Dataset helpers ----

def load_ham_spam(rng: random.Random) -> list[dict]:
    with open(RAW / "ham_spam_dataset.json") as f:
        data = json.load(f)
    rows = []
    for i, item in enumerate(data):
        rows.append({
            "sequence": item["Message"],
            "uuid": _gen_uuid(rng, "hs"),
            "source": "ham_spam",
            "is_synthetic": False,
            "bank": None,
            "country": None,
            "currency": None,
            "template_key": None,
            "class_label": "non_financial",
            "label_source": "heuristic",
            "extracted_json": {k: None for k in FIELD_KEYS},
            "extracted_condensed": json_to_condensed({k: None for k in FIELD_KEYS}),
            "field_density": 0.0,
            "expected_data_detail_level": "null",
            "char_len": len(item["Message"]),
            "word_count": len(item["Message"].split()),
            "split": None,
        })
    return rows


def load_external_ham_spam(rng: random.Random, n: int = 2000) -> list[dict]:
    path = RAW / "sms-spam-collection-llama2-5k.json"
    if not path.exists():
        print(f"WARNING: {path} not found, skipping external ham/spam")
        return []
    with open(path) as f:
        data = json.load(f)
    if len(data) > n:
        sampled = rng.sample(data, k=n)
    else:
        sampled = data
    rows = []
    for item in sampled:
        msg = item.get("message") or item.get("v2_raw") or item.get("text") or ""
        if msg.startswith("<s>[INST]"):
            msg = item.get("message", msg)
        if not msg:
            continue
        rows.append({
            "sequence": msg,
            "uuid": _gen_uuid(rng, "ext"),
            "source": "external_ham_spam_v1",
            "is_synthetic": False,
            "bank": None,
            "country": None,
            "currency": None,
            "template_key": None,
            "class_label": "non_financial",
            "label_source": "heuristic",
            "extracted_json": {k: None for k in FIELD_KEYS},
            "extracted_condensed": json_to_condensed({k: None for k in FIELD_KEYS}),
            "field_density": 0.0,
            "expected_data_detail_level": "null",
            "char_len": len(msg),
            "word_count": len(msg.split()),
            "split": None,
        })
    return rows


def create_synthetic_variants(rec: dict, rng: random.Random) -> list[dict]:
    json_data = rec["extracted_json"].copy()
    condensed = json_to_condensed(json_data)
    return [{
        "sequence": rec["body"],
        "uuid": _gen_uuid(rng, "syn"),
        "source": "synthetic",
        "is_synthetic": True,
        "bank": rec["bank"],
        "country": rec["country"],
        "currency": rec["currency"],
        "template_key": rec["template"],
        "class_label": "financial",
        "label_source": "template_slots",
        "extracted_json": json_data,
        "extracted_condensed": condensed,
        "field_density": 1.0,
        "expected_data_detail_level": "very_detailed",
        "char_len": len(rec["body"]),
        "word_count": len(rec["body"].split()),
        "split": None,
    }]


def dedup(rows: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for r in rows:
        norm = re.sub(r"\s+", " ", r["sequence"].strip())
        detail = r.get("expected_data_detail_level") or ""
        json_hash = hashlib.sha256(json.dumps(r.get("extracted_json", {}), sort_keys=True).encode()).hexdigest()[:8]
        key = hashlib.sha256((norm + "|" + r["source"] + "|" + detail + "|" + json_hash).encode()).hexdigest()[:16]
        if key not in seen:
            seen.add(key)
            unique.append(r)
    print(f"Dedup: {len(rows)} → {len(unique)}")
    return unique


def stratified_split(rows: list[dict], seed: int = 42) -> list[dict]:
    random.seed(seed)
    groups = defaultdict(list)
    for r in rows:
        key = (r["country"] or "UNK", r["bank"] or "UNK", r["class_label"], r.get("extracted_json", {}).get("txn_kind") or "UNK")
        groups[key].append(r)
    for group in groups.values():
        random.shuffle(group)
    for key, group in groups.items():
        n = len(group)
        n_train = max(1, int(n * 0.8))
        n_val = max(1, int(n * 0.1))
        for i, r in enumerate(group):
            if i < n_train:
                r["split"] = "train"
            elif i < n_train + n_val:
                r["split"] = "val"
            else:
                r["split"] = "test"
    return rows


def write_ndjson(rows: list[dict], path: Path):
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def write_meta(rows: list[dict], path: Path):
    from collections import Counter
    meta = {
        "total": len(rows),
        "by_source": dict(Counter(r["source"] for r in rows)),
        "by_country": dict(Counter(r["country"] for r in rows)),
        "by_class": dict(Counter(r["class_label"] for r in rows)),
        "by_split": dict(Counter(r["split"] for r in rows)),
        "by_detail_level": dict(Counter(r["expected_data_detail_level"] for r in rows)),
        "field_density_histogram": {
            "0": sum(1 for r in rows if r["field_density"] == 0),
            "0-0.33": sum(1 for r in rows if 0 < r["field_density"] <= 1/3),
            "0.33-0.66": sum(1 for r in rows if 1/3 < r["field_density"] <= 2/3),
            "0.66-1": sum(1 for r in rows if r["field_density"] > 2/3),
        },
        "created": datetime.now().isoformat(),
    }
    path.write_text(json.dumps(meta, indent=2))


def main():
    out_path = OUT_PATH if OUT_PATH else OUT_DIR / f"payday_{datetime.now():%Y%m%d}.ndjson"
    rng = random.Random(SEED)
    all_rows = []

    # Generate synthetic in-memory (no intermediate file)
    print("Generating synthetic data...")
    needed = {t.bank for t in TEMPLATES}
    all_regexes = load_bank_regexes()
    compiled_by_bank: dict[str, Compiled] = {}
    for bank in sorted(needed):
        if bank not in all_regexes:
            raise SystemExit(f"no Pennywise regexes for {bank}")
        compiled_by_bank[bank] = compile_bank(all_regexes[bank])
        if not compiled_by_bank[bank]:
            raise SystemExit(f"no usable extract regexes for {bank}")
    for tmpl in TEMPLATES:
        rec, _ = try_until(rng, tmpl, compiled_by_bank[tmpl.bank])
        if rec is None:
            raise SystemExit(f"template {tmpl.key} failed smoke ({RETRIES} tries)")
    print(f"smoke ok  {len(TEMPLATES)} templates")

    base_rows: list[dict] = []
    written = 0
    rejected = 0
    while written < SYNTH_N:
        tmpl = TEMPLATES[written % len(TEMPLATES)]
        rec, used = try_until(rng, tmpl, compiled_by_bank[tmpl.bank])
        rejected += used - 1 if rec else used
        if rec is None:
            raise SystemExit(f"template {tmpl.key} never passed regex gate")
        base_rows.append(rec)
        written += 1
        if written % 500 == 0 or written == SYNTH_N:
            print(f"wrote {written}/{SYNTH_N}  rejected={rejected}")
    print(f"  loaded {len(base_rows)} base synthetic rows")

    for rec in base_rows:
        all_rows.extend(create_synthetic_variants(rec, rng))
    print(f"  created {len(all_rows)} synthetic rows (all very_detailed)")

    print("Loading ham/spam...")
    ham_spam_rows = load_ham_spam(rng)
    print(f"  loaded {len(ham_spam_rows)} ham/spam rows from ham_spam_dataset.json")

    print("Loading external ham/spam (2k sample)...")
    external_rows = load_external_ham_spam(rng, n=2000)
    print(f"  loaded {len(external_rows)} rows from sms-spam-collection-llama2-5k.json")

    neg_pool = ham_spam_rows + external_rows
    rng.shuffle(neg_pool)
    print(f"  total negative pool: {len(neg_pool)} (ham_spam + external)")

    desired_neg = int(len(all_rows) * NEG_RATIO)
    if NEG_RATIO > 0 and desired_neg == 0 and len(all_rows) > 0:
        desired_neg = 1
    print(f"  NEG_RATIO={NEG_RATIO} -> desired negatives: {desired_neg} (positives {len(all_rows)} * ratio)")
    if desired_neg == 0:
        neg_rows = []
    elif desired_neg <= len(neg_pool):
        neg_rows = rng.sample(neg_pool, k=desired_neg)
        rng.shuffle(neg_rows)
    else:
        print(f"  WARNING: desired {desired_neg} > pool {len(neg_pool)}, oversampling with replacement to meet ratio")
        extra = desired_neg - len(neg_pool)
        neg_rows = neg_pool + rng.choices(neg_pool, k=extra)
        rng.shuffle(neg_rows)
    print(f"  sampled negatives: {len(neg_rows)} (from pool {len(neg_pool)})")

    print("Mixing positives & negatives throughout...")
    mixed_rows = []
    synth_iter = iter(all_rows)
    neg_iter = iter(neg_rows)
    synth_exhausted = False
    neg_exhausted = False
    while not synth_exhausted or not neg_exhausted:
        if not synth_exhausted:
            try:
                mixed_rows.append(next(synth_iter))
            except StopIteration:
                synth_exhausted = True
        if not neg_exhausted:
            try:
                mixed_rows.append(next(neg_iter))
            except StopIteration:
                neg_exhausted = True
    all_rows = mixed_rows
    print(f"  mixed total: {len(all_rows)} rows (financial={sum(1 for r in all_rows if r['class_label']=='financial')} non_financial={sum(1 for r in all_rows if r['class_label']=='non_financial')})")

    print("Deduplicating...")
    all_rows = dedup(all_rows)

    print("Stratified split...")
    all_rows = stratified_split(all_rows, SEED)

    print(f"Writing {len(all_rows)} rows to {out_path}")
    write_ndjson(all_rows, out_path)

    meta_path = out_path.with_suffix(".meta.json")
    write_meta(all_rows, meta_path)
    print(f"Meta written to {meta_path}")

    print("Done.")


if __name__ == "__main__":
    main()
