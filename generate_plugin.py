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


def generate_plugin(plugin_config, args):
    """Generate a new plugin."""
    plugin_config.validate()
    generator_utils.build_new_plugin(args, plugin_config)
    generator_utils.show_summary()


if __name__ == "__main__":
    # Parse cli, get required info, and generate plugin.
    args = cli.parse_cli()
    plugin_config = PluginConfig()
    generator_utils.get_plugin_info(plugin_config)

    generate_plugin(plugin_config, args)