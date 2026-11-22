"""Route-based pass pricing rules for the City Bus Pass application."""

DISCOUNTS = {7: 0.00, 30: 0.20, 90: 0.40}

def route_base_fare(route_name, routes):
    """Return the configured one-day fare for a route."""
    return float(routes[route_name]["fare"])

def calculate_pass_price(daily_fare, validity_days):
    """Calculate total fare, applying suggested discounts for longer passes."""
    days = int(validity_days)
    if days not in DISCOUNTS:
        raise ValueError("Validity must be 7, 30, or 90 days.")
    if float(daily_fare) < 0:
        raise ValueError("Daily fare cannot be negative.")
    return round(float(daily_fare) * days * (1 - DISCOUNTS[days]), 2)
