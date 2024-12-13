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


# --- Prompt for plugin info. ---

while True:
    msg = "What platform are you targeting? (Example: Fly.io) "
    platform_name = input(msg)

    msg = "What's the name of your plugin package? (Example: dsd-flyio) "
    while True:
        pkg_name = input(msg)
        if pkg_name.startswith("dsd-"):
            break
        else:
            print("The package name must start with `dsd-`.")

    msg = "Will your plugin support the --automate-all CLI arg? (yes/no) "
    response = input(msg)
    if response.lower() in ("yes", "y"):
        automate_all = True
    else:
        automate_all = False

    # Review responses.
    msg = "\nHere's the information you've provided:"
    print(msg)
    print(f"  Platform name: {platform_name}")
    print(f"  Package name: {pkg_name}")
    print(f"  Supports --automate-all: {automate_all}")

    msg = "\nIs this information correct? (yes/no) "
    response = input(msg)
    if response.lower() in ("yes", "y"):
        break

    msg = "Sorry, please try again.\n\n"
    print(msg)

print("\n\nThank you. Configuring plugin...")

# Define replacements dict.
replacements = {
    "{{PlatformName}}": platform_name,
    "{{PlatformNameLower}}": platform_name.lower().replace("-", "").replace("_", "").replace(".", ""),
    "{{PackageName}}": pkg_name,
    "{{PluginName}}": pkg_name.replace("-", "_"),
    "{{AutomateAllSupported}}": automate_all
}


# --- Make replacements in file contents. ---

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
    msg = f"Modifying file: {target_file}"
    path = path_root / target_file
    contents = path.read_text()

    for k, v in replacements.items():
        contents = contents.replace("k", "v")

    path.write_text(contents)

# 