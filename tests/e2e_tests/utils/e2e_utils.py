"""Utility functions for e2e tests."""


from argparse import Namespace
import shlex
import subprocess
import re

import pytest

import generate_plugin as gp
from utils.plugin_config import PluginConfig
from utils.generator_utils import _get_platform_name_lower


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

def generate_plugin(dev_env, plugin_config):
    """Generate a new plugin, and install it to the django-simple-deploy dev env.
    """
    dev_env_dir, path_to_python, path_dsd = dev_env

    args = Namespace(target_dir=dev_env_dir)
    gp.generate_plugin(plugin_config, args)

    # Make sure we have the correct path to the new plugin.
    path_new_plugin = dev_env_dir / plugin_config.pkg_name
    assert path_new_plugin.exists()

    # Install plugin editable to django-simple-deploy env.
    cmd = f'uv pip install --python {path_to_python} -e "{path_new_plugin.as_posix()}[dev]"'
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)


def run_dsd_core_tests(path_dsd, path_to_python, cli_options):
    """Run django-simple-deploy's test suite with no plugin installed."""
    tests_dir = path_dsd / "tests"
    cmd = f"{path_to_python} -m pytest {tests_dir.as_posix()}"
    cmd_parts = shlex.split(cmd)
    output = subprocess.run(cmd_parts, capture_output=True)
    stdout = output.stdout.decode()

    assert "[100%]" in stdout
    check_core_plugin_tests(stdout, cli_options, core_only=True)

def run_core_plugin_tests(path_dsd, plugin_config, cli_options):
    """Run django-simple-deploy's test suite with a plugin installed."""
    tests_dir = path_dsd / "tests"
    platform_name_lower = _get_platform_name_lower(plugin_config.platform_name)
    cmd = get_core_plugin_test_cmd(path_dsd, cli_options, platform_name_lower)

    output = subprocess.run(cmd, capture_output=True,shell=True)
    stdout = output.stdout.decode()
    print(stdout)

    assert "FAILURE" not in stdout
    check_core_plugin_tests(stdout, cli_options)


def get_core_plugin_test_cmd(path_dsd, cli_options, platform_name_lower):
    """Get the command for running django-simple-deploy tests after a new plugin has been installed."""
    test_filename = f"test_{platform_name_lower}_config.py"

    if cli_options.run_core_tests:
        # Run full set of core django-simple-deploy tests, and plugin integration tests.
        cmd = f"cd {path_dsd.as_posix()} && source .venv/bin/activate && pytest"
    else:
        # Only run the new plugin's integration tests.
        cmd = f"cd {path_dsd.as_posix()} && source .venv/bin/activate && pytest -k {test_filename} -k test_help_output.py"

    return cmd


def check_core_plugin_tests(stdout, cli_options, core_only=False):
    """Check number of core and plugin tests that passed and skipped."""
    # No assertions about number skipped, but helpful to know at times.
    re_passed_skipped = r"""(\d*) passed, (\d*) skipped"""
    m = re.findall(re_passed_skipped, stdout)
    if m:
        passed = int(m[0][0])
        skipped = int(m[0][1])

        if core_only:
            # Core tests, no plugin installed.
            assert passed >= 31
        elif cli_options.run_core_tests:
            # Core tests, and plugin's integrationtests.
            assert passed >= 65
        else:
            # Plugin's integration tests, no core tests.
            assert passed >= 18
