"""Configure the plugin to target a specific platform.

Usage:
$ python configure_plugin.py

That's all. You'll be asked a few questions, and this project will generate
a plugin with passing tests, that you can customize to target a specific platform
and deployment workflow.
"""

from utils import generator_utils
from utils.plugin_config import PluginConfig
from utils import cli

from pathlib import Path
import platform
import subprocess
import time
import shlex
import shutil
import sys


def generate_plugin(plugin_config, args):
    """Generate a new plugin."""
    plugin_config.validate()
    path_root = Path(__file__).parent

    # Make sure it's okay to write to the target directory.
    path_root_new = generator_utils.validate_target_dir(args, plugin_config, path_root)

    platform_name_lower = generator_utils.get_platform_name_lower(plugin_config.platform_name)

    generator_utils.build_new_plugin(plugin_config, path_root, path_root_new, platform_name_lower)
    generator_utils.show_summary()


if __name__ == "__main__":
    # Parse cli, get required info, and generate plugin.
    args = cli.parse_cli()
    plugin_config = PluginConfig
    generator_utils.get_plugin_info(plugin_config)

    generate_plugin(plugin_config, args)