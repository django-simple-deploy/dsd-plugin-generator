"""Test the plugin generator."""

import argparse
from argparse import Namespace

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
        # target_dir = tmp_path,
    )

    args = Namespace(target_dir=tmp_path)
    gp.generate_plugin(plugin_config, args)