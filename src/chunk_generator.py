import argparse
import os
import time

import database
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess Chunk generator script.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--connection_string',
                        default='mongodb://localhost:27017', help="Connection string")
    parser.add_argument('-d', '--database', default='chess_base', help="Database name")
    parser.add_argument('-t', '--collection', default='moves', help="Collection name")
    parser.add_argument('-p', '--path', default='./../data/csv/data.pgn', help="Data output")
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
    saved_records = 0

    if not os.path.exists(path):
        for game_dict in collection.find(filter).limit(1000):
            game = utils.dict_to_game(game_dict)
            saved_records += 1

            with open(path, "a") as f:
                f.write(game.__str__() + '\n\n')
        print(f'Total games saved: {saved_records}')

    result = os.system(f'bash ./../libs/trainingdata-tool/trainingdata-tool -v -files-per-dir 5000 {path}')
    if result != 0:
        print('Error: trainingdata-tool call failed')

    print(f'Time taken in seconds: {time.time() - start_time}')
