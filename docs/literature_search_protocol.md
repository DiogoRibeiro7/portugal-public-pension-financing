# Literature Search Protocol

Status: `partial_bounded_reconstruction`

Search date: 2026-08-21

Output map: `evidence/literature_map.csv`

## Scope

The bounded search covered:

- Portuguese pension financing and expenditure determinants.
- CGA history, closure, financial analysis, and public-employee pension reform.
- Pay-as-you-go versus funded pension accounting.
- Government assumption of private pension liabilities and bank pension transfers.
- ESA95/ESA2010 pension-transfer accounting.
- Actuarial and national-accounts treatment of pension liabilities.

## Search Sources

Searches used web-indexed scholarly and institutional sources, including Banco
de Portugal, OECD, RePEc/IDEAS, SSRN, Public Sector Economics metadata, European
Commission, ECB, Banco de Portugal statistical releases, CFP, and repository
PDFs surfaced by web search.

Each included row in `evidence/literature_map.csv` records:

- source category;
- topic;
- research question;
- method;
- data period and data source;
- main finding;
- relation to this project;
- inclusion decision;
- search database or channel;
- search query;
- search date;
- source URL.

## Inclusion Rules

Rows are marked `included_nearest_neighbor` when the work is a close academic
neighbour by question, method, or institutional object. Rows are marked
`included_context` when they supply institutional, accounting, or technical
context but should not be used as academic novelty evidence.

Legal and institutional sources are deliberately separated from academic
literature through the `source_category` field. Official reports may support
definitions, accounting treatment, source selection, or institutional facts;
they do not by themselves establish the academic contribution.

## Novelty Rule

The bounded search supports only a cautious contribution statement:

> Existing close work covers CGA reform simulations, long-run public-pension
> expenditure projections, macro determinants of pension expenditure, CGA
> financial description, financialisation context, and ESA/national-accounts
> treatment. This project adds a reproducible financing-flow reconstruction
> that separates CGA, RGSS, Social Security, State-transfer, bank-transfer,
> legal-remittance, employer-gap, actuarial-stock, and ESA-perimeter concepts.

This is evidence of absence within the recorded bounded search, not proof that
no prior paper exists.
