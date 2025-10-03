import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from typing import Dict, Any
from decimal import Decimal

EXPORT_PATH = os.path.join("app", "data", "exports")


class ExporterTool:
    """Tool for exporting portfolio data to CSV and PDF formats."""

    @staticmethod
    def export_portfolio_csv(user_id: str, portfolio: Dict[str, Any]) -> str | None:
        """
        Export user's portfolio to CSV.

        Args:
            user_id: Unique identifier for the user.
            portfolio: Portfolio dictionary from PortfolioManager.

        Returns:
            Path to the saved CSV file, or None if portfolio is empty.

        Raises:
            ValueError: If user_id is invalid.
            OSError: If file writing fails.
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")
        if not portfolio:
            return None

        # Prepare data for CSV
        data = []
        for asset_name, details in portfolio.items():
            price = (
                details["current_price"]
                if details["current_price"] is not None
                else details["purchase_prices"][-1]["price"]
            )
            value = float(
                Decimal(str(details["quantity"] * price)).quantize(Decimal("0.01"))
            )
            data.append(
                {
                    "Asset": asset_name,
                    "Quantity": details["quantity"],
                    "Price": price,
                    "Value": value,
                }
            )

        # Create CSV
        os.makedirs(EXPORT_PATH, exist_ok=True)
        csv_file = os.path.join(EXPORT_PATH, f"{user_id}_portfolio.csv")
        try:
            df = pd.DataFrame(data)
            df.to_csv(csv_file, index=False)
            return csv_file
        except OSError as e:
            raise OSError(f"Failed to write CSV file: {e}")

    @staticmethod
    def export_portfolio_pdf(user_id: str, portfolio: Dict[str, Any]) -> str | None:
        """
        Export user's portfolio to PDF with formatted table.

        Args:
            user_id: Unique identifier for the user.
            portfolio: Portfolio dictionary from PortfolioManager.

        Returns:
            Path to the saved PDF file, or None if portfolio is empty.

        Raises:
            ValueError: If user_id is invalid.
            OSError: If file writing fails.
        """
        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")
        if not portfolio:
            return None

        # Prepare PDF
        os.makedirs(EXPORT_PATH, exist_ok=True)
        pdf_file = os.path.join(EXPORT_PATH, f"{user_id}_portfolio.pdf")
        try:
            doc = SimpleDocTemplate(pdf_file, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []

            # Title
            elements.append(
                Paragraph(f"Portfolio Report for {user_id}", styles["Title"])
            )
            elements.append(
                Paragraph(
                    f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    styles["Normal"],
                )
            )
            elements.append(Spacer(1, 12))

            # Table data
            table_data = [["Asset", "Quantity", "Price ($)", "Value ($)"]]
            total_value = 0
            for asset_name, details in portfolio.items():
                price = (
                    details["current_price"]
                    if details["current_price"] is not None
                    else details["purchase_prices"][-1]["price"]
                )
                value = float(
                    Decimal(str(details["quantity"] * price)).quantize(Decimal("0.01"))
                )
                total_value += value
                table_data.append(
                    [
                        asset_name,
                        f"{details['quantity']:.2f}",
                        f"{price:.2f}",
                        f"{value:.2f}",
                    ]
                )
            table_data.append(["Total", "", "", f"{total_value:.2f}"])

            # Create table
            table = Table(table_data)
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, 0), 12),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                        ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ]
                )
            )
            elements.append(table)

            # Build PDF
            doc.build(elements)
            return pdf_file
        except OSError as e:
            raise OSError(f"Failed to write PDF file: {e}")
