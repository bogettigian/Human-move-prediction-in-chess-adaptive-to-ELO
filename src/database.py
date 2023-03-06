from pymongo import MongoClient


def get_database(connection_string: str, database_name: str, collection_name: str):
    client = MongoClient(connection_string)

    return client[database_name][collection_name]
