import argparse
import os
import time
import numpy as np

import database
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess CSV generator script.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--connection_string',
                        default='mongodb://localhost:27017', help="Connection string")
    parser.add_argument('-d', '--database', default='chess_base', help="Database name")
    parser.add_argument('-t', '--collection', default='moves', help="Collection name")
    parser.add_argument('-p', '--path', default='./../data/csv/data.csv', help="Data output")
    args = vars(parser.parse_args())

    connection_string = args['connection_string']
    database_name = args['database']
    collection_name = args['collection']
    path = args['path']

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    collection = database.get_database(connection_string, database_name, collection_name)
    filter = {}

    start_time = time.time()
    total_records = 0
    saved_records = 0

    with open(path, 'w') as f:
        np.savetxt(f, utils.columns(), delimiter=',', fmt='%s')

    for game_dict in collection.find(filter):
        data, records = utils.game_dict_to_array(game_dict)
        total_records += 1
        saved_records += records

        with open(path, 'a') as f:
            np.savetxt(f, data, delimiter=',', fmt='%s')

    print(f'Total games read: {total_records}')
    print(f'Total games saved: {saved_records}')
    print(f'Time taken in seconds: {time.time() - start_time}')
