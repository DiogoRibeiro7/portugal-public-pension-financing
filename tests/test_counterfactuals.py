import pytest

from portugal_pensions.counterfactuals import compound_reserve, funding_substitution


def test_compound_reserve() -> None:
    path = compound_reserve([100.0, 100.0], [0.10, 0.10])
    assert path == pytest.approx([110.0, 231.0])


def test_funding_substitution_does_not_create_extra_cash() -> None:
    employer, state = funding_substitution(100.0, 40.0)
    assert employer + state == pytest.approx(100.0)
