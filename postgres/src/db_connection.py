"""PostgreSQL connection module"""

import configparser
from contextlib import contextmanager
from psycopg2 import connect, DatabaseError

config = configparser.ConfigParser()
config.read("config.ini")

username = config.get("DB", "user")
password = config.get("DB", "pass")
domain = config.get("DB", "domain")
db_name = config.get("DB", "db_name")


@contextmanager
def connection():
    """
    Function that provides a connection to the PostgreSQL database
    """
    conn = None
    try:
        conn = connect(
            host=domain, user=username, database=db_name, password=password
        )
        yield conn
        conn.commit()
    except DatabaseError as err:
        print(err)
        conn.rollback() # type: ignore
    finally:
        if conn is not None:
            conn.close()
