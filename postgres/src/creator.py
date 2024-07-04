"""Script for creating tables in PostgreSQL"""

from psycopg2 import DatabaseError

from src.db_connection import connection

create_table_users = """
-- Table: users
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  fullname VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL
);
"""

create_table_status = """
-- Table: status
DROP TABLE IF EXISTS status CASCADE;
CREATE TABLE status (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL CHECK (name IN ('new', 'in progress', 'completed'))
);
"""

create_table_tasks = """
-- Table: tasks
DROP TABLE IF EXISTS tasks CASCADE;
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100),
  description TEXT,
  status_id INTEGER REFERENCES status (id),
  user_id INTEGER REFERENCES users (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
"""


def create_table(db_connection, sql: str):
    """
    Function for execution of SQL query
    """
    try:
        cur = db_connection.cursor()
        cur.execute(sql)
        cur.close()
    except DatabaseError as err:
        print(err)


def create_tables():
    """
    Function for execution of multiple SQL queries
    """
    with connection() as conn:
        if conn is not None:
            create_table(conn, create_table_users)
            create_table(conn, create_table_status)
            create_table(conn, create_table_tasks)
            print("--> All tables created")
        else:
            print("--> Error! Cannot create the database connection")


if __name__ == "__main__":
    create_tables()
