import os

if os.environ.get("DB_ENGINE") == "MYSQL":
    import pymysql

    pymysql.install_as_MySQLdb()