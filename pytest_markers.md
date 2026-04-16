# Pytest Marker Guide

## Purpose

This repository uses pytest markers for test selection, reporting clarity, and suite organization.

Markers are designed to be combined across multiple dimensions:
- suite
- component
- risk
- speed
- scenario type
- source

---

## Marker Taxonomy

### Suite markers
- `sanity`
- `smoke`
- `regression`

Use exactly one suite marker per test module.

### Component markers
- `component_auth`
- `component_inventory`
- `component_cart`
- `component_sort`
- `component_navigation`

Use component markers at the test level when a module contains mixed coverage.

### Risk markers
- `risk_p0` — highest business risk / must-pass path
- `risk_p1` — important but not release-blocking by default
- `risk_p2` — lower-risk coverage

### Speed markers
- `speed_fast`
- `speed_medium`
- `speed_slow`

### Scenario type markers
- `type_positive`
- `type_negative`
- `type_edge`

### Source markers
- `source_manual`
- `source_generated`

---

## Recommended Usage Pattern

### Module-level `pytestmark`
Use these at the module level:
- one suite marker
- one source marker
- Allure suite labels

Example:

```python
pytestmark = [
    pytest.mark.regression,
    pytest.mark.source_manual,
    allure.parent_suite("UI Tests"),
    allure.suite("Regression"),
]
```

### Test-level markers
Use these at the test level:
- component marker
- risk marker
- speed marker
- scenario type marker

Example:

```python
@allure.title("Regression: Sort products low to high")
@pytest.mark.component_sort
@pytest.mark.type_positive
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_sort_low_to_high(page):
    ...
```

---

## Example Selection Commands

Run smoke tests:

```powershell
.\venv\Scripts\python.exe -m pytest -m smoke
```

Run sort coverage only:

```powershell
.\venv\Scripts\python.exe -m pytest -m component_sort
```

Run only generated tests:

```powershell
.\venv\Scripts\python.exe -m pytest -m source_generated
```

Run manual regression tests only:

```powershell
.\venv\Scripts\python.exe -m pytest -m "regression and source_manual"
```

Run highest-risk coverage:

```powershell
.\venv\Scripts\python.exe -m pytest -m risk_p0
```

Run negative scenarios:

```powershell
.\venv\Scripts\python.exe -m pytest -m type_negative
```

---

## Conventions

- Prefer page-object methods over raw selectors in tests.
- Keep suite ownership stable: `tests/` contains manual suites, `generated_tests/` contains generated suites.
- Use `source_generated` for generated files under `generated_tests/`.
- Do not add new markers without registering them in `pytest.ini`.
- Keep marker usage conservative and consistent.

---

## Current Practical Rule

Because some modules cover multiple user journeys, component markers are currently applied per test rather than forcing one primary component per file.

This keeps the current suite layout intact while still enabling precise filtering.
