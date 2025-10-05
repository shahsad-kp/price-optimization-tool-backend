from decimal import Decimal
from typing import Optional

import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.exponential_smoothing import ExponentialSmoothing

from Products.models import Products


def generate_demand_forecast(instance: Products, number_of_days: int = 30) -> Optional[dict]:
    """
    Returns demand forecast (units), revenue forecast, and profit forecast.
    """
    sales = instance.sales.all()
    selling_price = float(instance.selling_price)
    cost_price = float(instance.cost_price)

    if sales.count() < number_of_days:
        return None

    data = {
        "date": list(sales.values_list("date", flat=True)),
        "units_sold": list(sales.values_list("units_sold", flat=True)),
    }
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values("date", inplace=True)
    df.set_index("date", inplace=True)

    df = df.asfreq("D")

    if len(df) < 2:
        units_forecast = int(df["units_sold"].iloc[0] * number_of_days)
        revenue_forecast = units_forecast * selling_price
        profit_forecast = units_forecast * (selling_price - cost_price)
        return {
            "units_forecast": units_forecast,
            "revenue_forecast": revenue_forecast,
            "profit_forecast": profit_forecast,
        }

    model = ExponentialSmoothing(df["units_sold"], trend="add", seasonal=None)
    fit = model.fit()
    forecast_units = fit.forecast(number_of_days)

    units_forecast = int(forecast_units.sum())
    revenue_forecast = units_forecast * selling_price
    profit_forecast = units_forecast * (selling_price - cost_price)

    return {
        "units_forecast": units_forecast,
        "revenue_forecast": revenue_forecast,
        "profit_forecast": profit_forecast,
    }


def calculate_optimal_price(current_price: float, total_forecasted_demand: int, cost_price: float, elasticity: float = -1.2) -> dict:
    prices = np.linspace(current_price * 0.8, current_price * 1.2, 50)

    profits = []
    for p in prices:
        estimated_demand = total_forecasted_demand * (p / current_price) ** elasticity
        profit = (p - cost_price) * estimated_demand
        profits.append(profit)

    optimal_index = np.argmax(profits)
    optimal_price = prices[optimal_index]
    max_profit = profits[optimal_index]

    return {
        "optimal_price": optimal_price,
        "max_profit": max_profit,
    }
