import os
import pytest
import allure
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
def page(browser, request):
    context = browser.new_context()
    page = context.new_page()

    console_logs = []
    page_errors = []

    def handle_console(msg):
        console_logs.append(f"{msg.type.upper()}: {msg.text}")

    def handle_page_error(exc):
        page_errors.append(str(exc))

    page.on("console", handle_console)
    page.on("pageerror", handle_page_error)

    request.node.console_logs = console_logs
    request.node.page_errors = page_errors

    yield page
    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)


@pytest.fixture(autouse=True)
def attach_artifacts_on_failure(request, page):
    yield
    

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="failure-screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

        allure.attach(
            page.url or "No URL available",
            name="failure-url",
            attachment_type=allure.attachment_type.TEXT,
        )

        allure.attach(
            page.content(),
            name="page-html",
            attachment_type=allure.attachment_type.HTML,
        )

        console_text = "\n".join(getattr(request.node, "console_logs", [])) or "No console logs captured."
        allure.attach(
            console_text,
            name="browser-console",
            attachment_type=allure.attachment_type.TEXT,
        )

        page_error_text = "\n".join(getattr(request.node, "page_errors", [])) or "No page errors captured."
        allure.attach(
            page_error_text,
            name="page-errors",
            attachment_type=allure.attachment_type.TEXT,
        )