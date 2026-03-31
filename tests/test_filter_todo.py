import pytest
from utils import get_logger, load_test_data

logger = get_logger("tests.test_filter_todo")


def data(test_name: str) -> list[dict]:
    """Load YAML iterations for a given test function from test_filter_todo.yaml."""
    return load_test_data(__file__, test_name)


class TestTodoCompletion:
    """Setup: open page → Tests: verify filters with parametrized data → Teardown: close context."""

    @pytest.fixture(autouse=True, scope="class")
    def setup(self, todo_page):
        logger.info("Setup: opening page and preparing completion test data")
        todo_page.open()
        todo_page.add_todo("Active task")
        todo_page.add_todo("Completed task")
        yield
        logger.info("Teardown: TestTodoCompletion complete")

    @pytest.mark.WRITE
    @pytest.mark.regression
    @pytest.mark.front_end
    @pytest.mark.parametrize("iteration", data("test_completed_item_appears_in_completed_view"),
                             ids=lambda it: it["test_id"])
    def test_completed_item_appears_in_completed_view(self, todo_page, iteration):
        logger.info(f"Starting test: {iteration['test_name']}")
        todo_page.toggle_todo(iteration["completed"])
        todo_page.click_completed_filter()
        todo_page.expect_todo_visible(iteration["completed"])
        todo_page.expect_todo_not_visible(iteration["active"])

    @pytest.mark.WRITE
    @pytest.mark.regression
    @pytest.mark.front_end
    @pytest.mark.parametrize("iteration", data("test_active_filter_shows_only_not_completed_items"),
                             ids=lambda it: it["test_id"])
    def test_active_filter_shows_only_not_completed_items(self, todo_page, iteration):
        logger.info(f"Starting test: {iteration['test_name']}")
        todo_page.click_active_filter()
        todo_page.expect_todo_visible(iteration["active"])
        todo_page.expect_todo_not_visible(iteration["completed"])

    @pytest.mark.WRITE
    @pytest.mark.regression
    @pytest.mark.front_end
    @pytest.mark.parametrize("iteration", data("test_completed_filter_shows_only_completed_items"),
                             ids=lambda it: it["test_id"])
    def test_completed_filter_shows_only_completed_items(self, todo_page, iteration):
        logger.info(f"Starting test: {iteration['test_name']}")
        todo_page.click_completed_filter()
        assert todo_page.get_visible_todo_texts() == [iteration["completed"]]