"""Configuration for e2e test runs."""

from dataclasses import dataclass

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--include-core-tests",
        action="store_true",
        help="Run the full set of core django-simple-deploy tests for each new plugin.",
    )

@dataclass
class CLIOptions:
    include_core_tests: bool=False

@pytest.fixture(scope="session")
def cli_options(request):
    return CLIOptions(
        include_core_tests=request.config.getoption("--include-core-tests"),
    )
