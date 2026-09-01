"""
Condensed <-> JSON converter.
"""

from __future__ import annotations

# Enum maps
DIR_TO_CODE = {"debit": "d", "credit": "c"}
CODE_TO_DIR = {v: k for k, v in DIR_TO_CODE.items()}

KIND_TO_CODE = {
    "upi": "u",
    "card": "cd",
    "atm": "a",
    "neft": "n",
    "imps": "i",
    "wallet": "w",
    "transfer": "t",
    "other": "o",
}
CODE_TO_KIND = {v: k for k, v in KIND_TO_CODE.items()}

EXP_TO_CODE = {
    "food": "f",
    "groceries": "g",
    "travel": "tr",
    "fuel": "fu",
    "shopping": "s",
    "bills": "b",
    "entertainment": "e",
    "health": "h",
    "transfer": "t",
    "income": "in",
    "cash": "ca",
    "unknown": "x",
}
CODE_TO_EXP = {v: k for k, v in EXP_TO_CODE.items()}

STAT_TO_CODE = {"posted": "p", "failed": "f", "otp": "otp", "info": "i"}
CODE_TO_STAT = {v: k for k, v in STAT_TO_CODE.items()}

INST_TO_CODE = {"account": "a", "card": "c", "wallet": "w"}
CODE_TO_INST = {v: k for k, v in INST_TO_CODE.items()}

ORDERED_KEYS = ["amt", "cur", "dir", "kind", "exp", "stat", "acct", "inst", "cp", "ref", "bal", "date"]
JSON_KEYS = ["amount", "currency", "direction", "txn_kind", "expense_type", "status", "account_last4", "instrument", "counterparty", "reference", "balance", "txn_date"]
KEY_MAP = dict(zip(ORDERED_KEYS, JSON_KEYS))
INV_KEY_MAP = {v: k for k, v in KEY_MAP.items()}


def _escape(s: str) -> str:
    # order matters: \ first, then \n, then :
    s = s.replace("\\", "\\\\")
    s = s.replace("\n", "\\n")
    s = s.replace(":", "\\:")
    return s

def _unescape(s: str) -> str:
    res = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt == "\\":
                res.append("\\")
                i += 2
            elif nxt == ":":
                res.append(":")
                i += 2
            elif nxt == "n":
                res.append("\n")
                i += 2
            else:
                # unknown escape, keep as is (e.g. \x -> x)
                res.append(nxt)
                i += 2
        else:
            res.append(s[i])
            i += 1
    return "".join(res)

def json_to_condensed(data: dict) -> str:
    """Convert canonical JSON (12 fields) to condensed 12-line string.

    Null fields are encoded as empty string after colon, e.g. "amt:".
    Raises ValueError on invalid enum / missing keys.
    """
    for k in JSON_KEYS:
        if k not in data:
            raise ValueError(f"missing key {k}")

    def enc_str(v):
        return "" if v is None else _escape(str(v))

    def enc_enum(v, mapping):
        if v is None:
            return ""
        if v not in mapping:
            raise ValueError(f"invalid enum value {v!r} not in {mapping}")
        return mapping[v]

    lines = [
        f"amt:{enc_str(data['amount'])}",
        f"cur:{enc_str(data['currency'])}",
        f"dir:{enc_enum(data['direction'], DIR_TO_CODE)}",
        f"kind:{enc_enum(data['txn_kind'], KIND_TO_CODE)}",
        f"exp:{enc_enum(data['expense_type'], EXP_TO_CODE)}",
        f"stat:{enc_enum(data['status'], STAT_TO_CODE)}",
        f"acct:{enc_str(data['account_last4'])}",
        f"inst:{enc_enum(data['instrument'], INST_TO_CODE)}",
        f"cp:{enc_str(data['counterparty'])}",
        f"ref:{enc_str(data['reference'])}",
        f"bal:{enc_str(data['balance'])}",
        f"date:{enc_str(data['txn_date'])}",
    ]
    return "\n".join(lines)

def condensed_to_json(text: str) -> dict:
    """Parse condensed 12-line string to canonical JSON.

    Raises ValueError on invalid format, line count, key order, enum code.
    """
    lines = text.split("\n")
    # allow trailing newline? strip empty trailing
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if len(lines) != 12:
        raise ValueError(f"expected 12 lines, got {len(lines)}: {lines!r}")

    def dec_str(v: str):
        if v == "" or v == "nl":
            return None
        return _unescape(v)

    def dec_enum(v: str, rev_map: dict, field: str):
        if v == "" or v == "nl":
            return None
        if v not in rev_map:
            raise ValueError(f"invalid code {v!r} for {field}")
        return rev_map[v]

    # validate order and parse
    result = {}
    for idx, line in enumerate(lines):
        expected_key = ORDERED_KEYS[idx]
        # first colon is separator (key never contains : or \)
        if ":" not in line:
            raise ValueError(f"line {idx+1} missing ':' : {line!r}")
        k, raw = line.split(":", 1)
        if k != expected_key:
            raise ValueError(f"line {idx+1} expected key {expected_key!r} got {k!r}")
        json_key = KEY_MAP[k]
        if k in ("dir", "kind", "exp", "stat", "inst"):
            # enum
            rev = {
                "dir": CODE_TO_DIR,
                "kind": CODE_TO_KIND,
                "exp": CODE_TO_EXP,
                "stat": CODE_TO_STAT,
                "inst": CODE_TO_INST,
            }[k]
            result[json_key] = dec_enum(raw, rev, k)
        else:
            result[json_key] = dec_str(raw)

    return result

def roundtrip_ok(data: dict) -> bool:
    return data == condensed_to_json(json_to_condensed(data))
