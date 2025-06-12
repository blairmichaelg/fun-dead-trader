import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from trader_companion_app.core.firestore_utils import init_firestore_client, get_trade_entries

st.set_page_config(page_title="Dashboard", page_icon="📈")

st.title("📈 Trade Dashboard")
st.markdown("Overview of your trade performance.")

db = init_firestore_client()

if db:
    st.header("Recent Trades")
    trades = get_trade_entries(db)

    if trades:
        # Convert list of dicts to DataFrame
        df = pd.DataFrame(trades)

        # Format timestamps for better readability
        if 'created_at' in df.columns:
            df['created_at'] = df['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        if 'entry_timestamp' in df.columns:
            df['entry_timestamp'] = df['entry_timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        if 'exit_timestamp' in df.columns:
            df['exit_timestamp'] = df['exit_timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Display trades
        st.dataframe(df)

        st.header("Performance Metrics")

        total_trades = len(df)
        total_pnl = df['pnl'].sum()
        winning_trades = df[df['pnl'] > 0]
        win_rate = (len(winning_trades) / total_trades) * 100 if total_trades > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Trades", total_trades)
        with col2:
            st.metric("Total P&L", f"${total_pnl:,.2f}")
        with col3:
            st.metric("Win Rate", f"{win_rate:.2f}%")

    else:
        st.info("No trade entries found. Add some trades using the 'Journal' page.")
else:
    st.warning("Firestore client not initialized. Please check your GCP credentials setup.")
