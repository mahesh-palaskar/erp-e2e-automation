import re
import warnings
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import allure
import pytest
from playwright.sync_api import sync_playwright

from config.settings import (
    APP_PASSWORD,
    APP_USERNAME,
    BASE_URL,
    BROWSER,
    DEFAULT_TIMEOUT,
    HEADLESS,
)
from pages.login_page import LoginPage


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = PROJECT_ROOT / "app"


@pytest.fixture(scope="session")
def app_base_url():
    if BASE_URL:
        yield BASE_URL.rstrip("/")
        return

    handler = partial(SimpleHTTPRequestHandler, directory=str(APP_DIR))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    server_thread = Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server_thread.join(timeout=5)
        server.server_close()


@pytest.fixture
def logged_in_page(page, app_base_url):
    page.goto(app_base_url)
    LoginPage(page).login(APP_USERNAME, APP_PASSWORD)
    return page


@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as playwright:
        try:
            browser_type = getattr(playwright, BROWSER)
        except AttributeError as exc:
            raise ValueError(
                f"Unsupported BROWSER={BROWSER!r}; use chromium, firefox, or webkit"
            ) from exc

        browser = browser_type.launch(headless=HEADLESS)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def context(browser_instance, request):
    context = browser_instance.new_context(
        viewport={
            "width": 1440,
            "height": 900
        }
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    try:
        yield context
    finally:
        setup_report = getattr(request.node, "rep_setup", None)
        call_report = getattr(request.node, "rep_call", None)
        failed = any(
            report is not None and report.failed
            for report in (setup_report, call_report)
        )

        try:
            if failed:
                artifact_dir = PROJECT_ROOT / "test-results"
                artifact_dir.mkdir(parents=True, exist_ok=True)
                test_name = re.sub(r"[^A-Za-z0-9._-]+", "_", request.node.nodeid)
                trace_path = artifact_dir / f"{test_name}.zip"
                context.tracing.stop(path=str(trace_path))
                allure.attach.file(
                    str(trace_path),
                    name="playwright-trace",
                    attachment_type=allure.attachment_type.ZIP,
                )
                for index, page in enumerate(context.pages, start=1):
                    if not page.is_closed():
                        allure.attach(
                            page.screenshot(full_page=True),
                            name=f"failure-screenshot-{index}",
                            attachment_type=allure.attachment_type.PNG,
                        )
            else:
                context.tracing.stop()
        except Exception as exc:
            warnings.warn(f"Could not save Playwright failure artifacts: {exc}")
        finally:
            context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    page.set_default_timeout(DEFAULT_TIMEOUT)
    page.set_default_navigation_timeout(DEFAULT_TIMEOUT)

    yield page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)