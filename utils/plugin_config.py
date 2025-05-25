"""Stores config info required to generate a new plugin."""

from dataclasses import dataclass


@dataclass
class PluginConfig:
    platform_name: str = ""
    plugin_name: str = ""
    support_automate_all: bool = False
    license_name: str = ""
