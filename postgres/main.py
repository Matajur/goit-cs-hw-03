"""Module for creating tables, populating and querying the Postgres database"""

from src import creator, seed, query


def main():
    """
    Aggregating function for creating tables, populating and querying the Postgres database
    """
    creator.create_tables()
    seed.seed_all()
    query.make_query()


if __name__ == "__main__":
    main()
