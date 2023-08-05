from config import Configuration

from pymongo import MongoClient


class MongoWorker:

    client = MongoClient(Configuration.mongo_db_uri)

    # Get the database
    db = client['ai-bot-db']
    users_container = db['users']

    @staticmethod
    def get_jsons(container, parameters):
        return container.find_all(parameters)

    @staticmethod
    def add_json(container, json):
        return container.insert_one(json)

    @staticmethod
    def update_json(container, parameters, updated_json):
        return container.update_one(parameters, {'$set': updated_json})

    @staticmethod
    def get_users(parameters):
        return MongoWorker.get_jsons(
            container=MongoWorker.users_container,
            parameters=parameters
        )

    @staticmethod
    def add_user(user_json):
        return MongoWorker.add_json(
            container=MongoWorker.users_container,
            json=user_json
        )

    @staticmethod
    def update_user_json(parameters, updated_json):
        return MongoWorker.update_json(
            container=MongoWorker.users_container,
            parameters=parameters,
            updated_json=updated_json
        )


