"""Stores config info required to generate a new plugin."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class PluginConfig:
    platform_name: str = ""
    pkg_name: str = ""
    support_automate_all: bool = False
    license_name: str = ""
    target_dir: Path = ""

    def validate(self):
        """Validate the plugin config."""
        assert self.platform_name
        assert self.pkg_name.startswith("dsd-")