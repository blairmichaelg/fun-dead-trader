def calculate_position_size(
    account_balance: float,
    risk_percentage: float,
    entry_price: float,
    stop_loss_price: float,
    is_long_trade: bool,
) -> dict:
    """
    Calculates position size based on account balance, risk percentage,
    and trade details.
    Returns a dictionary: {'position_size_units': float,
    'risk_amount_dollars': float, 'risk_per_unit': float}
    Includes robust input validation (positive balance, valid risk %,
    valid prices, logical entry/stop for trade direction).
    """
    # Input validation
    if not isinstance(account_balance, (int, float)) or account_balance <= 0:
        raise ValueError("Account balance must be a positive number.")
    if not isinstance(risk_percentage, (int, float)) or not (
        0 < risk_percentage <= 100
    ):
        raise ValueError(
            "Risk percentage must be between 0 and 100 "
            "(exclusive of 0, inclusive of 100)."
        )
    if not isinstance(entry_price, (int, float)) or entry_price <= 0:
        raise ValueError("Entry price must be a positive number.")
    if not isinstance(stop_loss_price, (int, float)) or stop_loss_price <= 0:
        raise ValueError("Stop loss price must be a positive number.")

    # Calculate risk per unit
    if is_long_trade:
        if stop_loss_price > entry_price:  # Changed from >= to >
            raise ValueError(
                "For a long trade, stop loss price must be "
                "less than entry price."
            )
        risk_per_unit = entry_price - stop_loss_price
    else:  # Short trade
        if stop_loss_price < entry_price:  # Changed from <= to <
            raise ValueError(
                "For a short trade, stop loss price must be "
                "greater than entry price."
            )
        risk_per_unit = stop_loss_price - entry_price

    if risk_per_unit <= 0:
        raise ValueError(
            "Risk per unit cannot be zero or negative. "
            "Adjust entry and stop loss prices."
        )

    # Calculate risk amount in dollars
    risk_amount_dollars = account_balance * (risk_percentage / 100)

    # Calculate position size
    position_size_units = risk_amount_dollars / risk_per_unit

    return {
        "position_size_units": position_size_units,
        "risk_amount_dollars": risk_amount_dollars,
        "risk_per_unit": risk_per_unit,
    }
