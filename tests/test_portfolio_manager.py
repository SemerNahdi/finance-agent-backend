import pytest
import os
from app.agent.tools.portfolio_manager import PortfolioManager
from app.agent.memory import MEMORY_FILE


@pytest.fixture(autouse=True)
def setup_memory():
    """Clear memory file before and after each test."""
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    yield
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)


def test_add_asset():
    portfolio = PortfolioManager.add_asset("user1", "BTC", 2, 30000)
    assert portfolio == {
        "BTC": {
            "quantity": 2.0,
            "purchase_prices": [{"quantity": 2, "price": 30000.0}],
            "current_price": None,
        }
    }
    # Add more of the same asset
    portfolio = PortfolioManager.add_asset("user1", "BTC", 3, 31000)
    assert portfolio["BTC"]["quantity"] == 5.0
    assert len(portfolio["BTC"]["purchase_prices"]) == 2


def test_remove_asset():
    PortfolioManager.add_asset("user1", "BTC", 2, 30000)
    portfolio = PortfolioManager.remove_asset("user1", "BTC")
    assert "BTC" not in portfolio
    # Remove non-existent asset
    portfolio = PortfolioManager.remove_asset("user1", "ETH")
    assert portfolio == {}


def test_get_portfolio():
    PortfolioManager.add_asset("user1", "ETH", 5, 2000)
    portfolio = PortfolioManager.get_portfolio("user1")
    assert portfolio == {
        "ETH": {
            "quantity": 5.0,
            "purchase_prices": [{"quantity": 5, "price": 2000.0}],
            "current_price": None,
        }
    }
    assert PortfolioManager.get_portfolio("unknown_user") == {}


def test_update_current_price():
    PortfolioManager.add_asset("user1", "BTC", 2, 30000)
    portfolio = PortfolioManager.update_current_price("user1", "BTC", 32000)
    assert portfolio["BTC"]["current_price"] == 32000.0


def test_invalid_inputs():
    with pytest.raises(ValueError, match="User ID must be a non-empty string"):
        PortfolioManager.add_asset("", "BTC", 2, 30000)
    with pytest.raises(ValueError, match="Quantity must be positive"):
        PortfolioManager.add_asset("user1", "BTC", -2, 30000)
    with pytest.raises(ValueError, match="Purchase price cannot be negative"):
        PortfolioManager.add_asset("user1", "BTC", 2, -30000)
    with pytest.raises(ValueError, match="Current price cannot be negative"):
        PortfolioManager.update_current_price("user1", "BTC", -32000)
