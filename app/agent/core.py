import logging
from typing import Any
from pydantic import BaseModel
from app.agent.tools.calculator import CalculatorTool
from app.agent.tools.portfolio_manager import PortfolioManager
from app.agent.tools.exporter import ExporterTool
from app.agent.tools import visualizer  # Optional, if implemented

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentResponse(BaseModel):
    text: str
    chart_path: str | None = None
    csv_path: str | None = None
    pdf_path: str | None = None


async def process_query(user_id: str, query: str) -> AgentResponse:
    """
    Core orchestrator handling queries for portfolio management, calculations, and exports.
    """
    if not user_id or not isinstance(user_id, str):
        return AgentResponse(text="Invalid user ID.")

    try:
        calculator = CalculatorTool()
        portfolio_manager = PortfolioManager()
        exporter = ExporterTool()

        # --- Portfolio Manager Queries ---
        if "add asset" in query.lower():
            parts = query.split()
            if len(parts) == 5:
                try:
                    _, _, asset_name, quantity, price = parts
                    quantity, price = float(quantity), float(price)
                    portfolio = portfolio_manager.add_asset(
                        user_id, asset_name, quantity, price
                    )
                    text = f"Added {quantity} {asset_name} at ${price} each."
                    chart_path = (
                        visualizer.generate_portfolio_chart(user_id, portfolio)
                        if hasattr(visualizer, "generate_portfolio_chart")
                        else None
                    )
                    return AgentResponse(text=text, chart_path=chart_path)
                except ValueError as e:
                    logger.error(f"Add asset error: {e}")
                    return AgentResponse(
                        text="Invalid quantity or price. Use: add asset [name] [quantity] [price]"
                    )
            return AgentResponse(
                text="Invalid format. Use: add asset [name] [quantity] [price]"
            )

        if "remove asset" in query.lower():
            parts = query.split()
            if len(parts) == 3:
                _, _, asset_name = parts
                portfolio = portfolio_manager.remove_asset(user_id, asset_name)
                text = f"Removed {asset_name} from your portfolio."
                chart_path = (
                    visualizer.generate_portfolio_chart(user_id, portfolio)
                    if hasattr(visualizer, "generate_portfolio_chart")
                    else None
                )
                return AgentResponse(text=text, chart_path=chart_path)
            return AgentResponse(text="Invalid format. Use: remove asset [name]")

        if "show portfolio" in query.lower():
            portfolio = portfolio_manager.get_portfolio(user_id)
            if not portfolio:
                return AgentResponse(text="Your portfolio is empty.")
            portfolio_text = "\n".join(
                [
                    f"{k}: {v['quantity']:.2f} units at ${v['purchase_prices'][-1]['price']:.2f}"
                    for k, v in portfolio.items()
                ]
            )
            text = f"Your portfolio:\n{portfolio_text}"
            chart_path = (
                visualizer.generate_portfolio_chart(user_id, portfolio)
                if hasattr(visualizer, "generate_portfolio_chart")
                else None
            )
            return AgentResponse(text=text, chart_path=chart_path)

        if "update current price" in query.lower():
            parts = query.split()
            if len(parts) == 5:
                try:
                    _, _, _, asset_name, price = parts
                    price = float(price)
                    portfolio = portfolio_manager.update_current_price(
                        user_id, asset_name, price
                    )
                    text = f"Updated {asset_name} current price to ${price}."
                    chart_path = (
                        visualizer.generate_portfolio_chart(user_id, portfolio)
                        if hasattr(visualizer, "generate_portfolio_chart")
                        else None
                    )
                    return AgentResponse(text=text, chart_path=chart_path)
                except ValueError as e:
                    logger.error(f"Update price error: {e}")
                    return AgentResponse(
                        text="Invalid price. Use: update current price [name] [price]"
                    )
            return AgentResponse(
                text="Invalid format. Use: update current price [name] [price]"
            )

        if "roi" in query.lower():
            portfolio = portfolio_manager.get_portfolio(user_id)
            if not portfolio:
                return AgentResponse(text="Your portfolio is empty. Add assets first.")
            try:
                roi = portfolio_manager.calculate_portfolio_roi(user_id, calculator)
                text = f"Your portfolio ROI is {roi:.2f}%."
                chart_path = (
                    visualizer.generate_portfolio_chart(user_id, portfolio)
                    if hasattr(visualizer, "generate_portfolio_chart")
                    else None
                )
                return AgentResponse(text=text, chart_path=chart_path)
            except ValueError as e:
                logger.error(f"ROI calculation failed: {e}")
                return AgentResponse(
                    text=f"Cannot calculate ROI: {str(e)} (Update current prices first.)"
                )

        if "simulate investment" in query.lower():
            parts = query.split()
            if len(parts) == 5:
                try:
                    _, _, principal, rate, years = parts
                    principal, rate, years = float(principal), float(rate), int(years)
                    sim_result = calculator.investment_simulation(
                        principal, rate, years
                    )
                    text = "Investment Simulation:\n" + "\n".join(
                        [f"Year {k}: ${v:.2f}" for k, v in sim_result.items()]
                    )
                    chart_path = (
                        visualizer.generate_simulation_chart(user_id, sim_result)
                        if hasattr(visualizer, "generate_simulation_chart")
                        else None
                    )
                    return AgentResponse(text=text, chart_path=chart_path)
                except ValueError as e:
                    logger.error(f"Simulation error: {e}")
                    return AgentResponse(
                        text="Invalid principal, rate, or years. Use: simulate investment [principal] [rate] [years]"
                    )
            return AgentResponse(
                text="Invalid format. Use: simulate investment [principal] [rate] [years]"
            )

        if "export portfolio" in query.lower():
            portfolio = portfolio_manager.get_portfolio(user_id)
            if not portfolio:
                return AgentResponse(text="Your portfolio is empty. Nothing to export.")
            try:
                csv_path = exporter.export_portfolio_csv(user_id, portfolio)
                pdf_path = exporter.export_portfolio_pdf(user_id, portfolio)
                text = f"Portfolio exported successfully. CSV: {csv_path or 'N/A'}, PDF: {pdf_path or 'N/A'}"
                return AgentResponse(text=text, csv_path=csv_path, pdf_path=pdf_path)
            except (ValueError, OSError) as e:
                logger.error(f"Export error: {e}")
                return AgentResponse(text=f"Failed to export portfolio: {str(e)}")

        return AgentResponse(text="Sorry, I didn't understand your request.")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return AgentResponse(text=f"An error occurred: {str(e)}")
