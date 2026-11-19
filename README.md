# ERP E2E Automation Framework

A portfolio project demonstrating UI automation for ERP workflows using Python, Playwright and Pytest. It includes a small local demo ERP application so the tests can run without access to a third-party website.

## Tech stack

- Python
- Playwright (synchronous API)
- Pytest
- Page Object Model (POM)
- Allure
- GitHub Actions

## Application features

- Demo login
- Customer creation and search
- Product creation and inventory
- Invoice calculation with GST
- Invoice persistence during the browser session
- Validation for invalid data and insufficient stock

## Architecture

`tests/` contains test scenarios. `pages/` contains page objects and locators. `config/` centralizes environment settings. `utils/` contains reusable test-data helpers. `app/` is the local application under test.

## Setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

After activation, install the project dependencies and browser:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Run tests

By default, the test fixture starts the local demo application on an available port and shuts it down after the test session. Set `BASE_URL` to target an already-running instance instead.

```bash
python -m pytest -v
python -m pytest -m smoke
python -m pytest -m regression
python -m pytest -m negative
python -m pytest -m api
python -m pytest tests/ui/test_invoices.py -v
```

Run with a visible browser:

**Windows PowerShell**
```powershell
$env:HEADLESS="false"
python -m pytest -m ui -s
```

**macOS/Linux**
```bash
HEADLESS=false python -m pytest -m ui -s
```

Failed UI tests save Playwright traces under `test-results/` and attach traces and screenshots to Allure results. CI uploads these with the JUnit and Allure result files.

## Allure report

```bash
python -m pytest --alluredir=allure-results
allure serve allure-results
```

Install the Allure command-line tool separately to use `allure serve`.

## Configuration

Defaults are in `config/settings.py`. Override them using environment variables:

- `BASE_URL`
- `APP_USERNAME`
- `APP_PASSWORD`
- `HEADLESS`
- `DEFAULT_TIMEOUT`

## Important scope note

This is a deliberately small demo application, not a production ERP. It uses browser memory for its sample data and is intended to demonstrate test architecture and business-flow automation. For a production-grade extension, add a real backend/database, API contract tests, role-based access tests, audit trails, tax-rule edge cases, and database/API test-data setup and cleanup.

## Suggested next improvements

1. Add tax, currency-rounding and discount boundary scenarios.
2. Add a Chromium, Firefox and WebKit CI matrix.
3. Add Allure business-flow steps and environment metadata.
4. Add API contract and authorization tests if a backend is introduced.
