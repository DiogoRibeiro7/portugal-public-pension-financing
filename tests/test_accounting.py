from portugal_pensions.accounting import reconcile_financing_identity


def test_financing_identity_reconciles() -> None:
    result = reconcile_financing_identity(
        employee_contributions=100.0,
        employer_contributions=50.0,
        state_transfers=30.0,
        other_financing=20.0,
        pension_expenditure=180.0,
        administrative_expenditure=10.0,
        other_expenditure=0.0,
        change_in_financial_position=10.0,
        tolerance=0.0,
    )
    assert result.reconciled
    assert result.residual == 0.0


def test_financing_identity_keeps_residual_uninterpreted() -> None:
    result = reconcile_financing_identity(
        employee_contributions=100.0,
        employer_contributions=0.0,
        state_transfers=0.0,
        other_financing=0.0,
        pension_expenditure=90.0,
        administrative_expenditure=0.0,
        other_expenditure=0.0,
        change_in_financial_position=0.0,
        tolerance=1.0,
    )
    assert not result.reconciled
    assert result.residual == 10.0
