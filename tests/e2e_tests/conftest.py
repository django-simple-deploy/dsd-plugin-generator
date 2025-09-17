"""Configuration for e2e test runs."""

from dataclasses import dataclass

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-core-tests",
        action="store_true",
        help="Run the full set of core django-simple-deploy tests for each new plugin.",
    )
    parser.addoption(
        # Useful for troubleshooting this test env. May also be useful for poking around
        # the full set of test plugins.
        # In a full test run, this test runs many django-simple-deploy pytest calls. Each of
        # those leads to a pytest-___ temp dir. That can make it difficult or impossible
        # to find the dir associated with a specific failing test.
        "--setup-plugins-only",
        action="store_true",
        help="Build full set of test dev env with test plugins, but don't run any tests."
    )

@dataclass
class CLIOptions:
    run_core_tests: bool=False
    setup_plugins_only: bool=False

@pytest.fixture(scope="session")
def cli_options(request):
    return CLIOptions(
        run_core_tests=request.config.getoption("--run-core-tests"),
        setup_plugins_only=request.config.getoption("--setup-plugins-only"),
    )
