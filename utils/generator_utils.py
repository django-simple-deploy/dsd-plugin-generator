"""Utility functions for generating a new plugin."""

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