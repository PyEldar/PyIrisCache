from pymongo import MongoClient, DESCENDING


class DataInterface:
    db = None

    def __init__(self, db):
        self.db = getattr(MongoClient(), db)

    def store(self, collection, data):
        self.db[collection].insert_one(data)

    def get_by_line(self, line):
        aggregation_string = [{
            "$match": {
                'vehicles.Line': line
            }
        },
        {
            "$project": {
                "vehicles": {
                    "$filter": {
                        "input": '$vehicles',
                        "as": 'vehicle',
                        "cond": {
                            "$eq: ['$$vehicle.Line', line]"
                        }
                    }
                },
                "last_updated": 1,
            }
        },
        ]
        return list(self.db.mhd_data.aggregate(aggregation_string))

    def get_one(self, collection):
        return self.db[collection].find_one({}, {"_id": 0}, sort=[('_id', DESCENDING)])
