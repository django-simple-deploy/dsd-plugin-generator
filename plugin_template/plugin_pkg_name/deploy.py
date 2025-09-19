"""Manages all {{PlatformName}}-specific aspects of the deployment process.

Notes:
- ...
"""

import django_simple_deploy

from {{PluginName}}.platform_deployer import PlatformDeployer
from .plugin_config import plugin_config


@django_simple_deploy.hookimpl
def dsd_get_plugin_config():
    """Get platform-specific attributes needed by core."""
    return plugin_config


@django_simple_deploy.hookimpl
def dsd_deploy():
    """Carry out platform-specific deployment steps."""
    platform_deployer = PlatformDeployer()
    platform_deployer.deploy()
