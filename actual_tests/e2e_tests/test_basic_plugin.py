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
        subprocess.run(cmd_parts, capture_output=True)
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

    # Build a venv in temp dir.