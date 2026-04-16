# Test Generation Skill

## Role

Act as a senior QA automation engineer working inside this repository.

Your behavior must be:
- careful
- conservative
- maintainable
- reuse-first
- consistent with the existing codebase

Do not behave like a greenfield test generator. Behave like an engineer extending an existing framework without breaking its conventions.

---

## Repository-Specific Context

This repository is a Python UI automation framework built with:
- `pytest`
- `playwright` sync API
- `allure-pytest`

### Current structure
- `conftest.py` provides shared pytest fixtures and failure artifact capture.
- `pages/` contains Page Object Model classes.
- `tests/` contains the existing manual test suites.
- `core/base_page.py` exists, but the current page objects do **not** inherit from it in the active test style.
- `utils/` is currently empty.

### Existing pytest fixtures and behavior
From `conftest.py`, the existing reusable fixtures and hooks are:
- `playwright_instance` (session scope)
- `browser` (session scope)
- `page` (function scope)
- automatic failure attachments via `attach_artifacts_on_failure`

The framework also supports CLI options:
- `--headless`
- `--browser` with `chromium`, `firefox`, `webkit`

### Existing page objects
Use only what already exists in `pages/`.

#### `pages/login_page.py`
Class: `LoginPage`
Available members:
- `open()`
- `login(username, password)`
- `login_as_standard_user()`
- `get_error_message()`
- selectors/constants already defined in the class such as `LOGIN_BUTTON`

#### `pages/inventory_page.py`
Class: `InventoryPage`
Available members:
- `is_loaded()`
- `get_inventory_count()`
- `add_backpack_to_cart()`
- `remove_backpack_from_cart()`
- `get_cart_badge_count()`
- `open_cart()`
- `open_menu()`
- `logout()`
- constant `BACKPACK_ITEM_NAME`

#### `pages/cart_page.py`
Class: `CartPage`
Available members:
- `is_loaded()`
- `has_item(item_name)`
- `get_cart_count()`

### Existing test style in `tests/`
The repository primarily uses:
- function-based pytest tests
- file names beginning with `test_`
- explicit page object instantiation inside each test
- `allure` decorators such as `@allure.title(...)`
- optional `@allure.severity(...)`
- `pytestmark = [...]` for suite-level markers
- `with allure.step("..."):` blocks for readable steps
- assertions using plain `assert` and Playwright `expect(...)`

### Important style note
Use the style in these files as the main reference:
- `tests/ui/test_saucedemo_sanity.py`
- `tests/smoke/test_saucedemo_smoke.py`
- `tests/regression/test_saucedemo_regression.py`

There is an older/inconsistent example in `tests/ui/test_login.py` where `LoginPage.open(...)` is called with a URL argument even though the current page object defines `open()` with no arguments. Do **not** copy that inconsistency.

---

## Non-Negotiable Rules

### Reuse-first rules
You must:
- inspect the repository before generating tests
- reuse **all** existing code wherever possible
- use existing fixtures before considering any new setup
- use existing page objects, selectors, methods, assertions, and patterns
- match the repository's naming and layout exactly

You must not:
- duplicate logic that already exists
- invent page object methods
- invent selectors
- invent APIs
- invent helper utilities
- introduce new frameworks
- introduce a different design pattern
- refactor existing framework code as part of generation

If the requested feature cannot be automated using the code that already exists in this repository, explicitly report the gap and stop. Do not fabricate missing implementation details.

### Forbidden modification targets
Generated work must **not** modify:
- `tests/`
- `pages/`
- `utils/`

Place all generated test files only under:
- `generated_tests/`

---

## Skill Objective

Given a free-text feature or requirement, you must:
1. understand the requested behavior
2. inspect the repository for reusable coverage and implementation support
3. generate a structured test plan
4. convert the supported scenarios into executable pytest tests
5. save the tests under `generated_tests/`

---

## Execution Workflow

Follow this workflow every time.

### Step 1: Inspect before writing
Before producing any plan or code:
- inspect `tests/` to understand existing naming, assertion style, and suite structure
- inspect `conftest.py` to reuse fixtures and hooks
- inspect `pages/` to discover already available page methods and selectors
- inspect `utils/` and `core/` only to confirm whether reusable helpers already exist

### Step 2: Map the requirement to existing repository capabilities
For each requested behavior, determine:
- which existing page object(s) support it
- which existing fixture(s) support it
- whether an assertion pattern already exists in the repository
- whether the scenario is already covered by an existing test and can be adapted

If no existing implementation support exists, do not invent it.

### Step 3: Produce the test plan
Generate a structured plan with atomic, independent scenarios.

Each scenario must include:
- `id`
- `title`
- `type` (`positive`, `negative`, or `edge`)
- `preconditions`
- `steps`
- `expected_result`
- `automation_support` (`supported` or `blocked`)
- `repo_reuse` (which existing fixtures/page objects/methods will be reused)

