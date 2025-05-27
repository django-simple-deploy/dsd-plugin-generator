"""Utility functions for e2e tests."""

import shlex
import subprocess
import re


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


def get_core_plugin_test_cmd(path_dsd, cli_options, platform_name_lower):
    """Get the command for running django-simple-deploy tests after a new plugin has been installed."""
    test_filename = f"test_{platform_name_lower}_config.py"

    if cli_options.include_core_tests:
        # Run full set of core django-simple-deploy tests, and plugin integration tests.
        cmd = f"cd {path_dsd.as_posix()} && source .venv/bin/activate && pytest"
    else:
        # Only run the new plugin's integration tests.
        cmd = f"cd {path_dsd.as_posix()} && source .venv/bin/activate && pytest -k {test_filename}"

    return cmd

# def check_core_only_tests(stdout):
#     """Check output of running core tests with no plugin installed."""
#     # No assertions about number skipped, but helpful to know at times.
#     re_passed_skipped = r"""(\d*) passed, (\d*) skipped"""
#     m = re.findall(re_passed_skipped, stdout)
#     if m:
#         passed = int(m[0][0])
#         skipped = int(m[0][1])
#         assert passed >= 31

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
        elif cli_options.include_core_tests:
            # Core tests, and plugin's integrationtests.
            assert passed >= 65
        else:
            # Plugin's integration tests, no core tests.
            assert passed >= 18