import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
from datetime import datetime, timezone

# Attempt to import Timestamp directly, if it fails, define a dummy for testing
try:
    from google.cloud.firestore import Timestamp as FirestoreTimestamp
except ImportError:
    # This block will be executed if google.cloud.firestore.Timestamp is not directly available
    # This is primarily for testing environments where the full Firestore client might not be mocked
    # or where Timestamp is not directly exposed at the top level.
    class FirestoreTimestamp:
        def __init__(self, dt):
            self.dt = dt

        @classmethod
        def from_datetime(cls, dt):
            return cls(dt)

        def isoformat(self):
            return self.dt.isoformat()

        def __eq__(self, other):
            if isinstance(other, FirestoreTimestamp):
                return self.dt == other.dt
            return NotImplemented

        @classmethod
        def now(cls):
            return cls(datetime.now(timezone.utc))

# Assign the correct Timestamp class to firestore.Timestamp for consistency
# This is crucial because the functions use firestore.SERVER_TIMESTAMP and firestore.Timestamp.from_datetime
firestore.Timestamp = FirestoreTimestamp


def init_firestore_client():
    """
    Initializes and returns a Firestore client.
    Prioritizes GOOGLE_APPLICATION_CREDENTIALS for local development,
    then falls back to Streamlit secrets for deployment.
    """
    if "firestore_client" not in st.session_state:
        db = None
        try:
            # First, try to initialize using GOOGLE_APPLICATION_CREDENTIALS environment variable
            # This is the recommended way for local development
            db = firestore.Client(database="fun-dead-trader") # Specify the database name
            st.success("Firestore client initialized using GOOGLE_APPLICATION_CREDENTIALS.")
        except Exception as e_env:
            st.warning(f"Could not initialize Firestore client using GOOGLE_APPLICATION_CREDENTIALS: {e_env}")
            st.info("Attempting to initialize using Streamlit secrets (for deployment)...")
            try:
                # Fallback to Streamlit secrets for deployment
                if "gcp_service_account" in st.secrets:
                    # Streamlit automatically parses secrets.toml into a dictionary-like object
                    key_dict = st.secrets["gcp_service_account"]
                    creds = service_account.Credentials.from_service_account_info(key_dict)
                    db = firestore.Client(credentials=creds, project=key_dict["project_id"], database="fun-dead-trader") # Specify the database name
                    st.success("Firestore client initialized using Streamlit secrets.")
                else:
                    st.error("Streamlit secret 'gcp_service_account' not found.")
            except Exception as e_secrets:
                st.error(f"Could not initialize Firestore client from Streamlit secrets: {e_secrets}")
        
        if db is None:
            st.error("Firestore client not initialized. Please ensure your GCP service account key is correctly set up "
                     "in GOOGLE_APPLICATION_CREDENTIALS environment variable (for local development) or "
                     "in Streamlit secrets (for deployment), and that the 'fun-dead-trader' database exists.")
        st.session_state["firestore_client"] = db
    return st.session_state.get("firestore_client")


def add_trade_entry(db, entry_data):
    """
    Adds a new trade entry to the 'journal_entries' collection in Firestore.
    Args:
        db: Firestore client instance.
        entry_data (dict): Dictionary containing trade entry details.
                           Expected keys: symbol, direction, entry_price, exit_price,
                           size, pnl, notes (optional), entry_timestamp (optional),
                           exit_timestamp (optional).
    Returns:
        str: Document ID of the newly added entry, or None if an error occurred.
    """
    if not db:
        st.error("Firestore client not initialized. Cannot add trade entry.")
        return None

    try:
        # Add created_at timestamp
        entry_data["created_at"] = firestore.SERVER_TIMESTAMP

        # Convert datetime objects to Firestore Timestamps if present
        if "entry_timestamp" in entry_data and \
           isinstance(entry_data["entry_timestamp"], datetime):
            entry_data["entry_timestamp"] = \
                firestore.Timestamp.from_datetime(entry_data["entry_timestamp"])
        if "exit_timestamp" in entry_data and \
           isinstance(entry_data["exit_timestamp"], datetime):
            entry_data["exit_timestamp"] = \
                firestore.Timestamp.from_datetime(entry_data["exit_timestamp"])

        doc_ref = db.collection("journal_entries").add(entry_data)
        st.success(f"Trade entry added with ID: {doc_ref[1].id}")
        return doc_ref[1].id
    except Exception as e:
        st.error(f"Error adding trade entry: {e}")
        return None


def get_trade_entries(db, limit=None):
    """
    Retrieves trade entries from the 'journal_entries' collection,
    ordered by 'created_at'.
    Args:
        db: Firestore client instance.
        limit (int, optional): Maximum number of entries to retrieve.
                               Defaults to None (all).
    Returns:
        list: A list of dictionaries, each representing a trade entry.
              Includes the document ID as 'id'.
    """
    if not db:
        st.error("Firestore client not initialized. Cannot retrieve trade entries.")
        return []

    try:
        query = db.collection("journal_entries").order_by(
            "created_at", direction=firestore.Query.DESCENDING)
        if limit:
            query = query.limit(limit)

        docs = query.stream()
        entries = []
        for doc in docs:
            entry = doc.to_dict()
            entry["id"] = doc.id
            # Convert Firestore Timestamps to datetime objects
            # for easier handling in Streamlit
            if "created_at" in entry and \
               isinstance(entry["created_at"], firestore.Timestamp):
                entry["created_at"] = entry["created_at"].astimezone(timezone.utc)
            if "entry_timestamp" in entry and \
               isinstance(entry["entry_timestamp"], firestore.Timestamp):
                entry["entry_timestamp"] = \
                    entry["entry_timestamp"].astimezone(timezone.utc)
            if "exit_timestamp" in entry and \
               isinstance(entry["exit_timestamp"], firestore.Timestamp):
                entry["exit_timestamp"] = \
                    entry["exit_timestamp"].astimezone(timezone.utc)
            entries.append(entry)
        return entries
    except Exception as e:
        st.error(f"Error retrieving trade entries: {e}")
        return []
