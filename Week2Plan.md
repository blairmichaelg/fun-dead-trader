__Overall Goals for Week 2:__ Implement a manual trade journaling feature persisting to Firestore. Display recent journal entries and basic performance metrics on a dashboard. Continue adhering to "Build–Measure–Learn Loops."

---

__1. Prioritized Task Plan (Under 10 Hours):__

- __Task 1: Firestore Setup & Secure Credentials (1.5 - 2 hours)__

  - Confirm Firestore DB (Native Mode).
  - Define basic Firestore security rules (single-user MVP: `allow read, write: if request.auth != null;` if you were to add Firebase Auth later, or `allow read, write: if true;` for absolute basic start, __with a strong warning in README about insecurity for public apps__). For now, `allow read, write: if true;` is acceptable given it's a personal tool and data isn't highly sensitive beyond trading records.
  - Generate GCP service account key JSON. __Store this securely and do not commit to Git.__
  - Set up Streamlit Secrets (`.streamlit/secrets.toml`) using the content of the service account key. Ensure `secrets.toml` is in `.gitignore`.
  - Update `README.md` with instructions for setting up `secrets.toml` or `GOOGLE_APPLICATION_CREDENTIALS` for local dev.

- __Task 2: Journal Entry Data Model & Firestore Utilities (2.5 - 3 hours)__

  - Finalize Firestore schema for `journal_entries` (as per original plan, ensuring all necessary fields like `symbol`, `entry_timestamp`, `exit_timestamp`, `direction`, `entry_price`, `exit_price`, `size`, `pnl`, `notes`, `created_at`).

  - Implement `core/firestore_utils.py`:

    - `init_firestore_client()`: Robustly initialize client (Streamlit secrets, then `GOOGLE_APPLICATION_CREDENTIALS` env var, then default ADC, with clear error if none).
    - `add_trade_entry(db, entry_data)`: Add entry, set `created_at` (server-side preferred: `firestore.SERVER_TIMESTAMP`). Return doc ID or success/failure.
    - `get_trade_entries(db, order_by_field="created_at", order_direction="DESCENDING", limit=None)`: More generic function to fetch trades, allowing optional limit.
    - Include basic error handling in these functions (e.g., log errors, return `None` or empty list on failure).

  - Write basic unit tests for these utility functions (might require `mock` for Firestore client).

- __Task 3: Journaling Feature UI - `pages/2_✍️_Journal.py` (3 - 3.5 hours)__

  - Build input form (using `st.form`) for manual trade details.
  - Use `st.date_input` and `st.time_input` for timestamps. Combine them into `datetime` objects for Firestore.
  - Client-side P\&L calculation for immediate feedback before saving.
  - On submission, call `add_trade_entry`. Display clear success/error messages (`st.success`, `st.error`).

- __Task 4: Basic Dashboard UI & Logic - `pages/3_📈_Dashboard.py` (2 - 2.5 hours)__

  - Fetch and display recent journal entries (e.g., last 10) in a `st.dataframe` or `st.table`. Format timestamps for readability.
  - Fetch all entries to calculate and display: Total Trades, Win Rate (Wins / Total Trades), Total P\&L.
  - Optionally: Average Win Amount, Average Loss Amount.
  - Use `core/dashboard_logic.py` if calculations become complex, otherwise can be direct in the page script.

- __Task 5: Testing, Refinement & Deployment (1 hour)__

  - Thoroughly test Firestore interactions locally and on Streamlit Cloud.
  - Update `requirements.txt` (`google-cloud-firestore`).
  - Commit changes, ensure deployment. Update `README.md`.

__Total Estimated Time: 10 - 12 hours__ (Slightly more due to added robustness and potential for basic tests for Firestore utils).
