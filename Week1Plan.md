__Overall Goal for Week 1:__ Develop and deploy a basic Streamlit application featuring a functional Position Sizing Tool. Establish the foundational project structure, version control, and a deployment pipeline to Streamlit Community Cloud. Adhere to "Early & Continuous Delivery" and "Simplicity First" principles.

---

__1. Features to Implement (Week 1 Focus):__

- __Core Feature: Position Sizing Tool__

  - Inputs: Account Balance, Risk Percentage (e.g., 1%), Entry Price, Stop-Loss Price, Trade Direction (Long/Short).
  - Output: Calculated position size (units/shares) and the dollar amount at risk.
  - Display: Clearly show inputs, calculated size, dollar amount at risk, and total position value. Include a warning if total position value exceeds account balance (implying leverage).

- __Basic Streamlit App Structure:__

  - Multi-page app structure (`app.py` as main, tools in `pages/`).
  - Main landing page (`app.py`) with project description and navigation hints.
  - Separate page for the Position Sizer (`pages/1_📊_Position_Sizer.py`).

- __Initial Setup (as per "Optimized Blueprint for Dev Environment"):__

  - Local Python virtual environment (e.g., `.venv`).
  - Git repository on GitHub, with an appropriate `.gitignore`.
  - Deployment to Streamlit Community Cloud.
  - Basic `README.md` with setup and run instructions.

---

__2. Directory Structure & Placeholder Files (Confirming original plan):__

```javascript
trader_companion_app/
├── .streamlit/
│   └── config.toml         # Optional: For Streamlit theme, settings
├── .venv/                  # Virtual environment (in .gitignore)
├── core/
│   ├── __init__.py
│   └── position_sizer.py   # Logic for position sizing
├── pages/
│   └── 1_📊_Position_Sizer.py # Streamlit UI for the position sizer tool
├── tests/
│   ├── __init__.py
│   └── test_position_sizer.py # Unit tests for position_sizer.py
├── app.py                  # Main Streamlit landing page
├── requirements.txt        # Python dependencies (streamlit, pytest)
├── .gitignore              # Standard Python/VSCode/venv ignores
└── README.md               # Project overview, setup, run, deployment
```

*(This structure aligns with best practices and your provided plans.)*

---

__3. Python Modules/Functions to Create (Confirming original plan, minor detail added):__

- __`core/position_sizer.py`:__

  - __Function:__ `calculate_position_size(account_balance: float, risk_percentage: float, entry_price: float, stop_loss_price: float, is_long_trade: bool) -> dict`

    - Returns: `{'position_size_units': float, 'risk_amount_dollars': float, 'risk_per_unit': float}` (Returning a dict for clarity).
    - Includes robust input validation.

- __`pages/1_📊_Position_Sizer.py`:__

  - Streamlit UI elements as per your starter code.
  - Clear display of results and any warnings.
  - User-friendly error messages.

- __`app.py` (Main Landing Page):__
  - Welcome message, brief explanation, navigation instructions. `st.set_page_config` here.

- __`tests/test_position_sizer.py`:__
  - Unit tests for `calculate_position_size` covering valid long/short trades, invalid inputs, and edge cases (e.g., entry_price == stop_loss_price). Aim for good coverage.

---

__4. Cloud Setup & Streamlit Boilerplate (Confirming original plan):__

- __Local Development Environment:__

  1. Create project directory, initialize Git.
  2. Create and activate Python virtual environment (`python -m venv .venv`).
  3. Install dependencies: `pip install streamlit pytest black flake8` (adding linters).
  4. Create `requirements.txt`: `pip freeze > requirements.txt`.
  5. Create `.gitignore` (using a standard Python template, including `.venv/`, `__pycache__/`, `.vscode/`).
  6. Configure VS Code settings for Python (Pylance, Black, Flake8, formatOnSave) as per your "VS Code Configuration" document.

- __GitHub Setup:__

  1. Create new GitHub repository.
  2. Link local repo and push initial structure.

- __Streamlit Community Cloud:__
  1. Deploy from GitHub repo, main branch, `app.py` as main file.

- __Google Cloud Platform (Minimal Setup):__

  1. Create GCP Project. Note Project ID.
  2. Enable Firestore API (for Week 2 prep).
  3. Install/authenticate `gcloud` CLI locally and set default project.

---

__5. Prioritized Task List for Week 1 (Refined Time Estimates):__

1. __Setup & Configuration (1.5 - 2 hours):__

   - Project directory, Git, virtual env, `.gitignore`, `requirements.txt`.
   - VS Code linters/formatters setup.
   - Push to GitHub.
   - Initial Streamlit Community Cloud deployment (can be a placeholder `app.py`).
   - GCP project creation & Firestore API enabling.

2. __Core Logic - `core/position_sizer.py` (2 - 2.5 hours):__
   - Implement `calculate_position_size` function.

3. __Unit Tests - `tests/test_position_sizer.py` (1.5 - 2 hours):__
   - Write comprehensive unit tests. Ensure `pytest` runs and all tests pass.

4. __Streamlit UI - `app.py` & `pages/1_📊_Position_Sizer.py` (3 - 3.5 hours):__

   - Develop landing page and position sizer UI.
   - Integrate `calculate_position_size` function.
   - Ensure clear display of results and error handling.
   - Thorough local testing (`streamlit run app.py`).

5. __Deployment, README & Review (1 hour):__

   - Update `README.md` with setup, run, and basic usage instructions.
   - Push final Week 1 code to GitHub.
   - Verify deployment on Streamlit Community Cloud.
   - Brief self-review against Week 1 goals.

__Total Estimated Time: 9 - 11 hours__ (The original <10 hours is feasible, especially with your excellent starter code).
