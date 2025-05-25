"""Test the plugin generator."""

import argparse
from argparse import Namespace
from pathlib import Path
from filecmp import dircmp

import pytest

from utils.plugin_config import PluginConfig
import generate_plugin as gp


# @pytest.fixture(tmp_dir):
# def get_tmp_dir():
#     tmp_path = tmp_path_factory.mktemp("sample_code")
#     print(f"\nWriting plugin to: {tmp_path.as_posix()}")

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

    assert plugin_dirs_match(path_test_plugin, path_ref_dir)


# --- Helper functions ---

def plugin_dirs_match(test_dir, ref_dir):
    """Check that a test plugin dir and a reference plugin dir match, recursively."""
    dc = dircmp(test_dir, ref_dir, ignore=[".DS_Store", "__pycache__"], shallow=False)
    check_dc(dc)
    return True

def check_dc(dc):
    assert not dc.left_only
    assert not dc.right_only
    assert not dc.diff_files
    assert not dc.funny_files

    for dirname, dc in dc.subdirs.items():
        check_dc(dc)