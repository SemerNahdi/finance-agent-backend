from typing import Dict, Union
from decimal import Decimal, ROUND_HALF_UP


class CalculatorTool:
    """A tool for financial calculations like ROI, compound interest, and investment simulations."""

    @staticmethod
    def calculate_roi(initial_investment: float, final_value: float) -> float:
        """Calculate Return on Investment (ROI) as a percentage.

        Args:
            initial_investment: Initial amount invested.
            final_value: Final value of the investment.

        Returns:
            ROI as a percentage, rounded to 2 decimal places.

        Raises:
            ValueError: If initial_investment is zero or negative, or final_value is negative.
        """
        if initial_investment <= 0:
            raise ValueError("Initial investment must be positive")
        if final_value < 0:
            raise ValueError("Final value cannot be negative")
        roi = (final_value - initial_investment) / initial_investment * 100
        return float(
            Decimal(str(roi)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        )

    @staticmethod
    def compound_interest(
        principal: float, rate: float, years: int, n: int = 1
    ) -> float:
        """Calculate compound interest.

        Formula: A = P(1 + r/n)^(n*t)

        Args:
            principal: Initial investment amount.
            rate: Annual interest rate (as decimal, e.g., 0.05 for 5%).
            years: Number of years.
            n: Compounding frequency per year (default 1 for annual).

        Returns:
            Final amount, rounded to 2 decimal places.

        Raises:
            ValueError: If principal, rate, years, or n are invalid.
        """
        if principal <= 0:
            raise ValueError("Principal must be positive")
        if rate < 0:
            raise ValueError("Interest rate cannot be negative")
        if years < 0:
            raise ValueError("Years cannot be negative")
        if n <= 0:
            raise ValueError("Compounding frequency must be positive")
        if years == 0:
            return float(
                Decimal(str(principal)).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            )

        amount = principal * (1 + rate / n) ** (n * years)
        return float(
            Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        )

    @staticmethod
    def investment_simulation(
        principal: float, rate: float, years: int, n: int = 1
    ) -> Dict[int, float]:
        """Simulate investment growth over time.

        Args:
            principal: Initial investment amount.
            rate: Annual interest rate (as decimal, e.g., 0.05 for 5%).
            years: Number of years.
            n: Compounding frequency per year (default 1 for annual).

        Returns:
            Dictionary mapping year to investment value, rounded to 2 decimal places.

        Raises:
            ValueError: If principal, rate, years, or n are invalid.
        """
        if principal <= 0:
            raise ValueError("Principal must be positive")
        if rate < 0:
            raise ValueError("Interest rate cannot be negative")
        if years < 0:
            raise ValueError("Years cannot be negative")
        if n <= 0:
            raise ValueError("Compounding frequency must be positive")

        result = {}
        for year in range(years + 1):
            amount = (
                principal if year == 0 else principal * (1 + rate / n) ** (n * year)
            )
            result[year] = float(
                Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            )
        return result

    @staticmethod
    def simple_interest(principal: float, rate: float, years: int) -> float:
        """Calculate simple interest.

        Formula: A = P(1 + r*t)

        Args:
            principal: Initial investment amount.
            rate: Annual interest rate (as decimal, e.g., 0.05 for 5%).
            years: Number of years.

        Returns:
            Final amount, rounded to 2 decimal places.

        Raises:
            ValueError: If principal, rate, or years are invalid.
        """
        if principal <= 0:
            raise ValueError("Principal must be positive")
        if rate < 0:
            raise ValueError("Interest rate cannot be negative")
        if years < 0:
            raise ValueError("Years cannot be negative")
        if years == 0:
            return float(
                Decimal(str(principal)).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            )

        amount = principal * (1 + rate * years)
        return float(
            Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        )


# Test functions
if __name__ == "__main__":
    calc = CalculatorTool()
    try:
        print("ROI:", calc.calculate_roi(1000, 1200))
        print(
            "Compound Interest (3 years, annual):",
            calc.compound_interest(1000, 0.05, 3),
        )
        print(
            "Compound Interest (3 years, monthly):",
            calc.compound_interest(1000, 0.05, 3, n=12),
        )
        print("Simple Interest:", calc.simple_interest(1000, 0.05, 3))
        print("Simulation:", calc.investment_simulation(1000, 0.05, 5))
    except ValueError as e:
        print(f"Error: {e}")
