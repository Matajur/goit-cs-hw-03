"""Scripts with queries to the PostgreSQL database"""

from psycopg2 import DatabaseError

from src.db_connection import connection


def get_tasks_by_user_id(cursor):
    """
    Function providing tasks of a specific user by user_id
    """
    result = None
    sql = """
        SELECT title, description
        FROM tasks
        WHERE user_id=%s
        """
    user_id = input("Specify the user ID: ")
    user_id = int(user_id)
    cursor.execute(sql, (user_id,))
    result = cursor.fetchall()
    return result


def get_tasks_by_status(cursor):
    """
    Function providing tasks of a specific user by status
    """
    result = None
    sql = """
        SELECT t.title, t.description
        FROM tasks t
        JOIN status s ON s.id = t.status_id
        WHERE s.name=%s
        """
    task_status = input("Specify the task status ('new', 'in progress', 'completed'): ")
    cursor.execute(sql, (task_status,))
    result = cursor.fetchall()
    return result


def update_status(cursor):
    """
    Function to update the status of a specific task
    """
    sql = """
        UPDATE tasks
        SET status_id = (
            SELECT id FROM status WHERE name = %s
        )
        WHERE id = %s
        """
    task_id = input("Specify the task ID for the status update: ")
    task_id = int(task_id)
    new_status = input(
        "Provide a new status of the task ('new', 'in progress', 'completed'): "
    )
    cursor.execute(sql, (new_status, task_id))
    return "Task completed"


def get_users_with_no_tasks(cursor):
    """
    Function to get a list of users who do not have any tasks
    """
    sql = """
        SELECT fullname
        FROM users
        WHERE id NOT IN (
            SELECT user_id
            FROM tasks
        )
        """
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def add_new_task_for_user(cursor):
    """
    Function to add a new task for a specific user
    """
    user_id = input("Specify the user ID: ")
    task_title = input("Specify a title of the new task: ")
    task_description = input("Specify the task description: ")

    status_id_sql = """
        SELECT id
        FROM status
        WHERE name = 'new'
        """
    cursor.execute(status_id_sql)
    status_id = cursor.fetchone()[0]

    sql = """
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (%s, %s, %s, %s)
        """
    cursor.execute(sql, (task_title, task_description, status_id, user_id))

    return "Task completed"


def get_incompleted_tasks(cursor):
    """
    Function to get all tasks that have not yet been completed
    """
    sql = """
        SELECT tasks.title, tasks.description, status.name AS status
        FROM tasks
        JOIN status ON tasks.status_id = status.id
        WHERE status.name != 'completed';
        """
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def delete_task(cursor):
    """
    Function to delete a specific task
    """
    task_id = input("Specify the task ID: ")
    sql = """DELETE FROM tasks
        WHERE id = %s
        """
    cursor.execute(sql, (task_id,))
    return "Task completed"


def get_user_by_email(cursor):
    """
    Function to find users with a specific email
    """
    user_email = input("Specify the user email: ")
    sql = """
        SELECT fullname, email
        FROM users
        WHERE email LIKE %s;
        """
    cursor.execute(sql, (user_email,))
    result = cursor.fetchall()
    return result


def update_username(cursor):
    """
    Function to update username
    """
    user_id = input("Specify the user ID: ")
    new_fullname = input("Provide the new fullname: ")
    sql = """
        UPDATE users
        SET fullname = %s
        WHERE id = %s;
        """
    cursor.execute(sql, (new_fullname, user_id))
    return "Task completed"


def count_tasks_by_status(cursor):
    """
    Function to get the number of tasks for each status
    """
    sql = """
        SELECT status.name, COUNT(tasks.id) AS task_count
        FROM tasks
        JOIN status ON tasks.status_id = status.id
        GROUP BY status.name;
        """
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_tasks_by_email_domain(cursor):
    """
    Function to get tasks that are assigned to users with a specific email domain part
    """
    email_domain = input("Provide the email domain: ")
    sql = """
        SELECT tasks.title, tasks.description, users.fullname, users.email
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        WHERE users.email LIKE %s;
        """
    cursor.execute(sql, (email_domain,))
    result = cursor.fetchall()
    return result


def get_undescribed_tasks(cursor):
    """
    Function to get a list of tasks that do not have a description
    """
    sql = """
        SELECT title, description
        FROM tasks
        WHERE description IS NULL OR description = '';
        """
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_users_with_ongoing_tasks(cursor):
    """
    Function to get users and their tasks that are in progress
    """
    sql = """
        SELECT users.fullname, tasks.title, tasks.description, status.name AS status
        FROM users
        INNER JOIN tasks ON users.id = tasks.user_id
        INNER JOIN status ON tasks.status_id = status.id
        WHERE status.name = 'in progress';
        """
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def get_users_workload(cursor):
    """
    Function to get users and the number of their tasks
    """
    sql = """
        SELECT users.fullname, COUNT(tasks.id) AS task_count
        FROM users
        LEFT JOIN tasks ON users.id = tasks.user_id
        GROUP BY users.id, users.fullname, users.email
        ORDER BY users.id;
        """
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


TASKS = {
    1: ("Get all tasks of a specific user", get_tasks_by_user_id),
    2: ("Select a task by a certain status", get_tasks_by_status),
    3: ("Update the status of a specific task", update_status),
    4: ("Get a list of users without tasks", get_users_with_no_tasks),
    5: ("Add a new task for a specific user", add_new_task_for_user),
    6: ("Get all tasks that have not yet been completed", get_incompleted_tasks),
    7: ("Delete a specific task", delete_task),
    8: ("Find users with a specific email", get_user_by_email),
    9: ("Update username", update_username),
    10: ("Get the number of tasks for each status", count_tasks_by_status),
    11: (
        "Get tasks assigned to users with a specific email domain",
        get_tasks_by_email_domain,
    ),
    12: ("Get a list of tasks without description", get_undescribed_tasks),
    13: (
        "Select users and their tasks that are in progress",
        get_users_with_ongoing_tasks,
    ),
    14: ("Get users and the number of their tasks", get_users_workload),
}


def make_query():
    """
    Aggregation function of all queries that provides CLI
    interface for the user
    """
    while True:
        print()
        for number, task in TASKS.items():
            print(f"{number} - {task[0]}")
        print()
        choice = input("Type serial number of the request to perform ('0' to exit): ")

        try:
            choice = int(choice)
            if choice == 0:
                break
            if choice not in range(1, len(TASKS) + 1):
                print("Unsupported command")
            else:
                with connection() as conn:
                    cur = conn.cursor()
                    query_function = TASKS[choice][1]
                    try:
                        result = query_function(cur)
                        print("\n", result)
                    except DatabaseError as err:
                        print(err)
                    finally:
                        cur.close()
        except ValueError:
            print("Unsupported command")
            continue
    print("--> Queries are completed")


if __name__ == "__main__":
    make_query()
