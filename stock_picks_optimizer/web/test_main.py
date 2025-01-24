import pytest
from playwright.sync_api import Page

from stock_picks_optimizer.helpers.process import StockPicksOptimizerModuleRunner


def get_server_url(path: str) -> str:
    return "http://localhost:9999{}".format(path)


@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    module_runner = StockPicksOptimizerModuleRunner(["web", "--port", "9999"])

    yield

    module_runner.stop()


def test_index_should_return_default_stock_group(page: Page):
    page.goto(get_server_url("/"))
    assert page.get_by_text("Default")
    # assert page.is_visible("text='Default'")


# def test_index_should_redirect_to_add_group_page_when_add_group_clicked(
#     page: Page,
# ):
#     page.goto(get_server_url("/"))
#     page.get_by_text("Add group").click()
#     page.wait_for_url(get_server_url("/add-group"))
