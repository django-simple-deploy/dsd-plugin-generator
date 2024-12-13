"""Manages all {{PlatformName}}-specific aspects of the deployment process.

Notes:
- 
"""

import sys, os, re, json
from pathlib import Path

from django.utils.safestring import mark_safe

import requests

from . import deploy_messages as platform_msgs

from simple_deploy.management.commands.utils import plugin_utils
from simple_deploy.management.commands.utils.plugin_utils import sd_config
from simple_deploy.management.commands.utils.command_errors import SimpleDeployCommandError


class PlatformDeployer:
    """Perform the initial deployment to {{PlatformName}}

    If --automate-all is used, carry out an actual deployment.
    If not, do all configuration work so the user only has to commit changes, and ...
    """

    def __init__(self):
        self.templates_path = Path(__file__).parent / "templates"

    # --- Public methods ---

    def deploy(self, *args, **options):
        """Coordinate the overall configuration and deployment."""
        plugin_utils.write_output("\nConfiguring project for deployment to {{PlatformName}}...")

        self._validate_platform()
        self._prep_automate_all()

        # Configure project for deployment to {{PlatformName}}

        self._conclude_automate_all()
        self._show_success_message()

    # --- Helper methods for deploy() ---

    def _validate_platform(self):
        """Make sure the local environment and project supports deployment to {{PlatformName}}.

        Returns:
            None
        Raises:
            SimpleDeployCommandError: If we find any reason deployment won't work.
        """
        pass


    def _prep_automate_all(self):
        """Take any further actions needed if using automate_all."""
        pass


    def _conclude_automate_all(self):
        """Finish automating the push to {{PlatformName}}.

        - Commit all changes.
        - ...
        """
        # Making this check here lets deploy() be cleaner.
        if not sd_config.automate_all:
            return

        plugin_utils.commit_changes()

        # Push project.
        plugin_utils.write_output("  Deploying to {{PlatformName}}...")

        # Should set self.deployed_url, which will be reported in the success message.
        pass

    def _show_success_message(self):
        """After a successful run, show a message about what to do next.

        Describe ongoing approach of commit, push, migrate.
        """
        if sd_config.automate_all:
            msg = platform_msgs.success_msg_automate_all(self.deployed_url)
        else:
            msg = platform_msgs.success_msg(log_output=sd_config.log_output)
        plugin_utils.write_output(msg)
