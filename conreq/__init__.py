from conreq.utils.generic import get_str_from_env

if get_str_from_env("DB_ENGINE") == "MYSQL":
    import pymysql

    pymysql.install_as_MySQLdb()
