# Initial source audit — banking-sector pension transfer

This note records only source-backed facts used to design the research pipeline. It is not a conclusion on whether the transaction was economically harmful or beneficial.

## Acquisition status

Retrieval date: 2026-08-19.

The initial acquisition pass now stores and hashes official PDFs for the core sources in `evidence/source_registry.csv`. Diário da República legal acts are stored as full issue PDFs from `files.diariodarepublica.pt`, because direct act-page downloads from `diariodarepublica.pt` returned JavaScript shell HTML rather than citable raw text. Those failed captures were removed and are not registered as acquired evidence.

Acquired source files:

- `data/raw/legislation/DR_DL54_2009_issue.pdf`
- `data/raw/legislation/DR_DL1A_2011_issue.pdf`
- `data/raw/legislation/DR_DL127_2011_issue.pdf`
- `data/raw/legislation/DR_DL88_2012_issue.pdf`
- `data/raw/cge/DGO_CGE_2011_vol1.pdf`
- `data/raw/european_accounts/EC_EXPOST_PAEF_ip040_en.pdf`

The validation gate now checks that every source marked `acquired` has a relative raw path, a 64-character SHA-256 hash, an existing file, and matching bytes.

## Decree-Law 54/2009

Primary source: Diário da República.

The decree required workers hired by banking institutions after its entry into force to be covered by the general Social Security regime, while preserving the substitute regime for workers hired before that date where applicable.

Source registry ID: `DR_DL54_2009`.

## Decree-Law 1-A/2011

Primary source: Diário da República.

The decree integrated active banking-sector workers covered by the substitute regime into the general Social Security regime for specified contingencies and extinguished CAFEB by integration into the Instituto da Segurança Social.

Source registry ID: `DR_DL1A_2011`.

## Decree-Law 127/2011

Primary source: Diário da República.

The decree:

- assigned Social Security responsibility for specified pensions already in payment at 31 December 2011;
- transferred to the State ownership of the portion of pension-fund assets associated with those liabilities;
- made the State responsible for financing the pensions and administrative costs through a specific transfer to Social Security;
- required transferred assets to equal the actuarial value of assumed responsibilities under the prescribed valuation method;
- prescribed a 4% discount rate and specified mortality tables;
- allowed up to 50% of transferred assets to be Portuguese public debt securities valued at market prices;
- required at least 55% of provisional liabilities to be transferred by 31 December 2011, with later completion and final adjustment;
- extinguished definitively and irreversibly the covered responsibilities of participating credit institutions after the transfer;
- retained specified updates, complements, SAMS contributions and certain survivor benefits with the banks/funds.

Source registry ID: `DR_DL127_2011`.

## European Commission ex-post evaluation

Official evaluation of Portugal's 2011-2014 adjustment programme.

The evaluation reports that:

- the 2011 transfer of banks' pension funds to the State improved the headline deficit under ESA-95 by about 3.5% of GDP;
- under ESA-2010 the operation is treated as a financial transaction with no direct deficit impact;
- transferred banking-sector pensions added about EUR 0.5 billion of pension expenditure in 2012;
- Social Security contribution revenue also benefited from the inclusion of banking employees in the general scheme.

These are published benchmarks to reproduce from primary national accounts and Social Security accounts, not values to copy directly into the manuscript.

Source registry ID: `EC_EXPOST_PAEF`.
