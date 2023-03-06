import os
import time
import chess.pgn
import argparse

import database
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chess ingestion script.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--connection_string',
                        default='mongodb://localhost:27017', help="Connection string")
    parser.add_argument('-d', '--database', default='chess_base', help="Database name")
    parser.add_argument('-t', '--collection', default='moves', help="Collection name")
    parser.add_argument('-p', '--path', default='./../data/', help="Data source")
    args = vars(parser.parse_args())

    connection_string = args['connection_string']
    database_name = args['database']
    collection_name = args['collection']
    path = args['path']

    collection = database.get_database(connection_string, database_name, collection_name)

    start_time = time.time()
    total_records = 0
    saved_records = 0

    for file in os.listdir(path):
        if not file.endswith('.pgn'):
            continue

        pgn = open(path + file)

        game = chess.pgn.read_game(pgn)
        while game is not None:
            total_records += 1
            if utils.valid_game(game):
                game_parsed = utils.game_to_dict(game)
                collection.insert_one(game_parsed)
                saved_records += 1

            game = chess.pgn.read_game(pgn)

    print(f'Total games read: {total_records}')
    print(f'Total moves saved: {saved_records}')
    print(f'Time taken in seconds: {time.time() - start_time}')
