"""Test a plugin that uses a custom CLI arg.

Some of the code that supports a custom CLI is commented out in the generated plugin.
So, we need to uncomment that code, then run the tests.

This test:
- Generates a new plugin.
- Modifies the generated files to enable a custom CLI arg.
- Modifies platform_deployer.py to use the custom CLI arg in a testable way.
- Sets up a development environment for django-simple-deploy core.
- Installs the new plugin to the development environment.
- Runs the plugin's integration tests, using a `deploy` call that includes the custom CLI arg.

Notes:
- This makes an editable install of both django-simple-deploy and the new plugin.
- If there are issues, you can go the test env and modify both core and the new
  plugin to troubleshoot.
- If you want to do this, you may need to use `--setup-plugins-only`, otherwise
  the pytest temp dir will be garbage collected because so many temp dirs are being made.
"""

from argparse import Namespace
import subprocess
import shlex

import pytest

from utils.plugin_config import PluginConfig
from tests.e2e_tests.utils import e2e_utils


# Skip these tests if uv is not available.
pytestmark = pytest.mark.skipif(
    not e2e_utils.uv_available(), reason="uv must be installed in order to run e2e tests."
)


def test_custom_cli_arg(get_dev_env, cli_options):
    """Test a simple plugin config."""
    dev_env_dir, path_to_python, path_dsd = get_dev_env

    plugin_config = PluginConfig(
        platform_name = "NewFly",
        pkg_name = "dsd-newfly",
        support_automate_all = True,
        license_name = "eric",
    )
    e2e_utils.generate_plugin(get_dev_env, plugin_config)

    # Uncomment CLI-related code.
    path_plugin_dir = dev_env_dir / plugin_config.pkg_name
    path_main_dir = path_plugin_dir / plugin_config.pkg_name.replace("-", "_")

    path_cli = path_main_dir / "cli.py"
    path_platform_deployer = path_main_dir / "platform_deployer.py"

    path_tests = path_plugin_dir / "tests" / "integration_tests"
    path_test_custom_cli = path_tests/ "test_custom_cli_arg.py"
    path_test_help = path_tests / "test_help_output.py"

    # Assert these paths all exist.
    assert all([path_cli.exists(), path_platform_deployer.exists(), path_test_custom_cli.exists(), path_test_help.exists()])






    if not cli_options.setup_plugins_only:
        e2e_utils.run_core_plugin_tests(path_dsd, plugin_config, cli_options)