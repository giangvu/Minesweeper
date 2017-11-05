from extensions import mongo
from bson.objectid import ObjectId


class DatabaseConnector:

    @classmethod
    def insert_game(cls, data):
        result = mongo.db.games.insert_one({'data': data})
        return str(result.inserted_id)

    @classmethod
    def update_game(cls, id, data):
        result = mongo.db.games.update_one({'_id': ObjectId(id)}, {"$set": {"data": data}})
        return result.modified_count

    @classmethod
    def get_game(cls, id):
        result = mongo.db.games.find_one({'_id': ObjectId(id)})
        return result