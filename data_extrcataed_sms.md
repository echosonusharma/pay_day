# Structured data to be extracted from the SMS

> we will build outputs for json & custom condensed format (lesser tokens = faster inference)

- as json

```json
  {
    "amount": null,
    "currency": null,
    "direction": null,
    "txn_kind": null,
    "expense_type": null,
    "status": null,
    "account_last4": null,
    "instrument": null,
    "counterparty": null,
    "reference": null,
    "balance": null,
    "txn_date": null
  }
```

- as condensed text format

```shell
amt:null
cur:null
dir:null
kind:null
exp:null
stat:null
acct:null
inst:null
cp:null
ref:null
bal:null
date:null
```

┌────────────┬──────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────┐
│ Field      │ From the text                        │ Example                                                                 │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ amount     │ the money moved                      │ "512.75"                                                                │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ currency   │ Rs / INR / AED / $                   │ "INR"                                                                   │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ direction  │ sent / debited / credited / spent    │ "debit" | "credit"                                                      │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ txn_kind   │ how it moved                         │ "upi" | "card" | "atm" | "neft" | "imps" | "wallet" | "transfer" |      │
│            │                                      │ "other"                                                                 │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ expense_ty │ usually not in SMS — you guess from  │ "food" | "travel" | "shopping" | "bills" | "fuel" | "transfer" |        │
│ pe         │ merchant                             │ "income" | "unknown"                                                    │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ status     │ posted vs failed / OTP               │ "posted" | "failed" | "otp" | "info"                                    │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ account_la │ *7391 / XX4412                       │ "7391"                                                                  │
│ st4        │                                      │                                                                         │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ instrument │ A/c vs card vs wallet                │ "account" | "card" | "wallet"                                           │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ counterpar │ who / where                          │ "Sharma Sweets Corner"                                                  │
│ ty         │                                      │                                                                         │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ reference  │ RRN / UPI / TxnId                    │ "738291450628"                                                          │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ balance    │ Avl Bal / limit                      │ "18420.50"                                                              │
├────────────┼──────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ txn_date   │ date inside the SMS                  │ "2026-08-18"                                                            │
└────────────┴──────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────┘

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
    "counterparty": "Sharma Sweets Corner",
    "reference": "738291450628",
    "balance": "18420.50",
    "txn_date": "2026-08-18"
  }
```

## system prompt

User message is only the SMS body. Model replies with one JSON object, nothing else.

You extract structured data from a single bank/wallet SMS body. You have only the message text — no sender, no metadata.
Return ONE JSON object and nothing else (no markdown, no comments). Use this exact schema:

```json
{
    "amount": string | null,
    "currency": string | null,
    "direction": "debit" | "credit" | null,
    "txn_kind": "upi" | "card" | "atm" | "neft" | "imps" | "wallet" | "transfer" | "other" | null,
    "expense_type": "food" | "groceries" | "travel" | "fuel" | "shopping" | "bills" | "entertainment" | "health" | "transfer" | "income" | "cash" | "unknown" | null,
    "status": "posted" | "failed" | "otp" | "info" | null,
    "account_last4": string | null,
    "instrument": "account" | "card" | "wallet" | null,
    "counterparty": string | null,
    "reference": string | null,
    "balance": string | null,
    "txn_date": string | null
}
```

<rules>
- If a field is not clearly in the text, use null. Do not invent account numbers, refs, or amounts.
- amount / balance: digits only, with a decimal point if present (e.g. "512.75", "18420.50"). Strip currency words, commas, and
symbols (Rs, INR, ₹, $, AED, Ksh, Tk).
- currency: ISO-4217 when you can infer it from the text (INR, USD, AED, SAR, ETB, TZS, NGN, NPR, EGP, KES, BDT, OMR, PKR, LKR,
EUR, TRY, RUB, CZK, MZN). If only "Rs"/"₹" → INR. If only "$" → USD. If unknown → null.
- direction: debit = spent, sent, withdrawn, paid, Dr, purchase. credit = credited, received, deposited, refund, Cr, salary.
OTP / failed / marketing → direction null unless money clearly moved.
- txn_kind: pick the most specific channel in the text (UPI/VPA/RRN-UPI → upi; card/POS/spent on card → card; ATM/withdrawn at
ATM → atm; NEFT/RTGS → neft; IMPS → imps; M-PESA/bKash/Tigo/Opay/wallet → wallet). Else transfer or other.
- expense_type is NOT usually written in the SMS. Infer loosely from counterparty (Sweets/Cafe/Zomato → food; fuel/petrol →
fuel; Amazon/Flipkart → shopping; electricity/recharge → bills; person-to-person or “to Rahul” → transfer; credited salary/from
employer → income; ATM → cash). If unsure → "unknown". Never invent a category that contradicts a credit/income message.
- status: posted if the txn succeeded; failed if declined/not completed/could not; otp if the SMS is only an OTP; info for
balance/limit/marketing with no txn.
- account_last4: last 4 digits of A/c, card, or wallet mask (*7391, XX4412, ending 4412). Digits only, length 4. Not part of
the amount or phone number.
- instrument: A/c or account → account; card/credit card/debit card → card; wallet/M-PESA/bKash → wallet.
- counterparty: merchant, payee, or payer name as in the text. Strip trailing bank boilerplate (Not you, SMS BLOCK, Avl Bal…).
Not the bank name unless it is the other party. null if none.
- reference: a single best id (RRN, UPI ref, TxnId, IMPS, TrxID). Digits/letters only, no label. If several, prefer RRN then
UPI then TxnId.
- txn_date: date stated in the SMS, ISO "YYYY-MM-DD". 2-digit years 24–26 → 2024–2026. If no date in the body → null. Do not
use “today”.
- Ignore phishing footers, BLOCK numbers, and URLs unless they are the counterparty.
</rules>

<user_message>
Sent Rs.512.75 from A/c *7391 on 18-08-26 to Sharma Sweets Corner.RRN 738291450628.Avl Bal Rs.18420.50.Not you?SMS BLOCK to
9444412345-Indian Bank
</user_message>

---

in compressed text format

```shell
amt: str|nl
cur: str|nl
dir: d|c|nl
kind: u|cd|a|n|i|w|t|o|nl
exp: f|g|tr|fu|s|b|e|h|t|in|ca|x|nl
stat: p|f|otp|i|nl
acct: str|nl
inst: a|c|w|nl
cp: str|nl
ref: str|nl
bal: str|nl
date: str|nl
```

- where

```shell
dir:    d=debit c=credit
kind:   u=upi cd=card a=atm n=neft i=imps w=wallet t=transfer o=other
exp:    f=food g=groceries tr=travel fu=fuel s=shopping b=bills
        e=entertainment h=health t=transfer in=income ca=cash x=unknown
stat:   p=posted f=failed otp=otp i=info
inst:   a=account c=card w=wallet
```

and nl=null

> we can have a parser that translate this back to json.

---

## Test model performance

- Benchmarks, Evaluations ...etc
- Data set - improvements
- quantization or how can we improve the model performance
- more output compression for fewer output tokens
- test on a bigger data set - see how it performs and find failure cases
