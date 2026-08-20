# Pension Flow-of-Funds Matrix

`data/processed/pension_flow_of_funds_long.csv` records the currently supported cross-entity pension-financing rows.

The matrix is long-form rather than a wide annual table because the registered evidence is still uneven across institutions. Each row identifies the paying entity, receiving entity, transaction type, accounting basis, stock/flow category and whether the row disappears under general-government consolidation.

## Bridge Use

Rows with a `bridge_definition_id` other than `not_applicable` are selectable components for balance calculations. The current checked bridges are:

- `cga_2011_balance_decomposition`: reported CGA global balance, PT pension-fund effect and CGA balance excluding that effect.
- `bank_2011_recorded_asset_receipt`: 2011 credit-institution pension-fund asset receipt recorded in the State accounts.
- `bank_2011_total_transfer_value`: aggregate 2011 banking pension-fund transfer value, kept separate from the recorded receipt.
- `bank_2012_cash_identity`: State Budget financing to Social Security and matching pension payments to households.
- `bank_2012_financing_split`: State Budget and CGA BPN-related financing components.
- `bpn_2012_legal_transfer`: DL88 BPN asset transfer to CGA.
- `bpn_2012_account_extract`: BPN pensions paid by the CGA fund in 2012.

## Current Limits

The matrix is not a complete system-wide annual account. RGSS/previdential balances, FEFSS annual cash flows, detailed CGA component flows and bank-level transfer schedules remain open data-quality gaps. Rows with blocked statuses mark those gaps explicitly and must not be interpreted as zero-valued transactions.
