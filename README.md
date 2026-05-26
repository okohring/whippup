# Stagecard

Stagecard is a WordPress plugin designed for creating, managing, and customizing program agendas, including individual speaker, event, and sponsor pages. 

Made with ChatGPT. 

## Current updater workflow

This repository hosts Stagecard releases for WordPress plugin updates.

Each client-ready version should have:

1. A matching plugin version in `program-agenda/program-agenda.php`.
2. A matching GitHub release tag, such as `v1.15.144`.
3. A plugin ZIP attached to the release, such as `program-agenda-v1-15-144.zip`.

The updater inside Stagecard checks this GitHub repository for the latest release and downloads the uploaded plugin ZIP asset.

## Important packaging note

The plugin ZIP must contain the plugin folder at the top level:

```text
program-agenda/
  program-agenda.php
  uninstall.php
  assets/
```

Do not use GitHub's automatic "Source code" ZIP as the WordPress plugin ZIP. Use the packaged plugin ZIP that contains the correct `program-agenda` folder.

## Release checklist

Before giving a version to a client:

1. Test the ZIP on a personal/staging WordPress site.
2. Confirm the version number is correct in the plugin header and class constant.
3. Upload the ZIP as a GitHub Release asset, or use the GitHub Actions packaging workflow once source files are in the repo.
4. Confirm WordPress detects the update on the test site.
5. Click through Programs, Events, Speakers, Sponsors, Mass Import, and public shortcodes.
