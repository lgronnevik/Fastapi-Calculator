from operations import CalculationFactory
import pytest

# ...existing tests...

def test_factory_returns_correct_operation():
    assert CalculationFactory.get_operation("Add").compute(2, 3) == 5
    assert CalculationFactory.get_operation("Sub").compute(5, 2) == 3
    assert CalculationFactory.get_operation("Multiply").compute(3, 4) == 12
    assert CalculationFactory.get_operation("Divide").compute(8, 2) == 4

def test_factory_invalid_type():
    with pytest.raises(ValueError):
        CalculationFactory.get_operation("Modulo")