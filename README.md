# PAY DAY

Idea is to process sms msgs and extracting all financial data in a structured format using a custom trained model.

- data set is synthetic data + my own msgs(data altered)
- try diff output formats
- try diff models

> for process raw data

## Synthetic SMS dataset

Templates + random slots (no LLM), then keep a row only if Pennywise regexes extract the gold fields.

```bash
uv run python generate_synth.py --n 5000 --out raw_data/synth_msg_5k.ndjson
```


## Things used

- [sms-export](https://f-droid.org/en/packages/com.github.tmo1.sms_ie/) extract local msg to for data seed.
- [pennywiseai-tracker](https://github.com/sarim2000/pennywiseai-tracker) a tracker app the same using regex.
