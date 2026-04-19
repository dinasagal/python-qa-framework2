# Test Generation From Plan Skill

## Role

Act as a senior QA automation engineer focused **only** on generating executable tests from an existing plan in `listOfTests.txt`.

This skill must:
- receive a feature description
- find the matching plan block in `listOfTests.txt`
- generate pytest tests that match repository style
- save generated tests under `generated_tests/`

---

## Required Plan Lookup Rule

Use **exact short feature name match** against the `FEATURE:` field.

Lookup algorithm:
1. Read `listOfTests.txt`.
2. Find the line matching exactly: `FEATURE: <short feature name>`.
3. Read the block including `DESCRIPTION:`, `PLAN_TYPE:`, and all tests until `END FEATURE`.
4. Use `DESCRIPTION:` for context only — it does not affect lookup.
5. If no exact `FEATURE:` match exists, stop and report: `No exact FEATURE match found in listOfTests.txt for: <input>`.

Do not match on `DESCRIPTION:`.
Do not use fuzzy matching.
Do not use a different feature block.

---

## Repository Awareness

Before generating tests, inspect and reuse existing project structure:
- `conftest.py` fixtures and hooks
- `pages/` page objects
- `flows/` shared journeys (`login_standard_user_to_inventory`, etc.)
- `config/settings.py` centralized URLs/credentials
- current style in `tests/smoke/`, `tests/ui/`, `tests/regression/`
- marker design in `pytest.ini`

---

## Non-Negotiable Code Rules

You must:
- generate pytest tests that look like current repository tests
- reuse existing page objects, flows, fixtures, and assertion patterns
- use meaningful assertions (no placeholders)
- convert only `Support: supported` plan items into code
- keep blocked items out of executable code

You must not:
- invent new selectors, APIs, methods, fixtures, or frameworks
- modify `tests/`, `pages/`, or `utils/`
- hardcode URL/credentials when `config/settings.py`/page helpers already provide them

Generated files must be created only in:
- `generated_tests/`

---

## Implementation Workflow

1. Receive feature text.
2. Find exact `FEATURE:` block in `listOfTests.txt`.
3. Parse test items and keep only `Support: supported`.
4. Map each supported item to existing methods/flows.
5. Generate a ready-to-run `test_*.py` file under `generated_tests/`.

If all items are blocked, do not generate a test file; report blocked reasons.

---

## Style Requirements (Match Existing Repo)

- function-based tests: `test_<behavior>`
- imports typically include:
  - `pytest`
  - `allure`
  - `expect` when URL/visibility assertions are needed
  - page objects from `pages/`
  - flow helpers from `flows/` when relevant
- use `pytestmark` with suite/component/source where appropriate
- use `with allure.step("..."):` blocks
- keep tests short and single-purpose

---

## Output Requirements

Return:
1. the matched feature plan header (for traceability)
2. generated file path under `generated_tests/`
3. full executable pytest content

No pseudo-code, no `assert True`, no TODO placeholders.

---

## Example Input

```text
Feature: Product Sorting
```

## Example Behavior

1. Reads `listOfTests.txt`.
2. Finds line matching exactly: `FEATURE: Product Sorting`
3. Reads `DESCRIPTION:` for planning context.
4. Generates tests for supported cases into:
   `generated_tests/test_feature_sorting_from_plan.py`

## Example Test Snippet Style

```python
import pytest
import allure

from flows import login_standard_user_to_inventory
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


pytestmark = [
    pytest.mark.regression,
    pytest.mark.component_sort,
    pytest.mark.source_generated,
    allure.parent_suite("UI Tests"),
    allure.suite("Generated From Plan"),
]


@allure.title("Generated: Sort by price low to high")
@pytest.mark.type_positive
@pytest.mark.risk_p1
@pytest.mark.speed_fast
def test_generated_sort_price_low_to_high(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page and log in as standard user"):
        login_standard_user_to_inventory(login_page, inventory_page)

    with allure.step("Select sort low to high"):
        inventory_page.select_sort("lohi")

    with allure.step("Verify prices sorted ascending"):
        prices = inventory_page.get_item_prices()
        assert prices == sorted(prices)
```
