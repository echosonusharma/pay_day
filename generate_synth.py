"""Generate synthetic bank SMS from templates; keep rows Pennywise regexes parse.

    uv run python generate_synth.py --n 5000 --out raw_data/synth_msg_5k.ndjson
"""

from __future__ import annotations

import argparse
import json
import random
import re
import string
from collections import Counter
from pathlib import Path

from synth_templates import AMOUNT_RANGE, LOCALES, PREFIXES, TEMPLATES, Locale, Template

ROOT = Path(__file__).resolve().parent
PENNYWISE_PATH = ROOT / "raw_data" / "pennywise_regex.json"
DEFAULT_OUT = ROOT / "raw_data" / "synth_msg_5k.ndjson"

Compiled = list[tuple[dict, re.Pattern[str]]]


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
            # skip money captures so last4 is not "found" inside 16781.73
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
    labels = {
        "txn_type": tmpl.txn_type,
        "amount": slots["amount"],
        "account": f"*{slots['last4']}",
        "last4": slots["last4"],
        "merchant": slots["merchant"],
        "reference": ref,
        "balance": slots["balance"],
        "date": slots["date_dmy"],
    }
    if not labels_ok(labels, hits, tmpl.required):
        return None
    return {
        "bank": tmpl.bank,
        "country": tmpl.country,
        "currency": tmpl.currency,
        "source": "synthetic",
        "template": tmpl.key,
        "address": f"{rng.choice(PREFIXES)}-{tmpl.sender_core}",
        "body": body,
        "labels": labels,
        "regex_hits": hits,
    }


def try_until(rng: random.Random, tmpl: Template, compiled: Compiled, retries: int) -> tuple[dict | None, int]:
    for i in range(1, retries + 1):
        rec = generate_one(rng, tmpl, compiled)
        if rec is not None:
            return rec, i
    return None, retries


def smoke_templates(rng: random.Random, compiled_by_bank: dict[str, Compiled], retries: int) -> None:
    for tmpl in TEMPLATES:
        rec, _ = try_until(rng, tmpl, compiled_by_bank[tmpl.bank], retries)
        if rec is None:
            raise SystemExit(f"template {tmpl.key} failed smoke ({retries} tries)")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate synthetic bank SMS dataset")
    p.add_argument("--n", type=int, default=5000, help="accepted rows to write")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--retries", type=int, default=12, help="slot retries per row")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    p.add_argument("--skip-smoke", action="store_true", help="do not preflight every template")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if args.n < 1:
        raise SystemExit("--n must be >= 1")
    rng = random.Random(args.seed)
    needed = {t.bank for t in TEMPLATES}
    all_regexes = load_bank_regexes()
    compiled_by_bank: dict[str, Compiled] = {}
    for bank in sorted(needed):
        if bank not in all_regexes:
            raise SystemExit(f"no Pennywise regexes for {bank}")
        compiled_by_bank[bank] = compile_bank(all_regexes[bank])
        if not compiled_by_bank[bank]:
            raise SystemExit(f"no usable extract regexes for {bank}")

    if not args.skip_smoke:
        smoke_templates(random.Random(args.seed), compiled_by_bank, args.retries)
        print(f"smoke ok  {len(TEMPLATES)} templates")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    counts = Counter()
    rejected = 0
    written = 0

    with args.out.open("w") as f:
        while written < args.n:
            tmpl = TEMPLATES[written % len(TEMPLATES)]
            rec, used = try_until(rng, tmpl, compiled_by_bank[tmpl.bank], args.retries)
            rejected += used - 1 if rec else used
            if rec is None:
                raise SystemExit(f"template {tmpl.key} never passed regex gate")
            rec["id"] = f"synth_{written + 1:05d}"
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            counts[tmpl.key] += 1
            written += 1
            if written % 500 == 0 or written == args.n:
                print(f"wrote {written}/{args.n}  rejected={rejected}")

    by_country: Counter[str] = Counter()
    for tmpl in TEMPLATES:
        by_country[tmpl.country] += counts[tmpl.key]
    print(f"done {written} rows -> {args.out}")
    print("by country:", json.dumps(dict(by_country), indent=2))
    print("by template:", json.dumps(dict(counts), indent=2))


if __name__ == "__main__":
    main()
