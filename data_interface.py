#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime

from pymongo import MongoClient, DESCENDING


class DataInterface:
    db = None

    def __init__(self, db):
        self.db = getattr(MongoClient(), db)

    def store(self, collection, data):
        self.db[collection].insert_one(data)

    def get_by_line(self, line):
        aggregation_string = [{
            '$match': {
                'vehicles.Line': line
            }
        },
        {
            '$project': {
                'vehicles': {
                    '$filter': {
                        'input': '$vehicles',
                        'as': 'vehicle',
                        'cond': {
                            '$eq': ['$$vehicle.Line', line]
                        }
                    }
                },
                'last_updated': 1,
            }
        },
        ]
        data = list(self.db.mhd_data.aggregate(aggregation_string))
        for i in range(len(data)):
            data[i]['last_updated'] = datetime.datetime.strptime(data[i]['last_updated'], '%Y/%m/%d %H:%M:%S')

        return data

    def get_one(self, collection):
        return self.db[collection].find_one({}, {"_id": 0}, sort=[('_id', DESCENDING)])

    def get_stop_key(self, stop_name):
        for key, value in self.db.stops.find_one().items():
            try:
                if value['Name'] == stop_name:
                    return key
            except TypeError:
                continue