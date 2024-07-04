"""Script for filling PostgreSQL tables with data"""

from random import randint

from faker import Faker
from psycopg2 import DatabaseError

from src.db_connection import connection

NUMBER_TASKS = randint(30, 50)
NUMBER_USERS = randint(5, 8)
STATUS = ("new", "in progress", "completed")

fake = Faker()


def seed_users(cursor):
    """
    Function of seeding random users in the dedicated table of the database
    """
    sql = """
    INSERT INTO users(fullname, email) VALUES(%s, %s);
    """
    for _ in range(NUMBER_USERS):
        cursor.execute(sql, (fake.name(), fake.email()))


def seed_status(cursor):
    """
    Function of seeding statuses in the dedicated table of the database
    """
    sql = """
    INSERT INTO status(name) VALUES(%s);
    """
    for status in STATUS:
        cursor.execute(sql, (status,))


def seed_tasks(cursor):
    """
    Function of seeding tasks for users
    """
    sql = """
    INSERT INTO tasks(title, description, status_id, user_id) VALUES(%s, %s, %s, %s);
    """
    for _ in range(NUMBER_TASKS):
        cursor.execute(
            sql,
            (
                fake.sentence(nb_words=6),
                fake.text(max_nb_chars=200),
                randint(1, len(STATUS)),
                randint(1, NUMBER_USERS),
            ),
        )


def seed_all():
    """
    Function for seeding database tables with random data
    """
    with connection() as conn:
        try:
            if conn is not None:
                cur = conn.cursor()
                seed_users(cur)
                seed_status(cur)
                seed_tasks(cur)
                cur.close()
                print("--> Seeding operation is successful")
            else:
                print("--> Error! Cannot create the database connection")
        except DatabaseError as err:
            print(err)


if __name__ == "__main__":
    seed_all()
