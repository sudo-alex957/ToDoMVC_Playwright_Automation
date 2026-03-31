# TodoMVC Playwright Python Automation

Automated UI tests for [https://demo.playwright.dev/todomvc/#/](https://demo.playwright.dev/todomvc/#/)

## Tech stack

- **Python 3.10+**
- **Playwright** (sync API) — browser automation
- **Pytest** — test runner, fixtures, parametrize
- **pytest-html** — self-contained HTML reports
- **pytest-rerunfailures** — automatic retry for flaky UI tests
- **PyYAML** — YAML-driven test data

## Project structure

```text
.
├── .github/
│   └── workflows/
│       └── tests.yml               # CI pipeline — runs on push/PR to main
├── pages/
│   ├── base_page.py               # BasePage (reusable actions) + PageFactory
│   └── todo_page.py               # TodoPage — page object for TodoMVC
├── tests/
│   ├── conftest.py                 # Fixtures, hooks, reporting & artifact capture
│   ├── test_todo.py                # Tests: add todo items
│   ├── test_todo.yaml              # Test data: add todo iterations
│   ├── test_filter_todo.py         # Tests: completed / active filters
│   ├── test_filter_todo.yaml       # Test data: filter iterations
│   ├── test_delete_todo.py         # Tests: delete todo items
│   └── test_delete_todo.yaml       # Test data: delete iterations
├── utils/
│   └── __init__.py                 # Logger + YAML test data loader
├── reports/                        # Generated after a run (git-ignored)
│   ├── report.html                 # Self-contained HTML report
│   ├── screenshots/                # Failure screenshots (.png)
│   └── traces/                     # Playwright traces (.zip)
├── pytest.ini                      # Pytest config + custom marks + reruns
├── requirements.txt
└── README.md
```

## Architecture

### Page Object Model

```
BasePage  →  reusable wrappers (goto, click, fill, press, expect)
  └── TodoPage  →  domain actions (add_todo, toggle_todo, delete_todo, filters, expect_todo_count)
```

`PageFactory` creates page objects sharing the same underlying Playwright `Page` instance.
It is fully typed using `TypeVar` — IDE autocomplete and type checking work out of the box.

### Fixture chain (all class-scoped)

```
browser (session) → page (class) → page_factory (class) → todo_page (class)
```

Each test class follows **Setup → Tests → Teardown**: the `setup` fixture opens the page
and prepares data once, all test methods in the class run against the same browser context,
then the context is closed.

### Configurable base URL

The target URL is configurable via the `BASE_URL` environment variable, allowing the same
tests to run against different environments (dev, staging, production):

```bash
BASE_URL=https://staging.example.com/todomvc/#/ pytest
```

Falls back to `https://demo.playwright.dev/todomvc/#/` when not set.

### YAML-driven test data

Test data lives in `.yaml` files next to the corresponding test file (same name, different
extension). Tests use `@pytest.mark.parametrize` with `load_test_data(__file__, "test_name")`
to iterate over data entries — adding new scenarios requires **no Python code changes**, just
a new entry in the YAML file.

```yaml
test_add_new_todo_with_various_text:
  - test_id: NX-10000
    test_name: "Todo - Add new Todo with English text"
    text: "Buy groceries"
  - test_id: NX-10001
    test_name: "Todo - Add new Todo with Spanish text"
    text: "Comprar comestibles"
```

### Logging

Built-in logger (`utils.get_logger`) is used across pages, fixtures, and tests.
Output format: `2026-03-31 16:39:28 | INFO | TodoPage | Adding todo: 'Buy milk'`

Use `-s` flag to see log output in the console:

```bash
pytest -v -s
```

### Flaky test retry

UI tests can be inherently flaky due to network or rendering timing. `pytest-rerunfailures`
is configured to automatically retry failed tests once (`--reruns 1` in `pytest.ini`).
Reruns are visible in both the console output and the HTML report.

## Test coverage

| Test ID | Scenario |
|---|---|
| NX-10000 – NX-10004 | Add new todo with various text (English, non-English, special chars, long text) |
| NX-10100 | Completed item appears in Completed view |
| NX-10200 | Active filter shows only non-completed items |
| NX-10300 | Completed filter shows only completed items |
| NX-10400 | Deleted item absent from all views |

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright browser binaries:

```bash
playwright install chromium
```

## Run tests

Run all tests:

```bash
pytest
```

Run with verbose output and logs:

```bash
pytest -v -s
```

Run with headed browser:

```bash
HEADLESS=false pytest
```

Run in slow motion (value in milliseconds):

```bash
HEADLESS=false SLOW_MO=500 pytest
```

Run against a different environment:

```bash
BASE_URL=https://staging.example.com/todomvc/#/ pytest
```

Run a specific test file:

```bash
pytest tests/test_todo.py -v
```

Run a specific test class or method:

```bash
pytest tests/test_todo.py::TestAddTodo -v
pytest tests/test_filter_todo.py::TestTodoCompletion::test_active_filter_shows_only_not_completed_items -v
```

Run by custom mark:

```bash
pytest -m regression
pytest -m "WRITE and front_end"
```

## Custom marks

| Mark | Description |
|---|---|
| `WRITE` | Tests that create or modify data |
| `regression` | Regression test suite |
| `front_end` | Front-end UI tests |

## CI / CD

A GitHub Actions workflow (`.github/workflows/tests.yml`) runs on every push and PR to `main`:

1. Sets up Python 3.10 and installs dependencies
2. Installs Chromium via Playwright
3. Runs all tests with retry (`--reruns 1`)
4. Uploads the `reports/` directory as a downloadable artifact (retained 14 days)

## Reporting

After each run a `reports/` directory is generated containing:

| Artifact | Location | Description |
|---|---|---|
| HTML report | `reports/report.html` | Self-contained report — open in any browser |
| Screenshots | `reports/screenshots/` | Full-page PNG captured automatically on **failure** |
| Traces | `reports/traces/` | Playwright trace ZIP captured on **failure** |

### Viewing a trace

```bash
playwright show-trace reports/traces/<class_name>.zip
```

This opens the Playwright Trace Viewer with a timeline of actions, DOM snapshots,
network requests, and console logs for the failed test.
