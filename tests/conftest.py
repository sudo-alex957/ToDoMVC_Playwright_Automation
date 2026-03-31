import base64
import os
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from pages.base_page import PageFactory
from pages.todo_page import TodoPage
from utils import get_logger

logger = get_logger("conftest")

DEFAULT_BASE_URL = "https://demo.playwright.dev/todomvc/#/"

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
TRACES_DIR = REPORTS_DIR / "traces"


def pytest_configure(config):
    """Set BASE_URL from environment or fall back to default."""
    config.base_url = os.getenv("BASE_URL", DEFAULT_BASE_URL)
    logger.info(f"BASE_URL: {config.base_url}")


@pytest.fixture(scope="session")
def base_url(request) -> str:
    """Session-scoped base URL — configurable via BASE_URL env var."""
    return request.config.base_url


@pytest.fixture(scope="session")
def playwright() -> Playwright:
    with sync_playwright() as playwright_instance:
        yield playwright_instance


@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Browser:
    headless = os.getenv("HEADLESS", "true").lower() != "false"
    slow_mo = int(os.getenv("SLOW_MO", "0"))
    logger.info(f"Launching Chromium (headless={headless}, slow_mo={slow_mo})")
    browser_instance = playwright.chromium.launch(headless=headless, slow_mo=slow_mo)
    yield browser_instance
    logger.info("Closing browser")
    browser_instance.close()


@pytest.fixture(scope="class")
def page(browser: Browser, request: pytest.FixtureRequest) -> Page:
    """Class-scoped page: one browser context per test class."""
    logger.info(f"Creating browser context for {request.node.name}")
    context = browser.new_context(viewport={"width": 1366, "height": 768})
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page_instance = context.new_page()

    yield page_instance

    failed = any(
        getattr(item, "rep_call", None) and item.rep_call.failed
        for item in request.node.collect()
    )
    if failed:
        logger.warning(f"Test failure detected in {request.node.name} — saving artifacts")
        _save_screenshot(page_instance, request.node.name)
        _save_trace(context, request.node.name)

    context.tracing.stop()
    logger.info(f"Closing browser context for {request.node.name}")
    context.close()


@pytest.fixture(scope="class")
def page_factory(page) -> PageFactory:
    """Class-scoped PageFactory: creates page objects sharing the same Playwright Page."""
    return PageFactory(page)


@pytest.fixture(scope="class")
def todo_page(page_factory, base_url) -> TodoPage:
    """Class-scoped TodoPage: created via PageFactory with configurable base URL."""
    todo = page_factory(TodoPage)
    todo.url = base_url
    return todo


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call):
    """Store test outcome on the item so the ``page`` fixture can inspect it."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: pytest.Item):
    """After the test call, embed screenshot in the HTML report on failure."""
    yield

    report = getattr(item, "rep_call", None)
    if report and report.failed:
        screenshot_path = SCREENSHOTS_DIR / f"{item.name}.png"
        if screenshot_path.exists():
            encoded = base64.b64encode(screenshot_path.read_bytes()).decode()
            if hasattr(item.config, "_html"):
                extra = getattr(report, "extras", [])
                from pytest_html import extras as html_extras

                extra.append(html_extras.png(encoded))
                report.extras = extra


def _save_screenshot(page: Page, test_name: str) -> None:
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(SCREENSHOTS_DIR / f"{test_name}.png"), full_page=True)


def _save_trace(context, test_name: str) -> None:
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=str(TRACES_DIR / f"{test_name}.zip"))


