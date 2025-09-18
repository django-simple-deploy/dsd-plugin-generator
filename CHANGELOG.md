Changelog: dsd-generator
===

For inspiration and motivation, see [Keep a CHANGELOG](https://keepachangelog.com/en/0.3.0/).

Versions are informal at this point, since this is not released as a package. Version numbers correspond to Git tags.

1.0 - Stable release
---

This series corresponds to 1.x releases of django-simple-deploy.

### 1.1.0

#### External changes

- Uses plugin name with underscores for main source code directory.
- Document project structure and naming conventions.
- Document e2e tests.
- E2e test supports CLI arg `--setup-plugins-only`, which sets up a django-simple-deploy develop environment in a temp test location with numerous freshly-generated plugins. It does not run any tests. These resources can be examined, or copied to a more stable location for more extensive development and testing.

#### Internal changes

- Restructure e2e tests to use fixtures.
- In e2e tests, use independent tests for each test plugin.
