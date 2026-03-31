from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class TodoPage(BasePage):
    DEFAULT_URL = "https://demo.playwright.dev/todomvc/#/"

    NEW_TODO_INPUT = ".new-todo"
    TODO_ITEMS = ".todo-list li"
    TODO_LABELS = ".todo-list li label"
    TODO_COUNT = ".todo-count"
    FILTER_ALL = "a[href='#/']"
    FILTER_ACTIVE = "a[href='#/active']"
    FILTER_COMPLETED = "a[href='#/completed']"

    def __init__(self, page: Page):
        self.page = page
        super().__init__(page)
        self.url = self.DEFAULT_URL

    def open(self) -> None:
        self.logger.info("Opening TodoMVC page")
        self.goto(self.url)
        self.expect_visible(self.NEW_TODO_INPUT)

    def add_todo(self, text: str) -> None:
        self.logger.info(f"Adding todo: '{text}'")
        field = self.page.get_by_placeholder("What needs to be done?")
        field.fill(text)
        field.press("Enter")

    def toggle_todo(self, text: str) -> None:
        self.logger.info(f"Toggling todo: '{text}'")
        item = self.page.get_by_test_id("todo-item").filter(has_text=text)
        checkbox = item.get_by_role("checkbox", name="Toggle Todo")
        checkbox.check()

    def delete_todo(self, text: str) -> None:
        self.logger.info(f"Deleting todo: '{text}'")
        todo_items = self.page.get_by_test_id("todo-item")
        job_item = todo_items.filter(has_text=text)
        job_item.hover()
        job_item.get_by_role("button", name="Delete").click()

    def click_all_filter(self) -> None:
        self.logger.info("Clicking 'All' filter")
        all_filter = self.page.get_by_role("link", name="All", exact=True)
        all_filter.click()

    def click_active_filter(self) -> None:
        self.logger.info("Clicking 'Active' filter")
        active_filter = self.page.get_by_role("link", name="Active", exact=True)
        active_filter.click()

    def click_completed_filter(self) -> None:
        self.logger.info("Clicking 'Completed' filter")
        completed_filter = self.page.get_by_role("link", name="Completed", exact=True)
        completed_filter.click()

    def get_visible_todo_texts(self) -> list[str]:
        #texts = self.locator(self.TODO_LABELS).all_inner_texts()
        texts = self.page.get_by_test_id("todo-item").all_inner_texts()
        self.logger.info(f"Visible todos: {texts}")
        return texts

    def expect_todo_visible(self, text: str) -> None:
        self.logger.info(f"Expecting todo visible: '{text}'")
        item = self.page.get_by_test_id("todo-item").filter(has_text=text)
        expect(item).to_be_visible()

    def expect_todo_not_visible(self, text: str) -> None:
        self.logger.info(f"Expecting todo not visible: '{text}'")
        item = self.page.get_by_test_id("todo-item").filter(has_text=text)
        expect(item).to_have_count(0)


