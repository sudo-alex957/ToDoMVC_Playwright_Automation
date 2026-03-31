import pytest
from utils import get_logger, load_test_data

logger = get_logger("tests.test_delete_todo")


def data(test_name: str) -> list[dict]:
    """Load YAML iterations for a given test function from test_delete_todo.yaml."""
    return load_test_data(__file__, test_name)


class TestDeleteTodo:
    """Setup: open page → Test: delete and verify absence → Teardown: close context."""

    @pytest.fixture(autouse=True, scope="class")
    def setup(self, todo_page):
        logger.info("Setup: opening TodoMVC page")
        todo_page.open()
        yield
        logger.info("Teardown: TestDeleteTodo complete")

    @pytest.mark.WRITE
    @pytest.mark.regression
    @pytest.mark.front_end
    @pytest.mark.parametrize("iteration", data("test_deleted_todo_does_not_appear_in_any_view"),
                             ids=lambda it: it["test_id"])
    def test_deleted_todo_does_not_appear_in_any_view(self, todo_page, iteration):
        logger.info(f"Starting test: {iteration['test_name']}")
        todo_page.add_todo(iteration["keeper"])
        todo_page.add_todo(iteration["delete"])
        todo_page.delete_todo(iteration["delete"])

        todo_page.click_all_filter()
        todo_page.expect_todo_not_visible(iteration["delete"])

        todo_page.click_active_filter()
        todo_page.expect_todo_not_visible(iteration["delete"])

        todo_page.click_completed_filter()
        todo_page.expect_todo_not_visible(iteration["delete"])