Environment variables can be used to customize core Conreq features at boot.

## Environment Variables File

Editing Conreq's `settings.env` file is the recommended way of adding environment variables.

Here are some common locations of this file.

| Operating System                   | Location                                    |
| ---------------------------------- | ------------------------------------------- |
| Manually Run (Windows/Linux/MacOS) | `<CONREQ_DIR>/data/settings.env`            |
| Unraid Docker                      | `<UNRAID_APP_DATA_DIR>/conreq/settings.env` |
| Docker (Other)                     | `/config/settings.env`                      |

## System Variables

Variables can alternatively be set through the system's evironment variables.

_Note: These variables take priority over those stored in `settings.env`._

| Operating System                   | Location                                                                                                                                    |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Manually Run (Windows/Linux/MacOS) | [Varies depending on operating system.](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html)                          |
| Unraid Docker                      | Through a docker's `Edit` menu, click `Add another Path, Port, Variable, Label, or Device`, and then under `Config Type` select `Variable`. |
| Docker (Other)                     | [Add as a `-e` parameter.](https://docs.docker.com/compose/environment-variables/#set-environment-variables-in-containers)                  |

## Available Variables

| Variable                 | Default        | Example(s)                                                                                                                                                         | Description                                                                                                                                       |
| ------------------------ | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `BASE_URL`               | None           | `requests`                                                                                                                                                         | Used within URLs, such as `example.com/base-url`                                                                                                  |
| `HOME_URL`               | `home`         | `conreq`                                                                                                                                                           | Used within URLs, such as `example.com/base-url/home`                                                                                             |
| `LOG_LEVEL`              | `WARNING`      | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`                                                                                                                    | Used by Python's standard logging module.                                                                                                         |
| `CONREQ_ENV_PREFIX`      | `CONREQ`       | `COOL_VALUE`                                                                                                                                                       | All **system variables** will need to be prefixed by this value. Does not apply to the environment variables file.                                |
| `DEBUG_MODE`             | `True`         | `False`                                                                                                                                                            | Provides **sensitive** diagnostic information during development. Turned off by default in dockers.                                               |
| `SAFE_MODE`              | `False`        | `True`                                                                                                                                                             | Disables apps when attempting to boot Conreq.                                                                                                     |
| `DATA_DIR`               | `/data`        | `/config`, `/mnt/data`                                                                                                                                             | The location where Conreq will store its data files. Automatically set within dockers.                                                            |
| `SECURE_REFERRER_POLICY` | `no-referrer`  | `no-referrer`, `no-referrer-when-downgrade`, `origin`, `origin-when-cross-origin`, `same-origin`, `strict-origin`, `strict-origin-when-cross-origin`, `unsafe-url` | Value set within the HTTP referrer header.                                                                                                        |
| `ALLOWED_HOST`           | `*`            | `mywebsite.com`, `localhost`                                                                                                                                       | A host or domain that is allowed.                                                                                                                 |
| `ALLOWED_HOSTS`          | None           | `["192.168.0.199", "192.168.0.150"]`                                                                                                                               | Allows for listing multiple hosts or domains. Takes priority over `ALLOWED_HOST`.                                                                 |
| `DB_ENCRYPTION_KEY`      | Auto Generated | None                                                                                                                                                               | Automatically generated during first run. For security, this can be self migrated to an environment variable. **Make sure not to lose this key.** |
| `WEB_ENCRYPTION_KEY`     | Auto Generated | None                                                                                                                                                               | Automatically generated during first run. For security, this can be self migrated to an environment variable.                                     |
