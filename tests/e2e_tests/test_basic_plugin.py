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
import json
from pathlib import Path
import subprocess
import shlex

import pytest

from utils.plugin_config import PluginConfig
from tests.e2e_tests.utils import e2e_utils
import generate_plugin as gp


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


@pytest.mark.skipif(not e2e_utils.uv_available(), reason="uv must be installed in order to run e2e tests.")
def test_simple_plugin(get_dev_env, cli_options):
    """Test a simple plugin config."""
    dev_env_dir, path_to_python, path_dsd = get_dev_env

    plugin_config = PluginConfig(
        platform_name = "NewFly",
        pkg_name = "dsd-newfly",
        support_automate_all = True,
        license_name = "eric",
    )

    args = Namespace(target_dir=dev_env_dir)
    gp.generate_plugin(plugin_config, args)

    # Make sure we have the correct path to the new plugin.
    path_new_plugin = dev_env_dir / "dsd-newfly"
    assert path_new_plugin.exists()

    # Install plugin editable to django-simple-deploy env.
    cmd = f'uv pip install --python {path_to_python} -e "{path_new_plugin.as_posix()}[dev]"'
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

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