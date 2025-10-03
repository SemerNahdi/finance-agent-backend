import pytest

from app.agent.tools.calculator import CalculatorTool

# from app.agent.tools.calculator import CalculatorTool

calc = CalculatorTool()


def test_calculate_roi():
    assert calc.calculate_roi(1000, 1200) == 20.0
    assert calc.calculate_roi(1000, 1000) == 0.0
    assert calc.calculate_roi(1000, 800) == -20.0
    with pytest.raises(ValueError, match="Initial investment must be positive"):
        calc.calculate_roi(0, 1200)
    with pytest.raises(ValueError, match="Final value cannot be negative"):
        calc.calculate_roi(1000, -100)


def test_compound_interest():
    assert calc.compound_interest(1000, 0.05, 3) == 1157.63
    assert calc.compound_interest(1000, 0.05, 0) == 1000.0
    assert calc.compound_interest(1000, 0.05, 1, n=12) == pytest.approx(1051.16, 0.01)
    with pytest.raises(ValueError, match="Principal must be positive"):
        calc.compound_interest(-1000, 0.05, 3)
    with pytest.raises(ValueError, match="Compounding frequency must be positive"):
        calc.compound_interest(1000, 0.05, 3, n=0)


def test_investment_simulation():
    result = calc.investment_simulation(1000, 0.05, 2)
    assert result == {0: 1000.0, 1: 1050.0, 2: 1102.5}
    assert len(calc.investment_simulation(1000, 0.05, 5)) == 6  # Includes year 0
    with pytest.raises(ValueError, match="Years cannot be negative"):
        calc.investment_simulation(1000, 0.05, -1)


def test_simple_interest():
    assert calc.simple_interest(1000, 0.05, 3) == 1150.0
    assert calc.simple_interest(1000, 0.05, 0) == 1000.0
    with pytest.raises(ValueError, match="Interest rate cannot be negative"):
        calc.simple_interest(1000, -0.05, 3)
