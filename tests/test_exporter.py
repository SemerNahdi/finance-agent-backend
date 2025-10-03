import pytest
import os
import shutil
import pandas as pd
from app.agent.tools.exporter import ExporterTool


@pytest.fixture(autouse=True)
def cleanup_exports():
    """Clean up exports directory before and after tests."""
    export_dir = os.path.join("app", "data", "exports")
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)
    yield
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)


def test_export_portfolio_csv():
    portfolio = {
        "BTC": {
            "quantity": 2.0,
            "purchase_prices": [{"quantity": 2, "price": 30000.0}],
            "current_price": 32000.0,
        },
        "ETH": {
            "quantity": 5.0,
            "purchase_prices": [{"quantity": 5, "price": 2000.0}],
            "current_price": None,
        },
    }
    csv_path = ExporterTool.export_portfolio_csv("user1", portfolio)
    expected_path = os.path.join("app", "data", "exports", "user1_portfolio.csv")
    assert csv_path == expected_path
    assert os.path.exists(csv_path)
    assert os.path.getsize(csv_path) > 0
    # Verify CSV content
    df = pd.read_csv(csv_path)
    assert len(df) == 2
    assert df.iloc[0]["Asset"] == "BTC"
    assert df.iloc[0]["Value"] == 64000.0
    assert df.iloc[1]["Asset"] == "ETH"
    assert df.iloc[1]["Value"] == 10000.0


def test_export_portfolio_csv_empty():
    assert ExporterTool.export_portfolio_csv("user1", {}) is None


def test_export_portfolio_pdf():
    portfolio = {
        "BTC": {
            "quantity": 2.0,
            "purchase_prices": [{"quantity": 2, "price": 30000.0}],
            "current_price": 32000.0,
        },
        "ETH": {
            "quantity": 5.0,
            "purchase_prices": [{"quantity": 5, "price": 2000.0}],
            "current_price": None,
        },
    }
    pdf_path = ExporterTool.export_portfolio_pdf("user1", portfolio)
    expected_path = os.path.join("app", "data", "exports", "user1_portfolio.pdf")
    assert pdf_path == expected_path
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 0


def test_export_portfolio_pdf_empty():
    assert ExporterTool.export_portfolio_pdf("user1", {}) is None


def test_invalid_user_id():
    portfolio = {
        "BTC": {
            "quantity": 2.0,
            "purchase_prices": [{"quantity": 2, "price": 30000.0}],
            "current_price": None,
        }
    }
    with pytest.raises(ValueError, match="User ID must be a non-empty string"):
        ExporterTool.export_portfolio_csv("", portfolio)
    with pytest.raises(ValueError, match="User ID must be a non-empty string"):
        ExporterTool.export_portfolio_pdf("", portfolio)
