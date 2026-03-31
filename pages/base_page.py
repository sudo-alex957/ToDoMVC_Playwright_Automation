from typing import Type, TypeVar

from playwright.sync_api import Locator, Page, expect

from utils import get_logger

T = TypeVar("T", bound="BasePage")


class PageFactory:
    """Creates page objects that share the same underlying Playwright Page."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def get_page(self, page_class: Type[T]) -> T:
        return page_class(self.page)

    def __call__(self, page_class: Type[T]) -> T:
        return self.get_page(page_class)


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def goto(self, url: str) -> None:
        self.logger.info(f"Navigating to {url}")
        self.page.goto(url)

    def click(self, selector: str) -> None:
        self.logger.info(f"Clicking '{selector}'")
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str) -> None:
        self.logger.info(f"Filling '{selector}' with '{text}'")
        self.page.locator(selector).fill(text)

    def press(self, selector: str, key: str) -> None:
        self.logger.info(f"Pressing '{key}' on '{selector}'")
        self.page.locator(selector).press(key)

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def expect_visible(self, selector: str) -> None:
        self.logger.info(f"Expecting '{selector}' to be visible")
        expect(self.page.locator(selector)).to_be_visible()

