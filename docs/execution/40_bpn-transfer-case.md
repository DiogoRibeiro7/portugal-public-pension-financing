# Analyze BPN transfer

Instruction file: `prompts/40_bpn_2012_separate_case.md`
Date: 2026-08-19
Status: `partial_bounded_reconstruction`

## Actions

- Read the instruction file together with the master research guardrails.
- Checked the current repository architecture, registries, tests, and validation commands.
- Extracted Decree-Law 88/2012 to text for line-level reconstruction of the BPN-specific legal path.
- Replaced the placeholder `data/processed/bpn_2012_pension_transfer.csv` with a long-form separate-case ledger.
- Added validation for required BPN measures, legal amounts, Tribunal de Contas account extracts, and exclusion from the main 2011 DL127 panel.
- Recorded the panel boundary in the claim registry, reconciliation log, and data-quality registry.
- Preserved existing validated outputs.
- Did not invent historical values, legal provisions, pension populations, actuarial cash flows, accounting classifications, or source URLs.

## Result

Decree-Law 88/2012 is now represented as a separate 2012 BPN case. Unlike the 2011 DL127 private-bank transfer, the covered BPN responsibilities are assigned to CGA, with ISS/CNP paying values communicated by CGA. DL88 required EUR 96.768004m to be transferred from the BPN pension fund to CGA and EUR 7.319430m to be returned to the entities for retained SAMS contribution responsibilities.

Tribunal de Contas 2012 account extracts record 11 BPN retirees, 18 survivor-pension beneficiaries, EUR 0.17927m in BPN fund pension and benefit payments, and a rounded EUR 96.8m BPN reserve constitution value.

## Current Stop Condition

The BPN case remains bounded because the registered evidence does not provide the full actuarial valuation, cash versus public-debt-security mix, bank-level worker population, monthly payment path, or post-2012 fund drawdown. The main 2011 bank-transfer estimates must not include BPN values unless a broader perimeter is explicitly defined.

## Validation

This branch ran `make quality` after regenerating `MANIFEST.sha256`.
