        # This is a dummy block to write a fly.toml file with only the 
        # text needed to pass the test_custom_cli_arg.py test. It is 
        # not a valid fly.toml file.
        path = dsd_config.project_root / "fly.toml"

        contents = "Dummy fly.toml file."
        contents += '\n\nThe text \n\nsize = "shared-cpu-2x"\n\n appears in this file.\n'
        plugin_utils.add_file(path, contents)