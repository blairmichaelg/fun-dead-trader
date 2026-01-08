# Contributing to Trader Companion

First off, thank you for considering contributing to Trader Companion! It's people like you that make this project a great tool for the trading community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
  - [Pull Requests](#pull-requests)
- [Style Guidelines](#style-guidelines)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Style Guide](#python-style-guide)
  - [Documentation Style Guide](#documentation-style-guide)
- [Development Setup](#development-setup)
- [Testing](#testing)
- [Additional Notes](#additional-notes)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up your development environment (see [Development Setup](#development-setup))
4. Create a new branch for your feature or bug fix
5. Make your changes
6. Test your changes thoroughly
7. Submit a pull request

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible using our bug report template.

**To submit a bug report:**

1. Use the bug report template in `.github/ISSUE_TEMPLATE/bug_report.md`
2. Include a clear and descriptive title
3. Describe the exact steps to reproduce the problem
4. Provide specific examples to demonstrate the steps
5. Describe the behavior you observed and what you expected to see
6. Include screenshots if applicable
7. Note your environment (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, use the feature request template and include:

1. A clear and descriptive title
2. A detailed description of the proposed feature
3. Explain why this enhancement would be useful
4. List any alternative solutions you've considered
5. Include mockups or examples if applicable

### Your First Code Contribution

Unsure where to begin? You can start by looking through `good-first-issue` and `help-wanted` issues:

- **Good first issues**: Simple issues that require only a few lines of code
- **Help wanted issues**: More involved issues that need attention

### Pull Requests

1. **Fork and clone** the repository
2. **Create a new branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our style guidelines
4. **Add tests** for any new functionality
5. **Run the test suite** to ensure all tests pass:
   ```bash
   pytest tests/
   ```
6. **Run code formatting** with black:
   ```bash
   black .
   ```
7. **Run linting** with flake8:
   ```bash
   flake8 .
   ```
8. **Commit your changes** with a descriptive message
9. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
10. **Open a Pull Request** against the `main` branch

## Style Guidelines

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` - Improving structure/format of the code
  - ⚡ `:zap:` - Improving performance
  - 🐛 `:bug:` - Fixing a bug
  - 🔥 `:fire:` - Removing code or files
  - 📝 `:memo:` - Writing docs
  - ✨ `:sparkles:` - Introducing new features
  - ✅ `:white_check_mark:` - Adding tests
  - 🔒 `:lock:` - Fixing security issues
  - ⬆️ `:arrow_up:` - Upgrading dependencies

### Python Style Guide

This project follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide with these specifics:

- **Line length**: Maximum 88 characters (Black default)
- **Indentation**: 4 spaces
- **Naming conventions**:
  - Functions and variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`
- **Imports**: Group imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application imports
- **Docstrings**: Use Google-style docstrings for all public modules, functions, classes, and methods
- **Type hints**: Use type hints for function signatures where applicable

Example:
```python
def calculate_position_size(
    account_balance: float,
    risk_percentage: float,
    entry_price: float,
    stop_loss_price: float,
    is_long_trade: bool,
) -> dict:
    """
    Calculates position size based on risk parameters.

    Args:
        account_balance: The total account balance in dollars.
        risk_percentage: The percentage of account to risk (0-100).
        entry_price: The price at which the trade will be entered.
        stop_loss_price: The price at which the stop loss is set.
        is_long_trade: True for long trades, False for short trades.

    Returns:
        A dictionary containing position_size_units, risk_amount_dollars,
        and risk_per_unit.

    Raises:
        ValueError: If any input validation fails.
    """
    # Implementation here
    pass
```

### Documentation Style Guide

- Use Markdown for documentation
- Keep line length reasonable (80-100 characters when possible)
- Use clear, concise language
- Include code examples where appropriate
- Keep documentation up-to-date with code changes

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/blairmichaelg/fun-dead-trader.git
   cd fun-dead-trader
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies** (if applicable):
   ```bash
   pip install black flake8 pytest pytest-cov
   ```

5. **Set up pre-commit hooks** (optional but recommended):
   ```bash
   # Format code before committing
   echo "black ." > .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

## Testing

We use pytest for testing. All new features should include tests.

### Running Tests

```bash
# Run all tests
pytest tests/

# Run tests with coverage
pytest --cov=core tests/

# Run specific test file
pytest tests/test_position_sizer.py

# Run tests in verbose mode
pytest -v tests/
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with the prefix `test_`
- Name test functions with the prefix `test_`
- Use descriptive test names that explain what is being tested
- Follow the Arrange-Act-Assert pattern
- Use pytest fixtures for common setup
- Aim for high test coverage (>80%)

Example:
```python
def test_calculate_position_size_valid_long_trade():
    """Test position size calculation for a valid long trade."""
    # Arrange
    account_balance = 10000
    risk_percentage = 1
    entry_price = 100
    stop_loss_price = 99
    
    # Act
    result = calculate_position_size(
        account_balance, risk_percentage, entry_price,
        stop_loss_price, is_long_trade=True
    )
    
    # Assert
    assert result["position_size_units"] == 100
    assert result["risk_amount_dollars"] == 100
```

## Additional Notes

### Issue and Pull Request Labels

This project uses labels to organize and track issues and pull requests:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested
- `wontfix` - This will not be worked on
- `duplicate` - This issue or pull request already exists

### Community

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Provide constructive feedback
- Focus on what is best for the community

### Recognition

Contributors will be recognized in the project. Major contributions may be acknowledged in release notes.

---

Thank you for contributing to Trader Companion! 🎉
