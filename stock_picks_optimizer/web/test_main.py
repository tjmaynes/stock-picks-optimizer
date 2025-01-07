import pytest
from playwright.sync_api import Page

from stock_picks_optimizer.helpers.process import StockPicksOptimizerModuleRunner


def get_server_url(path: str) -> str:
    return "http://localhost:9080{}".format(path)


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    module_runner = StockPicksOptimizerModuleRunner(["web", "--port", "9080"])

    yield

    module_runner.stop()


def test_index_should_return_default_stock_group(page: Page):
    page.goto(get_server_url("/"))
    assert page.get_by_text("Default")
    # #click on sign button
    # page.click('#signin')
    # #select Username
    # page.get_by_text("Select Username").click()
    # page.locator("#react-select-2-option-0-0").click()
    # #select Password
    # page.get_by_text("Select Password").click()
    # page.locator("#react-select-3-option-0-0").click()
    # #click login
    # page.get_by_role("button", name="Log In").click()
    # #verify user have logged in
    # assert page.get_by_text("demouser").is_visible()
