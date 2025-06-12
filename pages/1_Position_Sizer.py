import streamlit as st
from core.position_sizer import calculate_position_size

st.set_page_config(page_title="Position Sizer")

st.title("📊 Position Sizing Tool")

st.markdown(
    """
    Calculate your position size based on your account balance,
    risk tolerance, and trade entry/stop-loss prices.
    """
)

# Input widgets
account_balance = st.number_input(
    "Account Balance ($)", min_value=0.01, value=10000.00, step=1000.00
)
risk_percentage = st.slider(
    "Risk per Trade (%)", min_value=0.01, max_value=10.00, value=1.00, step=0.01
)
entry_price = st.number_input(
    "Entry Price ($)", min_value=0.01, value=100.00, step=0.01
)
stop_loss_price = st.number_input(
    "Stop Loss Price ($)", min_value=0.01, value=99.00, step=0.01
)
trade_direction = st.radio("Trade Direction", ("Long", "Short"))

is_long_trade = trade_direction == "Long"

if st.button("Calculate Position Size"):
    try:
        result = calculate_position_size(
            account_balance=account_balance,
            risk_percentage=risk_percentage,
            entry_price=entry_price,
            stop_loss_price=stop_loss_price,
            is_long_trade=is_long_trade,
        )

        st.subheader("Calculation Results:")
        st.metric(
            label="Position Size (Units/Shares)",
            value=f"{result['position_size_units']:.2f}",
        )
        st.metric(
            label="Dollar Amount at Risk", value=f"${result['risk_amount_dollars']:.2f}"
        )

        total_position_value = result["position_size_units"] * entry_price
        st.metric(label="Total Position Value", value=f"${total_position_value:.2f}")

        if total_position_value > account_balance:
            st.warning(
                "⚠️ Warning: Total position value exceeds account balance. "
                "Consider adjusting inputs or leverage."
            )

        st.markdown("---")
        st.subheader("Summary of Inputs and Risk:")
        st.write(f"**Account Balance:** ${account_balance:.2f}")
        st.write(f"**Risk Percentage:** {risk_percentage:.2f}%")
        st.write(f"**Entry Price:** ${entry_price:.2f}")
        st.write(f"**Stop Loss Price:** ${stop_loss_price:.2f}")
        st.write(f"**Trade Direction:** {trade_direction}")
        st.write(f"**Risk per Unit:** ${result['risk_per_unit']:.2f}")

    except ValueError as e:
        st.error(f"Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
