import os
import pytest
from playwright.sync_api import sync_playwright


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to run tests with",
    )


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance, request):
    browser_name = request.config.getoption("--browser")
    cli_headless = request.config.getoption("--headless")

    env_headless = os.getenv("HEADLESS", "").lower() == "true"
    ci_headless = os.getenv("CI", "").lower() == "true"

    headless = cli_headless or env_headless or ci_headless

    browser_launcher = getattr(playwright_instance, browser_name)
    browser = browser_launcher.launch(headless=headless)
    yield browser
    browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()