# Article Evidence

This file summarizes the bounded article-evidence gate in `evidence/article_evidence.csv`.

## Ready For Bounded Use

- `BANK_FISCAL_001`: ESA-95 3.5 percent GDP treatment is reconciled from CGE and EC sources.
- `BANK_FISCAL_002`: ESA-2010 no-direct-deficit-impact classification is confirmed from the EC source.
- `BANK_COST_001`: the EC roughly EUR 0.5bn statement is reconciled to the official EUR 516.0m 2012 account value.
- `CGA_CGE_2011_001`: CGA 2011 balance decomposition is extracted and checked within rounding.
- `BANK_AL_2011_001` and `BANK_AL_2011_002`: aggregate 2011 bank-transfer amounts are extracted, with bank-level interpretation blocked.
- `BPN_2012_002`: DL88 BPN transfer amount is extracted and reconciled to the rounded official account value.

## Gate

The article must not treat bounded rows as complete lifecycle or causal findings. Rows marked `bounded_only` can support caveated discussion only. Any future material claim with status `to_replicate`, `unresolved`, missing source IDs, missing transformation, missing processed dataset or missing output artifact must block article generation.
