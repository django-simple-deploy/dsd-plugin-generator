"""Test a basic plugin in a real-world environment.

This test:
- Generates a new plugin.
- Sets up a development environment for django-simple-deploy core.
- Installs the new plugin to the development environment.
- Runs the initial set of tests against the plugin.
"""

from argparse import Namespace
from pathlib import Path
import subprocess
import shlex

import pytest

from utils.plugin_config import PluginConfig
import generate_plugin as gp


def uv_available():
    """Ensure uv is available before running test."""
    cmd = "uv self version -q"
    cmd_parts = shlex.split(cmd)
    try:
        subprocess.run(cmd_parts)
        return True
    except FileNotFoundError:
        # This is the exception raised on macOS when the command uv is unavailable.
        return False


### --- Test function ---

@pytest.mark.skipif(not uv_available(), reason="uv must be installed in order to run e2e tests.")
def test_new_plugin_e2e(tmp_path_factory):

    # Build a new plugin in temp dir.
    tmp_path = tmp_path_factory.mktemp("e2e_new_plugin_test")
    print(f"\nBuilding e2e test env at: {tmp_path.as_posix()}")

    plugin_config = PluginConfig(
        platform_name = "NewFly",
        pkg_name = "dsd-newfly",
        support_automate_all = True,
        license_name = "eric",
    )

    args = Namespace(target_dir=tmp_path)
    gp.generate_plugin(plugin_config, args)

    # Clone django-simple-deploy in temp env.
    path_dsd = tmp_path / "django-simple-deploy"
    cmd = f"git clone https://github.com/django-simple-deploy/django-simple-deploy.git {path_dsd.as_posix()}"
    cmd_parts = shlex.split(cmd)
    # breakpoint()
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

    # Run core tests without a plugin installed.
    tests_dir = path_dsd / "tests"
    cmd = f"{path_to_python} -m pytest {tests_dir.as_posix()}"
    cmd_parts = shlex.split(cmd)
    output = subprocess.run(cmd_parts, capture_output=True)
    stdout = output.stdout.decode()
    breakpoint()