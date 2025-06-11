import pytest
from core.position_sizer import calculate_position_size


# Test cases for valid long trade calculation
def test_valid_long_trade():
    result = calculate_position_size(
        account_balance=10000,
        risk_percentage=1,
        entry_price=100,
        stop_loss_price=99,
        is_long_trade=True,
    )
    assert result["position_size_units"] == 100
    assert result["risk_amount_dollars"] == 100
    assert result["risk_per_unit"] == 1

    result = calculate_position_size(
        account_balance=50000,
        risk_percentage=0.5,
        entry_price=50,
        stop_loss_price=49.5,
        is_long_trade=True,
    )
    assert result["position_size_units"] == 500
    assert result["risk_amount_dollars"] == 250
    assert result["risk_per_unit"] == 0.5


# Test cases for valid short trade calculation
def test_valid_short_trade():
    result = calculate_position_size(
        account_balance=10000,
        risk_percentage=1,
        entry_price=100,
        stop_loss_price=101,
        is_long_trade=False,
    )
    assert result["position_size_units"] == 100
    assert result["risk_amount_dollars"] == 100
    assert result["risk_per_unit"] == 1

    result = calculate_position_size(
        account_balance=20000,
        risk_percentage=2,
        entry_price=200,
        stop_loss_price=202,
        is_long_trade=False,
    )
    assert result["position_size_units"] == 200
    assert result["risk_amount_dollars"] == 400
    assert result["risk_per_unit"] == 2


# Test cases for invalid inputs
@pytest.mark.parametrize(
    "account_balance, risk_percentage, entry_price, stop_loss_price, "
    "is_long_trade, expected_error",
    [
        (0, 1, 100, 99, True, "Account balance must be a positive number."),
        (-100, 1, 100, 99, True, "Account balance must be a positive number."),
        (
            10000, 0, 100, 99, True,
            "Risk percentage must be between 0 and 100 "
            "(exclusive of 0, inclusive of 100).",
        ),
        (
            10000, 101, 100, 99, True,
            "Risk percentage must be between 0 and 100 "
            "(exclusive of 0, inclusive of 100).",
        ),
        (10000, 1, 0, 99, True, "Entry price must be a positive number."),
        (10000, 1, -100, 99, True, "Entry price must be a positive number."),
        (10000, 1, 100, 0, True, "Stop loss price must be a positive number."),
        (10000, 1, 100, -99, True, "Stop loss price must be a positive number."),
    ],
)
def test_invalid_inputs(
    account_balance,
    risk_percentage,
    entry_price,
    stop_loss_price,
    is_long_trade,
    expected_error,
):
    with pytest.raises(ValueError) as excinfo:
        calculate_position_size(
            account_balance,
            risk_percentage,
            entry_price,
            stop_loss_price,
            is_long_trade,
        )
    assert expected_error in str(excinfo.value)


# Test cases for logical errors (stop loss price incorrect relative to entry price)
@pytest.mark.parametrize(
    "account_balance, risk_percentage, entry_price, stop_loss_price, "
    "is_long_trade, expected_error",
    [
        (
            10000, 1, 100, 100, True,  # Long trade, SL == Entry
            "Risk per unit cannot be zero or negative.",
        ),
        (
            10000, 1, 100, 101, True,  # Long trade, SL > Entry
            "For a long trade, stop loss price must be less than entry price.",
        ),
        (
            10000, 1, 100, 100, False,  # Short trade, SL == Entry
            "Risk per unit cannot be zero or negative.",
        ),
        (
            10000, 1, 100, 99, False,  # Short trade, SL < Entry
            "For a short trade, stop loss price must be "
            "greater than entry price.",
        ),
    ],
)
def test_logical_errors(
    account_balance,
    risk_percentage,
    entry_price,
    stop_loss_price,
    is_long_trade,
    expected_error,
):
    with pytest.raises(ValueError) as excinfo:
        calculate_position_size(
            account_balance,
            risk_percentage,
            entry_price,
            stop_loss_price,
            is_long_trade,
        )
    assert expected_error in str(excinfo.value)


# Test cases for edge cases (entry_price == stop_loss_price leading to zero risk_per_unit)
def test_edge_case_zero_risk_per_unit():
    with pytest.raises(ValueError) as excinfo:
        calculate_position_size(
            account_balance=10000,
            risk_percentage=1,
            entry_price=100,
            stop_loss_price=100,
            is_long_trade=True,
        )
    assert "Risk per unit cannot be zero or negative." in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        calculate_position_size(
            account_balance=10000,
            risk_percentage=1,
            entry_price=100,
            stop_loss_price=100,
            is_long_trade=False,
        )
    assert "Risk per unit cannot be zero or negative." in str(excinfo.value)
