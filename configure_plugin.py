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
import platform
import subprocess
import time
import shlex
import shutil
import sys


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

    msg = "What name do you want to appear in the LICENSE file? "
    license_name = input(msg)

    # Review responses.
    msg = "\nHere's the information you've provided:"
    print(msg)
    print(f"  Platform name: {platform_name}")
    print(f"  Package name: {pkg_name}")
    print(f"  Supports --automate-all: {automate_all}")
    print(f"  Name on license: {license_name}")

    msg = "\nIs this information correct? (yes/no) "
    response = input(msg)
    if response.lower() in ("yes", "y"):
        break

    msg = "Sorry, please try again.\n\n"
    print(msg)

# Get permission to write to target directory.
path_root = Path(__file__).parent
path_root_new = path_root.parent / pkg_name

if path_root_new.exists():
    msg = "\nThe new repo needs to be written alongside this project,"
    msg += f"\n  but a directory already exists at {path_root_new.as_posix()}."
    msg += "\nPlease either move or rename that directory, choose a different package name,"
    msg += "\n  or copy this project to a different location and try again."
    sys.exit(msg)

while True:
    msg = f"\nOkay to write new project at {path_root_new.as_posix()}? (yes/no) "
    response = input(msg)
    if response.lower() in ("yes", "y"):
        break
    if response.lower() in ("no", "n"):
        msg = "\nOkay, feel free to copy this project to a different location and try again."
        msg += "\n  The new repo will be written alongside this project."
        sys.exit(msg)

print("\n\nThank you. Configuring plugin...")

# Define replacements dict.
platform_name_lower = platform_name.lower().replace("-", "").replace("_", "").replace(".", "")
replacements = {
    "{{PlatformName}}": platform_name,
    "{{PlatformNameLower}}": platform_name_lower,
    "{{PackageName}}": pkg_name,
    "{{PluginName}}": pkg_name.replace("-", "_"),
    "{{AutomateAllSupported}}": str(automate_all),
    "{{LicenseName}}": license_name,
}


# --- Build out directory structure ---

# Make new plugin dir, and required directory structure.
print(f"\nMaking new directory: {path_root_new.as_posix()}")
path_root_new.mkdir()

print("Building inner directory structure...")

# Using mkdir(parents=True), only need to make most deeply nested dirs.
new_dirs = [
    "developer_resources",
    f"dsd_{platform_name_lower}/templates",
    "tests/integration_tests/reference_files",
    "tests/e2e_tests",
]

for new_dir in new_dirs:
    path_new_dir = path_root_new / new_dir
    print(f"  Making new directory: {path_new_dir.as_posix()}")
    path_new_dir.mkdir(parents=True)


# --- Copy files that don't need modification. ---

print(f"\nCopying files...")
target_files = [
    ".gitignore",
    "developer_resources/README.md",
    "dsd_platformname/__init__.py",
    "tests/e2e_tests/__init__.py",
    "tests/integration_tests/reference_files/.gitignore",
    "tests/integration_tests/reference_files/Pipfile",
    "tests/integration_tests/reference_files/pyproject.toml",
    "tests/integration_tests/reference_files/requirements.txt",
    "tests/integration_tests/reference_files/settings.py",
]

for target_file in target_files:
    print(f"  Copying file: {target_file}")
    path_src = path_root / target_file
    target_file_new = target_file.replace("dsd_platformname", f"dsd_{platform_name_lower}")
    path_dest = path_root_new / target_file_new
    shutil.copy(path_src, path_dest)

# --- Make replacements in file contents. ---

# Files that need to be parsed.
target_files = [
    "pyproject.toml",
    "tests/conftest.py",
    "tests/integration_tests/test_platformname_config.py",
    "tests/e2e_tests/utils.py",
    "tests/e2e_tests/test_deployment.py",
    "MANIFEST.in",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "dsd_platformname/platform_deployer.py",
    "dsd_platformname/deploy.py",
    "dsd_platformname/plugin_config.py",
    "dsd_platformname/templates/dockerfile_example",
    "dsd_platformname/templates/settings.py",
    "dsd_platformname/deploy_messages.py",
]

print("\nCustomizing files...")
for target_file in target_files:
    # Read file.
    path = path_root / target_file
    contents = path.read_text()

    # Modify contents and write file.
    for k, v in replacements.items():
        contents = contents.replace(k, v)

    target_file_new = target_file.replace("dsd_platformname", f"dsd_{platform_name_lower}")
    path_new = path_root_new / target_file_new
    path_new.write_text(contents)

    msg = f"  Wrote modified file: {target_file_new}"
    print(msg)

sys.exit()
# --- Make other appropriate changes.

# Rename test file.
print("\nRenaming integration test file...")
path_test_file = path_root / "tests" / "integration_tests" / "test_platformname_config.py"
path_test_file_renamed = path_root / "tests" / "integration_tests" / f"test_{platform_name_lower}_config.py"
# path_test_file.rename(path_test_file_renamed)

# Remove automate_all support if needed.
if not automate_all:
    print("Commenting out support for --automate-all...")
    path = path_root / "dsd_platformname" / "deploy_messages.py"
    lines = path.read_text().splitlines()
    new_lines = []
    for line_num, line in enumerate(lines):
        if line_num in (9,10,11,12,13,14,15, 77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95):
            new_lines.append(f"# {line}")
        else:
            new_lines.append(line)

    new_contents = "\n".join(new_lines)
    # path.write_text(new_contents)

# Rename dsd_platformname dir.
print("Renaming main plugin directory...")
path_dsd_dir = path_root / "dsd_platformname"
path_dsd_dir_new = path_root / f"dsd_{platform_name_lower}"
# path_dsd_dir.rename(path_dsd_dir_new)

# Remove unneeded lines from README.
print("Modifying README...")
path = path_root / "README.md"
lines = path.read_text().splitlines()[:4]
contents = "\n".join(lines)
# path.write_text(contents)

# Rename repo dir.
print("Modifying parent directory...")
repo_name = path_root.name
path_root_new = Path(__file__).parent.parent / pkg_name
# path_root.rename(path_root_new)

# Delete this file.
print("Deleting this configuration script...")
path = path_root_new / "configure_plugin.py"
# path.unlink()

msg = "\nFinished setting up your plugin. If there are any issues,"
msg += "\nplease download a fresh copy of the repo and try again."
print(msg)

msg = f"\nYou'll probably need to `cd ..` and then `cd {pkg_name}` to see"
msg += "\nthe new name of this directory."
print(msg)

msg = "\nYou should now be able to make an editable install of this project into"
msg += "\na development version of django-simple-deploy, and run a small set of"
msg += "\ninitial tests."
print(msg)