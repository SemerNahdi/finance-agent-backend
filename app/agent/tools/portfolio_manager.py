from typing import Dict
from decimal import Decimal, ROUND_HALF_UP
from app.agent.memory import load_memory, save_memory


class PortfolioManager:
    """Manages user portfolios, including adding, removing, and fetching assets."""

    @staticmethod
    def add_asset(
        user_id: str, asset_name: str, quantity: float, purchase_price: float
    ) -> Dict:
        """Add an asset to the user's portfolio or update its quantity.

        Args:
            user_id: Unique identifier for the user.
            asset_name: Name of the asset (e.g., 'BTC', 'ETH').
            quantity: Quantity of the asset to add.
            purchase_price: Price at which the asset was purchased.

        Returns:
            Updated portfolio dictionary.

        Raises:
            ValueError: If user_id, asset_name, quantity, or purchase_price is invalid.
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")
        if not asset_name or not isinstance(asset_name, str):
            raise ValueError("Asset name must be a non-empty string")
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if purchase_price < 0:
            raise ValueError("Purchase price cannot be negative")

        memory = load_memory(user_id)
        portfolio = memory.get("portfolio", {})

        if asset_name in portfolio:
            # Update quantity and maintain a list of purchase prices for accurate ROI
            portfolio[asset_name]["quantity"] += float(
                Decimal(str(quantity)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            )
            portfolio[asset_name]["purchase_prices"].append(
                {
                    "quantity": quantity,
                    "price": float(
                        Decimal(str(purchase_price)).quantize(
                            Decimal("0.01"), rounding=ROUND_HALF_UP
                        )
                    ),
                }
            )
        else:
            portfolio[asset_name] = {
                "quantity": float(
                    Decimal(str(quantity)).quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    )
                ),
                "purchase_prices": [
                    {
                        "quantity": quantity,
                        "price": float(
                            Decimal(str(purchase_price)).quantize(
                                Decimal("0.01"), rounding=ROUND_HALF_UP
                            )
                        ),
                    }
                ],
                "current_price": None,  # To be updated separately (e.g., via API)
            }

        memory["portfolio"] = portfolio
        save_memory(user_id, memory)
        return portfolio

    @staticmethod
    def remove_asset(user_id: str, asset_name: str) -> Dict:
        """Remove an asset from the user's portfolio.

        Args:
            user_id: Unique identifier for the user.
            asset_name: Name of the asset to remove.

        Returns:
            Updated portfolio dictionary.

        Raises:
            ValueError: If user_id or asset_name is invalid.
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")
        if not asset_name or not isinstance(asset_name, str):
            raise ValueError("Asset name must be a non-empty string")

        memory = load_memory(user_id)
        portfolio = memory.get("portfolio", {})

        if asset_name in portfolio:
            del portfolio[asset_name]
            memory["portfolio"] = portfolio
            save_memory(user_id, memory)

        return portfolio

    @staticmethod
    def get_portfolio(user_id: str) -> Dict:
        """Retrieve the user's portfolio.

        Args:
            user_id: Unique identifier for the user.

        Returns:
            Portfolio dictionary.

        Raises:
            ValueError: If user_id is invalid.
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")

        memory = load_memory(user_id)
        return memory.get("portfolio", {})

    @staticmethod
    def update_current_price(
        user_id: str, asset_name: str, current_price: float
    ) -> Dict:
        """Update the current price of an asset in the portfolio.

        Args:
            user_id: Unique identifier for the user.
            asset_name: Name of the asset.
            current_price: Current market price of the asset.

        Returns:
            Updated portfolio dictionary.

        Raises:
            ValueError: If user_id, asset_name, or current_price is invalid.
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")
        if not asset_name or not isinstance(asset_name, str):
            raise ValueError("Asset name must be a non-empty string")
        if current_price < 0:
            raise ValueError("Current price cannot be negative")

        memory = load_memory(user_id)
        portfolio = memory.get("portfolio", {})

        if asset_name in portfolio:
            portfolio[asset_name]["current_price"] = float(
                Decimal(str(current_price)).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            )
            memory["portfolio"] = portfolio
            save_memory(user_id, memory)

        return portfolio


# Test functions
if __name__ == "__main__":
    try:
        uid = "test_user"
        print("Adding BTC...")
        print(PortfolioManager.add_asset(uid, "BTC", 2, 30000))
        print("Adding ETH...")
        print(PortfolioManager.add_asset(uid, "ETH", 5, 2000))
        print("Updating BTC price...")
        print(PortfolioManager.update_current_price(uid, "BTC", 32000))
        print("Fetching portfolio...")
        print(PortfolioManager.get_portfolio(uid))
        print("Removing BTC...")
        print(PortfolioManager.remove_asset(uid, "BTC"))
        print("Final portfolio...")
        print(PortfolioManager.get_portfolio(uid))
    except ValueError as e:
        print(f"Error: {e}")
