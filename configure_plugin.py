"""Configure the plugin to target a specific platform.

Usage:
$ python configure_plugin.py

That's all. You'll be asked a few questions, and this project will be converted
to a plugin with passing tests, that you can customize to target a specific platform
and deployment workflow.

This script, and other meta-files, will be removed. If you don't like what you end
up with, download a fresh copy of the plugin template and run this script again.

Development notes:

To identify which files to parse, run:

$ grep -Rl {{ .
./pyproject.toml
./tests/conftest.py
./tests/integration_tests/test_flyio_config.py
  ...
./dsd_platformname/deploy_messages.py
"""

from pathlib import Path

# Files that need to be parsed.
target_files = [
    "pyproject.toml",
    "tests/conftest.py",
    "tests/integration_tests/test_flyio_config.py",
    "tests/e2e_tests/utils.py",
    "tests/e2e_tests/test_deployment.py",
    "MANIFEST.in",
    "README.md",
    "dsd_platformname/platform_deployer.py",
    "dsd_platformname/deploy.py",
    "dsd_platformname/plugin_config.py",
    "dsd_platformname/templates/dockerfile_example",
    "dsd_platformname/templates/settings.py",
    "dsd_platformname/deploy_messages.py",
]

path_root = Path(__file__).parent

for target_file in target_files:
    # Read file, make replacements, rewrite file.
    path = path_root / target_file
    contents = path.read_text()