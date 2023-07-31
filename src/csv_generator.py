import argparse
import json
import os
import time
import numpy as np

import database
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess CSV generator script.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--connection_string', default='mongodb://localhost:27017', help="Connection string")
    parser.add_argument('-d', '--database', default='chess-mongo', help="Database name")
    parser.add_argument('-t', '--collection', default='moves', help="Collection name")
    parser.add_argument('-p', '--path', default='./../data/csv/data.csv', help="Data output")

    parser.add_argument('-f', '--filter', default={}, type=json.loads, help="Database query filter")
    parser.add_argument('-s', '--skip', default=0, type=int, help="Database query skip")
    parser.add_argument('-l', '--limit', default=0, type=int, help="Database query limit")
    args = vars(parser.parse_args())

    connection_string = args['connection_string']
    database_name = args['database']
    collection_name = args['collection']
    path = args['path']

    db_filter = args['filter']
    db_skip = args['skip']
    db_limit = args['limit']

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    start_time = time.time()
    total_records = 0
    saved_records = 0

    filter = {}
    collection = database.get_database(connection_string, database_name, collection_name)
    with open(path, 'w') as f:
        np.savetxt(f, utils.columns(), delimiter=',', fmt='%s')

    for game_dict in collection.find(db_filter).sort({'$natural': 1}).skip(db_skip).limit(db_limit):
        data, records = utils.game_dict_to_array(game_dict)
        total_records += 1
        saved_records += records
        if total_records % 10000 == 0:
            print(f'Games read: {total_records}')

        with open(path, 'a') as f:
            np.savetxt(f, data, delimiter=',', fmt='%s')

    print(f'Total games read: {total_records}')
    print(f'Total games saved: {saved_records}')
    print(f'Time taken in seconds: {time.time() - start_time}')
