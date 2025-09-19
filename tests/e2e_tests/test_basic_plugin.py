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


def test_simple_plugin(get_dev_env, cli_options):
    """Test a simple plugin config."""
    dev_env_dir, path_to_python, path_dsd = get_dev_env

    plugin_config = PluginConfig(
        platform_name = "NewFly",
        pkg_name = "dsd-newfly",
        support_automate_all = True,
        license_name = "eric",
    )
    e2e_utils.generate_plugin(get_dev_env, plugin_config)

    if not cli_options.setup_plugins_only:
        e2e_utils.run_core_plugin_tests(path_dsd, plugin_config, cli_options)

def test_plugin_single_space_platform_name(get_dev_env, cli_options):
    """Test a plugin for a platform with a space in the name."""
    dev_env_dir, path_to_python, path_dsd = get_dev_env

    plugin_config = PluginConfig(
        platform_name = "New Platform",
        pkg_name = "dsd-newplatform",
        support_automate_all = True,
        license_name = "eric",
    )
    e2e_utils.generate_plugin(get_dev_env, plugin_config)

    if not cli_options.setup_plugins_only:
        e2e_utils.run_core_plugin_tests(path_dsd, plugin_config, cli_options)

def test_plugin_different_plugin_platform_name(get_dev_env, cli_options):
    """Test a plugin where platform and plugin names differ significantly."""
    dev_env_dir, path_to_python, path_dsd = get_dev_env

    plugin_config = PluginConfig(
        platform_name = "MyNewPlatform",
        pkg_name = "dsd-my-plugin",
        support_automate_all = True,
        license_name = "eric",
    )
    e2e_utils.generate_plugin(get_dev_env, plugin_config)

    if not cli_options.setup_plugins_only:
        e2e_utils.run_core_plugin_tests(path_dsd, plugin_config, cli_options)