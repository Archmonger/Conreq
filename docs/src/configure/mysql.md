1.  Install and run MySQL using your preferred method.

2.  Create a file within your Conreq data directory create a MySQL configuration file (`mysql.cnf`). At minimum you must include the following...

    ```toml
    [client]
    database = conreq
    user = db_username
    password = db_password
    host = 192.168.86.200
    default-character-set = utf8
    ```

    _Take a look at MySQL's "Options Files" docs for all available parameters._

3.  Set your `DB_ENGINE ` variable to `MYSQL` and your `MYSQL_CONFIG_FILE` variable to the path to your `mysql.cnf` file.

    _If using Unraid/Docker, add this as a Docker variable. Otherwise, search "How to set environment variables in ... Windows 10"_
