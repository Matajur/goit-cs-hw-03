"""Module that provides crud operations with MongoDB"""

from pymongo.errors import PyMongoError
from src.db_connection import collect, collection, db, db_name


def create_database_and_collection():
    """
    Function to create a collection inside of a database
    """
    try:
        if collect not in db.list_collection_names():
            db.create_collection(collect)
            print(f"Created {collect} collection in {db_name}")
        else:
            print(f"{collect} collection already exists in {db_name}")
    except PyMongoError as err:
        print(err)


def create_cat(db_collection):
    """
    Function with CLI interface to add a new cat to the collection
    """
    name = input("Enter the cat's name: ")
    age = input("Enter the cat's age: ")
    try:
        age = int(age)
    except ValueError:
        print("Age must be an integer")
    features = input("Enter the cat's featur (use ';' to split multiple entries): ")
    features = features.split(";")
    features = [f.strip() for f in features]
    cat = {"name": name, "age": age, "features": features}
    result = db_collection.insert_one(cat)
    print(f"Cat inserted with id: {result.inserted_id}")


def read_all_cats(db_collection):
    """
    Function to output all records from a collection
    """
    cats = db_collection.find()
    if cats:
        for cat in cats:
            print(cat)
    else:
        print(f"The collection {collect} has no records")


def read_cat_by_name(db_collection):
    """
    Function with CLI interface to search a cat by name
    """
    name = input("Enter the cat's name: ")
    cat = db_collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print(f"No cat found with name {name}")


def update_cat_age(db_collection):
    """
    Function with CLI interface to update the age of a specific cat
    """
    name = input("Enter the cat's name: ")
    new_age = input("Enter the cat's new age: ")
    try:
        new_age = int(new_age)
    except ValueError:
        print("Age must be an integer")
    result = db_collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count > 0:
        print(f"Updated age of {name} to {new_age}")
    else:
        print(f"No cat found with name {name}")


def add_feature_to_cat(db_collection):
    """
    Function with CLI interface to add a new feature for a specific cat
    """
    name = input("Enter the cat's name: ")
    new_feature = input("Enter the cat's new feature: ")
    result = db_collection.update_one(
        {"name": name}, {"$addToSet": {"features": new_feature}}
    )
    if result.matched_count > 0:
        print(f"Added feature '{new_feature}' to {name}")
    else:
        print(f"No cat found with name {name}")


def delete_cat_by_name(db_collection):
    """
    Function with CLI interface to delete a cat
    """
    name = input("Enter the cat's name: ")
    result = db_collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Deleted cat with name {name}")
    else:
        print(f"No cat found with name {name}")


def delete_all_cats(db_collection):
    """
    Function to delete all cats from the collection
    """
    result = db_collection.delete_many({})
    print(f"Deleted {result.deleted_count} cats")


TASKS = {
    1: ("Add a new cat to the collection", create_cat),
    2: ("Display all entries from the collection", read_all_cats),
    3: ("Search a cat by name", read_cat_by_name),
    4: ("Update the age of a specific cat", update_cat_age),
    5: ("Add a new feature for a specific cat", add_feature_to_cat),
    6: ("Delete a cat by name", delete_cat_by_name),
    7: ("Delete all cats from the collection", delete_all_cats),
}


def main():
    """
    Aggregation function of all crud operations that provides CLI
    interface for the user
    """
    create_database_and_collection()

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
                query_function = TASKS[choice][1]
                try:
                    query_function(collection)
                except PyMongoError as err:
                    print(err)
        except ValueError:
            print("Unsupported command")
            continue
    print("--> Queries are completed")


if __name__ == "__main__":
    main()
