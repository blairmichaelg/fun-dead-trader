import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
import json

# Import firestore directly, as it's used in the tests
from google.cloud import firestore
# from google.cloud.firestore import Timestamp # Explicitly import Timestamp - will use dummy instead

# Define a dummy Timestamp class for testing purposes
class DummyTimestamp:
    def __init__(self, dt):
        self.dt = dt

    @classmethod
    def from_datetime(cls, dt):
        return cls(dt)

    def isoformat(self):
        return self.dt.isoformat()

    def __eq__(self, other):
        if isinstance(other, DummyTimestamp):
            return self.dt == other.dt
        return NotImplemented

# Use the dummy Timestamp for all tests
Timestamp = DummyTimestamp


# Import the functions to be tested
from core.firestore_utils import (
    init_firestore_client,
    add_trade_entry,
    get_trade_entries
)

class TestFirestoreUtils(unittest.TestCase):

    def setUp(self):
        # Use a real dictionary for the internal state of session_state mock
        self._session_state_data = {}
        self.mock_st_session_state = MagicMock(
            __getitem__=MagicMock(side_effect=self._session_state_data.__getitem__),
            __setitem__=MagicMock(side_effect=self._session_state_data.__setitem__),
            get=MagicMock(side_effect=self._session_state_data.get),
            clear=MagicMock(side_effect=self._session_state_data.clear),
            __contains__=MagicMock(side_effect=self._session_state_data.__contains__)
        )

        # Use a real dictionary for the internal state of secrets mock
        self._secrets_data = {}
        self.mock_st_secrets = MagicMock(
            __getitem__=MagicMock(side_effect=self._secrets_data.__getitem__),
            __setitem__=MagicMock(side_effect=self._secrets_data.__setitem__),
            clear=MagicMock(side_effect=self._secrets_data.clear),
            __contains__=MagicMock(side_effect=self._secrets_data.__contains__)
        )

        # Patch Streamlit components directly in the firestore_utils module
        self.patcher_st_session_state = patch('trader_companion_app.core.firestore_utils.st.session_state', new=self.mock_st_session_state)
        self.patcher_st_secrets = patch('trader_companion_app.core.firestore_utils.st.secrets', new=self.mock_st_secrets)
        self.patcher_st_success = patch('trader_companion_app.core.firestore_utils.st.success', new_callable=MagicMock)
        self.patcher_st_warning = patch('trader_companion_app.core.firestore_utils.st.warning', new_callable=MagicMock)
        self.patcher_st_info = patch('trader_companion_app.core.firestore_utils.st.info', new_callable=MagicMock)
        self.patcher_st_error = patch('trader_companion_app.core.firestore_utils.st.error', new_callable=MagicMock)
        self.patcher_firestore_timestamp = patch('trader_companion_app.core.firestore_utils.firestore.Timestamp', new=DummyTimestamp)
        self.patcher_firestore_query = patch('trader_companion_app.core.firestore_utils.firestore.Query', new_callable=MagicMock)


        self.mock_st_session_state = self.patcher_st_session_state.start()
        self.mock_st_secrets = self.patcher_st_secrets.start()
        self.mock_st_success = self.patcher_st_success.start()
        self.mock_st_warning = self.patcher_st_warning.start()
        self.mock_st_info = self.patcher_st_info.start()
        self.mock_st_error = self.patcher_st_error.start()
        self.mock_firestore_timestamp = self.patcher_firestore_timestamp.start()
        self.mock_firestore_query = self.patcher_firestore_query.start()
        self.mock_firestore_query.DESCENDING = "descending" # Mock the DESCENDING attribute


        # Clear session_state and secrets for each test
        self.mock_st_session_state.clear()
        self.mock_st_secrets.clear()

    def tearDown(self):
        self.patcher_st_session_state.stop()
        self.patcher_st_secrets.stop()
        self.patcher_st_success.stop()
        self.patcher_st_warning.stop()
        self.patcher_st_info.stop()
        self.patcher_st_error.stop()
        self.patcher_firestore_timestamp.stop()
        self.patcher_firestore_query.stop()


    @patch('google.cloud.firestore.Client')
    @patch('google.oauth2.service_account.Credentials.from_service_account_info')
    def test_init_firestore_client_with_secrets(self, mock_credentials, mock_firestore_client):
        """
        Test that init_firestore_client initializes with Streamlit secrets.
        """
        mock_key_dict = {
            "type": "service_account",
            "project_id": "test-project",
            "private_key_id": "some_id",
            "private_key": "-----BEGIN PRIVATE KEY-----\nTEST_KEY\n-----END PRIVATE KEY-----\n",
            "client_email": "test@test-project.iam.gserviceaccount.com",
            "client_id": "12345",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test%40test-project.iam.gserviceaccount.com"
        }
        self.mock_st_secrets["gcp_service_account"] = json.dumps(mock_key_dict)

        mock_db_instance = mock_firestore_client.return_value
        mock_creds_instance = mock_credentials.return_value

        db_client = init_firestore_client()

        mock_credentials.assert_called_once_with(mock_key_dict)
        mock_firestore_client.assert_called_once_with(
            credentials=mock_creds_instance, project="test-project"
        )
        self.assertEqual(db_client, mock_db_instance)
        self.assertIn("firestore_client", self.mock_st_session_state)
        self.assertEqual(self.mock_st_session_state["firestore_client"], mock_db_instance)
        self.mock_st_success.assert_called_once_with("Firestore client initialized using Streamlit secrets.")
        self.mock_st_warning.assert_not_called()
        self.mock_st_info.assert_not_called()
        self.mock_st_error.assert_not_called()


    @patch('google.cloud.firestore.Client')
    @patch('google.oauth2.service_account.Credentials.from_service_account_info')
    def test_init_firestore_client_with_env_var_fallback(self, mock_credentials, mock_firestore_client):
        """
        Test that init_firestore_client falls back to GOOGLE_APPLICATION_CREDENTIALS
        if Streamlit secrets are not available.
        """
        # Ensure no secrets are set
        self.mock_st_secrets.clear()

        mock_db_instance = mock_firestore_client.return_value
        db_client = init_firestore_client()

        self.mock_st_warning.assert_called_once_with("Streamlit secret 'gcp_service_account' not found.")
        self.mock_st_info.assert_called_once_with("Attempting to initialize using GOOGLE_APPLICATION_CREDENTIALS environment variable...")
        mock_firestore_client.assert_called_once_with() # Called without args for env var
        self.assertEqual(db_client, mock_db_instance)
        self.assertIn("firestore_client", self.mock_st_session_state)
        self.assertEqual(self.mock_st_session_state["firestore_client"], mock_db_instance)
        self.mock_st_success.assert_called_once_with("Firestore client initialized using GOOGLE_APPLICATION_CREDENTIALS.")
        self.mock_st_error.assert_not_called() # Should not error if env var works
        mock_credentials.assert_not_called() # Should not try to use credentials from secrets


    @patch('google.cloud.firestore.Client')
    # Removed the patch for firestore.Timestamp here, as it's now patched in setUp
    def test_add_trade_entry_success(self, mock_firestore_client):
        """
        Test that add_trade_entry successfully adds an entry.
        """
        mock_db = mock_firestore_client.return_value
        mock_collection = mock_db.collection.return_value
        mock_add_result = MagicMock()
        mock_add_result.id = "test_doc_id"
        mock_collection.add.return_value = (None, mock_add_result) # Mocking doc_ref tuple

        entry_data = {
            "symbol": "AAPL",
            "direction": "Long",
            "entry_price": 150.0,
            "exit_price": 155.0,
            "size": 10,
            "pnl": 50.0,
            "notes": "Test trade",
            "entry_timestamp": datetime(2023, 1, 1, 9, 30, 0, tzinfo=timezone.utc),
            "exit_timestamp": datetime(2023, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
        }

        doc_id = add_trade_entry(mock_db, entry_data)

        mock_db.collection.assert_called_once_with("journal_entries")
        mock_collection.add.assert_called_once()
        self.assertEqual(doc_id, "test_doc_id")
        self.mock_st_error.assert_not_called()
        self.mock_st_success.assert_called_once_with("Trade entry added with ID: test_doc_id")

        # Verify timestamps are converted
        added_data = mock_collection.add.call_args[0][0]
        self.assertIsInstance(added_data["entry_timestamp"], DummyTimestamp)
        self.assertIsInstance(added_data["exit_timestamp"], DummyTimestamp)
        self.assertEqual(added_data["entry_timestamp"].isoformat(), DummyTimestamp.from_datetime(entry_data["entry_timestamp"]).isoformat())
        self.assertEqual(added_data["exit_timestamp"].isoformat(), DummyTimestamp.from_datetime(entry_data["exit_timestamp"]).isoformat())
        self.assertIn("created_at", added_data)
        self.assertEqual(added_data["created_at"], firestore.SERVER_TIMESTAMP)


    def test_add_trade_entry_no_db(self):
        """
        Test that add_trade_entry handles uninitialized Firestore client.
        """
        doc_id = add_trade_entry(None, {})
        self.assertIsNone(doc_id)
        self.mock_st_error.assert_called_once_with("Firestore client not initialized. Cannot add trade entry.")


    @patch('google.cloud.firestore.Client')
    # Removed the patch for firestore.Timestamp here, as it's now patched in setUp
    def test_get_trade_entries_success(self, mock_firestore_client):
        """
        Test that get_trade_entries successfully retrieves entries.
        """
        mock_db = mock_firestore_client.return_value
        mock_collection = mock_db.collection.return_value
        
        # Mocking stream() to return a list of mock documents
        mock_doc1 = MagicMock()
        mock_doc1.id = "doc1"
        mock_doc1.to_dict.return_value = {
            "symbol": "GOOG",
            "created_at": DummyTimestamp.from_datetime(datetime(2023, 2, 1, 9, 0, 0, tzinfo=timezone.utc)),
            "entry_timestamp": DummyTimestamp.from_datetime(datetime(2023, 2, 1, 10, 0, 0, tzinfo=timezone.utc))
        }
        mock_doc2 = MagicMock()
        mock_doc2.id = "doc2"
        mock_doc2.to_dict.return_value = {
            "symbol": "MSFT",
            "created_at": DummyTimestamp.from_datetime(datetime(2023, 2, 2, 10, 0, 0, tzinfo=timezone.utc)),
            "exit_timestamp": DummyTimestamp.from_datetime(datetime(2023, 2, 2, 11, 0, 0, tzinfo=timezone.utc))
        }
        
        # Mock the entire chain: collection().order_by().limit().stream()
        mock_stream_result = [mock_doc1, mock_doc2]
        mock_query_obj = MagicMock()
        mock_query_obj.stream.return_value = mock_stream_result
        mock_query_obj.limit.return_value = mock_query_obj # For chaining
        mock_collection.order_by.return_value = mock_query_obj # For chaining

        entries = get_trade_entries(mock_db, limit=2)

        mock_db.collection.assert_called_once_with("journal_entries")
        mock_collection.order_by.assert_called_once_with("created_at", direction=self.mock_firestore_query.DESCENDING)
        mock_query_obj.limit.assert_called_once_with(2)
        mock_query_obj.stream.assert_called_once() # Assert stream was called
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["id"], "doc1")
        self.assertIsInstance(entries[0]["created_at"], datetime)
        self.assertIsInstance(entries[0]["entry_timestamp"], datetime)
        self.assertIsInstance(entries[1]["created_at"], datetime)
        self.assertIsInstance(entries[1]["exit_timestamp"], datetime)
        self.mock_st_error.assert_not_called()


    def test_add_trade_entry_no_db(self):
        """
        Test that add_trade_entry handles uninitialized Firestore client.
        """
        doc_id = add_trade_entry(None, {})
        self.assertIsNone(doc_id)
        self.mock_st_error.assert_called_once_with("Firestore client not initialized. Cannot add trade entry.")


    @patch('google.cloud.firestore.Client')
    def test_get_trade_entries_exception(self, mock_firestore_client):
        """
        Test that get_trade_entries handles exceptions during retrieval.
        """
        mock_db = mock_firestore_client.return_value
        mock_db.collection.side_effect = Exception("Firestore error")

        entries = get_trade_entries(mock_db)
        self.assertEqual(entries, [])
        self.mock_st_error.assert_called_once_with("Error retrieving trade entries: Firestore error")


if __name__ == '__main__':
    unittest.main()
