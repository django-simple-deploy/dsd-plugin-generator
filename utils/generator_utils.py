"""Utility functions for generating a new plugin."""

from pathlib import Path
import sys

def get_plugin_info(plugin_config):
    """Prompts user for all the info needed to generate a new plugin."""
    while True:
        msg = "What platform are you targeting? (Example: Fly.io) "
        plugin_config.platform_name = input(msg)

        msg = "What's the name of your plugin package? (Example: dsd-flyio) "
        while True:
            plugin_config.pkg_name = input(msg)
            if plugin_config.pkg_name.startswith("dsd-"):
                break
            else:
                print("The package name must start with `dsd-`.")

        msg = "Will your plugin support the --automate-all CLI arg? (yes/no) "
        response = input(msg)
        if response.lower() in ("yes", "y"):
            plugin_config.support_automate_all = True
        else:
            plugin_config.support_automate_all = False

        msg = "What name do you want to appear in the LICENSE file? "
        plugin_config.license_name = input(msg)

        # Review responses.
        msg = "\nHere's the information you've provided:"
        print(msg)
        print(f"  Platform name: {plugin_config.platform_name}")
        print(f"  Package name: {plugin_config.pkg_name}")
        print(f"  Supports --automate-all: {plugin_config.support_automate_all}")
        print(f"  Name on license: {plugin_config.license_name}")

        msg = "\nIs this information correct? (yes/no) "
        response = input(msg)
        if response.lower() in ("yes", "y"):
            break

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

def get_platform_name_lower(platform_name):
    """Return a lowercase version of the platform name."""
    return platform_name.lower().replace("-", "").replace("_", "").replace(".", "").replace(" ", "")