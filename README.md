# Trader Companion MVP

This is the Minimum Viable Product for the Trader Companion application, focusing initially on a Position Sizing Tool.

## Setup and Run Instructions

To set up and run this application locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/blairmichaelg/fun-dead-trader.git
    cd fun-dead-trader/trader_companion_app
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows:
    .\.venv\Scripts\activate
    # On macOS/Linux:
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    This will open the application in your default web browser.

## Google Cloud Firestore Setup

This application uses Google Cloud Firestore for trade journaling. To enable this feature, you need to set up Google Cloud Platform (GCP) service account credentials.

### For Local Development

1.  **Download your GCP service account key:**
    *   Go to the Google Cloud Console.
    *   Navigate to `IAM & Admin` -> `Service Accounts`.
    *   Select your service account (or create a new one with `Firestore User` role).
    *   Click on `Keys` -> `Add Key` -> `Create new key` -> `JSON`.
    *   Download the JSON file.
2.  **Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:**
    *   Point this environment variable to the path of the downloaded JSON key file.
    *   **On Windows (Command Prompt):**
        ```bash
        set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json"
        ```
    *   **On Windows (PowerShell):**
        ```powershell
        $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json"
        ```
    *   **On macOS/Linux:**
        ```bash
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
        ```
    *   Ensure this variable is set in the terminal session *before* running `streamlit run app.py`.

### For Deployment on Streamlit Community Cloud

1.  **Open your service account key JSON file** (the one you downloaded for local development).
2.  **Copy the entire content** of the JSON file.
3.  **Go to your Streamlit app's settings** on Streamlit Community Cloud.
4.  **Navigate to `Secrets`** and add a new secret named `gcp_service_account`.
5.  **Paste the entire JSON content** into the value field for `gcp_service_account`. Streamlit will automatically parse this as a TOML table.
    *   **Important:** Ensure the key `gcp_service_account` is used exactly as shown, as the application expects this name.

## Deployed Application

You can access the live deployed application here:
[https://fun-dead-trader.streamlit.app/](https://fun-dead-trader.streamlit.app/)

## Usage

Navigate to the "📊 Position Sizing Tool" in the sidebar. Enter your account balance, risk percentage, entry price, and stop-loss price, then select your trade direction (Long/Short) and click "Calculate Position Size" to see the results.
