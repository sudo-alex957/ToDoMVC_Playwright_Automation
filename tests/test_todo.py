import pytest
from utils import get_logger, load_test_data

logger = get_logger("tests.test_todo")


def data(test_name: str) -> list[dict]:
    """Load YAML iterations for a given test function from test_todo.yaml."""
    return load_test_data(__file__, test_name)


class TestAddTodo:
    """Setup: open the todo page once → Tests: add items → Teardown: close context."""

    @pytest.fixture(autouse=True, scope="class")
    def setup(self, todo_page):
        logger.info("Setup: opening TodoMVC page")
        todo_page.open()
        yield
        logger.info("Teardown: TestAddTodo complete")

    @pytest.mark.WRITE
    @pytest.mark.regression
    @pytest.mark.front_end
    @pytest.mark.parametrize("iteration", data("test_add_new_todo_with_various_text"),
                             ids=lambda it: it["test_id"])
    def test_add_new_todo_with_various_text(self, todo_page, iteration):
        logger.info(f"Starting test: {iteration['test_name']}")
        todo_text = iteration["text"]
        todo_page.add_todo(todo_text)
        todo_page.expect_todo_visible(todo_text)