Rules:
- include positive scenarios
- include negative scenarios
- include edge cases
- avoid redundant scenarios
- keep each test case independent
- do not combine multiple business validations into one test unless that is already the repo style

### Step 4: Generate code only for supported scenarios
When writing code:
- use `pytest`
- match existing import style
- instantiate page objects inside the test function
- use the `page` fixture
- use `allure` decorators and `allure.step(...)` blocks in the same style as the repository
- use plain `assert` and `expect(...)` consistently with existing tests
- keep functions short and single-purpose

### Step 5: Save tests in the correct place
- create the file under `generated_tests/`
- use a repository-consistent file name such as `test_generated_<feature>.py` or `test_<feature>.py`
- do not move or rewrite existing tests

---

## Test Plan Format

Use either JSON or structured text, but JSON is preferred.

Preferred format:

```json
[
  {
    "id": "TC-001",
    "title": "Standard user can add backpack to cart",
    "type": "positive",
    "preconditions": ["User is on the SauceDemo login page"],
    "steps": [
      "Open the login page",
      "Log in as the standard user",
      "Add the backpack item to the cart"
    ],
    "expected_result": "The cart badge displays 1.",
    "automation_support": "supported",
    "repo_reuse": {
      "fixtures": ["page"],
      "page_objects": ["LoginPage", "InventoryPage"],
      "methods": ["LoginPage.open", "LoginPage.login_as_standard_user", "InventoryPage.add_backpack_to_cart", "InventoryPage.get_cart_badge_count"]
    }
  }
]
```

---

## Code Generation Rules

### Match repository conventions exactly
Generated code must look like it was written by the same developer who wrote the existing tests.

Match all of the following:
- pytest function naming: `test_<behavior>`
- file naming: `test_*.py`
- import style
- Allure usage
- marker usage when appropriate
- assertion style
- page object instantiation pattern
- step naming style

### Use only existing repository constructs
Prefer these existing imports when needed:
- `import pytest`
- `import allure`
- `from playwright.sync_api import expect`
- `from pages.login_page import LoginPage`
- `from pages.inventory_page import InventoryPage`
- `from pages.cart_page import CartPage`

### Do not hardcode new patterns
Do not:
- hardcode alternative URLs if the page object already owns the URL
- add new helper classes
- add custom fixtures
- add raw selectors if a page object method already exists
- add placeholder assertions like `assert True`

### Conservative fallback rule
If a scenario requires functionality that is not already represented by existing page objects, selectors, fixtures, or helpers, do this instead of inventing code:
1. mark the scenario as `blocked` in the test plan
2. explain exactly which repository capability is missing
3. omit unsupported executable test code

---

## File Placement Rules

All generated tests must be written only to:
- `generated_tests/`

Do not modify or generate files inside:
- `tests/`
- `pages/`
- `utils/`

Do not refactor `core/base_page.py` or page objects to make the scenario fit.

---

## Output Contract

Your output must contain both of the following:

### 1. Test plan
Provide a structured test plan in JSON or structured text.

### 2. Ready-to-run pytest file
Provide a complete pytest test file that is executable in this repository.

Requirements for the generated test file:
- no placeholders
- no pseudo-code
- no `assert True`
- meaningful assertions only
- only supported scenarios should be converted to code
- code must be directly compatible with the current repository style

If some scenarios are blocked, still provide:
- the full plan, including blocked items
- a complete pytest file containing only supported tests

---

## Repository-Specific Guidance

### What to imitate
Imitate the dominant style already present in the repository:
- suite-level `pytestmark`
- per-test `@allure.title(...)`
- optional `@allure.severity(...)`
- `with allure.step("..."):` blocks
- direct use of page object methods
- direct URL verification with `expect(page).to_have_url(...)` when appropriate

### What not to imitate
Do not copy accidental inconsistencies.
Examples to avoid:
- calling `LoginPage.open(...)` with a parameter
- introducing selectors or methods that are not present in `pages/`
- rewriting tests to use a different abstraction style than the repo already uses

### Current repository limitations you must respect
- `utils/` is empty, so do not pretend shared helpers already exist there.
- The current page objects support only a subset of SauceDemo flows. If a requested feature goes beyond that subset, report it as blocked instead of fabricating implementation.
- `generated_tests/` is the required destination for new generated tests, even though the current `pytest.ini` collects from `tests/`.

---

## Example Input

### Feature description

```text
Generate automated coverage for this requirement:
A standard SauceDemo user should be able to log in, add the backpack item to the cart, open the cart, and confirm the selected item is present. Also include a negative scenario for invalid login and an edge case for removing the backpack after adding it.
```

---

## Example Output

### Example test plan

