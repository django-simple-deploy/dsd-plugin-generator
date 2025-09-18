Plugin project structure
===

This document describes the overall project structure, and naming conventions within the project.

Example plugin
---

Consider a plugin that should be built from the following user input:

```sh
$ python generate_plugin.py
What platform are you targeting? (Example: Fly.io) GreenHost
What's the name of your plugin package? (Example: dsd-flyio) dsd-greenhost-high-traffic
Will your plugin support the --automate-all CLI arg? (yes/no) y
What name do you want to appear in the LICENSE file? Eric
```

This is a plugin that will support high-traffic sites on a platform called GreenHost.

Example project structure
---

Here's the project structure for the plugin that's generated:

```sh
$ tree -L 3 dsd-greenhost-high-traffic
dsd-greenhost-high-traffic
├── CHANGELOG.md
├── LICENSE
├── MANIFEST.in
├── README.md
├── developer_resources
│   └── README.md
├── dsd_greenhost_high_traffic
│   ├── __init__.py
│   ├── deploy.py
│   ├── deploy_messages.py
│   ├── platform_deployer.py
│   ├── plugin_config.py
│   └── templates
│       ├── dockerfile_example
│       └── settings.py
├── pyproject.toml
└── tests
    ├── conftest.py
    ├── e2e_tests
    │   ├── __init__.py
    │   ├── test_deployment.py
    │   └── utils.py
    └── integration_tests
        ├── reference_files
        └── test_greenhost_config.py

8 directories, 18 files
```

Notes
---

Here's what's important to note:

- The outer project directory is the name of the plugin package.
- The main project directory is the plugin package name, with hyphens replaced by underscores.
- The main integration test for configuration changes is named `test_<platform_name_lower>_config.py`.

Currently, plugin package names need to start with `dsd-`. This requirement will be removed before long.
