"""Utility functions for generating a new plugin."""

from pathlib import Path
import sys
import shutil


def get_plugin_info(args, plugin_config):
    """Prompts user for all the info needed to generate a new plugin."""
    while True:
        # Platform
        msg = "What platform are you targeting? (Example: Fly.io) "
        plugin_config.platform_name = input(msg)

        # Plugin package name
        msg = "What's the name of your plugin package? (Example: dsd-flyio) "
        while True:
            plugin_config.pkg_name = input(msg)
            if plugin_config.pkg_name.startswith("dsd-"):
                break
            else:
                print("The package name must start with `dsd-`.")

        # --automate-all support
        msg = "Will your plugin support the --automate-all CLI arg? (yes/no) "
        response = input(msg)
        if response.lower() in ("yes", "y"):
            plugin_config.support_automate_all = True
        else:
            plugin_config.support_automate_all = False

        # LICENSE name
        msg = "What name do you want to appear in the LICENSE file? "
        plugin_config.license_name = input(msg)

        # Path to new plugin
        path_root = Path(__file__).parents[1]
        default_target_dir = path_root.parent
        msg = "Where do you want to write the new plugin? "
        msg += f"\n  Default location: {default_target_dir.as_posix()}"
        msg += "\n(Press Enter to accept default location, or specify a different location.)"
        msg += "\n"
        target_dir_response = input(msg)
        if not target_dir_response:
            plugin_config.target_dir = default_target_dir
        else:
            plugin_config.target_dir = Path(target_dir_response)
        breakpoint()

        # Review responses.
        msg = "\nHere's the information you've provided:"
        print(msg)
        print(f"  Platform name: {plugin_config.platform_name}")
        print(f"  Package name: {plugin_config.pkg_name}")
        print(f"  Supports --automate-all: {plugin_config.support_automate_all}")
        print(f"  Name on license: {plugin_config.license_name}")
        print(f"  Path for new plugin: {plugin_config.target_dir}")

        msg = "\nIs this information correct? (yes/no) "
        response = input(msg)
        if response.lower() in ("yes", "y"):
            return

        msg = "Sorry, please try again.\n\n"
        print(msg)

def validate_target_dir(args, plugin_config, path_root):
    if args.target_dir:
        # If target_dir provided, make sure it exists and is safe to write to.
        path = Path(args.target_dir)
        if not path.exists():
            msg = f"The path {path.as_posix()} does not exist."
            sys.exit(msg)
        path_root_new = path / plugin_config.pkg_name
        if path_root_new.exists():
            msg += f"\nA directory already exists at {path_root_new.as_posix()}."
            msg += "\nPlease either move or rename that directory, choose a different package name,"
            msg += "\n  or write the new plugin to a different location."
            sys.exit(msg)
    else:
        # Get permission to write to target directory.
        # path_root = Path(__file__).parent
        path_root_new = path_root.parent / plugin_config.pkg_name

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
    return path_root_new

def build_new_plugin(args, plugin_config):
    """Build the new plugin in the target directory."""
    path_root = Path(__file__).parents[1]

    # Make sure it's okay to write to the target directory.
    path_root_new = validate_target_dir(args, plugin_config, path_root)

    platform_name_lower = get_platform_name_lower(plugin_config.platform_name)
    replacements = _get_replacements(plugin_config, platform_name_lower)

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
        path_src = path_root / "plugin_template" / target_file
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
        path = path_root / "plugin_template" / target_file
        contents = path.read_text()

        # Modify contents and write file.
        for k, v in replacements.items():
            contents = contents.replace(k, v)

        target_file_new = target_file.replace("platformname", f"{platform_name_lower}")
        path_new = path_root_new / target_file_new
        path_new.write_text(contents)

        msg = f"  Wrote modified file: {target_file_new}"
        print(msg)


    # --- Make other changes.

    # Remove automate_all support if needed.
    if not plugin_config.support_automate_all:
        print("Commenting out support for --automate-all...")
        path = path_root_new / f"dsd_{platform_name_lower}" / "deploy_messages.py"
        lines = path.read_text().splitlines()
        new_lines = []
        for line_num, line in enumerate(lines):
            if line_num in (9,10,11,12,13,14,15, 77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95):
                new_lines.append(f"# {line}")
            else:
                new_lines.append(line)

        new_contents = "\n".join(new_lines)
        path.write_text(new_contents)

def show_summary():
    """Show a summary message after building the new plugin."""
    msg = "\nFinished setting up your plugin. If there are any issues,"
    msg += "\nplease delete the new plugin and try again, or make manual changes"
    msg += "\nand file an issue on this project's repo:"
    msg += "\n  https://github.com/django-simple-deploy/dsd-plugin-template/issues"
    print(msg)

    msg = "\nYou should now be able to make an editable install of this project into"
    msg += "\na development version of django-simple-deploy, and all initial tests"
    msg += "\nshould pass."
    print(msg)

def get_platform_name_lower(platform_name):
    """Return a lowercase version of the platform name."""
    return platform_name.lower().replace("-", "").replace("_", "").replace(".", "").replace(" ", "")


# --- Helper functions ---

def _get_replacements(plugin_config, platform_name_lower):
    """Get substitions for..."""
    replacements = {
        "{{PlatformName}}": plugin_config.platform_name,
        "{{PlatformNameLower}}": platform_name_lower,
        "{{PackageName}}": plugin_config.pkg_name,
        "{{PluginName}}": plugin_config.pkg_name.replace("-", "_"),
        "{{AutomateAllSupported}}": str(plugin_config.support_automate_all),
        "{{LicenseName}}": plugin_config.license_name,
    }

    return replacements

