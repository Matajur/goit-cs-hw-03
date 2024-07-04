# Tier 2. Module 1: Computer Systems and Their Fundamentals

## Topic 5 - Working with relational databases
## Homework

### Task

Create a database for a task management system using PostgreSQL. The database should contain tables for users, job statuses, and jobs themselves. Perform the necessary queries in the database of the task management system.

### Instructions

1. Create tables in your PostgreSQL database as required. Use proper data types and constraints.

#### Database structure requirements:

**Table `users`**:

* `id`: Primary key, autoincrement (type `SERIAL`),
* `fullname`: Full name of the user (type `VARCHAR(100)`),
* `email`: The user's email address, which must be unique (type `VARCHAR(100)`).

**Table `status`**:

* `id`: Primary key, autoincrement (type `SERIAL`),
* `name`: Name of the status (type `VARCHAR(50)`), must be unique. We offer the following types `[('new',), ('in progress',), ('completed',)]`.

**Table `tasks`**:

* `id`: Primary key, autoincrement (type `SERIAL`),
* `title`: Name of the task (type `VARCHAR(100)`),
* `description`: Task description (type `TEXT`),
* `status_id`: Foreign key pointing to the `id` in the `status` table (type `INTEGER`),
* `user_id`: Foreign key pointing to the `id` in the `users` table (type `INTEGER`).

![DB structure](images/db.png)

2. Make sure that the `email` fields in the `users` table and `name` in the `status` table are unique.

3. Set up relationships between tables so that when a user is deleted, all his tasks are automatically deleted (cascade deletion).

4. Write a script for creating these tables.

5. Write a `seed.py` script in Python that will populate these tables with random values. Use the Faker library.

6. Using SQL, execute the following queries against the task management system database.

#### Requests to perform:

* __Get all tasks of a specific user__. Use `SELECT` to get jobs of a specific user by their `user_id`.
* __Select a task by a certain status__. Use a subquery to select tasks with a specific status, for example `'new'`.
* __Update the status of a specific task__. Change the status of a specific task to `'in progress'` or another status.
* __Get a list of users who do not have any tasks__. Use a combination of `SELECT`, `WHERE NOT IN` and a subquery.
* __Add a new task for a specific user__. Use `INSERT` to add a new task.
* __Get all tasks that have not yet been completed__. Select a task whose status is not 'completed'.
* __Delete a specific task__. Use `DELETE` to delete a task by its `id`.
* __Find users with a specific email__. Use `SELECT` with a `LIKE` condition to filter by email.
* __Update username__. Change the username using `UPDATE`.
* __Get the number of tasks for each status__. Use `SELECT`, `COUNT`, `GROUP BY` to group tasks by status.
* __Get tasks that are assigned to users with a specific email domain part__. Use `SELECT` with a `LIKE` condition in combination with a `JOIN` to select tasks assigned to users whose email contains a specific domain (eg `'%@example.com'`).
* __Get a list of tasks that do not have a description__. Select tasks that do not have a description.
* __Select users and their tasks that are `in progress`__. Use an `INNER JOIN` to get a list of users and their jobs with a certain status.
* __Get users and the number of their tasks__. Use `LEFT JOIN` and `GROUP BY` to select users and count their tasks.

### Acceptance criteria

1. Tables have been created and requirements for the database structure have been met.
2. The fields `email` in the `users` table and `name` in the `status` table are unique.
3. When a user is deleted, all his tasks are automatically deleted (cascade deletion).
4. The table creation script is written.
5. A `seed.py` script is written in Python, which will fill these tables with random values, using the Faker library.
6. All necessary requests in the database of the task management system have been completed.

#### Hint

Run the console script
`docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=yourpassword -d postgres`
to install a Postgres DB instance locally using Docker


## Topic 6 - Working with NoSQL and MongoDB
## Homework

### Task

Develop a Python script that uses the PyMongo library to implement basic CRUD (Create, Read, Update, Delete) operations in MongoDB.

### Instructions

1. Create the database as required.

__Requirements for the structure of the document__

Each document in your database should have the following structure:

`{                                                                            `
` "_id": ObjectId("60d24b783733b1ae668d4a77"),                                `
` "name": "barsik",                                                           `
` "age": 3,                                                                   `
` "features": ["walks in slippers", "allows himself to be stroked", "redhead"]`
`}                                                                            `

The document presents information about the cat, its `name`, `age` and `features`.

2. Develop a Python script `main.py` to perform the following tasks.

#### Tasks to be performed:

**Read**

* Implement a function to retrieve all records from a collection.
* Implement a function that allows the user to enter a cat's name and displays information about that cat.

**Update**

* Create a function that allows the user to update the age of a cat by name.
* Create a function that allows you to add a new characteristic to the list of `features` of a cat by name.

**Delete**

* Implement a function to remove an entry from the collection by the name of the animal.
* Implement a function to remove all records from a collection.

### Recommendations for implementation:

- Use MongoDB Atlas or a locally installed MongoDB instance using Docker.
- Install the PyMongo library via `pip` or another package manager like `pipenv` or `poetry`.
- Don't forget to handle possible exceptions when performing database operations.
- Make sure your functions are well commented and well structured.
- The use of Python virtual environment is encouraged to isolate project dependencies.

### Acceptance criteria

1. A database has been created and requirements regarding the structure of documents have been met.
2. All necessary operations have been implemented.
3. Handled possible exceptions when performing database operations.
4. Functions are clearly commented and well structured.


#### Hint

Run the console script
`docker run -d -p 27017:27017 --name yourdbname -e MONGO_INITDB_ROOT_USERNAME=yourusername -e MONGO_INITDB_ROOT_PASSWORD=yourpassword mongo`
to install a MongoDB instance locally using Docker
