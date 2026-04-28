# Python QA Framework (Playwright + Pytest + Allure)

UI automation framework for SauceDemo using:
- **Pytest** for test execution
- **Playwright (sync API)** for browser automation
- **Allure** for reporting
- **Page Object Model (POM)** + reusable **flows**

---

## Tech Stack

- Python 3.11+
- pytest
- playwright
- allure-pytest
- python-dotenv

Dependencies are listed in `requirements.txt`.

---

## Project Structure

```text
.
├─ conftest.py                  # pytest fixtures, browser/page setup, failure artifacts
├─ pytest.ini                   # pytest config, markers, Allure output dir
├─ listOfTests.txt              # manual + feature plan definitions
├─ config/
│  └─ settings.py               # env-driven URLs and credentials
├─ pages/                       # page objects
│  ├─ login_page.py
│  ├─ inventory_page.py
│  ├─ cart_page.py
│  └─ product_detail_page.py
├─ flows/                       # reusable multi-step journeys
│  └─ saucedemo_flows.py
├─ tests/
│  ├─ ui/
│  ├─ smoke/
│  └─ regression/
├─ generated_tests/             # AI-generated executable tests
├─ qa_agent/skills/             # planning + generation skills
├─ allure-results/              # raw Allure results
└─ allure-report/               # generated Allure HTML report
```

---

## Local Setup (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install
```

---

## Environment Variables

The framework reads configuration from `.env` (via `python-dotenv`) or environment variables.

Create a `.env` file in project root:

```env
QA_BASE_URL=https://www.saucedemo.com/
QA_STANDARD_USERNAME=standard_user
QA_STANDARD_PASSWORD=secret_sauce
QA_LOCKED_USERNAME=locked_out_user
QA_LOCKED_PASSWORD=secret_sauce
```

Notes:
- `QA_BASE_URL` is normalized to include trailing `/`
- `inventory_url` is derived as `<base_url>inventory.html`

---

## Running Tests

### Run all tests

```powershell
pytest
```

### Run by suite marker

```powershell
pytest -m sanity
pytest -m smoke
pytest -m regression
```

### Run by component marker

```powershell
pytest -m component_auth
pytest -m component_inventory
pytest -m component_cart
pytest -m component_sort
pytest -m component_navigation
```

### Run generated tests only

```powershell
pytest generated_tests
```

### Browser options

`conftest.py` supports:
- `--browser` (`chromium`, `firefox`, `webkit`)
- `--headless`

Examples:

```powershell
pytest --browser firefox --headless
pytest -m regression --browser chromium
```

Headless is enabled when any of these are true:
- `--headless` is passed
- `HEADLESS=true`
- `CI=true`

---

## Allure Reporting

`pytest.ini` writes results to `allure-results/` automatically.

Generate and open report locally:

```powershell
allure generate allure-results --clean -o allure-report
allure open allure-report
```

If Allure CLI is missing:

```powershell
npm install -g allure-commandline --save-dev
```

---

## Marker Taxonomy

Registered markers include:
- Suites: `sanity`, `smoke`, `regression`
- Component: `component_auth`, `component_inventory`, `component_cart`, `component_sort`, `component_navigation`
- Risk: `risk_p0`, `risk_p1`, `risk_p2`
- Speed: `speed_fast`, `speed_medium`, `speed_slow`
- Type: `type_positive`, `type_negative`, `type_edge`
- Source: `source_manual`, `source_generated`

---

## CI Workflows

- `.github/workflows/ui-tests.yml`
  - Trigger: push to `main` + manual dispatch
  - Runs `pytest -m "sanity"`
  - Generates and publishes Allure report

- `.github/workflows/regression-daily.yml`
  - Trigger: daily cron (`0 2 * * *`) + manual dispatch
  - Runs `pytest -m "regression"`
  - Generates and publishes Allure report

Both workflows install Playwright browsers and populate `.env` from GitHub vars/secrets.

---

## Failure Diagnostics

On test failure, `conftest.py` automatically attaches to Allure:
- screenshot
- current URL
- page HTML
- browser console logs
- page errors

---

## AI-Assisted Test Workflow

Skills live in `qa_agent/skills/`:
- `test_plan_generation.md` — create/append feature plans to `listOfTests.txt`
- `test_generation_from_plan.md` — generate executable tests from plan blocks
- `test_generation.md` — compatibility/deprecation pointer

Generated files are created under `generated_tests/`.

---

## Add New Feature Plan + Generate Tests

Use this sequence when you want to add coverage for a new feature.

1. Choose a short feature name (2–4 words), for example: `Checkout Flow`.
2. Ask the planner skill to append a new block to `listOfTests.txt`.
3. Ask the generator skill to create executable tests from that exact `FEATURE:` block.
4. Run only the generated file first, then run the full marker suite.

### Example prompts for the agent

```text
Use qa_agent/skills/test_plan_generation.md
Feature: Checkout Flow
```

```text
Use qa_agent/skills/test_generation_from_plan.md
Feature: Checkout Flow
```

### Validate generated tests

```powershell
pytest generated_tests -q
pytest -m regression
```

### If plan items are blocked

- The generation flow runs an **Unblock Phase** for `missing POM` / `missing flow` items.
- It extends page objects or flows minimally, updates `Support: blocked` → `Support: supported`, then continues generation.

---

## Quick Start

```powershell
.\venv\Scripts\Activate.ps1
pytest -m sanity
allure generate allure-results --clean -o allure-report
```
