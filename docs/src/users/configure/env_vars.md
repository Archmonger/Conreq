???+ summary

    Environment variables can be used to customize core Conreq features at boot.

    The most common way of setting them is via the `settings.env` file, but they can alternatively be set via system variables.

---

## Using the `settings.env` File

!!! tip "Many settings from the interface use this config file!"

Editing Conreq's `settings.env` file is the recommended way of adding or modifying environment variables.

Here are some common locations of this file.

| Operating System    | Location                                   |
| ------------------- | ------------------------------------------ |
| Windows/Linux/MacOS | `<CONREQ_DIR>/data/settings.env`           |
| Unraid              | `<UNRAID_APPDATA_DIR>/conreq/settings.env` |
| Docker              | `/config/settings.env`                     |

## Using System Variables

!!! tip "These variables take priority over those stored in `settings.env`"

!!! tip "System variables must be prefixed by `CONREQ_ENV_PREFIX` (default: `CONREQ`)"

Variables can alternatively be set through the system's evironment variables.

| Operating System | Location |
| --- | --- |
| Windows/Linux/MacOS | [Varies depending on operating system.](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) |
| Unraid | Through a docker's `Edit` menu, click `Add another Path, Port, Variable, Label, or Device`, and then under `Config Type` select `Variable`. |
| Docker | Various methods. [See Docker documentation.](https://docs.docker.com/compose/environment-variables/#set-environment-variables-in-containers) |

## Common Variables

These are the common variables that aren't modifiable within Conreq interface.

| Variable | Default | Example(s) | Description |
| --- | --- | --- | --- |
| `DATA_DIR` | `/data` | `/config`, `/mnt/data` | The location where Conreq will store its data files. Automatically set within dockers. |
| `DB_ENCRYPTION_KEY` | Auto Generated | `None` | Automatically generated during first run. For security, this can be self migrated to an environment variable. **Make sure not to lose this key.** |
| `WEB_ENCRYPTION_KEY` | Auto Generated | `None` | Automatically generated during first run. For security, this can be self migrated to an environment variable. |
| `CONREQ_ENV_PREFIX` | `CONREQ` | `COOL_VALUE` | All **system variables** will need to be prefixed by this value. This setting does not apply to the environment variables file. |
