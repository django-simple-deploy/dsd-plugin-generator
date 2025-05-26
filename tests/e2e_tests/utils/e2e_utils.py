"""Utility functions for e2e tests."""



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