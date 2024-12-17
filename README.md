# {{PackageName}}

A plugin for deploying Django projects to {{PlatformName}}, using django-simple-deploy.

For full documentation, see the documentation for [django-simple-deploy](https://django-simple-deploy.readthedocs.io/en/latest/).

Usage notes
---

- Download this repo; don't clone it.
- Run `python configure_plugin.py`, and answer the small set of prompts:

```sh
$ python configure_plugin.py 
What platform are you targeting? (Example: Fly.io) CodeRed
What's the name of your plugin package? (Example: dsd-flyio) dsd-codered
Will your plugin support the --automate-all CLI arg? (yes/no) yes
What name do you want to appear in the LICENSE file? Eric Matthes

Here's the information you've provided:
  Platform name: CodeRed
  Package name: dsd-codered
  Supports --automate-all: True
  Name on license: Eric Matthes

Is this information correct? (yes/no) y

Okay to write new project at /Users/eric/projects/dsd-codered? (yes/no) y


Thank you. Configuring plugin...
...
```

- Most files are filled in for you based on the information you provide.
- Fill out the messages in *deploy_messages.py*.
- Write methods in *platform_deployer.py* to carry out configuration for the target platform.
- For more information about writing a plugin, see the [Plugins](https://django-simple-deploy.readthedocs.io/en/latest/plugins/) section of the django-simple-deploy documentation.

Note
---

This README serves as a template README for new plugins. The `{{PackageName}}` placeholder at the top of this file is replaced with the name of the new plugin.
