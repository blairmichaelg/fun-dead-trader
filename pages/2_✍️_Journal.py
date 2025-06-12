import streamlit as st
from datetime import datetime, time, timezone
from ..core.firestore_utils import init_firestore_client, add_trade_entry

st.set_page_config(page_title="Journal", page_icon="✍️")

st.title("✍️ Trade Journal")
st.markdown("Record your trades and track your performance.")

db = init_firestore_client()

if db:
    with st.form("trade_entry_form"):
        st.header("New Trade Entry")

        col1, col2 = st.columns(2)
        with col1:
            symbol = st.text_input("Symbol", placeholder="e.g., BTCUSD, AAPL",
                                   help="Trading pair or stock symbol.")
            direction = st.selectbox("Direction", ["Long", "Short"],
                                     help="Whether you bought (Long) or sold (Short).")
            entry_price = st.number_input("Entry Price", min_value=0.0,
                                          format="%.2f",
                                          help="Price at which you entered the "
                                               "trade.")
            exit_price = st.number_input("Exit Price", min_value=0.0,
                                         format="%.2f",
                                         help="Price at which you exited the "
                                               "trade.")
            size = st.number_input("Size", min_value=0.0, format="%.4f",
                                   help="Amount of asset traded (e.g., 0.01 BTC, "
                                         "100 shares).")

        with col2:
            st.subheader("Entry Timestamp")
            entry_date = st.date_input("Entry Date", value="today")
            entry_time = st.time_input("Entry Time", value=time(9, 30))
            
            st.subheader("Exit Timestamp")
            exit_date = st.date_input("Exit Date", value="today")
            exit_time = st.time_input("Exit Time", value=time(16, 0))

        notes = st.text_area("Notes",
                             help="Any relevant notes about the trade (e.g., "
                                  "strategy, emotions, news).")

        submitted = st.form_submit_button("Add Trade Entry")

        if submitted:
            # Input Validation
            # Combine date and time for timestamps
            entry_timestamp = datetime.combine(entry_date, entry_time,
                                               tzinfo=timezone.utc)
            exit_timestamp = datetime.combine(exit_date, exit_time,
                                              tzinfo=timezone.utc)

            # Input Validation
            if not symbol:
                st.error("Symbol is required.")
            elif (entry_price <= 0 or exit_price <= 0 or size <= 0):
                st.error("Entry Price, Exit Price, and Size must be greater than zero.")
            elif entry_timestamp >= exit_timestamp:
                st.error("Exit Timestamp must be after Entry Timestamp.")
            else:
                # Calculate P&L
                pnl = (exit_price - entry_price) * size
                if direction == "Short":  # Reverse P&L for short trades
                    pnl = -pnl

                trade_data = {
                    "symbol": symbol.upper(),
                    "direction": direction,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "size": size,
                    "pnl": pnl,
                    "notes": notes,
                    "entry_timestamp": entry_timestamp,
                    "exit_timestamp": exit_timestamp
                }

                trade_doc_id = add_trade_entry(db, trade_data)
                if trade_doc_id:
                    st.success(f"Trade for {symbol.upper()} (ID: {trade_doc_id}) "
                               "added successfully!")
                    # Clear form fields (requires re-running the script, which
                    # happens on successful form submission in Streamlit)
                    # For a more direct clear, one might use st.experimental_rerun()
                    # or manage state more explicitly, but for now, the form
                    # will reset on next interaction.
                # No else block needed, as add_trade_entry already handles errors.
else:
    st.warning("Firestore client not initialized. "
               "Please check your GCP credentials setup.")
