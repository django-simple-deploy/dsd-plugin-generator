"""Configuration for e2e test runs."""

# from argparse import Namespace
import json
# from pathlib import Path
import subprocess
import shlex

import pytest

# from utils.plugin_config import PluginConfig
from tests.e2e_tests.utils import e2e_utils
# import generate_plugin as gp


from dataclasses import dataclass

import pytest


# --- Custom CLI args ---
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


# --- Fixtures ---

@pytest.fixture(scope="module")
def get_dev_env(tmp_path_factory, cli_options):
    """Set up an env where plugins can be generated and tested within django-simple-deploy.

    - Set up a temp dir.
    - Install dev env for django-simple-deploy.
    - We can generate plugins, with this temp dir as target location.
    - Then install newly-generated plugins to dsd dev env, and run tests from dsd.
    """
    # Make the temp directory for the dsd development env.
    tmp_path = tmp_path_factory.mktemp("e2e_new_plugin_test")
    print(f"\nBuilding e2e test env at: {tmp_path.as_posix()}")

    # Clone django-simple-deploy in temp env.
    path_dsd = tmp_path / "django-simple-deploy"
    cmd = f"git clone https://github.com/django-simple-deploy/django-simple-deploy.git {path_dsd.as_posix()} --depth 1"
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

    # Build a venv in the django-simple-deploy temp dir.
    venv_dir = path_dsd / ".venv"
    cmd = f"uv venv {venv_dir}"
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

    # Make an editable install of django-simple-deploy in its environment.
    path_to_python = venv_dir / "bin" / "python"
    cmd = f'uv pip install --python {path_to_python} -e "{path_dsd.as_posix()}[dev]"'
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

    if not cli_options.setup_plugins_only:
        # Run core tests without a plugin installed.
        e2e_utils.run_dsd_core_tests(path_dsd, path_to_python, cli_options)

    return tmp_path, path_to_python, path_dsd

@pytest.fixture(scope="function", autouse=True)
def clear_plugins(get_dev_env):
    """Remove any plugins from dev env.

    Most tests install a plugin to the dev env. Remove each plugin after its test runs.
    """
    dev_env_dir, path_to_python, path_dsd = get_dev_env

    # Yield to let test function run, then clear any plugins that were installed.
    yield

    cmd = f"uv pip list --python {path_to_python} --format=json"
    cmd_parts = shlex.split(cmd)
    package_dicts_str = subprocess.run(cmd_parts, capture_output=True).stdout
    package_dicts = json.loads(package_dicts_str)
    package_names = [pd["name"] for pd in package_dicts if pd["name"].startswith("dsd-")]

    for pkg_name in package_names:
        cmd = f"uv pip uninstall {pkg_name} --python {path_to_python}"
        cmd_parts = shlex.split(cmd)
        subprocess.run(cmd_parts)