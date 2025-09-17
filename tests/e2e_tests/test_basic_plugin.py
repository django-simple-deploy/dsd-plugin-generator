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
import subprocess
import shlex

import pytest

from utils.plugin_config import PluginConfig
from tests.e2e_tests.utils import e2e_utils
import generate_plugin as gp


# Skip these tests if uv is not available.
pytestmark = pytest.mark.skipif(
    not e2e_utils.uv_available(), reason="uv must be installed in order to run e2e tests."
)


def _generate_plugin(dev_env, plugin_config):
    """Generate a new plugin, and install it to the django-simple-deploy dev env.
    """
    dev_env_dir, path_to_python, path_dsd = dev_env

    args = Namespace(target_dir=dev_env_dir)
    gp.generate_plugin(plugin_config, args)

    # Make sure we have the correct path to the new plugin.
    path_new_plugin = dev_env_dir / "dsd-newfly"
    assert path_new_plugin.exists()

    # Install plugin editable to django-simple-deploy env.
    cmd = f'uv pip install --python {path_to_python} -e "{path_new_plugin.as_posix()}[dev]"'
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)



def test_simple_plugin(get_dev_env, cli_options):
    """Test a simple plugin config."""
    dev_env_dir, path_to_python, path_dsd = get_dev_env

    plugin_config = PluginConfig(
        platform_name = "NewFly",
        pkg_name = "dsd-newfly",
        support_automate_all = True,
        license_name = "eric",
    )

    _generate_plugin(get_dev_env, plugin_config)

    # args = Namespace(target_dir=dev_env_dir)
    # gp.generate_plugin(plugin_config, args)

    # # Make sure we have the correct path to the new plugin.
    # path_new_plugin = dev_env_dir / "dsd-newfly"
    # assert path_new_plugin.exists()

    # # Install plugin editable to django-simple-deploy env.
    # cmd = f'uv pip install --python {path_to_python} -e "{path_new_plugin.as_posix()}[dev]"'
    # cmd_parts = shlex.split(cmd)
    # subprocess.run(cmd_parts)

    if not cli_options.setup_plugins_only:
        e2e_utils.run_core_plugin_tests(path_dsd, plugin_config, cli_options)


def test_plugin_single_space_platform_name(get_dev_env, cli_options):
    """Test a plugin for a platform with a space in the name."""
    dev_env_dir, path_to_python, path_dsd = get_dev_env

    # Flag to temporarily disable running dsd and plugin tests. This is helpful when
    # examining this environment. Otherwise pytest runs so many tests, this one can't
    # easily be found. This is not a CLI arg, because it only needs to be modified when you're
    # working on this test, not when you're just running it.
    run_core_plugin_tests = True

    plugin_config = PluginConfig(
        platform_name = "New Platform",
        pkg_name = "dsd-newplatform",
        support_automate_all = True,
        license_name = "eric",
    )

    args = Namespace(target_dir=dev_env_dir)
    gp.generate_plugin(plugin_config, args)

    # Make sure we have the correct path to the new plugin.
    path_new_plugin = dev_env_dir / "dsd-newplatform"
    assert path_new_plugin.exists()

    # Install plugin editable to django-simple-deploy env.
    cmd = f'uv pip install --python {path_to_python} -e "{path_new_plugin.as_posix()}[dev]"'
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

    if not cli_options.setup_plugins_only:
        e2e_utils.run_core_plugin_tests(path_dsd, plugin_config, cli_options)

def test_plugin_different_plugin_platform_name(get_dev_env, cli_options):
    """Test a plugin where platform and plugin names differ significantly."""
    dev_env_dir, path_to_python, path_dsd = get_dev_env

    # Flag to temporarily disable running dsd and plugin tests. This is helpful when
    # examining this environment. Otherwise pytest runs so many tests, this one can't
    # easily be found. This is not a CLI arg, because it only needs to be modified when you're
    # working on this test, not when you're just running it.
    run_core_plugin_tests = True

    plugin_config = PluginConfig(
        platform_name = "MyNewPlatform",
        pkg_name = "dsd-my-plugin",
        support_automate_all = True,
        license_name = "eric",
    )

    args = Namespace(target_dir=dev_env_dir)
    gp.generate_plugin(plugin_config, args)

    # Make sure we have the correct path to the new plugin.
    path_new_plugin = dev_env_dir / "dsd-my-plugin"
    assert path_new_plugin.exists()

    # Install plugin editable to django-simple-deploy env.
    cmd = f'uv pip install --python {path_to_python} -e "{path_new_plugin.as_posix()}[dev]"'
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

    if not cli_options.setup_plugins_only:
        e2e_utils.run_core_plugin_tests(path_dsd, plugin_config, cli_options)