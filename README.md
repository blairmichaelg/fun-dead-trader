<div align="center">

# 📊 Trader Companion

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.45+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**A professional-grade trading companion application designed to help traders manage risk, track trades, and analyze performance.**

[Live Demo](https://fun-dead-trader.streamlit.app/) · [Report Bug](https://github.com/blairmichaelg/fun-dead-trader/issues) · [Request Feature](https://github.com/blairmichaelg/fun-dead-trader/issues)

</div>

---

## ✨ Features

- **📐 Position Size Calculator**: Calculate optimal position sizes based on account balance, risk percentage, and stop-loss levels
- **📝 Trade Journal**: Record and document all your trades with detailed entry/exit timestamps and notes
- **📈 Performance Dashboard**: Visualize trading performance with key metrics including win rate, total P&L, and trade history
- **☁️ Cloud Persistence**: Seamless integration with Google Cloud Firestore for reliable data storage
- **🎨 Intuitive UI**: Clean, responsive interface built with Streamlit for an excellent user experience
- **🔐 Secure**: Industry-standard authentication and data security practices

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Interactive web application framework
- **Backend**: [Python 3.8+](https://www.python.org/) - Core application logic
- **Database**: [Google Cloud Firestore](https://cloud.google.com/firestore) - NoSQL cloud database
- **Data Processing**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Visualization**: [Altair](https://altair-viz.github.io/)
- **Testing**: [pytest](https://pytest.org/)
- **Code Quality**: [black](https://github.com/psf/black), [flake8](https://flake8.pycqa.org/)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Cloud Platform account (for Firestore integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/blairmichaelg/fun-dead-trader.git
   cd fun-dead-trader
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv .venv
   .\.venv\Scripts\activate

   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud Firestore** (Optional but recommended)
   
   See the [Firestore Setup](#firestore-setup) section below for detailed instructions.

5. **Run the application**
   ```bash
   streamlit run app.py
   ```
   
   The application will open automatically in your default web browser at `http://localhost:8501`

## 🔧 Configuration

### Firestore Setup

This application uses Google Cloud Firestore for persistent storage of trade data.

#### Local Development

1. **Create a GCP service account**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Navigate to `IAM & Admin` → `Service Accounts`
   - Create a new service account with `Firestore User` role
   - Generate and download a JSON key file

2. **Set environment variable**:
   ```bash
   # Windows (Command Prompt)
   set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json"

   # Windows (PowerShell)
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json"

   # macOS/Linux
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
   ```

#### Streamlit Cloud Deployment

1. Copy the entire contents of your service account JSON file
2. In your Streamlit Cloud app settings, navigate to `Secrets`
3. Add a secret named `gcp_service_account` and paste the JSON content

## 📖 Usage

### Position Sizing Tool

1. Navigate to **📊 Position Sizing Tool** in the sidebar
2. Enter your account balance and risk percentage
3. Input entry price and stop-loss price
4. Select trade direction (Long/Short)
5. Click **Calculate Position Size** to get results

### Trade Journal

1. Go to **✍️ Trade Journal** page
2. Fill in trade details (symbol, direction, prices, size)
3. Add entry and exit timestamps
4. Include any relevant notes
5. Submit to save the trade

### Dashboard

View your trading performance metrics including:
- Total number of trades
- Cumulative P&L
- Win rate percentage
- Detailed trade history

## 🧪 Testing

Run the test suite with pytest:

```bash
pytest tests/
```

Run tests with coverage:

```bash
pytest --cov=core tests/
```

## 🤝 Contributing

We welcome contributions from the community! Please read our [Contributing Guidelines](CONTRIBUTING.md) to get started.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📋 Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Cloud Platform](https://cloud.google.com/)
- Inspired by the trading community

## 📞 Contact

**Project Maintainer**: Blair Michael G

**Project Link**: [https://github.com/blairmichaelg/fun-dead-trader](https://github.com/blairmichaelg/fun-dead-trader)

**Live Demo**: [https://fun-dead-trader.streamlit.app/](https://fun-dead-trader.streamlit.app/)

---

<div align="center">
Made with ❤️ by the trading community
</div>