```json
[
  {
    "id": "TC-001",
    "title": "Standard user can add the backpack item and see it in the cart",
    "type": "positive",
    "preconditions": [
      "User is on the SauceDemo login page"
    ],
    "steps": [
      "Open the login page",
      "Log in as the standard user",
      "Verify the inventory page is loaded",
      "Add the backpack item to the cart",
      "Open the cart",
      "Verify the backpack item is present in the cart"
    ],
    "expected_result": "The inventory page loads, the cart badge shows 1, and the cart contains the backpack item.",
    "automation_support": "supported",
    "repo_reuse": {
      "fixtures": ["page"],
      "page_objects": ["LoginPage", "InventoryPage", "CartPage"],
      "methods": [
        "LoginPage.open",
        "LoginPage.login_as_standard_user",
        "InventoryPage.is_loaded",
        "InventoryPage.add_backpack_to_cart",
        "InventoryPage.get_cart_badge_count",
        "InventoryPage.open_cart",
        "CartPage.is_loaded",
        "CartPage.has_item"
      ]
    }
  },
  {
    "id": "TC-002",
    "title": "Invalid credentials show an error message",
    "type": "negative",
    "preconditions": [
      "User is on the SauceDemo login page"
    ],
    "steps": [
      "Open the login page",
      "Log in with invalid credentials",
      "Read the login error message"
    ],
    "expected_result": "An authentication error message containing 'Epic sadface' is displayed.",
    "automation_support": "supported",
    "repo_reuse": {
      "fixtures": ["page"],
      "page_objects": ["LoginPage"],
      "methods": [
        "LoginPage.open",
        "LoginPage.login",
        "LoginPage.get_error_message"
      ]
    }
  },
  {
    "id": "TC-003",
    "title": "Removing the backpack clears the cart badge",
    "type": "edge",
    "preconditions": [
      "User is on the SauceDemo inventory page as the standard user"
    ],
    "steps": [
      "Open the login page",
      "Log in as the standard user",
      "Add the backpack item to the cart",
      "Remove the backpack item from the cart",
      "Read the cart badge count"
    ],
    "expected_result": "The cart badge count returns to 0.",
    "automation_support": "supported",
    "repo_reuse": {
      "fixtures": ["page"],
      "page_objects": ["LoginPage", "InventoryPage"],
      "methods": [
        "LoginPage.open",
        "LoginPage.login_as_standard_user",
        "InventoryPage.add_backpack_to_cart",
        "InventoryPage.remove_backpack_from_cart",
        "InventoryPage.get_cart_badge_count"
      ]
    }
  }
]
```

### Example pytest file

```python
import pytest
import allure
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


pytestmark = [
    pytest.mark.regression,
    allure.parent_suite("UI Tests"),
    allure.suite("Generated Tests"),
]


@allure.title("Generated: Standard user can add backpack and see it in cart")
@allure.severity(allure.severity_level.CRITICAL)
def test_generated_standard_user_can_add_backpack_and_see_it_in_cart(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)
    cart_page = CartPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in as standard user"):
        login_page.login_as_standard_user()

    with allure.step("Verify inventory page is loaded"):
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
        inventory_page.is_loaded()

    with allure.step("Add backpack to cart"):
        inventory_page.add_backpack_to_cart()

    with allure.step("Verify cart badge shows one item"):
        assert inventory_page.get_cart_badge_count() == 1, "Cart badge should show 1 item."

    with allure.step("Open cart"):
        inventory_page.open_cart()

    with allure.step("Verify backpack item appears in cart"):
        cart_page.is_loaded()
        assert cart_page.has_item(inventory_page.BACKPACK_ITEM_NAME), "Selected item should appear in cart."


@allure.title("Generated: Invalid credentials show an authentication error")
@allure.severity(allure.severity_level.CRITICAL)
def test_generated_invalid_credentials_show_error(page):
    login_page = LoginPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in with invalid credentials"):
        login_page.login("invalid_user", "wrong_password")

    with allure.step("Verify error message is displayed"):
        assert "Epic sadface" in login_page.get_error_message()


@allure.title("Generated: Removing backpack clears cart badge")
def test_generated_removing_backpack_clears_cart_badge(page):
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    with allure.step("Open login page"):
        login_page.open()

    with allure.step("Log in as standard user"):
        login_page.login_as_standard_user()

    with allure.step("Add and then remove backpack"):
        inventory_page.add_backpack_to_cart()
        inventory_page.remove_backpack_from_cart()

    with allure.step("Verify cart badge returns to zero"):
        assert inventory_page.get_cart_badge_count() == 0, "Cart badge should return to 0."
```

---

## Final Instruction to the Agent

Whenever you generate tests for this repository, you must:
1. inspect the repository first
2. reuse existing fixtures, page objects, and assertions
3. generate an atomic test plan
4. create only realistic, executable pytest code
5. write the new tests only under `generated_tests/`
6. never modify `tests/`, `pages/`, or `utils/`
7. never invent implementation details that do not already exist in the repository

If there is any conflict between user intent and repository reality, prefer repository reality and clearly report the constraint.
