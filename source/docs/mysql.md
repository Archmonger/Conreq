1. Set up a MySQL database (ex. a MySQL Docker)

2. Create a file within your Conreq data directory create a MySQL configuration file (ex. `mysql.cnf`). At minimum you must include the following:

   - If you have to customize other parameters, such as the port, take a look at [MySQL's configuration file documentation](https://dev.mysql.com/doc/refman/8.0/en/option-files.html).

```python
[client]
database = conreq
user = db_username
password = db_password
host = 192.168.86.200
default-character-set = utf8
```

3. Within your Conreq environment settings, set your `DB_ENGINE ` variable to `MYSQL`, and your `MYSQL_CONFIG_FILE` variable to the path where your configuration file is stored (ex. `/config/mysql.cnf`)

   - If using Unraid/Docker, add this as a Docker Variable. If you are self hosting Conreq on your own operating system, consider searching searching "How to set environment variables in _... Windows 10_"
