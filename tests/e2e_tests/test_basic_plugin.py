"""Test a basic plugin in a real-world environment.

This test:
- Generates a new plugin.
- Sets up a development environment for django-simple-deploy core.
- Installs the new plugin to the development environment.
- Runs the plugin's integration tests.

Notes:
- This makes an editable install of both django-simple-deploy and the new plugin.
- If there are issues, you can go the test env and modify both core and the new
  plugin to troubleshoot.
- If you want to do this, ou may need to set run_core_plugin_tests to False, otherwise
  the pytest temp dir will be garbage collected because so many temp dirs are being made.
"""

from argparse import Namespace
from pathlib import Path
import subprocess
import shlex

import pytest

from utils.plugin_config import PluginConfig
from tests.e2e_tests.utils import e2e_utils
import generate_plugin as gp


@pytest.mark.skipif(not e2e_utils.uv_available(), reason="uv must be installed in order to run e2e tests.")
def test_new_plugin_e2e(tmp_path_factory, cli_options):
    # Flag to temporarily disable running dsd and plugin tests. This is helpful when
    # examining this environment. Otherwise pytest runs so many tests, this one can't
    # easily be found. This is not a CLI arg, because it only needs to be modified when you're
    # working on this test, not when you're just running it.
    run_core_plugin_tests = True

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

    # Make sure we have the correct path to the new plugin.
    path_new_plugin = tmp_path / "dsd-newfly"
    assert path_new_plugin.exists()

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

    if run_core_plugin_tests:
        # Run core tests without a plugin installed.
        e2e_utils.run_core_tests(path_dsd, path_to_python, cli_options)

    # Install plugin editable to django-simple-deploy env.
    cmd = f'uv pip install --python {path_to_python} -e "{path_new_plugin.as_posix()}[dev]"'
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

    if run_core_plugin_tests:
        e2e_utils.run_core_plugin_tests(path_dsd, plugin_config, cli_options)


    # Remove plugin, and test another one.
    # This is much faster than having a completely separate test. We lose some test
    # independence, but the speedup is worthwhile.

    # Uninstall previous plugin.
    cmd = f'uv pip uninstall --python {path_to_python} dsd-newfly'
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

    # Build "New Platform" plugin.
    plugin_config = PluginConfig(
        platform_name = "New Platform",
        pkg_name = "dsd-newplatform",
        support_automate_all = True,
        license_name = "eric",
    )

    args = Namespace(target_dir=tmp_path)
    gp.generate_plugin(plugin_config, args)

    # Make sure we have the correct path to the new plugin.
    path_new_plugin = tmp_path / "dsd-newplatform"
    assert path_new_plugin.exists()

    # Install plugin editable to django-simple-deploy env.
    cmd = f'uv pip install --python {path_to_python} -e "{path_new_plugin.as_posix()}[dev]"'
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

    if run_core_plugin_tests:
        e2e_utils.run_core_plugin_tests(path_dsd, plugin_config, cli_options)
