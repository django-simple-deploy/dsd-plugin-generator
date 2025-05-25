"""Test the plugin generator."""

import argparse
from argparse import Namespace
from pathlib import Path
from filecmp import dircmp

import pytest

from utils.plugin_config import PluginConfig
import generate_plugin as gp


def test_no_spaces_anywhere(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("sample_plugin")
    print(f"\nWriting plugin to: {tmp_path.as_posix()}")

    plugin_config = PluginConfig(
        platform_name = "NewFly",
        pkg_name = "dsd-newfly",
        support_automate_all = True,
        license_name = "eric",
    )

    args = Namespace(target_dir=tmp_path)
    gp.generate_plugin(plugin_config, args)

    path_ref_dir = Path(__file__).parent / "reference_files" / "dsd-newfly"
    path_test_plugin = tmp_path / "dsd-newfly"

    dc = dircmp(path_test_plugin, path_ref_dir, ignore=[".DS_Store", "__pycache__"])
    assert_dirs_match(dc)


# --- Helper functions ---

def assert_dirs_match(dc):
    """Check there are no differences in the dircmp object, and recurse all subdirs."""
    assert not dc.left_only
    assert not dc.right_only
    assert not dc.diff_files
    assert not dc.funny_files

    for dirname, dc in dc.subdirs.items():
        assert_dirs_match(dc)