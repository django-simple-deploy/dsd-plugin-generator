"""Test the plugin generator."""

import pytest

from utils.plugin_config import PluginConfig


# @pytest.fixture(tmp_dir):
# def get_tmp_dir():
#     tmp_path = tmp_path_factory.mktemp("sample_code")
#     print(f"\nWriting plugin to: {tmp_path.as_posix()}")

def test_no_spaces_anywhere(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("sample_plugin")
    print(f"\nWriting plugin to: {tmp_path.as_posix()}")

